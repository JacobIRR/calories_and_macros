from macros import Macros

class GainOrMaintainConfig:
    """ for gaining or maintaining target_weight """
    def __init__(self, target_weight, gain=True):
        self.epsilon = 5  # fudge factor for calculations
        self.target_weight = target_weight
        self.gain = gain
        self.fetch_config(target_weight)

    def fetch_config(self, target_weight):
        '''
        Calories per day to gain 3389
        Calories per day to maintain 2965
        '''
        # TODO: use target_weight arg to get these values from an API
        self.daily_calories_needed = 3389 if self.gain else 2965
        self.macros = self.get_plan_macros()

    def get_plan_macros(self):
        '''
        Gain:
        149g protein
        113g fats
        445g carbs
        total calories: 3,389

        Maintain:
        165g protein
        99g fat
        354g carbs
        total calories: 2,965
        '''
        if self.gain:
            return Macros(protein_grams=149, fat_grams=113, carb_grams=445)
        else:
            return Macros(protein_grams=165, fat_grams=99, carb_grams=354)

    def __str__(self):
        macros_sum = (self.macros.protein_grams * 4 +
                      self.macros.carb_grams * 4 +
                      self.macros.fat_grams * 9)
        assert macros_sum - self.epsilon <= self.daily_calories_needed <= macros_sum + self.epsilon
        return """MACROS: \n
Daily Calories Needed: {} \n
Grams of Protein: {} \n
Grams of Carbs: {} \n
Grams of Fat: {}""".format(self.daily_calories_needed,
                       self.macros.protein_grams,
                       self.macros.fat_grams,
                       self.macros.carb_grams)


# test:
gain_config = GainOrMaintainConfig(200)
print(gain_config)
