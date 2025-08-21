"""
Authentication Controller
Handles user registration, login, and logout
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app.models.user import User
from app import db

class AuthController:
    """Controller for authentication operations"""
    
    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user
        
        Args:
            username: User's username
            email: User's email
            password: User's password
            
        Returns:
            tuple: (success, message, user)
        """
        try:
            # Check if username already exists
            if User.query.filter_by(username=username).first():
                return False, 'Username already exists', None
            
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                return False, 'Email already registered', None
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            
            db.session.add(user)
            db.session.commit()
            
            return True, 'Registration successful! Please login.', user
            
        except Exception as e:
            db.session.rollback()
            return False, f'Registration failed: {str(e)}', None
    
    @staticmethod
    def login_user(username_or_email, password):
        """
        Authenticate and login user
        
        Args:
            username_or_email: Username or email
            password: User's password
            
        Returns:
            tuple: (success, message, user)
        """
        try:
            # Try to find user by username first, then by email
            user = User.query.filter_by(username=username_or_email).first()
            if not user:
                user = User.query.filter_by(email=username_or_email).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return True, 'Login successful', user
            else:
                return False, 'Invalid username/email or password', None
                
        except Exception as e:
            return False, f'Login failed: {str(e)}', None
    
    @staticmethod
    def logout_user():
        """
        Logout current user
        
        Returns:
            tuple: (success, message)
        """
        try:
            logout_user()
            return True, 'Logout successful'
        except Exception as e:
            return False, f'Logout failed: {str(e)}'
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User: User object or None
        """
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """
        Get user by username
        
        Args:
            username: Username
            
        Returns:
            User: User object or None
        """
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        
        Args:
            email: Email address
            
        Returns:
            User: User object or None
        """
        return User.query.filter_by(email=email).first()
