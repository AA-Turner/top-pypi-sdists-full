"""Run Mandate ↔ Run Typed Agent ↔ Run Workflow — the converter is lossless or refuses.

Arman, 2026-10-27: a utility that converts a mandate step to an agent or workflow step and back.
These pin: the mandate's holder, kind, goal (+ approval), binding and cost attribution land on
the typed step; edges are rewired from the state/envelope to the variables/answer; the round
trip mandate → agent → mandate is identity on every meaningful field; and the refusals.
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from matrx_ai.graph_nodes.step_conversion import (
    JOIN_STEP,
    MANDATE_STEP,
    TYPED_AGENT_STEP,
    WORKFLOW_STEP,
    MandateFacts,
    StepConversionRefused,
    as_patch_ops,
    convert_step,
)

HOLDER = "aaaaaaaa-0000-0000-0000-000000000001"
HOLDER_V = "aaaaaaaa-0000-0000-0000-0000000000v1"
CHILD_WF = "bbbbbbbb-0000-0000-0000-000000000001"


def _entry(target: str) -> dict[str, Any]:
    return {"target": target, "compact": False, "deliver": "variable", "mapType": "offered_value",
            "required": False, "when_absent": "skip", "item_separator": "\n"}


FACTS = MandateFacts(
    mandate_key="education.summarize",
    holder_type="agent",
    holder_id=HOLDER,
    holder_version_id=HOLDER_V,
    output_kind="study_summary",
    goal="Summarize the material so a student can revise from it.",
    goal_grounding="H",
    consumption_map={"material": _entry("source_text"), "level": _entry("level")},
)


def _definition() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "in", "type": "io.user_input", "data": {"spec_type": "io.user_input", "config": {}}},
            {"id": "state", "type": "data.transform", "data": {"spec_type": "data.transform", "config": {}}},
            {
                "id": "sum",
                "type": MANDATE_STEP,
                "position": {"x": 10, "y": 20},
                "data": {
                    "label": "Summarize",
                    "icon": "bot",
                    "category": "agent",
                    "spec_type": MANDATE_STEP,
                    "once": {"key": ["material"], "scope": "workflow"},
                    "input": {"source_app": "workflow-studio", "source_feature": "study_kit",
                              "mandate_key": "education.summarize", "provision_values": {"level": "intro"}},
                    "config": {"include_org_catalog": False},
                },
            },
            {"id": "out", "type": "data.transform", "data": {"spec_type": "data.transform", "config": {}}},
        ],
        "edges": [
            {"id": "e_state", "source": "state", "target": "sum", "data": {"kind": "data", "mappings": {"provision_values": "provision_values"}}},
            {"id": "e_out", "source": "sum", "target": "out", "data": {"kind": "data", "mappings": {"summary": "structured_output", "title": "structured_output.title"}}},
            {"id": "e_plain", "source": "sum", "target": "out", "data": {"kind": "data"}},
        ],
    }


def _apply(definition: dict[str, Any], conversion: Any) -> dict[str, Any]:
    out = copy.deepcopy(definition)
    gone = set(conversion.removed_nodes)
    out["nodes"] = [conversion.node if n["id"] == conversion.node["id"] else n for n in out["nodes"] if n["id"] not in gone]
    out["nodes"] += copy.deepcopy(conversion.added_nodes)
    changed = {e["id"]: e for e in conversion.edges}
    out["edges"] = [changed.get(e["id"], e) for e in out["edges"]
                    if e["id"] not in set(conversion.removed_edges) and e["source"] not in gone and e["target"] not in gone]
    out["edges"] += copy.deepcopy(conversion.added_edges)
    return out


def _canon(definition: dict[str, Any]) -> dict[str, Any]:
    return {"nodes": sorted(definition["nodes"], key=lambda n: n["id"]),
            "edges": sorted(definition["edges"], key=lambda e: e["id"])}


def test_mandate_to_typed_agent_carries_what_the_mandate_gave() -> None:
    conv = convert_step(_definition(), "sum", "agent", FACTS)
    node = conv.node
    assert node["type"] == TYPED_AGENT_STEP and node["data"]["spec_type"] == TYPED_AGENT_STEP
    data = node["data"]
    assert data["input"]["agent_id"] == HOLDER and "is_version" not in data["input"]
    assert "mandate_key" not in data["input"] and "provision_values" not in data["input"]
    assert data["input"]["level"] == "intro"  # static state → the agent's own variable
    assert data["input"]["source_feature"] == "study_kit"  # cost attribution carried
    assert data["output_kind"] == "study_summary"
    assert data["config"]["goal"] == FACTS.goal and data["config"]["goal_approved"] is True
    assert set(data["config"]["exposed_variables"]) == {"material", "level"}
    assert data["once"] == {"key": ["material"], "scope": "workflow"} and data["label"] == "Summarize"
    edges = {e["id"]: e for e in conv.edges}
    assert edges["e_state"]["data"]["mappings"] == {"material": "provision_values.source_text", "level": "provision_values.level"}
    assert edges["e_out"]["data"]["mappings"] == {"summary": "$FULL_PAYLOAD", "title": "title"}
    assert edges["e_plain"]["data"]["mappings"] == {"structured_output": "$FULL_PAYLOAD"}
    assert [op["op"] for op in as_patch_ops(conv)] == ["replace_node", "replace_edge", "replace_edge", "replace_edge"]


def test_mandate_to_agent_to_mandate_is_identity() -> None:
    original = _definition()
    there = _apply(original, convert_step(original, "sum", "agent", FACTS))
    back = _apply(there, convert_step(there, "sum", "mandate", FACTS))
    assert back == original


def test_an_unapproved_goal_arrives_unapproved_and_a_pin_pins_the_version() -> None:
    facts = MandateFacts(**{**FACTS.__dict__, "goal_grounding": "A"})
    conv = convert_step(_definition(), "sum", "agent", facts, pin_version=True)
    assert conv.node["data"]["config"]["goal_approved"] is False
    assert conv.node["data"]["input"]["agent_id"] == HOLDER_V and conv.node["data"]["input"]["is_version"] is True


def test_workflow_holder_converts_to_run_another_workflow_and_back() -> None:
    facts = MandateFacts(**{**FACTS.__dict__, "holder_type": "workflow", "holder_id": CHILD_WF})
    original = _definition()
    conv = convert_step(original, "sum", "workflow", facts)
    assert conv.node["data"]["spec_type"] == WORKFLOW_STEP
    assert conv.node["data"]["config"] == {"definition_id": CHILD_WF}
    assert conv.node["data"]["input"] == {"inputs": {"level": "intro"}}
    assert {e["id"]: e for e in conv.edges}["e_out"]["data"]["mappings"] == {"summary": "output", "title": "output.title"}
    with pytest.raises(StepConversionRefused, match="workflow"):
        convert_step(original, "sum", "agent", facts)


@pytest.mark.parametrize(
    ("change", "match"),
    [
        (lambda d, f: (d, MandateFacts(**{**f.__dict__, "output_kind": "json"})), "format, not a structure"),
        (lambda d, f: (d, MandateFacts(**{**f.__dict__, "consumption_map": {"material": [_entry("a"), {"mapType": "prompt_user", "prompt": "Level?"}]}})), "asks a person"),
        (lambda d, f: (d, MandateFacts(**{**f.__dict__, "pinned_context": ("level",)})), "pins"),
        (lambda d, f: (_reads(d, "no_such_field"), f), "no run has that field"),
        (lambda d, f: (_set(d, "mandate_key", None), f), "run time"),
    ],
)
def test_conversions_that_would_change_behavior_refuse(change: Any, match: str) -> None:
    definition, facts = change(_definition(), FACTS)
    with pytest.raises(StepConversionRefused, match=match):
        convert_step(definition, "sum", "agent", facts)


_WALLED = [
    (lambda d, f: (_set(d, "must_not_contain", ["secret"]), f)),
    # The firewall can also ARRIVE: mapped by a connection, or per item from a For Each (live: the
    # AI-visibility blind writer) — and a mandate can carry dispatch guards (the blind wall).
    (lambda d, f: (_firewall_on_connection(d), f)),
    (lambda d, f: (_firewall_from_for_each(d), f)),
    (lambda d, f: (d, MandateFacts(**{**f.__dict__, "dispatch_guarded": True}))),
]


@pytest.mark.parametrize("change", _WALLED)
def test_a_walled_step_converts_to_a_typed_step_that_keeps_the_wall(change: Any) -> None:
    """Run Typed Agent declares and enforces the same firewall and runs AS the mandate
    (``config.mandate_key_origin``: guards, contract, spend holds, pause) — 2026-10-28. Every way the
    firewall reaches the step (on it, by connection, from a For Each) arrives unchanged."""
    definition, facts = change(_definition(), FACTS)
    original = copy.deepcopy(definition)
    conv = convert_step(definition, "sum", "agent", facts)
    data = conv.node["data"]
    assert data["config"]["mandate_key_origin"] == FACTS.mandate_key
    before = next(n for n in original["nodes"] if n["id"] == "sum")["data"]["input"]
    for key in ("must_not_contain", "must_not_contain_match", "no_tools", "no_auto_context"):
        assert data["input"].get(key) == before.get(key)
    fed = next((e for e in conv.edges if e.get("target") == "sum" and "must_not_contain" in (_maps(e) or {})), None)
    if "must_not_contain" in (_maps(next(e for e in original["edges"] if e["target"] == "sum")) or {}):
        assert fed is not None and _maps(fed)["must_not_contain"] == "terms"
    back = convert_step(_apply(definition, conv), "sum", "mandate", facts).node["data"]
    assert "mandate_key_origin" not in back["config"] and back["input"]["mandate_key"] == FACTS.mandate_key


@pytest.mark.parametrize("change", _WALLED)
def test_a_walled_step_never_converts_to_a_workflow_step(change: Any) -> None:
    """Run Workflow has no firewall and does not run as the mandate: converting would drop the wall."""
    definition, facts = change(_definition(), MandateFacts(**{**FACTS.__dict__, "holder_type": "workflow",
                                                              "holder_id": CHILD_WF}))
    with pytest.raises(StepConversionRefused, match="request firewall|dispatch guards"):
        convert_step(definition, "sum", "workflow", facts)


def _maps(edge: dict[str, Any]) -> dict[str, Any] | None:
    return (edge.get("data") or {}).get("mappings")


def _set(definition: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    node = next(n for n in definition["nodes"] if n["id"] == "sum")
    if value is None:
        node["data"]["input"].pop(key, None)
    else:
        node["data"]["input"][key] = value
    return definition


def _reads(definition: dict[str, Any], source: str) -> dict[str, Any]:
    edge = next(e for e in definition["edges"] if e["id"] == "e_out")
    edge["data"]["mappings"]["text"] = source
    return definition


def test_keys_settings_grounding_carry_and_rebindings_are_said_loudly() -> None:
    facts = MandateFacts(**{**FACTS.__dict__, "goal_grounding": "V", "required_output_keys": ("title",),
                            "default_config_overrides": {"temperature": 0.2}, "binding_overrides": 2})
    original = _definition()
    conv = convert_step(original, "sum", "agent", facts)
    cfg, inputs = conv.node["data"]["config"], conv.node["data"]["input"]
    assert cfg["goal_grounding"] == "V" and cfg["required_output_keys"] == ["title"]
    assert inputs["config_overrides"] == {"temperature": 0.2}
    assert any(n.startswith("WARNING") and "2 organization/person" in n for n in conv.notes)
    back = _apply(_apply(original, conv), convert_step(_apply(original, conv), "sum", "mandate", facts))
    assert back == original


def test_a_text_mandate_converts_to_a_text_typed_step() -> None:
    facts = MandateFacts(**{**FACTS.__dict__, "output_kind": "text"})
    conv = convert_step(_definition(), "sum", "agent", facts)
    assert conv.node["data"]["output_kind"] == "text"


def test_a_markdown_mandate_converts_and_its_final_text_reads_round_trip() -> None:
    """Incident Assurance's written report: a ``markdown`` mandate is a typed step, not a refusal."""
    facts = MandateFacts(**{**FACTS.__dict__, "output_kind": "markdown"})
    original = _definition()
    original["edges"] = [e for e in original["edges"] if e["id"] not in ("e_out", "e_plain")]
    original["edges"].append({"id": "e_txt", "source": "sum", "target": "out", "data": {"kind": "data", "mappings": {"report": "final_text"}}})
    conv = convert_step(original, "sum", "agent", facts)
    assert conv.node["data"]["output_kind"] == "markdown"
    assert {e["id"]: e for e in conv.edges}["e_txt"]["data"]["mappings"] == {"report": "text"}
    there = _apply(original, conv)
    assert _apply(there, convert_step(there, "sum", "mandate", facts)) == original


