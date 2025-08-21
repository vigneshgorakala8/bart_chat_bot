"""
OpenAI Service for Bart Chatbot
Handles all OpenAI API interactions and conversation management
"""

from openai import OpenAI
from datetime import datetime
import os

class OpenAIService:
    def __init__(self, api_key=None):
        """
        Initialize OpenAI Service
        
        Args:
            api_key: OpenAI API key (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.system_prompt = "You are Bart, a helpful and intelligent AI assistant. You are knowledgeable, creative, and always strive to provide accurate and helpful responses."
    
    def get_chat_response(self, messages, model="gpt-4o", max_tokens=2000, temperature=0.7):
        """
        Get response from OpenAI with conversation history
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: OpenAI model to use (default: gpt-4o)
            max_tokens: Maximum tokens for response (default: 2000)
            temperature: Response creativity 0.0 to 1.0 (default: 0.7)
        
        Returns:
            dict: Response with 'success', 'response', 'usage', and 'error' fields
        """
        try:
            # Prepare messages for OpenAI
            openai_messages = [{"role": "system", "content": self.system_prompt}]
            openai_messages.extend(messages)
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=model,
                messages=openai_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'success': True,
                'response': ai_response,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': None,
                'usage': {}
            }
    
    def get_conversation_history(self, chat_history_records):
        """
        Convert database chat history to OpenAI message format
        
        Args:
            chat_history_records: List of ChatHistory objects from database
        
        Returns:
            list: List of message dictionaries for OpenAI
        """
        try:
            messages = []
            for msg in chat_history_records:
                # Add user message
                messages.append({
                    "role": "user",
                    "content": msg.question
                })
                # Add assistant response
                messages.append({
                    "role": "assistant", 
                    "content": msg.answer
                })
            
            return messages
            
        except Exception as e:
            print(f"Error converting conversation history: {e}")
            return []
    
    def generate_chat_title(self, first_message, model="gpt-4o"):
        """
        Generate a title for a new chat based on the first message
        
        Args:
            first_message: The first message in the conversation
            model: OpenAI model to use for title generation
        
        Returns:
            str: Generated title or default title
        """
        try:
            title_prompt = f"Generate a short, descriptive title (max 50 characters) for a chat that starts with this message: '{first_message[:200]}...'"
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates concise, descriptive titles for chat conversations. Return only the title, nothing else."},
                    {"role": "user", "content": title_prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            title = response.choices[0].message.content.strip()
            # Clean up the title
            title = title.replace('"', '').replace("'", "").strip()
            
            # If title is too long, truncate it
            if len(title) > 50:
                title = title[:47] + "..."
            
            return title if title else "New Chat"
            
        except Exception as e:
            print(f"Error generating chat title: {e}")
            return "New Chat"
    
    def update_system_prompt(self, new_prompt):
        """
        Update the system prompt for the AI assistant
        
        Args:
            new_prompt: New system prompt
        """
        self.system_prompt = new_prompt
    
    def get_models(self):
        """
        Get available OpenAI models
        
        Returns:
            list: List of available model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"Error getting models: {e}")
            return ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
    
    def test_connection(self):
        """
        Test OpenAI API connection
        
        Returns:
            dict: Test result with 'success' and 'message' fields
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return {
                'success': True,
                'message': 'OpenAI API connection successful'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'OpenAI API connection failed: {str(e)}'
            }
