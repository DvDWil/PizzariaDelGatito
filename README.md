# PizzariaDelGatito

Trabalho desenvolvido para a disciplina de **Estrutura de Dados**, com o objetivo de implementar um sistema de **delivery de pizza**, aplicando conceitos fundamentais como listas, filas, pilhas, dicionários e banco de dados relacional.

---

## Descrição do Projeto

O projeto **PizzariaDelGatito** simula o funcionamento de uma pizzaria, permitindo:

- Cadastro de clientes, pedidos, funcionários, pizzas, bebidas e ingredientes.
- Montagem dos pedidos com controle de itens e estoque.
- Processamento de pagamentos.
- Acompanhamento do status dos pedidos.

Foi desenvolvido utilizando **Python e Flask**, representando na prática conceitos de estrutura de dados no desenvolvimento de sistemas.

---

## Tecnologias Utilizadas

- **Python 3.x**
- **Flask** (framework web)
- **SQLite** (banco de dados leve)
- **HTML/CSS** (para páginas básicas, se aplicável)
- **SQLAlchemy** (se utilizado para ORM)
- Conceitos de **Estrutura de Dados**

---

## Estrutura dos Arquivos

```plaintext
PizzariaDelGatito/
├── app.py                 # Arquivo principal da aplicação Flask
├── models.py              # Definição das classes e modelos do banco
├── templates/             # Páginas HTML (se houver)
├── static/                # Arquivos CSS, JS, imagens (se houver)
├── requirements.txt       # Dependências do projeto
├── README.md              # Documentação do projeto
├── database/              # Arquivos relacionados ao banco de dados (se aplicável)
└── venv/                  # Ambiente virtual (não enviado para o GitHub)
```

---

## Instruções de Execução

### 1. Clone o repositório

```bash
git clone https://github.com/usuario/PizzariaDelGatito.git
cd PizzariaDelGatito
```

### 2. Crie e ative o ambiente virtual

#### Windows (PowerShell)

```powershell
python -m venv venv
.env\Scriptsctivate
```

> Se der erro de permissão, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

#### Windows (CMD)

```cmd
venv\Scriptsctivate.bat
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

#### Windows

```powershell
set FLASK_APP=app.py
flask run
```

#### macOS / Linux

```bash
export FLASK_APP=app.py
flask run
```

Acesse no navegador:

```
http://127.0.0.1:5000
```

---

## Integrantes do Grupo

- Isabely Costa
- Fernanda Barbosa
- David Wilton Souza Barbosa

---

## Observações Finais

Este projeto foi desenvolvido com fins **educacionais**, para a disciplina de **Estrutura de Dados** ministrada pela professora **Karla Roberto Sartin**, aplicando conceitos teóricos na prática.

## Dúvidas

Se tiver qualquer dúvida, fique à vontade para perguntar!

---

Obrigado por usar o projeto PizzariaDelGatito! 🍕😺
