from flask import request, jsonify
from app import app, db
from app.models import Item, Category

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.serialize() for item in items])

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], category_id=data['category_id'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'}), 201
