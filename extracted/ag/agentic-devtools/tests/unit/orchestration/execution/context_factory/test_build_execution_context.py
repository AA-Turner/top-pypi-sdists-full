"""Tests for build_execution_context() factory function."""

from __future__ import annotations

import threading
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

import agentic_devtools.orchestration.execution.context_factory as _cf_module
from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.context_factory import (
    _get_async_bridge_executor,
    _NullReasoningProvider,
    _NullToolRegistry,
    _ReasoningAdapter,
    build_execution_context,
)


class TestBuildExecutionContext:
    """Tests for the context factory function."""

    def test_returns_execution_context(self) -> None:
        """Factory returns an ExecutionContext instance."""
        ctx = build_execution_context()
        assert isinstance(ctx, ExecutionContext)

    def test_null_providers_when_no_args(self) -> None:
        """Without provider/registry args, null implementations are used."""
        ctx = build_execution_context()
        assert isinstance(ctx.reasoning, _NullReasoningProvider)
        assert isinstance(ctx.tools, _NullToolRegistry)

    def test_null_reasoning_raises_on_invoke(self) -> None:
        """NullReasoningProvider raises RuntimeError on invoke."""
        provider = _NullReasoningProvider()
        with pytest.raises(RuntimeError, match="No LLM provider configured"):
            provider.invoke("test prompt")

    def test_null_tool_registry_raises_on_invoke(self) -> None:
        """NullToolRegistry raises RuntimeError on invoke."""
        registry = _NullToolRegistry()
        with pytest.raises(RuntimeError, match="No tool registry configured"):
            registry.invoke("test_tool")

    def test_null_tool_registry_list_all(self) -> None:
        """NullToolRegistry.list_all() returns empty dict."""
        registry = _NullToolRegistry()
        assert registry.list_all() == {}

    def test_null_tool_registry_get_categories(self) -> None:
        """NullToolRegistry.get_categories() returns empty list."""
        registry = _NullToolRegistry()
        assert registry.get_categories() == []

    def test_config_contains_run_id_and_dry_run(self) -> None:
        """Context config dict includes run_id and dry_run."""
        ctx = build_execution_context(run_id="test-run-123", dry_run=True)
        assert ctx.config["run_id"] == "test-run-123"
        assert ctx.config["dry_run"] is True

    def test_logging_trace_emitter_fallback(self) -> None:
        """Without state_dir, LoggingTraceEmitter is used."""
        from agentic_devtools.orchestration.execution.tracing import LoggingTraceEmitter

        ctx = build_execution_context(run_id="abc")
        assert isinstance(ctx.tracer, LoggingTraceEmitter)

    def test_persistent_trace_emitter_with_state_dir(self, tmp_path: Path) -> None:
        """With state_dir and run_id, PersistentTraceEmitter is used."""
        from agentic_devtools.orchestration.execution.trace_persistence import PersistentTraceEmitter

        ctx = build_execution_context(run_id="test-run", state_dir=tmp_path)
        assert isinstance(ctx.tracer, PersistentTraceEmitter)

    def test_dry_run_passed_to_tool_executor(self) -> None:
        """dry_run=True creates a ToolExecutor with dry_run_fn."""
        from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry

        registry = ConcreteToolRegistry()
        ctx = build_execution_context(registry=registry, dry_run=True)
        # The tools should be a ToolExecutor with dry_run enabled
        from agentic_devtools.orchestration.tools.executor import ToolExecutor

        assert isinstance(ctx.tools, ToolExecutor)

    def test_provider_creates_reasoning_adapter(self) -> None:
        """Providing a provider wraps it in _ReasoningAdapter."""
        mock_provider = MagicMock()
        ctx = build_execution_context(provider=mock_provider)
        assert isinstance(ctx.reasoning, _ReasoningAdapter)


