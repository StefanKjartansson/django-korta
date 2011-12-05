from django.test import TestCase

from .forms import PaymentInfoForm


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
        self.assertEqual(order.state, 'SUCCESS')

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

    def test_helpers(self):
        f = PaymentInfoForm()
        self.assertIsNotNone(f.helper)
