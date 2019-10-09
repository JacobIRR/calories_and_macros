from datetime import datetime
from functools import lru_cache
from pprint import pprint
from collections import defaultdict
from configs import GainOrMaintainConfig
from food_ids import FOOD_IDS
from food import Food
from random import choice

DUMP_PATH = './dump.json'
SKIP_LOG = './skip_log.txt'
RESULT_LOG = './result_log.txt'

FOOD_NAMES_ORDERED_BY_CALORIE = [
    'Avocado',
    'Sweet Potato',
    'Mixed Nuts',
    'Brown Rice',
    'Chicken Breast',
    'Salmon',
    'Bacon',
    'Boiled Egg',
    'Good Seed bread',
    'Green Peas',
    'Pineapple',
    'Spinach',
    'Whole Milk',
     ]

class ConsumableFood:
    def __init__(self, name, num_servings):
        self.name = name
        self.num_servings = num_servings

class FoodOptions:
    """
    little struct to represent and print:
    comsumable_foods :
        food : num_servings
        ...
    macros : Macros object
    """
    def __init__(self, comsumable_foods, macros):
        self.comsumable_foods = comsumable_foods
        self.macros = macros

    def __str__(self):
        output = "Foods: \n"
        for f in self.comsumable_foods:
            output += "\t {} : {} \n".format(f.name, f.num_servings)
        output += "Macros: \n"
        output += "\t Calories: \n".format(self.macros.calories)
        output += "\t Protein: \n".format(self.macros.protein)
        output += "\t Carbs: \n".format(self.macros.carbs)
        output += "\t Fat: \n".format(self.macros.fat)
        return output


class DailyConsumption:
    """
    The task here is to:
    1. Obtain a config object based on gain or maintain
    2. Fetch and cache all food macros in JSON (to limit API calls)
    3. Generate combinations of foods to match config,
        using `calories` as a limit in a while loop
    4. Loop over all these combinations and select/save the ones
        that match the target macro ratios within a certain margin
        of error/epsilon.
    * We are creating a DAILY collection of foods since I may not
      eat the same number of meals each day, and since many smaller meals
      allow for higher calorie consumption.
    """

    def __init__(self, config):
        self.config = config

    def combos(self):  # menu: list of values
        # TODO / BUG : this sometimes outputs negative numbers!:
        # e.g. [9, 9, 9, 7, 0, 0, -1, 0, 0, 4, 0, 8, 0]

        # make a menu dict to show which foods have which calories
        menu = {}
        for food in self.get_foods_from_id_bank():
            menu[food.name] = int(food.macros.calories)
        print("menu is : ")
        pprint(menu)

        # Put the biggest first for efficiency and to avoid large shortfalls
        # We enumerate these with indexes and use the second value for sorting
        sort_desc_tuple_func = lambda e: -e[1]
        ordered = sorted(enumerate(menu.values()), key=sort_desc_tuple_func)

        # We need to construct an inverse permutation
        # Make a list full of None entries...
        inverse = [None] * len(menu)
        # loop over the ordered list of tuples and put the index of each
        #  as the value in the list at the index of the value
        for i, (j, _) in enumerate(ordered):
            inverse[j] = i
        # result is something like:
        # [9, 7, 8, 11, 0, 5, 12, 2, 1, 6, 3, 10, 4]

        # Now we call our helper method
        sorted_calories = [v for _,v in ordered]
        # ^ [247, 204, 184, 169, 157, 114, 105, 91, 82, 68, 68, 40, 20] ^

        for c in self.combos_helper(tuple(sorted_calories),
                                    self.config.daily_calories_needed,
                                    ()):
            # c comes back out of order, so this next line let's us
            # yield the servings back in the original order:
            yield [c[i] for i in inverse]

    @lru_cache(maxsize=1024)
    def combos_helper(self, sorted_calories, target, prefix):
        """
        In order to use this method with the lru_cache,
        all args must be immutable, meaning lists must be tuples
        """
        target_with_epsilon = target + self.config.epsilon
        # get a single value from the sorted_calories based on
        # the length of the prefix list
        # note that the length of prefix is never as long as sorted_calories
        calories_per_food = sorted_calories[len(prefix)]
        # "Leave no budget unspent":
        # Here we have two cases:
        # 1) BASE CASE: The prefix has reached its max length:
        if len(prefix) == len(sorted_calories) - 1:
            num_servings = -(-target // calories_per_food) # TODO: why?
            try:
                assert num_servings >= 0
            except AssertionError:
                 # no negative numbers allowed! bail out
                 return
            # Here we check that our servings equal the calories we want
            # TODO: add another macro check here
            calories_per_n_servings = num_servings * calories_per_food
            if target_with_epsilon >= calories_per_n_servings:
                yield list(prefix) + [num_servings]
        # 2) RECURSIVE CASE: The prefix is smaller than its max length
        else:
            # find out how many servings we need by dividing target by calories
            servings_needed = target_with_epsilon // calories_per_food + 1
            # Loop over this range of servings
            for serving in range(servings_needed):
                # Calculate a new target for the remainder of calories needed
                new_target = target - (serving * calories_per_food)
                # Rescurse using the current prefix plus this serving
                recursive_combos = self.combos_helper(sorted_calories,
                                                      new_target,
                                                      tuple(list(prefix) + [serving]))
                for combo in recursive_combos:
                    yield combo

    def get_foods_from_id_bank(self, use_json=True, store=0):
        out = []
        if use_json:
            import json

            with open(DUMP_PATH) as fp:
                json_content = json.load(fp)
                # Create objects from dict
                for d in json_content:
                    out.append(Food(update_dict=d))
        else:
            for k in FOOD_IDS:
                try:
                    out.append(Food(k))
                except:
                    print("cannot make this food: ", k)
            if store:
                print("saving to file....")
                res = json.dumps(out)
                print("res:")
                print(res)
        return out
        # return [Food(k) for k in FOOD_IDS] - this blows up sometimes


# Test:
if __name__ == '__main__':
    goal_pounds = 200
    day = DailyConsumption(GainOrMaintainConfig(goal_pounds))
    counter = 0
    start_time = datetime.now()
    # option 3
    combos = day.combos()
    for combo in combos:
        # we can make sure that we don't have too many servings of a single food
        # (no more than 5 servings) and we don't want to exclude more than 5 foods
        if max(combo) < 5 and combo.count(0) < 5:
            # Here we have lists of serving counts like this:
            # [0, 0, 0, 0, 0, 0, 170, 0, 0, 0, 0, 0, 0]
            # We need to reverse map the position of the serving
            # to know which food the count is referencing
            with open(RESULT_LOG, 'a') as f:
                for food_name, servings in zip(FOOD_NAMES_ORDERED_BY_CALORIE, combo):
                    f.write("{} servings of {} \n".format(str(servings), food_name))
                f.write("==================================================\n\n")
        else:
            # Only log millions of rows. Otherwise the file blows up the disk space
            counter += 1
            if counter % 1000000 == 0:
                millions_rows = counter // 1000000 # TODO: format with commas
                delta = datetime.now() - start_time
                minutes = delta.seconds // 60  # TODO: format with commas or hours, etc.
                log_str = "Skipped {} million rows after {} minutes \n"
                with open(SKIP_LOG, 'w') as fp:
                    fp.write(log_str.format(millions_rows, minutes))
