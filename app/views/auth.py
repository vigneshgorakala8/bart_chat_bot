"""
Authentication Views
"""
import os
import pdb
import requests
import base64
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, logout_user, current_user
from app.controllers.auth_controller import AuthController
from flask import request, session, flash


import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
       # Debug breakpoint
    
    if current_user.is_authenticated:
        return redirect(url_for('chat.dashboard'))
    
    if request.method == 'POST':
        print(f"DEBUG: Registration POST request received")
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        print(f"DEBUG: Username={username}, Email={email}, Password length={len(password)}")
        
        success, message, user = AuthController.register_user(username, email, password)
        
        print(f"DEBUG: Registration result - Success={success}, Message={message}")
        
        if success:
            flash(message)
            return redirect(url_for('auth.login'))
        else:
            flash(message)
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('chat.dashboard'))
    
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']
        
        success, message, user = AuthController.login_user(username_or_email, password)
        
        if success:
            flash(message)
            return redirect(url_for('chat.dashboard'))
        else:
            flash(message)
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth_bp.route('/onelogin')
def onelogin():
    """OneLogin authentication"""
    # Get OneLogin configuration from environment variables
    client_id = os.getenv('ONELOGIN_CLIENT_ID')
    redirect_uri = os.getenv('ONELOGIN_REDIRECT_URI', 'http://localhost:5001/auth/callback')
    
    # Generate a random state parameter for security
    state = "ucj1dkt98h" #secrets.token_urlsafe(32)
    
    # Store state in session for verification
    from flask import session
    session['onelogin_state'] = state
    
    # Build the OneLogin authorization URL
    auth_url = f"https://bart.onelogin.com/oidc/2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=openid+profile+email&state={state}"
    
    return redirect(auth_url)

@auth_bp.route('/callback')
def onelogin_callback():
    """OneLogin callback handler"""
    # Get the authorization code and state from the callback
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    # Check for errors
    if error:
        flash(f'OneLogin authentication failed: {error}')
        return redirect(url_for('auth.login'))
    
    # Verify state parameter
    stored_state = session.get('onelogin_state')
    if not stored_state or state != stored_state:
        flash('Invalid state parameter. Authentication failed.')
        return redirect(url_for('auth.login'))
    
    # Clear the state from session
    session.pop('onelogin_state', None)
    
    try:
        # Exchange code for token and get user info
        user_data = bart_login(code)
        
        if user_data:
            # Create user session
            from flask_login import login_user
            from app.models.user import User
            
            # Check if user exists in our database
            user = User.query.filter_by(one_login_id=user_data['one_login_id']).first()
            
            if not user:
                # Create new user
                user = User(
                    username=user_data['email'],
                    email=user_data['email'],
                    one_login_id=user_data['one_login_id'],
                    name=user_data['name']
                )
                from app import db
                db.session.add(user)
                db.session.commit()
            
            # Login the user
            login_user(user)
            flash('Successfully logged in with OneLogin!')
            return redirect(url_for('chat.dashboard'))
        else:
            flash('Failed to authenticate with OneLogin')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        flash(f'OneLogin authentication error: {str(e)}')
        return redirect(url_for('auth.login'))

def bart_login(code: str):
    """Get access token using the authorization code and fetch user info"""
    # Get access token using the authorization code
    access_token = exchange_code_for_token(code)
    if not access_token:
        raise Exception("Failed to obtain access token")
    
    user_info_url = f"https://bart.onelogin.com/oidc/2/me"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(user_info_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Response Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        raise Exception(f"Failed to fetch user details: {response.text}")

    result = response.json()
    
    # Return user data in the expected format
    user_data = {
        "one_login_id": result['sub'],
        "email": result['email'],
        "name": result['name'],
        "faceDescriptor": []
    }
    
    return user_data

def exchange_code_for_token(code):
    
    """Exchange authorization code for access token"""
    import os
    
    # URL to request the access token
    url = "https://bart.onelogin.com/oidc/2/token"
    client_id = os.getenv('ONELOGIN_CLIENT_ID')
    client_secret = os.getenv('ONELOGIN_CLIENT_SECRET')
    redirect_uri = os.getenv('ONELOGIN_REDIRECT_URI', 'http://localhost:5001/auth/callback')
    
    # Encode the client credentials
    auth_string = f"{client_id}:{client_secret}"
    auth_value = base64.b64encode(auth_string.encode()).decode('utf-8')
    
    # Request payload and headers
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email groups"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_value}"
    }
    
    try:
        # Make the POST request
        
        response = requests.post(url, data=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            error_detail = response.json().get('error_description', 'Unknown error occurred')
            raise Exception(f"Error obtaining access token: {error_detail}")
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    success, message = AuthController.logout_user()
    flash(message)
    return redirect(url_for('main.index'))
