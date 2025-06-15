class ThirdPartyIntegration:
    def __init__(self, appName: str):
        self.appName = appName
        self.permissionsGranted = False

    def linkWithThirdPartyApp(self, appName: str) -> bool:
        self.permissionsGranted = True
        return True

    def syncNutritionalData(self, data: dict) -> None:
        print(f"[SYNC] Synced with {self.appName}")

    def checkDataAvailability(self) -> bool:
        return self.permissionsGranted
