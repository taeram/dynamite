from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR
from flask.ext.script import Manager, prompt_bool
from datetime import datetime

db = SQLAlchemy(app)

manager = Manager(usage="Manage the database")

@manager.command
def create():
    "Create the database"
    db.create_all()

@manager.command
def drop():
    "Empty the database"
    if prompt_bool("Are you sure you want to drop all tables from the database?"):
        db.drop_all()

@manager.command
def recreate():
    "Recreate the database"
    drop()
    create()

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
        return "<Whois (id='%r', domain='%r', created='%r', value=%r)>" % (self.id, self.domain, self.created.strftime('%Y-%m-%d %H:%M:%S'), self.value)

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
    name = db.Column(VARCHAR(255), unique=True)
    whois_id = db.Column(db.Integer, db.ForeignKey(Whois.id))
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Domain (id='%r', name='%r', whois_id='%r', created=%r)>" % (self.id, self.name, self.whois_id, self.created.strftime('%Y-%m-%d %H:%M:%S'))

    def toObject(self):
        return {
            "name": self.name,
            "created": self.created.strftime('%Y-%m-%d %H:%M:%S')
        }
