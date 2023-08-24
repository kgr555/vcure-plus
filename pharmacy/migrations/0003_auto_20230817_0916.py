# Generated by Django 3.2.6 on 2023-08-17 09:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0002_order_orderitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateField(default=datetime.datetime(2023, 8, 17, 9, 16, 14, 661450)),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pharmacy.order'),
        ),
    ]
