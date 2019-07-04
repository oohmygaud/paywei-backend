from apps.invoices.models import Invoice, Payment
from rest_framework import serializers
import re

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('__all__')

    def validate_pay_to(self, value):
        if not value.status == 'verified':
            raise serializers.ValidationError({'pay_to': 'Must be a whitelist-verified address'})
        return value

    def validate(self, data):
        if data['pay_to'].user != data['user']:
            raise serializers.ValidationError({'pay_to': 'This address does not belong to you'})
            
        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')