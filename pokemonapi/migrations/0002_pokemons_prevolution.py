# Generated by Django 2.1.1 on 2021-07-06 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemonapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemons',
            name='prevolution',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
