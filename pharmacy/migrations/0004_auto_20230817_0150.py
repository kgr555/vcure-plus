# Generated by Django 3.2.6 on 2023-08-16 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0003_alter_order_ordered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateField(default=datetime.datetime(2023, 8, 17, 1, 50, 59, 299597)),
        ),
    ]
