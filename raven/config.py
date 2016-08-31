import json

class Config(object):
    DEBUG = True

    MAILGUN_DEFAULT_FROM = '<Raven> raven@mg.mylesbraithwaite.com'
    MAILGUN_DOMAIN = 'mg.mylesbraithwaite.com'
    MAILGUN_API_KEY = 'key-91c3a0eaecb6e0214bcd201e0cd0f973'

    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = '6LfRiigTAAAAADn4oUneyMYcV7wMNB6k9VkvdY0_'
    RECAPTCHA_SECRET_KEY = '6LfRiigTAAAAACwdNwjdITJL2aOjMPQyqv-Jnblr'
    RECAPTCHA_TYPE = 'image'

    with open('config.json', 'r') as fobj:
        RAVEN_CONFIG = json.loads(fobj.read())
