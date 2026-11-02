"""A stored schema's trigger-stamped ``__kind`` on a map is not drift.

The registry's write trigger guarantees ``__kind`` on every object in a stored
schema, including a ``dict[str, str]`` map. Comparing through that stamp made
every kind with a map field read as drifted forever, and ``publish_kind_catalog``'s
post-write verify fail on the very row it had just written (``topical_map_result``,
2026-09-22). ``wf_122`` later pinned unidentified positions to ``const: ""``;
that storage-only stamp must be stripped too. Everything else still counts.
"""

from __future__ import annotations

from pydantic import BaseModel

from matrx_graph.content_ir.markers import strip_optional_schema_kind_stamps
from matrx_graph.content_ir.sdk import _structurally_equal

STAMP = {
    "type": "string",
    "description": "The registered kind this payload is an instance of, when it is one.",
}


class Topic(BaseModel):
    slug: str
    facets: dict[str, str] | None = None


def _stamped(schema: dict) -> dict:
    facets = schema["properties"]["facets"]["anyOf"][0]
    return {
        **schema,
        "properties": {
            **schema["properties"],
            "facets": {
                **schema["properties"]["facets"],
                "anyOf": [{**facets, "properties": {"__kind": STAMP}}, {"type": "null"}],
            },
        },
    }


def test_the_trigger_stamp_on_a_map_is_not_drift():
    schema = Topic.model_json_schema()
    assert _structurally_equal(schema, _stamped(schema))


def test_the_current_nonidentity_trigger_stamp_on_an_open_object_is_not_drift():
    schema = Topic.model_json_schema()
    stamped = _stamped(schema)
    marker = stamped["properties"]["facets"]["anyOf"][0]["properties"]["__kind"]
    marker["const"] = ""
    marker["description"] = "No registered kind: this position is plain structure. Always empty."

    assert _structurally_equal(schema, stamped)


def test_the_trigger_stamp_on_a_closed_object_is_not_drift():
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
    }
    stamped = {
        **schema,
        "properties": {**schema["properties"], "__kind": STAMP},
    }
    assert _structurally_equal(schema, stamped)


def test_schema_stamp_comparison_reduces_a_copy_not_the_registered_schema():
    stamped = {"type": "object", "properties": {"__kind": {"type": "string"}}}

    normalized = strip_optional_schema_kind_stamps(stamped)

    assert normalized == {"type": "object"}
    assert stamped["properties"]["__kind"] == {"type": "string"}


def test_a_real_property_beside_the_stamp_is_still_drift():
    schema = Topic.model_json_schema()
    stamped = _stamped(schema)
    stamped["properties"]["facets"]["anyOf"][0]["properties"]["region"] = {"type": "string"}
    assert not _structurally_equal(schema, stamped)


def test_a_required_marker_is_a_real_constraint_not_a_stamp():
    schema = Topic.model_json_schema()
    stamped = _stamped(schema)
    stamped["properties"]["facets"]["anyOf"][0]["required"] = ["__kind"]
    assert not _structurally_equal(schema, stamped)


def test_a_changed_map_value_type_is_still_drift():
    schema = Topic.model_json_schema()
    stamped = _stamped(schema)
    stamped["properties"]["facets"]["anyOf"][0]["additionalProperties"] = {"type": "integer"}
    assert not _structurally_equal(schema, stamped)
