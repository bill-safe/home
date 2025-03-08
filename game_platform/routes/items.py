from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Item, User
from .. import db

items_bp = Blueprint('items', __name__)

@items_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': float(item.price),
        'stock': item.stock
    } for item in items]), 200

@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if user.role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')

    if not name or price is None or stock is None:
        return jsonify({'message': 'Missing required fields'}), 400

    item = Item(
        name=name,
        description=description,
        price=price,
        stock=stock
    )
    db.session.add(item)
    db.session.commit()

    return jsonify({
        'message': 'Item created successfully',
        'item': {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': float(item.price),
            'stock': item.stock
        }
    }), 201

@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': float(item.price),
        'stock': item.stock
    }), 200

@items_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if user.role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    item = Item.query.get_or_404(item_id)
    data = request.get_json()

    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']
    if 'price' in data:
        item.price = data['price']
    if 'stock' in data:
        item.stock = data['stock']

    db.session.commit()
    return jsonify({
        'message': 'Item updated successfully',
        'item': {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': float(item.price),
            'stock': item.stock
        }
    }), 200

@items_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if user.role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'}), 200
