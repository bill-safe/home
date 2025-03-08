import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    # Game platform specific settings
    ITEM_PRICE_MULTIPLIER = 1.0
    TASK_REWARD_MULTIPLIER = 1.0
    MAX_ITEMS_PER_USER = 100
    MAX_TASKS_PER_USER = 50
