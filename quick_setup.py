#!/usr/bin/env python3
"""
Quick setup script for Bart Chatbot Application
This script helps you get started quickly with the chatbot application.
"""

import os
import sys
import secrets

def create_env_file():
    """Create a .env file with default values."""
    print("Creating .env file...")
    
    # Generate a secure secret key
    secret_key = secrets.token_hex(32)
    
    env_content = f"""# Flask Configuration
SECRET_KEY={secret_key}

# Database Configuration
DATABASE_URL=postgresql://postgres@localhost/chatbot_db

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ .env file created with default values")
    print("⚠️  Please update the DATABASE_URL and OPENAI_API_KEY in the .env file")

def main():
    """Main setup function."""
    print("=== Bart Chatbot Quick Setup ===\n")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("   Please activate your virtual environment first:")
        print("   source venv/bin/activate")
        print()
    
    # Check if requirements are installed
    try:
        import flask
        import pg8000
        import openai
        print("✓ All required packages are installed")
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("Please install requirements first:")
        print("pip install -r requirements.txt")
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        create_env_file()
    else:
        print("✓ .env file already exists")
    
    print("\n=== Next Steps ===")
    print("1. Set up PostgreSQL database:")
    print("   python setup_database.py")
    print()
    print("2. Update .env file with your credentials:")
    print("   - DATABASE_URL: Your PostgreSQL connection string")
    print("   - OPENAI_API_KEY: Your OpenAI API key")
    print()
    print("3. Test the setup:")
    print("   python test_setup.py")
    print()
    print("4. Run the application:")
    print("   python app.py")
    print()
    print("5. Open your browser and go to: http://localhost:5001")
    
    return True

if __name__ == "__main__":
    main()
