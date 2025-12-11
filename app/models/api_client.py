import requests
from flask import current_app

class ApiClient:
    def __init__(self, token=None):
        self.base_url = current_app.config['API_BASE_URL']
        self.token = token
        self.headers = {}
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'

    def _get_url(self, endpoint):
        return f"{self.base_url}{endpoint}"

    def signup(self, username, password):
        url = self._get_url('/api/v1/auth/signup')
        response = requests.post(url, json={'username': username, 'password': password})
        return response

    def signin(self, username, password):
        url = self._get_url('/api/v1/auth/signin')
        response = requests.post(url, json={'username': username, 'password': password})
        return response

    def punch_in(self):
        url = self._get_url('/api/v1/time/punch_in')
        response = requests.post(url, headers=self.headers)
        return response

    def punch_out(self):
        url = self._get_url('/api/v1/time/punch_out')
        response = requests.post(url, headers=self.headers)
        return response

    def get_punch_status(self):
        url = self._get_url('/api/v1/time/status')
        # This is a GET according to spec
        response = requests.get(url, headers=self.headers)
        return response

    def get_current_user(self):
        url = self._get_url('/api/v1/users/me')
        response = requests.get(url, headers=self.headers)
        return response

    def get_all_users(self):
        url = self._get_url('/api/v1/users/')
        response = requests.get(url, headers=self.headers)
        return response

    def get_my_history(self):
        url = self._get_url('/api/v1/users/me/history')
        response = requests.get(url, headers=self.headers)
        return response

    def get_all_history(self):
        url = self._get_url('/api/v1/users/history')
        response = requests.get(url, headers=self.headers)
        return response

    def get_active_users(self):
        url = self._get_url('/api/v1/users/active')
        response = requests.get(url, headers=self.headers)
        return response
