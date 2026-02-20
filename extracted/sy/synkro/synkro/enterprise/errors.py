"""Enterprise SDK error classes."""


class SynkroError(Exception):
    """Base error for all Synkro enterprise SDK errors."""


class SynkroAuthError(SynkroError):
    """401 — invalid or expired API key."""


class SynkroRateLimitError(SynkroError):
    """429 — rate limited."""

    def __init__(self, message: str, retry_after: str | None = None):
        super().__init__(message)
        self.retry_after = retry_after


class SynkroAPIError(SynkroError):
    """4xx/5xx from the API."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class SynkroNotFoundError(SynkroAPIError):
    """404 — resource not found."""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)
