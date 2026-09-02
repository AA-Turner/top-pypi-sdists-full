"""The source_kind collision defusal — host-registered executors always win.

The failure class this pins: every matrx-local ``tool.definition`` row is
``source_kind='native'`` with an empty ``function_path`` → the registry types
it ``ToolType.LOCAL`` with no callable, and the executor rejects dispatch with
``no_viable_executor``. The host executes those tools through
``ExternalHandlerRegistry`` — so a server/DB load must never shadow that.

Two independent layers, each tested alone:
  1. LOAD  — ``_load_rows`` keeps an existing executable def / flips a
     no-path row to EXTERNAL_HANDLER when a handler is registered.
  2. DISPATCH — ``ToolExecutor._dispatch`` routes a LOCAL no-path def to the
     external handler instead of ``_execute_local``.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_ai.tools.external_handlers import ExternalHandlerRegistry
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry


@pytest.fixture
def handler_sandbox():
    """Snapshot + restore the process-global ExternalHandlerRegistry."""
    reg = ExternalHandlerRegistry.get_instance()
    saved_tools = dict(reg._tool_handlers)
    saved_apps = dict(reg._app_handlers)
    try:
        yield reg
    finally:
        reg._tool_handlers.clear()
        reg._tool_handlers.update(saved_tools)
        reg._app_handlers.clear()
        reg._app_handlers.update(saved_apps)


async def _ok_handler(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=True,
        output={"handled_by": "host", "echo": args},
        tool_name=ctx.tool_name,
        call_id=ctx.call_id,
    )


def _native_row(name: str) -> dict[str, Any]:
    """A tool.definition row exactly as matrx-local's 113 rows look."""
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": "cloud-canonical description",
        "source_kind": "native",
        "function_path": "",
        "parameters": {"type": "object", "properties": {}},
        "is_active": True,
    }


# ── Layer 1: load-time ──────────────────────────────────────────────────────


def test_load_keeps_existing_host_executable_definition(handler_sandbox):
    registry = ToolRegistry()
    host_def = ToolDefinition(
        name="local_read_file",
        tool_type=ToolType.EXTERNAL_HANDLER,
        source_kind="matrx_local",
        description="host def",
    )
    registry.register(host_def)

    row = _native_row("local_read_file")
    loaded = registry._load_rows([row])
    assert loaded == 1

    kept = registry.get("local_read_file")
    assert kept is host_def, "row without an execution path clobbered the host def"
    # Row identity adopted so UUID lookups resolve to the kept def.
    assert registry.get(row["id"]) is host_def


def test_load_flips_no_path_row_to_external_handler_when_handler_registered(
    handler_sandbox,
):
    handler_sandbox.register("local_write_file", _ok_handler)
    registry = ToolRegistry()

    loaded = registry._load_rows([_native_row("local_write_file")])
    assert loaded == 1
    tool_def = registry.get("local_write_file")
    assert tool_def is not None
    assert tool_def.tool_type == ToolType.EXTERNAL_HANDLER


def test_load_without_handler_stays_local_no_path(handler_sandbox):
    """No host executor at all → the row loads as-is (observable
    no_viable_executor at dispatch is the correct behavior)."""
    registry = ToolRegistry()
    registry._load_rows([_native_row("local_orphan_tool")])
    tool_def = registry.get("local_orphan_tool")
    assert tool_def is not None
    assert tool_def.tool_type == ToolType.LOCAL
    assert not tool_def.function_path


def test_load_from_definitions_applies_same_precedence(handler_sandbox):
    registry = ToolRegistry()
    host_def = ToolDefinition(
        name="local_shell",
        tool_type=ToolType.EXTERNAL_HANDLER,
        source_kind="matrx_local",
    )
    registry.register(host_def)

    incoming = ToolDefinition(
        name="local_shell",
        tool_type=ToolType.LOCAL,
        function_path="",
        source_kind="native",
    )
    registry.load_from_definitions([incoming])
    assert registry.get("local_shell") is host_def


# ── Layer 2: dispatch-time ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_dispatch_routes_local_no_path_def_to_external_handler(handler_sandbox):
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.guardrails import GuardrailEngine
    from matrx_ai.tools.lifecycle import ToolLifecycleManager
    from matrx_ai.tools.logger import ToolExecutionLogger

    handler_sandbox.register("local_screenshot", _ok_handler)

    registry = ToolRegistry()
    # The def exactly as a server registry load would produce it TODAY if the
    # load-time flip were somehow bypassed (e.g. a def registered before the
    # handler existed) — LOCAL, no path, no callable.
    tool_def = ToolDefinition(
        name="local_screenshot",
        tool_type=ToolType.LOCAL,
        function_path="",
        source_kind="native",
    )
    registry.register(tool_def)

    executor = ToolExecutor(
        registry=registry,
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )
    ctx = ToolContext(call_id="call-1", tool_name="local_screenshot", iteration=1)

    result = await executor._dispatch(tool_def, {"x": 1}, ctx, stream=None)
    assert result.success is True
    assert result.output == {"handled_by": "host", "echo": {"x": 1}}


@pytest.mark.asyncio
async def test_dispatch_still_rejects_when_no_handler_exists(handler_sandbox):
    """Without any host executor the LOCAL no-path def keeps failing loudly
    in _execute_local — the observable no_viable_executor class stays."""
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.guardrails import GuardrailEngine
    from matrx_ai.tools.lifecycle import ToolLifecycleManager
    from matrx_ai.tools.logger import ToolExecutionLogger

    registry = ToolRegistry()
    tool_def = ToolDefinition(
        name="local_nothing_runs_me",
        tool_type=ToolType.LOCAL,
        function_path="",
        source_kind="native",
    )
    registry.register(tool_def)
    executor = ToolExecutor(
        registry=registry,
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )
    ctx = ToolContext(call_id="call-2", tool_name="local_nothing_runs_me", iteration=1)
    result = await executor._dispatch(tool_def, {}, ctx, stream=None)
    assert result.success is False
