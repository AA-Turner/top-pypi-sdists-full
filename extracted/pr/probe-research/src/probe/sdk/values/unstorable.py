"""Escape NULs in descriptive span text without rewriting research identities.

PostgreSQL cannot store U+0000 in text/jsonb. Only known text fields of span
attributes are rewritten; keys, coordinates, identifiers, execution records and
unknown schemas are refused locally (permanent validation error; the outbox
keeps refused operations).

Literal backslash-zero is a display escape, not reversible; per-span counts
disclose it but not the positions. Binary artifact uploads bypass this module.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from . import values as _coerce
from ..errors import ValidationError
from ..routes import is_metrics_post, is_span_batch

NUL = "\x00"
ESCAPE = "\\0"
RECORD_KEY = "probe.nul_escaped"
_MAX_DEPTH = 256
# Descriptive span fields (incl. ATIF's nested tool-output copies). New fields are refused until understood.
_TEXT_FIELDS = frozenset(
    {
        "result",
        "message",
        "reasoning",
        "observation",
        "arguments",
        "extra",
        "result_extra",
        "observation_extra",
        "tool_result_metadata",
        "raw_tool_result",
        "text",
        "content",
        "stdout",
        "stderr",
        "prompt",
        "input",
        "output",
        "error",
    }
)
_IDENTITY_KEYS = frozenset(
    {
        "id",
        "key",
        "name",
        "hash",
        "ref",
        "dimensions",
        "coords",
        "labels",
        "where",
        "foreign_keys",
        "spec",
        "execution_record",
        "execution_records",
        "model",
        "model_name",
        "provider",
        "function_name",
        RECORD_KEY,
    }
)


def _refuse(reason: str) -> ValidationError:
    # No caller paths or values: this can reach shared logs.
    return ValidationError(
        f"probe: cannot send this JSON payload: {reason}. "
        "Preserve binary content in an artifact; do not rewrite identifiers.",
        status=422,
    )


def has_nul(value: Any) -> bool:
    """Whether any string holds a NUL; raises on cycles or nesting past 256.

    Shared (non-cyclic) subtrees are legal and scanned once; keys are never stringified for logs.
    """
    active: set[int] = set()
    complete: dict[int, tuple[bool, int]] = {}

    def visit(item: Any, depth: int) -> tuple[bool, int]:
        if depth > _MAX_DEPTH:
            raise _refuse("JSON nesting exceeds the client limit of 256")
        if isinstance(item, str):
            return NUL in item, 0
        if not isinstance(item, (dict, list, tuple, set)):
            return False, 0
        ident = id(item)
        if ident in active:
            raise _refuse("cyclic JSON container")
        if ident in complete:
            found, height = complete[ident]
            if depth + height > _MAX_DEPTH:
                raise _refuse("JSON nesting exceeds the client limit of 256")
            return found, height
        active.add(ident)
        found, height = False, 0
        children = (
            (part for pair in item.items() for part in pair)
            if isinstance(item, dict)
            else iter(item)
        )
        for child in children:
            child_found, child_height = visit(child, depth + 1)
            found = found or child_found
            height = max(height, 1 + child_height)
        active.remove(ident)
        complete[ident] = found, height
        return found, height

    return visit(value, 0)[0]


def _identity(key: Any) -> bool:
    return isinstance(key, str) and (
        key in _IDENTITY_KEYS or key.endswith(("_id", "_key", "_hash", "_ref"))
    )


def escape_nuls(body: Any, *, path: str, method: str = "POST") -> tuple[Any, dict[str, int]]:
    """Non-mutating rewrite plus counts keyed by span position.

    Only POST span batches and the span part of ingest-run batches are rewritten;
    others are checked only. A record collision refuses the request.
    """
    if not has_nul(body):
        return body, {}
    span_request = is_span_batch(method, path)
    counts: dict[str, int] = {}

    def walk(item: Any, location: tuple = (), allowed: bool = False, depth: int = 0):
        if depth > _MAX_DEPTH:
            raise _refuse("JSON nesting exceeds the client limit of 256")
        if isinstance(item, str):
            count = item.count(NUL)
            if count and not allowed:
                raise _refuse("NUL in a key, identity, or unsupported text field")
            return (item.replace(NUL, ESCAPE), count) if count else (item, 0)
        if isinstance(item, dict):
            attributes = (
                span_request
                and len(location) == 3
                and location[0] == "spans"
                and isinstance(location[1], int)
                and location[2] == "attributes"
            )
            out = {}
            total = 0
            for key, child in item.items():
                if isinstance(key, str) and NUL in key:
                    raise _refuse("NUL in a JSON key")
                child_allowed = (key in _TEXT_FIELDS if attributes else allowed) and not _identity(
                    key
                )
                out[key], count = walk(child, (*location, key), child_allowed, depth + 1)
                total += count
            if attributes and total:
                if RECORD_KEY in item:
                    raise _refuse("span escape record already exists alongside new NUL text")
                out[RECORD_KEY] = {"count": total, "encoding": "literal-backslash-zero"}
                counts[f"spans[{location[1]}].attributes"] = total
            return out, total
        if isinstance(item, (list, tuple, set)):
            out = []
            total = 0
            for index, child in enumerate(item):
                value, count = walk(child, (*location, index), allowed, depth + 1)
                out.append(value)
                total += count
            return out, total
        return item, 0

    rewritten, _ = walk(body)
    return rewritten, counts


def normalize_json(body: Any) -> Any:
    """Convert opaque values once, before validation, so redaction cannot erase a
    forbidden identity. No credential inspection or escaping here.
    """
    has_nul(body)

    def normalize(value):
        if value is None or isinstance(value, (str, bool, int, float)):
            return value
        if isinstance(value, dict):
            result = {}
            for key, child in value.items():
                key = str(key)
                if key in result:
                    raise _refuse("JSON key representations collide")
                result[key] = normalize(child)
            return result
        if isinstance(value, (list, tuple, set)):
            return [normalize(child) for child in value]
        # Plan (c): a numpy scalar / 0-d tensor is a number, not its repr.
        number = _coerce.scalar(value)
        if number is not _coerce.NOT_AN_ARRAY:
            return normalize(number)
        return repr(value)

    return normalize(body)


def validate_nuls(body: Any, *, path: str, method: str = "POST") -> None:
    """Check NUL policy before the scrubber can erase an invalid NUL identity.

    The rewrite is discarded: escaping must happen after scrubbing. Only NUL-bearing bodies pay the copy.
    """
    escape_nuls(body, path=path, method=method)


def describe(counts: Mapping[str, int]) -> str:
    """Bounded warning text; keys are span positions, never user keys."""
    total = sum(counts.values())
    return (
        f"probe: escaped {total} NUL character(s) as literal \\0 in descriptive "
        f"attributes of {len(counts)} span(s). Counts are recorded under {RECORD_KEY}. "
        "This is a display escape, not a reversible encoding. "
        "Binary artifact bytes are unchanged by this safeguard."
    )


# -- metric points the server cannot store (review of #2053) --------------------
#
# A step outside bigint, or a key past the btree row size (~2,700 B), is a 500
# the outbox retries for a day while blocking the run's later writes. Dropped
# at the door instead, one warning per kind per process. 2,048 B keeps every
# key stored in practice (random keys stored to ~2,500 B).

STEP_MIN, STEP_MAX = -(2**63), 2**63 - 1
MAX_METRIC_KEY_BYTES = 2048


def step_out_of_range(step: Any) -> bool:
    return isinstance(step, int) and not isinstance(step, bool) and not (
        STEP_MIN <= step <= STEP_MAX
    )


def key_too_long(key: Any) -> bool:
    return isinstance(key, str) and len(key.encode("utf-8", "surrogatepass")) > MAX_METRIC_KEY_BYTES


def drop_unstorable_points(method: str, path: str, body: Any) -> tuple[Any, list[str]]:
    """``body`` minus metric points the server cannot store, plus a reason per drop
    ("step" or "key"). Only a metrics POST is touched; else unchanged."""
    if not is_metrics_post(method, path):
        return body, []
    points = body.get("points") if isinstance(body, dict) else None
    if not isinstance(points, list):
        return body, []
    kept: list = []
    reasons: list[str] = []
    for point in points:
        if isinstance(point, dict) and step_out_of_range(point.get("step_index")):
            reasons.append("step")
        elif isinstance(point, dict) and key_too_long(point.get("key")):
            reasons.append("key")
        else:
            kept.append(point)
    if not reasons:
        return body, []
    return {**body, "points": kept}, reasons
