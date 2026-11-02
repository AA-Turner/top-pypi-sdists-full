"""Phase 5.3 — NextInvocation.config_override threading.

The recovery API stashes a one-shot config tweak in
NextInvocation.config_override; the scheduler merges it over the node's
authored config at execute time and re-validates through the config
schema. The workflow definition itself is untouched — this is the
"Retry without saving" UX.

Verifies:
    1. No override → executor sees the authored config (current behavior).
    2. Override present → executor sees the merged + re-validated config.
    3. Override survives a checkpoint round-trip (resume picks it up).
    4. Invalid override → ExecutionError, run errored.
"""

from __future__ import annotations

from typing import ClassVar
from uuid import UUID

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
from matrx_graph.executor.scheduler import Invocation, _workflow_invocation_conversation_id
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field

from tests._fixtures import FakeEmitter, make_app_context


class ConfigEchoInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class ConfigEchoOutput(BaseModel):
    model_config = ConfigDict(extra="allow")
    seen_max_tokens: int = 0
    seen_label: str = ""


class ConfigEchoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_tokens: int = Field(default=100, ge=1, le=100_000)
    label: str = "default"


_seen_configs: list[dict] = []


class ConfigEchoExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.config_echo",
        category=NodeCategory.DATA,
        display_name="Config Echo",
        description="Records the config it sees for assertion in tests.",
        input_schema=ConfigEchoInput,
        output_schema=ConfigEchoOutput,
        config_schema=ConfigEchoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ConfigEchoInput,
        config: ConfigEchoConfig,
    ) -> NodeResult[ConfigEchoOutput]:
        _seen_configs.append(config.model_dump())
        return success(ConfigEchoOutput(seen_max_tokens=config.max_tokens, seen_label=config.label))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(ConfigEchoExecutor(), overwrite=True)
    return reg


def _definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "echo",
                    "type": "test.config_echo",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"max_tokens": 100, "label": "authored"}},
                },
            ],
            "edges": [],
        }
    )


async def test_no_override_uses_authored_config():
    _seen_configs.clear()
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="cfg-default")
    assert result.status is RunStatus.COMPLETED
    assert len(_seen_configs) == 1
    assert _seen_configs[0]["max_tokens"] == 100
    assert _seen_configs[0]["label"] == "authored"


async def test_config_override_is_merged_over_authored():
    """Resume from a checkpoint whose NextInvocation carries a config_override.
    The scheduler should merge it over the node's authored config and the
    executor should see the merged values."""
    _seen_configs.clear()
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()

    # Pre-populate a checkpoint that says "next, run 'echo' at attempt 2
    # with this config_override". This simulates what _prepare_retry_checkpoint
    # writes in the recovery API.
    cp = Checkpoint(
        checkpoint_id="cp-override",
        run_id="cfg-override",
        thread_id="cfg-override",
        step=0,
        channel_values={},
        next_invocations=[
            NextInvocation(
                node_id="echo",
                inputs={},
                attempt=2,
                config_override={"max_tokens": 8192, "label": "overridden"},
            )
        ],
    )
    await checkpointer.save_checkpoint(cp)

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.resume(run_id="cfg-override", checkpoint_id="cp-override")
    assert result.status is RunStatus.COMPLETED
    assert len(_seen_configs) == 1
    assert _seen_configs[0]["max_tokens"] == 8192
    assert _seen_configs[0]["label"] == "overridden"


async def test_partial_config_override_preserves_other_authored_fields():
    """Override only one field; other authored fields stay intact."""
    _seen_configs.clear()
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()

    cp = Checkpoint(
        checkpoint_id="cp-partial",
        run_id="cfg-partial",
        thread_id="cfg-partial",
        step=0,
        channel_values={},
        next_invocations=[
            NextInvocation(
                node_id="echo",
                inputs={},
                attempt=2,
                # Only override max_tokens — label should stay "authored".
                config_override={"max_tokens": 4096},
            )
        ],
    )
    await checkpointer.save_checkpoint(cp)

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.resume(run_id="cfg-partial", checkpoint_id="cp-partial")
    assert result.status is RunStatus.COMPLETED
    assert _seen_configs[0]["max_tokens"] == 4096
    assert _seen_configs[0]["label"] == "authored"


