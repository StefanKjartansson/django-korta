from django.db import models
from django.utils.translation import ugettext as _

from .utils import make_reference, CURRENCY_CODES


AVAILABLE_CURRENCIES = (
    ('DDK', _(u'Danish Krona')),
    ('EUR', _(u'Euro')),
    ('GBP', _(u'Sterling Pound')),
    ('ISK', _(u'Icelandic Krona')),
    ('NOK', _(u'Norwegian Krona')),
    ('SEK', _(u'Swedish Krona')),
    ('USD', _(u'United States Dollar')),
)

ORDER_STATES = (
    ('NOT_SENT', _(u'Not Sent')),
    ('ERROR', _(u'Error')),
    ('SUCCESS', _(u'Successful')),
)


class ReferenceCommon(models.Model):
    """
    Abstract model for Korta related classes, all reference
    generation is delegated here.
    """

    def __init__(self, *args, **kwargs):
        if not 'reference' in kwargs.keys():
            ref = make_reference()
            while self.__class__.objects.filter(reference=ref).exists():
                ref = make_reference()
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


class OrderInfo(ReferenceCommon):

    amount = models.DecimalField(verbose_name=_(u'Amount'),
        max_digits=19, decimal_places=2)
    _currency = models.CharField(verbose_name=_(u'Currency'),
        max_length=3, choices=AVAILABLE_CURRENCIES)
    currency_exponent = models.IntegerField(
        verbose_name=_(u'Currency Exponent'),
        default=2)
    state = models.CharField(verbose_name=_(u'State'), max_length=16,
        choices=ORDER_STATES, default='NOT_SENT')

    @property
    def currency(self):
        return CURRENCY_CODES[self._currency]

    class Meta:
        verbose_name = _(u'Korta Order')
        verbose_name_plural = _(u'Korta Orders')
