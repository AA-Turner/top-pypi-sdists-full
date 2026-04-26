"""Compact tool output for conversation replay.

When resuming a conversation, historical tool results are replayed into the
context window.  Full payloads (which may be 100 KB+) would waste tokens.
This module produces a bounded, LLM-friendly summary while preserving
structured fields that the model needs (exit_code, error, path, etc.).

The original stored data is never mutated — compaction is applied only to
the messages sent to the LLM on resume.

This module also exposes :func:`summarize` — a CLI/UI-facing helper (added in
#1367, stable API consumed by web-UI follow-up #1467) that returns a plain-text
head/tail slice of a tool result for visual display. It is strictly additive:
``compact_tool_output`` (the LLM-replay path) is unchanged.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

# Fields that carry structured metadata the LLM should always see.
_STRUCTURED_FIELDS: frozenset[str] = frozenset(
    {
        "exit_code",
        "error",
        "status",
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


# ---------------------------------------------------------------------------
# CLI/UI-facing summariser (#1367)
# ---------------------------------------------------------------------------


def _head_tail_slice(text: str, head_lines: int, tail_lines: int) -> str:
    """Return a plain-text head/tail slice with a ``[+N lines]`` marker.

    Mirrors ``cli/density.densify_output`` for the COMPACT mode. Kept here so
    callers that want a field-aware summary (web UI, renderer fallback) can
    reuse it without importing CLI code.
    """
    head_lines = max(0, head_lines)
    tail_lines = max(0, tail_lines)
    if not text:
        return ""
    lines = text.split("\n")
    if len(lines) <= head_lines + tail_lines:
        return text
    omitted = len(lines) - head_lines - tail_lines
    parts: list[str] = []
    if head_lines:
        parts.extend(lines[:head_lines])
    parts.append(f"... [+{omitted} lines]")
    if tail_lines:
        parts.extend(lines[-tail_lines:])
    return "\n".join(parts)


def summarize(
    raw: Any,
    *,
    head_lines: int = 3,
    tail_lines: int = 2,
) -> str:
    """Return a plain-text summary of *raw* for CLI / UI display.

    Added in #1367. Additive to ``compact_tool_output`` — callers that need an
    LLM-replay JSON bundle must continue to use :func:`compact_tool_output`.

    Behaviour:
        - ``None`` / empty → empty string.
        - Plain strings → head/tail slice (``head_lines`` + marker + ``tail_lines``).
        - Dicts → prefer ``error`` (raised as-is), then ``stdout`` / ``content``
          / ``text`` / ``output`` / ``result`` in priority order. The selected
          bulk field is sliced via :func:`_head_tail_slice`.
        - Other types → ``repr()``.

    The helper never raises; pathological inputs degrade to ``repr(raw)``.
    """
    if raw is None:
        return ""

    if isinstance(raw, str):
        return _head_tail_slice(raw, head_lines, tail_lines)

    if isinstance(raw, dict):
        # Surface errors first — callers render them with salience.
        if "error" in raw and raw["error"]:
            err = raw["error"]
            return err if isinstance(err, str) else _safe_dumps(err)

        # Preferred bulk field order.
        for key in ("stdout", "content", "text", "output", "result"):
            if key in raw and raw[key]:
                value = raw[key]
                if isinstance(value, str):
                    return _head_tail_slice(value, head_lines, tail_lines)
                # Non-string bulk — repr as JSON then slice.
                return _head_tail_slice(_safe_dumps(value), head_lines, tail_lines)

        # Nothing to summarise — return a compact repr of the structured keys.
        cleaned = {k: v for k, v in raw.items() if not str(k).startswith("_")}
        return _safe_dumps(cleaned)

    # Fall-through for primitives / unexpected types.
    try:
        return str(raw)
    except Exception:
        return repr(raw)


# ---------------------------------------------------------------------------
# Web-UI helpers (#1467)
# ---------------------------------------------------------------------------

# Error-class taxonomy shared by CLI salience and web `tool-error-*` CSS.
# Keep in sync with docs/web-ui/tool-density.md and tests/js/tool_density.test.js.
_ERROR_CLASS_EXIT_NONZERO = "exit_nonzero"
_ERROR_CLASS_EXCEPTION = "exception"
_ERROR_CLASS_TIMEOUT = "timeout"
_ERROR_CLASS_DENIED = "denied"


def derive_error_class(output: Any, status: str | None) -> str | None:
    """Classify a tool-call failure into one of four buckets.

    Added in #1467. Pure, never raises.

    Returns one of ``"exit_nonzero"``, ``"exception"``, ``"timeout"``,
    ``"denied"``, or ``None`` when the call is not considered a failure.

    Heuristics:
        * ``status == "success"`` → always ``None`` (no error class applied).
        * Non-dict outputs with a non-success status map to ``exception``.
        * Dict outputs: inspect ``error``/``denied``/``timeout``/``exit_code``
          fields in order of specificity.

    Callers in ``routers/chat.py`` gate this helper on ``cli.density.mode``
    so the zero-config DOM stays byte-identical to today.
    """
    if status is None:
        return None
    if status == "success":
        return None

    if not isinstance(output, dict):
        return _ERROR_CLASS_EXCEPTION

    # Explicit denial (approval declined, hard-block, rate limit)
    if output.get("denied") or output.get("blocked"):
        return _ERROR_CLASS_DENIED
    error_str = output.get("error")
    if isinstance(error_str, str):
        lowered = error_str.lower()
        if "denied" in lowered or "blocked" in lowered or "not allowed" in lowered:
            return _ERROR_CLASS_DENIED
        if "timeout" in lowered or "timed out" in lowered:
            return _ERROR_CLASS_TIMEOUT

    # Explicit timeout signal
    if output.get("timeout") or output.get("timed_out"):
        return _ERROR_CLASS_TIMEOUT
    if status == "timeout":
        return _ERROR_CLASS_TIMEOUT

    # Non-zero exit code → exit_nonzero
    for key in ("exit_code", "returncode"):
        val = output.get(key)
        if isinstance(val, int) and val != 0:
            return _ERROR_CLASS_EXIT_NONZERO

    # Fallthrough: generic exception
    if output.get("error") or output.get("exception"):
        return _ERROR_CLASS_EXCEPTION

    # Unknown failure shape — treat as exception
    return _ERROR_CLASS_EXCEPTION


def _shape_signature(value: Any) -> Any:
    """Recursive structural signature capturing keys + types, not bulk content.

    Strings collapse to their type tag; numbers collapse to ``"int"``/``"float"``;
    dicts preserve key ordering by sorted key; lists capture length + element
    signatures (up to 8 elements, then a truncation marker).
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, dict):
        # Preserve exit_code/returncode values since they drive error-class
        # classification; other values collapse to their type signature.
        out: dict[str, Any] = {}
        for k in sorted(str(x) for x in value.keys()):
            raw_v = value.get(k)
            if k in ("exit_code", "returncode") and isinstance(raw_v, int):
                out[k] = raw_v
            else:
                out[k] = _shape_signature(raw_v)
        return out
    if isinstance(value, list):
        if not value:
            return []
        head = [_shape_signature(v) for v in value[:8]]
        if len(value) > 8:
            head.append(f"...[+{len(value) - 8}]")
        return head
    return type(value).__name__


def compute_shape_hash(output: Any) -> str:
    """Return a 16-char SHA-256 hex digest of *output*'s structural shape.

    Added in #1467. Used by the web UI to collapse ≥3 consecutive tool results
    with identical shape into a single ``.tool-repeat-collapsed`` row. Two
    tool outputs with the same bulk content but different structured fields
    (e.g., different ``exit_code``) hash to different values.

    Pure, never raises. ``None`` / pathological inputs hash to a stable value.
    """
    try:
        sig = _shape_signature(output)
        payload = json.dumps(sig, sort_keys=True, default=str)
    except Exception:
        payload = repr(output)
    return hashlib.sha256(payload.encode("utf-8", errors="replace")).hexdigest()[:16]
