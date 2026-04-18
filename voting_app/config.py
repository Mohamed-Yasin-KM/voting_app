import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'voting_app')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

    # Database URL
    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Logging
    LOG_DIR = 'logs'
    ERROR_LOG_FILE = os.path.join(LOG_DIR, 'error.log')
    SUCCESS_LOG_FILE = os.path.join(LOG_DIR, 'success.log')

    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
