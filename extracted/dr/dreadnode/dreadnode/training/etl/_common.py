"""Shared normalization helpers for training ETL."""

from __future__ import annotations

import typing as t


def normalize_optional_string(value: t.Any) -> str | None:
    """Normalize arbitrary input into a stripped string when possible."""

    if value is None:
        return None
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    return str(value)


def normalize_prompt(record: dict[str, t.Any]) -> str | None:
    """Return the best-effort prompt string from a dataset record."""

    for key in ("prompt", "input", "question", "task_prompt"):
        value = record.get(key)
        normalized = normalize_optional_string(value)
        if normalized:
            return normalized
    return None


def normalize_messages(value: t.Any) -> list[dict[str, str]]:
    """Return normalized chat messages from a dataset record field."""

    if not isinstance(value, list):
        return []
    messages: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        role = normalize_optional_string(item.get("role")) or "user"
        content = normalize_optional_string(item.get("content"))
        if content is None:
            continue
        messages.append({"role": role, "content": content})
    return messages


def apply_system_prompt(
    *,
    system_prompt: str | None,
    messages: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Inject or merge a system prompt into a chat message list."""

    normalized_system_prompt = normalize_optional_string(system_prompt)
    if normalized_system_prompt is None:
        return messages

    if messages and messages[0]["role"] == "system":
        merged = dict(messages[0])
        merged["content"] = (
            f"{normalized_system_prompt}\n\n{messages[0]['content']}".strip()
        )
        return [merged, *messages[1:]]

    return [{"role": "system", "content": normalized_system_prompt}, *messages]


__all__ = [
    "apply_system_prompt",
    "normalize_messages",
    "normalize_optional_string",
    "normalize_prompt",
]
