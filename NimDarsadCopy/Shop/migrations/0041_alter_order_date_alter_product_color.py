# Generated by Django 5.1.2 on 2024-12-09 15:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0040_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 12, 9, 18, 55, 51, 837820)),
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]
