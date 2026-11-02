"""A form gate's default answer settles it on timeout, and its wait may come from a run input.

2026-10-27 (run c6d31239): a ``control.human_input`` form gate with ``required: ["decision"]``
and an escalation ``fallback: "default_answer"`` whose default is JSON TEXT
(``'{"decision": "continue", ...}'``) resumed at the deadline with ``{"answer": "<text>"}``,
which its own schema refuses — the run FAILED instead of continuing. Every seeded
AI-visibility review gate used exactly this pattern. Now:

* JSON-object text on a gate whose schema wants an object resumes AS that object (the
  sweeper's helper and the engine's resume seam both), stamped ``authority: "default"``;
* a default that could never satisfy the gate's schema is refused at SAVE;
* ``escalation.after_seconds`` may read a run input (``{"$input": "wait_seconds"}``), still
  held to the 5-minute minimum, and the deadline frozen into the run uses the bound value.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from matrx_graph import (
    CompilationError,
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.decision_spec import default_answer_resume_value
from matrx_graph.decisions import DECISION_KEY, MIN_DEADLINE_SECONDS, default_answer_decision
from matrx_graph.validation import validate_definition

from tests._fixtures import make_app_context

GATE_SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {"type": "string", "enum": ["approve", "edit", "continue"]},
        "edits": {"type": "object"},
        "note": {"type": "string"},
    },
    "required": ["decision"],
}
JSON_DEFAULT = json.dumps({"decision": "continue", "note": "Nobody answered in time."})


def _registry() -> NodeRegistry:
    return register_builtin_nodes(NodeRegistry())


def _gate(config: dict, *, variables: list | None = None) -> dict:
    return {
        "variables": variables or [],
        "nodes": [
            {
                "id": "ask",
                "type": "control.human_input",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"prompt": "Approve?", **config}},
            }
        ],
        "edges": [],
    }


async def _park(definition: dict, run_id: str, **scheduler_kwargs):
    registry = _registry()
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    checkpointer = MemoryCheckpointer()
    result = await Scheduler(
        graph, checkpointer, make_app_context(), registry=registry, **scheduler_kwargs
    ).run(run_id=run_id)
    assert result.status is RunStatus.INTERRUPTED, result.error
    cp = next(c for c in await checkpointer.list_checkpoints(run_id) if c.interrupt_payload)
    return graph, checkpointer, registry, cp


async def _resume(parked, run_id: str, value: dict):
    graph, checkpointer, registry, cp = parked
    return await Scheduler(graph, checkpointer, make_app_context(), registry=registry).resume(
        run_id=run_id,
        checkpoint_id=cp.checkpoint_id,
        resume_value=value,
        decision=default_answer_decision(
            deadline_at=datetime.fromisoformat(cp.interrupt_payload["escalation"]["deadline_at"])
        ),
    )


FORM_GATE = {
    "preset": "form",
    "schema_hint": GATE_SCHEMA,
    "default_answer": JSON_DEFAULT,
    "escalation": {"after_seconds": 3600, "fallback": "default_answer"},
}


async def test_a_form_gate_times_out_to_its_json_default_and_continues() -> None:
    parked = await _park(_gate(FORM_GATE), "gate-json-default")
    value = default_answer_resume_value(parked[3].interrupt_payload)  # the sweeper's one helper
    assert value == {"decision": "continue", "note": "Nobody answered in time."}
    result = await _resume(parked, "gate-json-default", value)
    assert result.status is RunStatus.COMPLETED, result.error
    out = result.last_outputs["ask"]
    assert out["extras"]["decision"] == "continue"
    assert out[DECISION_KEY]["authority"] == "default"


async def test_a_host_that_resumes_with_the_wrapped_text_is_settled_by_the_engine() -> None:
    parked = await _park(_gate(FORM_GATE), "gate-json-wrapped")
    result = await _resume(parked, "gate-json-wrapped", {"answer": JSON_DEFAULT})
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["ask"]["extras"]["decision"] == "continue"
    assert result.last_outputs["ask"][DECISION_KEY]["authority"] == "default"


async def test_a_plain_text_default_with_no_schema_still_works() -> None:
    config = {
        "default_answer": "ok",
        "escalation": {"after_seconds": 3600, "fallback": "default_answer"},
    }
    parked = await _park(_gate(config), "gate-plain")
    value = default_answer_resume_value(parked[3].interrupt_payload)
    assert value == {"answer": "ok"}
    result = await _resume(parked, "gate-plain", value)
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["ask"]["answer"] == "ok"


@pytest.mark.parametrize(
    "bad_default",
    [json.dumps({"decision": "maybe"}), json.dumps({"note": "no decision"}), "continue"],
)
def test_a_default_that_breaks_the_gate_schema_is_refused_at_save(bad_default: str) -> None:
    result = validate_definition(
        _gate({**FORM_GATE, "default_answer": bad_default}), registry=_registry()
    )
    assert not result.valid
    assert any("default answer cannot settle this question" in i.message for i in result.issues), (
        result.issues
    )


def test_the_good_json_default_saves() -> None:
    assert validate_definition(_gate(FORM_GATE), registry=_registry()).valid


# ── the wait from a run input ─────────────────────────────────────────────


def _wait_gate(after_seconds: object, default: int = 3600) -> dict:
    return _gate(
        {**FORM_GATE, "escalation": {"after_seconds": after_seconds, "fallback": "default_answer"}},
        variables=[{"name": "wait_seconds", "default": default}],
    )


async def test_the_wait_comes_from_a_run_input_and_is_frozen_into_the_run() -> None:
    defn = _wait_gate({"$input": "wait_seconds"})
    assert validate_definition(defn, registry=_registry()).valid
    for wait in (600, 7200):
        parked = await _park(defn, f"gate-wait-{wait}", surface_inputs={"wait_seconds": wait})
        esc = parked[3].interrupt_payload["escalation"]
        assert esc["after_seconds"] == wait
        deadline = datetime.fromisoformat(esc["deadline_at"]) - datetime.fromisoformat(
            esc["waiting_since"]
        )
        assert deadline == timedelta(seconds=wait)


async def test_a_wait_below_the_minimum_is_refused() -> None:
    # at save, through the input's declared default
    result = validate_definition(
        _wait_gate({"$input": "wait_seconds"}, default=60), registry=_registry()
    )
    assert not result.valid
    # at run time, through the run's value
    registry = _registry()
    graph = compile_graph(
        Definition.model_validate(_wait_gate({"$input": "wait_seconds"})), registry=registry
    )
    result = await Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(),
        registry=registry,
        surface_inputs={"wait_seconds": 60},
    ).run(run_id="gate-wait-short")
    assert result.status in (RunStatus.FAILED, RunStatus.ERRORED)
    assert str(MIN_DEADLINE_SECONDS) in (result.error or "")


def test_the_whole_escalation_still_cannot_come_from_an_input() -> None:
    defn = _wait_gate(3600)
    defn["nodes"][0]["data"]["config"]["escalation"] = {"$input": "wait_seconds"}
    assert not validate_definition(defn, registry=_registry()).valid
    with pytest.raises(CompilationError):
        compile_graph(Definition.model_validate(defn), registry=_registry())


def test_the_wait_must_name_a_declared_input() -> None:
    result = validate_definition(_wait_gate({"$input": "nope"}), registry=_registry())
    assert any(
        "'nope', which is not on this workflow's input surface" in i.message for i in result.issues
    )
