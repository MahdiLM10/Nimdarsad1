# Generated by Django 5.1.2 on 2024-12-04 07:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0029_alter_order_date_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 12, 4, 10, 46, 36, 99001)),
        ),
    ]
