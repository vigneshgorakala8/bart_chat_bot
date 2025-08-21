"""
Chat Views
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.controllers.chat_controller import ChatController

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# Initialize controller
chat_controller = ChatController()

@chat_bp.route('/dashboard')
@login_required
def dashboard():
    """Main chat dashboard"""
    chats = chat_controller.get_user_chats()
    return render_template('dashboard.html', chats=chats)

@chat_bp.route('/<int:chat_id>')
@login_required
def view_chat(chat_id):
    """View specific chat"""
    success, message, chat_data = chat_controller.get_chat(chat_id)
    
    if not success:
        flash(message)
        return redirect(url_for('chat.dashboard'))
    
    return render_template('chat.html', chat=chat_data['chat'], messages=chat_data['messages'])

@chat_bp.route('/new', methods=['POST'])
@login_required
def new_chat():
    """Create new chat"""
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        title = data.get('title', 'New Chat')
        first_message = data.get('first_message', '')
    else:
        title = request.form.get('title', 'New Chat')
        first_message = request.form.get('first_message', '')
    
    success, message, chat = chat_controller.create_chat(title, first_message)
    
    # Always return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        if success:
            response_data = {
                'success': True,
                'chat_id': chat.id,
                'title': chat.title
            }
            
            # If first message was provided, get the AI response
            if first_message:
                # Get the latest message from the chat
                latest_message = chat.chat_history[-1] if chat.chat_history else None
                if latest_message:
                    response_data['ai_response'] = latest_message.answer
                    response_data['has_first_message'] = True
            
            return jsonify(response_data)
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    # Handle regular form submissions
    if success:
        flash(message)
        return redirect(url_for('chat.view_chat', chat_id=chat.id))
    else:
        flash(message)
        return redirect(url_for('chat.dashboard'))

@chat_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    """Send message and get AI response"""
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        chat_id = data.get('chat_id')
        message = data.get('message')
    else:
        chat_id = request.form.get('chat_id')
        message = request.form.get('message')
    
    # Validate required data
    if not chat_id or not message:
        return jsonify({'success': False, 'error': 'Missing chat_id or message'}), 400
    
    # Convert chat_id to integer
    try:
        chat_id = int(chat_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid chat_id format'}), 400
    
    success, message_text, response_data = chat_controller.send_message(chat_id, message)
    
    if success:
        return jsonify({
            'success': True,
            'response': response_data['response'],
            'timestamp': response_data['timestamp'],
            'usage': response_data.get('usage', {})
        })
    else:
        return jsonify({'success': False, 'error': message_text}), 500

@chat_bp.route('/delete/<int:chat_id>', methods=['POST', 'DELETE'])
@login_required
def delete_chat(chat_id):
    """Delete chat"""
    success, message = chat_controller.delete_chat(chat_id)
    
    if request.method == 'DELETE':
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
    
    if success:
        flash(message)
    else:
        flash(message)
    
    return redirect(url_for('chat.dashboard'))

# API Routes
@chat_bp.route('/api/chats')
@login_required
def api_chats():
    """API endpoint to get user's chat list"""
    chats = chat_controller.get_user_chats()
    chat_list = []
    
    for chat in chats:
        chat_list.append({
            'id': chat.id,
            'title': chat.title,
            'created_at': chat.created_at.isoformat(),
            'updated_at': chat.updated_at.isoformat(),
            'message_count': chat.message_count
        })
    
    return jsonify({'chats': chat_list})

@chat_bp.route('/api/chat/<int:chat_id>')
@login_required
def api_chat(chat_id):
    """API endpoint to get chat messages"""
    success, message, chat_data = chat_controller.get_chat(chat_id)
    
    if not success:
        return jsonify({'error': message}), 404
    
    return jsonify(chat_data)

@chat_bp.route('/api/chat/<int:chat_id>/summary')
@login_required
def api_chat_summary(chat_id):
    """API endpoint to get chat summary"""
    summary = chat_controller.get_chat_summary(chat_id)
    
    if summary is None:
        return jsonify({'error': 'Chat not found or access denied'}), 404
    
    return jsonify(summary)
