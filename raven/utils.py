import clearbit

from flask import current_app


def get_clearbit_data(email):
    clearbit.key = current_app.config['CLEARBIT_KEY']
    return clearbit.Enrichment.find(email=email, stream=True)
