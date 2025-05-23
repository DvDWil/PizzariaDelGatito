from app import app
from models.pedidos import db

def init_db():
    with app.app_context():
        db.create_all()
        print("Banco de dados criado com sucesso!")

if __name__ == '__main__':
    init_db()