# Pokemon Evolution Chain

This is a Django App that fetches pokemons evolution chains from the [PokeApi](https://pokeapi.co/) and stores the collected data in a local database to then use it to expose an api to fetch that pokemons data collected.

### Dependencies
- Django==3.1.5
- djangorestframework==3.12.2
- requests==2.25.1

### Installation

Install the dependencies and start the server.

```sh
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

### Fetching and Storing Pokemon Chains Data
To fetch and store the pokemons data you can use the `pokemonevolution` custom Django command passing de `id` of the evolution chain

```sh
$ python manage.py pokemonevolution <EVOLUTION_CHAIN_ID>
```

### API
The API has only one endpoint that receves a unique parameter pokemon `name`and returns the pokemon data stored in the local database
```sh
http://localhost:8000/api/pokemon/<POKEMON_NAME>
```
### Response
The pokemons data is returned in JSON format as follows
````
{
    "pokemon_id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 4,
    "stats": [
        {
            "name": "hp",
            "base_stat": 35
        },
        {
            "name": "attack",
            "base_stat": 55
        },
        {
            "name": "defense",
            "base_stat": 40
        },
        {
            "name": "special-attack",
            "base_stat": 50
        },
        {
            "name": "special-defense",
            "base_stat": 50
        },
        {
            "name": "speed",
            "base_stat": 90
        }
    ],
    "evolutions": [
        {
            "pokemon_id": 172,
            "name": "pichu",
            "evolution_type": "prevolution"
        },
        {
            "pokemon_id": 26,
            "name": "raichu",
            "evolution_type": "evolution"
        }
    ]
}
````