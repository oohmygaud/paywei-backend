# Generated by Django 2.0 on 2019-06-27 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_auto_20190626_1545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='description',
            new_name='notes',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='nickname',
            new_name='title',
        ),
    ]