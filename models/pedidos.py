from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

    def __init__(self, nome, endereco, telefone, email):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_pedido = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    itens = db.Column(db.JSON, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)
    local_entrega = db.Column(db.String(100), nullable=False)
    data_pedido = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Nova coluna para status do pedido
    status = db.Column(db.String(20), default='pendente', nullable=False)  # pendente, em_entrega, entregue

    def __init__(self, numero_pedido, cliente, itens, preco_total, local_entrega, status='pendente'):
        self.numero_pedido = numero_pedido
        # Se cliente for um objeto Cliente, use seu ID
        if hasattr(cliente, 'id'):
            self.cliente_id = cliente.id
        else:
            self.cliente_id = cliente  # Caso cliente já seja um ID
        self.itens = itens
        self.preco_total = preco_total
        self.local_entrega = local_entrega
        self.status = status