Dynamite
========

Dynamite is a Python powered Domain Name Monitoring service.

Requirements
============
You'll need the following:

* A [Heroku](https://www.heroku.com/) account
* [Python 2.7.3](http://www.python.org/)
* [pip](https://github.com/pypa/pip)
* [Virtualenv](https://github.com/pypa/virtualenv)

Setup
=====
```bash
    # Clone the repo
    git clone https://github.com/taeram/dynamite.git
    cd ./dynamite/

    # Create your Heroku app, and add a database addon
    heroku apps:create
    heroku addons:add heroku-postgresql

    # Promote your postgres database (your URL name may differ)
    heroku pg:promote HEROKU_POSTGRESQL_RED_URL

    # Setup and activate virtualenv
    virtualenv .venv
    source ./.venv/bin/activate

    # Install the pip requirements
    pip install -r requirements.txt

    # Set an "API key" for authorization
    heroku config:set API_KEY="secret_api_key"

    # Set your notification email
    heroku config:set NOTIFY_EMAIL="taeram@example.com"

    # Start the application
    python app.py
```

Usage
=====

To add domain names, POST a JSON array:

```bash
curl -X POST {{ url_for('collection', _external=True ) }} -H "Authorization: secret_api_key" -d '[ "example.com", "example2.com" ]'
```

To list all domain names, GET the list:

```bash
curl -X GET {{ url_for('collection', _external=True ) }} -H "Authorization: secret_api_key"
```

To list a single domain name, GET it:

```bash
curl -X GET {{ url_for('member', domain="example.com", _external=True ) }} -H "Authorization: secret_api_key"
```

To delete a domain name, DELETE it:

```bash
curl -X DELETE {{ url_for('member', domain="example.com", _external=True ) }} -H "Authorization: secret_api_key"
```
