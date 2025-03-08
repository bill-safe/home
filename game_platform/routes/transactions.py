from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Transaction, User
from .. import db
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    current_user = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=current_user).all()
    return jsonify([{
        'id': t.id,
        'type': t.type,
        'amount': float(t.amount),
        'description': t.description,
        'created_at': t.created_at.isoformat()
    } for t in transactions]), 200

@transactions_bp.route('/recharge', methods=['POST'])
@jwt_required()
def recharge():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    data = request.get_json()
    amount = data.get('amount')
    if not amount or amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400

    # Create transaction record
    transaction = Transaction(
        user_id=user.id,
        amount=amount,
        type='recharge',
        description='User recharge'
    )
    db.session.add(transaction)
    
    # Update user balance
    user.balance += amount
    db.session.commit()

    return jsonify({
        'message': 'Recharge successful',
        'balance': float(user.balance)
    }), 201

@transactions_bp.route('/purchase', methods=['POST'])
@jwt_required()
def purchase():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description')
    if not amount or amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400

    if user.balance < amount:
        return jsonify({'message': 'Insufficient balance'}), 400

    # Create transaction record
    transaction = Transaction(
        user_id=user.id,
        amount=-amount,
        type='purchase',
        description=description
    )
    db.session.add(transaction)
    
    # Update user balance
    user.balance -= amount
    db.session.commit()

    return jsonify({
        'message': 'Purchase successful',
        'balance': float(user.balance)
    }), 201

@transactions_bp.route('/reward', methods=['POST'])
@jwt_required()
def reward():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description')
    if not amount or amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400

    # Create transaction record
    transaction = Transaction(
        user_id=user.id,
        amount=amount,
        type='reward',
        description=description
    )
    db.session.add(transaction)
    
    # Update user balance
    user.balance += amount
    db.session.commit()

    return jsonify({
        'message': 'Reward successful',
        'balance': float(user.balance)
    }), 201

@transactions_bp.route('/admin_adjust', methods=['POST'])
@jwt_required()
def admin_adjust():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if user.role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    target_user_id = data.get('user_id')
    amount = data.get('amount')
    description = data.get('description')
    if not target_user_id or not amount:
        return jsonify({'message': 'Missing required fields'}), 400

    target_user = User.query.get_or_404(target_user_id)
    
    # Create transaction record
    transaction = Transaction(
        user_id=target_user.id,
        amount=amount,
        type='admin_adjust',
        description=description
    )
    db.session.add(transaction)
    
    # Update user balance
    target_user.balance += amount
    db.session.commit()

    return jsonify({
        'message': 'Balance adjusted successfully',
        'user': {
            'id': target_user.id,
            'username': target_user.username,
            'balance': float(target_user.balance)
        }
    }), 201
