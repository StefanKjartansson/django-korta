from django.test import TestCase

from . import CreditCard
from .forms import PaymentInfoForm
from .models import Order, OrderException, Customer


class PaymentInfoFormTest(TestCase):

    def test_valid_creditcard(self):
        post_data = {
            'number': 4571999400007492,
            'expiration_month': '05',
            'expiration_year': '15',
            'ccv': 123,
        }
        f = PaymentInfoForm(post_data)
        self.assertEqual(f.is_valid(), True)

        #charge $1
        order = f.process(100, currency='USD')
        self.assertEqual(order.status, 'SUCCESS')
        self.assertEqual(Order.objects.successful().count(), 1)
        self.assertEqual(Order.objects.by_currency_code('USD') \
            .successful().count(), 1)
        with self.assertRaises(OrderException):
            order.amount = 200

    def test_invalid_creditcard(self):
        post_data = {
            'number': 4571999400007492,
            'expiration_month': '05',
            'expiration_year': '11',
            'ccv': 123,
        }
        self.assertEqual(PaymentInfoForm(post_data).is_valid(), False)

        post_data = {
            'number': 4571234400007492,
            'expiration_month': '05',
            'expiration_year': '15',
            'ccv': 123,
        }
        self.assertEqual(PaymentInfoForm(post_data).is_valid(), False)
        self.assertEqual(Order.objects.failed().count(), 0)

    def test_customer_order(self):
        c = Customer(credit_card=CreditCard('4571999400007492', 5, 14, 123))
        c.save()
        self.assertTrue(c.charge(2000))
        self.assertEqual(c.orders.count(), 1)
        self.assertEqual(c.order_count, 1)
        c.delete()
