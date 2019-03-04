#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 11:10:55 2019

@author: dejanmaric
"""

import pandas as pd
import requests
import time

### Get pokemon stats from Kanto pokedex => to_csv

url = "https://pokeapi.co/api/v2/pokedex/2/"
get_pokemons = requests.get(url)
get_pokemons_json = get_pokemons.json()
elements = get_pokemons_json['pokemon_entries']
all_data=[]

start = time.time()

for x in elements:
    url = "https://pokeapi.co/api/v2/pokemon/" + str(x["entry_number"]) + "/"
    get_pokemon = requests.get(url)
    get_pokemon_json = get_pokemon.json()
    d = {'id': x["entry_number"], 
         'name': x["pokemon_species"]["name"],
         'order': get_pokemon_json["order"],
         'weight': get_pokemon_json["weight"],
         'height': get_pokemon_json["height"],
         'speed': get_pokemon_json["stats"][0]["base_stat"],
         'special_defense': get_pokemon_json["stats"][1]["base_stat"],
         'special_attack': get_pokemon_json["stats"][2]["base_stat"],
         'defense': get_pokemon_json["stats"][3]["base_stat"],
         'attack': get_pokemon_json["stats"][4]["base_stat"],
         'hp': get_pokemon_json["stats"][5]["base_stat"]}
all_data.append(d)

elapsed = (time.time() - start)
print("Time elapsed: ", elapsed)

df = pd.DataFrame(all_data)
df.sort_values(by=['id'])
df.to_csv('pokemon-stats.csv')


### Get more pokemon stats (Move and Type)

url = "https://pokeapi.co/api/v2/pokedex/2/"
get_pokemons = requests.get(url)
get_pokemons_json = get_pokemons.json()
elements = get_pokemons_json['pokemon_entries']

all_data=[]

start1 = time.time()
for x in elements:
    url = "https://pokeapi.co/api/v2/pokemon/" + str(x["entry_number"]) + "/"
    get_pokemon = requests.get(url)
    get_pokemon_json = get_pokemon.json()
    e = {'id': x["entry_number"], 
         'name': x["pokemon_species"]["name"],
         'speed' : get_pokemon_json["stats"][0]["base_stat"],
         'special_defense': get_pokemon_json["stats"][1]["base_stat"],
         'special_attack': get_pokemon_json["stats"][2]["base_stat"],
         'defense': get_pokemon_json["stats"][3]["base_stat"],
         'attack': get_pokemon_json["stats"][4]["base_stat"],
         'hp': get_pokemon_json["stats"][5]["base_stat"],
         'move': set(y['move']['name'] for y in get_pokemon_json["moves"]),
         'type': set(z['type']['name'] for z in get_pokemon_json['types'])
        }  
    all_data.append(e)
    
elapsed1 = (time.time() - start1)
print("Time elapsed: ", elapsed1)
df1 = pd.DataFrame(all_data)

# inverting data set (to make attributes pointing to id)
move_to_id = {}
for id, conds in df1["move"].items():
    for c in conds:
        move_to_id.setdefault(c, set()).add(id)

type_to_id = {}
for id, conds in df1["type"].items():
    for c in conds:
        type_to_id.setdefault(c, set()).add(id)


# random checks
[key for key, value in df1["type"].items() if 'ice' in value] ##id=86,90,123,130,143
[key for key, value in df1["move"].items() if 'laser-focus' in value] ##id=149

# define function (finding pokemon's id with the max stat id and match found id to the name id)
def getBest(move, tip, stat):
    argsAllowed = ['hp','attack','speed','special_attack','special_defense','defense']
    if stat not in argsAllowed: print("Not a valid stat"); return
    if move == 'all' and tip == 'all':
        print(df1['name'].values[df1[stat] == df1[stat].max()])    
    elif move == 'all':
        matches=type_to_id[tip]
        max_stat = max(df1[stat][id] for id in matches)
        return [df1["name"][id] for id in matches if df1[stat][id] == max_stat]
    elif tip == 'all':
        matches=move_to_id[move]
        max_stat = max(df1[stat][id] for id in matches)
        return [df1["name"][id] for id in matches if df1[stat][id] == max_stat]
    else:
        matches = move_to_id[move] & type_to_id[tip]
        max_stat = max(df1[stat][id] for id in matches)
        return [df1["name"][id] for id in matches if df1[stat][id] == max_stat]
        
    
## some testings to find best pokemon based on some criteria        
getBest('all', 'all', 'hp')
getBest('cut', 'rock', 'attack')
getBest('all', 'ice', 'speed')
getBest('laser-focus', 'all', 'hp')
getBest('mega-kick', 'water', 'special_defense')
getBest('light-screen', 'rock', 'special_attack')  #return "not found"

## Check random stat column
getBest('mega-kick', 'water', 'water')
getBest('mega-kick', 'water', 'bezveze')