def test_a_step_saved_with_data_inputs_converts_like_one_saved_with_data_input() -> None:
    """The compiler reads data.input first and data.inputs as the fallback (matrx_graph.compile);
    the converter reads the same way and writes the canonical singular key only."""
    canonical = _definition()
    plural = copy.deepcopy(canonical)
    sum_data = plural["nodes"][2]["data"]
    sum_data["inputs"] = sum_data.pop("input")
    assert "input" not in sum_data
    from_plural = convert_step(plural, "sum", "agent", FACTS)
    from_canonical = convert_step(canonical, "sum", "agent", FACTS)
    assert from_plural.node == from_canonical.node
    assert "inputs" not in from_plural.node["data"] and from_plural.node["data"]["input"]["agent_id"] == HOLDER
    back = _apply(plural, from_plural)
    assert "inputs" not in back["nodes"][2]["data"]
    assert convert_step(back, "sum", "mandate", FACTS).node["data"]["input"]["mandate_key"] == FACTS.mandate_key


def test_a_step_with_no_cost_stamp_files_under_the_mandates_registered_stamp() -> None:
    """A bare mandate key is refused at run time ("unregistered source_feature 'news.report'")."""
    original = _definition()
    for node in original["nodes"]:
        if node["id"] == "sum":
            node["data"]["input"].pop("source_feature")
    conv = convert_step(original, "sum", "agent", FACTS)
    assert conv.node["data"]["input"]["source_feature"] == f"mandate:{FACTS.mandate_key}"
    back = _apply(_apply(original, conv), convert_step(_apply(original, conv), "sum", "mandate", FACTS))
    assert back == original


