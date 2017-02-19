from os import environ

from flask import Flask

from raven.config import Config
from raven.extensions import *
from raven.blueprints import *


def create_app(configfile=None):
    app = Flask(__name__)

    app.config.from_object(Config.init_app(app))

    cors.init_app(app)
    mailgun.init_app(app)
    recaptcha.init_app(app)
    bootstrap.init_app(app)
    opbeat.init_app(app)

    app.register_blueprint(blueprint_frontend)
    app.register_blueprint(blueprint_backend, url_prefix='/api')

    return app


app = create_app()

port = int(environ.get("PORT", 5000))
host = str(environ.get("HOST", '0.0.0.0'))

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
