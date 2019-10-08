class Macros:
    PROTEIN_CALORIES_PER_GRAM = CARB_CALORIES_PER_GRAM = 4
    FAT_CALORIES_PER_GRAM = 9
    def __init__(self, serving_size=0, protein_grams=0, fat_grams=0, carb_grams=0):
        self.serving_size = serving_size
        self.protein_grams = protein_grams
        self.fat_grams = fat_grams
        self.carb_grams = carb_grams
        self.calories = self._get_total_calories()

    def _get_total_calories(self):
        return sum([
                self.protein_grams * self.PROTEIN_CALORIES_PER_GRAM,
                self.fat_grams * self.FAT_CALORIES_PER_GRAM,
                self.carb_grams * self.CARB_CALORIES_PER_GRAM
            ])

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
