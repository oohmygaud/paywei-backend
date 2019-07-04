from django.test import TestCase
from django.core import mail
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate
from apps.users.models import CustomUser as User, WhitelistAddress
from apps.invoices.models import Invoice
from datetime import datetime, timedelta
import json
import pytest
import io
from pprint import pprint

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
            'total_wei_due': 1000000000
        })

        force_authenticate(request, user=test_user)
        response= views.InvoiceViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(mail.outbox[-1].subject, 'Someone has sent you a bill on PayWei')

        request = factory.post('/invoices/', {
            'user': test_user.id,
            'pay_to': address.id,
            'recipient_email': email,
            'total_wei_due': 1000000000,
            'delivery': Invoice.DeliveryChoices.link
        })

        force_authenticate(request, user=test_user)
        response= views.InvoiceViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertNotEqual(mail.outbox[-1].subject, 'Someone has sent you a bill on PayWei')

