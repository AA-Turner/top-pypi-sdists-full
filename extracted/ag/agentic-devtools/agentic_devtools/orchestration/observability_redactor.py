"""Sensitive data redaction for observability logs.

Implements dual-strategy redaction:
1. Key-name matching (case-insensitive) for known sensitive field names.
2. Value-pattern matching for token/credential patterns.
"""

from __future__ import annotations

import copy
import re
from typing import Any

# Keys whose values should always be redacted (case-insensitive comparison)
_SENSITIVE_KEYS: frozenset[str] = frozenset(
    {
        "authorization",
        "cookie",
        "set-cookie",
        "token",
        "pat",
        "api_key",
        "api-key",
        "apikey",
        "password",
        "secret",
        "private_key",
        "private-key",
        "access_token",
        "refresh_token",
    }
)

# Patterns that indicate a value is a credential (compiled for performance).
# Unanchored with word-boundary prefix so search() catches tokens embedded in
# larger strings (e.g. "token=ghp_...") while avoiding false matches within
# longer identifiers (e.g. "my_ghp_value" is NOT matched).
_VALUE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bghp_[A-Za-z0-9_]+"),  # GitHub personal access token
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]+"),  # GitHub fine-grained PAT
    re.compile(r"\bgho_[A-Za-z0-9_]+"),  # GitHub OAuth token
    re.compile(r"\bghs_[A-Za-z0-9_]+"),  # GitHub server token
    re.compile(r"Bearer\s+\S+", re.IGNORECASE),  # ******
]

_REDACTED = "[REDACTED]"


def _normalize_key_name(key: str) -> str:
    """Normalize a key name for case-insensitive snake/camel/hyphen matching."""
    return key.replace("_", "").replace("-", "").lower()


def _split_key_words(key: str) -> set[str]:
    """Split a key into lowercase words across separators and camel-case boundaries."""
    separated = key.replace("_", " ").replace("-", " ")
    separated = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", separated)
    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", separated)
    return {part.lower() for part in separated.split() if part}


class Redactor:
    """Redacts sensitive data from observability event payloads.

    Supports customization via additional sensitive keys and value
    patterns provided at construction time.
    """

    def __init__(
        self,
        extra_keys: frozenset[str] | None = None,
        extra_patterns: list[re.Pattern[str]] | None = None,
    ) -> None:
        self._sensitive_keys = {_normalize_key_name(key) for key in (_SENSITIVE_KEYS | (extra_keys or frozenset()))}
        self._value_patterns = _VALUE_PATTERNS + (extra_patterns or [])

    def redact(self, data: Any) -> Any:
        """Return a deep copy of *data* with sensitive values masked.

        Args:
            data: Arbitrary data structure (dict, list, str, etc.).

        Returns:
            A sanitized copy; original data is never mutated.
            Falls back to ``None`` when the data cannot be deep-copied
            (e.g. objects that forbid copying or recursive structures),
            to preserve the best-effort logging contract.
        """
        if data is None:
            return None
        try:
            copied = copy.deepcopy(data)
        except Exception:
            # Best-effort: if we cannot deep-copy, return None so we never
            # expose (potentially partial) sensitive data and never crash.
            return None
        return self._redact_value(copied)

    def _is_sensitive_key(self, key: str) -> bool:
        """Check if a key name indicates sensitive content."""
        normalized = _normalize_key_name(key)
        if normalized in self._sensitive_keys:
            return True
        words = _split_key_words(key)
        if not words:
            return False
        if {"api", "key"} <= words or {"private", "key"} <= words or {"github", "pat"} <= words:
            return True
        return bool(words & {"authorization", "cookie", "password", "secret", "token"})

    def _is_sensitive_value(self, value: str) -> bool:
        """Check if a string value matches a credential pattern."""
        for pattern in self._value_patterns:
            if pattern.search(value):
                return True
        return False

    def _redact_value(self, data: Any) -> Any:
        """Recursively redact sensitive data."""
        if isinstance(data, dict):
            return {str(k): self._redact_dict_value(str(k), v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._redact_value(item) for item in data]
        if isinstance(data, str):
            if self._is_sensitive_value(data):
                return _REDACTED
            return data
        if isinstance(data, (bool, int, float, type(None))):
            # JSON-native primitives – pass through unchanged.
            return data
        # Unknown object: json.dumps(default=str) would coerce this via str(), potentially
        # exposing credentials embedded in __str__. Coerce eagerly so the value-pattern
        # check can catch any credential strings before they reach the log file.
        coerced = str(data)
        if self._is_sensitive_value(coerced):
            return _REDACTED
        return coerced

    def _redact_dict_value(self, key: str, value: Any) -> Any:
        """Redact a dictionary value based on its key and content."""
        if self._is_sensitive_key(key):
            return _REDACTED
        if isinstance(value, str):
            if self._is_sensitive_value(value):
                return _REDACTED
            return value
        if isinstance(value, dict):
            return {str(k): self._redact_dict_value(str(k), v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._redact_value(item) for item in value]
        if isinstance(value, (bool, int, float, type(None))):
            # JSON-native primitives – pass through unchanged.
            return value
        # Unknown object: same coercion as _redact_value to prevent __str__-based leakage.
        coerced = str(value)
        if self._is_sensitive_value(coerced):
            return _REDACTED
        return coerced
