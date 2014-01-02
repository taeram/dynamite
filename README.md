Dynamite
========

Dynamite is a Python powered Domain Name Monitoring service.

Requirements
============
You'll need the following:

* A [Heroku](https://www.heroku.com/) account, if you want to deploy to Heroku.
* [Python 2.7.3](http://www.python.org/)
* [pip](https://github.com/pypa/pip)
* [Virtualenv](https://github.com/pypa/virtualenv)

Setup
=====
Local development setup:
```bash
    # Clone the repo
    git clone https://github.com/taeram/dynamite.git

    cd ./dynamite/

    # Setup and activate virtualenv
    virtualenv .venv
    source ./.venv/bin/activate

    # Install the pip requirements
    pip install -r requirements.txt

    # Create the development database (SQLite by default)
    python manage.py database create

    # Start the daemon, prefixing with the required environment variables
    NOTIFY_EMAIL="you@example.com" python daemon.py

    # Start the application, prefixing with the required environment variables
    API_KEY="secret_api_key" python server.py
```

Heroku setup:
```bash
    # Clone the repo
    git clone https://github.com/taeram/dynamite.git

    cd ./dynamite/

    # Create your Heroku app, and the addons
    heroku apps:create
    heroku addons:add heroku-postgresql
    heroku addons:add mailgun

    # Promote your postgres database (your URL name may differ)
    heroku pg:promote HEROKU_POSTGRESQL_RED_URL

    # Set an "API key" for authorization
    heroku config:set API_KEY="secret_api_key"

    # Set your notification email
    heroku config:set NOTIFY_EMAIL="taeram@example.com"

    # Set the flask environment
    heroku config:set FLASK_ENV=production

    # Push to Heroku
    git push heroku master
    
    # Create the production database
    heroku run python manage.py database create
```

Usage
=====

To add domain names, POST a JSON array:

```bash
curl -X POST http://your-domain.com/domain -H "Authorization: secret_api_key" -d '[ "example.com", "example2.com" ]'
```

To list all domain names, GET the list:

```bash
curl -X GET http://your-domain.com/domain -H "Authorization: secret_api_key"
```

To list a single domain name, GET it:

```bash
curl -X GET http://your-domain.com/domain/example.com -H "Authorization: secret_api_key"
```

To delete a domain name, DELETE it:

```bash
curl -X DELETE http://your-domain.com/domain/example.com -H "Authorization: secret_api_key"
```

Notifications
=============

When the WHOIS record for a domain has changed, Dynamite will email you a diff of the changes at your NOTIFY_EMAIL address:

```
example.com changes:
--- old-whois.txt
+++ new-whois.txt
@@ -216,15 +216,6 @@
-  Expiration Date: 21-nov-2013
+  Expiration Date: 21-nov-2014
```


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/taeram/dynamite/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

