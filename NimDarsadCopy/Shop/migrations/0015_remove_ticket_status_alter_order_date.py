# Generated by Django 5.1.2 on 2024-11-28 09:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0014_rename_username_ticket_user_alter_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='status',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 11, 28, 13, 12, 12, 693148)),
        ),
    ]
