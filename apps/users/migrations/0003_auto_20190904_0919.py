# Generated by Django 2.0 on 2019-09-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190708_1842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='whitelistaddress',
            old_name='revoked_at',
            new_name='archived_at',
        ),
        migrations.AlterField(
            model_name='whitelistaddress',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified'), ('denied', 'Denied'), ('archived', 'Archived')], default='pending', max_length=32),
        ),
    ]
