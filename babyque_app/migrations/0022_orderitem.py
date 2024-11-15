# Generated by Django 5.0.7 on 2024-10-29 06:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babyque_app', '0021_order_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='babyque_app.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='babyque_app.product')),
            ],
        ),
    ]
