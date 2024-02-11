from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "your_secret_key"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)


@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        # first() because username is unique
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return jsonify({'message': 'Logged in successfully'})

    return jsonify({'error': 'Invalid credentials'}), 400


if __name__ == '__main__':
    app.run(debug=True)
