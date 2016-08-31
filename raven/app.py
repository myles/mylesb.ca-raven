import os

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


app = create_app()

port = int(os.environ.get("PORT", 5000))
host = str(os.environ.get("HOST", '0.0.0.0'))

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
