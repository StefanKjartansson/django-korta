#!/usr/bin/env python
# -*- coding: utf-8 -
# flake8: noqa
"""
djkorta.conf
~~~~~~~~~~~~

:copyright: (c) 2012 by the Stefán Kjartansson, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from django.conf import settings
from appconf import AppConf


class KortaConf(AppConf):
    DEFAULT_CURRENCY = "ISK"

    HOST = 'test.kortathjonustan.is'
    PORT = '8443'
    CREDIT_CARD_YEARS = 15

    CARD_TYPES = {
        'Visa': '/^4/',
        'Master': '/^5[1-5]/',
        'American Express': '/^3(4|7)/',
        'Discover': '/^6011/',
        'Diners Club': '/^(30[0-5]|36|38)/',
        'JCB': '/^(3|2131|1800)/',
    }

    class Meta:
        prefix = 'korta'
