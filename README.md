# Auth-Flask

CRUD simples criado para simular o funcionamento de um sistema WEB de login. Ele utiliza o SQLAlchemy como ORM para fazer as interações com um banco MySQL e o Flask-Login para cuidar das sessões dos usuários. Estes possuem controle de papel (user e admin).

## Pré-requisitos
- Python 3.6+
- Docker
- Flask
- Flask-Login
- Flask-SQLAlchemy
- PyMySQL
- Werkzeug
- Cryptography
- bcrypt

## Como Rodar?

1. Clone este repositório.
2. Instale os pacotes necessários, utilizando o comando `pip3 install -r requirements.txt --upgrade`.
3. Com o Docker rodando, use o comando `docker-compose up`.
4. Acesse o shell do Flask com `flask shell`. Em seguida, crie o banco com `db.create_all()`, `db.session.commit()` e `exit()`.
5. Rode a aplicação usando `python app.py`.


## Endpoints

- /login/ (POST): Login.
- /logout/ (GET): Logout.
- /user/ (POST): Criar um novo usuário.
- /user/<uuid:id> (GET): Listar detalhes de um usuário.
- /user/<uuid:id> (PUT): Atualizar informações de um usuário.
- /user/<uuid:id> (DELETE): Deletar um usuário.

