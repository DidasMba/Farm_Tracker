from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Define Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id
        }

# Endpoint for creating a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    category_id = data.get('category_id')

    # Assuming validation and error handling are implemented here

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
    items_data = [item.serialize() for item in items]
    return jsonify(items_data), 200

if __name__ == "__main__":
    app.run(debug=True)
