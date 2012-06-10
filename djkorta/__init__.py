#!/usr/bin/env python
# -*- coding: utf-8 -
# flake8: noqa
"""
djkorta
~~~~~~~

"""
from __future__ import absolute_import

from .conf import settings

from korta import Client, korta_reference
from korta.defaults import CURRENCY_CODES


if hasattr(settings, 'KORTA_URL'):
    client = Client.init_from_url(settings.KORTA_URL)
else:
    client = Client(
        settings.KORTA_USER,
        settings.KORTA_USER_PASSWORD,
        settings.KORTA_HOST,
        settings.KORTA_PORT,
        settings.KORTA_SITE_ID,
        settings.KORTA_CARD_ACCEPTOR_ID,
        settings.KORTA_CARD_ACCEPTOR_IDENTITY,
        settings.KORTA_PEM,
        settings.KORTA_DEFAULT_CURRENCY)