def test_a_control_connection_out_of_the_step_stays_a_bare_control_connection() -> None:
    """A control connection with mappings is refused by validation (Agent Foundry e_artisan_a_verify)."""
    original = _definition()
    original["edges"].append({"id": "e_ctl", "source": "sum", "target": "out", "data": {"kind": "control"}})
    conv = convert_step(original, "sum", "agent", FACTS)
    assert "e_ctl" not in {e["id"] for e in conv.edges}
    there = _apply(original, conv)
    assert next(e for e in there["edges"] if e["id"] == "e_ctl") == {"id": "e_ctl", "source": "sum", "target": "out", "data": {"kind": "control"}}
    assert _apply(there, convert_step(there, "sum", "mandate", FACTS)) == original


def test_a_run_once_key_on_the_mandates_state_follows_the_input_to_its_variable() -> None:
    """News report keyed on provision_values.run_summary.run_id; on the typed step that path is gone."""
    original = _definition()
    for node in original["nodes"]:
        if node["id"] == "sum":
            node["data"]["once"] = {"key": ["provision_values.source_text.id", "material"], "scope": "workflow"}
    conv = convert_step(original, "sum", "agent", FACTS)
    assert conv.node["data"]["once"]["key"] == ["material.id", "material"]


def test_a_text_mandates_final_text_reads_become_the_text_steps_text_and_back() -> None:
    """Deep Research's report and the podcast scripts read ``final_text``; a text step answers ``text``."""
    facts = MandateFacts(**{**FACTS.__dict__, "output_kind": "text"})
    original = _definition()
    original["edges"] = [e for e in original["edges"] if e["id"] not in ("e_out", "e_plain")]
    original["edges"].append({"id": "e_txt", "source": "sum", "target": "out", "data": {"kind": "data", "mappings": {"report": "final_text"}}})
    conv = convert_step(original, "sum", "agent", facts)
    assert {e["id"]: e for e in conv.edges}["e_txt"]["data"]["mappings"] == {"report": "text"}
    there = _apply(original, conv)
    assert _apply(there, convert_step(there, "sum", "mandate", facts)) == original


