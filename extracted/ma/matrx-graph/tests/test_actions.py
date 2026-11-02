from __future__ import annotations

import dataclasses

import pytest
from matrx_graph import (
    ActionAuthorizationError,
    ActionRegistry,
    ActionTier,
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    NodeRegistryError,
    RunStatus,
    Scheduler,
    register_node,
    compile_graph,
    resolve_action_executor,
)
from matrx_graph.actions.spec import ActionNameError
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, Field

from tests._fixtures import make_app_context


class _SumInput(BaseModel):
    a: int = Field(default=0)
    b: int = Field(default=0)


class _SumOutput(BaseModel):
    total: int


async def test_action_decorator_registers_node_and_action():
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.sum",
        description="Add two integers",
        category=NodeCategory.DATA,
        determinism=ActionTier.PURE,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _do_sum(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=inputs.a + inputs.b))

    # Registered as a node type
    assert nreg.has("test.sum")
    spec = nreg.get("test.sum").spec
    assert spec.node_type == "test.sum"
    assert spec.determinism is ActionTier.PURE
    assert spec.category is NodeCategory.DATA

    # Registered in the directive catalog
    assert areg.has("test.sum")
    action_spec = areg.get("test.sum")
    assert action_spec.name == "test.sum"
    assert action_spec.input_schema is _SumInput
    assert action_spec.output_schema is _SumOutput

    # The raw function still works — decorator returns it unchanged
    # (it now returns the NodeResult envelope, like every executor).
    result = await _do_sum(None, _SumInput(a=2, b=3))
    assert result.result.total == 5


async def test_action_runs_end_to_end_via_scheduler():
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.double",
        category=NodeCategory.DATA,
        determinism=ActionTier.PURE,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _double(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=(inputs.a + inputs.b) * 2))

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "d",
                    "type": "test.double",
                    "position": {"x": 0, "y": 0},
                    "data": {},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=nreg)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=nreg)
    result = await scheduler.run(run_id="run-action-1", inputs={"a": 3, "b": 4})

    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["d"]["total"] == 14


async def test_resolve_action_executor_finds_adapter():
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.echo",
        category=NodeCategory.CUSTOM,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _echo(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=inputs.a))

    exec_ = resolve_action_executor("test.echo", node_registry=nreg, action_registry=areg)
    assert exec_.spec.node_type == "test.echo"


def test_action_name_must_not_include_action_prefix() -> None:
    nreg = NodeRegistry()
    areg = ActionRegistry()

    with pytest.raises(ActionNameError, match="must not include an 'action.' prefix"):

        @register_node(
            name="action.bad.name",
            input_schema=_SumInput,
            output_schema=_SumOutput,
            node_registry=nreg,
            action_registry=areg,
        )
        async def _bad(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
            return success(_SumOutput(total=0))


async def test_duplicate_action_rejected_without_overwrite():
    nreg = NodeRegistry()
    areg = ActionRegistry()

    def _register() -> None:
        @register_node(
            name="test.dup",
            input_schema=_SumInput,
            output_schema=_SumOutput,
            node_registry=nreg,
            action_registry=areg,
        )
        async def _x(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
            return success(_SumOutput(total=0))

    _register()
    with pytest.raises(NodeRegistryError):
        _register()


def test_directive_catalog_descriptor_shape():
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.cat",
        description="catalog test",
        category=NodeCategory.TOOL,
        determinism=ActionTier.IDEMPOTENT,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        icon="calculator",
        tags=("math", "arithmetic"),
        node_registry=nreg,
        action_registry=areg,
    )
    async def _op(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=0))

    catalog = areg.catalog()
    assert len(catalog) == 1
    entry = catalog[0]
    assert entry["name"] == "test.cat"
    assert entry["category"] == "tool"
    assert entry["determinism"] == "idempotent"
    assert entry["icon"] == "calculator"
    assert entry["tags"] == ["math", "arithmetic"]
    assert entry["spec_type"] == "test.cat"
    assert entry["admin_only"] is False
    assert entry["input_schema"]["type"] == "object"
    assert entry["output_schema"]["type"] == "object"


# ---------------------------------------------------------------------------
# admin_only gating — the privilege-escalation fix.
#
# admin.sql.* (aidream/graph_actions/admin/sql.py) runs raw asyncpg on the primary
# pool with no RLS and no acting-as-user scoping — the graph-action
# equivalent of matrx-ai's admin_only `sql` tool. These tests prove the gate
# using a throwaway admin_only action (no live DB needed) against every
# dispatch path the real db.* actions can be reached through: a direct
# registered node via the Scheduler, and the dynamic tool.call node. Both
# converge on _ActionExecutor.execute (see its docstring) — one assertion
# per path proves there's no separate, forgettable check to keep in sync.
# ---------------------------------------------------------------------------


