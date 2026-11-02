"""The mid-run pause, end to end, as a PERSON experiences it.

W47 (expert-book challenge, 2026-09-12). A Conductor told a parent this
platform had no step that pauses mid-run to ask a follow-up question, while a
sibling Conductor was shipping exactly that (definition 129a4ec1, node
``consult_pause`` — an AI step wrote the questions, the parent typed an answer,
the same run carried on with it). ``test_scheduler_interrupt_siblings`` already
guards what the SCHEDULER does around an interrupt. What nothing guarded is the
round trip the person actually lives through, and it has three parts that can
each break on their own:

  1. THE QUESTION REACHES THE SCREEN. An upstream step writes the question; the
     pause node interpolates it into ``prompt`` and it must arrive in the
     interrupt payload the page renders. If interpolation regresses, the person
     is shown a literal ``{questions}`` and cannot answer sensibly.
  2. THE ANSWER IS DURABLY RECORDED AS THE NODE'S OUTCOME — not merely passed
     along in memory. This is the row a reloaded page reads: the resume
     response is a stream the client throws away, so if the answer is not in
     the outcome store, reloading after answering loses it.
  3. THE DOWNSTREAM STEP RECEIVES THE ANSWER ITSELF, through a normal mapping
     from ``answer`` — the contract every author is now taught in
     ``build-matrx-workflow`` §7 and the tool's ``pausing_to_ask_the_person``
     note.

Everything here is the REAL engine: the real registry, the real compiler, the
real ``Scheduler.run``/``resume``, the real ``control.human_input`` executor and
the real checkpointer protocol. The store is ``MemoryCheckpointer`` because the
only Postgres this repo can reach is production and ``tests/_db_guard.py``
rightly refuses it; it is the same ``save_checkpoint`` / ``record_outcome`` /
``get_outcome`` protocol ``PostgresCheckpointer`` implements over
``workflow.checkpoint`` and ``workflow.node_outcome``, and the durable half is
proven live on a real run besides.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context

RUN = "run-w47-pause"


def _consultation_graph() -> dict[str, Any]:
    """The live shape, minus the paid AI call: a step WRITES the question, the
    pause asks it, a later step reads the person's answer."""
    return {
        "nodes": [
            {
                "id": "ask_questions",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "'Q1. How old is she?'"}},
            },
            {
                "id": "consult_pause",
                "type": "control.human_input",
                "position": {"x": 320, "y": 0},
                "data": {
                    "label": "The parent answers",
                    "config": {
                        "title": "A few questions before I advise",
                        "preset": "free_text",
                        "presentation": "showcase",
                        "prompt": "{questions}\n\nAnswer in your own words.",
                    },
                },
            },
            {
                "id": "case_file",
                "type": "data.transform",
                "position": {"x": 640, "y": 0},
                "data": {"config": {"expression": "'CASE: ' + inputs['answers']"}},
            },
        ],
        "edges": [
            {
                "id": "e_ask_pause",
                "source": "ask_questions",
                "target": "consult_pause",
                "data": {"kind": "data", "mappings": {"questions": "result"}},
            },
            {
                "id": "e_pause_case",
                "source": "consult_pause",
                "target": "case_file",
                "data": {"kind": "data", "mappings": {"answers": "answer"}},
            },
        ],
    }


def _scheduler() -> tuple[Scheduler, MemoryCheckpointer]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(_consultation_graph()), registry=registry)
    checkpointer = MemoryCheckpointer()
    return (
        Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry),
        checkpointer,
    )


async def test_the_run_pauses_with_the_question_the_upstream_step_wrote() -> None:
    scheduler, checkpointer = _scheduler()

    result = await scheduler.run(run_id=RUN)

    assert result.status is RunStatus.INTERRUPTED, (
        "the run did not stop to ask — a workflow with a Pause & Ask step ran "
        f"straight through to {result.status}"
    )
    assert result.interrupt is not None and result.interrupt["node_id"] == "consult_pause"

    payload = result.interrupt["payload"]
    assert "Q1. How old is she?" in payload["prompt"], (
        "the question the upstream step wrote never reached the screen: "
        f"{payload['prompt']!r}"
    )
    assert "{questions}" not in payload["prompt"], (
        "the prompt placeholder was shown to the person verbatim instead of "
        "being filled in."
    )
    # The presentation block the page renders travels with the question.
    assert payload["title"] == "A few questions before I advise"
    assert payload["preset"] == "free_text"
    assert payload["presentation"] == "showcase"

    # And it is on the durable checkpoint, not only in this return value — a
    # process that dies here still knows what it was waiting for.
    parked = await checkpointer.latest_checkpoint(RUN)
    assert parked is not None and parked.interrupt_payload
    assert "Q1. How old is she?" in parked.interrupt_payload["prompt"]


async def test_the_answer_is_recorded_on_the_run_and_reaches_the_next_step() -> None:
    scheduler, checkpointer = _scheduler()
    await scheduler.run(run_id=RUN)
    parked = await checkpointer.latest_checkpoint(RUN)
    assert parked is not None

    resumed = await scheduler.resume(
        run_id=RUN,
        checkpoint_id=parked.checkpoint_id,
        resume_value={"answer": "She is four and a half."},
    )

    assert resumed.status is RunStatus.COMPLETED
    assert resumed.last_outputs["case_file"]["result"] == "CASE: She is four and a half.", (
        "the step after the pause did not receive the person's answer: "
        f"{resumed.last_outputs.get('case_file')}"
    )

    # THE RELOAD GUARANTEE: the answer is persisted as the pause node's own
    # outcome, so a page that re-reads the run after answering still has it.
    # The resume response itself is a stream the client discards.
    paused_invocation = next(
        ni for ni in parked.next_invocations if ni.node_id == "consult_pause"
    )
    recorded = await checkpointer.get_outcome(
        RUN,
        step=parked.step,
        node_id="consult_pause",
        attempt=paused_invocation.attempt,
        dispatch_id=paused_invocation.dispatch_id,
        item_index=paused_invocation.item_index,
    )
    assert recorded is not None, (
        "nothing was recorded for the pause node, so a reload after answering "
        "has no record of what the person said."
    )
    stored = recorded.output
    assert stored["answer"] == "She is four and a half.", stored
    # Undeclared keys the screen collected are kept, one level down, rather
    # than dropped — the client authors the resume payload, the node still has
    # an honest output shape. (WHO decided is stamped by the resume ROUTE, not
    # by the engine, so it is not asserted here.)
    assert "extras" in stored, stored
