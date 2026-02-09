# config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rahasia-sangat-rahasia-123456'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'instance' / 'kasir.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Backup settings
    BACKUP_DIR = BASE_DIR / 'backups'
    MAX_BACKUPS = 10
    
    # Security
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPER = True
    PASSWORD_REQUIRE_DIGIT = True