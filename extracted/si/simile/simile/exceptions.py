class SimileAPIError(Exception):
    """Base exception for Simile API client errors."""

    def __init__(self, message: str, status_code: int = None, detail: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail

    def __str__(self):
        if self.status_code and self.detail:
            return f"{super().__str__()} (Status Code: {self.status_code}, Detail: {self.detail})"
        elif self.status_code:
            return f"{super().__str__()} (Status Code: {self.status_code})"
        return super().__str__()


class SimileAuthenticationError(SimileAPIError):
    """Exception for authentication errors (e.g., invalid API key)."""

    def __init__(
        self,
        message: str = "Authentication failed. Ensure API key is valid.",
        status_code: int = 401,
        detail: str = None,
    ):
        super().__init__(message, status_code, detail)


class SimileNotFoundError(SimileAPIError):
    """Exception for resource not found errors (404)."""

    def __init__(
        self,
        message: str = "Resource not found.",
        status_code: int = 404,
        detail: str = None,
    ):
        super().__init__(message, status_code, detail)


class SimileBadRequestError(SimileAPIError):
    """Exception for bad request errors (400)."""

    def __init__(self, message: str = "Bad request.", status_code: int = 400, detail: str = None):
        super().__init__(message, status_code, detail)
