# Generated by Django 3.2 on 2021-04-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_wallet_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prevtrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('pname', models.CharField(max_length=200)),
                ('month', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
            ],
        ),
    ]