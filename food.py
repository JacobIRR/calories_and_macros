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
    def __init__(self, name="", update_dict=None, debug=False):
        if update_dict:
            self.__dict__.update(update_dict)
            m = update_dict['macros']
            self.macros = Macros(m['serving_size'],
                                 m['protein_grams'],
                                 m['fat_grams'],
                                 m['carb_grams'])
        else:
            self.name = name
            self.id = FOOD_IDS[name]  # ndbno
            self.debug = debug
            self.macros = self._fetch_food_info()

    def __str__(self):
        return self.name

    def _fetch_food_info(self):
        resp = requests.get(URL.format(self.id, API_KEY))
        json_dict = resp.json()
        if self.debug:
            print("============BEGIN RESPONSE:===============")
            pprint(json_dict)
            print("============END RESPONSE:===============")
        food_obj = json_dict['foods'][0]['food']
        nutrients = food_obj['nutrients']
        try:
            serving_grams = nutrients[0]['measures'][0]['eqv']
            assert nutrients[0]['measures'][0]['eunit'] == 'g'
        except (KeyError, AssertionError):
            # Not all foods have a "measures" key
            if self.debug:
                print("We cannot find the `measures` key, continuing...")
            if self.name == "Avocado":
                serving_grams = 136
            elif self.name == "Whole Milk":
                serving_grams = 240  # mililiters not grams
            else:
                raise

        # now build the macros
        protein = fat = carbs = 0
        for d in nutrients:
            if d['nutrient_id'] == NUTRIENT_IDS['protein']:
                protein = self._calc_calorie_for_macro(serving_grams, float(d['value']))
            elif d['nutrient_id'] == NUTRIENT_IDS['fat']:
                fat = self._calc_calorie_for_macro(serving_grams, float(d['value']))
            elif d['nutrient_id'] == NUTRIENT_IDS['carbs']:
                carbs = self._calc_calorie_for_macro(serving_grams, float(d['value']))
        return Macros(serving_grams, protein, fat, carbs)

    def _calc_calorie_for_macro(self, serving_size, value):
        return round(serving_size / DEFAULT_SERVING * value, 1)



# Tests:
if __name__ == '__main__':
    out = []
    for k in FOOD_IDS:
        try:
            print("k is : ", k)
            out.append(Food(k))
        except Exception as e:
            print("cannot make this food: ", k)
            print("... because: ", e)
            raise
    print([f.__dict__ for f in out])
