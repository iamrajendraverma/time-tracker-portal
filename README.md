# Time Tracker Portal

A premium web portal for the Time Tracker system, built with Flask and Jinja2.

## Features
- User Authentication (Login/Signup)
- Real-time Punch In/Out
- Status Dashboard
- Punch History
- User Directory
- Dark Mode / Modern UI

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**:
   The app connects to the API at `http://127.0.0.1:5001`. You can change this in `config.py` or by setting the `API_BASE_URL` environment variable.

3. **Run the Portal**:
   ```bash
   python run.py
   ```
   The portal will start at `http://127.0.0.1:5002`.

## Project Structure
- `app/models`: API Client wrapper
- `app/controllers`: Flask Blueprints for routing logic
- `app/templates`: Jinja2 HTML templates
- `app/static`: CSS and JS assets
