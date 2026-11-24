"""A work queue's ``done`` releases downstream ONCE, at drain — never per wave.

Live failure (knowledge buckets run 40a1144a, 2026-10-31): the definition wired
``go → seed → drain``, ``drain(done) → wait_for_units → spread_read`` (control)
and ``go → spread_read`` (data). Every non-final wave of ``control.work_queue``
did not emit ``done``; the engine resolved that edge as PRUNED ("branch not
taken"), the prune propagated through ``wait_for_units``, and ``spread_read`` —
holding go's delivery plus a pruned gate — FIRED after wave 1, 6,500 items
early. Its second firing then waited for a ``go`` delivery that could never
come again, and the first resume (a deploy) was refused by the pre-flight:
"step 'spread_read' needs input from 'go', which will not run again".

A firing that Sends ITSELF a continuation has not finished: its un-emitted
handles are NOT a branch not taken, and stay unresolved until the firing that
does not continue. These tests drive the real Scheduler through a drain and
through a hard kill + fresh-scheduler resume mid-drain.
"""

from __future__ import annotations

import asyncio
from typing import ClassVar
from uuid import uuid4

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    MemoryWorkSetStore,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    configure_work_set_store,
    register_builtin_nodes,
)
from matrx_graph.executor.resume_preflight import resume_preflight_problems
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.workset import get_work_set_store
from tests._fixtures import FakeEmitter, make_app_context

ITEMS = ["a", "b", "c", "d", "e", "f"]


@pytest.fixture(autouse=True)
def _fresh_store():
    configure_work_set_store(MemoryWorkSetStore())
    yield
    configure_work_set_store(None)


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _spec(type_: str) -> NodeSpec:
    return NodeSpec(
        type=type_,
        category=NodeCategory.DATA,
        display_name=type_,
        description=type_,
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )


class _Worker:
    """One item; can hold item 'c' open so the test can kill mid-drain."""

    spec: ClassVar[NodeSpec] = _spec("test.dq_worker")

    def __init__(self) -> None:
        self.done: list[str] = []
        self.block_c = False
        self.holding_c = asyncio.Event()
        self.release_c = asyncio.Event()

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _AnyIO, _c: _NoConfig
    ) -> NodeResult[_AnyIO]:
        key = inputs.model_dump(mode="json")["value"]["key"]
        if key == "c" and self.block_c:
            self.holding_c.set()
            await self.release_c.wait()
        self.done.append(key)
        return success(_AnyIO(key=key))


class _Join:
    """The ``spread_read`` stand-in: records when it fires and what it got."""

    spec: ClassVar[NodeSpec] = _spec("test.dq_join")

    def __init__(self, worker: _Worker) -> None:
        self.worker = worker
        self.firings: list[dict[str, object]] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _AnyIO, _c: _NoConfig
    ) -> NodeResult[_AnyIO]:
        self.firings.append(
            {"processed_before": sorted(self.worker.done), "inputs": inputs.model_dump(mode="json")}
        )
        return success(_AnyIO(ok=True))


class _Echo:
    spec: ClassVar[NodeSpec] = _spec("test.dq_echo")

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _AnyIO, _c: _NoConfig
    ) -> NodeResult[_AnyIO]:
        return success(_AnyIO(**inputs.model_dump(mode="json")))


def _node(nid: str, type_: str, config: dict | None = None, inp: dict | None = None) -> dict:
    data: dict = {"config": config or {}}
    if inp is not None:
        data["input"] = inp
    return {"id": nid, "type": type_, "position": {"x": 0, "y": 0}, "data": data}


def _edge(eid: str, src: str, tgt: str, kind: str = "data", handle: str | None = None, **data) -> dict:
    edge: dict = {"id": eid, "source": src, "target": tgt, "data": {"kind": kind, **data}}
    if handle:
        edge["sourceHandle"] = handle
    return edge


