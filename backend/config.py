import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key-for-dev'
    
    # Database Setup
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///clinic.db'
    
    # Fix for Render Postgres URLs (postgres:// -> postgresql://)
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Production Cookie Settings (Required for cross-domain requests on Render)
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    # Flask-Login cookie settings
    REMEMBER_COOKIE_SAMESITE = 'None'
    REMEMBER_COOKIE_SECURE = True
