"""The ceiling on a span's encoded payload, and the trimming that enforces it.

A span's whole payload (input, output, contexts, prompt, metadata) ships as a
single ``bitfab.payload`` string attribute, and the exporter drops any carrier
that exceeds the per-request byte ceiling outright rather than trimming it.
Capping each value on its own cannot prevent that: two values that each fit can
still add up to an undeliverable span. So the budget is enforced on the encoded
payload as a whole, and an oversized span ships with its largest fields stubbed
instead of vanishing.

The budget is measured on the *carrier* (the payload re-escaped into the OTLP
attribute), not on the payload body, because the carrier is what the exporter
weighs. Bounding the body instead leaves escape-heavy content to blow the
request ceiling anyway: a body of escaped JSON, Windows paths, or regexes is
nearly all backslashes, and every one of them doubles. Measured on a body sized
exactly to a 2.4 MB cap, prose produced a 2.4 MB carrier but backslash-dense
content produced 4.8 MB, which the exporter dropped.

The normal 2.8 MB fallback leaves room beneath the 3 MB wire target. Trace
transport may first preserve a carrier up to 7.8 MB when its single-span
request compresses below that wire target and remains below ingress's 8 MB
decompressed ceiling.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

MAX_SPAN_CARRIER_BYTES = 2_800_000
MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES = 7_800_000

# Span fields that identify the span rather than carry user data. Trimming one
# would leave a span that no longer says what it is, so they stay whatever the
# payload costs.
_STRUCTURAL_SPAN_KEYS = frozenset(
    {"name", "type", "function_name", "error_source", "variant"}
)


def byte_length(value: str) -> int:
    return len(value.encode("utf-8"))


def carrier_byte_length(body: str) -> int:
    """The byte length ``body`` occupies once re-escaped as a JSON string value.

    ``body`` is itself JSON text from :func:`encode_json`, which leaves it pure
    ASCII (``json.dumps`` defaults to ``ensure_ascii``), so every character is
    one byte and only ``"`` and ``\\`` grow, by one byte each.

    Counts over the encoded bytes rather than the string: ``bytes.count`` is 3-5x
    faster than ``str.count`` here, and the encode it needs is close to free
    because CPython keeps the UTF-8 form of an ASCII string on the object.

    A non-ASCII body cannot come from this SDK's encoder, but is still measured
    correctly rather than under-counted: ``ensure_ascii`` would expand each such
    character to a ``\\uXXXX`` escape, so that case defers to a real encode.
    """
    if not body.isascii():
        return len(json.dumps(body).encode("utf-8"))
    encoded = body.encode("utf-8")
    return len(encoded) + encoded.count(b'"') + encoded.count(b"\\") + 2


# The most carrier bytes one character of an ASCII JSON body can become: `"` and
# `\` are the only characters that grow, from one byte to two. The invariant
# that bodies are ASCII is pinned by a test, and `fits_carrier_budget` checks it
# rather than assuming it.
_MAX_BYTES_PER_ASCII_CHAR = 2


def fits_carrier_budget(body: str, max_bytes: int = MAX_SPAN_CARRIER_BYTES) -> bool:
    """Whether ``body`` fits the carrier budget, escalating only as far as it must.

    ``len(body)`` is O(1) and brackets the answer for both ordinary spans (far
    under the budget) and hopeless ones (already past it on raw length alone),
    which is every span in normal traffic: neither case encodes the string. Only
    a body near the budget is measured exactly.
    """
    chars = len(body)
    # `str.isascii()` reads a flag CPython already keeps on the object, so this
    # stays O(1) rather than scanning.
    if body.isascii() and chars * _MAX_BYTES_PER_ASCII_CHAR + 2 <= max_bytes:
        return True
    if chars + 2 > max_bytes:
        return False
    return carrier_byte_length(body) <= max_bytes


def _clone_trimmable(
    payload: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Copy the records holding user data so trimming never mutates the caller's."""
    copy = dict(payload)
    containers: list[dict[str, Any]] = []

    span_data = copy.get("span_data")
    if isinstance(span_data, dict):
        clone = dict(span_data)
        copy["span_data"] = clone
        containers.append(clone)

    raw_span = copy.get("rawSpan")
    if isinstance(raw_span, dict) and isinstance(raw_span.get("span_data"), dict):
        clone = dict(raw_span["span_data"])
        raw_span_copy = dict(raw_span)
        raw_span_copy["span_data"] = clone
        copy["rawSpan"] = raw_span_copy
        containers.append(clone)

    # No span_data anywhere: a trace-level or otherwise unfamiliar payload. Trim
    # its own fields rather than give up, so an oversized body still ships.
    if not containers:
        containers.append(copy)

    return copy, containers


