"""THE STEP WALL CLOCK — a node that declares no timeout is still bounded.

🚨 THE CLASS THIS GUARDS. ``NodeSpec.timeout_ms`` has existed since Phase 1.2 and
NO shipped node spec sets it, so until 2026-09-15 every agent, AI and tool step
in this engine ran with no clock at all — the scheduler's ``else`` branch was a
bare ``await executor.execute(...)``.

What that cost, measured live: Masterwork run
``e991e70e-4c2f-4444-8c9f-e107888da36a`` (arm C of the Gio Valiante bench trial)
reached step 9 of 12 and then held node ``chief`` for **18 minutes 52 seconds**
(``workflow.node_outcome.duration_ms = 1132252``) on ONE Anthropic call that
reported ``api_duration_ms = 1,087,650`` (``chat.request 401262dc``). The same
node finished in ~82s on two interactive runs of the identical Masterwork
minutes earlier. The provider stream stalled mid-answer with the connection
still open, so every read-level timeout in the stack kept resetting — only a
WALL CLOCK over the whole step catches that shape.

THE FORCING LEG is ``test_step_that_never_returns_fails_within_the_bound``: its
executor awaits an ``asyncio.Event`` nobody ever sets — the shape of a provider
call that never comes back. On the pre-fix scheduler that test does not fail,
it HANGS for ever (pytest's own timeout kills the session), which is precisely
the defect stated as a test.
"""

from __future__ import annotations

import asyncio
from typing import ClassVar

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
from matrx_graph import knobs as graph_knobs
from matrx_graph.errors import NodeTimeoutError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class WedgedInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class WedgedOutput(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: str = "ok"


class WedgedConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


#: Set by the test body so the wedged executor can prove it was CANCELLED rather
#: than merely abandoned — a step left running behind a timeout still holds the
#: provider connection this fix exists to release.
_cancelled = asyncio.Event()


class NeverReturnsExecutor:
    """A step whose provider call never comes back.

    NOTE the spec: ``timeout_ms`` is **not set** — this is an ordinary node,
    exactly like every AI, agent and tool node the platform actually ships.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.never_returns",
        category=NodeCategory.DATA,
        display_name="A step whose provider never answers",
        description="Awaits an event nobody sets.",
        input_schema=WedgedInput,
        output_schema=WedgedOutput,
        config_schema=WedgedConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: WedgedInput,
        config: WedgedConfig,
    ) -> NodeResult[WedgedOutput]:
        try:
            await asyncio.Event().wait()  # the hung provider call
        except asyncio.CancelledError:
            _cancelled.set()
            raise
        return success(WedgedOutput())


class QuickExecutor:
    """An ordinary, healthy step that declares no timeout either."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.quick",
        category=NodeCategory.DATA,
        display_name="A healthy step",
        description="Returns immediately.",
        input_schema=WedgedInput,
        output_schema=WedgedOutput,
        config_schema=WedgedConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: WedgedInput,
        config: WedgedConfig,
    ) -> NodeResult[WedgedOutput]:
        await asyncio.sleep(0.01)
        return success(WedgedOutput(result="healthy"))


def _registry(executor: object) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(executor, overwrite=True)
    return reg


def _definition(node_type: str) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "chief",
                    "type": node_type,
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                }
            ],
            "edges": [],
        }
    )


def _events_of_kind(emitter: FakeEmitter, event: str) -> list[dict]:
    return [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == event
    ]


@pytest.fixture(autouse=True)
def _clean_knob_cache():
    graph_knobs.clear_knob_cache()
    yield
    graph_knobs.clear_knob_cache()


def _pin_ceiling(monkeypatch: pytest.MonkeyPatch, seconds: int) -> None:
    """Pin the platform ceiling for the test. The knob is read live in prod;
    here we prove the MECHANISM, at a duration a test can wait for."""

    async def _values(feature: str):
        if feature == graph_knobs.STEP_CLOCK_FEATURE:
            return {graph_knobs.DEFAULT_STEP_SECONDS_KEY: seconds}
        return None

    monkeypatch.setattr(graph_knobs, "_feature_values", _values)


