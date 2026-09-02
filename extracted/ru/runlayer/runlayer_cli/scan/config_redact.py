"""Redact MCP configuration values before they leave the device.

Only references to environment variables are useful to the backend. Literal
values may be credentials, so they are reduced to a length marker. This module
uses only the stdlib plus the RE2 ``regex_safe`` wrapper, because it is part
of the frozen ``aiwatch`` import closure.
"""

from __future__ import annotations

from collections.abc import Collection
from typing import Any

from runlayer_cli import regex_safe

BENIGN_ENV_KEYS = frozenset(
    {
        "DEBUG",
        "HOST",
        "LOG_LEVEL",
        "NODE_ENV",
        "PORT",
        "TZ",
    }
)

_PLACEHOLDER = regex_safe.compile(
    r"(?:"
    r"\$\{env:[A-Za-z_][A-Za-z0-9_.-]*\}"
    r"|\{env:[A-Za-z_][A-Za-z0-9_.-]*\}"
    r"|\$\{[A-Za-z_][A-Za-z0-9_.-]*\}"
    r")",
    regex_safe.IGNORECASE,
)
_SAFE_SCAFFOLD_WORDS = frozenset({"basic", "bearer", "token"})
_SCAFFOLD_WORD = regex_safe.compile(r"[A-Za-z]+")


def _is_placeholder_value(value: str) -> bool:
    """Return whether ``value`` contains placeholders and only safe scaffolding."""
    if _PLACEHOLDER.search(value) is None:
        return False
    remainder = _PLACEHOLDER.sub("", value)
    words = _SCAFFOLD_WORD.findall(remainder)
    if any(word.lower() not in _SAFE_SCAFFOLD_WORDS for word in words):
        return False
    return _SCAFFOLD_WORD.sub("", remainder).strip(" \t:=_-") == ""


def redact_config_mapping(
    value: Any,
    *,
    allowed_literal_keys: Collection[str] = (),
) -> Any:
    """Redact literal mapping values while retaining useful placeholders.

    ``allowed_literal_keys`` is explicit so the benign environment-variable
    allowlist is never accidentally applied to HTTP headers.
    """
    if not isinstance(value, dict):
        return value

    allowed = {key.upper() for key in allowed_literal_keys}
    redacted: dict[str, str] = {}
    for raw_key, raw_value in value.items():
        key = str(raw_key)
        string_value = str(raw_value)
        if key.upper() in allowed or _is_placeholder_value(string_value):
            redacted[key] = string_value
        else:
            redacted[key] = f"<redacted:len={len(string_value)}>"
    return redacted
