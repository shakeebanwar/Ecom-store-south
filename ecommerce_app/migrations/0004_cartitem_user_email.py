# Generated by Django 4.0.4 on 2022-05-17 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0003_remove_order_address_order_agree'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='user_email',
            field=models.EmailField(default=0, max_length=254),
        ),
    ]
