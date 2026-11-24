"""Durability levels and the re-runnable chain (L-SPEED round 6a, items 3 + Arman's flag).

* A read step (IDEMPOTENT, spends nothing) joins a chain like a PURE transform: the chain's rows
  land in ONE transaction instead of one save per step.
* ``durability="boundaries"`` (a workflow's ``metadata.durability`` or the caller's kwarg): inside a
  chain only the LAST checkpoint is written, carrying every outcome of the chain, so the per-step
  record stays whole. A step that fails mid-chain resumes from the checkpoint before the chain and
  ends with outputs identical to a clean run. Default ``every_step`` is today's behaviour.
"""

from __future__ import annotations

from typing import ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from tests._fixtures import FakeEmitter, make_app_context
from tests.test_scheduler_ready_nodes_do_not_wait import _edge, _node, _Sleeper

CHAIN = ("a", "b", "c", "d", "e")


class _Reader(_Sleeper):
    spec: ClassVar[NodeSpec] = _Sleeper.spec.model_copy(
        update={"node_type": "test.reader", "determinism": ActionTier.IDEMPOTENT, "spends": False}
    )


class _SideEffect(_Sleeper):
    spec: ClassVar[NodeSpec] = _Sleeper.spec.model_copy(
        update={"node_type": "test.side_effect", "determinism": ActionTier.SIDE_EFFECT}
    )


class _Shows(_Sleeper):
    """Show on Screen's shape: SIDE_EFFECT whose only effect is an emission (``emits_only``)."""

    spec: ClassVar[NodeSpec] = _Sleeper.spec.model_copy(
        update={"node_type": "test.shows", "determinism": ActionTier.SIDE_EFFECT, "emits_only": True, "spends": False}
    )


class _PaidTool(_Sleeper):
    """An IDEMPOTENT tool that declares nothing about spending (http.get, files.download …): it MAY spend."""

    spec: ClassVar[NodeSpec] = _Sleeper.spec.model_copy(
        update={"node_type": "test.paid_tool", "determinism": ActionTier.IDEMPOTENT, "category": NodeCategory.TOOL}
    )


class _Crash(BaseException):
    """The process dying while the chain's one transaction is in flight."""


class _CountingCheckpointer(MemoryCheckpointer):
    def __init__(self) -> None:
        super().__init__()
        self.transactions = 0
        self.crash_on_chain = False

    async def save_checkpoint(self, checkpoint):  # type: ignore[override]
        self.transactions += 1
        await super().save_checkpoint(checkpoint)

    async def save_checkpoint_with_outcomes(self, checkpoint, outcomes):  # type: ignore[override]
        self.transactions += 1
        await MemoryCheckpointer.save_checkpoint(self, checkpoint)
        for outcome in outcomes:
            await self.record_outcome(outcome)

    async def save_checkpoint_chain(self, items):  # type: ignore[override]
        if self.crash_on_chain:
            raise _Crash()
        self.transactions += 1
        for checkpoint, outcomes in items:
            await MemoryCheckpointer.save_checkpoint(self, checkpoint)
            for outcome in outcomes:
                await self.record_outcome(outcome)


def _definition(
    *,
    reader_at: str | None = None,
    side_effect_at: str | None = None,
    shows_at: str | None = None,
    durability: str | None = None,
) -> Definition:
    nodes = []
    for node_id in CHAIN:
        node = _node(node_id)
        if node_id == reader_at:
            node["type"] = "test.reader"
        if node_id == side_effect_at:
            node["type"] = "test.side_effect"
        if node_id == shows_at:
            node["type"] = "test.shows"
        nodes.append(node)
    return Definition.model_validate(
        {
            "nodes": nodes,
            "edges": [_edge(x, y) for x, y in zip(CHAIN, CHAIN[1:])],
            "entry_nodes": ["a"],
            "metadata": {"durability": durability} if durability else {},
        }
    )


def _scheduler(definition: Definition, sleeper: _Sleeper, checkpointer=None, side=None, **kwargs):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(sleeper)
    registry.register(_Reader())
    registry.register(side or _SideEffect())
    registry.register(_Shows())
    registry.register(_PaidTool())
    checkpointer = checkpointer or _CountingCheckpointer()
    graph = compile_graph(definition, registry=registry)
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry, **kwargs), checkpointer


async def _outcomes(checkpointer: MemoryCheckpointer) -> dict[str, object]:
    return {key[2]: o.output for key, o in checkpointer._outcomes.items() if o.error is None}


