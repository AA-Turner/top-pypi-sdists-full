"""Execution context factory — assembles ``ExecutionContext`` from config.

Builds the fully-wired ``ExecutionContext`` that node factories receive,
connecting LLM providers, tool registries, and trace emitters.
"""

from __future__ import annotations

import asyncio
import atexit
import concurrent.futures
import logging
import threading
from pathlib import Path
from typing import Any

from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.tracing import LoggingTraceEmitter
from agentic_devtools.orchestration.execution.types import JSONValue, ReasoningResponse

logger = logging.getLogger(__name__)

# Shared single-thread executor used to bridge async coroutines when an event
# loop is already running.  A single worker is intentional: the bridge is
# strictly sequential (one coroutine at a time), so a pool of size > 1 would
# only add overhead without benefit.  Module-level to avoid per-call thread
# creation/teardown under repeated LLM invocations.
_ASYNC_BRIDGE_EXECUTOR: concurrent.futures.ThreadPoolExecutor | None = None
_ASYNC_BRIDGE_THREAD_LOCAL = threading.local()
_ASYNC_BRIDGE_LOCK = threading.Lock()


def _get_async_bridge_executor() -> concurrent.futures.ThreadPoolExecutor:
    """Return (creating if necessary) the module-level async-bridge executor.

    Double-checked locking ensures only one ``ThreadPoolExecutor`` is ever
    created even when multiple threads call this concurrently for the first
    time.
    """
    global _ASYNC_BRIDGE_EXECUTOR
    if _ASYNC_BRIDGE_EXECUTOR is not None:
        return _ASYNC_BRIDGE_EXECUTOR
    with _ASYNC_BRIDGE_LOCK:
        if _ASYNC_BRIDGE_EXECUTOR is None:
            _ASYNC_BRIDGE_EXECUTOR = concurrent.futures.ThreadPoolExecutor(
                max_workers=1,
                thread_name_prefix="async-bridge",
            )
            atexit.register(_ASYNC_BRIDGE_EXECUTOR.shutdown, wait=False)
    return _ASYNC_BRIDGE_EXECUTOR


def _run_async(coro: Any) -> Any:
    """Run provider coroutines on a single dedicated bridge thread.

    This keeps async client lifetimes thread-stable even when callers invoke
    from mixed sync/async contexts. If already executing on the bridge thread,
    execute directly with ``asyncio.run()`` (new loop in the current thread)
    to avoid deadlocking by re-submitting to the same single-worker executor.
    """
    if getattr(_ASYNC_BRIDGE_THREAD_LOCAL, "in_bridge", False):
        return asyncio.run(coro)

    executor = _get_async_bridge_executor()
    future = executor.submit(_run_coroutine_in_bridge_thread, coro)
    return future.result()


def _run_coroutine_in_bridge_thread(coro: Any) -> Any:
    """Run a coroutine on the bridge thread, marking thread-local context."""
    _ASYNC_BRIDGE_THREAD_LOCAL.in_bridge = True
    try:
        return asyncio.run(coro)
    finally:
        _ASYNC_BRIDGE_THREAD_LOCAL.in_bridge = False


