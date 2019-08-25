import json
import requests
from pprint import pprint
from macros import Macros
from food_ids import FOOD_IDS, NUTRIENT_IDS, API_KEY

# NOTE: type b is basic, type f is full, s is stats
URL = 'https://api.nal.usda.gov/ndb/V2/reports?ndbno={}&type=s&format=json&api_key={}'


class Food(object):
    """a food object from an ndbno ID """
    def __init__(self, ndbno):
        self.id = ndbno
        self.macros = self.fetch_food_info()

    def fetch_food_info(self):
        resp = requests.get(URL.format(self.id, API_KEY))
        json_dict = resp.json()
        pprint(json_dict)
        # TODO: deal with serving size, qty also from this response
        nutrients = json_dict['foods'][0]['food']['nutrients']
        # now build the macros
        protein = fat = carbs = 0
        for d in nutrients:
            if d['nutrient_id'] == NUTRIENT_IDS['protein']:
                protein = float(d['value'])
            elif d['nutrient_id'] == NUTRIENT_IDS['fat']:
                fat = float(d['value'])
            elif d['nutrient_id'] == NUTRIENT_IDS['carbs']:
                carbs = float(d['value'])
        return Macros(protein, fat, carbs)



# Tests:
egg = Food(FOOD_IDS["Boiled Egg"])
print(egg.macros.__dict__)
print(egg.macros._get_total_calories()) # TODO: this is all based on 100 grams!! ahh!!
