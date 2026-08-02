"""Utilities for sanitising LLM `extra_headers` dictionaries.

Organization-default and agent-override headers are user-editable (stored in
Supabase as `jsonb`). It is therefore possible for the dict to contain empty
keys, empty values, or whitespace-only strings that crash downstream provider
clients (OpenAI, Anthropic, Azure, etc.). This helper defensively drops any
entry that would not be a valid HTTP header.

See PRO-1300.
"""

from typing import Any, Dict, Optional


def sanitize_extra_headers(headers: Optional[Dict[Any, Any]]) -> Dict[str, str]:
    """Return a copy of ``headers`` with empty/invalid entries removed.

    Rules:
      * ``None`` or non-dict input → ``{}``.
      * Keys that are not strings (or that become empty after ``strip``) are
        dropped.
      * Values are coerced to ``str`` (so JSON numbers/bools survive), trimmed,
        and dropped if the trimmed value is empty.
      * ``None`` values are always dropped.

    The function is idempotent: ``sanitize_extra_headers(sanitize_extra_headers(x))``
    equals ``sanitize_extra_headers(x)``.
    """
    if not headers or not isinstance(headers, dict):
        return {}

    sanitized: Dict[str, str] = {}
    for raw_key, raw_value in headers.items():
        if not isinstance(raw_key, str):
            continue
        key = raw_key.strip()
        if not key:
            continue
        if raw_value is None:
            continue
        value = raw_value if isinstance(raw_value, str) else str(raw_value)
        value = value.strip()
        if not value:
            continue
        sanitized[key] = value
    return sanitized
