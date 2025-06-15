class ClipboardManager:
    def __init__(self):
        self.copiedText = ""

    def copyResults(self, text: str) -> None:
        self.copiedText = text
        print("[CLIPBOARD] Text copied.")

    def checkOutputBeforeCopy(self) -> bool:
        return len(self.copiedText) > 0
