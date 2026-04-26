"""Helpers for provider-facing chat message payloads."""

from __future__ import annotations

from typing import Any

_PROVIDER_MESSAGE_KEYS = {
    "role",
    "content",
    "name",
    "tool_call_id",
    "tool_calls",
}


def strip_local_message_fields(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return provider-safe message dicts without local persistence metadata.

    Conversation rows carry application-only keys such as ``id``, ``position``,
    ``metadata``, attachments, and usage fields. Provider chat APIs reject
    unknown per-message keys, so strip them at the egress boundary without
    mutating the caller's in-memory history.
    """
    sanitized: list[dict[str, Any]] = []
    for msg in messages:
        sanitized.append({key: msg[key] for key in _PROVIDER_MESSAGE_KEYS if key in msg})
    return sanitized
