"""Converting a step carries its 'Only when', 'If skipped' and 'Shape the result' — or refuses.

``data.when`` / ``data.if_skipped`` read the step's INPUTS and ``data.if_skipped`` / ``data.shape`` are in
the step's ANSWER shape; both change when a Run Mandate step becomes a Run Typed Agent or Run Workflow
step. Before 2026-10-28 the converter carried them verbatim (Smart Add unit 7 / 8 conversions), so the
converted gate read ``inputs['provision_values']`` that no longer exists and the skipped result arrived
as a run envelope downstream no longer reads.
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from matrx_ai.graph_nodes.step_conversion import MandateFacts, StepConversionRefused, convert_step

HOLDER = "aaaaaaaa-0000-0000-0000-000000000001"
CHILD_WF = "bbbbbbbb-0000-0000-0000-000000000001"


def _entry(target: str) -> dict[str, Any]:
    return {"target": target, "compact": False, "deliver": "variable", "mapType": "offered_value",
            "required": False, "when_absent": "skip", "item_separator": "\n"}


FACTS = MandateFacts(
    mandate_key="identity.is_match", holder_type="agent", holder_id=HOLDER, output_kind="identity_match_decisions",
    goal="Decide.", goal_grounding="H",
    consumption_map={"candidates": _entry("candidates"), "subject": _entry("subject_text")},
)

WHEN = "len(inputs['provision_values']['candidates']) > 0 and inputs[\"provision_values\"][\"subject_text\"] != ''"
IF_SKIPPED = "{'structured_output': {'decisions': [], 'suggestions': []}, 'content': []}"
SHAPE = "{'decisions': inputs['structured_output']['decisions']}"


def _definition(**settings: str) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "build", "type": "data.transform", "data": {"spec_type": "data.transform", "config": {}}},
            {"id": "ask", "type": "ai.mandate.start", "data": {
                "spec_type": "ai.mandate.start", "label": "Ask",
                "input": {"mandate_key": "identity.is_match", "source_feature": "smart_add"},
                "config": {}, **settings}},
            {"id": "after", "type": "data.transform", "data": {"spec_type": "data.transform", "config": {}}},
        ],
        "edges": [
            {"id": "e_in", "source": "build", "target": "ask", "data": {"kind": "data", "mappings": {"provision_values": "state"}}},
            {"id": "e_out", "source": "ask", "target": "after", "data": {"kind": "data", "mappings": {"decisions": "structured_output.decisions"}}},
        ],
    }


def _apply(definition: dict[str, Any], conv: Any) -> dict[str, Any]:
    out = copy.deepcopy(definition)
    out["nodes"] = [conv.node if n["id"] == conv.node["id"] else n for n in out["nodes"]]
    changed = {e["id"]: e for e in conv.edges}
    out["edges"] = [changed.get(e["id"], e) for e in out["edges"]]
    return out


def _evaluate(expr: str, inputs: dict[str, Any]) -> Any:
    return eval(expr, {"len": len}, {"inputs": inputs})  # the test's stand-in for the step-settings sandbox


def test_to_a_typed_step_the_gate_reads_the_variables_and_the_skipped_result_is_the_answer() -> None:
    conv = convert_step(_definition(when=WHEN, if_skipped=IF_SKIPPED, shape=SHAPE), "ask", "agent", FACTS)
    data = conv.node["data"]
    assert "provision_values" not in data["when"]
    assert _evaluate(data["when"], {"candidates": [1], "subject": "Patagonia"}) is True
    assert _evaluate(data["when"], {"candidates": [], "subject": "Patagonia"}) is False
    # The typed step's result IS the answer: downstream now reads `decisions`, not structured_output.decisions.
    assert _evaluate(data["if_skipped"], {}) == {"decisions": [], "suggestions": []}
    assert _evaluate(data["shape"], {"decisions": ["d"], "suggestions": []}) == {"decisions": ["d"]}


def test_a_run_fact_read_downstream_stays_beside_the_skipped_answer() -> None:
    definition = _definition(when=WHEN, if_skipped=IF_SKIPPED)
    definition["edges"][1]["data"]["mappings"]["blocks"] = "content"
    data = convert_step(definition, "ask", "agent", FACTS).node["data"]
    assert _evaluate(data["if_skipped"], {}) == {"decisions": [], "suggestions": [], "content": []}


def test_to_a_workflow_step_the_skipped_result_is_the_workflows_output() -> None:
    facts = MandateFacts(**{**FACTS.__dict__, "holder_type": "workflow", "holder_id": CHILD_WF})
    data = convert_step(_definition(when=WHEN, if_skipped=IF_SKIPPED), "ask", "workflow", facts).node["data"]
    assert _evaluate(data["when"], {"candidates": [1], "subject": "x"}) is True
    assert _evaluate(data["if_skipped"], {}) == {"output": {"decisions": [], "suggestions": []}}


def test_converting_back_restores_what_the_mandate_step_reads() -> None:
    original = _definition(when=WHEN, if_skipped="{'structured_output': {'decisions': []}}", shape=SHAPE)
    there = _apply(original, convert_step(original, "ask", "agent", FACTS))
    back = convert_step(there, "ask", "mandate", FACTS).node["data"]
    state = {"provision_values": {"candidates": [1], "subject_text": "x"}}
    assert _evaluate(back["when"], state) is True
    assert _evaluate(back["if_skipped"], {}) == {"structured_output": {"decisions": []}}
    assert _evaluate(back["shape"], {"structured_output": {"decisions": ["d"]}}) == {"decisions": ["d"]}


def test_a_gate_reading_the_whole_state_or_an_unbound_value_refuses_naming_it() -> None:
    for when in ("len(inputs['provision_values']) > 0", "inputs['provision_values']['not_in_binding'] != ''"):
        with pytest.raises(StepConversionRefused, match="provision_values"):
            convert_step(_definition(when=when), "ask", "agent", FACTS)
