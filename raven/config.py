import json
from os import environ
from os.path import join, dirname

from flask_dotenv import DotEnv


class Config(object):
    DEBUG = True

    SECRET_KEY = environ.get('RAVEN_SECRET_KEY', 'secret-key')

    CORS_ORIGINS = environ.get('RAVEN_CORS_ORIGINS', '*')
    CORS_RESOURCES = r'/api/*'

    MAILGUN_DEFAULT_FROM = environ.get('RAVEN_MAILGUN_DEFAULT_FROM')
    MAILGUN_DOMAIN = environ.get('RAVEN_MAILGUN_DOMAIN')
    MAILGUN_API_KEY = environ.get('RAVEN_MAILGUN_API_KEY')

    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = environ.get('RAVEN_RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = environ.get('RAVEN_RECAPTCHA_SECRET_KEY')
    RECAPTCHA_TYPE = 'image'

    CLEARBIT_KEY = environ.get('RAVEN_CLEARBIT_KEY')

    OPBEAT_ORGANIZATION_ID = environ.get('RAVEN_OPBEAT_ORGANIZATION_ID')
    OPBEAT_APP_ID = environ.get('RAVEN_OPBEAT_APP_ID')
    OPBEAT_SECRET_TOKEN = environ.get('RAVEN_OPBEAT_SECRET_TOKEN')

    with open('config.json', 'r') as fobj:
        RAVEN_CONFIG = json.loads(fobj.read())

    @classmethod
    def init_app(self, app):
        env = DotEnv()
        env.init_app(app, env_file=join(dirname(__file__), '../.env'))
