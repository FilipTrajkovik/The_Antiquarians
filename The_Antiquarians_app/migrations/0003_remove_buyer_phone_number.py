# Generated by Django 4.2.2 on 2023-07-13 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('The_Antiquarians_app', '0002_buyer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='phone_number',
        ),
    ]
