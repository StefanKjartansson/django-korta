#!/usr/bin/env python
# -*- coding: utf-8 -
"""
djkorta.admin
~~~~~~~~~~~~~

:copyright: (c) 2012 by the Stefán Kjartansson, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _

from .models import Customer
from .forms import MONTHS, cc_clean
from .fields import CreditCardField


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        exclude = ('reference', 'expires', 'registered')

    number = CreditCardField(required=True,
        label=_(u"Card Number"))

    expiration_month = forms.ChoiceField(required=True,
        label=_(u'Month'), choices=MONTHS)

    expiration_year = forms.CharField(required=True,
        label=_(u'Year'), max_length=4)

    ccv = forms.IntegerField(required=True,
        label=_(u"CCV Number"),
        max_value=9999,
        widget=forms.TextInput(attrs={'size': '4'}))

    clean = cc_clean

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        i = super(CustomerForm, self).save(commit=False)
        i.credit_card = data['credit_card']
        i.save()
        return i


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['reference', 'expires', 'registered', 'order_count']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            kwargs.update({'form': CustomerForm})
        return super(CustomerAdmin, self).get_form(request, obj=obj, **kwargs)


admin.site.register(Customer, CustomerAdmin)
