from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(80), unique=True, nullable=False)  # User's username
    password_hash = db.Column(db.String(128))  # Hashed password for security
    score = db.Column(db.Integer, default=0)  # User's score, default is set to 0

    # Method to set the user's password securely
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check if the provided password matches the hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Function to register a new user
def register_user(username, password):
    user = User(username=username)  # Create a new user instance with the provided username
    user.set_password(password)  # Set the password using the set_password method
    db.session.add(user)  # Add the user to the database session
    db.session.commit()  # Commit the changes to the database

# Function to check user credentials during login
def check_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()  # Query the database for the user by username
    # Check if a user with the provided username exists and if the password is correct
    if user and user.check_password(password):
        return True  # Return True if the credentials are valid
    return False  # Return False if the credentials are invalid or user not found
