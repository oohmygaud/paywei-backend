from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Sum
from apps.invoices.serializers import InvoiceSerializer
from apps.invoices.models import Invoice
from rest_framework import viewsets
from apps.users.permissions import IsOwner
from django.utils import timezone


# Create your views here.

class InvoiceViewSet(viewsets.ModelViewSet):
    model = Invoice
    permission_classes = (IsOwner,)
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

