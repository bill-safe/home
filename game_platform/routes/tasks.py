from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Task, User, Item
from .. import db
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'publisher': task.publisher.username,
        'accepter': task.accepter.username if task.accepter else None,
        'item': {
            'id': task.item.id,
            'name': task.item.name
        } if task.item else None,
        'type': task.type,
        'price': float(task.price),
        'quantity': task.quantity,
        'status': task.status,
        'created_at': task.created_at.isoformat()
    } for task in tasks]), 200

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    data = request.get_json()
    item_id = data.get('item_id')
    task_type = data.get('type')
    price = data.get('price')
    quantity = data.get('quantity')

    if not item_id or not task_type or price is None or quantity is None:
        return jsonify({'message': 'Missing required fields'}), 400

    item = Item.query.get_or_404(item_id)
    if item.stock < quantity:
        return jsonify({'message': 'Not enough stock'}), 400

    task = Task(
        publisher_id=user.id,
        item_id=item_id,
        type=task_type,
        price=price,
        quantity=quantity
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({
        'message': 'Task created successfully',
        'task': {
            'id': task.id,
            'status': task.status,
            'created_at': task.created_at.isoformat()
        }
    }), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'publisher': task.publisher.username,
        'accepter': task.accepter.username if task.accepter else None,
        'item': {
            'id': task.item.id,
            'name': task.item.name
        } if task.item else None,
        'type': task.type,
        'price': float(task.price),
        'quantity': task.quantity,
        'status': task.status,
        'created_at': task.created_at.isoformat()
    }), 200

@tasks_bp.route('/<int:task_id>/accept', methods=['POST'])
@jwt_required()
def accept_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    task = Task.query.get_or_404(task_id)
    if task.status != 'open':
        return jsonify({'message': 'Task is not available'}), 400

    task.accepter_id = user.id
    task.status = 'locked'
    db.session.commit()

    return jsonify({
        'message': 'Task accepted successfully',
        'task': {
            'id': task.id,
            'status': task.status
        }
    }), 200

@tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
@jwt_required()
def complete_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    task = Task.query.get_or_404(task_id)
    if task.status != 'locked' or task.accepter_id != user.id:
        return jsonify({'message': 'Cannot complete this task'}), 400

    task.status = 'completed'
    task.item.stock -= task.quantity
    db.session.commit()

    return jsonify({
        'message': 'Task completed successfully',
        'task': {
            'id': task.id,
            'status': task.status
        }
    }), 200

@tasks_bp.route('/<int:task_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_task(task_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    task = Task.query.get_or_404(task_id)
    if task.status not in ['open', 'locked']:
        return jsonify({'message': 'Cannot cancel this task'}), 400

    if task.status == 'locked' and task.accepter_id != user.id and task.publisher_id != user.id:
        return jsonify({'message': 'Permission denied'}), 403

    task.status = 'cancelled'
    db.session.commit()

    return jsonify({
        'message': 'Task cancelled successfully',
        'task': {
            'id': task.id,
            'status': task.status
        }
    }), 200
