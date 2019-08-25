import json
import requests
from pprint import pprint
from macros import Macros
from food_ids import FOOD_IDS, NUTRIENT_IDS, API_KEY

# NOTE: type b is basic, type f is full, s is stats
URL = 'https://api.nal.usda.gov/ndb/V2/reports?ndbno={}&type=s&format=json&api_key={}'
DEFAULT_SERVING = 100  # grams

class Food(object):
    """a food object from an ndbno ID """
    def __init__(self, ndbno):
        self.id = ndbno
        self.macros = self._fetch_food_info()

    def _fetch_food_info(self):
        resp = requests.get(URL.format(self.id, API_KEY))
        json_dict = resp.json()
        print("============BEGIN RESPONSE:===============")
        pprint(json_dict)
        print("============END RESPONSE:===============")
        nutrients = json_dict['foods'][0]['food']['nutrients']
        serving_grams = nutrients[0]['measures'][0]['eqv']
        assert nutrients[0]['measures'][0]['eunit'] == 'g'
        # now build the macros
        protein = fat = carbs = 0
        for d in nutrients:
            if d['nutrient_id'] == NUTRIENT_IDS['protein']:
                protein = self._calc_calorie_for_macro(serving_grams, float(d['value']))
            elif d['nutrient_id'] == NUTRIENT_IDS['fat']:
                fat = self._calc_calorie_for_macro(serving_grams, float(d['value']))
            elif d['nutrient_id'] == NUTRIENT_IDS['carbs']:
                carbs = self._calc_calorie_for_macro(serving_grams, float(d['value']))
        return Macros(protein, fat, carbs)

    def _calc_calorie_for_macro(self, serving_size, value):
        return round(serving_size / DEFAULT_SERVING * value, 1)



# Tests:
egg = Food(FOOD_IDS["Boiled Egg"])
print(egg.macros.__dict__)
print(egg.macros._get_total_calories())
