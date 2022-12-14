# Generated by Django 3.2.10 on 2022-02-01 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0008_alter_carona_dias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carona',
            name='enderecoDestino',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carpool.endereco'),
        ),
        migrations.AlterField(
            model_name='carona',
            name='enderecoSaida',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='enderecoSaida', to='carpool.endereco'),
        ),
    ]
