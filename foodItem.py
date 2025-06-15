from image import Image

class FoodItem:
    def __init__(self, itemID: str, itemName: str, quantity: float):
        self.itemID = itemID
        self.itemName = itemName
        self.quantity = quantity

    def detectFoodItem(self, image: Image) -> list[str]:
        print(f"[DETECT] Detecting items from image {image.imageID}")
        return ["apple", "banana"]

    def displayItemName(self) -> str:
        return self.itemName