class TestGetAsyncBridgeExecutor:
    """Tests for the _get_async_bridge_executor() helper."""

    def test_returns_thread_pool_executor(self) -> None:
        """Returns a ThreadPoolExecutor instance."""
        import concurrent.futures

        executor = _get_async_bridge_executor()
        assert isinstance(executor, concurrent.futures.ThreadPoolExecutor)

    def test_returns_same_instance_on_repeated_calls(self) -> None:
        """Covers the cached-executor branch (33→39): second call returns same object."""
        first = _get_async_bridge_executor()
        second = _get_async_bridge_executor()
        assert first is second

    def test_creates_new_executor_when_none(self) -> None:
        """Creates a fresh executor when module-level variable is None."""
        import concurrent.futures

        saved = _cf_module._ASYNC_BRIDGE_EXECUTOR
        try:
            _cf_module._ASYNC_BRIDGE_EXECUTOR = None
            executor = _get_async_bridge_executor()
            assert isinstance(executor, concurrent.futures.ThreadPoolExecutor)
        finally:
            _cf_module._ASYNC_BRIDGE_EXECUTOR = saved

    def test_concurrent_calls_return_same_instance(self) -> None:
        """Concurrent calls during first initialization return the same executor."""
        import concurrent.futures as cf

        saved = _cf_module._ASYNC_BRIDGE_EXECUTOR
        try:
            _cf_module._ASYNC_BRIDGE_EXECUTOR = None
            results: list[cf.ThreadPoolExecutor] = []

            with cf.ThreadPoolExecutor(max_workers=8) as pool:
                futures = [pool.submit(_get_async_bridge_executor) for _ in range(16)]
                results = [f.result() for f in futures]

            assert all(r is results[0] for r in results)
        finally:
            _cf_module._ASYNC_BRIDGE_EXECUTOR = saved

    def test_inner_check_skips_creation_when_executor_set_before_lock(self) -> None:
        """Covers inner double-check branch (44→50): executor set between outer and inner checks.

        Simulates the race where Thread A passes the outer None-check, then Thread B
        acquires the lock first, creates the executor, and releases the lock.  When
        Thread A finally acquires the lock the inner check (line 44) sees a non-None
        executor and must return it without creating a second one.
        """
        import concurrent.futures as cf

        saved_executor = _cf_module._ASYNC_BRIDGE_EXECUTOR
        saved_lock = _cf_module._ASYNC_BRIDGE_LOCK
        sentinel: cf.ThreadPoolExecutor = cf.ThreadPoolExecutor(max_workers=1)
        try:

            class _RaceSimulatingLock:
                """Sets _ASYNC_BRIDGE_EXECUTOR upon lock entry, mimicking Thread B."""

                def __enter__(self) -> _RaceSimulatingLock:
                    _cf_module._ASYNC_BRIDGE_EXECUTOR = sentinel
                    return self

                def __exit__(self, *args: object) -> None:
                    pass

            _cf_module._ASYNC_BRIDGE_EXECUTOR = None  # outer check passes
            _cf_module._ASYNC_BRIDGE_LOCK = _RaceSimulatingLock()  # type: ignore[assignment]

            result = _get_async_bridge_executor()
            assert result is sentinel
        finally:
            _cf_module._ASYNC_BRIDGE_EXECUTOR = saved_executor
            _cf_module._ASYNC_BRIDGE_LOCK = saved_lock
            sentinel.shutdown(wait=False)


