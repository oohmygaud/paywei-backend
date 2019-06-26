from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from uuid import uuid4
from apps.users.models import CustomUser
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail, mail_admins
from apps import model_base
from django.core.validators import MaxValueValidator
from djchoices import ChoiceItem, DjangoChoices

def makeKey():
    return str(uuid4()).replace('-', '')[:16].upper()

class Invoice(model_base.NicknamedBase):

    class InvoiceStatus(DjangoChoices):
        new = ChoiceItem('new', 'New')
        published = ChoiceItem('published', 'Published')
        partial_payment = ChoiceItem('partial_payment', 'Partial Payment')
        paid_in_full = ChoiceItem('paid_in_full', 'Paid in Full')


    objects = models.Manager()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='invoices')
    status = models.CharField(max_length=32, default='new', choices=InvoiceStatus.choices)
    recipient_email = models.CharField(max_length=64, null=True, blank=True)
    payee = models.CharField(max_length=64, null=True, blank=True)
    key = models.CharField(max_length=32, default=makeKey)
    archived_at = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    total_wei_due = models.DecimalField(max_digits=50, decimal_places=0)
    min_payment_threshold = models.PositiveIntegerField(blank=True, default=100, validators=[MaxValueValidator(100),])


    class Meta:
        ordering = ('-created_at',)

    
