from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch
from foodItem import FoodItem

class CalorieDetector:
    def __init__(self):
        self.api_key = "USEAPIKEYHERE"  # Replace with your actual API key
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
        self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    def processImage(self, image):
        print("[PROCESS] Running DETR model for object detection...")
        img = Image.open(image.filePath).convert("RGB")

        inputs = self.processor(images=img, return_tensors="pt")
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([img.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        labels = []
        for score, label_id in zip(results["scores"], results["labels"]):
            label = self.model.config.id2label[label_id.item()]
            print(f"Detected: {label} ({score:.2f})")
            labels.append(label.lower())

        return labels

    def fetchCalories(self, foodItem: FoodItem) -> float:
        import requests
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={foodItem.itemName}&api_key={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "foods" in data and data["foods"]:
                    nutrients = data["foods"][0].get("foodNutrients", [])
                    for nutrient in nutrients:
                        if nutrient.get("nutrientName") == "Energy" and nutrient.get("unitName") == "KCAL":
                            return float(nutrient.get("value", 0))
            return 0
        except Exception as e:
            print("[API ERROR]", str(e))
            return 0

    def matchFoodItemInDatabase(self, foodName: str) -> dict:
        item = FoodItem("001", foodName, 1.0)
        calories = self.fetchCalories(item)
        return {"name": foodName, "calories": calories}
