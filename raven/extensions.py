from flask_cors import CORS
from flask_dotenv import DotEnv
from flask_mailgun import Mailgun
from flask_recaptcha import ReCaptcha
from flask_bootstrap import Bootstrap
from opbeat.contrib.flask import Opbeat

__app__ = ['cors', 'mailgun', 'recaptcha', 'bootstrap', 'opbeat']

cors = CORS()
env = DotEnv()
mailgun = Mailgun()
recaptcha = ReCaptcha()
bootstrap = Bootstrap()
opbeat = Opbeat()