async def test_step_that_never_returns_fails_within_the_bound(
    monkeypatch: pytest.MonkeyPatch,
):
    """🚨 THE FORCING LEG. A provider call that never returns must not hang the
    run: within the bound the step fails, by name, with a reason and a remedy,
    the coroutine is CANCELLED (the connection is released), and the run reaches
    a terminal-and-resumable state instead of sitting there looking busy."""
    _cancelled.clear()
    _pin_ceiling(monkeypatch, 1)
    registry = _registry(NeverReturnsExecutor())
    graph = compile_graph(_definition("test.never_returns"), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)

    started = asyncio.get_running_loop().time()
    # On the pre-fix scheduler this never returns and the wait_for below is what
    # turns "hangs for ever" into a failing test rather than a hung suite.
    result = await asyncio.wait_for(scheduler.run(run_id="wall-clock-forcing"), timeout=30)
    elapsed = asyncio.get_running_loop().time() - started

    assert result.status is RunStatus.ERRORED
    assert elapsed < 15, f"the bound did not hold: the step ran {elapsed:.1f}s"

    failed = _events_of_kind(emitter, "node_failed")
    assert len(failed) == 1, failed
    assert failed[0]["error_type"] == "NodeTimeoutError"
    message = failed[0]["error_message"]
    # NAMED, not a shrug: the step, the ceiling, and what to do about it.
    assert "chief" in message
    assert "time limit every step gets" in message
    assert "workflow.step_clock.default_step_seconds" in message

    # The hung coroutine is cancelled, not orphaned — otherwise the provider
    # connection this whole fix exists to release stays held.
    await asyncio.wait_for(_cancelled.wait(), timeout=5)


async def test_a_healthy_step_is_untouched_by_the_ceiling(
    monkeypatch: pytest.MonkeyPatch,
):
    """The clock bounds a stall; it must never fail ordinary work."""
    _pin_ceiling(monkeypatch, 600)
    registry = _registry(QuickExecutor())
    graph = compile_graph(_definition("test.quick"), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="wall-clock-healthy")
    assert result.status is RunStatus.COMPLETED
    assert _events_of_kind(emitter, "node_failed") == []


async def test_an_unreadable_knob_still_bounds_the_step(
    monkeypatch: pytest.MonkeyPatch,
):
    """🚨 A knob that cannot be read degrades to the recorded ceiling — LOUDLY —
    and never back to 'no ceiling'. "The row was missing" must not be a way to
    reopen the class this closes."""

    async def _unreadable(feature: str):
        return None

    monkeypatch.setattr(graph_knobs, "_feature_values", _unreadable)
    seconds, source = await graph_knobs.step_timeout_seconds(None)
    assert seconds == float(graph_knobs.STARTING_DEFAULT_STEP_SECONDS)
    assert source == "platform"


async def test_a_zero_or_negative_row_is_refused(monkeypatch: pytest.MonkeyPatch):
    """A ceiling of 0 IS 'no ceiling'. The row is clamped to the floor instead."""

    async def _values(feature: str):
        return {graph_knobs.DEFAULT_STEP_SECONDS_KEY: 0}

    monkeypatch.setattr(graph_knobs, "_feature_values", _values)
    seconds, _ = await graph_knobs.step_timeout_seconds(None)
    assert seconds == float(graph_knobs.MIN_STEP_SECONDS)


async def test_a_declared_node_timeout_still_wins(monkeypatch: pytest.MonkeyPatch):
    """An author who set a limit on their own step keeps it, and the failure
    says so — the two have different remedies."""
    _pin_ceiling(monkeypatch, 600)
    seconds, source = await graph_knobs.step_timeout_seconds(50)
    assert seconds == 0.05
    assert source == "declared"


def test_the_run_error_a_person_reads_names_the_step_and_the_remedy():
    """🚨 NOTHING FAILS SILENTLY. What reaches the durable-run client is
    ``workflow.run.error.message``. Derived from the cause alone that sentence is
    "This step ran past its time limit and was stopped." — true, and a shrug: no
    step, no ceiling, no remedy. The exception knows all three, so the failure
    builder believes it."""
    from matrx_graph.failure import Cause, failure_from_exception

    failure = failure_from_exception(NodeTimeoutError("chief", 600_000, 1, source="platform"))
    assert failure.cause == Cause.TIMED_OUT
    assert failure.step_id == "chief"
    assert "chief" in failure.message
    assert "600s" in failure.message
    assert "workflow.step_clock.default_step_seconds" in failure.message


