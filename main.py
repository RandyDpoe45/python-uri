import urllib3
import json
import re

def count_pokemons():
    pokemon_counter = 0
    http = urllib3.PoolManager()
    r = http.request('GET',"https://pokeapi.co/api/v2/pokemon?limit=1120")
    pokemon_data = json.loads(r.data)
    for obj in pokemon_data["results"]:
        if "at" in obj["name"] and obj["name"].count("a") == 2:
            pokemon_counter += 1

    print(f'Numero total de pokemones con at y dos a: {pokemon_counter}')
    return pokemon_counter

def count_possible_breeding_partners(pokemon_name = "raichu"):
    possible_partners = set()
    http = urllib3.PoolManager()
    r = http.request('GET', f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    pokemon_data = json.loads(r.data)
    s = http.request('GET', pokemon_data["species"]["url"])
    species_data =  json.loads(s.data)
    for egg_group in species_data["egg_groups"] :
        e = http.request('GET', egg_group["url"])
        egg_data = json.loads(e.data)
        for species in egg_data["pokemon_species"]:
            possible_partners.add(species["name"])
    print(f'Numero de pokemones que pueden procrear con {pokemon_name} {len(possible_partners)}')
    return len(possible_partners)

def min_max_weight(generation_id = 1, id_limit = 151):
    weight_set = set()
    http = urllib3.PoolManager()
    g = http.request('GET', f"https://pokeapi.co/api/v2/generation/{generation_id}")
    generation_data = json.loads(g.data)
    for species in generation_data["pokemon_species"]:
        try :
            s = http.request('GET', f'https://pokeapi.co/api/v2/pokemon/{species["name"]}')
            pokemon_data = json.loads(s.data)
            if is_fighting_type(pokemon_data) and int(pokemon_data["id"]) <= id_limit:
                weight_set.add(int(pokemon_data["weight"]))
        except :
            print(s.data)
            print(f'https://pokeapi.co/api/v2/pokemon/{species["name"]}')
    result = [max(weight_set),min(weight_set)]
    print(f'Peso maximo {result[0]} Peso minimo {result[1]}')
    return result

def is_fighting_type(pokemon):
    types = filter(lambda x: x["type"]["name"] == "fighting", pokemon["types"])
    return len(list(types)) > 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count_pokemons()
    count_possible_breeding_partners()
    min_max_weight()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
