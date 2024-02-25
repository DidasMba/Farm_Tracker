# app.py

from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Item,Category, Task, Inventory, Report, register_user, check_user_credentials
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secrets.token_urlsafe(32)'
migrate=Migrate(app,db)
db.init_app(app)
jwt = JWTManager(app)
#db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

 #Dashboard route
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    tasks = user.tasks  # Fetch user's tasks
    inventory = user.inventory  # Fetch user's inventory
    reports = user.reports  # Fetch user's reports
    return render_template('dashboard.html', tasks=tasks, inventory=inventory, reports=reports)
   

# Logout Route
@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    # Clear the session or JWT token
    session.clear()  # If using sessions
    return redirect(url_for('login'))

# Notification Route
@app.route('/notifications', methods=['GET'])
@jwt_required()
def notifications():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    notifications = user.notifications  # Assuming you have implemented Notifications model
    return render_template('notifications.html', notifications=notifications)

# Register Route
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json  # Get JSON data from request
        username = data.get('username')
        email = data.get('email')  # Make sure to get email from request data
        password = data.get('password')
        role = data.get('role', 'user')  # Set default role to 'user'

        if not username or not email or not password:
            return jsonify({"msg": "Username, email, and password are required."}), 400
        
        # Check if username is provided and contains only alphabets
        if not username or not username.isalpha():
            return jsonify({"msg": "Invalid username. Please provide a valid username with only characters."}), 400
        
        # Check if email is provided
        if not email:
            return jsonify({"msg": "Email is required."}), 400
        
        # Check if password is provided
        if not password:
            return jsonify({"msg": "Password is required."}), 400
        
        # Check if password is at least 8 characters long
        if len(password) < 8:
            return jsonify({"msg": "Password must be at least 8 characters long."}), 400
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists."}), 400
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "Email already exists."}), 400
        
        # Check if password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            return jsonify({"msg": "Password must contain at least one uppercase letter."}), 400
        
        
        # Assuming register_user is a function that registers the user
        register_user(username, password, email, role)  # Pass username, password, and email to register_user function
        return jsonify({"msg": "User created successfully"}), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    
def register_user(username, password, email, role='user'):
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
  # Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify({
            "name": user.username,
            "role": user.role,
            "email": user.email,
            "access_token": access_token
            
        }), 200
    else:
        return jsonify({"msg": "User not found or wrong credentials"}), 401
    
    # Example route that requires admin privileges
@app.route('/admin_only_route', methods=['GET'])
@jwt_required()
def admin_only_route():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    # Check if the user is an admin
    if user.role != 'admin':
        return jsonify({"msg": "Unauthorized access"}), 403  # Return Forbidden status if not admin
    
    # Admin-only logic here
    return jsonify({"msg": "Welcome admin"}), 200
 

# User Profile
@app.route('/profile/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    # Retrieve the user from the database by ID
    user = User.query.get_or_404(user_id)
    
    # Example of customizing the response format
    profile_data = {
        'username': user.username,
        'email': user.email,
        'tasks': [{'title': task.title, 'description': task.description} for task in user.tasks]
    }
    
    # Convert the profile data to JSON and return it with a 200 status code
    return jsonify(profile_data), 200

# Delete User
@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": f"User {username} deleted successfully"}), 200
    else:
        return jsonify({"msg": f"User {username} not found"}), 404

# Update User Data
@app.route('/update_user/<username>', methods=['PATCH'])
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        new_password = request.json.get('new_password', user.password)
        user.password = new_password
        db.session.commit()
        return jsonify({"msg": f"Password for user {username} updated successfully"}), 200
    else:
        return jsonify({"msg": f"User {username} not found"}), 404

# Get Users
@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'username': user.username, 'email': user.email} for user in users]
    return jsonify(user_list), 200


# Items and Category
#from flask import request, jsonify
#from models import db, Item, Category

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


# Create a Task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json

    # Validate request data
    if not data.get('description') or not data.get('type'):
        return jsonify({'error': 'Description and type are required'}), 400

    # Create new task object
    new_task = Task(
        description=data['description'],
        type=data['type'],
        assigned_worker=data.get('assigned_worker'),
        deadline=data.get('deadline')
    )

    # Add task to database
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task added successfully', 'task': new_task.to_dict()}), 201

if __name__ == '__main__':
    app.run(debug=True)
