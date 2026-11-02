"""Phase 1.2 — per-node timeout enforcement.

NodeSpec.timeout_ms wraps the executor in asyncio.wait_for. On timeout
the scheduler raises NodeTimeoutError, which the RetryPolicy treats like
any other exception (retryable if listed in retry_on or retry_on empty).

Verifies:
    1. timeout_ms=None inherits the PLATFORM step ceiling (workflow.step_clock),
       which is wide enough that healthy nodes complete untouched.
    2. Slow node times out → NodeTimeoutError surfaces as node_failed +
       run_errored.
    3. Timeout + retry policy retries on NodeTimeoutError when retry_on
       includes it.
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
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import (
    ActionTier,
    BackoffStrategy,
    NodeCategory,
    RetryPolicy,
)
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class SlowInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class SlowOutput(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: str = "ok"


class SlowConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


_attempts_seen: list[int] = []


def _build_slow_executor(
    *,
    sleep_seconds: float,
    timeout_ms: int | None,
    retry_policy: RetryPolicy = RetryPolicy(),
    succeed_on_attempt: int | None = None,
) -> type:
    """Build an executor that sleeps for `sleep_seconds` before returning.

    If `succeed_on_attempt` is set, the executor returns immediately (no sleep)
    starting on that attempt — useful for retry+timeout combination tests.
    """

    class SlowExecutor:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type="test.slow",
            category=NodeCategory.DATA,
            display_name="Slow Test Node",
            description="Sleeps before returning to exercise timeout.",
            input_schema=SlowInput,
            output_schema=SlowOutput,
            config_schema=SlowConfig,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.IDEMPOTENT,
            retry=retry_policy,
            timeout_ms=timeout_ms,
        )

        async def execute(
            self,
            ctx: NodeExecutionContext,
            inputs: SlowInput,
            config: SlowConfig,
        ) -> NodeResult[SlowOutput]:
            _attempts_seen.append(ctx.attempt)
            if succeed_on_attempt is not None and ctx.attempt >= succeed_on_attempt:
                return success(SlowOutput(result=f"ok-attempt-{ctx.attempt}"))
            await asyncio.sleep(sleep_seconds)
            return success(SlowOutput(result=f"slept-attempt-{ctx.attempt}"))

    return SlowExecutor


def _slow_registry(executor_cls: type) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(executor_cls(), overwrite=True)
    return reg


def _single_slow_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "s",
                    "type": "test.slow",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
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


async def test_timeout_none_falls_back_to_the_platform_ceiling():
    """timeout_ms=None no longer means NO clock (that class closed 2026-09-15 —
    see tests/test_scheduler_step_wall_clock.py). It means the node inherits the
    platform ceiling, which is wide enough that ordinary work completes."""
    _attempts_seen.clear()
    slow = _build_slow_executor(sleep_seconds=0.05, timeout_ms=None)
    registry = _slow_registry(slow)
    graph = compile_graph(_single_slow_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="timeout-none")
    assert result.status is RunStatus.COMPLETED
    assert _attempts_seen == [1]


async def test_timeout_fires_and_parks_run_as_errored():
    """timeout_ms=50, sleep=1s, no retry → run ERRORED with NodeTimeoutError."""
    _attempts_seen.clear()
    slow = _build_slow_executor(sleep_seconds=1.0, timeout_ms=50)
    registry = _slow_registry(slow)
    graph = compile_graph(_single_slow_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="timeout-fires")
    assert result.status is RunStatus.ERRORED
    failed = _events_of_kind(emitter, "node_failed")
    assert len(failed) == 1
    assert failed[0]["error_type"] == "NodeTimeoutError"
    assert "50ms" in failed[0]["error_message"]


async def test_timeout_with_retry_succeeds_on_second_attempt():
    """timeout_ms=50, sleep=1s on attempt 1, instant on attempt 2 — with
    retry policy that includes NodeTimeoutError, run COMPLETES."""
    _attempts_seen.clear()
    policy = RetryPolicy(
        max_attempts=3,
        backoff=BackoffStrategy.NONE,
        retry_on=("NodeTimeoutError",),
    )
    slow = _build_slow_executor(
        sleep_seconds=1.0,
        timeout_ms=50,
        retry_policy=policy,
        succeed_on_attempt=2,
    )
    registry = _slow_registry(slow)
    graph = compile_graph(_single_slow_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="timeout-retry")
    assert result.status is RunStatus.COMPLETED
    assert _attempts_seen == [1, 2]
    retries = _events_of_kind(emitter, "node_retry_scheduled")
    assert len(retries) == 1
    assert retries[0]["error_type"] == "NodeTimeoutError"
    completed = _events_of_kind(emitter, "node_completed")
    assert completed[0]["output"]["result"] == "ok-attempt-2"


async def test_timeout_excluded_from_retry_on_short_circuits():
    """retry_on=('ValueError',) excludes timeouts — the timeout is NOT retried."""
    _attempts_seen.clear()
    policy = RetryPolicy(
        max_attempts=5,
        backoff=BackoffStrategy.NONE,
        retry_on=("ValueError",),
    )
    slow = _build_slow_executor(
        sleep_seconds=1.0,
        timeout_ms=50,
        retry_policy=policy,
    )
    registry = _slow_registry(slow)
    graph = compile_graph(_single_slow_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="timeout-no-retry-class")
    assert result.status is RunStatus.ERRORED
    # NodeTimeoutError not in retry_on → no retries.
    assert _attempts_seen == [1]
    assert len(_events_of_kind(emitter, "node_retry_scheduled")) == 0
