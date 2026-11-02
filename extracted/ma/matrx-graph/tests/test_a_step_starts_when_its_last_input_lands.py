"""START WHEN READY — a step starts the moment its last input lands (executor/FEATURE.md).

Smart Add Identify (run 105d7531, 2026-10-30): ``classify`` started at 48.7 s although everything
it reads was ready at ~27 s. Plain run-ahead routes a finished result alone (or with its own
step's finished members), once, against the barrier's join state, so a join fed by two early
launches, or by results that finished before the barrier advanced, waited for an unrelated slow
step. ``Definition.metadata["start_when_ready"]`` re-routes every finished result the barrier has not routed
yet, in step order, whenever a new fact arrives — and keeps every key, checkpoint and replay the
barrier's.

Each timing test is red with the setting off (asserted in the same test).
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

import pytest

from matrx_graph import Definition, RunStatus
from matrx_graph.compile import START_WHEN_READY_KEY
from matrx_graph.executor.scheduler import RUN_AHEAD_ENABLED
from tests.test_scheduler_ready_nodes_do_not_wait import (
    SLOW_S,
    _edge,
    _engine_leftovers,
    _JsonRoundTripCheckpointer,
    _node,
    _scheduler,
    _Sleeper,
)

pytestmark = pytest.mark.skipif(not RUN_AHEAD_ENABLED, reason="run-ahead kill switch is off")


def _definition(raw: dict[str, Any], *, eager: bool) -> Definition:
    metadata = {**raw.get("metadata", {}), START_WHEN_READY_KEY: True} if eager else raw.get("metadata", {})
    return Definition.model_validate({**raw, "metadata": metadata})


def _two_launches_join() -> dict[str, Any]:
    """``join`` reads ``b`` (two hops) and ``c3`` (three hops); ``slow`` runs beside them and
    nothing reads it. On the barrier both inputs are early launches, each routed alone, so the
    join waits for ``slow``."""
    return {
        "nodes": [
            _node("start"), _node("slow", SLOW_S), _node("a"), _node("b"),
            _node("c1"), _node("c2"), _node("c3"), _node("join"), _node("after"),
        ],
        "edges": [
            _edge("start", "slow"), _edge("start", "a"), _edge("a", "b"),
            _edge("start", "c1"), _edge("c1", "c2"), _edge("c2", "c3"),
            _edge("b", "join", "value"), _edge("c3", "join", "c"), _edge("join", "after"),
        ],
        "entry_nodes": ["start"],
    }


def _finished_before_the_barrier_advanced() -> dict[str, Any]:
    """The Smart Add shape: ``r1`` and ``r2`` finish while step 1 still waits on ``s1``, each routed
    alone; when step 2 begins they are already finished and plain run-ahead never routes them
    again, so ``join`` waits for ``s2`` — which it never reads."""
    return {
        "nodes": [
            _node("start"), _node("q"), _node("s1", SLOW_S / 2), _node("s2", SLOW_S),
            _node("r1"), _node("r2"), _node("join"),
        ],
        "edges": [
            _edge("start", "q"), _edge("start", "s1"), _edge("s1", "s2"),
            _edge("q", "r1"), _edge("q", "r2"),
            _edge("r1", "join", "value"), _edge("r2", "join", "other"),
        ],
        "entry_nodes": ["start"],
    }


async def _timed(raw: dict[str, Any], *, eager: bool, run_id: str) -> tuple[Any, _Sleeper, Any]:
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(_definition(raw, eager=eager), sleeper)
    result = await scheduler.run(run_id=run_id)
    assert result.status is RunStatus.COMPLETED, result.error
    assert all(count == 1 for count in sleeper.runs.values()), sleeper.runs
    return result, sleeper, checkpointer


async def test_a_join_of_two_early_launches_starts_while_an_unrelated_step_works():
    warm, *_ = _scheduler(_definition(_two_launches_join(), eager=True), _Sleeper())
    assert (await warm.run(run_id="eager-warmup")).status is RunStatus.COMPLETED

    _off, barrier, _cp = await _timed(_two_launches_join(), eager=False, run_id="join-off")
    assert barrier.started["join"] >= barrier.finished["slow"], "the off case must show the wait"

    on, eager, checkpointer = await _timed(_two_launches_join(), eager=True, run_id="join-on")
    assert eager.finished["after"] < eager.finished["slow"] - SLOW_S / 2, "the join waited for 'slow'"
    # The barrier's numbering: start 0, {slow, a, c1} 1, {b, c2} 2, c3 3, join 4, after 5.
    assert on.steps_executed == 6
    for step, node_id in ((4, "join"), (5, "after")):
        outcome = await checkpointer.get_outcome(run_id="join-on", step=step, node_id=node_id, attempt=1)
        assert outcome is not None and outcome.error is None, (step, node_id)


async def test_results_finished_before_their_step_began_are_routed_together():
    _off, barrier, _cp = await _timed(_finished_before_the_barrier_advanced(), eager=False, run_id="smart-off")
    assert barrier.started["join"] >= barrier.finished["s2"], "the off case must show the wait"

    _on, eager, _cp2 = await _timed(_finished_before_the_barrier_advanced(), eager=True, run_id="smart-on")
    assert eager.finished["join"] < eager.finished["s1"], "the join waited for the barrier"


def _outcome_map(checkpointer: Any, run_id: str) -> dict[tuple[Any, ...], tuple[Any, bool]]:
    """Every outcome by (step, node, item, attempt) — a dispatch id is minted per run, so it reads
    as "fanned"."""
    return {
        (key[1], key[2], bool(key[3]), key[4], key[5]): (o.output, o.error is None)
        for key, o in checkpointer._outcomes.items()
        if key[0] == run_id
    }


def _routes() -> dict[str, Any]:
    """Conditional edges (one taken, one not), a caught failure (error edge), an optional step
    that fails, and a for_each + gather — every route beside a slow step nothing reads early."""
    sleeper_nodes = [
        _node("start"), _node("slow", SLOW_S), _node("gate"), _node("yes"), _node("no"),
        _node("after_no"), _node("boom"), _node("handler"), _node("opt"), _node("join"),
        _node("worker", 0.01), _node("land"), _node("end"),
    ]
    sleeper_nodes[[n["id"] for n in sleeper_nodes].index("opt")]["data"]["optional"] = True
    nodes = sleeper_nodes + [
        {"id": "fan", "type": "control.map", "position": {"x": 0, "y": 0},
         "data": {"config": {"target_node_id": "worker", "payload_key": "value", "max_dispatches": 10}}},
        {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
    ]
    edges = [
        _edge("start", "slow"), _edge("start", "gate"), _edge("start", "boom"), _edge("start", "opt"),
        {"id": "e_gate_yes", "source": "gate", "target": "yes",
         "data": {"kind": "conditional", "condition": "inputs['value'] != ''", "mappings": {"value": "value"}}},
        {"id": "e_gate_no", "source": "gate", "target": "no",
         "data": {"kind": "conditional", "condition": "inputs['value'] == ''", "mappings": {"value": "value"}}},
        _edge("no", "after_no"),
        {"id": "e_boom_handler", "source": "boom", "target": "handler",
         "data": {"kind": "error", "mappings": {"value": "message"}}},
        _edge("yes", "join", "value"), _edge("handler", "join", "caught"), _edge("opt", "join", "opt"),
        {"id": "e_start_fan", "source": "start", "target": "fan",
         "data": {"kind": "data", "mappings": {"items": "items"}}},
        {"id": "e_worker_gather", "source": "worker", "target": "gather",
         "data": {"kind": "data", "mappings": {"value": "value"}}},
        {"id": "e_gather_land", "source": "gather", "target": "land", "data": {"kind": "data"}},
        _edge("join", "end", "value"), _edge("land", "end", "landed"),
    ]
    return {"nodes": nodes, "edges": edges, "entry_nodes": ["start"]}


async def _run_routes(*, eager: bool, run_id: str) -> tuple[Any, _Sleeper, Any]:
    sleeper = _Sleeper(fail_once={"boom", "opt"})
    raw = _routes()
    # start emits a list for the fan-out to walk.
    raw["nodes"][0] = {
        "id": "start", "type": "data.transform", "position": {"x": 0, "y": 0},
        "data": {"config": {"expression": "{'value': 'v', 'items': ['x', 'y', 'z']}"}},
    }
    scheduler, checkpointer, _em = _scheduler(_definition(raw, eager=eager), sleeper, _JsonRoundTripCheckpointer())
    result = await scheduler.run(run_id=run_id)
    return result, sleeper, checkpointer


async def test_every_route_resolves_exactly_as_on_the_barrier():
    off, off_sleeper, off_cp = await _run_routes(eager=False, run_id="routes")
    on, on_sleeper, on_cp = await _run_routes(eager=True, run_id="routes")
    assert off.status is RunStatus.COMPLETED, off.error
    assert on.status is RunStatus.COMPLETED, on.error
    # Same steps ran, the same number of times, under the same keys, with the same outputs.
    assert on_sleeper.runs == off_sleeper.runs
    assert "no" not in on_sleeper.runs and "after_no" not in on_sleeper.runs
    assert on_sleeper.runs["worker"] == 3 and on_sleeper.runs["handler"] == 1
    assert _outcome_map(on_cp, "routes") == _outcome_map(off_cp, "routes")
    assert on.steps_executed == off.steps_executed
    assert on.last_outputs["end"] == off.last_outputs["end"]
    # The caught failure's route and the optional step finished long before 'slow'.
    assert on_sleeper.finished["handler"] < on_sleeper.finished["slow"] - SLOW_S / 2


async def test_resume_from_every_checkpoint_never_reruns_a_step():
    raw = _two_launches_join()
    sleeper = _Sleeper()
    checkpointer = _JsonRoundTripCheckpointer()
    scheduler, _cp, _em = _scheduler(_definition(raw, eager=True), sleeper, checkpointer)
    first = await scheduler.run(run_id="eager-replay")
    assert first.status is RunStatus.COMPLETED, first.error
    finished = dict(sleeper.runs)

    checkpoints = [cp for cp in await checkpointer.list_checkpoints("eager-replay") if cp.next_invocations]
    assert len(checkpoints) >= 5
    for checkpoint in checkpoints:
        replayer, _cp2, _em2 = _scheduler(_definition(raw, eager=True), sleeper, checkpointer)
        replayed = await replayer.resume(run_id="eager-replay", checkpoint_id=checkpoint.checkpoint_id)
        assert replayed.status is RunStatus.COMPLETED, (checkpoint.step, replayed.error)
        assert sleeper.runs == finished, (checkpoint.step, sleeper.runs)


async def test_a_crash_mid_flight_resumes_without_rerunning_what_ran_ahead():
    raw = _two_launches_join()
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(_definition(raw, eager=True), sleeper)
    run = asyncio.create_task(scheduler.run(run_id="eager-crash"))
    for _ in range(200):
        if "after" in sleeper.finished:
            break
        await asyncio.sleep(0.01)
    assert "after" in sleeper.finished and "slow" not in sleeper.finished, sleeper.finished
    run.cancel()  # the process dies while 'slow' still works
    with pytest.raises(asyncio.CancelledError):
        await run
    assert _engine_leftovers() == []

    last = max(await checkpointer.list_checkpoints("eager-crash"), key=lambda c: c.step)
    resumer, _cp, _em2 = _scheduler(_definition(raw, eager=True), sleeper, checkpointer)
    resumed = await resumer.resume(run_id="eager-crash", checkpoint_id=last.checkpoint_id)
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert sleeper.runs["slow"] == 2, "the cut-off slow step runs again"
    for node_id in ("a", "b", "c1", "c2", "c3", "join", "after"):
        assert sleeper.runs[node_id] == 1, (node_id, sleeper.runs)


async def test_an_interrupt_resumes_without_rerunning_what_ran_ahead():
    raw = _two_launches_join()
    raw["nodes"][1] = _node("slow", SLOW_S, ask=True)
    sleeper = _Sleeper()
    scheduler, checkpointer, _em = _scheduler(_definition(raw, eager=True), sleeper)
    parked = await scheduler.run(run_id="eager-ask")
    assert parked.status is RunStatus.INTERRUPTED, parked.error
    assert "join" in sleeper.finished, "the join ran while the question waited"

    resumer, _cp, _em2 = _scheduler(_definition(raw, eager=True), sleeper, checkpointer)
    resumed = await resumer.resume(
        run_id="eager-ask", checkpoint_id=parked.interrupt["checkpoint_id"], resume_value={"value": "yes"}
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    for node_id in ("a", "b", "c1", "c2", "c3", "join", "after"):
        assert sleeper.runs[node_id] == 1, (node_id, sleeper.runs)


async def test_cancel_mid_flight_launches_nothing_more_and_leaves_nothing_running():
    raw = _two_launches_join()
    sleeper = _Sleeper()

    async def cancel_once_b_done() -> bool:
        return "b" in sleeper.finished

    scheduler, _cp, _em = _scheduler(_definition(raw, eager=True), sleeper, cancel_check=cancel_once_b_done)
    began = time.monotonic()
    result = await scheduler.run(run_id="eager-cancel")
    elapsed = time.monotonic() - began
    assert result.status is RunStatus.CANCELLED, result.error
    # The stop poll is throttled (RUN_AHEAD_STOP_POLL_SECONDS), so a launch already in flight may
    # finish; the run itself stops at the step boundary and nothing is left running.
    assert elapsed < SLOW_S * 1.6, f"cancel waited {elapsed:.2f}s"
    assert _engine_leftovers() == []


def test_only_a_literal_true_opts_in():
    raw = _two_launches_join()
    assert _scheduler(_definition(raw, eager=True), _Sleeper())[0].graph.start_when_ready is True
    assert _scheduler(_definition(raw, eager=False), _Sleeper())[0].graph.start_when_ready is False
    for value in ("true", 1, "yes", None, False):
        opted = Definition.model_validate({**raw, "metadata": {START_WHEN_READY_KEY: value}})
        assert _scheduler(opted, _Sleeper())[0].graph.start_when_ready is False, value
