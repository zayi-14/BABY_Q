# Generated by Django 5.0.7 on 2024-10-29 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babyque_app', '0019_remove_payment_order_remove_order_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
