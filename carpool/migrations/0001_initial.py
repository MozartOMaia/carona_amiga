# Generated by Django 3.2.10 on 2022-01-27 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('horario', models.TimeField()),
                ('descricao', models.CharField(max_length=400)),
                ('dias', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=2)),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=4)),
                ('bairro', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=11)),
                ('cnh', models.CharField(max_length=11)),
                ('telefone', models.CharField(max_length=11)),
                ('carro', models.BooleanField()),
                ('email', models.CharField(max_length=50)),
                ('nomeUsuario', models.CharField(max_length=50)),
                ('bio', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='MensagemUsuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('diaHora', models.DateTimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='carpool.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='MensagemCarona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('diaHora', models.DateTimeField()),
                ('carona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool.carona')),
            ],
        ),
        migrations.AddField(
            model_name='carona',
            name='enderecoDestino',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carpool.endereco'),
        ),
        migrations.AddField(
            model_name='carona',
            name='enderecoSaida',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='enderecoSaida', to='carpool.endereco'),
        ),
        migrations.AddField(
            model_name='carona',
            name='motorista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='motorista', to='carpool.usuario'),
        ),
        migrations.AddField(
            model_name='carona',
            name='passageiros',
            field=models.ManyToManyField(related_name='passageiro', to='carpool.Usuario'),
        ),
    ]