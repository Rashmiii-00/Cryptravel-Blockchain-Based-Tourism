# Generated by Django 3.1.7 on 2021-04-18 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_auto_20210418_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='public_key',
        ),
    ]
