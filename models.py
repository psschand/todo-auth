from datetime import datetime
from flask_login import UserMixin
from __init__ import db


class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id:d}>'


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    todos = db.relationship('Todo', backref="user", lazy=True)

    def __repr__(self):
        return f'<User {self.username}'
