# Generated by Django 3.1.7 on 2021-04-18 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0023_auto_20210419_0159'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Block_Chain',
        ),
        migrations.AddField(
            model_name='transaction',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
