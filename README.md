# Bart Chatbot Application

A modern chatbot application built with Flask, PostgreSQL, and OpenAI's GPT technology using MVC architecture. This application provides a user-friendly interface for interacting with a Bart assistant while maintaining conversation history.

**📁 This project now uses MVC (Model-View-Controller) architecture. For detailed information about the new structure, see [README_MVC.md](README_MVC.md)**

## Features

- 🤖 **Bart-Powered Chat**: Powered by OpenAI's GPT-4o model
- 👤 **User Authentication**: Secure user registration and login system
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
- `password_hash`: Hashed password
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

## Quick Start

For a quick setup, run:
```bash
python quick_setup.py
```

This will guide you through the initial configuration.

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: If you encounter issues with `psycopg2-binary` on Python 3.13+, use the alternative requirements:
   ```bash
   pip install -r requirements_alternative.txt
   ```

4. **Set up PostgreSQL database**
   
   **Option A: Use the automated setup script**
   ```bash
   python setup_database.py
   ```
   
   **Option B: Manual setup**
   ```sql
   CREATE DATABASE chatbot_db;
   CREATE USER chatbot_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
   ```

5. **Configure environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://chatbot_user:your_password@localhost/chatbot_db
   OPENAI_API_KEY=your-openai-api-key
   ```

6. **Test the setup**
   ```bash
   python test_setup.py
   ```

7. **Run the application**
   ```bash
   python run.py
   ```

8. **Access the application**
   Open your browser and navigate to `http://localhost:5001`
   
   **Note**: On macOS, port 5000 may be used by AirPlay. The application runs on port 5001 by default.

## Usage

1. **Register a new account** or **login** with existing credentials
2. **Create a new chat** from the dashboard
3. **Start chatting** with the AI assistant
4. **View your chat history** on the dashboard
5. **Delete chats** you no longer need

## API Endpoints

- `GET /` - Landing page
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /login` - Login page
- `POST /login` - User authentication
- `GET /logout` - User logout
- `GET /dashboard` - User dashboard
- `GET /chat/<chat_id>` - Chat interface
- `POST /new_chat` - Create new chat
- `POST /send_message` - Send message to AI
- `POST /delete_chat/<chat_id>` - Delete chat

## Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key

### Database Configuration

The application uses SQLAlchemy ORM with PostgreSQL. Make sure your database is running and accessible with the credentials provided in the `DATABASE_URL`.

### OpenAI Configuration

You need an OpenAI API key to use the chatbot functionality. Sign up at [OpenAI](https://openai.com) and get your API key.

## Security Features

- Password hashing using Werkzeug's security functions
- User session management with Flask-Login
- SQL injection protection through SQLAlchemy ORM
- CSRF protection through Flask-WTF
- Secure password storage (hashed, not plain text)

## Project Structure

**📁 This project now uses MVC architecture. For the complete structure, see [README_MVC.md](README_MVC.md)**

```
chatbot-app/
├── run.py                # Application entry point
├── app/                  # Main application package (MVC)
│   ├── models/          # Database models
│   ├── views/           # Route handlers
│   ├── controllers/     # Business logic
│   ├── services/        # External services
│   ├── templates/       # HTML templates
│   └── static/          # Static files
├── requirements.txt      # Python dependencies
└── README_MVC.md        # Detailed MVC documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

## Acknowledgments

- Flask framework
- OpenAI for providing the GPT API
- Bootstrap for the UI framework
- Font Awesome for icons
