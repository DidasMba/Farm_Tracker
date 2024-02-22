from flask import jsonify, request
from app import app
from app.models import Item, Category

# Endpoint for creating a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if 'name' not in data or 'category_id' not in data:
        return jsonify({'error': 'Missing required data (name or category_id)'}), 400

    name = data['name']
    category_id = data['category_id']

    # Consider adding validation for category_id here if needed

    new_item = Item(name=name, category_id=category_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item created successfully'}), 201

# Endpoint for updating an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404

    item.name = data.get('name', item.name)
    item.category_id = data.get('category_id', item.category_id)

    # Consider adding validation for category_id here if needed

    db.session.commit()

    return jsonify({'message': 'Item updated successfully'}), 200

# Endpoint for deleting an existing item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item deleted successfully'}), 200

# Endpoint for retrieving all items
@app.route('/items', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    items_data = [{'id': item.id, 'name': item.name, 'category_id': item.category_id} for item in items]
    return jsonify(items_data), 200
