"""Fidelity tests for the faithful variable → tool-parameter converter (W3-A).

Pins the replacement of the lossy ``_variable_definitions_to_parameters``
(everything → bare string) with ``matrx_ai.agents.variable_schema``:
option sets, open-enum (``allowOther``) anyOf semantics, defaults,
descriptions, numeric bounds, checkbox items enums, toggleValues-as-enum,
and the out-of-band treatment of picklist/scope bindings and media.

The fixture set is the SAME 18 live variable docs the frontend bridge test
uses (``tests/fixtures/live_agent_variables.json`` — pulled read-only from
``agent.definition.variable_definitions`` on 2026-07-15; provenance in
matrx-frontend ``features/content-ir/__tests__/fixtures/``), so both halves
of the bridge are proven against identical real data.

WIRE COMPAT is deliberately untouched: values remain strings on the wire
(``agent_tool._merge_projected_variables`` json.dumps-es non-string args) —
these tests cover SCHEMA fidelity plus that invariant.
"""

from __future__ import annotations

import json
from pathlib import Path

from matrx_ai.agents.variable_schema import (
    variable_definition_to_parameter,
    variable_definitions_to_parameters,
)
from matrx_ai.tools.agent_projection import (
    AUTO_INPUT_DESCRIPTION,
    _variable_definitions_to_parameters,
)
from matrx_ai.tools.models import ToolDefinition, ToolType

FIXTURES = json.loads(
    (Path(__file__).parent / "fixtures" / "live_agent_variables.json").read_text()
)


def _by_category(cat: str) -> list[dict]:
    return [f["variable"] for f in FIXTURES if f["category"] == cat]


def _tool_def(variable_definitions: list[dict]) -> ToolDefinition:
    return ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        function_path="agent:abc",
        prompt_id="abc",
        parameters=_variable_definitions_to_parameters(variable_definitions),
    )


# ---------------------------------------------------------------------------
# fixture coverage
# ---------------------------------------------------------------------------


def test_fixture_set_covers_the_acceptance_categories():
    cats = {f["category"] for f in FIXTURES}
    assert {
        "allow_other",
        "checkbox",
        "closed_options",
        "media",
        "number",
        "picklist",
        "scope_bound",
        "textarea",
        "toggle_values",
    } <= cats
    assert len(FIXTURES) >= 15


# ---------------------------------------------------------------------------
# per-category schema fidelity (live docs)
# ---------------------------------------------------------------------------


def test_allow_other_options_project_as_open_enum_anyof():
    for var in _by_category("allow_other"):
        param = variable_definition_to_parameter(var)
        options = var["customComponent"]["options"]
        assert param["anyOf"] == [
            {"type": "string", "enum": options},
            {"type": "string"},
        ], f"{var['name']} lost its option set"
        # help text and default survive
        if var.get("helpText"):
            assert param["description"] == var["helpText"]
        if var.get("defaultValue"):
            assert param["default"] == var["defaultValue"]


def test_closed_options_project_as_string_enum():
    for var in _by_category("closed_options"):
        param = variable_definition_to_parameter(var)
        assert param["type"] == "string"
        assert param["enum"] == var["customComponent"]["options"]


def test_checkbox_projects_as_array_with_items_enum():
    for var in _by_category("checkbox"):
        param = variable_definition_to_parameter(var)
        options = var["customComponent"]["options"]
        assert param["type"] == "array"
        items = param["items"]
        if var["customComponent"].get("allowOther"):
            assert items == {
                "anyOf": [
                    {"type": "string", "enum": options},
                    {"type": "string"},
                ]
            }
        else:
            assert items == {"type": "string", "enum": options}


def test_number_projects_with_bounds():
    for var in _by_category("number"):
        cc = var["customComponent"]
        param = variable_definition_to_parameter(var)
        assert param["type"] == "number"
        if "min" in cc:
            assert param["minimum"] == cc["min"]
        if "max" in cc:
            assert param["maximum"] == cc["max"]
        if "step" in cc:
            assert param["multipleOf"] == cc["step"]


def test_media_projects_as_string_reference():
    for var in _by_category("media"):
        param = variable_definition_to_parameter(var)
        assert param["type"] == "string"
        assert "reference" in param["description"]


def test_scope_bound_projects_as_string_with_runtime_note():
    saw_resolvable = False
    for var in _by_category("scope_bound"):
        param = variable_definition_to_parameter(var)
        assert param["type"] == "string"
        binding = var.get("binding") or {}
        if binding.get("itemKey") or binding.get("contextItemId"):
            # Resolvable binding → runtime-fill note.
            saw_resolvable = True
            assert "active scope" in param["description"]
        else:
            # An EMPTY binding (all-blank keys — one live doc has this) is
            # unresolvable; runtime ignores it (AgentVariable.scope_binding
            # returns None) and so does the converter.
            assert "active scope" not in param["description"]
    assert saw_resolvable, "fixture set must include a resolvable scope binding"


