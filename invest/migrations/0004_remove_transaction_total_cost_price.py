# Generated by Django 4.2.6 on 2023-10-25 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invest", "0003_transaction_cost_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="transaction", name="total_cost_price",),
    ]
