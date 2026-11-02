"""Step-mode engine primitives — the basis for "run exactly one node, persist
its result, and stop" (aidream ``POST /runs/{id}/nodes/{nid}/execute``).

Two additions to ``Scheduler.resume`` power it, with NO second execution path:
- ``stop_after_steps=N`` — park as PAUSED after N super-steps instead of running
  to completion. One super-step = "run this node (and any already-satisfied
  frontier), then stop at the resulting frontier".
- ``select_node_ids={...}`` — on the FIRST super-step only, run just these
  frontier nodes and defer the rest, folding the deferred siblings back into the
  next frontier so nothing is lost and "run the rest" picks them up.

These tests drive the seed-checkpoint + resume contract the router stands on
(mirrors ``_save_step_injection_checkpoint`` / the step-run seed), so a
regression trips here in the package with no DB.
"""

from __future__ import annotations

from pydantic import BaseModel

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checkpoint.protocol import Checkpoint, NextInvocation
from matrx_graph.executor.introspect import resolve_invocation_inputs
from matrx_graph.types.compiled import CompiledNode

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _fanout_definition() -> Definition:
    """``a`` fans out to ``b`` and ``c`` (both scheduled in the same super-step);
    b and c are terminal. Frontier after ``a`` is {b, c} — the multi-node
    frontier ``select_node_ids`` needs. Constant-expression transforms ignore
    their input, so routing edges never trips input validation."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "'ALPHA'"}},
                },
                {
                    "id": "b",
                    "type": "data.transform",
                    "position": {"x": 200, "y": -50},
                    "data": {"config": {"expression": "'BETA'"}},
                },
                {
                    "id": "c",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 50},
                    "data": {"config": {"expression": "'GAMMA'"}},
                },
            ],
            "edges": [
                {"id": "e_ab", "source": "a", "target": "b"},
                {"id": "e_ac", "source": "a", "target": "c"},
            ],
        }
    )


def _seed_at_entry(run_id: str, entry_ids: list[str]) -> Checkpoint:
    """A step-mode seed checkpoint at step 0: empty channels, one invocation per
    entry node — the frontier a step-run is born with (mirrors the router's
    step-run seed, which builds next_invocations like ``Scheduler.run``)."""
    return Checkpoint(
        checkpoint_id=f"seed-{run_id}",
        run_id=run_id,
        thread_id=run_id,
        parent_checkpoint_id=None,
        step=0,
        channel_values={},
        next_invocations=[NextInvocation(node_id=nid, inputs={}, attempt=1) for nid in entry_ids],
        interrupt_payload=None,
    )


async def _latest_checkpoint(cp: MemoryCheckpointer, run_id: str) -> Checkpoint:
    chks = await cp.list_checkpoints(run_id)
    assert chks, f"no checkpoints for {run_id}"
    return chks[-1]


# ---------------------------------------------------------------------------


async def test_stop_after_steps_parks_then_resumes_to_completion():
    """stop_after_steps=1 runs exactly one super-step (a) and PARKS at the
    resulting frontier {b, c}; a subsequent unbounded resume finishes the run
    with outcomes for every node — identical to an uninterrupted run."""
    registry = _registry()
    graph = compile_graph(_fanout_definition(), registry=registry)
    cp = MemoryCheckpointer()
    seed = _seed_at_entry("step-1", list(graph.entry_node_ids))
    await cp.save_checkpoint(seed)

    sched = Scheduler(graph, cp, make_app_context(FakeEmitter()), registry=registry)
    r1 = await sched.resume(run_id="step-1", checkpoint_id=seed.checkpoint_id, stop_after_steps=1)
    assert r1.status is RunStatus.PAUSED

    # Only 'a' executed; the parked frontier is {b, c}.
    assert await cp.get_outcome("step-1", 0, "a", 1) is not None
    assert await cp.get_outcome("step-1", 1, "b", 1) is None
    parked = await _latest_checkpoint(cp, "step-1")
    assert {ni.node_id for ni in parked.next_invocations} == {"b", "c"}

    # Hand off to the normal scheduler — runs to completion.
    r2 = await sched.resume(run_id="step-1", checkpoint_id=parked.checkpoint_id)
    assert r2.status is RunStatus.COMPLETED
    for nid in ("a", "b", "c"):
        assert await _any_outcome(cp, "step-1", nid)


async def _any_outcome(cp: MemoryCheckpointer, run_id: str, node_id: str) -> bool:
    for chk in await cp.list_checkpoints(run_id):
        for step in range(chk.step + 1):
            for attempt in (1, 2, 3):
                if await cp.get_outcome(run_id, step, node_id, attempt) is not None:
                    return True
    return False


async def test_select_node_ids_runs_target_defers_sibling():
    """From the {b, c} frontier, executing ONLY b (select_node_ids={'b'},
    stop_after_steps=1) records an outcome for b, NOT c, and c survives as a
    deferred frontier node; the next resume runs c and completes."""
    registry = _registry()
    graph = compile_graph(_fanout_definition(), registry=registry)
    cp = MemoryCheckpointer()
    sched = Scheduler(graph, cp, make_app_context(FakeEmitter()), registry=registry)

    # Get to the {b, c} frontier first.
    seed = _seed_at_entry("step-2", list(graph.entry_node_ids))
    await cp.save_checkpoint(seed)
    await sched.resume(run_id="step-2", checkpoint_id=seed.checkpoint_id, stop_after_steps=1)
    frontier = await _latest_checkpoint(cp, "step-2")
    assert {ni.node_id for ni in frontier.next_invocations} == {"b", "c"}

    # Execute ONLY b.
    r = await sched.resume(
        run_id="step-2",
        checkpoint_id=frontier.checkpoint_id,
        stop_after_steps=1,
        select_node_ids={"b"},
    )
    assert r.status is RunStatus.PAUSED
    assert await cp.get_outcome("step-2", frontier.step, "b", 1) is not None
    assert await cp.get_outcome("step-2", frontier.step, "c", 1) is None

    # c must still be pending in the new frontier (deferred, not lost).
    after_b = await _latest_checkpoint(cp, "step-2")
    assert "c" in {ni.node_id for ni in after_b.next_invocations}

    # Run the rest → c executes, run completes.
    r2 = await sched.resume(run_id="step-2", checkpoint_id=after_b.checkpoint_id)
    assert r2.status is RunStatus.COMPLETED
    assert await _any_outcome(cp, "step-2", "c")


async def test_stepping_final_node_completes_run():
    """Stepping the last node with an empty routed frontier yields COMPLETED."""
    registry = _registry()
    graph = compile_graph(_fanout_definition(), registry=registry)
    cp = MemoryCheckpointer()
    sched = Scheduler(graph, cp, make_app_context(FakeEmitter()), registry=registry)

    seed = _seed_at_entry("step-3", list(graph.entry_node_ids))
    await cp.save_checkpoint(seed)
    # Walk the whole graph one super-step at a time.
    current = seed.checkpoint_id
    status = None
    for _ in range(10):
        r = await sched.resume(run_id="step-3", checkpoint_id=current, stop_after_steps=1)
        status = r.status
        if status is RunStatus.COMPLETED:
            break
        current = (await _latest_checkpoint(cp, "step-3")).checkpoint_id
    assert status is RunStatus.COMPLETED


def test_resolve_invocation_inputs_merges_static_then_invocation():
    """The shared merge: authored static_inputs first, invocation payload on
    top (last-writer-wins) — the exact payload the scheduler validates."""

    class _Cfg(BaseModel):
        pass

    node = CompiledNode(
        node_id="n",
        spec_type="data.transform",
        config=_Cfg(),
        static_inputs={"topic": "authored", "keep": 1},
        incoming_edge_ids=(),
        outgoing_edge_ids=(),
        reads_channels=(),
        writes_channels=(),
    )
    merged = resolve_invocation_inputs(node, {"topic": "from_edge", "extra": 2})
    assert merged == {"topic": "from_edge", "keep": 1, "extra": 2}
    # Empty invocation → just the static inputs.
    assert resolve_invocation_inputs(node, {}) == {"topic": "authored", "keep": 1}
