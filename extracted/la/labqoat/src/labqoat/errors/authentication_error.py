"""Typed authentication failures without secrets."""

from __future__ import annotations

from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument


class AuthenticationError(ApiError):
    """Rejected credentials for an API request."""

    def __init__(
        self,
        message: str = "Authentication failed.",
        status: int = 401,
        problem: JsonDocument | None = None,
        request_id: str | None = None,
        retry_after: str | None = None,
    ) -> None:
        """Store the message and safe response context."""
        super().__init__(message, status, problem, request_id, retry_after)
