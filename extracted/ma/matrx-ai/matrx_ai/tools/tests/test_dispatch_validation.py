"""Tests for the executor's pre-flight viable-executor check.

This pre-flight catches the bug class where a tool has neither a live
client-side delegation NOR a server-side function_path — without it, a
LOCAL-tool-type row with empty function_path fails with a generic
import error mid-dispatch, or worse, silently runs on the wrong
executor (the matrx-extend incident's root cause).
"""
from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.lifecycle import ToolLifecycleManager
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry


async def test_web_inner_constraints_reject_before_dispatch(
    isolated_registry, executor, monkeypatch, app_ctx_set
) -> None:
    """Wire validation must stop calls the inner web worker would reject."""
    import matrx_ai.tools._generated_declarations  # noqa: F401

    definition = ToolDefinition(
        name="web",
        description="Web dispatcher",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.implementations.web.web",
    )

    body_called = False
    captures: list[str] = []

    async def must_not_run(*_args, **_kwargs):
        nonlocal body_called
        body_called = True
        raise AssertionError("invalid web arguments reached the tool body")

    async def capture_spy(**kwargs):
        captures.append(kwargs["tool_name"])

    definition._callable = must_not_run
    isolated_registry._tools["web"] = definition
    monkeypatch.setattr(
        "matrx_ai.tools.executor._capture_tool_argument_validation_failed",
        capture_spy,
    )

    content, result = await executor.execute(
        "web",
        {"action": "search", "queries": [f"query-{i}" for i in range(8)]},
        _make_ctx(),
    )

    assert body_called is False
    assert captures == ["web"]
    assert content
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "invalid_arguments"
    assert "at most 5 items" in result.error.message


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


@pytest.fixture
def isolated_registry():
    """Register fixture tools and clean up after each test so other tests
    don't see them leaking through the singleton."""
    registry = ToolRegistry.get_instance()
    saved = dict(registry._tools)

    yield registry

    registry._tools = saved


@pytest.fixture
def executor(isolated_registry):
    return ToolExecutor(
        registry=isolated_registry,
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )


def _make_ctx() -> ToolContext:
    return ToolContext(
        call_id="call-test",
        tool_name="dummy",
        emitter=_NullEmitter(),
    )


@pytest.fixture
def app_ctx_set():
    """Set an AppContext so the logger doesn't blow up. Only needed for
    tests that progress past the pre-flight check (where logging fires).
    """
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import (
        clear_app_context,
        set_app_context,
    )

    ctx = AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True)
    token = set_app_context(ctx)
    yield ctx
    clear_app_context(token)


# ---------------------------------------------------------------------------
# Pre-flight viable-executor check
# ---------------------------------------------------------------------------


