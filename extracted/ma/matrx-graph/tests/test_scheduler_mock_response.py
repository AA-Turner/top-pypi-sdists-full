"""Phase 6.2 — per-node mock_response short-circuit.

When NodeDef.data.mock_response = {enabled: true, output: {...}} is set,
the compile step surfaces it on CompiledNode.mock_response and the
scheduler skips the executor entirely, validating the supplied output
against the node's output_schema and recording a ``source="mocked"``
NodeOutcome.

Verifies:
    1. No mock → normal execution.
    2. mock_response.enabled=true with a valid output → executor skipped,
       output is the mock, NodeOutcome.source = "mocked".
    3. mock_response.enabled=false → executor runs normally (treated as
       no-mock).
    4. Invalid mock output → ExecutionError, run errored.
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
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field

from tests._fixtures import FakeEmitter, make_app_context


class _Input(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    result: str = Field(default="real")


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


_invocation_count = 0


class _RealExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.real_or_mock",
        category=NodeCategory.DATA,
        display_name="Real-or-mock",
        description="Records whether the real executor ran.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_Output]:
        global _invocation_count
        _invocation_count += 1
        return success(_Output(result="real"))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_RealExecutor(), overwrite=True)
    return reg


def _definition(mock: dict | None = None) -> Definition:
    node_data: dict = {"config": {}}
    if mock is not None:
        node_data["mock_response"] = mock
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "rm",
                    "type": "test.real_or_mock",
                    "position": {"x": 0, "y": 0},
                    "data": node_data,
                },
            ],
            "edges": [],
        }
    )


async def test_no_mock_runs_executor():
    global _invocation_count
    _invocation_count = 0
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="mock-none")
    assert result.status is RunStatus.COMPLETED
    assert _invocation_count == 1
    assert result.last_outputs["rm"]["result"] == "real"


async def test_mock_enabled_short_circuits_executor():
    global _invocation_count
    _invocation_count = 0
    registry = _registry()
    graph = compile_graph(
        _definition(mock={"enabled": True, "output": {"result": "mocked"}}),
        registry=registry,
    )
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="mock-on")
    assert result.status is RunStatus.COMPLETED
    # Executor was NOT called.
    assert _invocation_count == 0
    # Output is the mock.
    assert result.last_outputs["rm"]["result"] == "mocked"
    # Outcome recorded with source="mocked".
    outcome = await checkpointer.get_outcome(run_id="mock-on", step=0, node_id="rm", attempt=1)
    assert outcome is not None
    assert outcome.source == "mocked"
    # Event emitted as node_skipped (mock + replay share the visual).
    skipped = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "node_skipped"
    ]
    assert len(skipped) == 1


async def test_mock_disabled_runs_executor():
    """mock_response with enabled=false is treated as if no mock is set."""
    global _invocation_count
    _invocation_count = 0
    registry = _registry()
    graph = compile_graph(
        _definition(mock={"enabled": False, "output": {"result": "ignored"}}),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="mock-off")
    assert result.status is RunStatus.COMPLETED
    assert _invocation_count == 1
    assert result.last_outputs["rm"]["result"] == "real"


async def test_invalid_mock_output_errors_run():
    """A mock that doesn't pass output_schema validation errors cleanly."""
    global _invocation_count
    _invocation_count = 0
    registry = _registry()
    # _Output has extra="forbid"; "garbage_field" should fail.
    graph = compile_graph(
        _definition(
            mock={"enabled": True, "output": {"garbage_field": "no_such_field"}},
        ),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="mock-bad")
    assert result.status is RunStatus.ERRORED
    # Executor was NOT called (we failed before invoking).
    assert _invocation_count == 0
