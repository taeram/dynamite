from os import getenv

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    STRIP_WWW_PREFIX = True
    API_KEY = getenv('API_KEY')

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