class TestReasoningAdapter:
    """Tests for the _ReasoningAdapter class."""

    def test_invoke_calls_provider_complete(self) -> None:
        """invoke() calls provider.complete() when no output_schema."""
        from agentic_devtools.orchestration.llm.types import LLMResponse, ProviderType

        mock_provider = MagicMock()
        mock_response = LLMResponse(
            text='{"result": "test"}',
            model="test-model",
            provider_type=ProviderType.LOCAL_MODEL,
        )
        mock_provider.complete = AsyncMock(return_value=mock_response)

        adapter = _ReasoningAdapter(mock_provider)
        result = adapter.invoke("test prompt")

        assert result.raw_text == '{"result": "test"}'
        mock_provider.complete.assert_called_once()

    def test_invoke_forwards_tools_parameter(self) -> None:
        """invoke() forwards tools= kwarg to provider.complete()."""
        from agentic_devtools.orchestration.execution.types import JSONValue
        from agentic_devtools.orchestration.llm.types import LLMResponse, ProviderType

        mock_provider = MagicMock()
        mock_response = LLMResponse(
            text="ok",
            model="test-model",
            provider_type=ProviderType.LOCAL_MODEL,
        )
        mock_provider.complete = AsyncMock(return_value=mock_response)

        tools: list[dict[str, JSONValue]] = [{"name": "my_tool", "description": "does something"}]
        adapter = _ReasoningAdapter(mock_provider)
        adapter.invoke("test prompt", tools=tools)

        call_kwargs = mock_provider.complete.call_args[1]
        assert call_kwargs.get("tools") == tools

    def test_invoke_forwards_model_parameter(self) -> None:
        """invoke() forwards model= kwarg to provider.complete()."""
        from agentic_devtools.orchestration.llm.types import LLMResponse, ProviderType

        mock_provider = MagicMock()
        mock_response = LLMResponse(
            text="ok",
            model="gpt-4",
            provider_type=ProviderType.LOCAL_MODEL,
        )
        mock_provider.complete = AsyncMock(return_value=mock_response)

        adapter = _ReasoningAdapter(mock_provider)
        adapter.invoke("test prompt", model="gpt-4")

        call_kwargs = mock_provider.complete.call_args[1]
        assert call_kwargs.get("model") == "gpt-4"

    def test_invoke_handles_running_event_loop(self) -> None:
        """invoke() works when called from within a running event loop."""
        import asyncio
        from unittest.mock import patch as mock_patch

        from agentic_devtools.orchestration.llm.types import LLMResponse, ProviderType

        mock_provider = MagicMock()
        mock_response = LLMResponse(
            text="async-context result",
            model="test-model",
            provider_type=ProviderType.LOCAL_MODEL,
        )
        mock_provider.complete = AsyncMock(return_value=mock_response)

        adapter = _ReasoningAdapter(mock_provider)

        # Simulate a running event loop by patching get_running_loop to succeed
        fake_loop = MagicMock(spec=asyncio.AbstractEventLoop)
        with mock_patch("asyncio.get_running_loop", return_value=fake_loop):
            result = adapter.invoke("test prompt")

        assert result.raw_text == "async-context result"

    def test_invoke_translates_retry_exhausted_error(self) -> None:
        """LLM RetryExhaustedError is translated to execution-layer error."""
        from agentic_devtools.orchestration.execution.exceptions import RetryExhaustedError
        from agentic_devtools.orchestration.llm.errors import (
            RetryExhaustedError as LLMRetryExhaustedError,
        )

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(
            side_effect=LLMRetryExhaustedError(
                "test exhaustion",
                attempts=3,
                total_wait_seconds=1.5,
                last_status_code=429,
            )
        )

        adapter = _ReasoningAdapter(mock_provider)
        with pytest.raises(RetryExhaustedError) as exc_info:
            adapter.invoke("test prompt")

        assert exc_info.value.attempts == 3
        assert "attempts=3" in exc_info.value.last_error
        assert "total_wait_seconds=1.5" in exc_info.value.last_error
        assert "last_status_code=429" in exc_info.value.last_error

    def test_invoke_with_pydantic_output_schema(self) -> None:
        """invoke() with Pydantic BaseModel output_schema uses complete_structured."""
        from pydantic import BaseModel

        from agentic_devtools.orchestration.llm.types import LLMResponse, ProviderType, TokenUsage

        class MySchema(BaseModel):
            value: str = ""

        mock_provider = MagicMock()
        mock_response = LLMResponse(
            text='{"value": "hello"}',
            model="test-model",
            provider_type=ProviderType.LOCAL_MODEL,
            usage=TokenUsage(input_tokens=10, output_tokens=5, total_tokens=15),
        )
        mock_provider.complete_structured = AsyncMock(return_value=mock_response)

        adapter = _ReasoningAdapter(mock_provider)
        result = adapter.invoke("test prompt", output_schema=MySchema)

        assert result.raw_text == '{"value": "hello"}'
        assert result.usage is not None
        assert result.usage.prompt_tokens == 10
        assert result.usage.completion_tokens == 5
        assert result.usage.total_tokens == 15
        mock_provider.complete_structured.assert_called_once()

    def test_invoke_with_dict_output_schema(self) -> None:
        """invoke() with a dict output_schema passes it directly."""
        from agentic_devtools.orchestration.llm.types import LLMResponse, ProviderType

        mock_provider = MagicMock()
        mock_response = LLMResponse(
            text='{"result": "ok"}',
            model="test-model",
            provider_type=ProviderType.LOCAL_MODEL,
        )
        mock_provider.complete_structured = AsyncMock(return_value=mock_response)

        adapter = _ReasoningAdapter(mock_provider)
        schema_dict = {"type": "object", "properties": {"result": {"type": "string"}}}
        result = adapter.invoke("test prompt", output_schema=schema_dict)  # type: ignore[arg-type]

        assert result.raw_text == '{"result": "ok"}'
        mock_provider.complete_structured.assert_called_once()

    def test_invoke_with_non_basemodel_type_output_schema(self) -> None:
        """invoke() with a non-BaseModel type uses empty dict as schema."""
        from agentic_devtools.orchestration.llm.types import LLMResponse, ProviderType

        mock_provider = MagicMock()
        mock_response = LLMResponse(
            text="plain text",
            model="test-model",
            provider_type=ProviderType.LOCAL_MODEL,
        )
        mock_provider.complete_structured = AsyncMock(return_value=mock_response)

        adapter = _ReasoningAdapter(mock_provider)
        # Pass a non-BaseModel type (str) as output_schema
        result = adapter.invoke("test prompt", output_schema=str)

        assert result.raw_text == "plain text"
        mock_provider.complete_structured.assert_called_once()
        # The schema arg should be empty dict for non-BaseModel, non-dict types
        call_args = mock_provider.complete_structured.call_args
        assert call_args[0][1] == {}

    def test_persistent_trace_emitter_exception_fallback(self, tmp_path: Path) -> None:
        """Falls back to LoggingTraceEmitter when PersistentTraceEmitter creation fails."""
        from unittest.mock import patch as mock_patch

        from agentic_devtools.orchestration.execution.tracing import LoggingTraceEmitter

        with mock_patch(
            "agentic_devtools.orchestration.execution.trace_persistence.PersistentTraceEmitter",
            side_effect=RuntimeError("simulated failure"),
        ):
            ctx = build_execution_context(run_id="test-run", state_dir=tmp_path)
            assert isinstance(ctx.tracer, LoggingTraceEmitter)


