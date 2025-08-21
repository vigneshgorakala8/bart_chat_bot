"""
Views Package
"""

from .auth import auth_bp
from .chat import chat_bp
from .main import main_bp

__all__ = ['auth_bp', 'chat_bp', 'main_bp']