# ── joins and run facts (2026-10-27): never lose a door ──────────────────────


def _headed(target: str, heading: str) -> dict[str, Any]:
    return {**_entry(target), "heading": heading}


JOIN_FACTS = MandateFacts(**{**FACTS.__dict__, "consumption_map": {
    "material": [_headed("source_text", "Source"), _headed("notes", "Notes"), {"mapType": "direct_value", "target": "Be brief."}],
    "level": _entry("level"),
}})


def test_a_join_becomes_a_visible_join_values_step_fed_what_fed_the_state() -> None:
    conv = convert_step(_definition(), "sum", "agent", JOIN_FACTS)
    (join,) = conv.added_nodes
    assert join["type"] == JOIN_STEP and join["id"] == "sum__build_material"
    assert join["data"]["input"]["parts"] == JOIN_FACTS.consumption_map["material"]
    edges = {e["id"]: e for e in conv.added_edges}
    assert edges["e_state__sum__build_material"]["data"]["mappings"] == {"values": "provision_values"}
    assert edges["sum__build_material__sum"]["data"]["mappings"] == {"material": "value"}
    # The pass-through variable still reads straight off the state connection.
    assert {e["id"]: e for e in conv.edges}["e_state"]["data"]["mappings"] == {"level": "provision_values.level"}
    assert "material" in conv.node["data"]["config"]["exposed_variables"]
    ops = [o["op"] for o in as_patch_ops(conv)]
    assert ops[0] == "add_node" and ops.count("add_edge") == 2