def _definition() -> Definition:
    """The knowledge-buckets v35 shape, in miniature."""
    return Definition.model_validate(
        {
            "nodes": [
                _node("go", "test.dq_echo", inp={"handed_on": "from-go"}),
                _node(
                    "seed",
                    "control.work_seed",
                    {"key_template": "$item.key"},
                    {"items": [{"key": k} for k in ITEMS]},
                ),
                _node("drain", "control.work_queue", {"target_node_id": "ingest", "batch_size": 2}),
                {**_node("ingest", "test.dq_worker"), "data": {"config": {}, "on_item_failure": "hole"}},
                _node("wait_for_units", "test.dq_echo"),
                _node("spread_read", "test.dq_join"),
            ],
            "edges": [
                _edge("e_go_seed", "go", "seed", "control"),
                _edge("e_seed_drain", "seed", "drain", "control"),
                _edge("e_drain_wait", "drain", "wait_for_units", "control", handle="done"),
                _edge("e_wait_spread", "wait_for_units", "spread_read", "control"),
                _edge(
                    "e_go_spread",
                    "go",
                    "spread_read",
                    "data",
                    mappings={"handed_on": "handed_on"},
                ),
            ],
            "entry_nodes": ["go"],
        }
    )


def _registry(worker: _Worker, join: _Join) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for executor in (worker, join, _Echo()):
        reg.register(executor, overwrite=True)
    return reg


def _assert_joined_once_after_drain(join: _Join) -> None:
    assert len(join.firings) == 1, join.firings
    [firing] = join.firings
    assert firing["processed_before"] == sorted(ITEMS), (
        "spread_read fired before the queue drained — the per-wave un-emitted "
        f"'done' was treated as a branch not taken: {firing}"
    )
    assert firing["inputs"].get("handed_on") == "from-go", firing


async def test_done_waits_for_the_whole_drain():
    worker = _Worker()
    join = _Join(worker)
    registry = _registry(worker, join)
    scheduler = Scheduler(
        compile_graph(_definition(), registry=registry),
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id=str(uuid4()), max_steps=200)
    assert result.status is RunStatus.COMPLETED, result.error
    _assert_joined_once_after_drain(join)


async def test_a_kill_mid_drain_resumes_and_finishes_the_drain():
    worker = _Worker()
    worker.block_c = True
    join = _Join(worker)
    registry = _registry(worker, join)
    graph = compile_graph(_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()
    run_id = str(uuid4())

    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    task = asyncio.create_task(scheduler.run(run_id=run_id, max_steps=200))
    await asyncio.wait_for(worker.holding_c.wait(), timeout=600)
    # Die only once the in-flight wave has claimed the rest of the set (the
    # queue fires beside the held worker in the same super-step). Cancelling
    # the instant the worker blocks races the queue's firing: if the cancel
    # lands first there is nothing for the resumed wave to release, and the
    # claim-release guards that drive this scenario see no release at all.
    async def _rest_claimed() -> None:
        while (await get_work_set_store().counts(run_id, "default")).pending:
            await asyncio.sleep(0)

    await asyncio.wait_for(_rest_claimed(), timeout=60)
    task.cancel()  # the deploy: the process dies mid-drain
    with pytest.raises(asyncio.CancelledError):
        await task

    assert join.firings == [], "spread_read fired while the queue was still draining"
    latest = await checkpointer.latest_checkpoint(run_id)
    assert latest is not None
    cp = await checkpointer.load_checkpoint(latest.checkpoint_id)
    assert resume_preflight_problems(graph, cp, registry) == []

    worker.block_c = False
    worker.release_c.set()
    fresh = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    resumed = await fresh.resume(run_id=run_id, checkpoint_id=latest.checkpoint_id, max_steps=200)
    assert resumed.status is RunStatus.COMPLETED, resumed.error

    counts = await get_work_set_store().counts(run_id, "default")
    assert counts.succeeded == len(ITEMS) and counts.drained, counts
    # Finished items were skipped on resume: nothing ran twice.
    assert sorted(worker.done) == sorted(ITEMS), worker.done
    _assert_joined_once_after_drain(join)
