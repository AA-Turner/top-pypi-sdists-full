"""A caller of a runtime-agent unit hands it the agent, its binding, kind and goal — not a mandate key.

Units such as "Draft one specialist's options" run whichever agent the caller names, and each agent's
binding joins the caller's values with its own headings and templates. Converting the CALLER
(``caller_to_agent``) replaces ``mandate_key`` with ``agent_id`` + ``binding`` + ``output_kind`` + goal;
the unit's Join Values step takes ``binding`` as an input. The binding handed over must be exactly the
parts a fixed-mandate conversion would put on its Join Values steps, so both routes join identically.
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from matrx_ai.graph_nodes.step_conversion import (
    CALLER_AGENT_FIELDS,
    MANDATE_STEP,
    WORKFLOW_STEP,
    MandateFacts,
    StepConversionRefused,
    as_patch_ops,
    caller_agent_inputs,
    convert_step,
    split_binding,
)

HOLDER = "aaaaaaaa-0000-0000-0000-000000000001"
HOLDER_V = "aaaaaaaa-0000-0000-0000-0000000000v1"


def _src(target: str, **extra: Any) -> dict[str, Any]:
    return {"mapType": "offered_value", "target": target, "deliver": "variable", "when_absent": "skip", **extra}


FACTS = MandateFacts(
    mandate_key="brand.specialist_voice",
    holder_type="agent",
    holder_id=HOLDER,
    holder_version_id=HOLDER_V,
    output_kind="brand_option_set",
    goal="Draft the voice options.",
    goal_grounding="H",
    consumption_map={
        "brand": [_src("fact_home_brand", heading="Brand"), _src("choices_voice", heading="Choices", max_items=5),
                  {"mapType": "direct_value", "target": "Answer in English.", "deliver": "variable"}],
        "caps": _src("caps"),
    },
)


def _caller() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "in", "type": "io.user_input", "data": {"spec_type": "io.user_input", "config": {}}},
            {"id": "draft", "type": WORKFLOW_STEP, "position": {"x": 1, "y": 2},
             "data": {"label": "Draft voice", "spec_type": WORKFLOW_STEP,
                      "config": {"workflow_key": "platform:brand.draft_options"},
                      "input": {"mandate_key": "brand.specialist_voice", "values": {"caps": 3}}}},
        ],
        "edges": [{"id": "e1", "source": "in", "target": "draft", "data": {"kind": "data", "mappings": {"values": "values"}}}],
    }


def test_the_caller_hands_agent_binding_kind_and_goal_instead_of_the_key() -> None:
    original = _caller()
    conv = convert_step(original, "draft", "agent", FACTS)
    inputs = conv.node["data"]["input"]
    assert "mandate_key" not in inputs
    assert inputs["agent_id"] == HOLDER
    assert inputs["binding"] == FACTS.consumption_map and inputs["binding"] is not FACTS.consumption_map
    assert inputs["output_kind"] == "brand_option_set"
    assert inputs["goal"] == FACTS.goal and inputs["goal_approved"] is True
    assert inputs["values"] == {"caps": 3}  # what the caller already passed is untouched
    assert conv.node["type"] == WORKFLOW_STEP and conv.node["data"]["config"] == original["nodes"][1]["data"]["config"]
    assert [o["op"] for o in as_patch_ops(conv)] == ["replace_node"]
    assert set(CALLER_AGENT_FIELDS) <= set(inputs)
    assert original == _caller()  # pure: the definition handed in is never mutated


def test_the_binding_handed_over_is_what_a_fixed_conversion_joins() -> None:
    # A fixed Run Mandate step converts to one Join Values step per joined variable, carrying the
    # binding's parts; the caller-side spec carries the whole binding — the same parts, so the unit's
    # Join Values(binding) builds the same text the fixed conversion's steps would.
    direct, joins = split_binding(FACTS)
    binding = caller_agent_inputs(FACTS)["binding"]
    for variable, parts in joins.items():
        assert binding[variable] == parts
    for variable, offered in direct.items():
        assert binding[variable]["target"] == offered


def test_pinning_hands_the_version() -> None:
    assert caller_agent_inputs(FACTS, pin_version=True)["agent_id"] == HOLDER_V


@pytest.mark.parametrize(
    ("facts", "match"),
    [
        (MandateFacts(**{**FACTS.__dict__, "output_kind": None}), "a format, not a structure"),
        (MandateFacts(**{**FACTS.__dict__, "output_kind": "json"}), "a format, not a structure"),
        (MandateFacts(**{**FACTS.__dict__, "holder_type": "workflow"}), "not an agent"),
        (MandateFacts(**{**FACTS.__dict__, "consumption_map": {"q": {"mapType": "prompt_user", "target": "q"}}}),
         "asks a person"),
    ],
)
def test_refusals_name_the_reason(facts: MandateFacts, match: str) -> None:
    with pytest.raises(StepConversionRefused, match=match):
        convert_step(_caller(), "draft", "agent", facts)


def test_a_caller_whose_key_is_chosen_at_run_time_is_refused() -> None:
    wf = _caller()
    wf["nodes"][1]["data"]["input"]["mandate_key"] = {"$input": "mandate_key"}
    with pytest.raises(StepConversionRefused, match="only a fixed key"):
        convert_step(wf, "draft", "agent", FACTS)


def test_a_caller_that_already_sets_an_agent_is_refused() -> None:
    wf = _caller()
    wf["nodes"][1]["data"]["input"]["agent_id"] = "someone"
    with pytest.raises(StepConversionRefused, match="already sets"):
        convert_step(wf, "draft", "agent", FACTS)


def test_a_run_mandate_step_still_converts_the_fixed_way() -> None:
    wf = copy.deepcopy(_caller())
    wf["nodes"][1].update(type=MANDATE_STEP)
    wf["nodes"][1]["data"].update(spec_type=MANDATE_STEP, input={"mandate_key": FACTS.mandate_key, "provision_values": {"caps": 3}})
    conv = convert_step(wf, "draft", "agent", FACTS)
    assert conv.node["type"] == "ai.agent.produce" and conv.added_nodes  # the fixed route: Join Values steps


def test_the_caller_hands_the_origin_mandate_so_the_units_typed_step_runs_as_that_job() -> None:
    """Break: the caller drops the mandate key and hands nothing, so a unit's Run Typed Agent step
    (``config.mandate_key_origin: {"$input": "mandate_key_origin"}``) runs unguarded."""
    conv = convert_step(_caller(), "draft", "agent", FACTS)
    assert conv.node["data"]["input"]["mandate_key_origin"] == FACTS.mandate_key
    assert "mandate_key_origin" in CALLER_AGENT_FIELDS
    assert any("mandate_key_origin" in n for n in conv.notes), conv.notes
    assert caller_agent_inputs(FACTS, pin_version=True)["mandate_key_origin"] == FACTS.mandate_key


def test_a_caller_that_already_sets_the_origin_is_refused() -> None:
    wf = _caller()
    wf["nodes"][1]["data"]["input"]["mandate_key_origin"] = "something.else"
    with pytest.raises(StepConversionRefused, match="already sets"):
        convert_step(wf, "draft", "agent", FACTS)


def test_the_units_typed_step_takes_the_origin_as_a_run_input() -> None:
    """The unit side: ``config.mandate_key_origin`` as a ``$input`` setting is accepted by the real
    workflow validator and a typed step resolves it (the field exists on ``TypedAgentConfig``)."""
    from matrx_ai.graph_nodes.agent_produce_action import TypedAgentConfig

    assert "mandate_key_origin" in TypedAgentConfig.model_fields
    assert TypedAgentConfig.model_validate({"mandate_key_origin": "brand.specialist_voice"}).mandate_key_origin
