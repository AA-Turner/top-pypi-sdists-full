"""Deterministic one-line structure sketch for offloaded tool results.

A head truncation of a large JSON payload tells the model nothing about the
payload's shape, so "retrieve everything" is the only safe move it can make.
The sketch answers the shape question inline: how many records, which keys,
which types - computed synchronously from stdlib json, with no values in the
output so nothing leaks past result redaction.
"""

from __future__ import annotations

import json
from collections import Counter
from typing import Any, Dict, List, Optional

# Above this, inspecting the payload costs more than the sketch can save.
_MAX_PARSE_CHARS = 2_000_000
# Items inspected per array, plus its last one so a tail difference shows up.
_SAMPLE_ITEMS = 25
_MAX_DEPTH = 3
_MAX_KEYS_PER_LEVEL = 12
# Shorter strings are not worth a nested parse attempt.
_NESTED_JSON_STR_MIN = 200
_DEFAULT_MAX_CHARS = 600


def sketch_structure(
    content: str, *, max_chars: int = _DEFAULT_MAX_CHARS
) -> Optional[str]:
    """Describe the shape of a JSON payload in one line, or None when not JSON."""
    if not isinstance(content, str) or len(content) > _MAX_PARSE_CHARS:
        return None
    parsed = _parse(content)
    if isinstance(parsed, list):
        return _clip(f"JSON {_describe_list(parsed, 0)}", max_chars)
    if isinstance(parsed, dict):
        return _clip(f"JSON object {_describe_dict(parsed, 0)}", max_chars)
    return None


def _parse(text: str) -> Any:
    stripped = text.lstrip()
    if not stripped or stripped[0] not in "{[":
        return None
    try:
        return json.loads(stripped)
    except Exception:  # best-effort: a sketch must never break the preview
        return None


def _type_name(value: Any) -> str:
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
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "value"


def _describe(value: Any, depth: int) -> str:
    if isinstance(value, dict):
        return _describe_dict(value, depth)
    if isinstance(value, list):
        return _describe_list(value, depth)
    if isinstance(value, str):
        nested = _nested_json(value)
        if nested is not None and depth < _MAX_DEPTH:
            return f"str holding {_describe(nested, depth + 1)}"
        return "str"
    return _type_name(value)


def _describe_dict(value: Dict[str, Any], depth: int) -> str:
    if not value:
        return "{}"
    if depth >= _MAX_DEPTH:
        return "{...}"
    keys = list(value)
    # A wide dict of same-shaped values is a map keyed by ids, not a record.
    if len(keys) > _MAX_KEYS_PER_LEVEL:
        shapes = {_describe(value[key], depth + 1) for key in keys[:_SAMPLE_ITEMS]}
        if len(shapes) == 1:
            return f"map of {len(keys):,} entries, each {shapes.pop()}"
    parts = [
        f"{key}: {_describe(value[key], depth + 1)}"
        for key in keys[:_MAX_KEYS_PER_LEVEL]
    ]
    remaining = len(keys) - _MAX_KEYS_PER_LEVEL
    if remaining > 0:
        parts.append(f"+{remaining} more keys")
    return "{" + ", ".join(parts) + "}"


def _describe_list(value: List[Any], depth: int) -> str:
    count = len(value)
    if count == 0:
        return "empty array"
    sample = value[:_SAMPLE_ITEMS]
    if count > len(sample):
        sample = sample + [value[-1]]
    kinds = {_type_name(item) for item in sample}
    if len(kinds) > 1:
        return f"array of {count:,} items (mixed: {_histogram(sample, count)})"
    kind = kinds.pop()
    if kind == "object":
        return f"array of {count:,} objects {_merged_object_shape(sample, depth + 1)}"
    if kind == "array":
        if depth >= _MAX_DEPTH:
            return f"array of {count:,} arrays"
        return f"array of {count:,} arrays, each {_describe_list(sample[0], depth + 1)}"
    return f"array of {count:,} {kind}"


def _histogram(sample: List[Any], total: int) -> str:
    counts = Counter(_type_name(item) for item in sample)
    breakdown = ", ".join(f"{n} {kind}" for kind, n in sorted(counts.items()))
    if len(sample) >= total:
        return breakdown
    return f"{breakdown} in {len(sample)} sampled"


def _merged_object_shape(items: List[Dict[str, Any]], depth: int) -> str:
    """Key map merged across sampled objects; a key missing from some is marked ``?``."""
    if depth >= _MAX_DEPTH:
        return "{...}"
    order: List[str] = []
    types: Dict[str, str] = {}
    present: Counter = Counter()
    for item in items:
        for key, val in item.items():
            if key not in types:
                order.append(key)
                types[key] = _describe(val, depth + 1)
            elif types[key] == "null":
                types[key] = _describe(val, depth + 1)
            present[key] += 1
    parts = []
    for key in order[:_MAX_KEYS_PER_LEVEL]:
        optional = "" if present[key] == len(items) else "?"
        parts.append(f"{key}{optional}: {types[key]}")
    remaining = len(order) - _MAX_KEYS_PER_LEVEL
    if remaining > 0:
        parts.append(f"+{remaining} more keys")
    return "{" + ", ".join(parts) + "}"


def _nested_json(value: str) -> Any:
    if len(value) < _NESTED_JSON_STR_MIN or len(value) > _MAX_PARSE_CHARS:
        return None
    return _parse(value)


def _clip(text: str, max_chars: int) -> Optional[str]:
    single_line = " ".join(text.split())
    if max_chars <= 3:
        return None
    if len(single_line) <= max_chars:
        return single_line
    return single_line[: max_chars - 3].rstrip() + "..."
