"""
Bart Chatbot - Main Application Entry Point
MVC Structure with Flask Application Factory
"""

from app import create_app, db
from app.models import User, Chat, ChatHistory
from flask_login import LoginManager

# Create the application
app = create_app()

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
