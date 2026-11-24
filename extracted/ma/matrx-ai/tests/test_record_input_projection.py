"""A record input projected as an agent-tool parameter, and its value at the prompt door."""

from __future__ import annotations

from matrx_ai.agents.variable_schema import variable_definition_to_parameter
from matrx_ai.config.prompt_values import prompt_safe_value

NOTE_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"


def test_a_record_parameter_is_a_relation_object_limited_to_its_tokens() -> None:
    param = variable_definition_to_parameter(
        {"name": "brief", "customComponent": {"type": "record", "tokens": ["note"]}}
    )
    assert param["type"] == "object"
    assert param["required"] is False  # the variable's own required flag, never the relation's
    assert param["properties"]["token"]["enum"] == ["note"]


def test_a_multiple_record_parameter_is_a_list_of_relations() -> None:
    param = variable_definition_to_parameter(
        {"name": "refs", "customComponent": {"type": "record", "multiple": True}}
    )
    assert param["type"] == "array"
    assert param["items"]["required"] == ["_record_id"]


def test_text_is_a_plain_string_parameter() -> None:
    assert variable_definition_to_parameter({"name": "t", "customComponent": {"type": "text"}})["type"] == "string"


def test_the_prompt_reads_a_relation_as_label_and_pointer() -> None:
    one = {"__kind": "relation", "_record_id": NOTE_ID, "token": "note", "label": "Launch plan"}
    assert prompt_safe_value(one) == f"Launch plan (note {NOTE_ID})"
    assert prompt_safe_value([one, {"_record_id": NOTE_ID}]) == f"Launch plan (note {NOTE_ID})\nrecord {NOTE_ID}"


def test_a_dict_that_only_carries_a_record_id_keeps_its_fields() -> None:
    assert prompt_safe_value({"_record_id": NOTE_ID, "name": "Pat"}) == f'{{"_record_id": "{NOTE_ID}", "name": "Pat"}}'


def test_a_label_with_a_line_break_stays_on_one_line() -> None:
    assert prompt_safe_value({"_record_id": NOTE_ID, "token": "note", "label": "Q3\nplan"}) == f"Q3 plan (note {NOTE_ID})"


def test_a_legacy_stored_element_projects_through_the_door() -> None:
    param = variable_definition_to_parameter(
        {"name": "tone", "componentType": "radio", "description": "How it sounds", "default_value": "warm"}
    )
    assert param["description"] == "How it sounds"
    assert param["default"] == "warm"
