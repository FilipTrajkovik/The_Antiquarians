# Generated by Django 4.2.2 on 2023-07-15 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_Antiquarians_app', '0007_remove_buyer_password_remove_product_posted_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Mebel', 'Мебел'), ('Nakit', 'Накит'), ('Chasovnici', 'Часовници'), ('Kujnski pribor', 'Кујнски прибор'), ('Dekorativni raboti', 'Декоративни работи'), ('Interior', 'Интериор'), ('Muzichki instrumenti', 'Музички инструменти'), ('Igrachki', 'Играчки'), ('Tekstil', 'Текстил')], max_length=255),
        ),
    ]