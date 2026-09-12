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
    captures: list[dict[str, Any]] = []

    async def must_not_run(*_args, **_kwargs):
        nonlocal body_called
        body_called = True
        raise AssertionError("invalid web arguments reached the tool body")

    async def capture_spy(**kwargs):
        captures.append(kwargs)

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
    assert captures[0]["tool_name"] == "web"
    assert captures[0]["validation_error"].errors()[0]["type"] == "too_long"
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
    @pytest.mark.parametrize("tool_name", ("shell_execute", "shell_python"))
    def test_process_tools_preserve_their_declared_deadline(self, tool_name: str) -> None:
        from matrx_ai.tools.executor import _dispatch_timeout_seconds

        definition = ToolDefinition(
            name=tool_name,
            timeout_seconds=0.01,
        )

        assert _dispatch_timeout_seconds(
            definition,
            {"timeout_seconds": 1},
            is_delegated=False,
        ) == 1

    async def test_shell_process_deadline_is_not_cut_off_by_registry_default(
        self, isolated_registry, executor, app_ctx_set
    ) -> None:
        """The declared shell timeout is authoritative up to its Pydantic cap."""
        finished = asyncio.Event()

        async def shell_child(_args: dict[str, Any], _ctx: ToolContext) -> dict[str, Any]:
            await asyncio.sleep(0.04)
            finished.set()
            return {"result": {"status": "finished"}}

        definition = ToolDefinition(
            name="shell_execute",
            description="Shell execution",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path="tests.shell_child",
            timeout_seconds=0.01,
        )
        definition._callable = shell_child
        isolated_registry._tools["shell_execute"] = definition

        _content, result = await executor.execute(
            "shell_execute",
            {"command": "echo bounded", "timeout_seconds": 1},
            _make_ctx(),
        )

        assert finished.is_set()
        assert result.success is True
        assert result.output == {"status": "finished"}

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


async def test_validation_capture_keeps_codes_without_model_content(monkeypatch, app_ctx_set):
    from pydantic import BaseModel, ValidationError, Field
    from matrx_ai.tools.executor import _capture_tool_argument_validation_failed

    class Arguments(BaseModel):
        queries: list[str] = Field(max_length=5)

    with pytest.raises(ValidationError) as failure:
        Arguments(queries=['private-query-sentinel'] * 10)
    captured = []

    async def capture_spy(*args, **kwargs):
        captured.append(kwargs)

    monkeypatch.setattr('matrx_connect.streaming.error_capture.capture_error', capture_spy)
    await _capture_tool_argument_validation_failed(
        ctx=_make_ctx(), tool_name='web', validation_error=failure.value,
    )
    assert captured[0]['kind'] == 'tool_argument_validation_failed'
    assert captured[0]['route'] == 'tool_executor.argument_validation'
    assert captured[0]['error_type'] == 'ToolArgumentValidationError'
    context = captured[0]['context']
    assert context['validation_error_count'] == 1
    assert context['validation_error_codes'] == ['too_long']
    assert context['validation_error_codes_truncated'] is False
    assert 'private-query-sentinel' not in str(captured)
    assert 'queries' not in str(captured)


async def test_validation_capture_hides_custom_code_and_message(monkeypatch, app_ctx_set):
    from pydantic import BaseModel, ValidationError, field_validator
    from pydantic_core import PydanticCustomError
    from matrx_ai.tools.executor import _capture_tool_argument_validation_failed

    class Arguments(BaseModel):
        value: str

        @field_validator('value')
        @classmethod
        def refuse(cls, value):
            raise PydanticCustomError('private-code-sentinel', 'private-message-sentinel')

    with pytest.raises(ValidationError) as failure:
        Arguments(value='private-input-sentinel')
    captured = []

    async def capture_spy(*args, **kwargs):
        captured.append(kwargs)

    monkeypatch.setattr('matrx_connect.streaming.error_capture.capture_error', capture_spy)
    await _capture_tool_argument_validation_failed(
        ctx=_make_ctx(), tool_name='web', validation_error=failure.value,
    )
    assert captured[0]['context']['validation_error_codes'] == ['custom_validation']
    assert 'sentinel' not in str(captured)
