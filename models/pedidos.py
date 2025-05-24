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

    def __init__(self, numero_pedido, cliente_id, itens, preco_total, local_entrega):
        self.numero_pedido = numero_pedido
        self.cliente_id = cliente_id  # Mudança aqui
        self.itens = itens
        self.preco_total = preco_total
        self.local_entrega = local_entrega
    
    @property 
    def sabor(self):
        """Propriedade para compatibilidade com o template"""
        import json
        if isinstance(self.itens, str):
            itens_list = json.loads(self.itens)
        else:
            itens_list = self.itens
        
        # Filtra apenas as pizzas
        pizzas = [item for item in itens_list if item.get('tipo') == 'pizza']
        return pizzas
    # Adicione esta classe ao seu arquivo models/pedidos.py

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    endereco = db.Column(db.String(200))
    data_cadastro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, nome, cpf, telefone, email, cargo, salario, data_admissao, endereco=None):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.cargo = cargo
        self.salario = salario
        self.data_admissao = data_admissao
        self.endereco = endereco
        self.ativo = True