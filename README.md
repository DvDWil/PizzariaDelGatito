# PizzariaDelGatito

Trabalho feito na faculdade, as pessoas que participaram do projeto são: Isabely Costa, Fernanda Barbosa, David Wilton.

---

## Como rodar o projeto

### Passo 1: Criar e ativar o ambiente virtual (venv)

#### Windows (PowerShell)

1. Abra o PowerShell na pasta do projeto.  
2. Rode para criar o ambiente virtual:

```powershell
python -m venv venv
```

3. Ative o ambiente virtual:

```powershell
.\venv\Scripts\activate
```

> **Importante:**  
> Se aparecer um erro falando que scripts não podem ser executados, rode este comando para liberar temporariamente nesta sessão do PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Depois tente ativar o ambiente virtual de novo.

#### Windows (Prompt de Comando - cmd)

Se o PowerShell bloquear, abra o Prompt de Comando e rode:

```cmd
venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Passo 2: Instalar as dependências

Com o ambiente virtual ativado, rode:

```bash
pip install -r requirements.txt
```

---

### Passo 3: Rodar o Flask

Se o seu arquivo principal do Flask for `app.py`, rode:

#### Windows (PowerShell ou cmd)

```powershell
set FLASK_APP=app.py
flask run
```

#### macOS / Linux

```bash
export FLASK_APP=app.py
flask run
```

Após isso, o Flask vai iniciar o servidor local e você poderá acessar o projeto no navegador pelo endereço:

```
http://127.0.0.1:5000
```

---

## Dúvidas

Se tiver qualquer dúvida, fique à vontade para perguntar!

---

Obrigado por usar o projeto PizzariaDelGatito! 🍕😺
