from app import app
from flask import request
from database import db, \
                     Domain, \
                     Whois
import re

def is_authenticated():
    return app.config['API_KEY'] == request.headers['Authorization'].strip()

def is_valid_domain(domain):
    """ From RFC 1035: https://tools.ietf.org/html/rfc1035

        The labels must follow the rules for ARPANET host names.  They must
        start with a letter, end with a letter or digit, and have as interior
        characters only letters, digits, and hyphen.  There are also some
        restrictions on the length.  Labels must be 63 characters or less.
    """
    return re.search(r'^[a-z][a-z0-9\-]{1,61}\.[a-z]{1,10}$', domain.lower())

def find_all_domains():
    return db.session.query(Domain).\
                     order_by(Domain.name).\
                     all()

def find_domain(domain, include_whois=False):
    domain = domain.strip()
    if not is_valid_domain(domain):
        raise ValueError("Invalid domain: %s" % domain)

    return db.session.query(Domain).\
                       select_from(Domain).\
                       filter(Domain.name == domain).\
                       first()

def find_whois(id):
    whois = db.session.query(Whois).\
                      filter(Whois.id == id).\
                      first()

    if whois:
        return whois.value

    return None
