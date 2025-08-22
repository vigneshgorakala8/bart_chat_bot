"""
User Model
"""

from flask_login import UserMixin
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    """User model for authentication and user management"""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=True)  # Nullable for OneLogin users
    one_login_id = db.Column(db.String(255), unique=True, nullable=True)
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    chats = db.relationship('Chat', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def chat_count(self):
        """Get the number of chats for this user"""
        return len(self.chats)
    
    @property
    def total_messages(self):
        """Get the total number of messages for this user"""
        total = 0
        for chat in self.chats:
            total += len(chat.chat_history)
        return total
