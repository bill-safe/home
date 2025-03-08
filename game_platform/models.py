from datetime import datetime
from game_platform import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_role_enum'), nullable=False, default='user')
    balance = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    published_tasks = db.relationship('Task', foreign_keys='Task.publisher_id', back_populates='publisher')
    accepted_tasks = db.relationship('Task', foreign_keys='Task.accepter_id', back_populates='accepter')
    transactions = db.relationship('Transaction', back_populates='user')

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tasks = db.relationship('Task', back_populates='item')

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accepter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    type = db.Column(db.Enum('exchange', 'task', name='task_type_enum'), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('open', 'locked', 'completed', 'cancelled', name='task_status_enum'), nullable=False, default='open')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    publisher = db.relationship('User', foreign_keys=[publisher_id], back_populates='published_tasks')
    accepter = db.relationship('User', foreign_keys=[accepter_id], back_populates='accepted_tasks')
    item = db.relationship('Item', back_populates='tasks')
    transactions = db.relationship('Transaction', back_populates='task')

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    type = db.Column(db.Enum('recharge', 'purchase', 'reward', 'admin_adjust', name='transaction_type_enum'), nullable=False)
    related_id = db.Column(db.Integer)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='transactions')
    task = db.relationship('Task', back_populates='transactions')
