# Generated by Django 3.2.10 on 2022-01-27 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0005_alter_carona_dias'),
    ]

    operations = [
        migrations.AddField(
            model_name='carona',
            name='vagas',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