def _collect_candidates(
    containers: list[dict[str, Any]],
    encode: Callable[[Any], str],
) -> list[tuple[dict[str, Any], str, int]]:
    candidates: list[tuple[dict[str, Any], str, int]] = []
    for container in containers:
        for key, value in container.items():
            if key in _STRUCTURAL_SPAN_KEYS or value is None:
                continue
            try:
                size = byte_length(encode(value))
            except Exception:
                continue
            candidates.append((container, key, size))
    candidates.sort(key=lambda entry: entry[2], reverse=True)
    return candidates


def trim_payload_to_budget(
    payload: dict[str, Any],
    encode: Callable[[Any], str],
    max_bytes: int = MAX_SPAN_CARRIER_BYTES,
) -> tuple[dict[str, Any], list[str]] | None:
    """Stub the largest payload fields until the encoded body fits the budget.

    Returns ``(trimmed_payload, trimmed_keys)``, or ``None`` when nothing could
    be trimmed (the caller then ships the oversized body and lets the exporter
    report the drop, which is still better than silently emptying a span).
    """
    copy, containers = _clone_trimmable(payload)
    candidates = _collect_candidates(containers, encode)
    if not candidates:
        return None

    trimmed: list[str] = []
    for container, key, size in candidates:
        container[key] = f"<unserializable: too_large_{size}_bytes>"
        trimmed.append(key)
        try:
            body = encode(copy)
        except Exception:
            return None
        if fits_carrier_budget(body, max_bytes):
            return copy, trimmed
    return None


def enforce_payload_budget(
    payload: Any,
    body: str,
    encode: Callable[[Any], str],
    max_bytes: int = MAX_SPAN_CARRIER_BYTES,
) -> tuple[Any, str, list[str]]:
    """Return a payload and body within budget, plus the fields that were stubbed.

    The payload comes back alongside the body because the transport reads it for
    span naming and timestamps: handing back the untrimmed one would describe a
    span by content the body no longer carries.
    """
    if not isinstance(payload, dict) or fits_carrier_budget(body, max_bytes):
        return payload, body, []
    result = trim_payload_to_budget(payload, encode, max_bytes)
    if result is None:
        return payload, body, []
    trimmed_payload, trimmed = result
    _mark_payload_trimmed(trimmed_payload, trimmed, max_bytes)
    try:
        return trimmed_payload, encode(trimmed_payload), trimmed
    except Exception:
        return payload, body, []


def _mark_payload_trimmed(
    payload: dict[str, Any], trimmed: list[str], max_bytes: int
) -> None:
    """Record the trim in the payload's own ``errors``, which the server reads to
    flag a trace as incomplete."""
    existing = payload.get("errors")
    errors = list(existing) if isinstance(existing, list) else []
    errors.append(
        {
            "source": "sdk",
            "step": "payload_budget",
            "error": (
                "trimmed oversized field(s) to fit the "
                f"{max_bytes}-byte span carrier budget: "
                f"{', '.join(dict.fromkeys(trimmed))}"
            ),
        }
    )
    payload["errors"] = errors
