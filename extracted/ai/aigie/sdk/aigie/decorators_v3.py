"""
Enhanced @traceable decorator for automatic function tracing.

Features:
- capture_input / capture_output: Control I/O capture
- process_inputs / process_outputs: Custom serialization
- user_id / session_id: User and session tracking
- trace_id: Explicit trace ID control
- client: Pass specific Aigie client instance
- mask: Data masking function for PII protection
- debug: Debug mode for troubleshooting
- completion_start_time: TTFT tracking for streaming
"""

import asyncio
import functools
import inspect
import logging
import os
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar
from uuid import uuid4

from .buffer import EventType
from .context_manager import (
    RunContext,
    get_current_span_context,
    get_current_trace_context,
    get_parent_context,
    get_project_name,
    is_tracing_enabled,
    merge_metadata,
    merge_tags,
    set_current_span_context,
    set_current_trace_context,
)

F = TypeVar("F", bound=Callable[..., Any])

# Global masking function (can be set via client configuration)
_global_mask_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None

# Debug mode flag
_debug_mode: bool = os.getenv("AIGIE_DEBUG", "").lower() in ("true", "1", "yes")

logger = logging.getLogger(__name__)


def set_global_mask_fn(mask_fn: Callable[[dict[str, Any]], dict[str, Any]] | None) -> None:
    """Set global masking function for PII protection."""
    global _global_mask_fn
    _global_mask_fn = mask_fn


def set_debug_mode(enabled: bool) -> None:
    """Enable or disable debug mode."""
    global _debug_mode
    _debug_mode = enabled
    if enabled:
        logging.getLogger("aigie").setLevel(logging.DEBUG)


def _auto_init_if_needed() -> bool:
    """
    Auto-initialize Aigie from environment variables if not already initialized.

    Returns True if a client is available (either existing or newly created).
    """
    from .client import get_aigie, init

    aigie = get_aigie()
    if aigie and aigie._initialized:
        return True

    # Check if we have API key in environment
    api_key = os.getenv("AIGIE_API_KEY")
    if not api_key:
        if _debug_mode:
            logger.debug("[traceable] No AIGIE_API_KEY set - auto-init skipped")
        return False

    try:
        # Auto-initialize with env vars
        init()
        if _debug_mode:
            logger.debug("[traceable] Auto-initialized Aigie from environment variables")
        return True
    except Exception as e:
        if _debug_mode:
            logger.warning(f"[traceable] Auto-init failed: {e}")
        return False


async def _queue_trace_event(run_ctx: "RunContext") -> None:
    """
    Queue a TRACE_CREATE event for root-level operations.

    Args:
        run_ctx: The RunContext with trace data (must be root - no parent)
    """
    try:
        from .client import get_aigie

        # Try auto-init if no client
        if not get_aigie():
            _auto_init_if_needed()

        aigie = get_aigie()
        if not aigie or not aigie._buffer:
            if _debug_mode:
                logger.debug("[traceable] No global Aigie client - skipping trace event")
            return

        end_time = datetime.utcnow()

        # Build trace payload
        trace_payload = {
            "id": run_ctx.id,
            "name": run_ctx.name,
            "start_time": run_ctx.start_time.isoformat()
            if run_ctx.start_time
            else end_time.isoformat(),
            "end_time": end_time.isoformat(),
            "metadata": run_ctx.metadata,
            "tags": run_ctx.tags,
            "input": run_ctx.metadata.get("input"),
            "output": run_ctx.metadata.get("output"),
            "status": "error" if run_ctx.metadata.get("status") == "error" else "success",
        }

        # Add optional fields
        if run_ctx.user_id:
            trace_payload["user_id"] = run_ctx.user_id
        if run_ctx.session_id:
            trace_payload["session_id"] = run_ctx.session_id
        if run_ctx.project_name:
            trace_payload["project_name"] = run_ctx.project_name

        # Calculate duration
        if run_ctx.start_time:
            duration_ns = int((end_time - run_ctx.start_time).total_seconds() * 1e9)
            trace_payload["duration"] = duration_ns

        # Queue trace creation
        await aigie._buffer.add(EventType.TRACE_CREATE, trace_payload)

        if _debug_mode:
            logger.debug(f"[traceable] Queued TRACE event: {run_ctx.name} ({run_ctx.id})")

    except Exception as e:
        if _debug_mode:
            logger.warning(f"[traceable] Failed to queue trace event: {e}")


