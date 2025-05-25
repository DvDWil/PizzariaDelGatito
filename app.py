from flask import Flask, render_template, request, redirect, url_for, session
from models.pedidos import db
from models.pedidos import Cliente, Pedido  # Agora importamos db separadamente
from datetime import datetime
import os
from models.funcionario import Funcionario
from collections import deque
from flask import jsonify

fila_pedidos = deque()
pilha_historico = []

def bubble_sort_clientes(clientes):
    n = len(clientes)
    for i in range(n):
        for j in range(0, n-i-1):
            if clientes[j].nome > clientes[j+1].nome:
                clientes[j], clientes[j+1] = clientes[j+1], clientes[j]

def quick_sort_pedidos(pedidos):
    if len(pedidos) <= 1:
        return pedidos
    else:
        pivot = pedidos[0]
        menores = [p for p in pedidos[1:] if p.preco_total <= pivot.preco_total]
        maiores = [p for p in pedidos[1:] if p.preco_total > pivot.preco_total]
        return quick_sort_pedidos(menores) + [pivot] + quick_sort_pedidos(maiores)

app = Flask(__name__, static_folder='static')
app.secret_key = "1234"

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pizzaria.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o db com o app
db.init_app(app)

with app.app_context():
    db.create_all()

from sqlalchemy import text

with app.app_context():
    db.create_all()
    
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE pedido ADD COLUMN status VARCHAR(20)'))
            conn.commit()
        print("Coluna 'status' adicionada com sucesso!")
    except Exception as e:
        print(f"Coluna 'status' já existe ou erro: {e}")
    
    try:
        pedidos_sem_status = Pedido.query.filter(Pedido.status.is_(None)).all()
        for pedido in pedidos_sem_status:
            pedido.status = 'pendente'
        db.session.commit()
        if pedidos_sem_status:
            print(f"Status 'pendente' definido para {len(pedidos_sem_status)} pedidos existentes")
    except Exception as e:
        print(f"Erro ao atualizar status dos pedidos: {e}")
        db.session.rollback()

sabores_disponiveis = ["Calabresa", "Mussarela", "Portuguesa", "Frango com Catupiry", "4 Queijos", "Bacon Supreme", "Pepperoni", "Vegetariana", "Especial da Casa", "Chocolate", "Chocolate com Morango", "Oreo", "Romeu e Julieta", "Banana com Canela"]

precos_pizza = {
    "Calabresa": {"pequena": 20.00, "media": 30.00, "grande": 40.00},
    "Mussarela": {"pequena": 18.00, "media": 28.00, "grande": 38.00},
    "Portuguesa": {"pequena": 22.00, "media": 32.00, "grande": 42.00},
    "Frango com Catupiry": {"pequena": 21.00, "media": 31.00, "grande": 41.00},
    "4 Queijos": {"pequena": 24.00, "media": 34.00, "grande": 44.00},
    "Bacon Supreme": {"pequena": 37.00, "media": 47.00, "grande": 57.00},
    "Pepperoni": {"pequena": 36.00, "media": 46.00, "grande": 56.00},
    "Vegetariana": {"pequena": 35.00, "media": 45.00, "grande": 55.00},
    "Carne Seca com Catupiry": {"pequena": 40.00, "media": 50.00, "grande": 60.00},
    "Especial da Casa": {"pequena": 42.00, "media": 52.00, "grande": 62.00},
    "Chocolate": {"pequena": 32.00, "media": 42.00, "grande": 52.00},
    "Chocolate com Morango": {"pequena": 35.00, "media": 45.00, "grande": 55.00},
    "Oreo": {"pequena": 32.00, "media": 42.00, "grande": 52.00},
    "Romeu e Julieta": {"pequena": 35.00, "media": 45.00, "grande": 55.00},
    "Banana com Canela": {"pequena": 33.00, "media": 43.00, "grande": 53.00}
}

bebidas_disponiveis = {
    "Coca-Cola": {"lata": 5.00, "600ml": 7.00, "2L": 10.00},
    "Guaraná": {"lata": 4.50, "600ml": 6.50, "2L": 9.00},
    "Suco": {"300ml": 6.00, "500ml": 8.00},
    "Água": {"500ml": 3.00}
}

fretes = {
    "Asa Sul": 5.00,
    "Asa Norte": 5.00,
    "Cruzeiro": 10.00,
    "Sudoeste": 10.00,
    "Octogonal": 15.00,
    "Guará": 15.00,
    "Retirar na Loja": 0.00
}

# Criando a hierarquia da pizzaria
dono = Funcionario("Fernanda", "Dona da Pizzaria")

gerente = Funcionario("Isabely", "Gerente")
chefe_cozinha = Funcionario("David", "Chefe de Cozinha")
entregador1 = Funcionario("Rafael", "Entregador")
entregador2 = Funcionario("Sofia", "Entregador")

