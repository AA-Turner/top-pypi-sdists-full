"""A question that was answered stays answered when its run is brought back.

Live run eedbb741 (2026-10-27): the person answered Pause & Ask gate 1 (asked
inside a called workflow, answered on the parent). The parent resumed and was
working when its server died — before it wrote its next checkpoint, so its
latest checkpoint was still the question's. Recovery had two choices and both
were wrong: resume with an empty answer (the engine rejected it against the
question's schema and burned the run), or call it "waiting on a person" and
cancel it (what happened).

The engine now reads the answer from the run itself:

- a step's OWN question: the person's answer is the recorded outcome; a resume
  with no value replays it — never validated as an empty answer, never recorded
  over the real one;
- a RELAYED question (a called workflow asked): the step runs again with no
  answer and its child decides.
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
from matrx_graph.errors import ExecutionError, GraphInterrupt
from matrx_graph.executor.answered_park import park_was_answered
from matrx_graph.nodes.subgraph.call import set_subgraph_resolver

from tests._fixtures import FakeEmitter, make_app_context

RUN = "run-answered-question"

_DECISION_SCHEMA = {
    "type": "object",
    "required": ["decision"],
    "properties": {"decision": {"type": "string", "enum": ["approve", "continue"]}},
}


def _scheduler(definition: dict[str, Any]) -> tuple[Scheduler, MemoryCheckpointer]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    checkpointer = MemoryCheckpointer()
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry), checkpointer


def _own_question() -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "ask",
                "type": "control.human_input",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"title": "Approve?", "preset": "free_text", "prompt": "Approve?"}},
            },
            {
                "id": "after",
                "type": "data.transform",
                "position": {"x": 320, "y": 0},
                "data": {"config": {"expression": "'GOT: ' + inputs['said']"}},
            },
        ],
        "edges": [
            {
                "id": "e1",
                "source": "ask",
                "target": "after",
                "data": {"kind": "data", "mappings": {"said": "answer"}},
            }
        ],
    }


async def test_a_resume_with_no_value_replays_the_answer_the_person_gave() -> None:
    scheduler, checkpointer = _scheduler(_own_question())
    await scheduler.run(run_id=RUN)
    parked = await checkpointer.latest_checkpoint(RUN)
    assert parked is not None and parked.interrupt_payload
    assert not await park_was_answered(checkpointer, parked)

    first = await scheduler.resume(run_id=RUN, checkpoint_id=parked.checkpoint_id, resume_value={"answer": "yes"})
    assert first.status is RunStatus.COMPLETED
    assert await park_was_answered(checkpointer, parked)

    # The server died after the answer: recovery resumes the SAME question checkpoint with no value.
    again = await scheduler.resume(run_id=RUN, checkpoint_id=parked.checkpoint_id, resume_value={})

    assert again.status is RunStatus.COMPLETED, again.error
    assert again.last_outputs["after"]["result"] == "GOT: yes", (
        "the recovered run did not carry the person's answer: " f"{again.last_outputs.get('after')}"
    )


async def test_an_unanswered_question_still_refuses_an_empty_answer() -> None:
    definition = _own_question()
    definition["nodes"][0]["data"]["config"]["schema_hint"] = _DECISION_SCHEMA
    scheduler, checkpointer = _scheduler(definition)
    await scheduler.run(run_id=RUN)
    parked = await checkpointer.latest_checkpoint(RUN)
    assert parked is not None and parked.interrupt_payload.get("schema_hint")

    with pytest.raises(ExecutionError, match="does not satisfy"):
        await scheduler.resume(run_id=RUN, checkpoint_id=parked.checkpoint_id, resume_value={})


@pytest.fixture
def _child_asks():
    """A called workflow that asks once, then answers whatever reaches it."""
    seen: list[Any] = []

    async def _resolver(ctx, _config, _inputs):
        seen.append(ctx.resume_answer)
        if len(seen) == 1:
            raise GraphInterrupt(node_id="child_ask", payload={"prompt": "Approve?", "schema_hint": _DECISION_SCHEMA})
        return {"run_id": "child-1", "last_outputs": {"result": {"decision": "approve"}}, "channel_values": {}}

    set_subgraph_resolver(_resolver)
    yield seen
    set_subgraph_resolver(None)


async def test_a_relayed_question_resumed_with_no_value_reruns_the_step_for_its_child(_child_asks) -> None:
    scheduler, checkpointer = _scheduler(
        {
            "nodes": [
                {
                    "id": "gate",
                    "type": "subgraph.call",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"definition_id": "11111111-1111-1111-1111-111111111111"}},
                }
            ],
            "edges": [],
        }
    )
    first = await scheduler.run(run_id=RUN)
    assert first.status is RunStatus.INTERRUPTED
    parked = await checkpointer.latest_checkpoint(RUN)
    assert parked is not None and parked.interrupt_payload

    # The person's answer already went down to the child; the parent died before its next checkpoint.
    resumed = await scheduler.resume(run_id=RUN, checkpoint_id=parked.checkpoint_id, resume_value={})

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert _child_asks == [None, None], (
        "the step must run again with NO answer (its child already has the real one), "
        f"never an empty answer passed down: {_child_asks}"
    )
