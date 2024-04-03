from tracker import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    expenses = db.Column(db.Integer(), default=0)
    income = db.Column(db.Integer(), default=0)
    transactions = db.relationship('Transaction', backref='owned_user', lazy=True)

    def get_id(self):
        return self.user_id

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'User {self.username}'

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    type = db.Column(db.String(length=30), nullable=False)
    category = db.Column(db.String(length=30), nullable=False)
    amount_rounded = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)

    @property
    def amount(self):
        return self.amount

    @amount.setter
    def amount(self, amount_to_add):
        self.amount_rounded = round(amount_to_add, 2)

    def __repr__(self):
        return f'Transaction {self.name}'

class Category(db.Model):
    category_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)  # removed unique=True
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f'Category {self.name}'
