# Generated by Django 4.1.5 on 2023-01-25 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gkapp', '0002_cart_order_verf_email_verf_mobile_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gkapp.product'),
        ),
    ]
