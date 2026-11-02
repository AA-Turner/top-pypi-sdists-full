"""Optimistic-concurrency failures for revisioned management documents."""

from __future__ import annotations

from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument


class RevisionConflictError(ApiError):
    """A conditional update was missing its revision (428) or used a stale one (412)."""

    def __init__(
        self,
        path: str,
        status: int,
        problem: JsonDocument | None = None,
        request_id: str | None = None,
    ) -> None:
        """Explain how to recover without exposing request material."""
        if status == 428:
            message = f"Update to {path} requires the current revision (If-Match)."
        else:
            message = f"{path} changed since its revision was read; re-read it and retry."
        super().__init__(message, status, problem, request_id)

    @property
    def stale(self) -> bool:
        """Return whether a newer revision exists rather than the revision being absent."""
        return self.status == 412
