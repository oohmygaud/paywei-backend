# Generated by Django 2.0 on 2019-09-18 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
        ('users', '0003_auto_20190904_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='default_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.WhitelistAddress'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='default_pricing_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='invoices.PaymentCurrency'),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='api_keys', to=settings.AUTH_USER_MODEL),
        ),
    ]
