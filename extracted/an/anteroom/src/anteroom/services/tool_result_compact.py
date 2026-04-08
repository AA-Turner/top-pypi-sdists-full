"""Compact tool output for conversation replay.

When resuming a conversation, historical tool results are replayed into the
context window.  Full payloads (which may be 100 KB+) would waste tokens.
This module produces a bounded, LLM-friendly summary while preserving
structured fields that the model needs (exit_code, error, path, etc.).

The original stored data is never mutated — compaction is applied only to
the messages sent to the LLM on resume.
"""

from __future__ import annotations

import json
from typing import Any

# Fields that carry structured metadata the LLM should always see.
_STRUCTURED_FIELDS: frozenset[str] = frozenset(
    {
        "exit_code",
        "error",
        "path",
        "file",
        "url",
        "returncode",
    }
)

# Fields that tend to hold large bulk content eligible for truncation.
_BULK_FIELDS: frozenset[str] = frozenset(
    {
        "stdout",
        "stderr",
        "output",
        "content",
        "text",
        "result",
    }
)


def _safe_dumps(obj: Any) -> str:
    try:
        return json.dumps(obj, default=str)
    except Exception:
        return repr(obj)


def _truncate_value(value: str, budget: int) -> str:
    """Truncate a string value to fit within budget, adding an info suffix."""
    if len(value) <= budget:
        return value
    total_chars = len(value)
    line_count = value.count("\n") + 1
    suffix = f"... [truncated -- {total_chars} chars total, {line_count} lines]"
    keep = max(0, budget - len(suffix))
    return value[:keep] + suffix


def _oversize_marker(max_chars: int) -> str:
    """Return a guaranteed-valid JSON marker indicating the result was too
    large to fit within ``max_chars``. Always parseable by ``json.loads``.
    """
    marker = '{"truncated": true}'
    if len(marker) <= max_chars:
        return marker
    # Even the marker doesn't fit -- return the smallest valid JSON object.
    return "{}"


def compact_tool_output(raw: Any, max_chars: int) -> str:
    """Return a JSON string of *raw* bounded to approximately *max_chars*.

    * Internal keys (starting with ``_``) are stripped.
    * Structured metadata fields survive intact.
    * Bulk content fields are truncated with an informative suffix when
      the serialized result would exceed *max_chars*.
    * Non-dict inputs are serialized with ``json.dumps`` and truncated
      if necessary.
    * Never raises -- returns a best-effort repr on unexpected input.
    """
    # Floor at 2 chars: the smallest valid JSON values are "{}" / "\"\"",
    # both 2 chars long. Callers' configs are already validated to >= 100,
    # so this is a defensive backstop.
    if max_chars < 2:
        max_chars = 2

    if not isinstance(raw, dict):
        text = _safe_dumps(raw)
        if len(text) <= max_chars:
            return text
        # For strings, try to keep as much of the value as fits inside a
        # valid JSON string literal with a truncation marker. For other
        # non-dict inputs, fall back to the oversize marker so the result
        # is always parseable JSON.
        if isinstance(raw, str):
            marker = "...[truncated]"
            # Reserve 2 chars for the surrounding quotes; if the marker
            # itself does not fit, fall through to the oversize marker.
            available = max_chars - 2 - len(marker)
            if available > 0:
                truncated = json.dumps(raw[:available] + marker)
                if len(truncated) <= max_chars:
                    return truncated
        return _oversize_marker(max_chars)

    # Strip internal metadata keys.
    cleaned: dict[str, Any] = {k: v for k, v in raw.items() if not k.startswith("_")}

    # Fast path: already small enough.
    full = _safe_dumps(cleaned)
    if len(full) <= max_chars:
        return full

    # Separate structured fields from bulk content.
    structured: dict[str, Any] = {}
    bulk: dict[str, Any] = {}
    other: dict[str, Any] = {}

    for key, value in cleaned.items():
        if key in _STRUCTURED_FIELDS:
            structured[key] = value
        elif key in _BULK_FIELDS:
            bulk[key] = value
        else:
            other[key] = value

    # Start with structured + other; compute remaining budget for bulk.
    base: dict[str, Any] = {**structured, **other}
    base_json = _safe_dumps(base)

    if not bulk:
        if len(base_json) <= max_chars:
            return base_json
        # Drop other fields one at a time if base is too large.
        structured_json = _safe_dumps(structured)
        if len(structured_json) <= max_chars:
            return structured_json
        return _oversize_marker(max_chars)

    remaining = max_chars - len(base_json)

    if remaining < 40:
        # No room for bulk content -- return just structured fields.
        result_json = _safe_dumps(structured)
        if len(result_json) <= max_chars:
            return result_json
        return _oversize_marker(max_chars)

    # Distribute remaining budget evenly across bulk fields.
    # We need to account for JSON overhead (key quoting, commas, colons).
    # Estimate: each field adds ~len(key) + 6 chars of JSON overhead.
    overhead_per_field = sum(len(k) + 6 for k in bulk)
    content_budget = max(20, remaining - overhead_per_field)
    per_field = max(10, content_budget // len(bulk))

    result: dict[str, Any] = dict(base)
    for key, value in bulk.items():
        text = value if isinstance(value, str) else _safe_dumps(value)
        result[key] = _truncate_value(text, per_field)

    out = _safe_dumps(result)
    if len(out) <= max_chars:
        return out

    # Still too large -- halve bulk budgets and retry once.
    per_field = max(10, per_field // 2)
    result2: dict[str, Any] = dict(base)
    for key, value in bulk.items():
        text = value if isinstance(value, str) else _safe_dumps(value)
        result2[key] = _truncate_value(text, per_field)

    out2 = _safe_dumps(result2)
    if len(out2) <= max_chars:
        return out2

    # Last resort: structured fields + minimal bulk summaries.
    result3: dict[str, Any] = dict(structured)
    for key, value in bulk.items():
        text = value if isinstance(value, str) else _safe_dumps(value)
        line_count = text.count("\n") + 1
        result3[key] = f"[{len(text)} chars, {line_count} lines]"

    out3 = _safe_dumps(result3)
    if len(out3) <= max_chars:
        return out3
    return _oversize_marker(max_chars)
