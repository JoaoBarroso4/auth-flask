import bcrypt
from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@localhost:3306/flask-crud'
app.config['SECRET_KEY'] = "your_secret_key"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
# view login
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        # first() because username is unique
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'})

    return jsonify({'error': 'Invalid credentials'}), 400


@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})


@app.route('/user/', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})

    return jsonify({'error': 'Invalid data'}), 400


@app.route('/user/<uuid:id>', methods=['GET'])
@login_required
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({'username': user.username})
    return jsonify({'error': 'User not found'}), 404


@app.route('/user/<uuid:id>', methods=['PUT'])
@login_required
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)

    if current_user.id != id and current_user.role == 'user':
        return jsonify({'error': 'Update not allowed'}), 403

    if user and data.get('password'):
        user.password = data.get('password')
        db.session.commit()

        return jsonify({'message': f'User {id} updated successfully'})
    return jsonify({'error': 'User not found'}), 404


@app.route('/user/<uuid:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.get(id)

    if current_user.role != 'admin':
        return jsonify({'error': 'Operation not allowed'}), 403

    if current_user.id == id:
        return jsonify({'error': 'Deletion not allowed'}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User {id} deleted successfully'})
    return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