async def test_a_read_step_joins_the_chain() -> None:
    sched, cp = _scheduler(_definition(reader_at="c"), _Sleeper())
    assert (await sched.run(run_id="chain-reader")).status is RunStatus.COMPLETED
    # Five pure/idempotent steps: one chain transaction (+ the run's final save), never one per step.
    assert cp.transactions <= 2, cp.transactions


async def test_every_step_is_the_default_and_keeps_every_checkpoint() -> None:
    sched, cp = _scheduler(_definition(), _Sleeper())
    assert (await sched.run(run_id="every-step")).status is RunStatus.COMPLETED
    assert len(await cp.list_checkpoints("every-step")) >= len(CHAIN)


async def test_boundaries_writes_one_checkpoint_per_chain_and_every_outcome() -> None:
    clean, clean_cp = _scheduler(_definition(), _Sleeper())
    await clean.run(run_id="clean")
    sched, cp = _scheduler(_definition(durability="boundaries"), _Sleeper())
    result = await sched.run(run_id="bounded")
    assert result.status is RunStatus.COMPLETED
    assert len(await cp.list_checkpoints("bounded")) < len(await clean_cp.list_checkpoints("clean"))
    assert len(await cp.list_checkpoints("bounded")) <= 2
    assert await _outcomes(cp) == await _outcomes(clean_cp)
    # The caller's word outranks the workflow's.
    forced, forced_cp = _scheduler(_definition(durability="boundaries"), _Sleeper(), durability="every_step")
    await forced.run(run_id="forced")
    assert len(await forced_cp.list_checkpoints("forced")) == len(await clean_cp.list_checkpoints("clean"))


async def test_a_crash_mid_chain_resumes_from_the_boundary_to_identical_outputs() -> None:
    clean, _ = _scheduler(_definition(side_effect_at="a"), _Sleeper())
    expected = (await clean.run(run_id="clean-2")).last_outputs

    side = _SideEffect()
    sched, cp = _scheduler(_definition(side_effect_at="a", durability="boundaries"), _Sleeper(), side=side)
    cp.crash_on_chain = True
    try:
        await sched.run(run_id="bounded-crash")
    except _Crash:
        pass
    else:
        raise AssertionError("the chain's transaction never ran")
    latest = await cp.latest_checkpoint("bounded-crash")
    assert latest is not None and latest.step == 0, latest  # the side-effect step's boundary, nothing after

    cp.crash_on_chain = False
    sleeper = _Sleeper()
    again, _ = _scheduler(_definition(side_effect_at="a", durability="boundaries"), sleeper, checkpointer=cp, side=side)
    resumed = await again.resume(run_id="bounded-crash", checkpoint_id=latest.checkpoint_id)
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.last_outputs == expected
    assert side.runs == {"a": 1}, "the side-effect step ran again on resume"
    assert set(sleeper.runs) == {"b", "c", "d", "e"}  # the lost chain re-ran


async def test_a_step_that_only_emits_joins_the_chain_a_real_side_effect_does_not() -> None:
    shows, shows_cp = _scheduler(_definition(shows_at="c"), _Sleeper())
    assert (await shows.run(run_id="chain-shows")).status is RunStatus.COMPLETED
    side, side_cp = _scheduler(_definition(side_effect_at="c"), _Sleeper())
    assert (await side.run(run_id="chain-side")).status is RunStatus.COMPLETED
    assert shows_cp.transactions <= 2, shows_cp.transactions
    assert side_cp.transactions > shows_cp.transactions, (side_cp.transactions, shows_cp.transactions)


def test_show_on_screen_declares_it_only_emits() -> None:
    from matrx_graph.nodes.output.to_frontend import ToFrontendExecutor

    assert ToFrontendExecutor.spec.emits_only is True


async def test_a_step_that_may_spend_never_rides_a_chain() -> None:
    """2026-11-09 review: 17 IDEMPOTENT tool/custom steps the spend reader treats as spending joined the
    chain. Only a step that spends nothing (``NodeSpec.spends`` False, or a PURE data step) rides it."""
    reader, reader_cp = _scheduler(_definition(reader_at="c"), _Sleeper())
    await reader.run(run_id="chain-declared-read")
    d = _definition()
    d.nodes[2].type = "test.paid_tool"
    tool, tool_cp = _scheduler(d, _Sleeper())
    assert (await tool.run(run_id="chain-paid-tool")).status is RunStatus.COMPLETED
    assert tool_cp.transactions > reader_cp.transactions, (tool_cp.transactions, reader_cp.transactions)
