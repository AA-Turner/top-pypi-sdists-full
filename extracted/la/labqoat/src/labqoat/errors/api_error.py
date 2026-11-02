"""Importable API errors for the Labqoat client."""

from __future__ import annotations

from labqoat.json_document import JsonDocument


class ApiError(Exception):
    """HTTP or transport failure with a safe message."""

    def __init__(
        self,
        message: str,
        status: int | None = None,
        problem: JsonDocument | None = None,
        request_id: str | None = None,
        retry_after: str | None = None,
    ) -> None:
        """Store safe Problem Details and response context."""
        super().__init__(message)
        self.message = message
        self.status = status
        self.problem = problem
        self.request_id = request_id
        self.retry_after = retry_after
