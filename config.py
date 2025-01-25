import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    DATABASE = 'app/db/database.db'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = 'app/db/development.db'

class TestingConfig(Config):
    TESTING = True
    DATABASE = 'app/db/test.db'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE = 'app/db/production.db'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}