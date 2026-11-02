"""A HUMAN GATE ADDRESSED TO A SEAT — asked of whoever holds it when the gate opens.

Owner, 2026-10-18: humans hold named positions in the org chart, and a decision
can be addressed to a position ("Brand owner") instead of to "whoever can open
the record". These tests prove, on the real scheduler:

1. The holder is resolved AT GATE OPEN (not at design time): a seat that changes
   hands between two runs of the same definition reaches the new holder, and the
   holder is told through the host's notifier.
2. An empty seat is honest: the gate opens, says "No one holds <seat>", waits —
   and nobody else is notified in its place.
3. A seat that does not exist, or no resolver at all, fails the step loudly.
4. A seated gate still resumes with the engine-built decision.
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
    SeatHolder,
    compile_graph,
    configure_seat_notifier,
    configure_seat_resolver,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context

SEAT = "6f1b0f5e-0000-4000-8000-000000000001"


def _graph(position_id: str = SEAT) -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "ask_owner",
                "type": "control.human_input",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {
                        "preset": "decision",
                        "title": "Approve the positioning",
                        "prompt": "Is this our positioning?",
                        "decision": {
                            "items": [{"key": "ok", "label": "Positioning", "value": "Calm care", "required": True}],
                            "seat": {"position_id": position_id, "label": "Brand owner"},
                        },
                    }
                },
            },
            {
                "id": "after",
                "type": "data.transform",
                "position": {"x": 320, "y": 0},
                "data": {"config": {"expression": "inputs['decision']"}},
            },
        ],
        "edges": [
            {
                "id": "e1",
                "source": "ask_owner",
                "target": "after",
                "data": {"kind": "data", "mappings": {"decision": "decision"}},
            }
        ],
    }


def _scheduler(checkpointer: MemoryCheckpointer, position_id: str = SEAT) -> Scheduler:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(_graph(position_id)), registry=registry)
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)


@pytest.fixture
def seats() -> Any:
    state: dict[str, Any] = {"holder": "user-arman", "name": "Arman", "notified": [], "asked": []}

    async def resolve(position_id: str, *, user_id: str | None, organization_id: str | None) -> SeatHolder | None:
        state["asked"].append(position_id)
        if position_id != SEAT:
            return None
        return SeatHolder(
            position_id=position_id,
            seat_name="Brand owner",
            holder_user_id=state["holder"],
            holder_name=state["name"],
        )

    async def notify(holder: SeatHolder, **kwargs: Any) -> None:
        state["notified"].append((holder.holder_user_id, kwargs["run_id"], kwargs["node_id"]))

    configure_seat_resolver(resolve)
    configure_seat_notifier(notify)
    yield state
    configure_seat_resolver(None)
    configure_seat_notifier(None)


async def _park(run_id: str, checkpointer: MemoryCheckpointer, position_id: str = SEAT):
    result = await _scheduler(checkpointer, position_id).run(run_id=run_id)
    return result, await checkpointer.latest_checkpoint(run_id)


async def test_the_holder_is_resolved_when_the_gate_opens_and_is_told(seats: Any) -> None:
    cp = MemoryCheckpointer()
    result, parked = await _park("run-a", cp)
    assert result.status is RunStatus.INTERRUPTED
    seat = parked.interrupt_payload["decision"]["seat"]
    assert seat["holder_user_id"] == "user-arman" and seat["filled"] is True
    assert seat["notice"] == "Waiting on Arman (Brand owner)" and seat["notified"] is True
    assert seats["notified"] == [("user-arman", "run-a", "ask_owner")]

    # The seat changes hands; the SAME definition's next run asks the new holder.
    seats["holder"], seats["name"] = "user-dana", "Dana"
    _, parked_b = await _park("run-b", MemoryCheckpointer())
    assert parked_b.interrupt_payload["decision"]["seat"]["holder_user_id"] == "user-dana"
    assert seats["notified"][-1] == ("user-dana", "run-b", "ask_owner")

    # And the gate still opens with the engine's decision.
    resumed = await _scheduler(cp).resume(
        run_id="run-a",
        checkpoint_id=parked.checkpoint_id,
        resume_value={"answer": {"answers": {"ok": {"verdict": "confirm"}}}},
    )
    assert resumed.status is RunStatus.COMPLETED
    assert resumed.last_outputs["after"]["result"][0]["value"] == "Calm care"


async def test_an_empty_seat_says_so_and_waits_without_asking_anyone_else(seats: Any) -> None:
    seats["holder"], seats["name"] = None, None
    result, parked = await _park("run-empty", MemoryCheckpointer())
    assert result.status is RunStatus.INTERRUPTED, "an empty seat must keep the gate open, not fail or pass it"
    seat = parked.interrupt_payload["decision"]["seat"]
    assert seat["filled"] is False and seat["holder_user_id"] is None
    assert seat["notice"] == "No one holds Brand owner"
    assert seats["notified"] == [], "an empty seat notified someone else in its place"
    assert "after" not in (result.last_outputs or {})


async def test_a_seat_that_does_not_exist_fails_loudly(seats: Any) -> None:
    result, _ = await _park("run-missing", MemoryCheckpointer(), position_id="no-such-seat")
    assert result.status is not RunStatus.COMPLETED and result.status is not RunStatus.INTERRUPTED
    assert seats["notified"] == []


async def test_no_resolver_never_falls_back_to_record_access() -> None:
    configure_seat_resolver(None)
    result, _ = await _park("run-unwired", MemoryCheckpointer())
    assert result.status is not RunStatus.INTERRUPTED, "a seated gate opened with nobody resolved"
    assert result.status is not RunStatus.COMPLETED
