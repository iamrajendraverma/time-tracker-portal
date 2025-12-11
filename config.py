import os

PROD_API_BASE_URL = 'https://rajendravofficial.pythonanywhere.com'
DEV_API_BASE_URL = 'http://127.0.0.1:5001'
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    API_BASE_URL = os.environ.get('API_BASE_URL') or PROD_API_BASE_URL

                                            