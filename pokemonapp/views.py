from django.shortcuts import render
from .models import Pokemon, Evolution
from .serializers import PokemonSerializer, PokemonPrevolutionSerializer, PokemonEvolutionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

class PokemonApiView(APIView):

  def get(self, request, name):
    try:
      pokemon = Pokemon.objects.get(name=name)
      if pokemon:
        response = PokemonSerializer(pokemon).data
        response["evolutions"] = []

        try:
          prevolution = Evolution.objects.get(evolves_to__name=name)
          prevolution_serializer = PokemonPrevolutionSerializer(prevolution.pokemon)
          response["evolutions"].append(prevolution_serializer.data)

        except Exception as e:
          pass

        try:
          evolution = Evolution.objects.get(pokemon__name=name)
          evolution_serializer = PokemonEvolutionSerializer(evolution.evolves_to)
          response["evolutions"].append(evolution_serializer.data)

        except Exception as e:
          pass
        
    except Exception as e:
      response = {
        "error": "pokemon not found"
      }

    return Response(response)