class TestRunAsync:
    """Tests for bridge-thread coroutine execution behavior."""

    def test_runs_on_bridge_thread_when_called_from_main_thread(self) -> None:
        """Coroutines run on the dedicated bridge thread by default."""

        async def _thread_id() -> int:
            return threading.get_ident()

        caller_thread_id = threading.get_ident()
        result_thread_id = _cf_module._run_async(_thread_id())
        assert result_thread_id != caller_thread_id

    def test_runs_directly_when_already_on_bridge_thread(self) -> None:
        """When already on bridge thread, execution is direct (no re-submit)."""

        async def _thread_id() -> int:
            return threading.get_ident()

        _cf_module._ASYNC_BRIDGE_THREAD_LOCAL.in_bridge = True
        try:
            caller_thread_id = threading.get_ident()
            result_thread_id = _cf_module._run_async(_thread_id())
            assert result_thread_id == caller_thread_id
        finally:
            _cf_module._ASYNC_BRIDGE_THREAD_LOCAL.in_bridge = False

    def test_sets_bridge_thread_local_flag_during_executor_execution(self) -> None:
        """Bridge-thread execution marks in_bridge=True for the coroutine lifetime."""

        async def _bridge_state() -> tuple[bool, int]:
            return (
                bool(getattr(_cf_module._ASYNC_BRIDGE_THREAD_LOCAL, "in_bridge", False)),
                threading.get_ident(),
            )

        caller_thread_id = threading.get_ident()
        in_bridge, result_thread_id = _cf_module._run_async(_bridge_state())
        assert in_bridge is True
        assert result_thread_id != caller_thread_id