class TestNoViableExecutor:
    """A LOCAL-typed tool with empty function_path AND no client-side
    delegation MUST fail pre-flight rather than attempt dispatch."""

    async def test_unviable_tool_returns_typed_error(
        self, isolated_registry, executor
    ) -> None:
        td = ToolDefinition(
            name="unviable_tool",
            description="server fallback expected, none configured",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path="",  # ← the trap: LOCAL but no implementation
            source_kind="native",
        )
        isolated_registry._tools["unviable_tool"] = td

        ctx = _make_ctx()
        content, result = await executor.execute(
            "unviable_tool", {}, ctx,
            client_tools=frozenset(),  # not in client delegation either
        )

        assert result.success is False
        assert result.error is not None
        assert result.error.error_type == "no_viable_executor"
        assert "unviable_tool" in result.error.message
        assert "no executor available" in result.error.message.lower() or \
               "no viable executor" in result.error.message.lower()

    async def test_delegated_tool_skips_preflight(
        self, isolated_registry, executor, app_ctx_set
    ) -> None:
        """Same tool, but the request envelope has it in client_tools —
        the pre-flight should NOT fire (delegation is a viable executor)."""
        td = ToolDefinition(
            name="delegated_tool",
            description="client-delegated; no server impl needed",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path="",
            source_kind="native",
        )
        isolated_registry._tools["delegated_tool"] = td

        ctx = _make_ctx()
        # The dispatch will progress past pre-flight and try the delegate
        # path, which without a real client connection times out — but
        # that's not what we're testing. We're testing that pre-flight
        # didn't reject. Use a very short max_client_wait_seconds to keep
        # the test fast.
        td.max_client_wait_seconds = 1
        content, result = await executor.execute(
            "delegated_tool", {}, ctx,
            client_tools=frozenset({"delegated_tool"}),
        )
        # Whatever the result, the error_type CANNOT be no_viable_executor
        # because the pre-flight should have skipped this case.
        if result.error is not None:
            assert result.error.error_type != "no_viable_executor", (
                f"pre-flight wrongly rejected a delegated tool: {result.error}"
            )

    async def test_tool_with_function_path_skips_preflight(
        self, isolated_registry, executor, app_ctx_set
    ) -> None:
        """A tool with a non-empty function_path bypasses pre-flight even
        if the import fails later — pre-flight only cares about absence,
        not validity."""
        td = ToolDefinition(
            name="path_set_tool",
            description="server impl declared (may not import successfully)",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path="some.module.path.that.does.not.exist",
            source_kind="native",
        )
        isolated_registry._tools["path_set_tool"] = td

        ctx = _make_ctx()
        content, result = await executor.execute(
            "path_set_tool", {}, ctx,
            client_tools=frozenset(),
        )
        # Will fail at dispatch (bad import), but NOT with no_viable_executor.
        if result.error is not None:
            assert result.error.error_type != "no_viable_executor"

    async def test_external_handler_type_skips_preflight(
        self, isolated_registry, executor, app_ctx_set
    ) -> None:
        """EXTERNAL_HANDLER tools always need a runtime-registered handler;
        pre-flight only gates LOCAL-typed tools."""
        td = ToolDefinition(
            name="ext_handler_tool",
            description="external handler, registered at runtime",
            parameters={},
            tool_type=ToolType.EXTERNAL_HANDLER,
            function_path="",
            source_kind="native",
        )
        isolated_registry._tools["ext_handler_tool"] = td

        ctx = _make_ctx()
        content, result = await executor.execute(
            "ext_handler_tool", {}, ctx,
            client_tools=frozenset(),
        )
        # Whatever happens, pre-flight didn't reject it.
        if result.error is not None:
            assert result.error.error_type != "no_viable_executor"


class TestMustCompleteExecution:
    async def test_soft_timeout_returns_the_real_result(
        self, isolated_registry, executor, app_ctx_set
    ) -> None:
        finished = asyncio.Event()

        async def paid_child(_args: dict[str, Any], _ctx: ToolContext) -> dict[str, Any]:
            await asyncio.sleep(0.04)
            finished.set()
            return {"result": {"status": "finished"}}

        definition = ToolDefinition(
            name="paid_child",
            description="Paid child execution",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path="tests.paid_child",
            timeout_seconds=0.01,
            must_complete=True,
        )
        definition._callable = paid_child
        isolated_registry._tools["paid_child"] = definition

        _content, result = await executor.execute("paid_child", {}, _make_ctx())

        assert finished.is_set()
        assert result.success is True
        assert result.output == {"status": "finished"}

    async def test_request_cancellation_waits_for_real_completion(
        self, isolated_registry, executor, app_ctx_set
    ) -> None:
        started = asyncio.Event()
        finished = asyncio.Event()

        async def paid_child(_args: dict[str, Any], _ctx: ToolContext) -> dict[str, Any]:
            started.set()
            await asyncio.sleep(0.04)
            finished.set()
            return {"result": {"status": "finished"}}

        definition = ToolDefinition(
            name="paid_child",
            description="Paid child execution",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path="tests.paid_child",
            timeout_seconds=10,
            must_complete=True,
        )
        definition._callable = paid_child
        isolated_registry._tools["paid_child"] = definition

        execution = asyncio.create_task(
            executor.execute("paid_child", {}, _make_ctx())
        )
        await started.wait()
        execution.cancel()

        with pytest.raises(asyncio.CancelledError):
            await execution

        assert finished.is_set()
