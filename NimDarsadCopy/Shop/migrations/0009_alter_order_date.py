# Generated by Django 5.1.2 on 2024-11-28 09:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0008_ticket_delete_poshtibani_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 11, 28, 12, 52, 5, 895027)),
        ),
    ]
