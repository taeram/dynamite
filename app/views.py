from app import app
import os
from flask import render_template, \
                  request, \
                  send_from_directory
from helpers import is_authenticated, \
                    find_domain, \
                    find_all_domains, \
                    find_whois
from database import db, \
                     Domain
import json

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
