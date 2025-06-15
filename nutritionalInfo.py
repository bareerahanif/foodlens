class NutritionalInfo:
    def __init__(self, calories, carbohydrates, proteins, fats, vitamins: dict):
        self.calories = calories
        self.carbohydrates = carbohydrates
        self.proteins = proteins
        self.fats = fats
        self.vitamins = vitamins

    def calculateTotalCalories(self) -> float:
        return self.calories

    def getNutritionalBreakdown(self) -> dict:
        return {
            "calories": self.calories,
            "carbohydrates": self.carbohydrates,
            "proteins": self.proteins,
            "fats": self.fats,
            "vitamins": self.vitamins
        }

    def displayNutritionalInfo(self) -> str:
        return str(self.getNutritionalBreakdown())
