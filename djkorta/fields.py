#!/usr/bin/env python
# -*- coding: utf-8 -
"""
djkorta.fields
~~~~~~~~~~~~~~

:copyright: (c) 2012 by the Stefán Kjartansson, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from django import forms
from django.utils.checksums import luhn
from django.utils.translation import ugettext as _


class CreditCardField(forms.IntegerField):

    def clean(self, value):
        if value and (len(str(value)) < 13 or len(str(value)) > 16 or not luhn(value)):
            raise forms.ValidationError(_(u"Please enter in a valid credit card number."))
        return super(CreditCardField, self).clean(value)
