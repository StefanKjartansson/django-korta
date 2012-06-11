#!/usr/bin/env python
# -*- coding: utf-8 -
"""
djkorta.models.order
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by the Stefán Kjartansson, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from decimal import Decimal

from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext as _

from model_utils.managers import PassThroughManager
from model_utils.models import StatusModel
from model_utils import Choices

from .base import ReferenceCommon
from .. import CURRENCY_CODES
from ..conf import settings


AVAILABLE_CURRENCIES = (
    ('DDK', _(u'Danish Krona')),
    ('EUR', _(u'Euro')),
    ('GBP', _(u'Pound Sterling')),
    ('ISK', _(u'Icelandic Krona')),
    ('NOK', _(u'Norwegian Krona')),
    ('SEK', _(u'Swedish Krona')),
    ('USD', _(u'United States Dollar')),
)


class OrderException(Exception):
    """
    """


class OrderQuerySet(QuerySet):

    def by_currency_code(self, currency_code):
        return self.filter(currency_code=currency_code)

    def successful(self):
        return self.filter(status=Order.STATUS.SUCCESS)

    def failed(self):
        return self.filter(status=Order.STATUS.ERROR)


class Order(StatusModel, ReferenceCommon):

    STATUS = Choices(
        ('NOT_SENT', _(u'Not Sent')),
        ('ERROR', _(u'Error')),
        ('SUCCESS', _(u'Successful')),
    )

    @property
    def amount(self):
        return Decimal(str(self.decimal_amount)) * \
            self.decimal_exponent

    @amount.setter
    def amount(self, value):
        if self.status == Order.STATUS.SUCCESS:
            raise OrderException('Order already fulfilled')
        self.decimal_amount = Decimal(value) / self.decimal_exponent

    @property
    def decimal_exponent(self):
        return Decimal('1%s' % ('0' * self.currency_exponent))

    @property
    def currency(self):
        return CURRENCY_CODES[self.currency_code]

    def process(self):
        pass

    objects = PassThroughManager.for_queryset_class(OrderQuerySet)()

    class Meta:
        verbose_name = _(u'Korta Order')
        verbose_name_plural = _(u'Korta Orders')
        app_label = 'djkorta'

    decimal_amount = models.DecimalField(verbose_name=_(u'Amount'),
        max_digits=19, decimal_places=2)

    currency_code = models.CharField(
        verbose_name=_(u'Currency'),
        max_length=3,
        choices=AVAILABLE_CURRENCIES,
        default=settings.KORTA_DEFAULT_CURRENCY)

    currency_exponent = models.IntegerField(
        verbose_name=_(u'Currency Exponent'),
        default=2)
