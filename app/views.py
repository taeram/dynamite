from app import app,
                mail
import os
from flask import render_template, \
                  request, \
                  send_from_directory
from flask.ext.mail import Message
from helpers import is_authenticated, \
                    find_domain, \
                    find_all_domains, \
                    find_whois
from database import db, \
                     Domain, \
                     Whois
import json
from pythonwhois.net import get_whois_raw as get_whois
from difflib import unified_diff
import re

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')

@app.route('/', methods=['GET'])
def hello():
    return render_template('hello.html')

@app.route('/domain', methods=['GET', 'POST'])
def collection():
    if not is_authenticated():
        return app.response_class(response='{"error": "Invalid API key"}', mimetype='application/json', status=403)

    if request.method == 'POST':
        try:
            domains = json.loads(request.data)
        except ValueError:
            return app.response_class(response='{"error": "Invalid JSON"}', mimetype='application/json', status=400)

        for domain in domains:
            try:
                row = find_domain(domain)
            except ValueError, e:
                db.session.rollback()
                return app.response_class(response='{"error": "%s"}' % e, mimetype='application/json', status=400)

            if row is None:
                row = Domain(name=domain)
                db.session.add(row)

        db.session.commit()

    domains = find_all_domains()
    response = []
    for domain in domains:
        response.append(domain.toObject())

    return app.response_class(response=json.dumps(response), mimetype='application/json')

@app.route('/domain/<domain>', methods=['GET', 'DELETE'])
def member(domain):
    if not is_authenticated():
        return app.response_class(response='{"error": "Invalid API key"}' % request.headers['Authorization'], mimetype='application/json', status=403)

    row = find_domain(domain)
    if not row:
        return app.response_class(response='{"error": "Not found"}' % domain, mimetype='application/json', status=404)

    response = {
        "id": row.id,
        "name": row.name,
        "whois": find_whois(row.whois_id)
    }

    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()

    return app.response_class(response=json.dumps(response), mimetype='application/json')

@app.route('/daemon', methods=['GET'])
def daemon():
    # Get a list of all domains
    domains = db.session.query(Domain).\
                         order_by(Domain.name).\
                         all()

    # Do a whois lookup on each domain
    for domain in domains:
        # Retrieve the stored whois for this domain
        whois = db.session.query(Whois).\
                           filter(Whois.id == domain.whois_id).\
                           first()

        # Lookup the current whois
        whois_fresh = get_whois(domain.name)[0]

        # Strip \r returns
        whois_fresh = re.sub(r'\r', '', whois_fresh, flags=re.MULTILINE)

        # Filter the whois info for .ca domains
        whois_fresh = re.sub(r'(%.*)\n', '', whois_fresh, flags=re.MULTILINE)

        # Filter the whois info for .com domains
        whois_fresh = re.sub(r'(>>>.*)\n', '', whois_fresh, flags=re.MULTILINE)
        whois_fresh = re.sub(r'(^Timestamp:.*)\n', '', whois_fresh, flags=re.MULTILINE)
        whois_fresh = re.sub(r'(^Cached on:.*)\n', '', whois_fresh, flags=re.MULTILINE)

        if whois is None:
            # No previous whois found, so just save it
            whois = Whois(domain=domain.name, value=whois_fresh)
            db.session.add(whois)
            db.session.commit()
        elif whois.value is not None and whois.value != whois_fresh:
            # Build the email body
            diff = unified_diff(whois.value.split('\n'), whois_fresh.split('\n'), fromfile="old-whois.txt", tofile="new-whois.txt")
            email_body = '<strong>%s changes:</strong><br /><pre>%s</pre>' % (domain.name, "\n".join(diff))

            # If the whois value differs, send an email with the difference
            email = Message("%s Domain Name Notification" % domain.name, recipients=[app.config['NOTIFY_EMAIL']], html=email_body)
            mail.send(email)

            # Save the new whois value
            whois = Whois(domain=domain.name, value=whois_fresh)
            db.session.add(whois)
            db.session.commit()

        # Associate the domain with this whois value
        if domain.whois_id != whois.id:
            domain.whois_id = whois.id
            db.session.add(domain)
            db.session.commit()

    return app.response_class(response='{"status":"ok"}', mimetype='application/json')
