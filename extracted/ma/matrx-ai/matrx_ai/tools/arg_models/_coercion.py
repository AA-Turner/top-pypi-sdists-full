"""Fuzzy JSON-string → container coercion for tool argument models.

Models — especially smaller ones — very often pass a structured argument as a
JSON *string* (e.g. data="{\"x\": 1}" or items="[1,2]") instead of a real
object/array. The wire type is a dict/list, so Pydantic would reject the string
with a cryptic "Input should be a valid dictionary/list", which the model can't
act on — it retries the same broken shape until the loop guard kills the run
(the 2026-05-25 SQL-tool incident).

A JSON-string object/array and the object/array itself resolve to exactly the
same thing, so we accept and decode the string form at the arg-model boundary
(`field_validator(mode="before")`). Anything that genuinely can't be the
expected container raises an ABUNDANTLY clear, instructive error — never the
default Pydantic message. This is the platform rule: be fuzzy where the value
resolves to the same thing, but keep the enforced contract real and the error
self-explanatory.

Use these in any tool arg model via a `field_validator(..., mode="before")`:

    from matrx_ai.tools.arg_models._coercion import coerce_object, coerce_rows, coerce_list

    class MyWire(ToolArgs):
        data: dict[str, Any]
        @field_validator("data", mode="before")
        @classmethod
        def _c(cls, v): return coerce_object(v, field="data", purpose="columns to set")
"""
from __future__ import annotations

import json
from typing import Any


def coerce_json_container(value: Any) -> Any:
    """Best-effort: if ``value`` is a JSON string encoding an object/array,
    decode it; otherwise return it unchanged. Never raises. Use for fields
    typed ``Any`` where a non-JSON value is also legitimate."""
    if isinstance(value, str):
        stripped = value.strip()
        if stripped[:1] in ("{", "["):
            try:
                return json.loads(stripped)
            except (ValueError, TypeError):
                return value
    return value


def coerce_object(value: Any, *, field: str, purpose: str = "key/value pairs") -> Any:
    """Coerce a value expected to be a JSON OBJECT (dict). Accepts a
    JSON-string object; passes ``None`` through (for Optional fields); raises a
    clear, instructive error for anything that isn't an object."""
    if value is None:
        return None
    coerced = coerce_json_container(value)
    if isinstance(coerced, dict):
        return coerced
    raise ValueError(
        f"`{field}` must be a JSON object of {purpose} "
        f'(for example {{"status": "active", "priority": 3}}). '
        f"You passed {type(value).__name__}. Pass the object directly as the "
        f"`{field}` argument — do NOT JSON-stringify it or wrap it in quotes."
    )


def coerce_rows(value: Any, *, field: str) -> Any:
    """Coerce a value expected to be an object OR a list of objects (e.g. rows
    to insert/upsert). Accepts a JSON-string form of either; passes ``None``
    through; raises a clear error otherwise."""
    if value is None:
        return None
    coerced = coerce_json_container(value)
    if isinstance(coerced, (dict, list)):
        return coerced
    raise ValueError(
        f"`{field}` must be a JSON object (one row) or a JSON array of objects "
        f'(many rows) — for example {{"name": "Foo"}} or [{{"name": "Foo"}}, '
        f'{{"name": "Bar"}}]. You passed {type(value).__name__}. Pass it directly '
        f"as the `{field}` argument — do NOT JSON-stringify it."
    )


def coerce_list(value: Any, *, field: str, purpose: str = "items") -> Any:
    """Coerce a value expected to be a JSON ARRAY (list). Accepts a JSON-string
    array; passes ``None`` through (for Optional fields); raises a clear error
    for anything that isn't a list."""
    if value is None:
        return None
    coerced = coerce_json_container(value)
    if isinstance(coerced, list):
        return coerced
    raise ValueError(
        f"`{field}` must be a JSON array of {purpose} "
        f'(for example ["a", "b"] or [{{"k": "v"}}]). You passed '
        f"{type(value).__name__}. Pass the array directly as the `{field}` "
        f"argument — do NOT JSON-stringify it or wrap it in quotes."
    )
