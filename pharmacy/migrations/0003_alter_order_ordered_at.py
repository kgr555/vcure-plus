# Generated by Django 3.2.6 on 2023-08-15 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0002_auto_20230815_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateField(default=datetime.datetime(2023, 8, 15, 17, 47, 21, 818394)),
        ),
    ]
