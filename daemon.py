from app import app
from app.database import db, \
                         Domain, \
                         Whois
from flask.ext.mail import Mail, Message
from pythonwhois.net import get_whois_raw as get_whois
from difflib import unified_diff
from time import sleep
import re

with app.app_context():
    mail = Mail(app)

    while True:
        # Get a list of all domains
        domains = db.session.query(Domain).\
                             order_by(Domain.name).\
                             all()

        # Do a whois lookup on each domain
        for domain in domains:
            print "*** Processing %s" % domain.name

            # Retrieve the stored whois for this domain
            whois = db.session.query(Whois).\
                              filter(Whois.id == domain.whois_id).\
                              first()

            # Lookup the current whois
            whois_fresh = get_whois(domain.name)[0]

            # Filter the whois info for .ca domains
            whois_fresh = re.sub(r'(%.*)\n', '', whois_fresh, flags=re.MULTILINE)

            # Filter the whois info for .com domains
            whois_fresh = re.sub(r'(>>>.*)\n', '', whois_fresh, flags=re.MULTILINE)
            whois_fresh = re.sub(r'(^Timestamp:.*)\n', '', whois_fresh, flags=re.MULTILINE)
            whois_fresh = re.sub(r'(^Cached on:.*)\n', '', whois_fresh, flags=re.MULTILINE)

            if whois is None:
                print "Saving new whois information for %s" % domain.name
                # No previous whois found, so just save it
                whois = Whois(domain=domain.name, value=whois_fresh)
                db.session.add(whois)
                db.session.commit()
            elif whois.value is not None and whois.value != whois_fresh:
                print "Whois information has changed for %s" % domain.name

                # Build the email body
                diff = unified_diff(whois.value.split(), whois_fresh.split(), fromfile="old-whois.txt", tofile="new-whois.txt")
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

            # Wait a second so as to not overwhelm the whois server
            sleep(1)

        print "### Sleeping. Will refresh values in %s hours" % app.config['DAEMON_SLEEP_INTERVAL']
        sleep(app.config['DAEMON_SLEEP_INTERVAL'] * 3600)
