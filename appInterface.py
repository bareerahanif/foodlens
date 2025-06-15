class AppInterface:
    def __init__(self, guiTheme: str, language: str, platform: str):
        self.guiTheme = guiTheme
        self.language = language
        self.platform = platform

    def renderUI(self) -> None:
        print(f"[UI] Theme: {self.guiTheme} | Lang: {self.language}")

    def displayOutput(self, data: str) -> None:
        print("[OUTPUT]", data)

    def displayImage(self, imagePath: str) -> None:
        print(f"[DISPLAY] Showing image at {imagePath}")
