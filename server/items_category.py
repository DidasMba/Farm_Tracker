# from flask import request, jsonify
# from models import db, Item, Category

# @app.route('/items', methods=['GET'])
# def get_items():
#     items = Item.query.all()
#     item_list = [{'id': item.id, 'name': item.name, 'description': item.description, 'category': item.category.name} for item in items]
#     return jsonify(item_list), 200

# @app.route('/items/<int:item_id>', methods=['GET'])
# def get_item(item_id):
#     item = Item.query.get_or_404(item_id)
#     item_data = {'id': item.id, 'name': item.name, 'description': item.description, 'category': item.category.name}
#     return jsonify(item_data), 200

# @app.route('/items', methods=['POST'])
# def create_item():
#     data = request.json
#     name = data.get('name')
#     description = data.get('description')
#     category_id = data.get('category_id')

#     if not name or not description or not category_id:
#         return jsonify({"msg": "Name, description, and category_id are required."}), 400
    
#     category = Category.query.get(category_id)
#     if not category:
#         return jsonify({"msg": "Category not found."}), 404

#     item = Item(name=name, description=description, category=category)
#     db.session.add(item)
#     db.session.commit()
    
#     return jsonify({"msg": "Item created successfully.", "item_id": item.id}), 201

# @app.route('/items/<int:item_id>', methods=['PUT'])
# def update_item(item_id):
#     item = Item.query.get_or_404(item_id)
#     data = request.json
#     name = data.get('name', item.name)
#     description = data.get('description', item.description)
#     category_id = data.get('category_id', item.category_id)

#     category = Category.query.get(category_id)
#     if not category:
#         return jsonify({"msg": "Category not found."}), 404

#     item.name = name
#     item.description = description
#     item.category = category
#     db.session.commit()

#     return jsonify({"msg": "Item updated successfully."}), 200

# @app.route('/items/<int:item_id>', methods=['DELETE'])
# def delete_item(item_id):
#     item = Item.query.get_or_404(item_id)
#     db.session.delete(item)
#     db.session.commit()
#     return jsonify({"msg": "Item deleted successfully."}), 200

# @app.route('/categories', methods=['GET'])
# def get_categories():
#     categories = Category.query.all()
#     category_list = [{'id': category.id, 'name': category.name} for category in categories]
#     return jsonify(category_list), 200

