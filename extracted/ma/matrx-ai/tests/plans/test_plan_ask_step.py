"""A plan step a PERSON answers (``PlanStep.ask``) — pauses the run, resumes with the answer.

The compiled-Orchestra seat member (a person holding an org-chart position) is
built on this: the step compiles to ``control.human_input`` and the run waits
durably at it; the answer becomes the step's ``final_text`` so every downstream
``$steps.N.output.final_text`` reads it exactly as it would an agent's. Proven on
the real scheduler, with a brand-new scheduler for the resume (a restart), and a
join whose other branch is an agent (the layer padding stays correct).
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from matrx_ai.graph_nodes import register_with_graph
from matrx_ai.plans import AgentPlan, compile_plan
from matrx_ai.plans.types import plan_json_schema
from matrx_graph import Definition, MemoryCheckpointer, RunStatus, Scheduler, compile_graph, register_builtin_nodes
from matrx_graph.executor.registry import default_registry

_A1 = "1fd0cb1f-5b95-49f0-a7f8-79308dc50f58"

_ASK = {
    "preset": "decision",
    "title": "Brand owner",
    "prompt": "Your part of this job",
    "decision": {"items": [{"key": "response", "label": "Your answer", "choices": ["custom"], "required": True}]},
}


def _plan() -> AgentPlan:
    return AgentPlan.model_validate(
        {
            "name": "draft, owner, finish",
            "reasoning": "an agent drafts, the owner answers, an agent finishes",
            "steps": [
                {"step": 1, "agent_id": _A1, "purpose": "draft", "inputs": {"user_input": "launch copy"}},
                {
                    "step": 2,
                    "ask": _ASK,
                    "purpose": "Brand owner",
                    "inputs": {"context": {"step_1_output": {"content": "$steps.1.output.final_text", "label": "Draft"}}},
                },
                {"step": 3, "agent_id": _A1, "purpose": "side", "inputs": {"user_input": "side"}, "depends_on": [1]},
                {
                    "step": 4,
                    "agent_id": _A1,
                    "purpose": "finish",
                    "inputs": {
                        "context": {
                            "owner": {"content": "$steps.2.output.final_text", "label": "Owner"},
                            "side": {"content": "$steps.3.output.final_text", "label": "Side"},
                        },
                        "host_turn": {"text": "Finish.", "reason": "test"},
                    },
                },
            ],
        }
    )


def _mocked(definition: Definition) -> Definition:
    for node in definition.nodes:
        if node.type == "ai.agent.start":
            node.data["mock_response"] = {
                "enabled": True,
                "output": {"conversation_id": "c", "request_id": "r", "iterations": 1, "final_text": f"out of {node.id}"},
            }
    return definition


def _scheduler(definition: Definition, checkpointer: MemoryCheckpointer) -> Scheduler:
    from matrx_connect.context.app_context import AppContext

    register_builtin_nodes(default_registry(), overwrite=True)
    register_with_graph()
    from matrx_connect.emitters.silent_emitter import SilentEmitter as _E
    ctx = AppContext(emitter=_E(), user_id="test-user", is_authenticated=True, conversation_id="c", request_id="r")
    return Scheduler(compile_graph(definition), checkpointer, ctx, registry=default_registry())


async def test_an_ask_step_pauses_and_its_answer_becomes_the_steps_output() -> None:
    definition = _mocked(compile_plan(_plan()))
    assert any(n.id == "step_2_ask" and n.type == "control.human_input" for n in definition.nodes)
    checkpointer = MemoryCheckpointer()

    parked = await _scheduler(definition, checkpointer).run(run_id="run-ask")
    assert parked.status is RunStatus.INTERRUPTED, parked.status
    assert "step_4" not in (parked.last_outputs or {}), "the step after the person ran before they answered"
    checkpoint = await checkpointer.latest_checkpoint("run-ask")
    assert checkpoint.interrupt_payload["context"]["step_1_output"]["content"] == "out of step_1"

    resumed = await _scheduler(definition, checkpointer).resume(
        run_id="run-ask",
        checkpoint_id=checkpoint.checkpoint_id,
        resume_value={"answer": {"answers": {"response": {"verdict": "custom", "value": "Lead with the calm."}}}},
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.status
    assert resumed.last_outputs["step_2"]["final_text"] == "Lead with the calm."
    finish_ctx = resumed.last_outputs["step_4_args"]["context"]
    assert finish_ctx["owner"]["content"] == "Lead with the calm."
    assert finish_ctx["side"]["content"] == "out of step_3"


def test_the_planners_contract_never_offers_ask_and_still_requires_an_agent() -> None:
    step = plan_json_schema()["$defs"]["PlanStep"]
    assert "ask" not in step["properties"]
    assert "agent_id" in step["required"]
    with pytest.raises(ValidationError):
        AgentPlan.model_validate({"name": "x", "reasoning": "y", "steps": [{"step": 1, "purpose": "nobody"}]})
    with pytest.raises(ValidationError):
        AgentPlan.model_validate(
            {"name": "x", "reasoning": "y", "steps": [{"step": 1, "agent_id": _A1, "ask": _ASK, "purpose": "both"}]}
        )