def test_a_join_round_trips_back_to_the_mandate_step() -> None:
    original = _definition()
    there = _apply(original, convert_step(original, "sum", "agent", JOIN_FACTS))
    back = _apply(there, convert_step(there, "sum", "mandate", JOIN_FACTS))
    assert _canon(back) == _canon(original)


def test_a_shaped_single_source_is_a_join_never_a_silent_pass_through() -> None:
    facts = MandateFacts(**{**FACTS.__dict__, "consumption_map": {"material": {**_entry("source_text"), "max_items": 3}, "level": _entry("level")}})
    conv = convert_step(_definition(), "sum", "agent", facts)
    assert [n["id"] for n in conv.added_nodes] == ["sum__build_material"]


def test_when_every_variable_is_joined_the_state_connection_moves_to_the_join_step() -> None:
    facts = MandateFacts(**{**FACTS.__dict__, "consumption_map": {"material": [_headed("source_text", "S"), _headed("level", "L")]}})
    original = _definition()
    conv = convert_step(original, "sum", "agent", facts)
    assert conv.removed_edges == ["e_state"]  # never left unmapped (it would hand its whole payload over)
    there = _apply(original, conv)
    back = _apply(there, convert_step(there, "sum", "mandate", facts))
    assert _canon(back) == _canon(original)


def test_run_fact_reads_are_kept_and_the_step_hands_them_over() -> None:
    original = _definition()
    edge = next(e for e in original["edges"] if e["id"] == "e_out")
    edge["data"]["mappings"].update({"text": "final_text", "images": "messages", "cid": "conversation_id", "cost": "usage.cost_usd"})
    conv = convert_step(original, "sum", "agent", FACTS)
    maps = {e["id"]: e for e in conv.edges}["e_out"]["data"]["mappings"]
    assert maps == {"summary": "$FULL_PAYLOAD", "title": "title", "text": "final_text", "images": "messages",
                    "cid": "conversation_id", "cost": "usage.cost_usd"}
    assert conv.node["data"]["config"]["run_envelope"] == ["final_text", "messages", "conversation_id", "usage"]
    there = _apply(original, conv)
    back = _apply(there, convert_step(there, "sum", "mandate", FACTS))
    assert back == original


