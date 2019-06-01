from os import getenv

class Config(object):
    API_KEY = getenv('API_KEY')
    DAEMON_SLEEP_INTERVAL = 6 # hours
    DEBUG = getenv('DEBUG', False)
    MAIL_DEBUG = getenv('MAIL_DEBUG', False)
    MAIL_DEFAULT_SENDER = getenv('SENDER_EMAIL', 'dynamite@example.com')
    MAIL_PASSWORD = getenv('MAILGUN_SMTP_PASSWORD', None)
    MAIL_PORT = getenv('MAILGUN_SMTP_PORT', 25)
    MAIL_SERVER = getenv('MAILGUN_SMTP_SERVER', 'localhost')
    MAIL_USE_SSL = False
    MAIL_USERNAME = getenv('MAILGUN_SMTP_LOGIN', None)
    NOTIFY_EMAIL = getenv('NOTIFY_EMAIL', 'dynamite@example.com')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', 'sqlite:///app.db').replace('mysql2:', 'mysql:')
    SQLALCHEMY_ECHO = getenv('SQLALCHEMY_ECHO', False)
    SQLALCHEMY_POOL_RECYCLE = 60
