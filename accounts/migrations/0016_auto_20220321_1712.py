# Generated by Django 3.0 on 2022-03-21 17:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20220321_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_licence_registration_date',
            field=models.CharField(blank=True, default=datetime.datetime(2022, 3, 21, 17, 12, 33, 742588, tzinfo=utc), max_length=200, null=True, verbose_name='Дата свидетельства о государственной регистрации'),
        ),
    ]
