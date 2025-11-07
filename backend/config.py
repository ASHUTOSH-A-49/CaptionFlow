import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    UPLOAD_FOLDER = 'uploads'
    CORS_ALLOWED_ORIGINS = "*"

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}