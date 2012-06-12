#!/usr/bin/env python
# -*- coding: utf-8 -
"""
djkorta.models.customer
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by the Stefán Kjartansson, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import datetime

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from model_utils.models import TimeStampedModel

from .. import client
from .base import ReferenceCommon
from .order import Order


class Customer(ReferenceCommon):

    expires = models.DateField(verbose_name=_(u'Date Expires'),
        null=True, blank=True)

    registered = models.DateField(verbose_name=_(u'Date Registered'),
        null=True, blank=True)

    def __init__(self, *args, **kwargs):
        self.credit_card = kwargs.pop('credit_card', None)
        super(Customer, self).__init__(*args, **kwargs)

    @property
    def duration(self):
        #todo, integrate with expires
        return 2

    @property
    def orders(self):
        return CustomerOrder.objects.filter(customer=self)

    @property
    def order_count(self):
        return self.orders.count()

    class Meta:
        verbose_name = _(u'Korta Customer')
        verbose_name_plural = _(u'Korta Customers')
        app_label = 'djkorta'

    def charge(self, amount, currency='ISK', currency_exponent=2):
        o = Order(amount=amount, currency_code=currency,
            currency_exponent=currency_exponent)
        o.save()
        CustomerOrder(customer=self, order=o).save()
        auth = client.request_authorization(o, reference=self.reference)
        cap = client.request_capture(auth)
        o.status = (Order.STATUS.SUCCESS if cap.action_code == '000' \
            else Order.STATUS.ERROR)
        o.save()
        return (o.status == Order.STATUS.SUCCESS)


@receiver(post_save, sender=Customer)
def register_customer(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    created = kwargs.pop('created', False)
    if not instance or not created:
        return
    if not hasattr(instance, 'credit_card'):
        raise Exception('Customer created without initial credit card')
    client.save_account(instance)
    instance.registered = datetime.datetime.now()
    instance.save()


@receiver(post_delete, sender=Customer)
def unregister_customer(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    if instance:
        client.delete_account(instance)


class CustomerOrder(TimeStampedModel):
    customer = models.ForeignKey(Customer)
    order = models.ForeignKey(Order)

    class Meta:
        verbose_name = _(u'Korta Customer Order')
        verbose_name_plural = _(u'Korta Customer Orders')
        app_label = 'djkorta'
