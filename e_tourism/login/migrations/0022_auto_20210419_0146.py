# Generated by Django 3.1.7 on 2021-04-18 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0021_auto_20210419_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='hashValue',
            field=models.CharField(default=0, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='nonce',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='prevHash',
            field=models.CharField(default=0, max_length=500, null=True),
        ),
    ]
