from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Sum
from apps.invoices.serializers import InvoiceSerializer, PaymentSerializer
from apps.invoices.models import Invoice, Payment
from rest_framework import viewsets
from apps.users.permissions import IsOwner
from django.utils import timezone
from rest_framework.decorators import action
import json


# Create your views here.

class InvoiceViewSet(viewsets.ModelViewSet):
    model = Invoice
    permission_classes = (IsOwner,)
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=['post'])
    def agree(self, request, pk=None):
        obj = self.get_object()
        if obj.status in ['new', 'published']:
            obj.status = 'agreed'
            obj.save()
            return Response(self.serializer_class(obj).data)
        else:
            return Response({'error': 'unable to agree to invoice'})

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Invoice.objects.none()
        return Invoice.objects.filter(user=self.request.user)
        

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    model = Payment
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Payment.objects.none()
        return Payment.objects.filter(invoice__user=self.request.user)


# TODO: SECURITY ALERT!
# We need to add an AdminEmail when a Payment is received in an invoice that is not Agreed
# because this should basically never happen! It is indicative of an attack on the service!


# TODO: Need to add support for Confirmations; right now, all payments are Confirmed

class PaymentNotification(APIView):
    def post(self, request, format=None):
        tx = request.data['transaction']
        if not tx['parameters_json']:
            return Response({
                'status': 'failed',
                'errors': {'parameters_json': 'No function parameters'}
            })

        parameters = json.loads(tx['parameters_json'])
        try:
            invoice = Invoice.objects.get(pk=parameters['values']['invoiceId'])
        except:
            return Response({
                'status': 'failed',
                'errors': {'invoice_id': 'No such invoice'}
            })

        obj = PaymentSerializer(data={
            'invoice': invoice.id,
            'block_hash': tx['block_hash'],
            'block_number': tx['block_number'],
            'from_address': tx['from_address'],
            'gas': tx['gas'],
            'gas_price': tx['gas_price'],
            'tx_hash': tx['tx_hash'],
            'tx_input': tx['tx_input'],
            'nonce': tx['nonce'],
            'to_address': tx['to_address'],
            'transaction_date_time': tx['created_at'],
            'amount_in_wei': int(tx['value']),
            'usd_eth_price': tx['pricing_info']['price'],
            'parameters_json': tx['parameters_json'],
            'status': 'confirmed',
            'created_at': timezone.now()
        })
        if not obj.is_valid():
            return Response({
                'status': 'failed',
                'errors': obj.errors
            })
        obj.save()
        invoice.save()
        return Response({
            'status': 'ok',
            'details': obj.data
        })