async def test_invalid_config_override_fails_cleanly():
    """An override that violates the config_schema fails with a clear
    ExecutionError; the run errors but doesn't crash the framework."""
    _seen_configs.clear()
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    checkpointer = MemoryCheckpointer()

    cp = Checkpoint(
        checkpoint_id="cp-bad",
        run_id="cfg-bad",
        thread_id="cfg-bad",
        step=0,
        channel_values={},
        next_invocations=[
            NextInvocation(
                node_id="echo",
                inputs={},
                attempt=2,
                # max_tokens has ge=1; -5 must fail schema validation.
                config_override={"max_tokens": -5},
            )
        ],
    )
    await checkpointer.save_checkpoint(cp)
    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.resume(run_id="cfg-bad", checkpoint_id="cp-bad")
    # ExecutionError surfaces as run_errored (recoverable).
    assert result.status is RunStatus.ERRORED
    assert len(_seen_configs) == 0


async def test_invocation_dataclass_carries_config_override():
    """Sanity check the Invocation dataclass — the public API the recovery
    helpers depend on. Default is None; explicit value is preserved."""
    inv = Invocation(node_id="x", inputs={})
    assert inv.config_override is None
    inv2 = Invocation(node_id="x", inputs={}, config_override={"a": 1})
    assert inv2.config_override == {"a": 1}


async def test_parallel_workflow_invocations_receive_distinct_durable_conversations():
    """A workflow step is an independent AI persistence/cache boundary.

    Sharing the run's root conversation made two ``ai.llm.chat`` calls look like
    rounds of one provider loop (false prompt-cache drift) and let concurrent
    conversation creation race on ``cx_conversation.id``.  The scheduler must
    fork a stable valid UUID for every invocation while preserving the common
    request identity for cost rollup.
    """

    seen: list[tuple[str, str, str, str]] = []

    class ConversationRecorder:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type="test.conversation_recorder",
            category=NodeCategory.DATA,
            display_name="Conversation Recorder",
            description="Records the invocation persistence identity.",
            input_schema=ConfigEchoInput,
            output_schema=ConfigEchoOutput,
            config_schema=ConfigEchoConfig,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
            determinism=ActionTier.PURE,
        )

        async def execute(
            self,
            ctx: NodeExecutionContext,
            _inputs: ConfigEchoInput,
            _config: ConfigEchoConfig,
        ) -> NodeResult[ConfigEchoOutput]:
            seen.append(
                (
                    ctx.app.conversation_id,
                    ctx.app.request_id,
                    ctx.app.conversation_type,
                    ctx.app.origin_class,
                )
            )
            return success(ConfigEchoOutput())

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(ConversationRecorder(), overwrite=True)
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "first", "type": "test.conversation_recorder", "position": {"x": 0, "y": 0}},
                {"id": "second", "type": "test.conversation_recorder", "position": {"x": 1, "y": 0}},
            ],
            "edges": [],
        }
    )
    app = make_app_context(FakeEmitter())
    scheduler = Scheduler(
        compile_graph(definition, registry=registry),
        MemoryCheckpointer(),
        app,
        registry=registry,
    )

    result = await scheduler.run(run_id="workflow-identity-test")

    assert result.status is RunStatus.COMPLETED
    assert len(seen) == 2
    conversation_ids = {row[0] for row in seen}
    assert len(conversation_ids) == 2
    for conversation_id, request_id, conversation_type, origin_class in seen:
        assert str(UUID(conversation_id)) == conversation_id
        assert request_id == app.request_id
        assert conversation_type == "workflow"
        assert origin_class == "workflow"


def test_workflow_invocation_conversation_identity_is_retry_stable_and_fanout_unique():
    """Retry is one durable invocation; fan-out coordinates are siblings."""

    original = Invocation(
        node_id="extract",
        inputs={},
        attempt=1,
        dispatch_id="fanout-42",
        item_index=0,
        firing=3,
    )
    retry = Invocation(
        node_id="extract",
        inputs={},
        attempt=2,
        dispatch_id="fanout-42",
        item_index=0,
        firing=3,
    )
    sibling = Invocation(
        node_id="extract",
        inputs={},
        attempt=1,
        dispatch_id="fanout-42",
        item_index=1,
        firing=3,
    )

    original_id = _workflow_invocation_conversation_id(
        run_id="identity-contract", step=7, invocation=original
    )
    assert original_id == _workflow_invocation_conversation_id(
        run_id="identity-contract", step=7, invocation=retry
    )
    assert original_id != _workflow_invocation_conversation_id(
        run_id="identity-contract", step=7, invocation=sibling
    )
