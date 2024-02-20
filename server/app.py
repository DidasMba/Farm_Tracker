# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, register_user, check_user_credentials

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secrets.token_urlsafe(32)'
migrate=Migrate(app,db)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json  # Get JSON data from request
        username = data.get('username')
        email = data.get('email')  # Make sure to get email from request data
        password = data.get('password')
        
        if not username or not username.isalpha():
            return jsonify({"msg": "Invalid username. Please provide a valid username with only characters."}), 400
        
        if not password:  # Check if password is provided
            return jsonify({"msg": "Password is required."}), 400
        
        register_user(username, password, email)  # Pass username and password to register_user function
        return jsonify({"msg": "User created successfully"}), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    from flask import jsonify

#from flask import jsonify

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify({
            "name": user.username,
            "email": user.email,
            "access_token": access_token
            
        }), 200
    else:
        return jsonify({"msg": "User not found or wrong credentials"}), 401

@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": f"User {username} deleted successfully"}), 200
    else:
        return jsonify({"msg": f"User {username} not found"}), 404

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

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'username': user.username, 'email': user.email} for user in users]
    return jsonify(user_list), 200

if __name__ == '__main__':
    app.run(debug=True)
