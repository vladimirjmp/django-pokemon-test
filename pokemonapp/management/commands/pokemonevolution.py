from django.core.management.base import BaseCommand
from pokemonapp.models import Pokemon, Evolution, Stat
import requests
import json

class Command(BaseCommand):
  help = "Fetch and Store Pokemon Chain Info"

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # Pokemon API Endpoint
    self.POKE_API_URL = "https://pokeapi.co/api/v2/"
    self.POKE_EVOLUTION_CHAIN_URL = self.POKE_API_URL + "evolution-chain/"
    self.POKE_DATA_URL = self.POKE_API_URL + "pokemon/"

  def add_arguments(self, parser):
    parser.add_argument("id", type=int, help="ID of the Evolution Chain")


  def handle(self, *args, **options):
    self.stdout.write(self.style.NOTICE("## Fetching Evolution Chain! ##"))

    request = requests.get(self.POKE_EVOLUTION_CHAIN_URL + str(options["id"]))
      
    try:
      response = json.loads(request.content)
      name = response["chain"]["species"]["name"]
      evolves_to = self.fetch_evolutions(response["chain"])
      evolution_chain = [name] + evolves_to.split(',')[:-1]

      self.stdout.write(self.style.SUCCESS(f"Evolution chain found: {' -> '.join(evolution_chain)}"))
      self.stdout.write("\n## Fetching and Storing Pokemons Data ##")

      pokemons = []
      for index, pokemon in enumerate(evolution_chain):
        data = self.fetch_pokemon_data(pokemon)
        pokemons.append(self.store_pokemon_data(data))

        if (index > 0):
          self.store_evolution(pokemons[index - 1], pokemons[index])
        
        self.stdout.write(f"{index+1}.- {data['name']} = {data}\n\n")
        
    except Exception as e:
      self.stdout.write(self.style.ERROR("Error fetching evolution chain, please try again later!"))

  def fetch_evolutions(self, chain):
    if len(chain["evolves_to"]) > 0:
      return chain["evolves_to"][0]["species"]["name"] + "," + self.fetch_evolutions(chain["evolves_to"][0])
    else:
      return ""
  
  def fetch_pokemon_data(self, name):
    request = requests.get(self.POKE_DATA_URL + name)
      
    try:
      response = json.loads(request.content)

      stats = []
      for stat in response["stats"]:
        stats.append({
          "stat": stat["stat"]["name"],
          "base_stat": stat["base_stat"]
        })

      return {
        "id": response["id"],
        "name": response["name"],
        "height": response["height"],
        "weight": response["height"],
        "stats": stats
      }

    except Exception as e:
      self.stdout.write(self.style.ERROR("Error fetching pokemon data, please try again later!"))
      return False

  def store_pokemon_data(self, data):
    pokemon = Pokemon.objects.filter(pokemon_id = data["id"])

    if not pokemon:
      pokemon = Pokemon(
        pokemon_id = data["id"],
        name = data["name"],
        height = data["height"],
        weight = data["weight"],
      )
      pokemon.save()

      for stat in data["stats"]:
        pokemon_stat = Stat(
          pokemon = pokemon,
          name = stat["stat"],
          base_stat = stat["base_stat"]
        )
        pokemon_stat.save()
      return pokemon

    return pokemon[0]

  def store_evolution(self, pokemon, evolves_to):
    evolution = Evolution.objects.filter(pokemon__pokemon_id=pokemon.pokemon_id)

    if not evolution:
      pokemon_evloution = Evolution(
        pokemon = pokemon,
        evolves_to = evolves_to
      )
      pokemon_evloution.save()