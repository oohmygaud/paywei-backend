# Generated by Django 2.0 on 2019-06-27 19:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20190627_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount_in_wei', models.DecimalField(decimal_places=0, max_digits=50)),
                ('usd_eth_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('block_hash', models.TextField()),
                ('block_number', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField()),
                ('gas', models.PositiveIntegerField()),
                ('gas_price', models.DecimalField(decimal_places=0, max_digits=50)),
                ('tx_hash', models.CharField(db_index=True, max_length=128)),
                ('tx_input', models.TextField()),
                ('nonce', models.PositiveIntegerField()),
                ('from_address', models.CharField(max_length=64)),
                ('to_address', models.CharField(max_length=64)),
                ('transaction_date_time', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
