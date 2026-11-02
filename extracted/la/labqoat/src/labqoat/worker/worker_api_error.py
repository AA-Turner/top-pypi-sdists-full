"""Sanitized assignment API errors with explicit retry classification."""

import json
import re


class WorkerApiError(RuntimeError):
    """A worker transport or HTTP failure without credential-bearing payloads."""

    def __init__(self, message: str, status: int | None = None, code: str | None = None) -> None:
        """Retain the HTTP status when a response was received."""
        super().__init__(message)
        self.status = status
        self.code = code

    def interrupted(self) -> bool:
        """Whether the connection, not the service's answer, failed: a lost or closed stream, overload or a 5xx."""
        if self.code == "stream_failed":
            return False
        return self.status is None or self.status >= 500 or self.status in (408, 429)

    @classmethod
    def from_response(cls, status: int, content: bytes) -> "WorkerApiError":
        """Retain only a bounded machine-readable reason and field names, never server-supplied diagnostic text."""
        try:
            document = json.loads(content)
        except (ValueError, UnicodeDecodeError):
            document = None
        candidate = document.get("code") if isinstance(document, dict) else None
        error = cls.coded(f"Worker API returned HTTP {status}", status, candidate)
        fields = cls.fields(document)
        return cls(f"{error} at {', '.join(fields)}", status, error.code) if fields else error

    @staticmethod
    def fields(document: object) -> list[str]:
        """Name up to three rejected fields by their bounded identifiers, never by the text that came with them."""
        errors = document.get("errors") if isinstance(document, dict) else None
        named = [item.get("field") for item in errors if isinstance(item, dict)] if isinstance(errors, list) else []
        return [name for name in named if isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.\[\]/-]{1,64}", name)][
            :3
        ]

    @classmethod
    def coded(cls, message: str, status: int | None, candidate: object) -> "WorkerApiError":
        """Name a well-formed reason in the message so tracebacks identify which authority check failed."""
        if isinstance(candidate, str) and re.fullmatch(r"[a-z][a-z0-9_]{0,99}", candidate):
            return cls(f"{message} ({candidate})", status, candidate)
        return cls(message, status)
