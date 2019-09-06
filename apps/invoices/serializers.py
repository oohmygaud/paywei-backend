from apps.invoices.models import Invoice, Payment, InvoiceItem
from rest_framework import serializers
import re

class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.PrimaryKeyRelatedField(read_only=True, required=False)

    class Meta:
        model = InvoiceItem
        fields = ('__all__')

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = ('__all__')

    def create(self, validated_data):
        item_data = validated_data.pop('invoice_items', [])
        invoice = Invoice.objects.create(**validated_data)
        for item in item_data:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice

    def validate_pay_to(self, value):
        if not value.status == 'verified':
            raise serializers.ValidationError({'pay_to': 'Must be a whitelist-verified address'})
        return value

    def validate(self, data):
        if data['pay_to'].user != data['user']:
            raise serializers.ValidationError({'pay_to': 'This address does not belong to you'})
        if self.instance and self.instance.status == 'agreed':
            raise serializers.ValidationError({ '_': 'This invoice has already been agreed upon'})
        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')



    