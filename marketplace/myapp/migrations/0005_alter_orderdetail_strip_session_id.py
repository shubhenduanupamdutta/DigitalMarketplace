# Generated by Django 4.2.8 on 2023-12-23 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_orderdetail_stripe_payment_intent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='strip_session_id',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]
