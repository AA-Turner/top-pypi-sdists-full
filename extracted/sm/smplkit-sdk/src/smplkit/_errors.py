"""Structured SDK error types."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ApiErrorDetail:
    """A single error object from the server's JSON:API ``errors`` array."""

    status: str | None = None
    code: str | None = None
    """
    Application-specific machine-readable error code (e.g.
    ``environment_unmanaged``). Per JSON:API §7, smplkit sets this on
    every error so callers can branch without string-matching the human
    ``detail``.
    """
    title: str | None = None
    detail: str | None = None
    source: dict[str, Any] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)
    """Additional structured context (e.g. ``{"environment": "staging"}``)."""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.status is not None:
            d["status"] = self.status
        if self.code is not None:
            d["code"] = self.code
        if self.title is not None:
            d["title"] = self.title
        if self.detail is not None:
            d["detail"] = self.detail
        if self.source:
            d["source"] = self.source
        if self.meta:
            d["meta"] = self.meta
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def _derive_message(errors: list[ApiErrorDetail]) -> str:
    """Derive a human-readable message from a list of API error details."""
    if not errors:
        return "An API error occurred"
    first = errors[0]
    msg = first.detail or first.title or first.status or "An API error occurred"
    extra = len(errors) - 1
    if extra == 1:
        msg += " (and 1 more error)"
    elif extra > 1:
        msg += f" (and {extra} more errors)"
    return msg


def _parse_error_body(content: bytes) -> list[ApiErrorDetail]:
    """Parse the JSON:API error body, returning an empty list on failure."""
    try:
        body = json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []
    raw_errors = body.get("errors") if isinstance(body, dict) else None
    if not isinstance(raw_errors, list):
        return []
    result: list[ApiErrorDetail] = []
    for item in raw_errors:
        if not isinstance(item, dict):
            continue
        source = item.get("source")
        meta = item.get("meta")
        result.append(
            ApiErrorDetail(
                status=item.get("status"),
                code=item.get("code"),
                title=item.get("title"),
                detail=item.get("detail"),
                source=source if isinstance(source, dict) else {},
                meta=meta if isinstance(meta, dict) else {},
            )
        )
    return result


class Error(Exception):
    """Base exception for all smplkit SDK errors."""

    def __init__(
        self,
        message: str | None = None,
        *,
        errors: list[ApiErrorDetail] | None = None,
        status_code: int | None = None,
    ) -> None:
        self.errors: list[ApiErrorDetail] = errors or []
        self.status_code: int | None = status_code
        if message is None:
            message = _derive_message(self.errors)
        super().__init__(message)

    def __str__(self) -> str:
        base = super().__str__()
        if not self.errors:
            return base
        if len(self.errors) == 1:
            return f"{base}\nError: {self.errors[0].to_json()}"
        lines = [base, "Errors:"]
        for i, err in enumerate(self.errors):
            lines.append(f"  [{i}] {err.to_json()}")
        return "\n".join(lines)


class ConnectionError(Error):
    """Raised when a network request fails."""


class TimeoutError(Error):
    """Raised when an operation exceeds its timeout."""


class NotFoundError(Error):
    """Raised when a requested resource does not exist."""


class ConflictError(Error):
    """Raised when an operation conflicts with current state (e.g., deleting a config that has children)."""


class ValidationError(Error):
    """Raised when the server rejects a request due to validation errors."""


class PaymentRequiredError(Error):
    """Raised when the server rejects a request because the account's
    subscription plan does not include the required entitlement."""


class NotInstalledError(Error):
    """Raised when a logging operation is attempted before ``install()``.

    Smpl Logging monkey-patches the standard logging framework, so it stays
    opt-in: its live surface requires an explicit
    :meth:`LoggingClient.install` first. Config and flags connect lazily on
    first live use and never raise this."""


def _raise_for_status(status_code: int, content: bytes) -> None:
    """Parse a non-2xx response and raise the appropriate SDK exception.

    Raises nothing if the status code is 2xx.
    """
    if 200 <= status_code < 300:
        return

    errors = _parse_error_body(content)
    message = _derive_message(errors) if errors else f"HTTP {status_code}"

    exc_cls: type[Error]
    if status_code == 402:
        exc_cls = PaymentRequiredError
    elif status_code == 404:
        exc_cls = NotFoundError
    elif status_code == 409:
        exc_cls = ConflictError
    elif status_code in (400, 422):
        exc_cls = ValidationError
    else:
        exc_cls = Error

    raise exc_cls(message, errors=errors, status_code=status_code)