atendente1 = Funcionario("Ana", "Atendente")
atendente2 = Funcionario("Lucas", "Atendente")

pizzaiolo1 = Funcionario("João", "Pizzaiolo")
pizzaiolo2 = Funcionario("Pedro", "Pizzaiolo")

dono.adicionar_subordinado(gerente)
dono.adicionar_subordinado(chefe_cozinha)
dono.adicionar_subordinado(entregador1)
dono.adicionar_subordinado(entregador2)

gerente.adicionar_subordinado(atendente1)
gerente.adicionar_subordinado(atendente2)

chefe_cozinha.adicionar_subordinado(pizzaiolo1)
chefe_cozinha.adicionar_subordinado(pizzaiolo2)

def encontrar_raiz(funcionario):
    return f"{funcionario.cargo} - {funcionario.nome}"

def encontrar_nos_internos(funcionario, internos=None):
    if internos is None:
        internos = []
    if funcionario.subordinados:
        internos.append(f"{funcionario.cargo} - {funcionario.nome}")
        for sub in funcionario.subordinados:
            encontrar_nos_internos(sub, internos)
    return internos

def encontrar_nos_folhas(funcionario, folhas=None):
    if folhas is None:
        folhas = []
    if not funcionario.subordinados:
        folhas.append(f"{funcionario.cargo} - {funcionario.nome}")
    else:
        for sub in funcionario.subordinados:
            encontrar_nos_folhas(sub, folhas)
    return folhas

def calcular_preco(carrinho):
    return sum(item["preco_total"] for item in carrinho)

@app.route('/')
def home():
    return render_template('index.html')

# Adicione essas rotas ao seu app.py

@app.route('/mandar_entrega/<int:numero_pedido>')
def mandar_entrega(numero_pedido):
    try:
        pedido = Pedido.query.filter_by(numero_pedido=numero_pedido).first()
        
        if pedido:
            pedido.status = 'em_entrega'
            db.session.commit()
            return redirect(url_for('lista_pedidos'))
        else:
            return "Pedido não encontrado", 404
    except Exception as e:
        db.session.rollback()
        print("Erro ao mandar pedido para entrega:", str(e))
        return "Ocorreu um erro ao processar a solicitação", 500

@app.route('/entregar_pedido/<int:numero_pedido>')
def entregar_pedido(numero_pedido):
    try:
        pedido = Pedido.query.filter_by(numero_pedido=numero_pedido).first()
        
        if pedido:
            pedido.status = 'entregue'
            db.session.commit()
            return redirect(url_for('lista_pedidos'))
        else:
            return "Pedido não encontrado", 404
    except Exception as e:
        db.session.rollback()
        print("Erro ao marcar pedido como entregue:", str(e))
        return "Ocorreu um erro ao processar a solicitação", 500

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        carrinho = session.get("carrinho", [])

        sabor1 = request.form.get("sabor1")
        sabor2 = request.form.get("sabor2")
        quantidade_pizza = int(request.form.get("quantidade", 0))

        if sabor1 and quantidade_pizza > 0:
            tamanho_pizza = request.form.get("tamanho")
            tipo = "Inteira" if sabor2 == "Nenhum" else "Meia a Meia"

            if sabor2 != "Nenhum":
                preco1 = precos_pizza.get(sabor1, {}).get(tamanho_pizza, 0)
                preco2 = precos_pizza.get(sabor2, {}).get(tamanho_pizza, 0)
                preco_unitario = (preco1 + preco2) / 2
            else:
                preco_unitario = precos_pizza.get(sabor1, {}).get(tamanho_pizza, 0)

            carrinho.append({
                "tipo": "pizza",
                "sabor1": sabor1,
                "sabor2": sabor2 if sabor2 != "Nenhum" else "",
                "quantidade": quantidade_pizza,
                "tipo_pizza": tipo,
                "tamanho": tamanho_pizza,
                "preco_unitario": preco_unitario,
                "preco_total": preco_unitario * quantidade_pizza
            })

        for bebida, tamanhos in bebidas_disponiveis.items():
            for tamanho in tamanhos:
                qtd_key = f"{bebida.lower().replace(' ', '_')}_{tamanho.lower()}_qtd"
                quantidade = int(request.form.get(qtd_key, 0))
                if quantidade > 0:
                    carrinho.append({
                        "tipo": "bebida",
                        "nome": bebida,
                        "tamanho": tamanho,
                        "quantidade": quantidade,
                        "preco_unitario": bebidas_disponiveis[bebida][tamanho],
                        "preco_total": bebidas_disponiveis[bebida][tamanho] * quantidade
                    })

        session["carrinho"] = carrinho
        return redirect(url_for('carrinho'))

    return render_template('menu.html', sabores=sabores_disponiveis, bebidas=bebidas_disponiveis)

