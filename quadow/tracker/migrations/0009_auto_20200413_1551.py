# Generated by Django 3.0.4 on 2020-04-13 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_auto_20200413_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['prioridad']},
        ),
    ]