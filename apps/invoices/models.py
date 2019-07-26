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
from django.core.mail import send_mail, mail_admins


def makeKey():
    return str(uuid4()).replace('-', '')[:16].upper()


class Invoice(model_base.TitledBase):

    class InvoiceStatus(DjangoChoices):
        new = ChoiceItem('new', 'New')
        published = ChoiceItem('published', 'Published')
        agreed = ChoiceItem('agreed', 'Agreed')
        partial_payment = ChoiceItem('partial_payment', 'Partial Payment')
        paid_in_full = ChoiceItem('paid_in_full', 'Paid in Full')
    
    class DeliveryChoices(DjangoChoices):
        email = ChoiceItem('email', 'Email')
        link = ChoiceItem('link', 'Link')
        

    objects = models.Manager()
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='invoices')
    status = models.CharField(
        max_length=32, default='new', choices=InvoiceStatus.choices)
    delivery = models.CharField(
        max_length=32, default='email', choices=DeliveryChoices.choices)
    recipient_email = models.CharField(max_length=64, null=True, blank=True)
    pay_to = models.ForeignKey(
        'users.WhitelistAddress', on_delete=models.DO_NOTHING, related_name='pay_to')
    key = models.CharField(max_length=32, default=makeKey)
    archived_at = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=512, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    agreed_at = models.DateTimeField(null=True, blank=True)
    invoice_amount_wei = models.DecimalField(max_digits=50, decimal_places=0)
    paid_amount_wei = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    min_payment_threshold = models.PositiveIntegerField(
        blank=True, default=100, validators=[MaxValueValidator(100), ])

    def save(self, *args, **kwargs):
        
        mail_admins(
            'New Invoice Created',
            'A new invoice was created on PayWei'
        )
        if(self.delivery == 'email' and self.status == 'published' and self.sent_date == None):
            send_mail(
                'Someone has sent you a bill on PayWei',
                'paywei.co/pay/' + self.id,
                'noreply@paywei.co',
                [self.recipient_email]
            )
            self.sent_date = timezone.now()
        self._update_paid_amount()
        super(Invoice, self).save(*args, **kwargs)

    def _update_paid_amount(self):
        self.paid_amount_wei = sum([p.amount_in_wei for p in self.payments.filter(status='confirmed')])
        if self.paid_amount_wei > 0 and self.status == 'agreed':
            self.status = 'partial_payment'
        if self.paid_amount_wei == self.invoice_amount_wei and self.status in ['agreed', 'partial_payment']:
            self.status = 'paid_in_full'
        

    class Meta:
        ordering = ('-created_at',)


class Payment(model_base.RandomPKBase):

    class PaymentStatus(DjangoChoices):
        new = ChoiceItem('new', 'New')
        confirmed = ChoiceItem('confirmed', 'Confirmed')

    objects = models.Manager()
    status = models.CharField(
        max_length=32, default='new', choices=PaymentStatus.choices)
    invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.DO_NOTHING)
    amount_in_wei = models.DecimalField(max_digits=50, decimal_places=0)
    usd_eth_price = models.DecimalField(max_digits=20, decimal_places=10)
    block_hash = models.TextField()
    block_number = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    gas = models.PositiveIntegerField()
    gas_price = models.DecimalField(max_digits=50, decimal_places=0)
    tx_hash = models.CharField(max_length=128, db_index=True)
    tx_input = models.TextField()
    parameters_json = models.TextField(null=True, blank=True)
    nonce = models.PositiveIntegerField()
    from_address = models.CharField(max_length=64)
    to_address = models.CharField(max_length=64)
    transaction_date_time = models.DateTimeField()

    @property
    def parameters(self):
        try:
            return json.loads(self.parameters_json)
        except:
            return {}
    
    class Meta:
        ordering = ('-created_at',)

    
