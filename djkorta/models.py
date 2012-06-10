#!/usr/bin/env python
# -*- coding: utf-8 -
"""
djkorta.models
~~~~~~~~~~~~~~

"""
from __future__ import absolute_import

from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext as _

from model_utils.models import StatusModel
from model_utils import Choices

from . import korta_reference, CURRENCY_CODES
from .conf import settings


AVAILABLE_CURRENCIES = (
    ('DDK', _(u'Danish Krona')),
    ('EUR', _(u'Euro')),
    ('GBP', _(u'Pound Sterling')),
    ('ISK', _(u'Icelandic Krona')),
    ('NOK', _(u'Norwegian Krona')),
    ('SEK', _(u'Swedish Krona')),
    ('USD', _(u'United States Dollar')),
)


class ReferenceCommon(models.Model):
    """
    Abstract model for Korta related classes, all reference
    generation is delegated here.
    """

    def __init__(self, *args, **kwargs):
        if not 'reference' in kwargs.keys():
            ref = korta_reference()
            while self.__class__.objects.filter(reference=ref).exists():
                ref = korta_reference()
            kwargs['reference'] = ref
        super(ReferenceCommon, self).__init__(*args, **kwargs)

    reference = models.CharField(verbose_name=_(u'Reference'), max_length=20,
        unique=True, db_index=True)

    date_created = models.DateTimeField(verbose_name=_(u'Date Created'),
        auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name=_(u'Date Edited'),
        auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-date_created', ]


class Customer(ReferenceCommon):
    expires = models.DateField(verbose_name=_(u'Date Expires'))


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
        self.decimal_amount = Decimal(value) / self.decimal_exponent

    @property
    def decimal_exponent(self):
        return Decimal('1%s' % ('0' * self.currency_exponent))

    @property
    def currency(self):
        return CURRENCY_CODES[self.currency_code]

    class Meta:
        verbose_name = _(u'Korta Order')
        verbose_name_plural = _(u'Korta Orders')

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


class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer)
    order = models.ForeignKey(Order)
    date_created = models.DateTimeField(verbose_name=_(u'Date Created'),
        auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name=_(u'Date Edited'),
        auto_now=True)
