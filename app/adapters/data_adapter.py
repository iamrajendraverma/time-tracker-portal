from datetime import datetime

class DataAdapter:
    @staticmethod
    def dashboard_data(user_data, status_data, history_data):
        # 1. User Data
        # Template usage: user.get('username'), user.get('id')
        user = {}
        if isinstance(user_data, dict):
            user['id'] = user_data.get('user_id') or user_data.get('id')
            user['username'] = user_data.get('username')
      
        # 2. Status Data
        # Template usage: status.get('date'), status.get('status') (checked for 'in')
        status = {}
        if isinstance(status_data, dict):
            # Map boolean is_punched_in to string 'in' or 'out' for template satisfaction
            is_punched_in = status_data.get('is_punched_in')
            status['status'] = 'in' if is_punched_in else 'out'
            
            # Map date. If punched in, show that date? Or today's date? 
            # Original code implies status_res might have had 'date'. 
            # We will use punch_in_time_ist date if available, or current date.
            today_date = datetime.now().date()
            if status_data.get('punch_in_time_ist'):
                try:
                    dt = datetime.fromisoformat(status_data.get('punch_in_time_ist'))
                    if dt.date() == today_date:
                        status['date'] = 'Today'
                    else:
                        status['date'] = dt.strftime('%b %d, %Y')
                except:
                    status['date'] = 'Today'
            else:
                status['date'] = 'Today'

        print("----------------------------------------------")
        print(f"DEBUG - Status : {status}")
        
        # 3. History Data
        # Template usage: log.get('date'), log.get('punch_in'), log.get('punch_out'), log.get('duration')
        raw_history = []
        if isinstance(history_data, list):
            raw_history = history_data
        elif isinstance(history_data, dict):
            raw_history = history_data.get('history') or history_data.get('data') or []
            
        history = []
        for h in raw_history:
            item = {} # strictly new dict
            try:
                # Calculate friendly date and punch_in from start_ist
                if h.get('start_ist'):
                    dt_start = datetime.fromisoformat(h['start_ist'])
                    item['date'] = dt_start.strftime('%b %d, %Y')
                    item['punch_in'] = dt_start.strftime('%I:%M %p')
                    item['sort_timestamp'] = dt_start
                else:
                    item['date'] = h.get('date') # Fallback if API changed
                    item['punch_in'] = h.get('punch_in')
                    item['sort_timestamp'] = datetime.min

                # Calculate friendly punch_out from end_ist
                if h.get('end_ist'):
                    dt_end = datetime.fromisoformat(h['end_ist'])
                    item['punch_out'] = dt_end.strftime('%I:%M %p')
                else:
                    item['punch_out'] = h.get('punch_out') or '-'

                # Map duration
                item['duration'] = h.get('formatted_duration') or h.get('duration') or '-'
                    
            except Exception as e:
                print(f"Error formatting history item in adapter: {e}")
                # Fallback to raw values if parsing fails
                item['date'] = h.get('start_ist')
                item['punch_in'] = h.get('start_ist')
                item['punch_out'] = h.get('end_ist')
                item['duration'] = h.get('formatted_duration')
            
            history.append(item)
            
        # Sort by timestamp descending
        history.sort(key=lambda x: x.get('sort_timestamp', datetime.min), reverse=True)

        return user, status, history[:5]
    @staticmethod
    def history_data(history_data):
        # Parse the history data structure which contains a list of users, each with their history
        all_history = []
        users_list = []
        
        if isinstance(history_data, list):
            users_list = history_data
        elif isinstance(history_data, dict):
            users_list = history_data.get('data') or history_data.get('users') or []

        for user in users_list:
            if not isinstance(user, dict):
                continue
                
            username = user.get('username')
            user_id = user.get('user_id')
            user_history = user.get('history', [])
            
            for h in user_history:
                item = {}
                item['username'] = username
                item['user_id'] = user_id
                
                try:
                    # Calculate friendly date and punch_in from start_ist
                    if h.get('start_ist'):
                        dt_start = datetime.fromisoformat(h['start_ist'])
                        item['date'] = dt_start.strftime('%b %d, %Y')
                        item['punch_in'] = dt_start.strftime('%I:%M %p')
                        item['sort_timestamp'] = dt_start
                    else:
                        item['date'] = h.get('date', '-')
                        item['punch_in'] = h.get('punch_in', '-')
                        item['sort_timestamp'] = datetime.min

                    # Calculate friendly punch_out from end_ist
                    if h.get('end_ist'):
                        dt_end = datetime.fromisoformat(h['end_ist'])
                        item['punch_out'] = dt_end.strftime('%I:%M %p')
                    else:
                        item['punch_out'] = h.get('punch_out') or '-'

                    # Map duration
                    item['duration'] = h.get('formatted_duration') or h.get('duration') or '-'
                    
                except Exception as e:
                    print(f"Error formatting history item: {e}")
                    # Fallback to raw values if parsing fails
                    item['date'] = h.get('start_ist')
                    item['punch_in'] = h.get('start_ist')
                    item['punch_out'] = h.get('end_ist')
                    item['duration'] = h.get('formatted_duration')
                
                all_history.append(item)
        
        # Sort by timestamp descending
        all_history.sort(key=lambda x: x.get('sort_timestamp', datetime.min), reverse=True)
        
        return all_history
    @staticmethod    
    def get_all_users(raw_users):
        users = []
        raw_users = raw_users.get('users')
        for user in raw_users:
            if not isinstance(user, dict):
                continue
            username = user.get('username')
            user_id = user.get('user_id')
            users.append({'username': username, 'id': user_id})
        return users