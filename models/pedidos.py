class Pedido:
    def __init__(self, numero_pedido, cliente, sabor, preco_total, local_entrega):
        self.numero_pedido = numero_pedido
        self.cliente = cliente  
        self.sabor = sabor
        self.preco_total = preco_total
        self.local_entrega = local_entrega