class _ReasoningAdapter:
    """Adapts an async ``LLMProvider`` to the sync ``ReasoningProvider`` protocol.

    Translates ``agentic_devtools.orchestration.llm.errors.RetryExhaustedError``
    into ``agentic_devtools.orchestration.execution.exceptions.RetryExhaustedError``
    so downstream node wrappers catch a single execution-layer type.
    """

    def __init__(self, provider: Any) -> None:
        self._provider = provider

    def invoke(
        self,
        prompt: str,
        *,
        tools: list[dict[str, JSONValue]] | None = None,
        output_schema: type | dict[str, Any] | None = None,
        model: str | None = None,
    ) -> ReasoningResponse[JSONValue]:
        """Invoke the LLM synchronously, forwarding all parameters."""
        from agentic_devtools.orchestration.llm.errors import (
            RetryExhaustedError as LLMRetryExhaustedError,
        )
        from agentic_devtools.orchestration.llm.types import LLMMessage

        from ..execution.exceptions import RetryExhaustedError as ExecutionRetryExhaustedError

        messages = [LLMMessage(role="user", content=prompt)]

        # Build extra kwargs to forward to the provider
        extra: dict[str, Any] = {}
        if tools is not None:
            extra["tools"] = tools
        if model is not None:
            extra["model"] = model

        try:
            if output_schema is not None:
                # Use complete_structured with JSON schema
                from pydantic import BaseModel

                if isinstance(output_schema, type) and issubclass(output_schema, BaseModel):
                    schema = output_schema.model_json_schema()
                else:
                    schema = output_schema if isinstance(output_schema, dict) else {}

                response = _run_async(self._provider.complete_structured(messages, schema, **extra))
            else:
                response = _run_async(self._provider.complete(messages, **extra))

            # Convert LLMResponse to ReasoningResponse
            from agentic_devtools.orchestration.execution.types import TokenUsage

            token_usage = None
            if response.usage is not None:
                token_usage = TokenUsage(
                    prompt_tokens=response.usage.input_tokens,
                    completion_tokens=response.usage.output_tokens,
                    total_tokens=response.usage.total_tokens,
                )

            return ReasoningResponse(
                raw_text=response.text,
                parsed_output=None,
                tool_calls=[],
                usage=token_usage,
                model=response.model,
                provider_type=getattr(response.provider_type, "value", response.provider_type),
                latency_ms=response.latency_ms,
                finish_reason=response.finish_reason,
            )

        except LLMRetryExhaustedError as exc:
            error_context = (
                f"{exc}; attempts={exc.attempts}, "
                f"total_wait_seconds={exc.total_wait_seconds}, "
                f"last_status_code={exc.last_status_code}"
            )
            raise ExecutionRetryExhaustedError(
                str(exc),
                attempts=exc.attempts,
                last_error=error_context,
            ) from exc


def build_execution_context(
    *,
    provider: Any | None = None,
    registry: Any | None = None,
    run_id: str = "",
    dry_run: bool = False,
    state_dir: Path | None = None,
) -> ExecutionContext:
    """Build an ``ExecutionContext`` from configuration components.

    Args:
        provider: An ``LLMProvider`` instance (or None for tool-only contexts).
        registry: A ``ConcreteToolRegistry`` instance (or None for LLM-only contexts).
        run_id: Unique run identifier for trace/idempotency scoping.
        dry_run: Whether to enable dry-run mode on tool execution.
        state_dir: State directory for persistent trace output.

    Returns:
        A fully-wired ``ExecutionContext``.
    """
    # Build reasoning adapter
    reasoning: Any
    if provider is not None:
        reasoning = _ReasoningAdapter(provider)
    else:
        reasoning = _NullReasoningProvider()

    # Build tool registry with dry-run support
    tools: Any
    if registry is not None:
        from agentic_devtools.orchestration.tools.executor import ToolExecutor

        dry_run_fn = (lambda: dry_run) if dry_run else None
        tools = ToolExecutor(
            registry,
            correlation_id=run_id,
            dry_run_fn=dry_run_fn,
        )
    else:
        tools = _NullToolRegistry()

    # Build trace emitter
    tracer: Any
    if run_id and state_dir is not None:
        try:
            from .trace_persistence import PersistentTraceEmitter

            tracer = PersistentTraceEmitter(state_dir=state_dir, run_id=run_id)
        except Exception:  # noqa: BLE001
            logger.warning("Failed to create PersistentTraceEmitter, falling back to logging")
            tracer = LoggingTraceEmitter()
    else:
        tracer = LoggingTraceEmitter()

    config: dict[str, JSONValue] = {
        "run_id": run_id,
        "dry_run": dry_run,
    }

    return ExecutionContext(
        reasoning=reasoning,
        tools=tools,
        tracer=tracer,
        config=config,
    )


class _NullReasoningProvider:
    """No-op reasoning provider for tool-only contexts."""

    def invoke(
        self,
        prompt: str,
        *,
        tools: list[dict[str, JSONValue]] | None = None,
        output_schema: type | dict[str, Any] | None = None,
        model: str | None = None,
    ) -> ReasoningResponse[JSONValue]:
        """Raise an error — no LLM provider is configured."""
        raise RuntimeError("No LLM provider configured in this ExecutionContext")


class _NullToolRegistry:
    """No-op tool registry for LLM-only contexts."""

    def invoke(self, tool_name: str, **kwargs: JSONValue) -> JSONValue:
        """Raise an error — no tool registry is configured."""
        raise RuntimeError("No tool registry configured in this ExecutionContext")

    def list_all(self) -> dict:
        """Return empty mapping."""
        return {}

    def get_categories(self) -> list[str]:
        """Return empty list."""
        return []
