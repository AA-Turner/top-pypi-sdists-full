"""Exceptions raised by the Daikin Onecta client."""

from .rate_limit import RateLimit


class OnectaError(Exception):
    """Base exception for Daikin Onecta errors."""


class OnectaAccessTokenError(OnectaError):
    """Raised when an OAuth access token cannot provide an account ID."""


class OnectaRequestError(OnectaError):
    """Base exception for a failed request to the Daikin Onecta API."""

    def __init__(self, message: str, *, method: str, path: str) -> None:
        """Initialize the request error with safe request context."""
        super().__init__(message)
        self.method = method
        self.path = path


class OnectaConnectionError(OnectaRequestError):
    """Raised when communication with the Daikin Onecta API fails."""


class OnectaAuthenticationError(OnectaRequestError):
    """Raised when authentication with the Daikin Onecta API fails."""

    def __init__(self, status: int, *, method: str, path: str) -> None:
        """Initialize the authentication error."""
        super().__init__(
            f"Daikin Onecta API authentication failed with HTTP {status}",
            method=method,
            path=path,
        )
        self.status = status


class OnectaRateLimitError(OnectaRequestError):
    """Raised when the Daikin Onecta API rate limit is exceeded."""

    def __init__(self, rate_limit: RateLimit, *, method: str, path: str) -> None:
        """Initialize the rate limit error."""
        super().__init__("Daikin Onecta API rate limit exceeded", method=method, path=path)
        self.rate_limit = rate_limit
        self.retry_after = rate_limit.retry_after


class OnectaApiError(OnectaRequestError):
    """Raised when the Daikin Onecta API returns an unexpected response."""

    def __init__(self, status: int, message: str, *, method: str, path: str) -> None:
        """Initialize the API error."""
        super().__init__(
            f"Daikin Onecta API returned HTTP {status}: {message}",
            method=method,
            path=path,
        )
        self.status = status
        self.message = message


class OnectaResponseError(OnectaApiError):
    """Raised when a successful API response has an invalid body."""
