from flask_mailgun import Mailgun
from flask_recaptcha import ReCaptcha
from flask_bootstrap import Bootstrap

__app__ = ['recaptcha', 'mailgun', 'bootstrap',]

mailgun = Mailgun()
recaptcha = ReCaptcha()
bootstrap = Bootstrap()
