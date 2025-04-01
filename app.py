from flask import Flask, render_template, request, redirect, url_for, session
from models.cliente import Cliente
from models.pedidos import Pedido

app = Flask(__name__, static_folder='static')
app.secret_key = "1234"

clientes = []
pedidos = []

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

fretes = {
    "Asa Sul": 5.00,
    "Asa Norte": 5.00,
    "Cruzeiro": 10.00,
    "Sudoeste": 10.00,
    "Octogonal": 15.00,
    "Guará": 15.00,
    "Retirar na Loja": 0.00
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        sabor1 = request.form.get("sabor1")
        sabor2 = request.form.get("sabor2")
        quantidade = int(request.form.get("quantidade"))
        tamanho = request.form.get("tamanho")
        tipo = "Inteira" if sabor2 == "Nenhum" else "Meia a Meia"

        if sabor2 != "Nenhum":
            preco1 = precos_pizza.get(sabor1, {}).get(tamanho, 0)
            preco2 = precos_pizza.get(sabor2, {}).get(tamanho, 0)
            preco_unitario = (preco1 + preco2) / 2  
        else:
            preco_unitario = precos_pizza.get(sabor1, {}).get(tamanho, 0)

        preco_total = preco_unitario * quantidade

        if "carrinho" not in session:
            session["carrinho"] = []

        session["carrinho"].append({
            "sabor1": sabor1,
            "sabor2": sabor2 if sabor2 != "Nenhum" else "",
            "quantidade": quantidade,
            "tipo": tipo,
            "tamanho": tamanho,
            "preco_unitario": preco_unitario,
            "preco_total": preco_total
        })

        session.modified = True
        return redirect(url_for('carrinho'))

    return render_template('menu.html', sabores=sabores_disponiveis)

def calcular_preco(carrinho):
    total = 0
    for item in carrinho:
        total += item["preco_total"]  
    return total

@app.route('/carrinho')
def carrinho():
    carrinho = session.get("carrinho", [])

    local_entrega = request.args.get("local_entrega", "Retirar na Loja")
    frete = fretes.get(local_entrega, 0.00)

    total_com_frete = calcular_preco(carrinho) + frete

    return render_template('carrinho.html', carrinho=carrinho, total_com_frete=total_com_frete, frete=frete, local_entrega=local_entrega)

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    nome = request.form.get("nome")
    endereco = request.form.get("endereco")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    local_entrega = request.form.get("local_entrega")  # Captura o local de entrega

    if not session.get("carrinho"):
        return redirect(url_for('menu'))

    valores_frete = {
        "Asa Sul": 5.00,
        "Asa Norte": 5.00,
        "Cruzeiro": 10.00,
        "Sudoeste": 10.00,
        "Octogonal": 15.00,
        "Guará": 15.00,
        "Retirar na Loja": 0.00
    }

    preco_pizzas = calcular_preco(session["carrinho"])  
    
    frete = fretes.get(local_entrega, 0.00)
    
    preco_total = preco_pizzas + frete 

    cliente = next((c for c in clientes if c.nome == nome and c.telefone == telefone), None)

    if not cliente:
        cliente = Cliente(nome, endereco, telefone, email)
        clientes.append(cliente)

    numero_pedido = len(pedidos) + 1
    preco_pizzas = calcular_preco(session["carrinho"])  
    frete = valores_frete.get(local_entrega, 0)  
    preco_total = preco_pizzas + frete  

    pedido = Pedido(numero_pedido, cliente, session["carrinho"], preco_total, local_entrega)
    pedidos.append(pedido)

    cliente.adicionar_pedido(pedido)  

    session.pop("carrinho", None)  
    return redirect(url_for('lista_pedidos'))

@app.route('/pedidos')
def lista_pedidos():
    return render_template('tabela_pedidos.html', pedidos=pedidos)

@app.route('/clientes')
def lista_clientes():
    return render_template('tabela_cliente.html', clientes=clientes)

@app.route('/limpar_carrinho')
def limpar_carrinho():
    session.pop("carrinho", None)
    return redirect(url_for('menu'))

@app.route('/excluir_pedido/<int:numero_pedido>')
def excluir_pedido(numero_pedido):
    global pedidos
    
    for i, pedido in enumerate(pedidos):
        if pedido.numero_pedido == numero_pedido:
            pedidos.pop(i)  
            break  
    return redirect(url_for('lista_pedidos'))

if __name__ == '__main__':
    app.run(debug=True)
    