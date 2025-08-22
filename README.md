# Bart Chatbot Application

A modern chatbot application built with Flask, PostgreSQL, and OpenAI's GPT technology using MVC architecture. This application provides a user-friendly interface for interacting with a Bart assistant while maintaining conversation history and supports OneLogin SSO authentication.

**📁 This project now uses MVC (Model-View-Controller) architecture. For detailed information about the new structure, see [README_MVC.md](README_MVC.md)**

## Features

- 🤖 **Bart-Powered Chat**: Powered by OpenAI's GPT-4o model
- 👤 **User Authentication**: Secure user registration and login system
- 🔐 **OneLogin SSO**: Single Sign-On authentication with OneLogin
- 💬 **Chat Management**: Create, view, and delete chat conversations
- 📝 **Chat History**: Persistent storage of all conversations
- 🎨 **Modern UI**: Beautiful, responsive design with Bootstrap 5
- 🔒 **Security**: Password hashing and user session management
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## Database Schema

The application uses three main database tables:

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password (nullable for OneLogin users)
- `one_login_id`: OneLogin user ID (for SSO users)
- `name`: User's full name (for OneLogin users)
- `created_at`: Account creation timestamp

### Chats Table
- `id`: Primary key
- `title`: Chat title
- `user_id`: Foreign key to users table
- `created_at`: Chat creation timestamp
- `updated_at`: Last activity timestamp

### Chat History Table
- `id`: Primary key
- `chat_id`: Foreign key to chats table
- `message`: User's message
- `response`: AI's response
- `timestamp`: Message timestamp

## Prerequisites

- Python 3.8 or higher (Python 3.13+ supported with pg8000)
- PostgreSQL database
- OpenAI API key
- OneLogin account (for SSO features)

## Step-by-Step Setup Guide

### Step 1: Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd brightcone_workspace

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import flask, openai, requests; print('Dependencies installed successfully!')"
```

### Step 3: Setup PostgreSQL Database

**Option A: Automated Setup (Recommended)**
```bash
# Run the automated database setup
python setup_database.py
```

This script will:
- Create the `chatbot_db` database
- Create all required tables with correct structure
- Generate `.env` file with OneLogin configuration
- Set up proper database URL

**Option B: Manual Database Setup**
```sql
-- Connect to PostgreSQL as admin
psql -U postgres

-- Create database
CREATE DATABASE chatbot_db;

-- Create user (optional)
CREATE USER chatbot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;

-- Exit psql
\q
```

### Step 4: Configure Environment Variables

The setup script creates a `.env` file, but you need to update it with your actual credentials:

```bash
# Edit the .env file
nano .env
```

Update the following values:

```env
# Flask Configuration
SECRET_KEY=your-actual-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://postgres@localhost/chatbot_db

# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# OneLogin Configuration (already configured)
ONELOGIN_URL=https://bart.onelogin.com/
ONELOGIN_CLIENT_ID=9ae7dbc0-88ce-013d-c8db-223c7d66b5e8136836
ONELOGIN_CLIENT_SECRET=770eca7bd57a5f5f230cc6947e41fdac0d074b942726c73d11b1f056e7ec661e
ONELOGIN_REDIRECT_URI=http://localhost:5001/auth/callback
```

**Important**: Replace the placeholder values with your actual credentials!

### Step 5: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the API key (starts with `sk-`)
5. Update the `OPENAI_API_KEY` in your `.env` file

### Step 6: Test the Setup

```bash
# Test database connection and table creation
python -c "
from app import create_app, db
from app.models.user import User
app = create_app()
with app.app_context():
    users = User.query.all()
    print(f'Database connection successful! Found {len(users)} users.')
    print('User table columns:', [col.name for col in User.__table__.columns])
"
```

### Step 7: Run the Application

```bash
# Start the Flask application
python run.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
```

### Step 8: Access the Application

1. Open your browser
2. Navigate to `http://localhost:5001`
3. You should see the Bart Chatbot landing page

## Usage Guide

### Regular Registration/Login
1. Click "Get Started" or "Login" on the landing page
2. Fill in your username, email, and password
3. Click "Register" or "Sign In"
4. Access the chat dashboard

### OneLogin SSO Authentication
1. Click "Login with OneLogin" on the login page
2. You'll be redirected to OneLogin for authentication
3. After successful authentication, you'll be automatically logged in
4. Access the chat dashboard

### Using the Chat Interface
1. **Create New Chat**: Click "New Chat" button
2. **Send Messages**: Type your message and press Enter
3. **View History**: All conversations are saved automatically
4. **Delete Chats**: Use the delete button next to chat titles

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error
```bash
# Error: connection to server at "localhost" failed
# Solution: Make sure PostgreSQL is running
brew services start postgresql  # macOS
sudo systemctl start postgresql  # Linux
```

#### 2. ModuleNotFoundError: No module named 'requests'
```bash
# Solution: Install missing dependencies
pip install requests==2.31.0
```

