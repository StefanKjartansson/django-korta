from django.conf import settings
from korta.defaults import CURRENCY_CODES
from korta.client import Client, korta_reference


KORTA_DEFAULT_CURRENCY = getattr(settings,
    'KORTA_DEFAULT_CURRENCY', 'USD')


def get_default_client():
    return Client(
        settings.KORTA_PEM_PATH,
        settings.KORTA_CA_PATH,
        settings.KORTA_USER,
        settings.KORTA_PASSWORD,
        settings.KORTA_SITE_ID,
        settings.KORTA_CARD_ACCEPTOR_ID,
        settings.KORTA_CARD_ACCEPTOR_IDENTITY,
        settings.KORTA_HOST,
        port=getattr(settings, 'KORTA_PORT', 8443),
        currency=KORTA_DEFAULT_CURRENCY)


make_reference = korta_reference
