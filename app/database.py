from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Whois(db.Model):
    """ A history of whois lookups
    """

    __tablename__ = 'whois'

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Text)
    value = db.Column(db.Text)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, domain, value):
        self.domain = domain
        self.value = value

    def __repr__(self):
        return "<Whois ('%r', '%r')>" % (self.domain, self.value)

    def toObject(self):
        return {
            "domain": self.domain,
            "value": self.value,
            "created": self.created.strftime('%Y-%m-%d %H:%M:%S')
        }

class Domain(db.Model):
    """ A list of domain names, and their most recent whois status
    """

    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    whois_id = db.Column(db.Integer, db.ForeignKey(Whois.id))
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Domain '%r'>" % self.name

    def toObject(self):
        return {
            "name": self.name,
            "created": self.created.strftime('%Y-%m-%d %H:%M:%S')
        }

db.create_all()
