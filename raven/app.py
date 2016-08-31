from flask import Flask

from raven.extensions import *
from raven.blueprints import *


def create_app(configfile=None):
    app = Flask(__name__)

    app.config.from_object('raven.config.Config')

    mailgun.init_app(app)
    recaptcha.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(blueprint_frontend)
    app.register_blueprint(blueprint_backend, url_prefix='/api')

    return app
