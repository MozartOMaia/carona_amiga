# Generated by Django 3.2.10 on 2022-01-27 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carona',
            name='passageiros',
            field=models.ManyToManyField(blank=True, related_name='passageiro', to='carpool.Usuario'),
        ),
    ]
