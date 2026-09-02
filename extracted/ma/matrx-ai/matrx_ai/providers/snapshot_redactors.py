"""Snapshot Redactors — single-purpose, self-documenting payload trimmers.

Why this module exists
======================
For every persisted run (capture is on by default — see
``REQUEST_SNAPSHOT_CAPTURE_DEFAULT``), we persist the *exact provider request
payload* (and best-effort response) to ``cx_request_snapshot`` so we can
reproduce what the model saw. Raw provider payloads can legitimately contain
multi-megabyte base64 blobs (inline PDFs, images, audio). Writing a 10 MB
jsonb row during an active stream saturates the DB write pool and the
snapshot write times out (seen in production 2026-04-21).

This module solves **only** that narrow problem — making the payload small
enough to write reliably — while giving up **as little fidelity as possible**.
Every byte removed is accounted for by an inline fingerprint.

Design rules (non-negotiable)
=============================
1. **Single purpose per class.** Each redactor has ONE narrowly-defined
   transformation it is allowed to perform. No redactor is allowed to do
   "whatever seems convenient". Adding a new behavior requires a new class
   with its own clear name, docstring, and reason_code.

2. **Structure is sacred.** Redactors never add, remove, rename, reorder, or
   retype keys. If the input is a dict, the output dict has identical keys in
   identical order. If a value is a string, its replacement is a string —
   not a dict, not None, not a summary object. Dict-in, dict-out;
   string-in, string-out; always.

3. **Self-describing fingerprint.** Every redacted value embeds an inline
   text marker identifying:
       - which redactor class did it
       - exactly what kind of redaction (reason_code)
       - how much (byte count + sha256 of the original)
       - the JSON path of the field
       - where to find the source code for more detail
   No "soft" redactions. No truncation without a marker.

4. **Preserve head and tail.** When shortening a long string, keep the first
   N and last N characters of the original verbatim. This lets a human
   reader visually recognize what kind of data used to be there:
       - "%PDF-1.4…"      → a PDF was here
       - "/9j/4AAQSk…"    → a JPEG was here
       - "data:image/png;base64,iVBORw0KGgo…" → PNG data URL was here
       - "<html><head>…"  → HTML was here
   The head/tail is NOT a summary — it's a verbatim slice of the original.

5. **Explicit pipeline, explicit order.** Redactors are applied by explicit
   registration order via ``apply_redactors()``. There is no hidden
   composition. There are no magic defaults baked into data structures. If
   a redactor didn't fire, it isn't in the list.

6. **Idempotent.** Running a redacted payload back through the pipeline is a
   no-op. Redactors detect their own previous work via the marker and skip.

7. **Clarity over performance.** This runs at most once per iteration on the
   write path. Correctness, readability, and auditability win every
   trade-off against micro-optimization.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

# ---------------------------------------------------------------------------
# Marker format
# ---------------------------------------------------------------------------
# The marker is a single-line, greppable sentinel that begins with
# MARKER_OPEN and ends with MARKER_CLOSE. Fields are space-separated
# key=value pairs. String values are double-quoted; numeric values are bare.
# Example (single line; wrapped here for readability):
#
#     <<<MATRX_SNAPSHOT_REDACTION
#         redactor="LargeBinaryStringRedactor"
#         reason="string_over_max_bytes"
#         original_bytes=7577567
#         original_sha256="1f3a…"
#         head_chars_preserved=128
#         tail_chars_preserved=128
#         path="$.contents[0].parts[1].inline_data.data"
#         source="matrx_ai.providers.snapshot_redactors"
#     >>>
#
# The redacted string has the shape:
#     <head_verbatim>\n<marker>\n<tail_verbatim>
# so the marker visually sits between the surviving real data.

MARKER_OPEN = "<<<MATRX_SNAPSHOT_REDACTION"
MARKER_CLOSE = ">>>"


def _fmt_marker(**fields: Any) -> str:
    """Build the inline redaction marker.

    All fields passed in are included, in insertion order. Strings are
    double-quoted with embedded quotes backslash-escaped; numbers are bare.
    """
    parts: list[str] = [MARKER_OPEN]
    for key, val in fields.items():
        if isinstance(val, bool):
            parts.append(f'{key}={"true" if val else "false"}')
        elif isinstance(val, (int, float)):
            parts.append(f"{key}={val}")
        else:
            escaped = str(val).replace("\\", "\\\\").replace('"', '\\"')
            parts.append(f'{key}="{escaped}"')
    parts.append(MARKER_CLOSE)
    return " ".join(parts)


def contains_redaction_marker(value: Any) -> bool:
    """True if ``value`` is a string already carrying a redaction marker.

    Used by redactors to guarantee idempotency — re-running the pipeline on
    an already-redacted payload is a no-op.
    """
    return isinstance(value, str) and MARKER_OPEN in value


# ---------------------------------------------------------------------------
# Redactor protocol
# ---------------------------------------------------------------------------

@runtime_checkable
class Redactor(Protocol):
    """Contract every redactor must implement.

    Implementations MUST:
      - Set ``name`` to the class name (for traceability in the marker).
      - Set ``reason_code`` to a stable, grep-friendly snake_case identifier.
      - Return the input unchanged if ``applies_to`` is False.
      - Never modify structure. Leaf-value substitutions only.
    """

    name: str
    reason_code: str

    def applies_to(self, value: Any) -> bool: ...
    def redact(self, value: Any, path: str) -> Any: ...


# ---------------------------------------------------------------------------
# LargeBinaryStringRedactor
# ---------------------------------------------------------------------------

@dataclass
class LargeBinaryStringRedactor:
    """Shortens strings that are too large to safely persist to jsonb.

    WHAT THIS REDACTOR DOES
    -----------------------
    For any string value whose UTF-8 byte length exceeds ``max_bytes``,
    replaces the *middle* of the string with a self-describing marker.
    Keeps the first ``head_chars`` and last ``tail_chars`` characters of the
    original string verbatim so a reader can visually recognize the data
    that used to be there (PDF magic bytes, base64 alphabet, JSON opening,
    HTML tags, etc.).

    WHAT THIS REDACTOR DOES NOT DO
    ------------------------------
    - Does not remove keys from dicts.
    - Does not shorten arrays.
    - Does not change a value's type (string-in ⇒ string-out, always).
    - Does not touch strings at or below ``max_bytes``.
    - Does not touch non-string values (ints, floats, bools, None, dicts,
      lists are all passed through untouched).
    - Does not re-encode, normalize, or pretty-print the bytes it keeps.
    - Does not modify a string that already contains a redaction marker
      (idempotent — see ``contains_redaction_marker``).

    WHY THIS REDACTOR EXISTS
    ------------------------
    Provider payloads legitimately contain multi-MB base64 blobs — inline
    PDFs in Google's ``contents[].parts[].inline_data.data``, inline images
    in Anthropic's ``source.data``, data-URL images in OpenAI's
    ``image_url.url``. Writing those verbatim to a jsonb row during an
    active stream saturates the DB write pool. This redactor is the
    narrowest cut that makes the write fit; anything that is NOT a giant
    leaf string is preserved exactly as the provider received it.

    TUNING
    ------
    - ``max_bytes=65536`` (64 KiB): larger than any realistic system prompt
      or human-authored message part, small enough to stop a 10 MB base64
      blob cold.
    - ``head_chars=128`` / ``tail_chars=128``: enough to identify magic
      bytes and file tails; short enough that the snapshot stays trivially
      readable.
    """

    max_bytes: int = 65536
    head_chars: int = 128
    tail_chars: int = 128

    name: str = "LargeBinaryStringRedactor"
    reason_code: str = "string_over_max_bytes"

    def applies_to(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        # Cheap upper-bound first: UTF-8 bytes >= char count, so if the char
        # count is already <= max_bytes we know bytes is too.
        if len(value) <= self.max_bytes:
            return False
        if contains_redaction_marker(value):
            return False
        # Exact check — confirm the true byte size exceeds the threshold.
        return len(value.encode("utf-8", errors="replace")) > self.max_bytes

    def redact(self, value: str, path: str) -> str:
        raw_bytes = value.encode("utf-8", errors="replace")
        total_bytes = len(raw_bytes)
        sha256_hex = hashlib.sha256(raw_bytes).hexdigest()

        head = value[: self.head_chars]
        tail = value[-self.tail_chars:] if self.tail_chars > 0 else ""

        marker = _fmt_marker(
            redactor=self.name,
            reason=self.reason_code,
            original_bytes=total_bytes,
            original_sha256=sha256_hex,
            head_chars_preserved=len(head),
            tail_chars_preserved=len(tail),
            path=path,
            source="matrx_ai.providers.snapshot_redactors",
        )
        # Shape: verbatim head + newline + marker + newline + verbatim tail.
        # The newlines visually isolate the marker in a pretty-printed JSON
        # viewer; they do not add any semantics.
        return f"{head}\n{marker}\n{tail}"


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def apply_redactors(
    value: Any,
    redactors: list[Redactor],
    *,
    path: str = "$",
) -> Any:
    """Walk a JSON-safe tree and apply each redactor to every leaf.

    Structure preservation is enforced by the walker itself:
      - dict keys are copied verbatim in original order
      - list items are copied verbatim in original order
      - only *leaf* values are offered to redactors
      - redactors receive the full JSON-path of the value they're inspecting

    Redactors run in registration order. Each redactor sees the value after
    any earlier redactor has transformed it. In practice we design redactors
    to be independent, but the pipeline ordering is explicit and stable so
    future composition is predictable.

    Parameters
    ----------
    value : Any
        A JSON-safe Python value (dict / list / str / int / float / bool /
        None). Non-JSON-safe values should have already been coerced by
        ``_json_safe`` upstream; this function does not coerce types.
    redactors : list[Redactor]
        Explicitly ordered list of redactors to apply. An empty list is a
        no-op copy of the input.
    path : str
        JSON-path of ``value`` relative to the document root. Defaults to
        "$" for the root invocation. Redactors see this path in their marker
        output.

    Returns
    -------
    Any
        A new value tree with the same shape, keys, order, and types as the
        input, with leaf strings possibly replaced via the configured
        redactors. Dicts and lists are fresh instances; unchanged leaves are
        returned by identity.
    """
    if isinstance(value, dict):
        return {
            k: apply_redactors(v, redactors, path=f"{path}.{k}")
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [
            apply_redactors(item, redactors, path=f"{path}[{i}]")
            for i, item in enumerate(value)
        ]
    out = value
    for r in redactors:
        if r.applies_to(out):
            out = r.redact(out, path)
    return out


# ---------------------------------------------------------------------------
# Default pipeline
# ---------------------------------------------------------------------------
# The single source of truth for what the snapshot system is allowed to
# modify. Changing this list is a deliberate act — not a quiet one-liner
# tucked into an unrelated PR.

DEFAULT_SNAPSHOT_REDACTORS: list[Redactor] = [
    LargeBinaryStringRedactor(max_bytes=65536, head_chars=128, tail_chars=128),
]