def _register_admin_only_action(
    *, nreg: NodeRegistry, areg: ActionRegistry, name: str = "test.admin_only"
):
    @register_node(
        name=name,
        category=NodeCategory.TOOL,
        determinism=ActionTier.SIDE_EFFECT,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        admin_only=True,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _privileged(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=inputs.a + inputs.b))

    return _privileged


def test_admin_only_flag_recorded_on_action_spec_and_catalog():
    nreg = NodeRegistry()
    areg = ActionRegistry()
    _register_admin_only_action(nreg=nreg, areg=areg)

    assert areg.get("test.admin_only").admin_only is True
    entry = next(e for e in areg.catalog() if e["name"] == "test.admin_only")
    assert entry["admin_only"] is True


async def test_admin_only_executor_rejects_non_admin_ctx_directly():
    """Unit-level: the _ActionExecutor adapter itself refuses to invoke the
    wrapped function for a non-admin ctx — proven without any scheduler
    machinery so the gate's own logic is pinned precisely."""
    nreg = NodeRegistry()
    areg = ActionRegistry()
    _register_admin_only_action(nreg=nreg, areg=areg)

    executor = nreg.get("test.admin_only")
    non_admin_ctx = _make_node_ctx(is_admin=False)

    with pytest.raises(ActionAuthorizationError) as exc_info:
        await executor.execute(non_admin_ctx, _SumInput(a=1, b=2), None)
    assert "test.admin_only" in str(exc_info.value)
    assert "non-admin" in str(exc_info.value).lower()


async def test_admin_only_executor_allows_admin_ctx_directly():
    nreg = NodeRegistry()
    areg = ActionRegistry()
    _register_admin_only_action(nreg=nreg, areg=areg)

    executor = nreg.get("test.admin_only")
    admin_ctx = _make_node_ctx(is_admin=True)

    result = await executor.execute(admin_ctx, _SumInput(a=1, b=2), None)
    assert result.result.total == 3


def _make_node_ctx(*, is_admin: bool):
    """Build a minimal NodeExecutionContext with a real AppContext carrying
    the given admin flag — enough to drive _ActionExecutor.execute directly
    without a full Scheduler run."""
    from matrx_graph.types.context import ChannelView, NodeExecutionContext

    app_ctx = make_app_context()
    app_ctx = dataclasses.replace(app_ctx, is_admin=is_admin)
    return NodeExecutionContext(
        app=app_ctx,
        run_id="run-admin-gate",
        thread_id="run-admin-gate",
        node_id="n",
        step=0,
        attempt=1,
        channels=ChannelView(_values={}, _pending_writes=[]),
        checkpointer=MemoryCheckpointer(),
    )


def test_node_context_stable_idempotency_excludes_retry_attempt():
    first = _make_node_ctx(is_admin=False)
    second = dataclasses.replace(
        first,
        attempt=9,
        dispatch_id="dispatch-1",
        item_index=3,
        firing=2,
    )
    same_logical_retry = dataclasses.replace(second, attempt=10)

    assert second.stable_idempotency_key == same_logical_retry.stable_idempotency_key
    assert second.idempotency_key != same_logical_retry.idempotency_key


async def test_admin_only_action_rejected_end_to_end_for_non_admin_via_scheduler():
    """End-to-end: a non-admin run's Scheduler parks ERRORED with the
    authorization failure attributed to the node — proving the direct
    direct registered-node dispatch path (inline/queued/resume all share this
    same Scheduler._execute_invocation_body call site) is covered, not just
    the adapter in isolation."""
    nreg = NodeRegistry()
    areg = ActionRegistry()
    _register_admin_only_action(nreg=nreg, areg=areg)

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "d",
                    "type": "test.admin_only",
                    "position": {"x": 0, "y": 0},
                    "data": {},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=nreg)
    non_admin_app_ctx = dataclasses.replace(make_app_context(), is_admin=False)
    scheduler = Scheduler(graph, MemoryCheckpointer(), non_admin_app_ctx, registry=nreg)

    result = await scheduler.run(run_id="run-admin-gate-2", inputs={"a": 1, "b": 2})

    assert result.status is RunStatus.ERRORED
    assert result.error is not None
    assert "ActionAuthorizationError" in result.error
    assert "d" not in result.last_outputs


