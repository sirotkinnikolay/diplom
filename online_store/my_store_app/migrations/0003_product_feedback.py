# Generated by Django 4.1.7 on 2023-03-01 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store_app', '0002_rename_reviews_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='feedback',
            field=models.IntegerField(default=0),
        ),
    ]