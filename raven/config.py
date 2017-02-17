import os
import json


class Config(object):
    DEBUG = True

    SECRET_KEY = os.environ.get('RAVEN_SECRET_KEY', 'secret-key')

    CORS_ORIGINS = os.environ.get('RAVEN_CORS_ORIGINS', '*')
    CORS_RESOURCES = r'/api/*'

    CLEARBIT_KEY = os.environ.get('RAVEN_CLEARBIT_KEY')

    MAILGUN_DEFAULT_FROM = os.environ.get('RAVEN_MAILGUN_DEFAULT_FROM')
    MAILGUN_DOMAIN = os.environ.get('RAVEN_MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.environ.get('RAVEN_MAILGUN_API_KEY')

    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = os.environ.get('RAVEN_RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = os.environ.get('RAVEN_RECAPTCHA_SECRET_KEY')
    RECAPTCHA_TYPE = 'image'

    CLEARBIT_KEY = os.environ.get('RAVEN_CLEARBIT_KEY')

    OPBEAT_ORGANIZATION_ID = os.environ.get('RAVEN_OPBEAT_ORGANIZATION_ID')
    OPBEAT_APP_ID = os.environ.get('RAVEN_OPBEAT_APP_ID')
    OPBEAT_SECRET_TOKEN = os.environ.get('RAVEN_OPBEAT_SECRET_TOKEN')

    with open('config.json', 'r') as fobj:
        RAVEN_CONFIG = json.loads(fobj.read())
