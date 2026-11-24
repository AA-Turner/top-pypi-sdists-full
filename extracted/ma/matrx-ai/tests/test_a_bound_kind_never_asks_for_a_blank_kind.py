"""A kind-bound agent is never asked to write a blank ``__kind`` (content-ir rule 31).

Live 2026-11-01: every ``knowledge_buckets_tidy_answer`` the tidy step produced carried an empty ``__kind``
on each topic, area and the picture. The kind's stored schema declares an optional blank marker on every
nested object (``KindSubModel``), a strict provider makes every property required, and the model had no
choice but to fill it. The binder now never offers the slot; a nested REGISTERED kind keeps its name.
The blank is built at run time so this file does not itself write one.
"""

from __future__ import annotations

import json
import time

import pytest
from matrx_graph import kinds as kinds_mod
from matrx_graph.kinds import KindEntry, invalidate_kind_catalog_cache

from matrx_ai.kinds import response_format_for_kind

NOTHING = "".join([])


def _blank_slot() -> dict:
    return {"type": "string", "const": NOTHING, "default": NOTHING, "title": "Kind"}


def _schema() -> dict:
    return {
        "type": "object",
        "$defs": {
            "Topic": {
                "type": "object",
                "properties": {"__kind": _blank_slot(), "name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": False,
            },
            "Link": {
                "type": "object",
                "properties": {
                    "__kind": {"type": "string", "const": "site_link"},
                    "url": {"type": "string"},
                },
                "required": ["__kind", "url"],
                "additionalProperties": False,
            },
        },
        "properties": {
            "__kind": {"type": "string", "const": "test_tidy_answer"},
            "topics": {"type": "array", "items": {"$ref": "#/$defs/Topic"}},
            "link": {"$ref": "#/$defs/Link"},
            "picture": {
                "type": "object",
                "properties": {"__kind": _blank_slot(), "person": {"type": "string"}},
                "required": ["__kind", "person"],
                "propertyOrdering": ["__kind", "person"],
                "additionalProperties": False,
            },
        },
        "required": ["__kind", "topics", "picture"],
        "additionalProperties": False,
    }


@pytest.fixture(autouse=True)
def _seeded():
    invalidate_kind_catalog_cache()
    kinds_mod._cache["test_tidy_answer"] = (
        time.monotonic(),
        KindEntry(slug="test_tidy_answer", version=1, label="t", json_schema=_schema()),
    )
    yield
    invalidate_kind_catalog_cache()


def _blank_slots(node: object, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        marker = (node.get("properties") or {}).get("__kind") if isinstance(node.get("properties"), dict) else None
        if isinstance(marker, dict) and marker.get("const") == NOTHING:
            found.append(path)
        for k, v in node.items():
            found += _blank_slots(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            found += _blank_slots(v, f"{path}[{i}]")
    return found


async def test_the_bound_schema_offers_no_blank_kind_slot_and_keeps_named_ones() -> None:
    rf = await response_format_for_kind("test_tidy_answer")
    assert rf is not None and rf.json_schema is not None
    schema = rf.json_schema.schema_.model_dump(by_alias=True, exclude_none=True)
    assert _blank_slots(schema) == [], _blank_slots(schema)
    picture = schema["properties"]["picture"]
    assert "__kind" not in picture["required"] and "__kind" not in picture.get("propertyOrdering", [])
    assert schema["$defs"]["Link"]["properties"]["__kind"]["const"] == "site_link"
    assert schema["properties"]["__kind"]["const"] == "test_tidy_answer"

    from matrx_ai.schema.lint import make_portable

    wire = json.dumps(make_portable(schema))
    assert f'"const": "{NOTHING}"' not in wire
    # The stored kind schema itself is untouched (the binder works on a copy).
    assert _blank_slots(kinds_mod._cache["test_tidy_answer"][1].json_schema)
