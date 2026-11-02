"""Phase 1.1 — RetryPolicy enforcement in the scheduler.

Today's recovery API bumps attempts externally. These tests cover the new
in-line retry path: when a node's RetryPolicy has remaining attempts AND
the raised exception is retryable, the scheduler sleeps + re-executes
within the same super-step, emitting NodeRetryScheduledEvent between
attempts. The run STAYS in RUNNING; it does not park as ERRORED until
retries are exhausted.

Verifies:
    1. No retries when max_attempts=1 (preserves current behavior).
    2. Success on attempt 2 emits exactly one node_retry_scheduled + one
       node_completed.
    3. Final failure after N attempts emits N-1 retries + one node_failed
       + parks the run as ERRORED.
    4. `retry_on` whitelist: ValueError NOT retried when only HTTPError
       is in retry_on.
    5. Crash-and-resume walks past historic retry-attempts without re-
       paying the backoff sleep.
"""

from __future__ import annotations

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


# ---------------------------------------------------------------------------
# Fixtures: a flaky test node that fails the first N attempts then succeeds,
# plus an always-failing variant for exhaustion tests.
# ---------------------------------------------------------------------------


class FlakyInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class FlakyOutput(BaseModel):
    model_config = ConfigDict(extra="allow")

    result: str = "ok"


class FlakyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


_attempts_seen: list[int] = []


def _build_flaky_executor(
    *,
    fail_until_attempt: int,
    exception_class: type[Exception] = RuntimeError,
    retry_policy: RetryPolicy = RetryPolicy(),
) -> type:
    """Build a one-off executor class that fails the first N attempts.

    Reset _attempts_seen between tests to track invocation history.
    """

    class FlakyExecutor:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type="test.flaky",
            category=NodeCategory.DATA,
            display_name="Flaky Test Node",
            description="Fails until a configured attempt, then returns ok.",
            input_schema=FlakyInput,
            output_schema=FlakyOutput,
            config_schema=FlakyConfig,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.IDEMPOTENT,
            retry=retry_policy,
        )

        async def execute(
            self,
            ctx: NodeExecutionContext,
            inputs: FlakyInput,
            config: FlakyConfig,
        ) -> NodeResult[FlakyOutput]:
            _attempts_seen.append(ctx.attempt)
            if ctx.attempt < fail_until_attempt:
                raise exception_class(f"deliberate failure on attempt {ctx.attempt}")
            return success(FlakyOutput(result=f"ok-attempt-{ctx.attempt}"))

    return FlakyExecutor


def _flaky_registry(executor_cls: type) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(executor_cls(), overwrite=True)
    return reg


def _single_flaky_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "f",
                    "type": "test.flaky",
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


# ---------------------------------------------------------------------------
# Test 1: default RetryPolicy = no retries (current behavior preserved)
# ---------------------------------------------------------------------------


async def test_default_policy_does_not_retry():
    """Default RetryPolicy(max_attempts=1) preserves pre-retry behavior:
    a failing node parks the run as ERRORED with no retry events."""
    _attempts_seen.clear()
    flaky = _build_flaky_executor(fail_until_attempt=99)  # always fails
    registry = _flaky_registry(flaky)
    graph = compile_graph(_single_flaky_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="retry-default")

    assert result.status is RunStatus.ERRORED
    assert _attempts_seen == [1]
    assert len(_events_of_kind(emitter, "node_retry_scheduled")) == 0
    assert len(_events_of_kind(emitter, "node_failed")) == 1
    assert len(_events_of_kind(emitter, "run_errored")) == 1


# ---------------------------------------------------------------------------
# Test 2: success on attempt 2 emits 1 retry, 1 completed
# ---------------------------------------------------------------------------


async def test_retry_succeeds_on_second_attempt():
    """max_attempts=3, fails on attempt 1, succeeds on attempt 2.
    Expect: one node_retry_scheduled, one node_completed, run COMPLETED."""
    _attempts_seen.clear()
    policy = RetryPolicy(max_attempts=3, backoff=BackoffStrategy.NONE)
    flaky = _build_flaky_executor(fail_until_attempt=2, retry_policy=policy)
    registry = _flaky_registry(flaky)
    graph = compile_graph(_single_flaky_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="retry-succeed-2")

    assert result.status is RunStatus.COMPLETED
    assert _attempts_seen == [1, 2]
    retries = _events_of_kind(emitter, "node_retry_scheduled")
    assert len(retries) == 1
    assert retries[0]["attempt"] == 1
    assert retries[0]["next_attempt"] == 2
    assert retries[0]["error_type"] == "RuntimeError"

    completed = _events_of_kind(emitter, "node_completed")
    assert len(completed) == 1
    assert completed[0]["attempt"] == 2
    assert completed[0]["output"]["result"] == "ok-attempt-2"