# ── A STEP MAY DECLARE ITS OWN, LONGER, CLOCK ────────────────────────────────
#
# Live kit build 3aa2c3a6 (2026-10-11): the audio-overview step — a podcast
# produced end to end, honestly ~10-20 minutes — was stopped at the platform's
# 600s. Raising the platform default would loosen every other step; instead ONE
# node of ONE definition declares its own limit (``data.step_clock``), knob-backed
# so an admin turns it, and every undeclared node keeps the platform ceiling.


class SlowExecutor:
    """A healthy step that simply takes longer than the platform ceiling."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.slow",
        category=NodeCategory.DATA,
        display_name="A long, healthy step",
        description="Sleeps past the (clamped, 5s) test ceiling, then answers.",
        input_schema=WedgedInput,
        output_schema=WedgedOutput,
        config_schema=WedgedConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: WedgedInput,
        config: WedgedConfig,
    ) -> NodeResult[WedgedOutput]:
        await asyncio.sleep(graph_knobs.MIN_STEP_SECONDS + 1.5)
        return success(WedgedOutput(result="long"))


def _slow_definition(step_clock: dict | None) -> Definition:
    data: dict = {"config": {}}
    if step_clock is not None:
        data["step_clock"] = step_clock
    return Definition.model_validate(
        {
            "nodes": [{"id": "audio", "type": "test.slow", "position": {"x": 0, "y": 0}, "data": data}],
            "edges": [],
        }
    )


async def _run_slow(step_clock: dict | None, run_id: str) -> tuple[RunStatus, FakeEmitter]:
    registry = _registry(SlowExecutor())
    graph = compile_graph(_slow_definition(step_clock), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await asyncio.wait_for(scheduler.run(run_id=run_id), timeout=30)
    return result.status, emitter


async def test_a_step_declaring_a_longer_clock_is_not_cut_off_at_the_platform_ceiling(
    monkeypatch: pytest.MonkeyPatch,
):
    _pin_ceiling(monkeypatch, 1)  # clamped to MIN_STEP_SECONDS: the scaled-down "600s"
    status, emitter = await _run_slow({"seconds": 20}, "declared-longer")
    assert status is RunStatus.COMPLETED, _events_of_kind(emitter, "node_failed")


async def test_an_undeclared_step_is_still_cut_off_at_the_platform_ceiling(
    monkeypatch: pytest.MonkeyPatch,
):
    _pin_ceiling(monkeypatch, 1)
    status, emitter = await _run_slow(None, "undeclared")
    assert status is RunStatus.ERRORED
    (failed,) = _events_of_kind(emitter, "node_failed")
    assert failed["error_type"] == "NodeTimeoutError"


async def test_a_declared_clock_reads_its_knob_and_falls_back_to_its_seconds(
    monkeypatch: pytest.MonkeyPatch,
):
    """The declared limit is a KNOB: the row wins; an unreadable row falls back
    to the declared starting seconds (never to the platform ceiling, never to
    no ceiling)."""

    async def _values(feature: str):
        if feature == graph_knobs.STEP_CLOCK_FEATURE:
            return {graph_knobs.DEFAULT_STEP_SECONDS_KEY: 1}
        if feature == "education.study_kit":
            return {"audio_step_seconds": 20}
        return None

    monkeypatch.setattr(graph_knobs, "_feature_values", _values)
    clock = {"seconds": 6, "knob": {"feature": "education.study_kit", "key": "audio_step_seconds"}}
    status, emitter = await _run_slow(clock, "declared-knob")
    assert status is RunStatus.COMPLETED, _events_of_kind(emitter, "node_failed")

    async def _no_row(feature: str):
        if feature == graph_knobs.STEP_CLOCK_FEATURE:
            return {graph_knobs.DEFAULT_STEP_SECONDS_KEY: 1}
        return {}

    monkeypatch.setattr(graph_knobs, "_feature_values", _no_row)
    graph_knobs.clear_knob_cache()
    seconds, source = await graph_knobs.step_timeout_seconds(
        None, node_clock=compile_graph(_slow_definition(clock), registry=_registry(SlowExecutor())).nodes["audio"].step_clock
    )
    assert (seconds, source) == (6.0, "declared")


def test_a_malformed_step_clock_fails_compilation():
    from matrx_graph.errors import CompilationError

    with pytest.raises(CompilationError):
        compile_graph(_slow_definition({"seconds": 0}), registry=_registry(SlowExecutor()))
