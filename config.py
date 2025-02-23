# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HH_API_URL = os.getenv('HH_API_URL')
    HH_CLIENT_ID = os.getenv('HH_CLIENT_ID')
    HH_CLIENT_SECRET = os.getenv('HH_CLIENT_SECRET')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    CACHE_EXPIRE = int(os.getenv('CACHE_EXPIRE', 86400))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 5))
    MAX_SKILLS = 15
