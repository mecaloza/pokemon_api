from django.db import models

# Create your models here.


class Pokemons(models.Model):

    # Requiered fields
    pokemon_id = models.AutoField(primary_key=True)
    pokemon_name = models.CharField(max_length=255)
    base_stats = models.TextField(blank=True, null=True)
    height = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    evolutions = models.CharField(max_length=255, null=True)
    prevolution = models.CharField(max_length=255, null=True)
