from datetime import datetime
from . import db


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)

    auth = db.relationship('Auth', backref='user', uselist=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.full_name}', '{self.email}')"


# Auth model (authentication details)
class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'Admin' or 'User'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Auth('{self.username}', '{self.user_type}')"


# Transaction model (for admin to manage and filter)
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.id}', '{self.amount}', '{self.date}')"