async def _queue_span_event(run_ctx: "RunContext", trace_id: str, is_create: bool = True) -> None:
    """
    Queue a span event to the global Aigie client buffer.

    Args:
        run_ctx: The RunContext with span data
        trace_id: The trace ID this span belongs to
        is_create: True for SPAN_CREATE, False for SPAN_UPDATE
    """
    try:
        from .client import get_aigie

        # Try auto-init if no client
        if not get_aigie():
            _auto_init_if_needed()

        aigie = get_aigie()
        if not aigie or not aigie._buffer:
            if _debug_mode:
                logger.debug("[traceable] No global Aigie client - skipping event queue")
            return

        end_time = datetime.utcnow()

        # Build span payload - always reference the root trace_id
        payload = {
            "id": run_ctx.id,
            "name": run_ctx.name,
            "trace_id": trace_id,  # Always use the root trace ID
            "parent_span_id": run_ctx.parent_id if run_ctx.parent_id != trace_id else None,
            "type": run_ctx.span_type or "chain",
            "start_time": run_ctx.start_time.isoformat()
            if run_ctx.start_time
            else end_time.isoformat(),
            "end_time": end_time.isoformat(),
            "metadata": run_ctx.metadata,
            "tags": run_ctx.tags,
            "input": run_ctx.metadata.get("input"),
            "output": run_ctx.metadata.get("output"),
            "status": run_ctx.metadata.get("status", "success"),
            "level": run_ctx.metadata.get("level", "DEFAULT"),
        }

        # Add optional fields
        if run_ctx.user_id:
            payload["user_id"] = run_ctx.user_id
        if run_ctx.session_id:
            payload["session_id"] = run_ctx.session_id
        if run_ctx.project_name:
            payload["project_name"] = run_ctx.project_name

        # Calculate duration
        if run_ctx.start_time:
            duration_ns = int((end_time - run_ctx.start_time).total_seconds() * 1e9)
            payload["duration"] = duration_ns

        # Extract LLM-specific fields from metadata and add as direct fields
        # This ensures LLM spans have proper model, token, and cost data
        if run_ctx.span_type == "llm":
            meta = run_ctx.metadata

            # Model name - check multiple possible keys
            model = meta.get("model") or meta.get("model_name") or meta.get("model_id")
            if model:
                payload["model"] = model

            # Token usage - check direct keys and nested token_usage
            token_usage = meta.get("token_usage", {})

            prompt_tokens = (
                meta.get("prompt_tokens")
                or meta.get("input_tokens")
                or token_usage.get("prompt_tokens")
                or token_usage.get("input_tokens")
                or 0
            )
            completion_tokens = (
                meta.get("completion_tokens")
                or meta.get("output_tokens")
                or token_usage.get("completion_tokens")
                or token_usage.get("output_tokens")
                or 0
            )
            total_tokens = (
                meta.get("total_tokens")
                or token_usage.get("total_tokens")
                or (prompt_tokens + completion_tokens)
            )

            if prompt_tokens or completion_tokens or total_tokens:
                payload["prompt_tokens"] = prompt_tokens
                payload["completion_tokens"] = completion_tokens
                payload["total_tokens"] = total_tokens

            # Cost data
            input_cost = meta.get("input_cost") or token_usage.get("input_cost") or 0.0
            output_cost = meta.get("output_cost") or token_usage.get("output_cost") or 0.0
            total_cost = (
                meta.get("total_cost")
                or meta.get("estimated_cost")
                or token_usage.get("total_cost")
                or token_usage.get("estimated_cost")
                or (input_cost + output_cost)
            )

            if input_cost or output_cost or total_cost:
                payload["input_cost"] = input_cost
                payload["output_cost"] = output_cost
                payload["total_cost"] = total_cost

        # Extract error fields from metadata and add as direct fields
        # This ensures errors have proper error_type and error_message
        meta = run_ctx.metadata
        error_info = meta.get("error", {})
        if error_info:
            error_type = error_info.get("type")
            error_message = error_info.get("message")
            if error_type:
                payload["error_type"] = error_type
            if error_message:
                payload["error_message"] = error_message
                payload["status_message"] = error_message  # Also set status_message

        # Queue to buffer
        event_type = EventType.SPAN_CREATE if is_create else EventType.SPAN_UPDATE
        await aigie._buffer.add(event_type, payload)

        if _debug_mode:
            logger.debug(
                f"[traceable] Queued span event: {run_ctx.name} ({run_ctx.id}) -> trace:{trace_id}"
            )

    except Exception as e:
        if _debug_mode:
            logger.warning(f"[traceable] Failed to queue span event: {e}")


def _queue_trace_event_sync(run_ctx: "RunContext") -> None:
    """
    Synchronously queue a trace event (schedules async operation).
    """
    from .utils.safe import schedule_async

    schedule_async(_queue_trace_event(run_ctx))


def _queue_span_event_sync(run_ctx: "RunContext", trace_id: str, is_create: bool = True) -> None:
    """
    Synchronously queue a span event (schedules async operation).

    Args:
        run_ctx: The RunContext with span data
        trace_id: The trace ID this span belongs to
        is_create: True for SPAN_CREATE, False for SPAN_UPDATE
    """
    from .utils.safe import schedule_async

    schedule_async(_queue_span_event(run_ctx, trace_id, is_create))


