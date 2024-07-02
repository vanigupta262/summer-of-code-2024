import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:tiger@localhost:5432/POS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
