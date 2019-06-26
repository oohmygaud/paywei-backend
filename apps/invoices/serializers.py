from apps.invoices.models import Invoice
from rest_framework import serializers
import re

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('__all__')