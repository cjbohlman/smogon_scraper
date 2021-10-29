# py -m pip install requests
import requests
# py -m pip install bs4
from bs4 import BeautifulSoup

import json
from string import Template

banned_formats = ["1v1", "Doubles", 'CAP', 'LGPE OU', "Battle Spot Singles", "Monotype", 'National Dex', "Almost Any Ability", 'STABmons', 'Camomons']
generations = ['rb', 'gs', 'rs', 'dp', 'bw', 'xy', 'sm', 'ss']

class SMOGON_RETRIEVER():

    def get_move(self, moveslist):
        moves = ''
        for s in moveslist:
            moves = moves + s['move'] + '/'
        return moves[0:-1]

    def get_data(self, str_pokemon, str_generation):
        if str_generation not in generations:
            return None

        url_template = Template('https://www.smogon.com/dex/$generation/pokemon/$pokemon')
        url = url_template.substitute(generation=str_generation.lower(), pokemon=str_pokemon.lower())

        res = requests.get(url)
        if res.status_code != 200:
            return None
        
        soup = BeautifulSoup(res.content, 'html.parser')

        # This script contains the HTML data we will extract from
        movesets = soup.select('script')[1].string

        # Beginning of JSON obj in script
        poke_dict = json.loads(movesets[movesets.find("{\"injectRpcs\""):])
        strats = poke_dict["injectRpcs"][2][1]["strategies"]

        # strats are on a per-format basis
        # Each format has a moveset kv pair with all of the different movesets
        valid_strats = [s for s in strats if s["format"] not in banned_formats]

        pokemon_dict = {}
        pokemon_dict['pokemon'] = str_pokemon
        pokemon_dict['generation'] = str_generation

        strategy_list = []
        for s in valid_strats:
            strategy_dict = {}
            strategy_dict['name'] = s['movesets'][0]['name']
            strategy_dict['format'] = s['format']
            strategy_dict['abilities'] = s['movesets'][0]['abilities']
            strategy_dict['items'] = s['movesets'][0]['items']
            strategy_dict['move1'] = self.get_move(s['movesets'][0]['moveslots'][0])
            strategy_dict['move2'] = self.get_move(s['movesets'][0]['moveslots'][1])
            strategy_dict['move3'] = self.get_move(s['movesets'][0]['moveslots'][2])
            strategy_dict['move4'] = self.get_move(s['movesets'][0]['moveslots'][3])
            strategy_dict['natures'] = s['movesets'][0]['natures']
            strategy_dict['evs'] = s['movesets'][0]['evconfigs']
            strategy_dict['ivs'] = s['movesets'][0]['ivconfigs']

            strategy_list.append(strategy_dict)
        
        pokemon_dict['strategies'] = strategy_list

        return pokemon_dict