from pprint import pprint
from collections import defaultdict
from configs import GainOrMaintainConfig
from food_ids import FOOD_IDS
from food import Food
from random import choice

DUMP_PATH = './dump.json'

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

    def get_daily_food_options(self):
        target = self.config.daily_calories_needed
        food_combinations = []
        groceries = self.get_foods_from_id_bank()
        num_iterations = 100 # I have to manually change this to get more/less results
        for i in range(num_iterations):
            temp_combination = defaultdict(int)
            current_calories = 0
            while current_calories < target:
                food = choice(groceries) # random (not smart)
                key = "{} ({}g per serving)".format(food.name, food.macros.serving_size)
                temp_combination[key] += 1
                current_calories += food.macros.calories
            food_combinations.append(temp_combination)
        return food_combinations


    def get_combinations(self):
        """
        This method is from https://stackoverflow.com/a/57764143/4225229
        This needs to unpack the calories dynamically to build calorie_counts
        We have the total_calories as self.config.daily_calories_needed.
        """
        from itertools import product
        total_calories = self.config.daily_calories_needed
        groceries = self.get_foods_from_id_bank()  # list of Food objects
        output = set()
        calorie_counts = []
        safe_level = 6 # out of 11 or 13
        for i in range(safe_level):
            groceries.pop() # take off some groceries to help it finish

        n = len(groceries)
        for g in groceries:
            # we are just adding total calories per food here.
            # We could add a richer object here to unpack into a dict later
            print("calorie_count addition:", g.macros.calories)
            calorie_counts.append(g.macros.calories)


        # calorie_counts = [300, 150, 200] # OVERRIDE for small tests
        # n = len(calorie_counts)

        max_factors = [total_calories // int(calorie_counts[i]) for i in range(n)]
        print("max_factors is : ", max_factors) # why do I need this?

        print("about to loop over product...")
        product_list = product(*(range(factors + 1) for factors in max_factors))
        # product_list_list = list(product_list)
        # print("Length: product(*(range(factors + 1) for factors in max_factors)) is : ", len(product_list_list))

        for t in product_list:
            calorie_count = sum([t[i] * calorie_counts[i] for i in range(n)])
            # print("calorie_count calculated as : ", calorie_count)
            if calorie_count >= total_calories and \
               calorie_count < total_calories + self.config.epsilon:
                # print("found a match!")
                output.add(t)
        print("about to return output...")
        return output


    def combos(self):  # menu: list of values
        target = self.config.daily_calories_needed
        menu = {}
        for food in self.get_foods_from_id_bank():
            menu[food.name] = int(food.macros.calories)
        print("menu is : ")
        pprint(menu)
        # Put the biggest first for efficiency
        # and to avoid large shortfalls:
        ordered = sorted(enumerate(menu.values()),key=lambda e: -e[1])
        print("ordered: ", ordered)
        # Construct inverse permutation:
        inv=[None]*len(menu)
        for i,(j,_) in enumerate(ordered): inv[j]=i
        for c in self.combos_helper([v for _,v in ordered], target, []):
            yield [c[i] for i in inv]

    def combos_helper(self, menu, target, pfx):
        v = menu[len(pfx)]
        # Leave no budget unspent:
        if len(pfx) == len(menu)-1:
            n =-(-target // v)  # ceiling division
            if target + self.config.epsilon >= n * v:
                yield pfx + [n]
        else:
            for i in range((target + self.config.epsilon) // v + 1):
                for c in self.combos_helper(menu, target - i * v, pfx + [i]):
                    yield c

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
    day = DailyConsumption(GainOrMaintainConfig(200))

    # option 3
    combs = day.combos()
    for c in combs:
        if len(c) - c.count(0) == 1:
            print(c)

    # option 2
    # combinations = day.get_combinations()
    # print(combinations)

    # option 1
    # food_options = day.get_daily_food_options()
    # for ix, opt in enumerate(food_options):
    #     print("=================================")
    #     print(" COMBINATION NUMBER {}".format(ix))
    #     print("=================================")
    #     for k, v in opt.items():
    #         print("{} : {} servings".format(k, v))
