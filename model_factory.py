from calorie_detector import CalorieDetector
from foodItem import FoodItem
import random

class BaseDetector:
    def analyze(self, image):
        raise NotImplementedError

class CorporateCalorieDetector(BaseDetector):
    def __init__(self):
        self.detector = CalorieDetector()

    def analyze(self, image):
        print("[Corporate] Using DETR + USDA API...")
        labels = self.detector.processImage(image)
        results = []
        for label in labels:
            food = FoodItem("f001", label, 1.0)
            calories = self.detector.fetchCalories(food)
            results.append({
                "name": label,
                "calories": calories
            })
        return results

class PersonalCalorieDetector(BaseDetector):
    def __init__(self):
        self.detector = CalorieDetector()
        self.allowed_items = ["apple", "banana", "bread", "rice", "pasta", "egg", 
                            "chicken", "fish", "potato", "tomato"]  # Basic food items

    def analyze(self, image):
        print("[Personal] Using lightweight detection...")
        labels = self.detector.processImage(image)
        
        results = []
        for label in labels:
            lower_label = label.lower()
            
            if lower_label not in self.allowed_items:
                print(f"[WARNING] '{label}' requires corporate tier for full analysis")
                results.append({
                    "name": label,
                    "calories": "Corporate tier required",
                    "message": "This item requires corporate subscription for full analysis"
                })
                continue
                
            food = FoodItem("f001", label, 1.0)
            calories = self.detector.fetchCalories(food)
            results.append({
                "name": label,
                "calories": calories
            })
        
        return results

class ModelFactory:
    @staticmethod
    def get_model(tier: str) -> BaseDetector:
        if tier == "corporate":
            return CorporateCalorieDetector()
        else:
            return PersonalCalorieDetector()