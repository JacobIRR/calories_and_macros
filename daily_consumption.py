from configs import GainOrMaintainConfig
from food_ids import FOOD_IDS
from food import Food
from random import choice

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
        groceries = []
        groceries.append(Food(FOOD_IDS["Boiled Egg"]))
        groceries.append(Food(FOOD_IDS["Brown Rice"]))
        groceries.append(Food(FOOD_IDS["Chicken Breast"]))
        num_iterations = 100 # I have to manually change this to get more/less results
        for i in range(num_iterations):
            temp_combination = []
            current_calories = 0
            while current_calories < target:
                food = choice(groceries) # random (not smart)
                temp_combination.append(food)
                current_calories += sum([f.macros.calories for f in temp_combination])
            food_combinations.append(temp_combination)
        return food_combinations


# Test:
goal_pounds = 200
day = DailyConsumption(GainOrMaintainConfig(200))
food_options = day.get_daily_food_options()
for ix, opt in enumerate(food_options):
    print("=================================")
    print(" COMBINATION NUMBER {}".format(ix))
    print("=================================")
    for f in opt:
        print(f)
