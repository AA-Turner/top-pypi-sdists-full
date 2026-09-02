from __future__ import annotations


class FastinoError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_data: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class FastinoAuthError(FastinoError):
    """401 — missing / invalid / expired API key."""


class FastinoValidationError(FastinoError):
    """400 / 422 — the request payload was rejected."""


class FastinoServerError(FastinoError):
    """5xx — the Fastino API failed server-side."""
