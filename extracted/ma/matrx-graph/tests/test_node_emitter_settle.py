"""A node's live frames land before its outcome — the node-emitter settle hook.

A host emitter may publish live frames off the critical path (enqueue, return,
a drain task does the I/O). The scheduler hands each invocation a scoped
emitter (``for_invocation``) but publishes ``node_completed`` / ``node_failed``
on the RUN-level emitter, so nothing ordered the outcome after the
invocation's queue: the last frames could reach the client after the node
ended, or after the run did. The scheduler now awaits an optional
``settle()`` on the invocation emitter after every attempt and before the
outcome event.

SUT: the real ``Scheduler``. Double: a host emitter whose scoped emitters
publish through a SLOW drain task (the shape aidream's ProgressTrackingEmitter
has), writing into one ordered wire shared with the run-level events.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import NodeCategory
from matrx_graph.types.result import success

from tests._fixtures import FakeEmitter, make_app_context

FRAMES = 12


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sent: int = 0


class _Wire:
    """The client's view: one ordered list of everything that reached it."""

    def __init__(self) -> None:
        self.log: list[tuple[str, Any]] = []


class _QueuedInvocationEmitter(FakeEmitter):
    """Publishes every chunk through a slow drain task, in order."""

    def __init__(self, wire: _Wire, node_id: str, *, settle_mode: str) -> None:
        super().__init__()
        self._wire = wire
        self._node_id = node_id
        self._queue: asyncio.Queue[str] = asyncio.Queue()
        self._task: asyncio.Task[None] | None = None
        self._settle_mode = settle_mode
        self.settled = 0

    async def _drain(self) -> None:
        while True:
            text = await self._queue.get()
            await asyncio.sleep(0.005)  # a round trip to a far database
            self._wire.log.append(("frame", (self._node_id, text)))
            self._queue.task_done()

    async def send_chunk(self, text: str) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._drain())
        self._queue.put_nowait(text)

    async def settle(self) -> None:
        self.settled += 1
        if self._settle_mode == "hang":
            await asyncio.sleep(3600)
        if self._settle_mode == "raise":
            raise RuntimeError("live wire unavailable")
        await self._queue.join()


class _HostEmitter(FakeEmitter):
    def __init__(self, wire: _Wire, *, settle_mode: str = "drain") -> None:
        super().__init__()
        self._wire = wire
        self._settle_mode = settle_mode
        self.scoped: list[_QueuedInvocationEmitter] = []

    def for_invocation(self, node_id: str, dispatch_id: str = "", item_index: int = 0, **_: Any):
        scoped = _QueuedInvocationEmitter(self._wire, node_id, settle_mode=self._settle_mode)
        self.scoped.append(scoped)
        return scoped

    async def send_data(self, payload: Any) -> None:
        if hasattr(payload, "model_dump"):
            payload = payload.model_dump(mode="json")
        self._wire.log.append(("event", payload))


class _Streamer:
    spec = NodeSpec(
        type="test.settle_streamer",
        category=NodeCategory.CUSTOM,
        display_name="Streamer",
        input_schema=_Open,
        output_schema=_Out,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
    )

    async def execute(self, ctx, inputs, config):  # noqa: ANN001
        for i in range(FRAMES):
            await ctx.app.emitter.send_chunk(f"{ctx.node_id}-{i}")
        if ctx.node_id == "breaks":
            raise ValueError("the step broke after streaming")
        return success(_Out(sent=FRAMES))


def _definition(node_ids: list[str]) -> Definition:
    return Definition.model_validate(
        {
            "version": "1",
            "nodes": [
                {
                    "id": nid,
                    "type": "test",
                    "position": {"x": 0, "y": 0},
                    "data": {"spec_type": "test.settle_streamer", "label": nid, "config": {}, "input": {}},
                }
                for nid in node_ids
            ],
            "edges": [
                {"id": f"e{i}", "source": a, "target": b}
                for i, (a, b) in enumerate(zip(node_ids, node_ids[1:], strict=False))
            ],
            "entry_nodes": [node_ids[0]],
            "metadata": {},
        }
    )


async def _run(host: _HostEmitter, node_ids: list[str], **sched_attrs: Any) -> Any:
    reg = register_builtin_nodes(NodeRegistry(), overwrite=True)
    reg.register(_Streamer(), overwrite=True)
    graph = compile_graph(_definition(node_ids), registry=reg)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(host), registry=reg)
    for name, value in sched_attrs.items():
        setattr(scheduler, name, value)
    return await scheduler.run(run_id="run-settle", inputs={})


def _position(log: list[tuple[str, Any]], event: str, node_id: str) -> int:
    for i, (kind, payload) in enumerate(log):
        if kind == "event" and payload.get("event") == event and payload.get("node_id") == node_id:
            return i
    raise AssertionError(f"no {event} for {node_id} on the wire")


def _frame_positions(log: list[tuple[str, Any]], node_id: str) -> list[int]:
    return [i for i, (kind, p) in enumerate(log) if kind == "frame" and p[0] == node_id]


def test_every_frame_lands_before_its_node_completed() -> None:
    wire = _Wire()
    result = asyncio.run(_run(_HostEmitter(wire), ["first", "second"]))
    assert result.status is RunStatus.COMPLETED, result.error
    for node_id in ("first", "second"):
        frames = _frame_positions(wire.log, node_id)
        assert len(frames) == FRAMES, f"{node_id}: {len(frames)}/{FRAMES} frames reached the wire"
        done = _position(wire.log, "node_completed", node_id)
        assert max(frames) < done, (
            f"{node_id}'s last live frame reached the client AFTER its node_completed"
        )


def test_a_failing_node_lands_its_frames_before_node_failed() -> None:
    wire = _Wire()
    result = asyncio.run(_run(_HostEmitter(wire), ["breaks"]))
    assert result.status is not RunStatus.COMPLETED
    frames = _frame_positions(wire.log, "breaks")
    assert len(frames) == FRAMES
    assert max(frames) < _position(wire.log, "node_failed", "breaks")


def test_an_emitter_without_settle_is_untouched() -> None:
    """The console/standalone emitter has no settle — runs exactly as before."""
    emitter = FakeEmitter()
    reg = register_builtin_nodes(NodeRegistry(), overwrite=True)
    reg.register(_Streamer(), overwrite=True)
    graph = compile_graph(_definition(["solo"]), registry=reg)

    async def go() -> Any:
        return await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=reg).run(
            run_id="run-bare", inputs={}
        )

    result = asyncio.run(go())
    assert result.status is RunStatus.COMPLETED, result.error
    assert [t for k, t in emitter.events if k == "chunk"] == [f"solo-{i}" for i in range(FRAMES)]


def test_a_hanging_settle_is_cut_off_loudly_and_the_run_finishes(caplog: pytest.LogCaptureFixture) -> None:
    wire = _Wire()
    host = _HostEmitter(wire, settle_mode="hang")
    with caplog.at_level(logging.ERROR, logger="matrx_graph.executor.scheduler"):
        result = asyncio.run(
            asyncio.wait_for(_run(host, ["first"], node_emitter_settle_timeout_s=0.05), timeout=10)
        )
    assert result.status is RunStatus.COMPLETED, result.error
    assert host.scoped and host.scoped[0].settled == 1
    assert any("did not settle" in r.getMessage() for r in caplog.records)


def test_a_raising_settle_never_fails_the_run() -> None:
    wire = _Wire()
    host = _HostEmitter(wire, settle_mode="raise")
    result = asyncio.run(_run(host, ["first"]))
    assert result.status is RunStatus.COMPLETED, result.error
    assert host.scoped[0].settled == 1
