# Generated by Django 5.1.2 on 2024-10-28 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_stock_buy_price_alter_currentstockvalue_stock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfoliostock',
            name='current_value',
        ),
    ]
