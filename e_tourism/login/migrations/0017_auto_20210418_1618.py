# Generated by Django 3.1.7 on 2021-04-18 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_transactions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
    ]