#### 3. OpenAI API Key Error
```
Error: Incorrect API key provided
# Solution: Update your .env file with a real OpenAI API key
```

#### 4. Database Table Missing Columns
```bash
# Solution: Recreate tables with correct structure
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print('Tables recreated successfully!')
"
```

#### 5. Port Already in Use
```bash
# Error: Address already in use
# Solution: Use a different port or kill the process
lsof -ti:5001 | xargs kill -9
```

### Debug Mode

To enable debugging for development:

```bash
# Add debug breakpoints in your code
import pdb; pdb.set_trace()

# Run with debug output
python run.py
```

## API Endpoints

### Authentication
- `GET /` - Landing page
- `GET /auth/register` - Registration page
- `POST /auth/register` - User registration
- `GET /auth/login` - Login page
- `POST /auth/login` - User authentication
- `GET /auth/onelogin` - OneLogin SSO authentication
- `GET /auth/callback` - OneLogin callback handler
- `GET /auth/logout` - User logout

### Chat Interface
- `GET /chat/dashboard` - User dashboard
- `GET /chat/<chat_id>` - Chat interface
- `POST /chat/new` - Create new chat
- `POST /chat/send_message` - Send message to AI
- `DELETE /chat/delete/<chat_id>` - Delete chat

### API Endpoints
- `GET /chat/api/chats` - Get user's chat list
- `GET /chat/api/chat/<chat_id>` - Get chat messages
- `GET /chat/api/chat/<chat_id>/summary` - Get chat summary

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for session management | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `ONELOGIN_URL` | OneLogin base URL | Yes |
| `ONELOGIN_CLIENT_ID` | OneLogin client ID | Yes |
| `ONELOGIN_CLIENT_SECRET` | OneLogin client secret | Yes |
| `ONELOGIN_REDIRECT_URI` | OneLogin callback URL | Yes |

### Database Configuration

The application uses SQLAlchemy ORM with PostgreSQL. The default configuration:
- Host: localhost
- Port: 5432
- Database: chatbot_db
- User: postgres

### OpenAI Configuration

You need an OpenAI API key to use the chatbot functionality:
1. Sign up at [OpenAI](https://openai.com)
2. Navigate to API Keys section
3. Create a new secret key
4. Add it to your `.env` file

## Security Features

- Password hashing using Werkzeug's security functions
- User session management with Flask-Login
- SQL injection protection through SQLAlchemy ORM
- CSRF protection through Flask-WTF
- Secure password storage (hashed, not plain text)
- OneLogin SSO integration with state parameter validation
- Environment variable protection for sensitive data

## Project Structure

**📁 This project uses MVC architecture. For the complete structure, see [README_MVC.md](README_MVC.md)**

```
brightcone_workspace/
├── run.py                    # Application entry point
├── setup_database.py         # Database setup script
├── requirements.txt          # Python dependencies
├── env.example              # Environment variables template
├── .env                     # Environment variables (created by setup)
├── app/                     # Main application package (MVC)
│   ├── __init__.py         # App factory and configuration
│   ├── models/             # Database models
│   │   ├── user.py        # User model with OneLogin support
│   │   └── chat.py        # Chat and message models
│   ├── views/              # Route handlers
│   │   ├── auth.py        # Authentication routes
│   │   ├── chat.py        # Chat interface routes
│   │   └── main.py        # Main page routes
│   ├── controllers/        # Business logic
│   │   ├── auth_controller.py  # Authentication logic
│   │   └── chat_controller.py  # Chat management logic
│   ├── services/           # External services
│   │   └── openai_service.py   # OpenAI API integration
│   ├── templates/          # HTML templates
│   │   ├── base.html      # Base template
│   │   ├── index.html     # Landing page
│   │   ├── login.html     # Login page with OneLogin
│   │   ├── register.html  # Registration page
│   │   ├── dashboard.html # Chat dashboard
│   │   ├── chat.html      # Chat interface
│   │   └── onelogin_callback.html  # OneLogin callback
│   └── static/             # Static files
│       ├── css/
│       │   └── style.css  # Application styles
│       ├── js/            # JavaScript files
│       └── images/        # Image assets
└── README_MVC.md          # Detailed MVC documentation
```

## Development

### Running in Development Mode

```bash
# Enable debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the application
python run.py
```

### Adding Debug Breakpoints

```python
# Add this line where you want to pause execution
import pdb; pdb.set_trace()

# Debug commands:
# c - continue execution
# n - next line
# s - step into function
# p variable_name - print variable
# l - list current location
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the error logs in the terminal
3. Open an issue on the GitHub repository
4. Include error messages and steps to reproduce

## Acknowledgments

- Flask framework for the web framework
- OpenAI for providing the GPT API
- OneLogin for SSO authentication
- Bootstrap for the UI framework
- Font Awesome for icons
- SQLAlchemy for database ORM
- PostgreSQL for the database

## Version History

- **v2.0**: Added OneLogin SSO integration, MVC architecture
- **v1.0**: Initial release with basic chat functionality
