# Generated by Django 3.1.7 on 2021-04-18 20:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0022_auto_20210419_0146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block_Chain',
            fields=[
                ('block_number', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('public_key', models.CharField(default=0, max_length=500, null=True)),
                ('address', models.CharField(default=0, max_length=500)),
                ('category', models.CharField(max_length=200, null=True)),
                ('amount', models.IntegerField()),
                ('hashValue', models.CharField(default=0, max_length=500, null=True)),
                ('prevHash', models.CharField(default=0, max_length=500, null=True)),
                ('nonce', models.IntegerField(default=0, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='hashValue',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='nonce',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='prevHash',
        ),
    ]
