from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.models.api_client import ApiClient
from functools import wraps

main_bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

from app.adapters.data_adapter import DataAdapter

@main_bp.route('/')
@login_required
def dashboard():
    client = ApiClient(token=session['token'])
    
    try:
        # Get User Info
        user_res = client.get_current_user()
        user_data = user_res.json() if user_res.status_code == 200 else {}
        
        # Get Status
        status_res = client.get_punch_status()
        status_data = status_res.json() if status_res.status_code == 200 else {}
        
        # Get Recent History (My History)
        history_res = client.get_my_history()
        history_data_raw = history_res.json() if history_res.status_code == 200 else []
        
        # Use Adapter to process data
        user, status, history = DataAdapter.dashboard_data(user_data, status_data, history_data_raw)
        
    except Exception as e:
        flash(f"Error connecting to backend: {str(e)}", "error")
        user, status, history = {}, {}, []
    
    # print(f"DEBUG - User: {user}")
    # print(f"DEBUG - Status: {status}")

    return render_template('main/dashboard.html', user=user, status=status, history=history)

@main_bp.route('/punch_in', methods=['POST'])
@login_required
def punch_in():
    client = ApiClient(token=session['token'])
    try:
        res = client.punch_in()
        if res.status_code == 200:
            flash('Punched in successfully!', 'success')
        else:
            try:
                msg = res.json().get('message', res.text)
            except:
                msg = res.text
            flash(f'Error punching in: {msg}', 'error')
    except Exception as e:
        flash(f"Error connecting to backend: {str(e)}", "error")
        
    return redirect(url_for('main.dashboard'))

@main_bp.route('/punch_out', methods=['POST'])
@login_required
def punch_out():
    client = ApiClient(token=session['token'])
    try:
        res = client.punch_out()
        if res.status_code == 200:
            flash('Punched out successfully!', 'success')
        else:
            try:
                msg = res.json().get('message', res.text)
            except:
                msg = res.text
            flash(f'Error punching out: {msg}', 'error')
    except Exception as e:
        flash(f"Error connecting to backend: {str(e)}", "error")
        
    return redirect(url_for('main.dashboard'))

@main_bp.route('/history')
@login_required
def history():
    client = ApiClient(token=session['token'])
    try:
        res = client.get_all_history()
        history_data = res.json() if res.status_code == 200 else []
        all_history = DataAdapter.history_data(history_data)
    
    except Exception as e:
        flash(f"Error connecting to backend: {str(e)}", "error")
        all_history = []
    return render_template('main/history.html', history=all_history)

@main_bp.route('/users')
@login_required
def users():
    client = ApiClient(token=session['token'])
    
    try:
        res_all = client.get_all_users()
        users_data = res_all.json() if res_all.status_code == 200 else []
        if isinstance(users_data, list):
            all_users = users_data
        elif isinstance(users_data, dict):
            all_users = users_data.get('users') or users_data.get('data') or []
        else:
            all_users = []
        
        res_active = client.get_active_users()
        active_data = res_active.json() if res_active.status_code == 200 else []
        if isinstance(active_data, list):
            active_users = active_data
        elif isinstance(active_data, dict):
            active_users = active_data.get('active_users') or active_data.get('users') or active_data.get('data') or []
        else:
            active_users = []
    except Exception as e:
        flash(f"Error connecting to backend: {str(e)}", "error")
        all_users, active_users = [], []
    
    return render_template('main/users.html', all_users=all_users, active_users=active_users)
