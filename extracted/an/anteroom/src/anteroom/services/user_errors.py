"""User-facing error normalization helpers for CLI and web surfaces."""

from __future__ import annotations

import re
from typing import Any, Mapping

_WHITESPACE_RE = re.compile(r"\s+")
_TRACEBACK_RE = re.compile(r"traceback \(most recent call last\):", re.IGNORECASE)


def normalize_error_text(text: Any, *, fallback: str = "An internal error occurred") -> str:
    """Collapse user-visible error text to a compact single line."""
    if text is None:
        return fallback
    value = str(text).strip()
    if not value:
        return fallback

    if _TRACEBACK_RE.search(value):
        lines = [line.strip() for line in value.splitlines() if line.strip()]
        if lines:
            value = lines[-1]

    value = _WHITESPACE_RE.sub(" ", value).strip()
    return value or fallback


def default_error_suggestion(code: str, *, base_url: str | None = None) -> str | None:
    """Return a short next-step suggestion for a known error code."""
    if code == "auth_failed":
        return "Run: aroom init"
    if code in {"connection_error", "html_response"} and base_url:
        return f"Check AI_CHAT_BASE_URL ({base_url})"
    if code == "connection_error":
        return "Check AI_CHAT_BASE_URL"
    if code == "context_length_exceeded":
        return "Start a new conversation or compact context"
    if code == "too_many_tools":
        return "Reduce MCP tools or set ai.max_tools"
    if code == "rate_limit":
        return "Wait a moment and retry"
    if code == "timeout":
        return "Retry or increase ai.request_timeout"
    if code == "api_error":
        return "Retry shortly"
    return None


def format_user_error(error: Mapping[str, Any] | str | None) -> str:
    """Render a compact user-facing one-line error message."""
    if isinstance(error, Mapping):
        message = normalize_error_text(error.get("message"))
        suggestion = normalize_error_text(error.get("suggestion"), fallback="") if error.get("suggestion") else ""
    else:
        message = normalize_error_text(error)
        suggestion = ""

    if suggestion and suggestion.lower() not in message.lower():
        return f"{message} — {suggestion}"
    return message


def build_user_error(
    message: str,
    *,
    code: str = "error",
    suggestion: str | None = None,
    retryable: bool = False,
    provider: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Create a backward-compatible user error payload with display text."""
    normalized_message = normalize_error_text(message)
    normalized_suggestion = normalize_error_text(
        suggestion or default_error_suggestion(code, base_url=base_url),
        fallback="",
    )
    payload: dict[str, Any] = {
        "message": normalized_message,
        "code": code,
        "retryable": bool(retryable),
        "display_message": normalized_message,
    }
    if normalized_suggestion:
        payload["suggestion"] = normalized_suggestion
        payload["display_message"] = f"{normalized_message} — {normalized_suggestion}"
    if provider:
        payload["provider"] = provider
    if model:
        payload["model"] = model
    return payload
