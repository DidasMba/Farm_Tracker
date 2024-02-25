from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, register_user, check_user_credentials

app = Flask(__name__)  # Initialize Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Set the URI for the SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking
app.config['JWT_SECRET_KEY'] = 'secrets.token_urlsafe(32)'  # Set the JWT secret key

db.init_app(app)  # Initialize the SQLAlchemy database with the Flask app
jwt = JWTManager(app)  # Initialize the JWTManager with the Flask app

with app.app_context():
    db.create_all()  # Create database tables based on defined models

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json  # Get JSON data from request
        username = data.get('username')
        password = data.get('password')
        
        # Check if username is valid
        if not username or not username.isalpha():
            return jsonify({"msg": "Invalid username. Please provide a valid username with only characters."}), 400
        
        # Check if password is provided
        if not password:
            return jsonify({"msg": "Password is required."}), 400
        
        register_user(username, password)  # Register the user
        return jsonify({"msg": "User created successfully"}), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if user and user.check_password(password):
        access_token = create_access_token(identity=username)  # Create JWT access token
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "User not found or wrong credentials"}), 401

# Endpoint to delete a user
@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)  # Delete user from the database
        db.session.commit()
        return jsonify({"msg": f"User {username} deleted successfully"}), 200
    else:
        return jsonify({"msg": f"User {username} not found"}), 404

# Endpoint to update user password
@app.route('/update_user/<username>', methods=['PATCH'])
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        new_password = request.json.get('new_password', user.password)
        user.password = new_password  # Update user's password
        db.session.commit()
        return jsonify({"msg": f"Password for user {username} updated successfully"}), 200
    else:
        return jsonify({"msg": f"User {username} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
