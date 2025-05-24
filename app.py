from flask import Flask, render_template, request, redirect, url_for, session
from models.pedidos import db
from models.pedidos import Cliente, Pedido  # Agora importamos db separadamente
from datetime import datetime
import os

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


def calcular_preco(carrinho):
    return sum(item["preco_total"] for item in carrinho)

@app.route('/')
def home():
    return render_template('index.html')

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
        
        # Código para verificar se o modelo Pedido está configurado para armazenar uma lista em 'itens'
        try:
            # Convertendo o carrinho para string JSON se o modelo esperar uma string
            import json
            itens_json = json.dumps(session["carrinho"])
            
            # Busca o maior número de pedido existente e adiciona 1
            ultimo_pedido = Pedido.query.order_by(Pedido.numero_pedido.desc()).first()
            numero_pedido = (ultimo_pedido.numero_pedido + 1) if ultimo_pedido else 1
            
            pedido = Pedido(
                numero_pedido=numero_pedido,
                cliente_id=cliente.id,  # Use cliente_id em vez de cliente direto
                itens=itens_json,       # Armazena como JSON
                preco_total=preco_total,
                local_entrega=local_entrega
            )
            db.session.add(pedido)
            db.session.commit()
            
            session.pop("carrinho", None)
            return redirect(url_for('lista_pedidos'))
        except Exception as e:
            db.session.rollback()
            print("Erro ao salvar itens do pedido:", str(e))
            # Tentar uma abordagem alternativa se a primeira falhar
            return "Erro ao processar os itens do pedido. Verifique o modelo Pedido.", 500
        
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


if __name__ == '__main__':
    app.run(debug=True)