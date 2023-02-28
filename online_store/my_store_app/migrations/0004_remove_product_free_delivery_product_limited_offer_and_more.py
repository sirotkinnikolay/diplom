# Generated by Django 4.1.7 on 2023-02-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store_app', '0003_product_limited_edition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='free_delivery',
        ),
        migrations.AddField(
            model_name='product',
            name='limited_offer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='limited_edition',
            field=models.BooleanField(default=False),
        ),
    ]
