# Generated by Django 3.0.4 on 2020-04-27 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0025_auto_20200422_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='imagen',
            field=models.ImageField(default='interr.jpg', upload_to='imagenes_proyectos'),
        ),
    ]