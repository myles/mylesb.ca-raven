from six.moves.urllib.parse import urlparse

from flask import (Blueprint, request, render_template, current_app,
                   make_response, jsonify)

from raven.extensions import recaptcha, mailgun

backend = Blueprint('backend', __name__)


def resp_json(data, code=200):
    return make_response(jsonify(data), code)


@backend.route('/<string:site_uuid>', methods=['POST'])
def api(site_uuid):
    raven_config = current_app.config.get('RAVEN_CONFIG')
    site = raven_config.get(site_uuid)

    referral = urlparse(request.headers.get("Referer"))

    if not referral.netloc in site['domains']:
        return resp_json({'error': 'Unauthorized referral domain.'}, code=403)

    if not recaptcha.verify():
        return resp_json({'error': 'reCaptcha failed to verify.'}, code=403)

    form = request.form

    data = {
        'from': current_app.config.get('MAILGUN_DEFAULT_FROM'),
        'to': site['email_to'],
    }

    msg_subject_tpl = site.get('tpl_subject', 'email/raven-subject.txt')
    msg_text_tpl = site.get('tpl_msg_plain', 'email/raven-text.txt')

    data['subject'] = render_template(msg_subject_tpl, form=form, site=site)
    data['text'] = render_template(msg_text_tpl, form=form, site=site)

    if site.get('tpl_msg_html', None):
        data['html'] = render_template(site.get('tpl_msg_html'),
                                       form=form, site=site)

    mailgun.send_email(**data)

    return resp_json({'sent': 'ok'}, 200)