@app.route('/carrinho')
def carrinho():
    carrinho = session.get("carrinho", [])

    local_entrega = request.args.get("local_entrega", "Retirar na Loja")
    frete = fretes.get(local_entrega, 0.00)

    total_com_frete = calcular_preco(carrinho) + frete

    return render_template('carrinho.html', carrinho=carrinho, total_com_frete=total_com_frete, frete=frete, local_entrega=local_entrega)

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    try:
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        local_entrega = request.form.get("local_entrega")

        if not session.get("carrinho"):
            return redirect(url_for('menu'))

        # Verifique se o carrinho tem itens
        print("Itens no carrinho:", session["carrinho"])  # Isso aparecerá no terminal

        preco_pizzas = calcular_preco(session["carrinho"])
        frete = fretes.get(local_entrega, 0.00)
        preco_total = preco_pizzas + frete

        # Tratamento do cliente
        cliente = Cliente.query.filter_by(telefone=telefone).first()
        if not cliente:
            cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone, email=email)
            db.session.add(cliente)
            db.session.commit()
        
        # Usar diretamente a lista do carrinho como JSON (SQLAlchemy/SQLite suporta isso)
        numero_pedido = Pedido.query.count() + 1
        
        pedido = Pedido(
            numero_pedido=numero_pedido,
            cliente=cliente,  # Nosso __init__ modificado lidará com isso corretamente
            itens=session["carrinho"],  # SQLAlchemy cuidará da conversão para JSON
            preco_total=preco_total,
            local_entrega=local_entrega
        )
        
        db.session.add(pedido)
        db.session.commit()
        fila_pedidos.append(pedido.numero_pedido)

        
        session.pop("carrinho", None)
        return redirect(url_for('lista_pedidos'))
        
    except Exception as e:
        db.session.rollback()  # Adiciona rollback para garantir integridade do banco
        print("Erro ao finalizar pedido:", str(e))  # Log do erro
        return "Ocorreu um erro ao processar seu pedido. Por favor, tente novamente.", 500

@app.route('/pedidos')
def lista_pedidos():
    try:
        pedidos = Pedido.query.order_by(Pedido.data_pedido.desc()).all()
        return render_template('tabela_pedidos.html', pedidos=pedidos)
    except Exception as e:
        print("Erro ao listar pedidos:", str(e))
        return "Ocorreu um erro ao carregar a lista de pedidos", 500

@app.route('/clientes')
def lista_clientes():
    clientes = Cliente.query.all()
    return render_template('tabela_cliente.html', clientes=clientes)

@app.route('/limpar_carrinho')
def limpar_carrinho():
    session.pop("carrinho", None)
    return redirect(url_for('menu'))

@app.route('/excluir_pedido/<int:numero_pedido>')
def excluir_pedido(numero_pedido):
    try:
        # Encontre o pedido no banco de dados
        pedido = Pedido.query.filter_by(numero_pedido=numero_pedido).first()
        
        if pedido:
            db.session.delete(pedido)
            db.session.commit()
            return redirect(url_for('lista_pedidos'))
        else:
            return "Pedido não encontrado", 404
    except Exception as e:
        db.session.rollback()
        print("Erro ao excluir pedido:", str(e))
        return "Ocorreu um erro ao excluir o pedido", 500
    
@app.route('/hierarquia')
def mostrar_hierarquia():
    raiz = encontrar_raiz(dono)
    internos = encontrar_nos_internos(dono)
    folhas = encontrar_nos_folhas(dono)

    return render_template('funcionario.html', raiz=raiz, internos=internos, folhas=folhas)



@app.route('/relatorio_clientes')
def relatorio_clientes():
    clientes = Cliente.query.all()
    bubble_sort_clientes(clientes)
    return render_template('tabela_cliente.html', clientes=clientes)

@app.route('/relatorio_pedidos')
def relatorio_pedidos():
    pedidos = Pedido.query.all()
    pedidos_ordenados = quick_sort_pedidos(pedidos)
    return render_template('tabela_pedidos.html', pedidos=pedidos_ordenados)

@app.route('/relatorio_estatisticas')
def relatorio_estatisticas():
    total_pedidos = Pedido.query.count()
    valor_medio = db.session.query(db.func.avg(Pedido.preco_total)).scalar()
    mais_caro = db.session.query(Pedido).order_by(Pedido.preco_total.desc()).first()

    valor_medio_str = f"R${valor_medio:.2f}" if valor_medio else "Nenhum pedido"
    mais_caro_num = mais_caro.numero_pedido if mais_caro else "Nenhum pedido"

    return render_template(
        'relatorio_estatisticas.html',
        total_pedidos=total_pedidos,
        valor_medio=valor_medio_str,
        pedido_mais_caro=mais_caro_num
    )


if __name__ == '__main__':
    app.run(debug=True)