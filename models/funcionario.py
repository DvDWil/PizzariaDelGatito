class Funcionario:
    def __init__(self, nome, cargo):
        self.nome = nome
        self.cargo = cargo
        self.subordinados = []

    def adicionar_subordinado(self, funcionario):
        self.subordinados.append(funcionario)
