#!/usr/bin/env python3
"""
Database setup script for AI Chatbot Application
This script helps you set up the PostgreSQL database for the chatbot application.
"""

import os
import sys
import pg8000

def create_database():
    """Create the database and user for the chatbot application."""
    
    print("=== AI Chatbot Database Setup ===\n")
    
    # Get database configuration
    print("Please provide the following information:")
    db_host = input("Database host (default: localhost): ").strip() or "localhost"
    db_port = input("Database port (default: 5432): ").strip() or "5432"
    admin_user = input("PostgreSQL admin username (default: postgres): ").strip() or "postgres"
    admin_password = input("PostgreSQL admin password: ").strip()
    
    if not admin_password:
        print("Error: Admin password is required!")
        return False
    
    # Database and user details
    db_name = "chatbot_db"
    db_user = "chatbot_user"
    db_password = input("Password for chatbot_user: ").strip()
    
    if not db_password:
        print("Error: Password for chatbot_user is required!")
        return False
    
    try:
        # Connect to PostgreSQL as admin
        print("\nConnecting to PostgreSQL...")
        conn = pg8000.connect(
            host=db_host,
            port=db_port,
            user=admin_user,
            password=admin_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if cursor.fetchone():
            print(f"Database '{db_name}' already exists.")
        else:
            # Create database
            print(f"Creating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully!")
        
        # Check if user exists
        cursor.execute("SELECT 1 FROM pg_user WHERE usename = %s", (db_user,))
        if cursor.fetchone():
            print(f"User '{db_user}' already exists.")
        else:
            # Create user
            print(f"Creating user '{db_user}'...")
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
            print(f"User '{db_user}' created successfully!")
        
        # Grant privileges
        print("Granting privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")
        cursor.execute(f"GRANT CONNECT ON DATABASE {db_name} TO {db_user}")
        
        # Close admin connection
        cursor.close()
        conn.close()
        
        # Test connection with new user
        print("Testing connection with new user...")
        test_conn = pg8000.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        test_conn.close()
        print("Connection test successful!")
        
        # Generate .env file content
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        print("\n=== Setup Complete! ===")
        print(f"Database: {db_name}")
        print(f"User: {db_user}")
        print(f"Database URL: {database_url}")
        
        # Create .env file
        env_content = f"""# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production

# Database Configuration
DATABASE_URL={database_url}

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n.env file created successfully!")
        print("Please update the SECRET_KEY and OPENAI_API_KEY in the .env file.")
        
        return True
        
    except pg8000.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function."""
    if create_database():
        print("\nYou can now run the application with: python app.py")
    else:
        print("\nDatabase setup failed. Please check your PostgreSQL configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
