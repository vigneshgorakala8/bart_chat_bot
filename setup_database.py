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
    
    # Direct database configuration
    db_host = "localhost"
    db_port = "5432"
    admin_user = "postgres"
    db_name = "chatbot_db"
    
    # Database URL for the application
    database_url = "postgresql://postgres@localhost/chatbot_db"
    
    try:
        # Connect to PostgreSQL as admin
        print("Connecting to PostgreSQL...")
        conn = pg8000.connect(
            host=db_host,
            port=db_port,
            user=admin_user
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
        
        # Close admin connection
        cursor.close()
        conn.close()
        
        # Test connection
        print("Testing connection...")
        test_conn = pg8000.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=admin_user
        )
        test_conn.close()
        print("Connection test successful!")
        
        # Create database tables
        print("Creating database tables...")
        create_tables(database_url)
        
        print("\n=== Setup Complete! ===")
        print(f"Database: {db_name}")
        print(f"Database URL: {database_url}")
        
        # Create .env file with OneLogin configuration
        env_content = f"""# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production

# Database Configuration
DATABASE_URL={database_url}

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# OneLogin Configuration
ONELOGIN_URL=https://bart.onelogin.com/
ONELOGIN_CLIENT_ID=9ae7dbc0-88ce-013d-c8db-223c7d66b5e8136836
ONELOGIN_CLIENT_SECRET=770eca7bd57a5f5f230cc6947e41fdac0d074b942726c73d11b1f056e7ec661e
ONELOGIN_REDIRECT_URI=http://localhost:5001/auth/callback
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

def create_tables(database_url):
    """Create database tables using Flask-SQLAlchemy."""
    try:
        # Set environment variable for database URL
        os.environ['DATABASE_URL'] = database_url
        
        # Import Flask app and create tables
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Created tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

def main():
    """Main function."""
    if create_database():
        print("\nYou can now run the application with: python run.py")
    else:
        print("\nDatabase setup failed. Please check your PostgreSQL configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
