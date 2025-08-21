#!/usr/bin/env python3
"""
Test script to verify the AI Chatbot application setup
"""

import os
import sys
import importlib.util

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'pg8000',
        'openai',
        'dotenv'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT FOUND")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nMissing packages: {', '.join(failed_imports)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    print("All packages imported successfully!")
    return True

def test_env_file():
    """Test if .env file exists and has required variables."""
    print("\nTesting environment configuration...")
    
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("Please create .env file from env.example")
        return False
    
    print("✓ .env file found")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL', 'OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your-'):
            print(f"✗ {var} - Not configured")
            missing_vars.append(var)
        else:
            print(f"✓ {var} - Configured")
    
    if missing_vars:
        print(f"\nPlease configure: {', '.join(missing_vars)}")
        return False
    
    return True

def test_database_connection():
    """Test database connection."""
    print("\nTesting database connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv('DATABASE_URL')
        if not database_url or database_url.startswith('postgresql://username:'):
            print("✗ DATABASE_URL not properly configured")
            return False
        
        import pg8000
        conn = pg8000.connect(database_url)
        conn.close()
        print("✓ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection."""
    print("\nTesting OpenAI API connection...")
    
    try:
        from app.services.openai_service import OpenAIService
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key.startswith('your-openai'):
            print("✗ OPENAI_API_KEY not configured")
            return False
        
        # Test with a simple request
        openai_service = OpenAIService()
        result = openai_service.test_connection()
        
        if result['success']:
            print("✓ OpenAI API connection successful!")
            return True
        else:
            print(f"✗ OpenAI API connection failed: {result['message']}")
            return False
        
    except Exception as e:
        print(f"✗ OpenAI API connection failed: {e}")
        return False

def main():
    """Main test function."""
    print("=== AI Chatbot Setup Test ===\n")
    
    tests = [
        test_imports,
        test_env_file,
        test_database_connection,
        test_openai_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("You can now run the application with: python run.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
