# Generated by Django 3.2.10 on 2022-01-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0004_alter_carona_dias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carona',
            name='dias',
            field=models.CharField(max_length=7),
        ),
    ]