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

    def __str__(self):
        return self.name

    def _fetch_food_info(self):
        resp = requests.get(URL.format(self.id, API_KEY))
        json_dict = resp.json()
        print("============BEGIN RESPONSE:===============")
        pprint(json_dict)
        print("============END RESPONSE:===============")
        food_obj = json_dict['foods'][0]['food']
        self.name = food_obj['desc']['name']
        nutrients = food_obj['nutrients']
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
foods = []
foods.append(Food(FOOD_IDS["Boiled Egg"]))
foods.append(Food(FOOD_IDS["Brown Rice"]))
foods.append(Food(FOOD_IDS["Chicken Breast"]))

print([f.macros.__dict__ for f in foods])
[{'protein_grams': 6.0, 'fat_grams': 4.5, 'carb_grams': 1.0, 'calories': 68.5}, {'protein_grams': 4.0, 'fat_grams': 1.5, 'carb_grams': 35.0, 'calories': 169.5}, {'protein_grams': 23.0, 'fat_grams': 2.5, 'carb_grams': 0.0, 'calories': 114.5}]

For simplicity, you could assume that
egg = 68.5
rice = 169.5
chicken = 114.5

# egg = Food(FOOD_IDS["Boiled Egg"])
# print(egg.macros.__dict__)
# {'protein_grams': 6.0, 'fat_grams': 4.5, 'carb_grams': 1.0, 'calories': 68.5}

