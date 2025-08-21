"""
Chat Models
"""

from app import db
from datetime import datetime

class Chat(db.Model):
    """Chat model for conversation management"""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chat_history = db.relationship('ChatHistory', backref='chat', lazy=True, 
                                  order_by='ChatHistory.created_at', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Chat {self.title}>'
    
    @property
    def message_count(self):
        """Get the number of messages in this chat"""
        return len(self.chat_history)
    
    @property
    def last_message_time(self):
        """Get the timestamp of the last message"""
        if self.chat_history:
            return self.chat_history[-1].created_at
        return self.created_at
    
    def get_conversation_summary(self):
        """Get a summary of the conversation"""
        if not self.chat_history:
            return "No messages yet"
        
        # Get first few messages for summary
        messages = self.chat_history[:3]
        summary = []
        for msg in messages:
            summary.append(f"User: {msg.question[:50]}...")
            summary.append(f"Bart: {msg.answer[:50]}...")
        
        return " | ".join(summary)

class ChatHistory(db.Model):
    """Chat history model for storing conversation messages"""
    
    __tablename__ = 'chat_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ChatHistory {self.id}>'
    
    @property
    def question_preview(self):
        """Get a preview of the user question"""
        return self.question[:100] + "..." if len(self.question) > 100 else self.question
    
    @property
    def answer_preview(self):
        """Get a preview of the AI answer"""
        return self.answer[:100] + "..." if len(self.answer) > 100 else self.answer
