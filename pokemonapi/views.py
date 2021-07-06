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

        url = "https://pokeapi.co/api/v2/evolution-chain/" + str(codigo)
        response = requests.get(url)
        content = []

        if response.status_code == 200:
            data = response.json()
            chain_evol = data["chain"]

            parameter_evol = 0
            prevolution = ""
            while parameter_evol == 0:
                pokemon_info = {}

                try:
                    print("pokmemon", chain_evol["species"]["name"])
                    pokemon_name = chain_evol["species"]["name"]
                    url_pokemon = "https://pokeapi.co/api/v2/pokemon/" + pokemon_name
                    response_pokemon = requests.get(url_pokemon)
                    if response_pokemon.status_code == 200:
                        pokemon_data = response_pokemon.json()
                        inner_evol = 0
                        evolutions = ""

                        try:
                            cahin_inner_evol = chain_evol["evolves_to"][0]
                            while inner_evol == 0:
                                try:
                                    evolutions = evolutions + \
                                        cahin_inner_evol["species"]["name"] + ","

                                    cahin_inner_evol = cahin_inner_evol["evolves_to"][0]
                                except:

                                    inner_evol = 1
                        except:
                            evolutions = ""
                        try:
                            Pokemons.objects.create(
                                pokemon_id=pokemon_data["id"],
                                pokemon_name=pokemon_name,
                                base_stats=pokemon_data["stats"],
                                height=pokemon_data["height"],
                                weight=pokemon_data["weight"],
                                evolutions=evolutions,
                                prevolution=prevolution
                            )
                            pokemon_info["pokemon_id"] = pokemon_data["id"]
                            pokemon_info["pokemon_name"] = pokemon_name
                            pokemon_info["base_stats"] = pokemon_data["stats"]
                            pokemon_info["weight"] = pokemon_data["weight"]
                            pokemon_info["height"] = pokemon_data["height"]
                            pokemon_info["evolutions"] = evolutions
                            prevolution = pokemon_name
                            content.append(pokemon_info)
                        except Exception as e:
                            print(e)

                            return Response("Esta cadena ya fue creada", status=status.HTTP_400_BAD_REQUEST)
                        chain_evol = chain_evol["evolves_to"][0]

                except Exception as e:
                    print(e)
                    parameter_evol = 1
                    print("se acabo")

                    return Response(content, status=status.HTTP_200_OK)


class Pokemoninfoview(APIView):
    def get(self, request, pokemon_name):
        content = {}
        try:
            pokemon = Pokemons.objects.get(pokemon_name=pokemon_name)
        except:
            return Response("Este pokemon no esta registrado en la base de datos", status=status.HTTP_400_BAD_REQUEST)

        content["id"] = pokemon.pokemon_id
        print(pokemon.pokemon_id)
        content["pokemon_name"] = pokemon.pokemon_name
        content["base_stats"] = pokemon.base_stats
        content["height"] = pokemon.height
        content["weight"] = pokemon.weight

        evolutions_info = []
        raw = {}
        try:
            arr = pokemon.evolutions.split(",")
            if len(arr) >= 1 and pokemon.prevolution == "":
                pokemon_prevolution = Pokemons.objects.get(pokemon_name=arr[0])
                raw["id"] = pokemon_prevolution.pokemon_id
                raw["pokemon_name"] = arr[0]
                raw["type"] = "prevolution"
                evolutions_info.append(raw)
            elif len(arr) >= 1 and pokemon.prevolution != "":
                pokemon_prevolution = Pokemons.objects.get(pokemon_name=arr[0])
                raw["id"] = pokemon_prevolution.pokemon_id
                raw["pokemon_name"] = arr[0]
                raw["type"] = "prevolution"
                evolutions_info.append(raw)

                raw = {}
                pokemon_evolution = Pokemons.objects.get(
                    pokemon_name=pokemon.prevolution)

                raw["id"] = pokemon_evolution.pokemon_id
                raw["pokemon_name"] = pokemon.prevolution
                raw["type"] = "evolution"
                evolutions_info.append(raw)
        except:

            if pokemon.evolutions == "" and pokemon.prevolution != "":

                pokemon_evolution = Pokemons.objects.get(
                    pokemon_name=pokemon.prevolution)

                raw["id"] = pokemon_evolution.pokemon_id
                raw["pokemon_name"] = pokemon.prevolution
                raw["type"] = "evolution"
                evolutions_info.append(raw)

        content["evolution_info"] = evolutions_info

        return Response(content, status=status.HTTP_200_OK)