async def test_admin_only_action_allowed_end_to_end_for_admin_via_scheduler():
    nreg = NodeRegistry()
    areg = ActionRegistry()
    _register_admin_only_action(nreg=nreg, areg=areg)

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "d",
                    "type": "test.admin_only",
                    "position": {"x": 0, "y": 0},
                    "data": {},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=nreg)
    admin_app_ctx = dataclasses.replace(make_app_context(), is_admin=True)
    scheduler = Scheduler(graph, MemoryCheckpointer(), admin_app_ctx, registry=nreg)

    result = await scheduler.run(run_id="run-admin-gate-3", inputs={"a": 1, "b": 2})

    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["d"]["total"] == 3


async def test_admin_only_action_rejected_via_dynamic_tool_call_dispatch():
    """The dynamic tool.call node resolves the SAME registered
    _ActionExecutor via resolve_action_executor and calls .execute(...)
    directly — proving that dispatch path is covered too, with no separate
    admin check to duplicate or forget. tool.call always resolves through
    the DEFAULT registries, so this test registers there and cleans up."""
    from matrx_graph.actions import default_action_registry
    from matrx_graph.executor.registry import default_registry
    from matrx_graph.nodes.tool.call import ToolCallConfig, ToolCallExecutor, ToolCallInput

    nreg = default_registry()
    areg = default_action_registry()
    action_name = "test.admin_only_toolcall"
    _register_admin_only_action(nreg=nreg, areg=areg, name=action_name)
    try:
        node = ToolCallExecutor()
        non_admin_ctx = _make_node_ctx(is_admin=False)
        config = ToolCallConfig(action_name=action_name)

        with pytest.raises(ActionAuthorizationError):
            await node.execute(non_admin_ctx, ToolCallInput(payload={"a": 1, "b": 2}), config)

        admin_ctx = _make_node_ctx(is_admin=True)
        result = await node.execute(admin_ctx, ToolCallInput(payload={"a": 1, "b": 2}), config)
        # Node Result System: tool.call returns Success[ToolCallOutput];
        # the payload is strictly {action, output} — no spread, no success flag.
        assert result.status == "success"
        assert result.result.action == action_name
        assert result.result.output["total"] == 3
        assert not hasattr(result.result, "success")
    finally:
        nreg.unregister(action_name)
        areg.unregister(action_name)


# ---------------------------------------------------------------------------
# tool.call — Node Result System failure paths (Wave 1 semantics change).
# The payload is strictly {action, output}; every can't-do-the-job case is a
# structured Failure with a stable code, and an inner action Failure becomes
# tool.call's OWN Failure with code/message/details preserved.
# ---------------------------------------------------------------------------


async def test_tool_call_unknown_action_is_failure():
    from matrx_graph.nodes.tool.call import ToolCallConfig, ToolCallExecutor, ToolCallInput
    from matrx_graph.types.result import Failure

    node = ToolCallExecutor()
    ctx = _make_node_ctx(is_admin=True)
    result = await node.execute(
        ctx, ToolCallInput(payload={}), ToolCallConfig(action_name="test.no_such_action")
    )
    assert isinstance(result, Failure)
    assert result.error.code == "unknown_action"


async def test_tool_call_invalid_input_is_failure():
    from matrx_graph.actions import default_action_registry
    from matrx_graph.executor.registry import default_registry
    from matrx_graph.nodes.tool.call import ToolCallConfig, ToolCallExecutor, ToolCallInput
    from matrx_graph.types.result import Failure

    nreg = default_registry()
    areg = default_action_registry()
    action_name = "test.invalid_input_toolcall"

    @register_node(
        name=action_name,
        category=NodeCategory.DATA,
        determinism=ActionTier.PURE,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _sum(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=inputs.a + inputs.b))

    try:
        node = ToolCallExecutor()
        ctx = _make_node_ctx(is_admin=True)
        result = await node.execute(
            ctx,
            ToolCallInput(payload={"a": "not-an-int"}),
            ToolCallConfig(action_name=action_name),
        )
        assert isinstance(result, Failure)
        assert result.error.code == "invalid_input"
        assert action_name in result.error.message
    finally:
        nreg.unregister(action_name)
        areg.unregister(action_name)


