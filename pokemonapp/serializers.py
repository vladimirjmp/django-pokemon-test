from rest_framework import serializers
from .models import Pokemon, Evolution, Stat

class PokemonPrevolutionSerializer(serializers.Serializer):
  pokemon_id = serializers.IntegerField()
  name = serializers.CharField(max_length=20)
  evolution_type = serializers.CharField(max_length=20, default="prevolution")

class PokemonEvolutionSerializer(serializers.Serializer):
  pokemon_id = serializers.IntegerField()
  name = serializers.CharField(max_length=20)
  evolution_type = serializers.CharField(max_length=20, default="evolution")

class StatSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=20)
  base_stat = serializers.IntegerField()

class PokemonSerializer(serializers.Serializer):
  pokemon_id = serializers.IntegerField()
  name = serializers.CharField(max_length=20)
  height = serializers.IntegerField()
  weight = serializers.IntegerField()
  stats = StatSerializer(many=True, read_only=True)