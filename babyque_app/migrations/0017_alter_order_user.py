# Generated by Django 5.0.7 on 2024-10-28 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babyque_app', '0016_remove_payment_order_remove_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='babyque_app.user'),
        ),
    ]
