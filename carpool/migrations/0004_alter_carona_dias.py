# Generated by Django 3.2.10 on 2022-01-27 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0003_usuario_avaliacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carona',
            name='dias',
            field=models.BinaryField(editable=True),
        ),
    ]