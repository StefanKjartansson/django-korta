import datetime
from collections import namedtuple

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from uni_form.helper import FormHelper
from uni_form.layout import *

from .fields import CreditCardField
from .utils import get_default_client
from .models import Order


#01 - 1 ... 12 - 12
MONTHS = [(i, i) for i in [str(i)
    if len(str(i)) > 1 else ('0%d' % i)
    for i in range(1, 13)]]


CC_YEARS = getattr(settings, 'CREDIT_CARD_YEARS', 15)


CreditCard = namedtuple('CreditCard', ['number', 'expires', 'ccv'])


class PaymentInfoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(PaymentInfoForm, self).__init__(*args, **kwargs)
        #No need to restart on new year's eve
        self.fields['expiration_year'].choices = [
            (i[-2:], i) for i in [
                str(datetime.datetime.now().year + i)
                for i in range(0, CC_YEARS)]]

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

    def clean(self):
        data = self.cleaned_data
        y = str(data['expiration_year'])
        m = data['expiration_month']
        if len(y) == 2:
            y = '20' + y
        expiration_date = datetime.date(int(y), int(m), 1)
        if expiration_date < datetime.date.today():
            raise forms.ValidationError(
                _(u'Expiration date is invalid'))
        data['expiration_date'] = expiration_date
        return data

    def process_order(self, order):
        data = self.clean()
        order.state = ('SUCCESS' if get_default_client().one_off(order,
            CreditCard(number=str(data['number']),
                expires=data['expiration_date'].strftime('%y%m'),
                ccv=data['ccv']))
            else 'ERROR')
        order.save()
        return order

    def process(self, amount, currency='ISK', currency_exponent=2):
        o = Order(amount=amount, _currency=currency,
            currency_exponent=currency_exponent)
        o.save()
        return self.process_order(o)

    @property
    def helper(self):
        helper = FormHelper()

        helper.form_id = 'id-payment-form'
        helper.form_class = 'korta-form'
        helper.form_method = 'post'
        helper.form_action = 'submit_payment'

        helper.layout = Layout(
            Fieldset(
                _(u'Payment Information'),
                HTML('{% include "djkorta/cc_types.html" %}'),
                'number',
                Row('expiration_month','expiration_year'),
                'ccv',
            ),
            ButtonHolder(
                Submit('submit', _(u'Checkout'),
                    css_class='button')
            )
        )
        return helper
