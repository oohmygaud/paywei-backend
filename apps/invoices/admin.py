from django.contrib import admin
from apps.invoices.models import Invoice, Payment

admin.site.register(Invoice)
admin.site.register(Payment)