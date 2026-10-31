"""The one input declaration: the generated twin, the normalizations and the schema agree."""

from __future__ import annotations

from matrx_ai.agents.input_declaration import (
    INPUT_DECLARATION_KINDS,
    VariableComponent,
    VariableContextBinding,
    VariableDefinition,
    VariableRecordBinding,
    source_schema,
    upgrade_agent_variable,
    upgrade_workflow_input,
    variable_component_types,
)
from matrx_ai.agents.input_declaration.upgrade import SETTING_TYPES

MODELS = {
    "variable_definition": VariableDefinition,
    "variable_component": VariableComponent,
    "variable_context_binding": VariableContextBinding,
    "variable_record_binding": VariableRecordBinding,
}


def test_each_kind_publishes_its_source_file_byte_for_byte() -> None:
    for slug in INPUT_DECLARATION_KINDS:
        assert MODELS[slug].model_json_schema() == source_schema(slug)
        assert MODELS[slug].kind_slug == slug


def test_component_vocabulary_is_27_plus_text_plus_record() -> None:
    types = variable_component_types()
    assert len(types) == 29 and len(set(types)) == 29
    assert {"text", "record"} <= set(types)


def test_the_normalizer_and_the_schema_agree_on_which_types_take_each_setting() -> None:
    schema = source_schema("variable_component")
    declared: dict[str, frozenset[str]] = {}
    for block in schema["allOf"]:
        (setting,) = block["then"]["properties"].keys()
        excluded = block["if"]["properties"]["type"]["not"]["enum"]
        declared[setting] = frozenset(excluded)
    assert declared == SETTING_TYPES


def test_a_record_input_round_trips_through_the_generated_model() -> None:
    raw = {"name": "brand", "customComponent": {"type": "record", "tokens": ["web_brand"], "multiple": True}}
    dumped = VariableDefinition.model_validate(raw).model_dump(mode="json", exclude_none=True)
    assert dumped == {
        "__kind": "variable_definition",
        "name": "brand",
        "customComponent": {"__kind": "variable_component", "type": "record", "tokens": ["web_brand"], "multiple": True},
    }
    assert next(iter(dumped)) == "__kind"


def test_agent_door_named_normalizations() -> None:
    out = upgrade_agent_variable({
        "name": "tone", "default_value": "warm", "title": "Tone", "description": "How it sounds",
        "componentType": "textarea",
        "customComponent": {"type": "textarea", "options": ["a"], "picklist": {"listId": "L"}},
    })
    assert out["__kind"] == "variable_definition"
    assert out["defaultValue"] == "warm" and out["label"] == "Tone" and out["helpText"] == "How it sounds"
    cc = out["customComponent"]
    assert cc["__kind"] == "variable_component" and cc["pick_list"] == {"listId": "L"}
    assert "options" not in cc and cc["stash"] == {"options": ["a"]}


def test_workflow_door_maps_a_user_input_field_losslessly() -> None:
    out = upgrade_workflow_input({
        "key": "site", "label": "Site", "type": "text", "picks": "web_site", "multiple": False,
        "help": "Pick one", "placeholder": "example.com", "primary": True, "required_in_form": True,
        "sourcing": "ask", "kind": "", "default": "",
    })
    assert out["name"] == "site" and out["helpText"] == "Pick one" and out["sourcing"] == "ask"
    assert out["customComponent"]["type"] == "record" and out["customComponent"]["tokens"] == ["web_site"]
    assert out["defaultValue"] is None
    assert out["hints"] == {"primary": True, "placeholder": "example.com", "requiredInForm": True}
    choice = upgrade_workflow_input({"key": "c", "type": "choice", "options": ["a", "b"], "choice_style": "select",
                                     "option_labels": {"a": "Alpha"}})
    assert choice["customComponent"]["type"] == "select" and choice["customComponent"]["optionLabels"] == {"a": "Alpha"}
    spec = upgrade_workflow_input({"name": "cfg", "description": "d", "help": "h", "default": {"x": 1}})
    assert spec["valueKind"] == "json" and spec["helpText"] == "h" and spec["purpose"] == "d"
