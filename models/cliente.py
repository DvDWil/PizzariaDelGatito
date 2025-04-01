class Cliente:
    def __init__(self, nome, endereco, telefone, email):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.pedidos = []  

    def adicionar_pedido(self, pedido):
        self.pedidos.append(pedido)
