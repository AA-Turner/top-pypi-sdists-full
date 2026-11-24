"""A run's spend reader is asked only after a step that may spend ran (L-SPEED round 6a, item 4).

Before: a mandate's per-run spend limit lived inside its ``control_check``, so EVERY super-step
boundary walked the run tree's cost ledger, and the cheap own-row status read was turned off for
the whole run. Now the limit is the Scheduler's ``spend_check``: a stretch of data steps never asks
it; a step that may spend (``spend_gate.may_spend`` — anything but data / control / in-out / info)
makes the NEXT boundary ask once; a True answer stops the run the same graceful way as a Cancel.
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
from matrx_graph.spend_gate import may_spend
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import NodeCategory
from tests._fixtures import FakeEmitter, make_app_context
from tests.test_scheduler_ready_nodes_do_not_wait import _edge, _node, _Sleeper


class _PaidSleeper(_Sleeper):
    spec: ClassVar[NodeSpec] = _Sleeper.spec.model_copy(
        update={"node_type": "test.paid_sleeper", "category": NodeCategory.TOOL}
    )


def _chain(paid_at: str | None) -> Definition:
    nodes = []
    for node_id in ("a", "b", "c", "d"):
        node = _node(node_id)
        if node_id == paid_at:
            node["type"] = "test.paid_sleeper"
        nodes.append(node)
    return Definition.model_validate(
        {
            "nodes": nodes,
            "edges": [_edge("a", "b"), _edge("b", "c"), _edge("c", "d")],
            "entry_nodes": ["a"],
        }
    )


def _run_with(paid_at: str | None, reached: bool) -> tuple[Scheduler, _Sleeper, _Sleeper, list[int]]:
    asks: list[int] = []

    async def spend_check() -> bool:
        asks.append(1)
        return reached

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    sleeper, paid = _Sleeper(), _PaidSleeper()
    registry.register(sleeper)
    registry.register(paid)
    graph = compile_graph(_chain(paid_at), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry,
        spend_check=spend_check,
    )
    return scheduler, sleeper, paid, asks


def test_only_data_control_io_and_info_steps_never_spend() -> None:
    free = {NodeCategory.DATA, NodeCategory.CONTROL, NodeCategory.IO, NodeCategory.INFO}
    for category in NodeCategory:
        spec = _Sleeper.spec.model_copy(update={"category": category})
        assert may_spend(spec) is (category not in free), category


async def test_a_run_of_data_steps_never_reads_its_spend() -> None:
    scheduler, sleeper, _paid, asks = _run_with(None, reached=True)
    result = await scheduler.run(run_id="spend-data-only")
    assert result.status is RunStatus.COMPLETED
    assert set(sleeper.runs) == {"a", "b", "c", "d"}
    assert asks == [], f"the spend reader was asked {len(asks)} times in a data-only run"


async def test_a_step_that_may_spend_is_followed_by_one_read_that_can_stop_the_run() -> None:
    scheduler, sleeper, paid, asks = _run_with("b", reached=True)
    result = await scheduler.run(run_id="spend-after-paid")
    assert result.status is RunStatus.CANCELLED
    assert paid.runs == {"b": 1}
    assert asks == [1], f"asked {len(asks)} times; once, after the paid step"
    assert "c" not in sleeper.runs and "d" not in sleeper.runs, sleeper.runs


async def test_a_reader_under_its_limit_lets_the_run_finish_and_is_asked_once() -> None:
    scheduler, sleeper, paid, asks = _run_with("b", reached=False)
    result = await scheduler.run(run_id="spend-under-limit")
    assert result.status is RunStatus.COMPLETED
    assert set(sleeper.runs) == {"a", "c", "d"} and paid.runs == {"b": 1}
    assert asks == [1], f"asked {len(asks)} times; once, after the paid step"


def test_category_alone_is_no_sign_of_spending() -> None:
    """search.decide is DATA and runs an agent; an IDEMPOTENT tool may call a paid API."""
    from matrx_graph.types.primitives import ActionTier

    assert may_spend(_Sleeper.spec.model_copy(update={"spends": True}))  # declared: DATA but paid
    assert may_spend(_Sleeper.spec.model_copy(update={"determinism": ActionTier.IDEMPOTENT}))  # undeclared read
    assert not may_spend(_Sleeper.spec.model_copy(update={"determinism": ActionTier.IDEMPOTENT, "spends": False}))
    assert not may_spend(_Sleeper.spec)  # PURE data transform
