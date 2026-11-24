"""The one input declaration: the generated twin, the normalizations and the schema agree."""

from __future__ import annotations

from matrx_graph.input_declaration import (
    INPUT_DECLARATION_KINDS,
    VariableComponent,
    VariableContextBinding,
    VariableDefinition,
    VariableActionBinding,
    VariableRecordBinding,
    source_schema,
    upgrade_agent_variable,
    upgrade_workflow_input,
    variable_component_types,
)
from matrx_graph.input_declaration.upgrade import SETTING_TYPES

MODELS = {
    "variable_definition": VariableDefinition,
    "variable_component": VariableComponent,
    "variable_context_binding": VariableContextBinding,
    "variable_record_binding": VariableRecordBinding,
    "variable_action_binding": VariableActionBinding,
}


def test_each_kind_publishes_its_source_file_byte_for_byte() -> None:
    for slug in INPUT_DECLARATION_KINDS:
        assert MODELS[slug].model_json_schema() == source_schema(slug)
        assert MODELS[slug].kind_slug == slug


def test_component_vocabulary_is_27_plus_text_record_and_rows() -> None:
    types = variable_component_types()
    assert len(types) == 30 and len(set(types)) == 30
    assert {"text", "record", "rows"} <= set(types)


def test_a_rows_component_keeps_its_fields_and_parks_them_off_type() -> None:
    from matrx_graph.input_declaration.generated import VariableComponent

    fields = [{"name": "name", "type": "text"}, {"name": "voice", "type": "select", "options": ["Kore", "Puck"]}]
    cc = VariableComponent.model_validate(
        {"__kind": "variable_component", "type": "rows", "fields": fields, "minRows": 1, "maxRows": 2}
    )
    assert cc.maxRows == 2 and cc.fields is not None and cc.fields[1].options == ["Kore", "Puck"]
    parked = upgrade_agent_variable({"name": "cast", "customComponent": {"type": "text", "fields": fields}})
    assert "fields" not in parked["customComponent"] and parked["customComponent"]["stash"]["fields"] == fields


def test_the_normalizer_and_the_schema_agree_on_which_types_take_each_setting() -> None:
    schema = source_schema("variable_component")
    declared: dict[str, frozenset[str]] = {}
    for block in schema["allOf"]:
        (setting,) = block["then"]["properties"].keys()
        excluded = block["if"]["properties"]["type"]["not"]["enum"]
        declared[setting] = frozenset(excluded)
    assert declared == SETTING_TYPES


def test_a_record_input_round_trips_through_the_generated_model() -> None:
    raw = {"name": "brand", "customComponent": {"type": "record", "tokens": ["brand"], "multiple": True}}
    dumped = VariableDefinition.model_validate(raw).model_dump(mode="json", exclude_none=True)
    assert dumped == {
        "__kind": "variable_definition",
        "name": "brand",
        "customComponent": {"__kind": "variable_component", "type": "record", "tokens": ["brand"], "multiple": True},
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


# ── upgrade_workflow_input: idempotent, list picks, picks_type_into (lane H repro, 2026-10-30) ────

_WORKFLOW_SAMPLES: list[dict] = [
    {"key": "tone", "label": "Tone", "type": "choice", "options": ["warm", "plain"], "default": "warm",
     "help": "How it sounds", "placeholder": "Pick one"},
    {"key": "brief", "type": "long_text", "required": True, "default": "", "description": "What to write"},
    {"name": "count", "default": 3, "description": "How many"},
    {"name": "flags", "default": {"a": 1}},
    {"key": "target", "type": "text", "picks": ["organization", "project"], "picks_type_into": "target_type",
     "default": ""},
    {"key": "files", "type": "file", "multiple": True, "accept": "image/*", "group": "Inputs", "order": 2},
    {"name": "who", "picks": "user", "multiple": True},
    {"key": "pick", "type": "choice", "options": list("abcdefgh"), "choice_style": "chips",
     "option_labels": {"a": "A"}, "binding": {"kind": "merge_field", "field": "x"}},
]


def test_workflow_door_is_idempotent() -> None:
    for raw in _WORKFLOW_SAMPLES:
        once = upgrade_workflow_input(raw)
        assert upgrade_workflow_input(once) == once, raw
        assert upgrade_agent_variable(once) == once, raw


def test_an_already_declared_input_keeps_its_default_help_and_options() -> None:
    declared = {
        "__kind": "variable_definition", "name": "tone", "defaultValue": "warm", "helpText": "How it sounds",
        "customComponent": {"__kind": "variable_component", "type": "pill-toggle", "options": ["warm", "plain"]},
    }
    assert upgrade_workflow_input(declared) == declared


def test_a_list_of_picks_flattens_into_tokens() -> None:
    out = upgrade_workflow_input({"key": "target", "picks": ["organization", "project"]})
    assert out["customComponent"]["tokens"] == ["organization", "project"]
    assert upgrade_workflow_input({"key": "who", "picks": "user"})["customComponent"]["tokens"] == ["user"]


def test_picks_type_into_lands_on_the_record_component() -> None:
    out = upgrade_workflow_input({"key": "target", "picks": ["note", "file"], "picks_type_into": "target_type"})
    assert out["customComponent"]["picksTypeInto"] == "target_type"
    VariableDefinition.model_validate(out)
    # Off a record it is parked in stash, never dropped.
    parked = upgrade_agent_variable({"name": "x", "customComponent": {"type": "text", "picksTypeInto": "t"}})
    assert parked["customComponent"]["stash"] == {"picksTypeInto": "t"}
    assert "picksTypeInto" not in parked["customComponent"]


# ── precedence / stash / parked keys (2026-10-30 fix: a null new key never beats a real legacy one) ──

def test_a_null_new_key_loses_to_its_legacy_key_and_a_real_one_wins() -> None:
    out = upgrade_agent_variable({
        "name": "n", "defaultValue": None, "default_value": "x", "label": None, "title": "T",
        "helpText": None, "description": "D", "purpose": None,
        "customComponent": {"type": None}, "componentType": "textarea",
    })
    assert out["defaultValue"] == "x" and out["label"] == "T" and out["helpText"] == "D"
    assert out["customComponent"]["type"] == "textarea"
    real = upgrade_agent_variable({
        "name": "n", "defaultValue": "new", "default_value": "old", "label": "L", "title": "T",
        "helpText": "H", "description": "D", "purpose": "P",
        "customComponent": {"type": "select"}, "componentType": "textarea",
    })
    assert real["defaultValue"] == "new" and real["label"] == "L" and real["helpText"] == "H"
    assert real["purpose"] == "P" and real["customComponent"]["type"] == "select"
    beside = upgrade_agent_variable({"name": "n", "helpText": "H", "purpose": None, "description": "D"})
    assert beside["purpose"] == "D"


def test_the_current_value_outranks_an_older_stashed_one() -> None:
    out = upgrade_agent_variable({"name": "x", "customComponent": {
        "type": "text", "options": ["new"], "stash": {"options": ["old"], "min": 1}}})
    assert out["customComponent"]["stash"] == {"options": ["new"], "min": 1}


def test_workflow_door_parks_settings_its_component_cannot_carry() -> None:
    out = upgrade_workflow_input({"key": "t", "type": "text", "options": ["a"], "option_labels": {"a": "A"},
                                  "accept": "image/*"})
    cc = out["customComponent"]
    assert cc["type"] == "text" and cc["stash"] == {"options": ["a"], "optionLabels": {"a": "A"}, "accept": "image/*"}
    VariableDefinition.model_validate(out)
    assert upgrade_workflow_input(out) == out
