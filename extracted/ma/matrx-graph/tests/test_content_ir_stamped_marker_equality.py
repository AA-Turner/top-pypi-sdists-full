"""A stored schema's trigger-stamped ``__kind`` on a map is not drift.

The registry's write trigger guarantees ``__kind`` on every object in a stored
schema, including a ``dict[str, str]`` map. Comparing through that stamp made
every kind with a map field read as drifted forever, and ``publish_kind_catalog``'s
post-write verify fail on the very row it had just written (``topical_map_result``,
2026-09-22). A blank ``const: ""`` (``wf_122``'s old pin) is NOT storage noise:
rule 31 makes it a defect, so it reads as drift and the publisher writes it away.
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


def test_a_stored_blank_kind_stamp_is_drift_to_remove():
    """Rule 31: a blank ``const ""`` is a defect, never storage noise — the publisher
    must see it so the republish writes it away."""
    schema = Topic.model_json_schema()
    stamped = _stamped(schema)
    # A fresh dict: ``_stamped`` shares STAMP, and mutating it leaked into later tests.
    stamped["properties"]["facets"]["anyOf"][0]["properties"]["__kind"] = {
        "type": "string",
        "const": "",
        "description": "No registered kind: this position is plain structure. Always empty.",
    }

    assert not _structurally_equal(schema, stamped)


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


def test_removing_a_blank_stamp_from_a_nullable_closed_object_is_backward_compatible():
    """Rule 31 on ``type: ["object", "null"]``: dropping the blank ``const ""`` is the
    publisher's cleanup, not a break (variable_definition.control was refused, 2026-11-02),
    and drift detection still sees it so the cleanup is written."""
    from matrx_graph.content_ir.sdk import compatibility_verdict

    def root(sub: dict) -> dict:
        return {"type": "object", "properties": {"control": sub}, "required": []}

    model_sub = {
        "type": ["object", "null"],
        "additionalProperties": False,
        "properties": {"key": {"type": "string"}},
        "required": ["key"],
    }
    live_sub = {**model_sub, "properties": {**model_sub["properties"], "__kind": {"type": "string", "const": ""}}}
    verdict = compatibility_verdict(root(model_sub), root(live_sub))
    assert verdict.compatible, verdict
    assert not _structurally_equal(root(model_sub), root(live_sub))
