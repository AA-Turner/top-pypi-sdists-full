"""Phase 6.1 — per-node RetryPolicy override.

A node can carry data.retry_policy = {max_attempts, backoff, ...}. The
compile step parses it onto CompiledNode.retry_policy; the scheduler
uses it INSTEAD of the registered NodeSpec's class-level spec.retry.

Verifies:
    1. No per-node override → falls back to the spec default (no retry).
    2. Per-node override with max_attempts=3 → node retries even though
       the spec default is max_attempts=1.
    3. Invalid retry_policy → CompilationError at compile time.
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
from matrx_graph.errors import CompilationError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _Input(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: str = "ok"


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


_attempts: list[int] = []


class _FlakyExecutor:
    # NOTE: spec default retry is the implicit RetryPolicy() = max_attempts=1.
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.flaky_override",
        category=NodeCategory.DATA,
        display_name="Flaky (override test)",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
    )

    async def execute(
        self, ctx: NodeExecutionContext, _i: _Input, _c: _Config
    ) -> NodeResult[_Output]:
        _attempts.append(ctx.attempt)
        if ctx.attempt < 2:
            raise RuntimeError(f"fail on attempt {ctx.attempt}")
        return success(_Output(result=f"ok-{ctx.attempt}"))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_FlakyExecutor(), overwrite=True)
    return reg


def _definition(retry_policy: dict | None = None) -> Definition:
    data: dict = {"config": {}}
    if retry_policy is not None:
        data["retry_policy"] = retry_policy
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "f",
                    "type": "test.flaky_override",
                    "position": {"x": 0, "y": 0},
                    "data": data,
                },
            ],
            "edges": [],
        }
    )


async def test_no_override_uses_spec_default():
    _attempts.clear()
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="override-none")
    # spec default = max_attempts 1 → no retry → ERRORED on first failure.
    assert result.status is RunStatus.ERRORED
    assert _attempts == [1]


async def test_per_node_override_enables_retry():
    _attempts.clear()
    registry = _registry()
    graph = compile_graph(
        _definition(retry_policy={"max_attempts": 3, "backoff": "none"}),
        registry=registry,
    )
    # Sanity: the compiled node carries the override.
    assert graph.nodes["f"].retry_policy is not None
    assert graph.nodes["f"].retry_policy.max_attempts == 3

    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="override-on")
    # With max_attempts=3, the node retries and succeeds on attempt 2.
    assert result.status is RunStatus.COMPLETED
    assert _attempts == [1, 2]


async def test_invalid_override_fails_compile():
    registry = _registry()
    with pytest.raises(CompilationError):
        compile_graph(
            # max_attempts has le=20 — 999 must fail validation.
            _definition(retry_policy={"max_attempts": 999}),
            registry=registry,
        )


def test_retry_policy_default_helper():
    # Belt-and-suspenders: the spec's implicit default is max_attempts=1.
    assert RetryPolicy().max_attempts == 1