def test_a_source_that_may_be_absent_is_optional_on_the_step_never_connected() -> None:
    # Live 2026-10-28, Report and deliver run 734d4832: the converted report step refused
    # "Agent variable 'angles' is set to connected" for an optional (when_absent skip) value.
    facts = MandateFacts(**{**FACTS.__dict__, "consumption_map": {
        "material": {**_entry("source_text"), "when_absent": "fail"},
        "level": {**_entry("level"), "when_absent": "use_default", "default": "basic"},
        "tone": _entry("tone"),
    }})
    original = _definition()
    conv = convert_step(original, "sum", "agent", facts)
    assert conv.node["data"]["config"]["variable_sources"] == {"level": "optional", "tone": "optional"}
    there = _apply(original, conv)
    back = _apply(there, convert_step(there, "sum", "mandate", facts))
    assert back == original


def test_an_optional_variable_with_no_value_falls_back_instead_of_refusing() -> None:
    from matrx_ai.graph_nodes.agent_action import _resolve_variable_sources

    assert _resolve_variable_sources({}, {}, {"angles": "optional"}) == {}
    assert _resolve_variable_sources({"angles": "d"}, {}, {"angles": "optional"}) == {"angles": "d"}
    assert _resolve_variable_sources({"angles": "d"}, {"angles": "x"}, {"angles": "optional"}) == {"angles": "x"}


def test_a_typed_only_setting_is_dropped_and_said_when_converting_back_to_a_mandate() -> None:
    """Agent Foundry 2026-10-28: ``config.label`` on a typed step made convert-to-mandate fail
    validation ("config.label: Extra inputs are not permitted") — the step could not go back."""
    from matrx_ai.graph_nodes.agent_action import AgentStartConfig

    original = _definition()
    there = _apply(original, convert_step(original, "sum", "agent", FACTS))
    node = next(n for n in there["nodes"] if n["id"] == "sum")
    node["data"]["config"]["label"] = "main"
    conv = convert_step(there, "sum", "mandate", FACTS)
    config = conv.node["data"]["config"]
    assert "label" not in config
    AgentStartConfig.model_validate(config)
    assert any("'label'" in note for note in conv.notes)


def test_an_error_connection_keeps_the_failures_own_fields() -> None:
    """`message`/`code` on an error connection are the failure's, not the run's: never refused, never rewritten."""
    definition = _definition()
    definition["nodes"].append({"id": "oops", "type": "data.transform", "data": {"spec_type": "data.transform", "config": {}}})
    definition["edges"].append(
        {"id": "e_err", "source": "sum", "target": "oops", "data": {"kind": "error", "mappings": {"first_error": "message"}}}
    )
    definition["edges"].append({"id": "e_err_bare", "source": "sum", "target": "oops", "data": {"kind": "error"}})
    conv = convert_step(definition, "sum", "agent", FACTS)
    assert "e_err" not in {e["id"] for e in conv.edges} and "e_err_bare" not in {e["id"] for e in conv.edges}


def _firewall_on_connection(definition: dict[str, Any]) -> dict[str, Any]:
    edge = next(e for e in definition["edges"] if e["target"] == "sum")
    edge["data"].setdefault("mappings", {})["must_not_contain"] = "terms"
    return definition


def _firewall_from_for_each(definition: dict[str, Any]) -> dict[str, Any]:
    definition["nodes"].append({"id": "each", "type": "control.map", "position": {"x": 0, "y": 0},
                                "data": {"spec_type": "control.map", "config": {
                                    "target_node_id": "sum", "payload_template": {"no_tools": True}}}})
    return definition
