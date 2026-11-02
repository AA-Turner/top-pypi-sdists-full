"""Transport failures without leaking request details."""

from __future__ import annotations

from labqoat.errors.api_error import ApiError


class TransportError(ApiError):
    """Unreachable API or timed-out request."""

    def __init__(self, message: str = "Could not reach the API.", timed_out: bool = False) -> None:
        """Store the message and whether a deadline expired."""
        super().__init__(message, status=None)
        self.timed_out = timed_out
