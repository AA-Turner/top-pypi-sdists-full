"""THE HUMAN GATE — a downstream step can NEVER start before a person decides.

Arman, 2026-10-12: "some downstream steps CANNOT ever start until we get some
basic feedback on a few things from a human." The gate is ``control.human_input``
with ``preset="decision"``. These tests prove, on the REAL scheduler, compiler,
registry and checkpointer protocol:

1. The run parks INTERRUPTED at the gate with the whole typed spec in the
   durable checkpoint, and the step after the gate has not run.
2. The ENGINE refuses an incomplete answer (a required item missing, too few
   answers) and an off-menu verdict — the gate stays shut, nothing downstream.
3. After a "restart" (a brand-new Scheduler over the same durable store) a
   valid answer opens the gate, and the step after it receives the decision the
   ENGINE built from the checkpoint — a client-forged ``decision`` is discarded.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.errors import ExecutionError

from tests._fixtures import FakeEmitter, make_app_context

RUN = "run-human-gate"

ITEMS = [
    {
        "key": "name",
        "label": "Brand name",
        "value": "Sunrise Dental",
        "source": "homepage title",
        "confidence": 0.9,
        "required": True,
        "writes": {"target": "brand.name"},
    },
    {
        "key": "what_you_do",
        "label": "What you do",
        "value": "Family dentistry",
        "source": "about page",
        "confidence": 0.6,
        "writes": {"target": "brand.profile_key", "key": "positioning"},
    },
    {
        "key": "audience",
        "label": "Audience",
        "choices": ["pick_many", "custom"],
        "options": [{"value": "families", "label": "Families"}, {"value": "seniors", "label": "Seniors"}],
        "writes": {"target": "brand.profile_key", "key": "audience"},
    },
]


def _gate_graph() -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "confirm_basics",
                "type": "control.human_input",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {
                        "preset": "decision",
                        "title": "Confirm your brand profile basics",
                        "prompt": "Is this right?",
                        "decision": {
                            "items": ITEMS,
                            "min_answers": 2,
                            "subject": {"entity_type": "web_brand", "id": "brand-1"},
                        },
                    }
                },
            },
            {
                "id": "research",
                "type": "data.transform",
                "position": {"x": 320, "y": 0},
                "data": {"config": {"expression": "inputs['decision']"}},
            },
        ],
        "edges": [
            {
                "id": "e_gate_research",
                "source": "confirm_basics",
                "target": "research",
                "data": {"kind": "data", "mappings": {"decision": "decision"}},
            }
        ],
    }


def _scheduler(checkpointer: MemoryCheckpointer) -> Scheduler:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(_gate_graph()), registry=registry)
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)


async def _parked(checkpointer: MemoryCheckpointer):
    result = await _scheduler(checkpointer).run(run_id=RUN)
    assert result.status is RunStatus.INTERRUPTED, result.status
    assert "research" not in (result.last_outputs or {}), "the step after the gate ran before anyone decided"
    parked = await checkpointer.latest_checkpoint(RUN)
    assert parked is not None and parked.interrupt_payload
    return parked


async def test_the_gate_parks_with_the_whole_spec_and_nothing_downstream_runs() -> None:
    checkpointer = MemoryCheckpointer()
    parked = await _parked(checkpointer)
    payload = parked.interrupt_payload
    assert payload["preset"] == "decision"
    spec = payload["decision"]
    assert [i["key"] for i in spec["items"]] == ["name", "what_you_do", "audience"]
    assert spec["items"][0]["source"] == "homepage title" and spec["items"][0]["confidence"] == 0.9
    assert spec["subject"] == {"entity_type": "web_brand", "id": "brand-1", "level": "editor"}
    answers = payload["schema_hint"]["properties"]["answer"]["properties"]["answers"]
    assert answers["required"] == ["name"] and answers["minProperties"] == 2


@pytest.mark.parametrize(
    "answers",
    [
        {},  # nothing answered
        {"what_you_do": {"verdict": "confirm"}, "audience": {"verdict": "custom", "value": "kids"}},  # required missing
        {"name": {"verdict": "confirm"}},  # below min_answers
        {"name": {"verdict": "confirm"}, "audience": {"verdict": "confirm"}},  # verdict the item does not offer
        {"name": {"verdict": "confirm"}, "audience": {"verdict": "pick_many", "value": ["pets"]}},  # off the options
        {"name": {"verdict": "edit"}, "what_you_do": {"verdict": "confirm"}},  # edit without a value
    ],
)
async def test_the_engine_refuses_an_incomplete_or_off_menu_answer(answers: dict[str, Any]) -> None:
    checkpointer = MemoryCheckpointer()
    parked = await _parked(checkpointer)
    with pytest.raises(ExecutionError):
        await _scheduler(checkpointer).resume(
            run_id=RUN, checkpoint_id=parked.checkpoint_id, resume_value={"answer": {"answers": answers}}
        )
    outcome = await checkpointer.get_outcome(RUN, step=parked.step, node_id="research", attempt=0)
    assert outcome is None, "a refused answer still let the step after the gate run"


async def test_after_a_restart_a_valid_answer_opens_the_gate_with_the_engines_decision() -> None:
    checkpointer = MemoryCheckpointer()
    parked = await _parked(checkpointer)

    # A brand-new scheduler over the same durable store: the process that
    # parked the run is gone.
    resumed = await _scheduler(checkpointer).resume(
        run_id=RUN,
        checkpoint_id=parked.checkpoint_id,
        resume_value={
            "answer": {
                "answers": {
                    "name": {"verdict": "confirm"},
                    "what_you_do": {"verdict": "edit", "value": "Family and cosmetic dentistry"},
                    "audience": {"verdict": "pick_many", "value": ["families"]},
                }
            },
            # A forged decision naming a target the author never declared.
            "decision": [{"key": "name", "writes": {"target": "iam.users"}}],
        },
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.status
    decided = {d["key"]: d for d in resumed.last_outputs["research"]["result"]}
    assert decided["name"]["verdict"] == "confirm" and decided["name"]["value"] == "Sunrise Dental"
    assert decided["name"]["writes"] == {"target": "brand.name", "key": None, "record_id": None}
    assert decided["what_you_do"]["value"] == "Family and cosmetic dentistry"
    assert decided["what_you_do"]["original"] == "Family dentistry"
    assert decided["audience"]["value"] == ["families"]
    assert all(d["writes"]["target"] != "iam.users" for d in decided.values())


async def test_a_gate_with_no_items_fails_loudly_instead_of_waving_the_run_through() -> None:
    graph = _gate_graph()
    graph["nodes"][0]["data"]["config"]["decision"] = {"items": []}
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    compiled = compile_graph(Definition.model_validate(graph), registry=registry)
    result = await Scheduler(compiled, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry).run(
        run_id="run-empty-gate"
    )
    assert result.status is not RunStatus.COMPLETED
    assert "research" not in (result.last_outputs or {})
