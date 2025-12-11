from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models.api_client import ApiClient

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        client = ApiClient()
        response = client.signin(username, password)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token') or data.get('access_token') # Handling potential naming variations
            if token:
                session['token'] = token
                session['username'] = username
                return redirect(url_for('main.dashboard'))
            else:
                flash('Login successful but no token received', 'error')
        else:
            flash(f'Login failed: {response.text}', 'error')
            
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        client = ApiClient()
        # Adjusted to match the likely API expectation or common practice
        response = client.signup(username, password)
        
        if response.status_code == 201 or response.status_code == 200:
            flash('Account created successfully. Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Signup failed: {response.text}', 'error')
            
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
