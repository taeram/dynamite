from os import getenv

class Config(object):
    API_KEY = getenv('API_KEY')
    DAEMON_SLEEP_INTERVAL = 6 # hours
    MAIL_DEBUG = False
    MAIL_DEFAULT_SENDER = getenv('SENDER_EMAIL', 'dynamite@example.com')
    MAIL_PASSWORD = getenv('MAILGUN_SMTP_PASSWORD', None)
    MAIL_PORT = getenv('MAILGUN_SMTP_PORT', 25)
    MAIL_SERVER = getenv('MAILGUN_SMTP_SERVER', 'localhost')
    MAIL_USERNAME = getenv('MAILGUN_SMTP_LOGIN', None)
    MAIL_USE_SSL = False
    NOTIFY_EMAIL = getenv('NOTIFY_EMAIL', 'dynamite@example.com')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

class TestingConfig(Config):
    TESTING = True
