"""
Chat Controller
Handles chat operations and messaging
"""

from flask_login import current_user
from app.models.chat import Chat, ChatHistory
from app.services.openai_service import OpenAIService
from app import db
from datetime import datetime

class ChatController:
    """Controller for chat operations"""
    
    def __init__(self):
        self.openai_service = OpenAIService()
    
    def create_chat(self, title="New Chat", first_message=""):
        """
        Create a new chat
        
        Args:
            title: Chat title
            first_message: First message for title generation and saving
            
        Returns:
            tuple: (success, message, chat)
        """
        try:
            # Generate title from first message if provided
            if first_message and title == "New Chat":
                title = self.openai_service.generate_chat_title(first_message)
            
            chat = Chat(title=title, user_id=current_user.id)
            db.session.add(chat)
            db.session.commit()
            
            # If first message is provided, save it and get AI response
            if first_message:
                # Get AI response for the first message
                conversation_history = [{"role": "user", "content": first_message}]
                ai_result = self.openai_service.get_chat_response(conversation_history)
                
                if ai_result['success']:
                    ai_response = ai_result['response']
                    
                    # Save to database
                    chat_history = ChatHistory(
                        chat_id=chat.id,
                        question=first_message,
                        answer=ai_response
                    )
                    db.session.add(chat_history)
                    chat.updated_at = datetime.utcnow()
                    db.session.commit()
            
            return True, 'Chat created successfully', chat
            
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to create chat: {str(e)}', None
    
    def send_message(self, chat_id, message):
        """
        Send a message and get AI response
        
        Args:
            chat_id: Chat ID
            message: User message
            
        Returns:
            tuple: (success, message, response_data)
        """
        try:
            # Validate chat ownership
            chat = Chat.query.get_or_404(chat_id)
            if chat.user_id != current_user.id:
                return False, 'Access denied', None
            
            # Get conversation history
            chat_history_records = ChatHistory.query.filter_by(chat_id=chat_id).order_by(ChatHistory.created_at).all()
            conversation_history = self.openai_service.get_conversation_history(chat_history_records)
            
            # Add current user message to conversation
            conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Get AI response with full conversation context
            ai_result = self.openai_service.get_chat_response(conversation_history)
            
            if not ai_result['success']:
                return False, ai_result['error'], None
            
            ai_response = ai_result['response']
            
            # Save to database
            chat_history = ChatHistory(
                chat_id=chat_id,
                question=message,
                answer=ai_response
            )
            db.session.add(chat_history)
            chat.updated_at = datetime.utcnow()
            db.session.commit()
            
            response_data = {
                'response': ai_response,
                'timestamp': chat_history.created_at.isoformat(),
                'usage': ai_result.get('usage', {})
            }
            
            return True, 'Message sent successfully', response_data
            
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to send message: {str(e)}', None
    
    def get_user_chats(self):
        """
        Get all chats for current user
        
        Returns:
            list: List of Chat objects
        """
        return Chat.query.filter_by(user_id=current_user.id).order_by(Chat.updated_at.desc()).all()
    
    def get_chat(self, chat_id):
        """
        Get specific chat with messages
        
        Args:
            chat_id: Chat ID
            
        Returns:
            tuple: (success, message, chat_data)
        """
        try:
            chat = Chat.query.get_or_404(chat_id)
            if chat.user_id != current_user.id:
                return False, 'Access denied', None
            
            messages = ChatHistory.query.filter_by(chat_id=chat_id).order_by(ChatHistory.created_at).all()
            
            chat_data = {
                'chat': {
                    'id': chat.id,
                    'title': chat.title,
                    'created_at': chat.created_at.isoformat(),
                    'updated_at': chat.updated_at.isoformat()
                },
                'messages': [
                    {
                        'id': msg.id,
                        'message': msg.question,
                        'response': msg.answer,
                        'timestamp': msg.created_at.isoformat()
                    }
                    for msg in messages
                ]
            }
            
            return True, 'Chat retrieved successfully', chat_data
            
        except Exception as e:
            return False, f'Failed to get chat: {str(e)}', None
    
    def delete_chat(self, chat_id):
        """
        Delete a chat and all its messages
        
        Args:
            chat_id: Chat ID
            
        Returns:
            tuple: (success, message)
        """
        try:
            chat = Chat.query.get_or_404(chat_id)
            if chat.user_id != current_user.id:
                return False, 'Access denied'
            
            # Delete chat (cascade will delete messages)
            db.session.delete(chat)
            db.session.commit()
            
            return True, 'Chat deleted successfully'
            
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete chat: {str(e)}'
    
    def get_chat_summary(self, chat_id):
        """
        Get a summary of chat activity
        
        Args:
            chat_id: Chat ID
            
        Returns:
            dict: Chat summary data
        """
        try:
            chat = Chat.query.get_or_404(chat_id)
            if chat.user_id != current_user.id:
                return None
            
            return {
                'id': chat.id,
                'title': chat.title,
                'message_count': chat.message_count,
                'created_at': chat.created_at,
                'updated_at': chat.updated_at,
                'last_message_time': chat.last_message_time,
                'summary': chat.get_conversation_summary()
            }
            
        except Exception as e:
            return None
