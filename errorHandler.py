class ErrorHandler:
    def __init__(self, errorCode="", errorMessage=""):
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.error_messages = {
            "API_KEY_MISSING": "API key not configured for this model",
            "API_REQUEST_FAILED": "API request failed",
            "API_RATE_LIMIT": "API rate limit exceeded",
            "API_INVALID_RESPONSE": "Invalid API response"
        }

    def displayErrorMessage(self, code: str) -> None:
        message = self.error_messages.get(code, "Something went wrong")
        print(f"[ERROR {code}] {message}")

    def logError(self, error: str) -> None:
        print(f"[API ERROR] {error}")

    def handle_api_error(self, response):
        """Handle specific API error responses"""
        if response.status_code == 401:
            self.displayErrorMessage("API_KEY_MISSING")
        elif response.status_code == 429:
            self.displayErrorMessage("API_RATE_LIMIT")
        else:
            self.displayErrorMessage("API_REQUEST_FAILED")
        self.logError(f"Status Code: {response.status_code}, Response: {response.text}")