# Generated by Django 3.2.5 on 2021-07-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemons',
            fields=[
                ('pokemon_id', models.AutoField(primary_key=True, serialize=False)),
                ('pokemon_name', models.CharField(max_length=255)),
                ('base_stats', models.TextField(blank=True, null=True)),
                ('height', models.CharField(max_length=255)),
                ('weight', models.CharField(max_length=255)),
                ('evolutions', models.CharField(max_length=255, null=True)),
                ('prevolution', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
