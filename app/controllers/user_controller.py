"""
User Controller
Handles user management operations
"""

from flask_login import current_user
from app.models.user import User
from app.models.chat import Chat
from datetime import datetime
from app import db

class UserController:
    """Controller for user operations"""
    
    @staticmethod
    def get_user_profile(user_id=None):
        """
        Get user profile information
        
        Args:
            user_id: User ID (optional, defaults to current user)
            
        Returns:
            dict: User profile data
        """
        try:
            if user_id is None:
                user = current_user
            else:
                user = User.query.get_or_404(user_id)
            
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat(),
                'chat_count': user.chat_count,
                'total_messages': user.total_messages
            }
            
        except Exception as e:
            return None
    
    @staticmethod
    def get_user_stats(user_id=None):
        """
        Get user statistics
        
        Args:
            user_id: User ID (optional, defaults to current user)
            
        Returns:
            dict: User statistics
        """
        try:
            if user_id is None:
                user = current_user
            else:
                user = User.query.get_or_404(user_id)
            
            # Get recent activity
            recent_chats = Chat.query.filter_by(user_id=user.id).order_by(Chat.updated_at.desc()).limit(5).all()
            
            stats = {
                'total_chats': user.chat_count,
                'total_messages': user.total_messages,
                'account_age_days': (datetime.utcnow() - user.created_at).days,
                'recent_chats': [
                    {
                        'id': chat.id,
                        'title': chat.title,
                        'message_count': chat.message_count,
                        'updated_at': chat.updated_at.isoformat()
                    }
                    for chat in recent_chats
                ]
            }
            
            return stats
            
        except Exception as e:
            return None
    
    @staticmethod
    def update_user_profile(user_id, **kwargs):
        """
        Update user profile information
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            tuple: (success, message)
        """
        try:
            user = User.query.get_or_404(user_id)
            
            # Only allow users to update their own profile
            if user.id != current_user.id:
                return False, 'Access denied'
            
            # Update allowed fields
            allowed_fields = ['username', 'email']
            for field, value in kwargs.items():
                if field in allowed_fields and value:
                    setattr(user, field, value)
            
            db.session.commit()
            return True, 'Profile updated successfully'
            
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to update profile: {str(e)}'
    
    @staticmethod
    def get_user_activity(user_id=None, limit=10):
        """
        Get user activity history
        
        Args:
            user_id: User ID (optional, defaults to current user)
            limit: Number of activities to return
            
        Returns:
            list: List of activity items
        """
        try:
            if user_id is None:
                user = current_user
            else:
                user = User.query.get_or_404(user_id)
            
            # Get recent chats with messages
            recent_chats = Chat.query.filter_by(user_id=user.id).order_by(Chat.updated_at.desc()).limit(limit).all()
            
            activity = []
            for chat in recent_chats:
                if chat.chat_history:
                    last_message = chat.chat_history[-1]
                    activity.append({
                        'type': 'message',
                        'chat_id': chat.id,
                        'chat_title': chat.title,
                        'message': last_message.question_preview,
                        'timestamp': last_message.created_at.isoformat()
                    })
                else:
                    activity.append({
                        'type': 'chat_created',
                        'chat_id': chat.id,
                        'chat_title': chat.title,
                        'timestamp': chat.created_at.isoformat()
                    })
            
            return activity
            
        except Exception as e:
            return []
