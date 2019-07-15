from django.test import TestCase
from django.core import mail
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
from apps.users.models import CustomUser as User, WhitelistAddress
from apps.invoices.models import Invoice, Payment
from datetime import datetime, timedelta
import json
import pytest
import io
from pprint import pprint

def get_payment_data(invoice, amount=None):
    data = json.load(open('tests/fixtures/testFullPayment.json'))
    data['transaction']['value'] = amount or invoice.invoice_amount_wei

    params = json.loads(data['transaction']['parameters_json'])
    params['values']['invoiceId'] = invoice.id

    data['transaction']['parameters_json'] = json.dumps(params)
    return data


@pytest.mark.django_db
class InvoiceTestCase(TestCase):
    @classmethod
    def setup_class(cls):
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
    
    def test_send_invoice(self):
        from apps.invoices import views

        factory = APIRequestFactory()
        test_user = User.objects.create_user(username="audrey", email="test@audrey.com", password="audrey")
        email = 'test@paywei.co'

        address = WhitelistAddress.objects.create(
            address='0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8',
            nickname='Barbara',
            user=test_user,
            status=WhitelistAddress.AddressStatus.verified
        )

        request = factory.post('/invoices/', {
            'user': test_user.id,
            'pay_to': address.id,
            'recipient_email': email,
            'invoice_amount_wei': 1000000000,
            'status': 'published'
        })

        force_authenticate(request, user=test_user)
        response= views.InvoiceViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(Invoice.objects.count(), 1)

        #Email subjects: New User Registration, New Invoice Created, Someone has sent you a bill on PayWei
        self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(mail.outbox[-1].subject, 'Someone has sent you a bill on PayWei')

        request = factory.post('/invoices/', {
            'user': test_user.id,
            'pay_to': address.id,
            'recipient_email': email,
            'invoice_amount_wei': 1000000000,
            'delivery': Invoice.DeliveryChoices.link
        })

        force_authenticate(request, user=test_user)
        response= views.InvoiceViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 4)
        self.assertNotEqual(mail.outbox[-1].subject, 'New Invoice Created')


    #test paying an invoice in full
    #   if I create an invoice, and a payment is made
    def test_pay_invoice_in_full(self):
        from apps.invoices import views

        factory = APIRequestFactory()
        test_user = User.objects.create_user(username="audrey", email="test@audrey.com", password="audrey")
        email = 'test@paywei.co'

        address = WhitelistAddress.objects.create(
            address='0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8',
            nickname='Barbara',
            user=test_user,
            status=WhitelistAddress.AddressStatus.verified
        )

        request = factory.post('/invoices/', {
            'user': test_user.id,
            'pay_to': address.id,
            'recipient_email': email,
            'invoice_amount_wei': 1000000000,
            'status': 'agreed'
        })

        force_authenticate(request, user=test_user)
        invoice_response= views.InvoiceViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(Invoice.objects.count(), 1)

        invoice = Invoice.objects.first()
        self.assertEqual(invoice.status, 'agreed')

        payment = factory.post('/api/payment_received/', get_payment_data(invoice), format='json')
        payment_response= views.PaymentNotification.as_view()(payment)
    
    #   should mark the invoice status paid
        invoice = Invoice.objects.first()
        self.assertEqual(invoice.status, 'paid_in_full')
    #   should have no balance due
        self.assertEqual(invoice.invoice_amount_wei - invoice.paid_amount_wei, 0)
    #   should have an associated payment
        self.assertEqual(Payment.objects.count(), 1)

    #test paying an invoice partially
    #   if I make a partial payment on an invoice
    def test_pay_invoice_partially(self):
        from apps.invoices import views

        factory = APIRequestFactory()
        test_user = User.objects.create_user(username="audrey", email="test@audrey.com", password="audrey")
        email = 'test@paywei.co'

        address = WhitelistAddress.objects.create(
            address='0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8',
            nickname='Barbara',
            user=test_user,
            status=WhitelistAddress.AddressStatus.verified
        )

        request = factory.post('/invoices/', {
            'user': test_user.id,
            'pay_to': address.id,
            'recipient_email': email,
            'invoice_amount_wei': 1000000000,
            'status': 'agreed',
            'min_payment_threshold': 500000000 
        })

        force_authenticate(request, user=test_user)
        invoice_response= views.InvoiceViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(Invoice.objects.count(), 1)
        invoice = Invoice.objects.first()

        payment = factory.post('/api/payment_received/', get_payment_data(invoice, 500000000), format='json')
        payment_response= views.PaymentNotification.as_view()(payment)

    #   should have the correct balance due
        self.assertEqual(invoice.invoice_amount_wei - invoice.paid_amount_wei, 500000000)
    #   should have an associated payment
    #   should make the invoice status partial payment
    #   if I make another partial payment on an invoice
    #   should have the correct balance due
    #   should have 2 associated payment
    #   should make the invoice status partial payment
    #   if I make a final partial payment on an invoice
    #   should have no balance due
    #   should have 3 associated payment
    #   should make the invoice status paid


    #test can't change agreed terms
    #   if an invoice has been agreed to
    #   should not be able to edit invoice details

    #test save invoice without sending
    #   if I save an invoice 
    #   should have an outbox of 0
    #   should have added an invoice to the invoice list
    #   should have an invoice status- new

    #test user api permissions
    #   if I make 2 users, and they make invoices
    #   they should not be able to list eachothers invoices
    #   they should not be able to list eachothers payments
    #   they should not be able to see eachothers invoice or payment details
    #   they should not be able to create an invoice with the other user's id 

