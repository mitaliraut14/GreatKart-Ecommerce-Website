# Generated by Django 4.1.5 on 2023-01-26 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gkapp', '0005_alter_cart_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pid',
            field=models.CharField(max_length=100),
        ),
    ]
