#!/usr/bin/env python3
"""
Script to test login functionality
"""

import os
import sys
from werkzeug.security import check_password_hash

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def test_login(username_or_email, password):
    """Test login with given credentials."""
    app = create_app()
    with app.app_context():
        # Try to find user by username first, then by email
        user = User.query.filter_by(username=username_or_email).first()
        if not user:
            user = User.query.filter_by(email=username_or_email).first()
        
        if user:
            print(f"Found user: {user.username} ({user.email})")
            if check_password_hash(user.password_hash, password):
                print("✅ Password is correct!")
                return True
            else:
                print("❌ Password is incorrect!")
                return False
        else:
            print(f"❌ User not found with username/email: {username_or_email}")
            return False

def show_users():
    """Show all users in the database."""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        print("Available users:")
        print("-" * 50)
        for user in users:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"ID: {user.id}")
            print("-" * 50)

def main():
    """Main function."""
    print("=== Login Test ===\n")
    
    show_users()
    print()
    
    # Test with the known users
    print("Testing login with known users:")
    print()
    
    # Test with username
    print("1. Testing with username 'Vignesh':")
    test_login("Vignesh", "password")  # Replace with actual password
    print()
    
    # Test with email
    print("2. Testing with email 'vignesh@gmail.com':")
    test_login("vignesh@gmail.com", "password")  # Replace with actual password
    print()
    
    print("To test with your actual password, run:")
    print("python -c \"from test_login import test_login; test_login('Vignesh', 'your_actual_password')\"")

if __name__ == "__main__":
    main()
