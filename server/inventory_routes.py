from flask import Blueprint, request, jsonify
from app.models import InventoryItem
from app import db

inventory_routes = Blueprint('inventory', __name__)

@inventory_routes.route('/inventory', methods=['GET'])
def get_inventory():
    inventory_items = InventoryItem.query.all()
    inventory = [{'id': item.id, 'name': item.name, 'quantity': item.quantity} for item in inventory_items]
    return jsonify({'inventory': inventory}), 200

@inventory_routes.route('/inventory', methods=['POST'])
def add_inventory_item():
    data = request.json

    # Validate request data
    required_fields = ['name', 'quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Create new inventory item object
    new_item = InventoryItem(
        name=data['name'],
        quantity=data['quantity']
    )

    # Add inventory item to database
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Inventory item added successfully', 'item': {'id': new_item.id, 'name': new_item.name, 'quantity': new_item.quantity}}), 201

@inventory_routes.route('/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    data = request.json

    # Retrieve inventory item from database
    item = InventoryItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    # Update inventory item quantity
    if 'quantity' in data:
        item.quantity = data['quantity']
        db.session.commit()

    return jsonify({'message': 'Inventory item updated successfully', 'item': {'id': item.id, 'name': item.name, 'quantity': item.quantity}}), 200

@inventory_routes.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    # Retrieve inventory item from database
    item = InventoryItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    # Delete inventory item from database
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Inventory item deleted successfully'}), 200
