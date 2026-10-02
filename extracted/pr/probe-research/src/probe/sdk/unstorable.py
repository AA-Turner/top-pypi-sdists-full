"""Escape descriptive span text without rewriting research identities.

PostgreSQL cannot store U+0000 in text/jsonb. Only recognized text fields in
span attributes are reading aids that this safeguard may rewrite. Keys,
coordinates, identifiers, execution records and unknown schemas are refused
locally as permanent validation errors. The outbox retains refused operations.

A literal backslash-zero is a display escape, not a reversible encoding.
Per-span counts disclose the transformation; they cannot recover its positions.
Binary artifact uploads do not pass through this module.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from . import coerce as _coerce
from .errors import ValidationError

NUL = "\x00"
ESCAPE = "\\0"
RECORD_KEY = "probe.nul_escaped"
_MAX_DEPTH = 256
_SPAN_ROUTE = re.compile(r"/v1/runs/[^/?#]+/spans/?")
# These are descriptive fields used by captured spans, including ATIF's nested
# copies of tool output. A new field is rejected until its semantics are known.
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
    # No caller-provided paths or values: this exception can reach shared logs.
    return ValidationError(
        f"probe: cannot send this JSON payload: {reason}. "
        "Preserve binary content in an artifact; do not rewrite identifiers.",
        status=422,
    )


def has_nul(value: Any) -> bool:
    """Scan JSON containers, rejecting cycles before scrubbing or serialization.

    Cache completed containers so shared (non-cyclic) subtrees are legal and
    scanned once. Bound recursion and never stringify arbitrary keys for logs.
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
    """Return a non-mutating rewrite and counts keyed only by span position.

    Only POST span batches and the span portion of ingest-run batches qualify.
    Everything else is checked but never rewritten. Record collisions refuse the
    request rather than overwriting user data or concealing a transformation.
    """
    if not has_nul(body):
        return body, {}
    span_request = method.upper() == "POST" and (
        _SPAN_ROUTE.fullmatch(path) is not None or path in ("/ingest/v1/runs", "/ingest/v1/runs/")
    )
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
    """Materialize the scrubber's supported representations before validation.

    Convert an opaque value once so its original representation is checked
    before redaction can erase a forbidden identity. No credential inspection or
    display escaping occurs here.
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
        # Plan (c): a numpy scalar or 0-d tensor is a number, not its repr --
        # `np.float32(0.1)` used to reach the server as that string.
        number = _coerce.scalar(value)
        if number is not _coerce.NOT_AN_ARRAY:
            return normalize(number)
        return repr(value)

    return normalize(body)


def validate_nuls(body: Any, *, path: str, method: str = "POST") -> None:
    """Check policy before a scrubber can erase an invalid NUL identity.

    Discard the non-mutating candidate: display escaping must still happen only
    after scrubbing. This copy is paid only by NUL-bearing bodies.
    """
    escape_nuls(body, path=path, method=method)


def describe(counts: Mapping[str, int]) -> str:
    """Bounded warning; keys here are generated span positions, never user keys."""
    total = sum(counts.values())
    return (
        f"probe: escaped {total} NUL character(s) as literal \\0 in descriptive "
        f"attributes of {len(counts)} span(s). Counts are recorded under {RECORD_KEY}. "
        "This is a display escape, not a reversible encoding. "
        "Binary artifact bytes are unchanged by this safeguard."
    )


# -- metric points the server cannot store (review of #2053) --------------------
#
# A step outside a Postgres bigint is an asyncpg DataError, and a key past the
# btree index row size (~2,700 bytes with the rest of the row) is an index
# error: both are 500s, which the outbox retries for a day and which held the
# run's later writes behind them. They are dropped at the door instead, with
# one warning per kind per process. 2,048 bytes keeps every key the server
# stores in practice (random keys stored to ~2,500 bytes).

STEP_MIN, STEP_MAX = -(2**63), 2**63 - 1
MAX_METRIC_KEY_BYTES = 2048
_METRICS_ROUTE = re.compile(r"/v1/runs/[^/?#]+/metrics/?")


def step_out_of_range(step: Any) -> bool:
    return isinstance(step, int) and not isinstance(step, bool) and not (
        STEP_MIN <= step <= STEP_MAX
    )


def key_too_long(key: Any) -> bool:
    return isinstance(key, str) and len(key.encode("utf-8", "surrogatepass")) > MAX_METRIC_KEY_BYTES


def drop_unstorable_points(method: str, path: str, body: Any) -> tuple[Any, list[str]]:
    """``body`` without the metric points the server cannot store, and why
    each dropped point was dropped. Only a metrics POST is touched; anything
    else (and a body it cannot read) comes back unchanged."""
    if method.upper() != "POST" or not _METRICS_ROUTE.fullmatch(path.split("?", 1)[0]):
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