async def test_tool_call_inner_failure_preserves_code_and_details():
    from matrx_graph.actions import default_action_registry
    from matrx_graph.executor.registry import default_registry
    from matrx_graph.nodes.tool.call import ToolCallConfig, ToolCallExecutor, ToolCallInput
    from matrx_graph.types.result import Failure, failure

    nreg = default_registry()
    areg = default_action_registry()
    action_name = "test.failing_inner_toolcall"
    usage = {"input_tokens": 10, "output_tokens": 0, "total_tokens": 10, "cost_usd": 0.01}

    @register_node(
        name=action_name,
        category=NodeCategory.TOOL,
        determinism=ActionTier.IDEMPOTENT,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _fail(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return failure("rate_limited", "provider throttled", details={"usage": usage})

    try:
        node = ToolCallExecutor()
        ctx = _make_node_ctx(is_admin=True)
        result = await node.execute(
            ctx, ToolCallInput(payload={"a": 1, "b": 2}), ToolCallConfig(action_name=action_name)
        )
        # The inner Failure becomes tool.call's OWN Failure — stable code,
        # message, and details (incl. details.usage for cost settlement).
        assert isinstance(result, Failure)
        assert result.error.code == "rate_limited"
        assert result.error.message == "provider throttled"
        assert result.error.details == {"usage": usage}
    finally:
        nreg.unregister(action_name)
        areg.unregister(action_name)


# ── Legacy spec_type alias (action.* eradication, 2026-08-08) ────────────────
# Stored workflow definitions / checkpoints still carry "action.<name>"
# spec_types. The registry resolves that spelling as an ALIAS of the bare
# canonical name — nothing stored is ever rewritten.


async def test_legacy_action_prefix_resolves_via_registry_alias():
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.alias.sum",
        category=NodeCategory.TOOL,
        determinism=ActionTier.IDEMPOTENT,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _sum(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=inputs.a + inputs.b))

    # Canonical spec_type is the bare name.
    assert nreg.get("test.alias.sum").spec.node_type == "test.alias.sum"
    # The legacy prefixed spelling resolves to the SAME executor.
    assert nreg.has("action.test.alias.sum")
    assert nreg.get("action.test.alias.sum") is nreg.get("test.alias.sum")
    # But the canonical listing never contains the prefixed form.
    assert "action.test.alias.sum" not in nreg.all_types()


async def test_stored_definition_with_legacy_spec_type_compiles_and_runs():
    """A stored definition authored before the eradication (spec_type
    "action.<name>") must compile and execute byte-identically."""
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.alias.double",
        category=NodeCategory.TOOL,
        determinism=ActionTier.IDEMPOTENT,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _double(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=(inputs.a + inputs.b) * 2))

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n1",
                    "type": "action.test.alias.double",
                    "position": {"x": 0, "y": 0},
                    "data": {"spec_type": "action.test.alias.double"},
                }
            ],
            "edges": [],
        }
    )
    compiled = compile_graph(definition, registry=nreg)
    # Compile resolves through the alias to the CANONICAL executor spec.
    scheduler = Scheduler(compiled, MemoryCheckpointer(), make_app_context(), registry=nreg)
    result = await scheduler.run(run_id="run-legacy-alias", inputs={"a": 2, "b": 3})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n1"]["total"] == 10


class _ScaleConfig(BaseModel):
    factor: int = Field(default=1)


async def test_a_three_parameter_action_receives_its_authored_config():
    """The config opt-in, end to end through the scheduler.

    An action that declares ``(ctx, inputs, config)`` is handed the validated
    ``config_schema`` model. This is the ONLY way to author a value on a node
    whose merged inputs are gated by a closed ``input_kind`` — a static input
    would be an undeclared key in the gated payload and park the run
    (``rag.embed``, 2026-08-23). If the adapter ever drops config again, this
    node silently multiplies by 1 instead of the authored factor.
    """
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.scale",
        category=NodeCategory.DATA,
        determinism=ActionTier.PURE,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        config_schema=_ScaleConfig,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _scale(_ctx, inputs: _SumInput, config: _ScaleConfig) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=(inputs.a + inputs.b) * config.factor))

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n1",
                    "type": "test.scale",
                    "position": {"x": 0, "y": 0},
                    "data": {"spec_type": "test.scale", "config": {"factor": 7}},
                }
            ],
            "edges": [],
        }
    )
    scheduler = Scheduler(
        compile_graph(definition, registry=nreg),
        MemoryCheckpointer(),
        make_app_context(),
        registry=nreg,
    )
    result = await scheduler.run(run_id="run-action-config", inputs={"a": 2, "b": 3})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n1"]["total"] == 35


async def test_a_two_parameter_action_still_never_sees_config():
    """The default is unchanged: two params, config dropped, no signature error."""
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.plain",
        category=NodeCategory.DATA,
        determinism=ActionTier.PURE,
        input_schema=_SumInput,
        output_schema=_SumOutput,
        config_schema=_ScaleConfig,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _plain(_ctx, inputs: _SumInput) -> NodeResult[_SumOutput]:
        return success(_SumOutput(total=inputs.a + inputs.b))

    assert nreg.get("test.plain")._wants_config is False
    assert nreg.get("test.plain").spec.config_schema is _ScaleConfig