def test_toggle_values_project_as_two_value_enum_of_the_labels():
    for var in _by_category("toggle_values"):
        labels = var["customComponent"]["toggleValues"]
        param = variable_definition_to_parameter(var)
        # The labels ARE the wire values — never a boolean.
        assert param["type"] == "string"
        assert param["enum"] == list(labels)


def test_textarea_projects_as_plain_string():
    for var in _by_category("textarea"):
        param = variable_definition_to_parameter(var)
        assert param["type"] == "string"
        assert "enum" not in param


def test_picklist_bindings_stay_out_of_band():
    for var in _by_category("picklist"):
        param = variable_definition_to_parameter(var)
        cc = var["customComponent"]
        options = cc.get("options") or []
        if options and not (cc.get("structured_list") or cc.get("picklist")).get(
            "multiple"
        ):
            # Cached static options are a real value domain (open here —
            # both live picklist docs carry allowOther).
            assert param.get("anyOf") or param.get("enum")
        else:
            assert param["type"] == "string"
            assert "run time" in param["description"]
        # The binding itself must NOT appear anywhere in the schema — it is
        # server-side provenance a caller can never forge.
        assert "listId" not in json.dumps(param)


# ---------------------------------------------------------------------------
# synthetic edges (constructs not present in the live sample)
# ---------------------------------------------------------------------------


def test_plain_toggle_projects_as_boolean():
    param = variable_definition_to_parameter(
        {"name": "flag", "customComponent": {"type": "toggle"}}
    )
    assert param == {"description": "", "required": False, "type": "boolean"}


def test_percent_projects_as_bounded_number():
    param = variable_definition_to_parameter(
        {"name": "p", "customComponent": {"type": "percent"}}
    )
    assert param["type"] == "number"
    assert param["minimum"] == 0
    assert param["maximum"] == 100


def test_zero_defaults_are_omissions_not_authored_defaults():
    for zero in ("", 0, False, None):
        param = variable_definition_to_parameter(
            {"name": "v", "defaultValue": zero}
        )
        assert "default" not in param


# ---------------------------------------------------------------------------
# end-to-end: internal params → provider JSON Schema
# ---------------------------------------------------------------------------


def test_build_json_schema_carries_the_new_constructs():
    tool = _tool_def([f["variable"] for f in FIXTURES])
    schema = tool._build_json_schema()
    props = schema["properties"]

    # auto input param intact (dispatch depends on the exact description)
    assert props["input"]["description"] == AUTO_INPUT_DESCRIPTION

    for fixture in FIXTURES:
        var = fixture["variable"]
        prop = props[var["name"]]
        cat = fixture["category"]
        if cat == "allow_other":
            variants = prop["anyOf"]
            assert variants[0]["enum"] == var["customComponent"]["options"]
            assert variants[1] == {"type": "string"}
        elif cat == "closed_options":
            assert prop["enum"] == var["customComponent"]["options"]
        elif cat == "checkbox":
            assert prop["type"] == "array"
            assert "items" in prop
        elif cat == "number":
            assert prop["type"] == "number"
            if "min" in var["customComponent"]:
                assert prop["minimum"] == var["customComponent"]["min"]
        elif cat == "toggle_values":
            assert prop["enum"] == var["customComponent"]["toggleValues"]

    # required merge still works through the new paths
    required_names = {
        f["variable"]["name"]
        for f in FIXTURES
        if f["variable"].get("required")
    }
    assert required_names <= set(schema["required"])


def test_openai_format_strips_bounds_but_keeps_enums_and_anyof():
    tool = _tool_def(
        [
            {
                "name": "count",
                "customComponent": {"type": "number", "min": 1, "max": 9},
            },
            {
                "name": "pick",
                "customComponent": {
                    "type": "select",
                    "options": ["a"],
                    "allowOther": True,
                },
            },
        ]
    )
    schema = tool._build_json_schema(strip_openai_unsupported=True)
    count = schema["properties"]["count"]
    assert "minimum" not in count and "maximum" not in count
    pick = schema["properties"]["pick"]
    assert pick["anyOf"][0]["enum"] == ["a"]


def test_wire_values_remain_strings_via_dispatch_json_dumps():
    """Guard the wire-compat invariant this module documents: non-string args
    become JSON strings before they hit the (string) agent variable."""
    from matrx_ai.tools.agent_tool import _merge_projected_variables

    tool = _tool_def(
        [
            {"name": "count", "customComponent": {"type": "number"}},
            {"name": "flag", "customComponent": {"type": "toggle"}},
            {"name": "topics", "customComponent": {"type": "checkbox", "options": ["a", "b"]}},
        ]
    )
    variables, _ = _merge_projected_variables(
        {"count": 5, "flag": True, "topics": ["a", "b"]}, tool
    )
    assert variables == {"count": "5", "flag": "true", "topics": '["a", "b"]'}