def _extract_inputs(
    func: Callable,
    args: tuple,
    kwargs: dict,
    process_inputs: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    mask_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Extract function inputs from args/kwargs based on signature.

    Args:
        func: Function being called
        args: Positional arguments
        kwargs: Keyword arguments
        process_inputs: Optional custom serialization function
        mask_fn: Optional masking function for PII protection

    Returns:
        Dictionary mapping parameter names to values
    """
    try:
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        # Convert to dict, serializing complex types
        inputs = {}
        for name, value in bound.arguments.items():
            try:
                # Skip 'self' and 'cls'
                if name in ("self", "cls"):
                    continue

                # Try to serialize
                if isinstance(value, (str, int, float, bool, type(None))):
                    inputs[name] = value
                elif isinstance(value, (list, tuple)):
                    inputs[name] = list(value)
                elif isinstance(value, dict):
                    inputs[name] = value
                else:
                    # For complex objects, use repr
                    inputs[name] = repr(value)[:500]  # Limit length
            except Exception:
                inputs[name] = f"<{type(value).__name__}>"

        # Apply custom processing if provided
        if process_inputs:
            try:
                inputs = process_inputs(inputs)
            except Exception as e:
                if _debug_mode:
                    logger.warning(f"process_inputs failed: {e}")

        # Apply masking if provided (global or local)
        effective_mask_fn = mask_fn or _global_mask_fn
        if effective_mask_fn:
            try:
                inputs = effective_mask_fn(inputs)
            except Exception as e:
                if _debug_mode:
                    logger.warning(f"mask_fn failed on inputs: {e}")

        return inputs
    except Exception as e:
        if _debug_mode:
            logger.warning(f"Input extraction failed: {e}")
        # Fallback: return positional args as dict
        return {"args": str(args)[:200], "kwargs": str(kwargs)[:200]}


def _serialize_output(
    output: Any,
    process_outputs: Callable[..., dict[str, Any]] | None = None,
    mask_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> Any:
    """
    Serialize function output for storage.

    Args:
        output: Function return value
        process_outputs: Optional custom serialization function
        mask_fn: Optional masking function for PII protection

    Returns:
        Serializable version of output
    """
    try:
        # First serialize to basic types
        if isinstance(output, (str, int, float, bool, type(None))):
            serialized = output
        elif isinstance(output, (list, tuple)):
            serialized = list(output)
        elif isinstance(output, dict):
            serialized = output
        else:
            serialized = repr(output)[:1000]

        # Apply custom processing if provided
        if process_outputs:
            try:
                if isinstance(serialized, dict):
                    serialized = process_outputs(serialized)
                else:
                    serialized = process_outputs({"output": serialized})
            except Exception as e:
                if _debug_mode:
                    logger.warning(f"process_outputs failed: {e}")

        # Apply masking if provided
        effective_mask_fn = mask_fn or _global_mask_fn
        if effective_mask_fn and isinstance(serialized, dict):
            try:
                serialized = effective_mask_fn(serialized)
            except Exception as e:
                if _debug_mode:
                    logger.warning(f"mask_fn failed on outputs: {e}")

        return serialized
    except Exception:
        return f"<{type(output).__name__}>"


class traceable:
    """
    Enhanced decorator for automatic tracing.

    Features:
    - Works with async/sync functions, generators, async generators
    - Automatic parent-child relationships via contextvars
    - Input/output capture with optional control
    - Custom input/output processing
    - Data masking for PII protection
    - User/session tracking
    - Explicit trace ID control
    - Debug mode
    - TTFT tracking for streaming

    Usage:
        # Basic usage
        @traceable(name="my_agent", run_type="agent")
        async def my_agent(query: str):
            return await process(query)

        # With I/O capture control
        @traceable(capture_input=False, capture_output=True)
        async def sensitive_function(secret_data):
            return public_result

        # With custom processing
        @traceable(
            process_inputs=lambda x: {k: v for k, v in x.items() if k != "password"},
            process_outputs=lambda x: {"summary": x.get("result", "")[:100]}
        )
        async def my_function(password, query):
            return {"result": "...long result..."}

        # With data masking
        @traceable(mask=lambda x: mask_pii(x))
        async def customer_support(customer_email, query):
            return response

        # With user/session tracking
        @traceable(user_id="user_123", session_id="session_456")
        async def chat_turn(message):
            return response

        # With explicit trace ID
        @traceable(trace_id="custom-trace-id-123")
        async def my_workflow():
            pass

        # Streaming with TTFT tracking
        @traceable(run_type="llm", reduce_fn=lambda x: "".join(x))
        async def stream_llm(prompt: str):
            async for chunk in llm.astream(prompt):
                yield chunk
    """

    def __init__(
        self,
        func: Callable | None = None,
        *,
        # Core parameters (existing)
        name: str | None = None,
        run_type: str = "chain",
        as_type: str | None = None,  # Alias for run_type
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        reduce_fn: Callable[[list[Any]], Any] | None = None,
        project_name: str | None = None,
        # I/O capture control
        capture_input: bool = True,
        capture_output: bool = True,
        # Custom processing
        process_inputs: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
        process_outputs: Callable[..., dict[str, Any]] | None = None,
        # NEW: Data masking
        mask: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
        # NEW: User/session tracking
        user_id: str | None = None,
        session_id: str | None = None,
        # NEW: Explicit trace ID control
        trace_id: str | None = None,
        # NEW: Client instance
        client: Any | None = None,  # Aigie client
        # NEW: Debug mode
        debug: bool | None = None,
    ):
        """
        Initialize traceable decorator.

        Args:
            func: Function to decorate (when used without parentheses)
            name: Custom name for the run (defaults to function name)
            run_type: Type of run ("chain", "llm", "tool", "agent", "retriever")
            tags: Tags to add to the run
            metadata: Metadata to add to the run
            reduce_fn: Function to aggregate streaming outputs
            project_name: Project name for grouping
            capture_input: Whether to capture function inputs (default: True)
            capture_output: Whether to capture function outputs (default: True)
            process_inputs: Custom function to process/serialize inputs
            process_outputs: Custom function to process/serialize outputs
            mask: Function to mask sensitive data (PII protection)
            user_id: User identifier for session tracking
            session_id: Session identifier for multi-turn conversations
            trace_id: Explicit trace ID (overrides auto-generated ID)
            client: Specific Aigie client instance to use
            debug: Enable debug mode for this function
        """
        self.func = func
        self.name = name
        self.run_type = as_type or run_type  # as_type takes precedence
        self.tags = tags or []
        self.metadata = metadata or {}
        self.reduce_fn = reduce_fn
        self.project_name = project_name

        # New parameters
        self.capture_input = capture_input
        self.capture_output = capture_output
        self.process_inputs = process_inputs
        self.process_outputs = process_outputs
        self.mask = mask
        self.user_id = user_id
        self.session_id = session_id
        self.trace_id = trace_id
        self.client = client
        self.debug = debug if debug is not None else _debug_mode

    def __call__(self, *args, **kwargs):
        """Handle both decorator usage patterns."""
        # If func is not set, we're being called with arguments
        if self.func is None:
            # First argument should be the function
            if len(args) == 1 and callable(args[0]) and not kwargs:
                self.func = args[0]
                return self._create_wrapper()
            raise ValueError("traceable must be called with a function or as a decorator")

        # Otherwise, we're calling the wrapped function
        return self._create_wrapper()(*args, **kwargs)

    def _create_wrapper(self):
        """Create the appropriate wrapper based on function type."""
        func = self.func
        name = self.name or func.__name__

        # Check function type
        if inspect.isasyncgenfunction(func):
            return self._wrap_async_generator(func, name)
        if asyncio.iscoroutinefunction(func):
            return self._wrap_async(func, name)
        if inspect.isgeneratorfunction(func):
            return self._wrap_generator(func, name)
        return self._wrap_sync(func, name)

    def _wrap_async(self, func: Callable, name: str):
        """Wrap async function."""

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Check if tracing is enabled
            if not is_tracing_enabled():
                return await func(*args, **kwargs)

            # Extract inputs (respecting capture_input setting)
            inputs = {}
            if self.capture_input:
                inputs = _extract_inputs(
                    func, args, kwargs, process_inputs=self.process_inputs, mask_fn=self.mask
                )

            # Merge tags and metadata with global context
            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            # Add user/session to metadata
            if self.user_id:
                merged_metadata["user_id"] = self.user_id
            if self.session_id:
                merged_metadata["session_id"] = self.session_id

            # Get parent context
            parent_ctx = get_parent_context()

            # Create run context with explicit or auto-generated ID
            run_id = self.trace_id or str(uuid4())
            run_ctx = RunContext(
                id=run_id,
                name=name,
                type="span",
                span_type=self.run_type,
                parent_id=parent_ctx.id if parent_ctx else None,
                metadata=merged_metadata,
                tags=merged_tags,
                start_time=datetime.utcnow(),
                project_name=self.project_name or get_project_name(),
                user_id=self.user_id,
                session_id=self.session_id,
            )

            # Set as current span context
            prev_span_ctx = get_current_span_context()
            set_current_span_context(run_ctx)

            # If no parent, also set as trace context
            if not parent_ctx:
                prev_trace_ctx = get_current_trace_context()
                set_current_trace_context(run_ctx)
            else:
                prev_trace_ctx = None

            # Debug logging
            if self.debug:
                logger.debug(f"[traceable] Starting {name} (id={run_id}, type={self.run_type})")
                if inputs:
                    logger.debug(f"[traceable] Inputs: {inputs}")

            try:
                # Execute function
                result = await func(*args, **kwargs)

                # Detect Starlette StreamingResponse — mark as streaming
                # Note: output capture is not possible here because the span event
                # is queued in the finally block before the iterator is consumed.
                # The body_iterator passes through unchanged for the consumer.
                if type(result).__name__ == "StreamingResponse" and hasattr(
                    result, "body_iterator"
                ):
                    run_ctx.metadata["status"] = "success"
                    run_ctx.metadata["streaming_response"] = True
                    return result

                # Extract usage_metadata from LangChain messages (Gemini returns tokens here)
                # This must happen BEFORE serialization to capture token counts
                if result is not None and self.run_type == "llm":
                    # Check for usage_metadata attribute (LangChain AIMessage)
                    if hasattr(result, "usage_metadata") and result.usage_metadata:
                        usage = result.usage_metadata
                        if isinstance(usage, dict):
                            run_ctx.metadata["input_tokens"] = usage.get("input_tokens", 0)
                            run_ctx.metadata["output_tokens"] = usage.get("output_tokens", 0)
                            run_ctx.metadata["total_tokens"] = usage.get("total_tokens", 0)
                        elif hasattr(usage, "input_tokens"):
                            # Object-style access
                            run_ctx.metadata["input_tokens"] = getattr(usage, "input_tokens", 0)
                            run_ctx.metadata["output_tokens"] = getattr(usage, "output_tokens", 0)
                            run_ctx.metadata["total_tokens"] = getattr(usage, "total_tokens", 0)

                        if self.debug:
                            logger.debug(
                                f"[traceable] Extracted tokens: input={run_ctx.metadata.get('input_tokens')}, output={run_ctx.metadata.get('output_tokens')}"
                            )

                    # Also check response_metadata (some LangChain models put it here)
                    elif hasattr(result, "response_metadata") and result.response_metadata:
                        resp_meta = result.response_metadata
                        if "token_usage" in resp_meta:
                            token_usage = resp_meta["token_usage"]
                            run_ctx.metadata["input_tokens"] = token_usage.get("prompt_tokens", 0)
                            run_ctx.metadata["output_tokens"] = token_usage.get(
                                "completion_tokens", 0
                            )
                            run_ctx.metadata["total_tokens"] = token_usage.get("total_tokens", 0)
                        elif "usage" in resp_meta:
                            usage = resp_meta["usage"]
                            run_ctx.metadata["input_tokens"] = usage.get(
                                "input_tokens", usage.get("prompt_tokens", 0)
                            )
                            run_ctx.metadata["output_tokens"] = usage.get(
                                "output_tokens", usage.get("completion_tokens", 0)
                            )
                            run_ctx.metadata["total_tokens"] = usage.get("total_tokens", 0)

                # Serialize output (respecting capture_output setting)
                output = None
                if self.capture_output:
                    output = _serialize_output(
                        result, process_outputs=self.process_outputs, mask_fn=self.mask
                    )

                # Store in context metadata
                # Track tool call in parent span for plan adherence
                if self.run_type == "tool" and parent_ctx:
                    if prev_span_ctx and hasattr(prev_span_ctx, "actual_tools_called"):
                        prev_span_ctx.actual_tools_called.append(name)

                # Include plan adherence data if tools were tracked
                if run_ctx.actual_tools_called:
                    run_ctx.metadata["actual_tools_called"] = run_ctx.actual_tools_called
                    run_ctx.metadata["plan_adherence_score"] = run_ctx.plan_adherence_score
                    if run_ctx.unexpected_tools:
                        run_ctx.metadata["unexpected_tools"] = run_ctx.unexpected_tools
                    if run_ctx.is_potential_stuck_loop:
                        run_ctx.metadata["is_potential_stuck_loop"] = True

                if self.capture_input:
                    run_ctx.metadata["input"] = inputs
                if self.capture_output:
                    run_ctx.metadata["output"] = output
                run_ctx.metadata["status"] = "success"

                if self.debug:
                    logger.debug(f"[traceable] Completed {name} successfully")
                    if output:
                        logger.debug(f"[traceable] Output: {str(output)[:200]}")

                return result

            except Exception as e:
                # Track error
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                run_ctx.metadata["level"] = "ERROR"

                if self.debug:
                    logger.debug(f"[traceable] {name} failed: {type(e).__name__}: {e}")

                raise

            finally:
                # Calculate duration
                run_ctx.metadata["duration_ms"] = (
                    (datetime.utcnow() - run_ctx.start_time).total_seconds() * 1000
                    if run_ctx.start_time
                    else None
                )

                # Determine trace_id: if this is a root span, use its own ID as trace_id
                # Otherwise, get trace_id from the trace context
                if not parent_ctx:
                    # This is a root span - create trace event first
                    trace_id = run_ctx.id
                    await _queue_trace_event(run_ctx)
                else:
                    # Get trace_id from trace context
                    trace_ctx = get_current_trace_context()
                    trace_id = trace_ctx.id if trace_ctx else run_ctx.id

                # Queue span event to buffer for API submission
                await _queue_span_event(run_ctx, trace_id, is_create=True)

                # Restore previous contexts
                set_current_span_context(prev_span_ctx)
                if prev_trace_ctx is not None:
                    set_current_trace_context(prev_trace_ctx)

        return wrapper

    def _wrap_sync(self, func: Callable, name: str):
        """Wrap synchronous function."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if tracing is enabled
            if not is_tracing_enabled():
                return func(*args, **kwargs)

            # Extract inputs (respecting capture_input setting)
            inputs = {}
            if self.capture_input:
                inputs = _extract_inputs(
                    func, args, kwargs, process_inputs=self.process_inputs, mask_fn=self.mask
                )

            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            # Add user/session to metadata
            if self.user_id:
                merged_metadata["user_id"] = self.user_id
            if self.session_id:
                merged_metadata["session_id"] = self.session_id

            parent_ctx = get_parent_context()
            run_id = self.trace_id or str(uuid4())
            run_ctx = RunContext(
                id=run_id,
                name=name,
                type="span",
                span_type=self.run_type,
                parent_id=parent_ctx.id if parent_ctx else None,
                metadata=merged_metadata,
                tags=merged_tags,
                start_time=datetime.utcnow(),
                project_name=self.project_name or get_project_name(),
                user_id=self.user_id,
                session_id=self.session_id,
            )

            prev_span_ctx = get_current_span_context()
            set_current_span_context(run_ctx)

            if not parent_ctx:
                prev_trace_ctx = get_current_trace_context()
                set_current_trace_context(run_ctx)
            else:
                prev_trace_ctx = None

            if self.debug:
                logger.debug(f"[traceable] Starting {name} (id={run_id}, type={self.run_type})")

            try:
                result = func(*args, **kwargs)

                # Detect Starlette StreamingResponse — mark as streaming
                # Note: output capture not possible here (span queued before iterator consumed)
                if type(result).__name__ == "StreamingResponse" and hasattr(
                    result, "body_iterator"
                ):
                    run_ctx.metadata["status"] = "success"
                    run_ctx.metadata["streaming_response"] = True
                    return result

                # Extract usage_metadata from LangChain messages (Gemini returns tokens here)
                # This must happen BEFORE serialization to capture token counts
                if result is not None and self.run_type == "llm":
                    # Check for usage_metadata attribute (LangChain AIMessage)
                    if hasattr(result, "usage_metadata") and result.usage_metadata:
                        usage = result.usage_metadata
                        if isinstance(usage, dict):
                            run_ctx.metadata["input_tokens"] = usage.get("input_tokens", 0)
                            run_ctx.metadata["output_tokens"] = usage.get("output_tokens", 0)
                            run_ctx.metadata["total_tokens"] = usage.get("total_tokens", 0)
                        elif hasattr(usage, "input_tokens"):
                            # Object-style access
                            run_ctx.metadata["input_tokens"] = getattr(usage, "input_tokens", 0)
                            run_ctx.metadata["output_tokens"] = getattr(usage, "output_tokens", 0)
                            run_ctx.metadata["total_tokens"] = getattr(usage, "total_tokens", 0)

                        if self.debug:
                            logger.debug(
                                f"[traceable] Extracted tokens: input={run_ctx.metadata.get('input_tokens')}, output={run_ctx.metadata.get('output_tokens')}"
                            )

                    # Also check response_metadata (some LangChain models put it here)
                    elif hasattr(result, "response_metadata") and result.response_metadata:
                        resp_meta = result.response_metadata
                        if "token_usage" in resp_meta:
                            token_usage = resp_meta["token_usage"]
                            run_ctx.metadata["input_tokens"] = token_usage.get("prompt_tokens", 0)
                            run_ctx.metadata["output_tokens"] = token_usage.get(
                                "completion_tokens", 0
                            )
                            run_ctx.metadata["total_tokens"] = token_usage.get("total_tokens", 0)
                        elif "usage" in resp_meta:
                            usage = resp_meta["usage"]
                            run_ctx.metadata["input_tokens"] = usage.get(
                                "input_tokens", usage.get("prompt_tokens", 0)
                            )
                            run_ctx.metadata["output_tokens"] = usage.get(
                                "output_tokens", usage.get("completion_tokens", 0)
                            )
                            run_ctx.metadata["total_tokens"] = usage.get("total_tokens", 0)

                output = None
                if self.capture_output:
                    output = _serialize_output(
                        result, process_outputs=self.process_outputs, mask_fn=self.mask
                    )

                # Track tool call in parent span for plan adherence
                if self.run_type == "tool" and parent_ctx:
                    if prev_span_ctx and hasattr(prev_span_ctx, "actual_tools_called"):
                        prev_span_ctx.actual_tools_called.append(name)

                # Include plan adherence data if tools were tracked
                if run_ctx.actual_tools_called:
                    run_ctx.metadata["actual_tools_called"] = run_ctx.actual_tools_called
                    run_ctx.metadata["plan_adherence_score"] = run_ctx.plan_adherence_score
                    if run_ctx.unexpected_tools:
                        run_ctx.metadata["unexpected_tools"] = run_ctx.unexpected_tools
                    if run_ctx.is_potential_stuck_loop:
                        run_ctx.metadata["is_potential_stuck_loop"] = True

                if self.capture_input:
                    run_ctx.metadata["input"] = inputs
                if self.capture_output:
                    run_ctx.metadata["output"] = output
                run_ctx.metadata["status"] = "success"

                if self.debug:
                    logger.debug(f"[traceable] Completed {name} successfully")

                return result

            except Exception as e:
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                run_ctx.metadata["level"] = "ERROR"

                if self.debug:
                    logger.debug(f"[traceable] {name} failed: {type(e).__name__}: {e}")

                raise

            finally:
                run_ctx.metadata["duration_ms"] = (
                    (datetime.utcnow() - run_ctx.start_time).total_seconds() * 1000
                    if run_ctx.start_time
                    else None
                )

                # Determine trace_id: if this is a root span, use its own ID as trace_id
                # Otherwise, get trace_id from the trace context
                if not parent_ctx:
                    # This is a root span - create trace event first
                    trace_id = run_ctx.id
                    _queue_trace_event_sync(run_ctx)
                else:
                    # Get trace_id from trace context
                    trace_ctx = get_current_trace_context()
                    trace_id = trace_ctx.id if trace_ctx else run_ctx.id

                # Queue span event to buffer for API submission
                _queue_span_event_sync(run_ctx, trace_id, is_create=True)

                set_current_span_context(prev_span_ctx)
                if prev_trace_ctx is not None:
                    set_current_trace_context(prev_trace_ctx)

        return wrapper

    def _wrap_async_generator(self, func: Callable, name: str):
        """Wrap async generator with streaming support and TTFT tracking."""

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not is_tracing_enabled():
                async for item in func(*args, **kwargs):
                    yield item
                return

            inputs = {}
            if self.capture_input:
                inputs = _extract_inputs(
                    func, args, kwargs, process_inputs=self.process_inputs, mask_fn=self.mask
                )

            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            if self.user_id:
                merged_metadata["user_id"] = self.user_id
            if self.session_id:
                merged_metadata["session_id"] = self.session_id

            parent_ctx = get_parent_context()
            run_id = self.trace_id or str(uuid4())
            run_ctx = RunContext(
                id=run_id,
                name=name,
                type="span",
                span_type=self.run_type,
                parent_id=parent_ctx.id if parent_ctx else None,
                metadata=merged_metadata,
                tags=merged_tags,
                start_time=datetime.utcnow(),
                project_name=self.project_name or get_project_name(),
                user_id=self.user_id,
                session_id=self.session_id,
            )

            prev_span_ctx = get_current_span_context()
            set_current_span_context(run_ctx)

            if not parent_ctx:
                prev_trace_ctx = get_current_trace_context()
                set_current_trace_context(run_ctx)
            else:
                prev_trace_ctx = None

            # Collect outputs for aggregation
            outputs = []
            first_token_time = None  # TTFT tracking

            if self.debug:
                logger.debug(f"[traceable] Starting streaming {name} (id={run_id})")

            try:
                async for item in func(*args, **kwargs):
                    # Track time to first token (TTFT)
                    if first_token_time is None:
                        first_token_time = datetime.utcnow()
                        run_ctx.metadata["completion_start_time"] = first_token_time.isoformat()

                        # Calculate TTFT in milliseconds
                        if run_ctx.start_time:
                            ttft_ms = (first_token_time - run_ctx.start_time).total_seconds() * 1000
                            run_ctx.metadata["time_to_first_token_ms"] = ttft_ms

                            if self.debug:
                                logger.debug(f"[traceable] TTFT: {ttft_ms:.2f}ms")

                    outputs.append(item)

                    # Track inter-token timing for streaming analysis
                    if len(outputs) > 1 and first_token_time:
                        elapsed_ms = (datetime.utcnow() - first_token_time).total_seconds() * 1000
                        if "token_timing_ms" not in run_ctx.metadata:
                            run_ctx.metadata["token_timing_ms"] = []
                        run_ctx.metadata["token_timing_ms"].append(round(elapsed_ms, 2))

                    yield item

                # Aggregate outputs if reduce_fn is provided
                final_output = self.reduce_fn(outputs) if self.reduce_fn and outputs else outputs

                # Track tool call in parent span for plan adherence
                if self.run_type == "tool" and parent_ctx:
                    if prev_span_ctx and hasattr(prev_span_ctx, "actual_tools_called"):
                        prev_span_ctx.actual_tools_called.append(name)

                # Include plan adherence data if tools were tracked
                if run_ctx.actual_tools_called:
                    run_ctx.metadata["actual_tools_called"] = run_ctx.actual_tools_called
                    run_ctx.metadata["plan_adherence_score"] = run_ctx.plan_adherence_score
                    if run_ctx.unexpected_tools:
                        run_ctx.metadata["unexpected_tools"] = run_ctx.unexpected_tools
                    if run_ctx.is_potential_stuck_loop:
                        run_ctx.metadata["is_potential_stuck_loop"] = True

                if self.capture_input:
                    run_ctx.metadata["input"] = inputs
                if self.capture_output:
                    run_ctx.metadata["output"] = _serialize_output(
                        final_output, process_outputs=self.process_outputs, mask_fn=self.mask
                    )
                run_ctx.metadata["status"] = "success"
                run_ctx.metadata["stream_count"] = len(outputs)

                if self.debug:
                    logger.debug(f"[traceable] Streaming {name} completed ({len(outputs)} chunks)")

            except Exception as e:
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                run_ctx.metadata["level"] = "ERROR"

                if self.debug:
                    logger.debug(f"[traceable] Streaming {name} failed: {e}")

                raise

            finally:
                run_ctx.metadata["duration_ms"] = (
                    (datetime.utcnow() - run_ctx.start_time).total_seconds() * 1000
                    if run_ctx.start_time
                    else None
                )

                # Determine trace_id: if this is a root span, use its own ID as trace_id
                # Otherwise, get trace_id from the trace context
                if not parent_ctx:
                    # This is a root span - create trace event first
                    trace_id = run_ctx.id
                    await _queue_trace_event(run_ctx)
                else:
                    # Get trace_id from trace context
                    trace_ctx = get_current_trace_context()
                    trace_id = trace_ctx.id if trace_ctx else run_ctx.id

                # Queue span event to buffer for API submission
                await _queue_span_event(run_ctx, trace_id, is_create=True)

                set_current_span_context(prev_span_ctx)
                if prev_trace_ctx is not None:
                    set_current_trace_context(prev_trace_ctx)

        return wrapper

    def _wrap_generator(self, func: Callable, name: str):
        """Wrap synchronous generator with TTFT tracking."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_tracing_enabled():
                for item in func(*args, **kwargs):
                    yield item
                return

            inputs = {}
            if self.capture_input:
                inputs = _extract_inputs(
                    func, args, kwargs, process_inputs=self.process_inputs, mask_fn=self.mask
                )

            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            if self.user_id:
                merged_metadata["user_id"] = self.user_id
            if self.session_id:
                merged_metadata["session_id"] = self.session_id

            parent_ctx = get_parent_context()
            run_id = self.trace_id or str(uuid4())
            run_ctx = RunContext(
                id=run_id,
                name=name,
                type="span",
                span_type=self.run_type,
                parent_id=parent_ctx.id if parent_ctx else None,
                metadata=merged_metadata,
                tags=merged_tags,
                start_time=datetime.utcnow(),
                project_name=self.project_name or get_project_name(),
                user_id=self.user_id,
                session_id=self.session_id,
            )

            prev_span_ctx = get_current_span_context()
            set_current_span_context(run_ctx)

            if not parent_ctx:
                prev_trace_ctx = get_current_trace_context()
                set_current_trace_context(run_ctx)
            else:
                prev_trace_ctx = None

            outputs = []
            first_token_time = None

            try:
                for item in func(*args, **kwargs):
                    # Track TTFT
                    if first_token_time is None:
                        first_token_time = datetime.utcnow()
                        run_ctx.metadata["completion_start_time"] = first_token_time.isoformat()
                        if run_ctx.start_time:
                            ttft_ms = (first_token_time - run_ctx.start_time).total_seconds() * 1000
                            run_ctx.metadata["time_to_first_token_ms"] = ttft_ms

                    outputs.append(item)

                    # Track inter-token timing for streaming analysis
                    if len(outputs) > 1 and first_token_time:
                        elapsed_ms = (datetime.utcnow() - first_token_time).total_seconds() * 1000
                        if "token_timing_ms" not in run_ctx.metadata:
                            run_ctx.metadata["token_timing_ms"] = []
                        run_ctx.metadata["token_timing_ms"].append(round(elapsed_ms, 2))

                    yield item

                final_output = self.reduce_fn(outputs) if self.reduce_fn and outputs else outputs

                # Track tool call in parent span for plan adherence
                if self.run_type == "tool" and parent_ctx:
                    if prev_span_ctx and hasattr(prev_span_ctx, "actual_tools_called"):
                        prev_span_ctx.actual_tools_called.append(name)

                # Include plan adherence data if tools were tracked
                if run_ctx.actual_tools_called:
                    run_ctx.metadata["actual_tools_called"] = run_ctx.actual_tools_called
                    run_ctx.metadata["plan_adherence_score"] = run_ctx.plan_adherence_score
                    if run_ctx.unexpected_tools:
                        run_ctx.metadata["unexpected_tools"] = run_ctx.unexpected_tools
                    if run_ctx.is_potential_stuck_loop:
                        run_ctx.metadata["is_potential_stuck_loop"] = True

                if self.capture_input:
                    run_ctx.metadata["input"] = inputs
                if self.capture_output:
                    run_ctx.metadata["output"] = _serialize_output(
                        final_output, process_outputs=self.process_outputs, mask_fn=self.mask
                    )
                run_ctx.metadata["status"] = "success"
                run_ctx.metadata["stream_count"] = len(outputs)

            except Exception as e:
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                run_ctx.metadata["level"] = "ERROR"
                raise

            finally:
                run_ctx.metadata["duration_ms"] = (
                    (datetime.utcnow() - run_ctx.start_time).total_seconds() * 1000
                    if run_ctx.start_time
                    else None
                )

                # Determine trace_id: if this is a root span, use its own ID as trace_id
                # Otherwise, get trace_id from the trace context
                if not parent_ctx:
                    # This is a root span - create trace event first
                    trace_id = run_ctx.id
                    _queue_trace_event_sync(run_ctx)
                else:
                    # Get trace_id from trace context
                    trace_ctx = get_current_trace_context()
                    trace_id = trace_ctx.id if trace_ctx else run_ctx.id

                # Queue span event to buffer for API submission
                _queue_span_event_sync(run_ctx, trace_id, is_create=True)

                set_current_span_context(prev_span_ctx)
                if prev_trace_ctx is not None:
                    set_current_trace_context(prev_trace_ctx)

        return wrapper


# Convenience function to create decorator with client
def create_traceable(client: Any) -> type:
    """
    Create a traceable decorator bound to a specific client.

    Usage:
        aigie = Aigie()
        await aigie.initialize()

        traceable = create_traceable(aigie)

        @traceable(name="my_function")
        async def my_function():
            pass
    """

    class BoundTraceable(traceable):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("client", client)
            super().__init__(*args, **kwargs)

    return BoundTraceable


# Alias for compatibility
trace = traceable
observe = traceable  # Alias
