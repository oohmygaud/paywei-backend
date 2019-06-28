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
import json


# Create your views here.

class InvoiceViewSet(viewsets.ModelViewSet):
    model = Invoice
    permission_classes = (IsOwner,)
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


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
            invoice = Invoice.objects.get(pk=parameters['values']['invoice_id'])
        except:
            return Response({
                'status': 'failed',
                'errors': {'invoice_id': 'No such invoice'}
            })

        obj = PaymentSerializer(data={
            'invoice_id': invoice.id,
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
            'amount_in_wei': tx['value'],
            'usd_eth_price': tx['pricing_info']['price'],
            'parameters_json': tx['parameters_json'],
            'created_at': timezone.now()
        })
        if not obj.is_valid():
            return Response({
                'status': 'failed',
                'errors': obj.errors
            })
        obj.save()
        return Response({
            'status': 'ok',
            'details': obj.data
        })
