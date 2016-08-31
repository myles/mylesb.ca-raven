import os
import json


class Config(object):
    DEBUG = True

    MAILGUN_DEFAULT_FROM = os.environ.get('RAVEN_MAILGUN_DEFAULT_FROM')
    MAILGUN_DOMAIN = os.environ.get('RAVEN_MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.environ.get('RAVEN_MAILGUN_API_KEY')

    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = os.environ.get('RAVEN_RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = os.environ.get('RAVEN_RECAPTCHA_SECRET_KEY')
    RECAPTCHA_TYPE = 'image'

    with open('config.json', 'r') as fobj:
        RAVEN_CONFIG = json.loads(fobj.read())
