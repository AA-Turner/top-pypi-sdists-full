"""A stored {"name","schema","strict"} envelope binds as structured output (ner.item_proposer v10)."""

from __future__ import annotations

import pytest

from matrx_ai.config.response_format import response_format_for_schema, unwrap_stored_envelope

BARE = {
    "type": "object",
    "required": ["proposed_items"],
    "properties": {"proposed_items": {"type": "array", "items": {"type": "string"}}},
    "additionalProperties": False,
}
ENVELOPE = {"name": "proposed_items_response", "schema": BARE, "strict": True, "description": "x"}


def test_envelope_unwraps_to_the_inner_schema_and_name() -> None:
    schema, name = unwrap_stored_envelope(ENVELOPE)
    assert schema is BARE
    assert name == "proposed_items_response"


def test_bare_schema_is_untouched() -> None:
    schema, name = unwrap_stored_envelope(BARE, "keep")
    assert schema is BARE and name == "keep"


def test_envelope_binds_like_the_bare_schema() -> None:
    bound = response_format_for_schema(ENVELOPE).model_dump(mode="json", by_alias=True, exclude_none=True)
    assert bound["json_schema"]["schema"]["type"] == "object"
    assert bound["json_schema"]["name"] == "proposed_items_response"


def test_a_real_non_object_root_is_still_refused() -> None:
    with pytest.raises(ValueError, match="Schema root must be an object"):
        response_format_for_schema({"type": "array", "items": {"type": "string"}})
