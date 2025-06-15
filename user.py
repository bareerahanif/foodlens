class User:
    def __init__(self, username: str, email: str, password: str, dob: str, tier: str = "personal"):
        self.username = username
        self.email = email
        self.__password = password
        self.dob = dob
        self.tier = tier

    def signUp(self, auth_manager) -> bool:
        return auth_manager.signUp(self.username, self.email, self.__password, self.dob)

    def login(self, auth_manager) -> bool:
        return auth_manager.authenticateUser(self.email, self.__password)

    def logout(self) -> None:
        print(f"[LOGOUT] {self.username} logged out.")

    def getSubscriptionTier(self) -> str:
        return self.tier