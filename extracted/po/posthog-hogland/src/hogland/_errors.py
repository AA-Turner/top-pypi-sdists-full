"""Exception hierarchy for the hogland SDK.

All errors raised by the public API derive from :class:`HoglandError`, so
callers can either catch the specific subclass or the umbrella. The HTTP
errors expose ``status_code`` and the parsed problem-details body when
available (hogplane returns ``application/problem+json`` per RFC 7807).
"""

from __future__ import annotations

from typing import Any


class HoglandError(Exception):
    """Base for every error the SDK raises."""


class ConfigurationError(HoglandError):
    """The client was constructed with missing or invalid configuration."""


class APIError(HoglandError):
    """Server returned a non-success HTTP response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        body: dict[str, Any] | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body or {}
        self.request_id = request_id


class AuthenticationError(APIError):
    """401 — missing or invalid bearer."""


class PermissionDeniedError(APIError):
    """403 — caller authenticated but isn't allowed to touch this box."""


class NotFoundError(APIError):
    """404 — box / snapshot / file path doesn't exist."""


class ConflictError(APIError):
    """409 — box is in a state that can't accept this op (e.g. snapshot while paused)."""


class ValidationError(APIError):
    """422 — request body failed server-side validation."""


class RateLimitError(APIError):
    """429 — too many requests."""


class ServerError(APIError):
    """5xx — hogplane or hogd reported an internal failure."""


def from_status(status_code: int, message: str, body: dict[str, Any] | None = None) -> APIError:
    """Map an HTTP status to the most specific :class:`APIError` subclass."""
    cls: type[APIError] = {
        401: AuthenticationError,
        403: PermissionDeniedError,
        404: NotFoundError,
        409: ConflictError,
        422: ValidationError,
        429: RateLimitError,
    }.get(status_code, ServerError if status_code >= 500 else APIError)
    return cls(message, status_code=status_code, body=body)
