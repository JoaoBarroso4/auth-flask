from uuid import uuid4
from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
