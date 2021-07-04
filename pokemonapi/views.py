from django.shortcuts import render
from django.urls.conf import include
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from pokemonapi.models import *

import requests
import json

# Create your views here.


class Pokemonview(APIView):
    def get(self, request, codigo):
        print("HOlis")
        url = "https://pokeapi.co/api/v2/evolution-chain/" + str(codigo)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            chain_evol = data["chain"]
            parameter_evol = 0
            while parameter_evol == 0:
                try:
                    print("pokmemon", chain_evol["species"]["name"])
                    pokemon_name = chain_evol["species"]["name"]
                    url_pokemon = "https://pokeapi.co/api/v2/pokemon/" + pokemon_name
                    response_pokemon = requests.get(url_pokemon)
                    if response_pokemon.status_code == 200:
                        pokemon_data = response_pokemon.json()
                        Pokemons.objects.create(
                            pokemon_id=pokemon_data["id"],
                            pokemon_name=pokemon_name,
                            base_stats=pokemon_data["stats"],
                            height=pokemon_data["height"],
                            weight=pokemon_data["weight"],
                        )

                    chain_evol = chain_evol["evolves_to"][0]

                except:
                    parameter_evol = 1
                    print("se acabo")

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

    def put(self, request):

        return Response(status=status.HTTP_200_OK)
