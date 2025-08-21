"""
Authentication Views
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, logout_user, current_user
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('chat.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        success, message, user = AuthController.register_user(username, email, password)
        
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
    # TODO: Implement OneLogin SSO integration
    # For now, redirect to regular login with a message
    flash('OneLogin integration is coming soon! Please use the regular login form.')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    success, message = AuthController.logout_user()
    flash(message)
    return redirect(url_for('main.index'))
