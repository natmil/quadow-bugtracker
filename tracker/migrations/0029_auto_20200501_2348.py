# Generated by Django 3.0.4 on 2020-05-01 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0028_auto_20200501_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(choices=[('ACTIVO', 'Activo'), ('FINALIZADO', 'Finalizado')], default='ABIERTO', max_length=10),
        ),
    ]
