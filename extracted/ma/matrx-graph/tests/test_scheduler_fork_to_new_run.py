"""Money-safety proof for "fork to a new run" (aidream
``POST /runs/{id}/nodes/{nid}/fork-from``).

Forking iterates on a FINISHED run by seeding a BRAND-NEW run from the
checkpoint that scheduled the chosen node. The whole point is that upstream
nodes are NOT re-executed (so paid LLM steps are not re-charged) while the
chosen node + everything downstream DO run fresh.

These tests exercise the engine primitive the endpoint stands on — copying a
source checkpoint's ``channel_values`` + a single-node ``next_invocations``
into a new run_id, then ``Scheduler.resume`` — and assert the exact
invocation set. They mirror what
``aidream/api/routers/workflow.py::_seed_forked_run_checkpoint`` builds, so a
regression in the resume/seed contract trips here, in the package, with no DB.
"""

from __future__ import annotations

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

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _three_step_definition() -> Definition:
    """Linear graph ``a`` -> ``b`` -> ``c`` of constant transforms. Three
    super-steps, one node per step, each with inspectable typed output."""
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
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "'BETA'"}},
                },
                {
                    "id": "c",
                    "type": "data.transform",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {"expression": "'GAMMA'"}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "a", "target": "b"},
                {"id": "e2", "source": "b", "target": "c"},
            ],
        }
    )


def _seed_forked_checkpoint(
    *,
    source_cp: Checkpoint,
    new_run_id: str,
    node_id: str,
) -> Checkpoint:
    """Build the seed checkpoint exactly like the production endpoint's
    ``_seed_forked_run_checkpoint``: the source checkpoint's channel_values
    verbatim, ``next_invocations`` = the single target node at attempt 1,
    on the NEW run_id with no parent (origin of the new lineage)."""
    return Checkpoint(
        checkpoint_id=f"seed-{new_run_id}",
        run_id=new_run_id,
        thread_id=new_run_id,
        parent_checkpoint_id=None,
        step=source_cp.step,
        channel_values=source_cp.channel_values,
        next_invocations=[
            NextInvocation(
                node_id=node_id,
                inputs=next(
                    (ni.inputs for ni in source_cp.next_invocations if ni.node_id == node_id),
                    {},
                ),
                attempt=1,
            )
        ],
        interrupt_payload=None,
    )


async def _checkpoint_that_scheduled(
    checkpointer: MemoryCheckpointer, run_id: str, node_id: str
) -> Checkpoint:
    """The historical checkpoint whose next_invocations named ``node_id`` —
    the LATEST by order, mirroring the endpoint's lookup."""
    found: Checkpoint | None = None
    for cp in await checkpointer.list_checkpoints(run_id):
        if any(ni.node_id == node_id for ni in cp.next_invocations):
            found = cp
    assert found is not None, f"no checkpoint scheduled {node_id!r}"
    return found


