#!/usr/bin/env python3
"""
Script to check users in the Bart Chatbot application
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Chat, ChatHistory

def check_users():
    """Check all users in the database."""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("No users found in the database.")
            return
        
        print(f"Found {len(users)} user(s) in the database:")
        print("-" * 60)
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Created: {user.created_at}")
            
            # Count user's chats
            chat_count = len(user.chats)
            print(f"Total Chats: {chat_count}")
            
            if chat_count > 0:
                print("Recent Chats:")
                for chat in user.chats[:3]:  # Show last 3 chats
                    print(f"  - {chat.title} (created: {chat.created_at.strftime('%Y-%m-%d %H:%M')})")
            
            print("-" * 60)

def check_chats():
    """Check all chats in the database."""
    app = create_app()
    with app.app_context():
        chats = Chat.query.all()
        
        if not chats:
            print("No chats found in the database.")
            return
        
        print(f"Found {len(chats)} chat(s) in the database:")
        print("-" * 60)
        
        for chat in chats:
            print(f"ID: {chat.id}")
            print(f"Title: {chat.title}")
            print(f"User: {chat.user.username}")
            print(f"Created: {chat.created_at}")
            print(f"Updated: {chat.updated_at}")
            print(f"Messages: {len(chat.chat_history)}")
            print("-" * 60)

def check_recent_messages():
    """Check recent chat messages."""
    app = create_app()
    with app.app_context():
        messages = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(5).all()
        
        if not messages:
            print("No messages found in the database.")
            return
        
        print(f"Recent {len(messages)} message(s):")
        print("-" * 60)
        
        for msg in messages:
            print(f"Chat ID: {msg.chat_id}")
            print(f"User Message: {msg.message[:50]}...")
            print(f"AI Response: {msg.response[:50]}...")
            print(f"Timestamp: {msg.timestamp}")
            print("-" * 60)

def main():
    """Main function."""
    print("=== Bart Chatbot Database Check ===\n")
    
    print("1. Checking Users:")
    check_users()
    print()
    
    print("2. Checking Chats:")
    check_chats()
    print()
    
    print("3. Checking Recent Messages:")
    check_recent_messages()

if __name__ == "__main__":
    main()
