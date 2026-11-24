"""A generated answer example is valid against its own wire schema for the shapes a placeholder cannot satisfy.

2026-11-06: ``brand_element_options`` failed the every-kind example test because its ``element`` slug pattern
(``b7_positioning``) matches no placeholder; ``variable_component`` returned no example at all (its ``allOf``
if/then rules were read as the whole schema) and a control's unused settings must be null.
"""

from __future__ import annotations

import jsonschema

from matrx_ai.schema.example import answer_example, wire_schema


def test_a_field_names_its_own_sample_when_a_pattern_matches_no_placeholder() -> None:
    schema = {
        "type": "object",
        "properties": {"element": {"type": "string", "pattern": r"^[a-p][0-9]{1,2}_[a-z_]+$", "examples": ["b7_positioning"]}},
        "required": ["element"],
    }
    example = answer_example(schema)
    assert example == {"element": "b7_positioning"}
    jsonschema.validate(example, wire_schema(schema))


def test_an_object_with_if_then_rules_is_sampled_from_its_properties_and_obeys_the_rules() -> None:
    schema = {
        "type": "object",
        "properties": {"type": {"enum": ["select", "number"]}, "unit": {"type": ["string", "null"]}},
        "required": ["type", "unit"],
        "allOf": [
            {"if": {"properties": {"type": {"not": {"enum": ["number"]}}}}, "then": {"properties": {"unit": {"type": "null"}}}}
        ],
    }
    example = answer_example(schema)
    assert example == {"type": "select", "unit": None}
    jsonschema.validate(example, wire_schema(schema))
