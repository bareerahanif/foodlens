class Image:
    def __init__(self, imageID: str, filePath: str, format: str, size: float, resolution: str):
        self.imageID = imageID
        self.filePath = filePath
        self.format = format
        self.size = size
        self.resolution = resolution

    def uploadImage(self) -> bool:
        print(f"[UPLOAD] Image {self.imageID} uploaded.")
        return True

    def validateImageFormat(self) -> bool:
        return self.format.lower() in ["jpg", "jpeg", "png"]

    def validateImageSize(self) -> bool:
        return self.size <= 5.0