# ---------------------------------------------------------------------------
# Test 3: exhaustion after N attempts → ERRORED
# ---------------------------------------------------------------------------


async def test_retry_exhausted_after_max_attempts():
    """max_attempts=3, always fails. Expect 2 retries + 1 final failure +
    run ERRORED. The node's attempt counter ends at 3."""
    _attempts_seen.clear()
    policy = RetryPolicy(max_attempts=3, backoff=BackoffStrategy.NONE)
    flaky = _build_flaky_executor(fail_until_attempt=99, retry_policy=policy)
    registry = _flaky_registry(flaky)
    graph = compile_graph(_single_flaky_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="retry-exhausted")

    assert result.status is RunStatus.ERRORED
    assert _attempts_seen == [1, 2, 3]
    retries = _events_of_kind(emitter, "node_retry_scheduled")
    assert len(retries) == 2
    assert [r["attempt"] for r in retries] == [1, 2]
    failed = _events_of_kind(emitter, "node_failed")
    assert len(failed) == 1
    assert failed[0]["attempt"] == 3


# ---------------------------------------------------------------------------
# Test 4: retry_on whitelist filters non-matching exceptions
# ---------------------------------------------------------------------------


async def test_retry_on_whitelist_skips_non_matching_exceptions():
    """retry_on=('HTTPError',) means a ValueError must NOT trigger retry.
    Expect the run to ERROR on the first failed attempt."""
    _attempts_seen.clear()
    policy = RetryPolicy(
        max_attempts=5,
        backoff=BackoffStrategy.NONE,
        retry_on=("HTTPError",),
    )
    flaky = _build_flaky_executor(
        fail_until_attempt=99,
        exception_class=ValueError,
        retry_policy=policy,
    )
    registry = _flaky_registry(flaky)
    graph = compile_graph(_single_flaky_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="retry-whitelist")

    assert result.status is RunStatus.ERRORED
    assert _attempts_seen == [1]
    assert len(_events_of_kind(emitter, "node_retry_scheduled")) == 0
    failed = _events_of_kind(emitter, "node_failed")
    assert len(failed) == 1
    assert failed[0]["error_type"] == "ValueError"


# ---------------------------------------------------------------------------
# Test 5: crash + resume walks past historic retries without re-sleeping
# ---------------------------------------------------------------------------


async def test_crash_recovery_walks_past_historic_retry_attempts():
    """Simulate a crash mid-retry: pre-populate the checkpointer with a
    failed retry outcome at attempt=1, then run with a flaky node that
    succeeds on attempt 2. The scheduler should walk past the historic
    retry without sleeping and execute attempt 2 fresh."""
    from matrx_graph.checkpoint.protocol import NodeOutcome

    _attempts_seen.clear()
    policy = RetryPolicy(
        max_attempts=3,
        backoff=BackoffStrategy.FIXED,
        initial_delay_ms=10_000,  # would be slow if we actually slept
    )
    # Use a flaky that ONLY records attempt 2 in _attempts_seen (because
    # the prior attempt 1 outcome is pre-populated, the executor shouldn't
    # be called for attempt 1).
    flaky = _build_flaky_executor(fail_until_attempt=2, retry_policy=policy)
    registry = _flaky_registry(flaky)
    graph = compile_graph(_single_flaky_definition(), registry=registry)

    checkpointer = MemoryCheckpointer()
    # Pre-populate the failed retry outcome at attempt=1 (as if a prior
    # boot got that far before crashing).
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="crash-resume",
            step=0,
            node_id="f",
            attempt=1,
            output={},
            error={"type": "RuntimeError", "message": "deliberate failure on attempt 1"},
            source="retry",
            duration_ms=10,
        )
    )

    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
    )

    import time as _time

    start = _time.time()
    result = await scheduler.run(run_id="crash-resume")
    elapsed = _time.time() - start

    # The historic retry should NOT have re-slept (delay 10s). Cap at 1s
    # to allow generous CI latency.
    assert elapsed < 1.0, f"resume re-slept ({elapsed:.2f}s) — backoff replay wasn't free"
    assert result.status is RunStatus.COMPLETED
    # Only attempt 2 invoked the executor (attempt 1 came from outcome replay).
    assert _attempts_seen == [2]
    # The replayed retry should still fire NodeRetryScheduledEvent for the UI.
    retries = _events_of_kind(emitter, "node_retry_scheduled")
    assert len(retries) == 1
    assert retries[0]["attempt"] == 1
    assert retries[0]["delay_ms"] == 0  # replayed = no sleep
