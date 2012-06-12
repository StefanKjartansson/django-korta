#!/usr/bin/env python
# -*- coding: utf-8 -
"""
djkorta.forms
~~~~~~~~~~~~~

:copyright: (c) 2012 by the Stefán Kjartansson, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import datetime
from collections import namedtuple

from django import forms
from django.utils.translation import ugettext as _

from . import client
from .conf import settings
from .fields import CreditCardField
from .models import Order


#01 - 1 ... 12 - 12
MONTHS = [(i, i) for i in [str(i)
    if len(str(i)) > 1 else ('0%d' % i)
    for i in range(1, 13)]]

CreditCard = namedtuple('CreditCard', ['number', 'expires', 'ccv'])


def cc_clean(self):
    data = self.cleaned_data
    if not data.get('number', None):
        raise forms.ValidationError(
            _(u'Invalid number'))
    exp_year = data.get('expiration_year', None)
    if not exp_year:
        raise forms.ValidationError(
            _(u'Expiration date is invalid'))
    y = str(exp_year)
    m = data['expiration_month']
    if len(y) == 2:
        y = '20' + y
    expiration_date = datetime.date(int(y), int(m), 1)
    if expiration_date < datetime.date.today():
        raise forms.ValidationError(
            _(u'Expiration date is invalid'))
    data['expiration_date'] = expiration_date
    data['credit_card'] = CreditCard(number=str(data['number']),
        expires=data['expiration_date'].strftime('%y%m'),
        ccv=data['ccv'])
    return data


class PaymentInfoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(PaymentInfoForm, self).__init__(*args, **kwargs)
        #No need to restart on new year's eve
        self.fields['expiration_year'].choices = [
            (i[-2:], i) for i in [
                str(datetime.datetime.now().year + i)
                for i in range(0, settings.KORTA_CREDIT_CARD_YEARS)]]

    number = CreditCardField(required=True,
        label=_(u"Card Number"))
    expiration_month = forms.ChoiceField(required=True,
        label=_(u'Month'), choices=MONTHS)
    expiration_year = forms.ChoiceField(required=True,
        label=_(u'Year'), choices=())
    ccv = forms.IntegerField(required=True,
        label=_(u"CCV Number"),
        max_value=9999,
        widget=forms.TextInput(attrs={'size': '4'}))

    clean = cc_clean

    def process_order(self, order):
        data = self.clean()
        order.status = (Order.STATUS.SUCCESS
            if client.one_off(order, data['credit_card'])
                else Order.STATUS.ERROR)
        order.save()
        return order

    def process(self, amount, currency='ISK', currency_exponent=2):
        o = Order(amount=amount, currency_code=currency,
            currency_exponent=currency_exponent)
        o.save()
        return self.process_order(o)