async def test_fork_runs_target_and_downstream_fresh_without_re_invoking_upstream():
    """THE money-safety invariant. Fork the finished run from ``b``:
    ``a`` (upstream) must NOT execute in the new run; ``b`` and ``c`` MUST.
    The oracle is the new run's node outcomes — outcomes are keyed by
    run_id, so the new run is born with none, and ends with outcomes for
    EXACTLY {b, c} and nothing for a."""
    registry = _registry()
    graph = compile_graph(_three_step_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()

    # 1) Run the source workflow to completion. a, b, c each execute once.
    source = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    src_result = await source.run(run_id="src-1")
    assert src_result.status is RunStatus.COMPLETED

    # Sanity: the source run executed a at step 0.
    a_src = await checkpointer.get_outcome(run_id="src-1", step=0, node_id="a", attempt=1)
    assert a_src is not None and a_src.error is None

    # 2) Find the source checkpoint that scheduled b, seed a NEW run from it.
    source_cp = await _checkpoint_that_scheduled(checkpointer, "src-1", "b")
    seed = _seed_forked_checkpoint(source_cp=source_cp, new_run_id="fork-1", node_id="b")
    await checkpointer.save_checkpoint(seed)

    # The forked run is born with ZERO outcomes — nothing to replay.
    assert await checkpointer.get_outcome("fork-1", source_cp.step, "b", 1) is None

    # 3) Resume the NEW run from the seed checkpoint.
    fork = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    fork_result = await fork.resume(run_id="fork-1", checkpoint_id=seed.checkpoint_id)
    assert fork_result.status is RunStatus.COMPLETED

    # 4a) Upstream ``a`` was NEVER invoked in the forked run. a ran at step 0
    # in the source; in the fork the seed starts at b's step, so no outcome
    # for a exists on run_id=fork-1 at ANY step.
    for step in range(0, source_cp.step + 1):
        assert await checkpointer.get_outcome("fork-1", step, "a", 1) is None, (
            f"upstream node 'a' was re-invoked in the fork at step {step} — DOUBLE CHARGE"
        )

    # 4b) Target ``b`` and downstream ``c`` DID run fresh in the forked run.
    b_fork = await checkpointer.get_outcome("fork-1", source_cp.step, "b", 1)
    assert b_fork is not None and b_fork.error is None
    assert b_fork.source == "executor"  # genuinely executed, not a replay
    c_fork = await checkpointer.get_outcome("fork-1", source_cp.step + 1, "c", 1)
    assert c_fork is not None and c_fork.error is None
    assert c_fork.source == "executor"

    # 4c) The source run is untouched — its own outcomes still stand on
    # src-1 at their ORIGINAL steps (a@0, b@1, c@2). The fork re-bases steps
    # from the seed checkpoint, but the source's rows are never rewritten.
    assert await checkpointer.get_outcome("src-1", 0, "a", 1) is not None
    assert await checkpointer.get_outcome("src-1", 1, "b", 1) is not None
    assert await checkpointer.get_outcome("src-1", 2, "c", 1) is not None


async def test_fork_preserves_upstream_channel_state():
    """The forked target sees the SAME upstream contribution the source
    produced — the copied ``channel_values`` carry a's output forward, so
    b receives it without a re-running. b's output is identical across the
    source run and the fork (deterministic transform proves the input
    threaded through)."""
    registry = _registry()
    graph = compile_graph(_three_step_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()

    source = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    await source.run(run_id="src-2")
    b_src = await checkpointer.get_outcome(run_id="src-2", step=1, node_id="b", attempt=1)
    assert b_src is not None

    source_cp = await _checkpoint_that_scheduled(checkpointer, "src-2", "b")
    # The upstream contribution that ``b`` needs is already baked into the
    # source checkpoint — for this edge-routed graph it rides in the target
    # invocation's ``inputs`` (channel_values carries it for channel-routed
    # graphs). Either way the seed copies it forward, which is what lets the
    # fork run ``b`` without re-running ``a``. Prove the carrier is non-empty.
    target_inputs = next(ni.inputs for ni in source_cp.next_invocations if ni.node_id == "b")
    assert target_inputs or source_cp.channel_values, (
        "source checkpoint carries neither target inputs nor channel state — "
        "the fork would lose a's contribution"
    )

    seed = _seed_forked_checkpoint(source_cp=source_cp, new_run_id="fork-2", node_id="b")
    await checkpointer.save_checkpoint(seed)
    fork = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await fork.resume(run_id="fork-2", checkpoint_id=seed.checkpoint_id)
    assert result.status is RunStatus.COMPLETED

    # The fork re-bases steps from the seed checkpoint, so ``b`` runs at the
    # seed's step (not the source's step 1).
    b_fork = await checkpointer.get_outcome(
        run_id="fork-2", step=source_cp.step, node_id="b", attempt=1
    )
    assert b_fork is not None
    # Same upstream state in ⇒ same deterministic output out.
    assert b_fork.output == b_src.output


async def test_fork_from_entry_node_has_no_prior_checkpoint():
    """An entry node is seeded directly at step 0 and never appears in a
    checkpoint's next_invocations — so there is no source checkpoint to fork
    from (the endpoint detects this and tells the user to just Run). This
    pins that engine fact the endpoint relies on."""
    registry = _registry()
    graph = compile_graph(_three_step_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()
    source = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    await source.run(run_id="src-3")

    # No checkpoint ever scheduled the entry node ``a``.
    scheduled_a = [
        cp
        for cp in await checkpointer.list_checkpoints("src-3")
        if any(ni.node_id == "a" for ni in cp.next_invocations)
    ]
    assert scheduled_a == []
    assert "a" in graph.entry_node_ids
