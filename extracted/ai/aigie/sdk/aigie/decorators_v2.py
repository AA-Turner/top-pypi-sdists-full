"""
Production-grade decorators with automatic context propagation.

Enterprise features:
- Automatic parent-child relationships via contextvars
- Support for sync/async functions, generators, and async generators
- Streaming support with reduce_fn for aggregating outputs
- Comprehensive error handling with graceful degradation
- Input/output capture from function signatures
"""

import asyncio
import functools
import inspect
import warnings
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar
from uuid import uuid4

warnings.warn(
    "aigie.decorators_v2 is deprecated. Use aigie.decorators_v3 or aigie.observe instead.",
    DeprecationWarning,
    stacklevel=2,
)

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


def _extract_inputs(func: Callable, args: tuple, kwargs: dict) -> dict[str, Any]:
    """
    Extract function inputs from args/kwargs based on signature.

    Args:
        func: Function being called
        args: Positional arguments
        kwargs: Keyword arguments

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
                    inputs[name] = repr(value)[:200]  # Limit length
            except Exception:
                inputs[name] = f"<{type(value).__name__}>"

        return inputs
    except Exception:
        # Fallback: return positional args as dict
        return {"args": str(args)[:200], "kwargs": str(kwargs)[:200]}


def _serialize_output(output: Any) -> Any:
    """
    Serialize function output for storage.

    Args:
        output: Function return value

    Returns:
        Serializable version of output
    """
    try:
        if isinstance(output, (str, int, float, bool, type(None))):
            return output
        if isinstance(output, (list, tuple)):
            return list(output)
        if isinstance(output, dict):
            return output
        return repr(output)[:500]
    except Exception:
        return f"<{type(output).__name__}>"


class traceable:
    """
    Decorator for automatic tracing with context propagation.

    Features:
    - Works with async/sync functions, generators, async generators
    - Automatic parent-child relationships via contextvars
    - Input/output capture
    - Streaming support with reduce_fn
    - Error handling and graceful degradation

    Usage:
        @traceable(name="my_agent", run_type="agent")
        async def my_agent(query: str):
            return await process(query)

        # Without parentheses (uses function name)
        @traceable
        async def my_function():
            pass

        # Streaming with aggregation
        @traceable(run_type="llm", reduce_fn=lambda outputs: "".join(outputs))
        async def stream_llm(prompt: str):
            async for chunk in llm.astream(prompt):
                yield chunk
    """

    def __init__(
        self,
        func: Callable | None = None,
        *,
        name: str | None = None,
        run_type: str = "chain",
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        reduce_fn: Callable[[list[Any]], Any] | None = None,
        project_name: str | None = None,
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
        """
        self.func = func
        self.name = name
        self.run_type = run_type
        self.tags = tags or []
        self.metadata = metadata or {}
        self.reduce_fn = reduce_fn
        self.project_name = project_name

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

            # Import here to avoid circular dependency
            from .client import Aigie

            # Extract inputs
            inputs = _extract_inputs(func, args, kwargs)

            # Get or create aigie client
            # Check if first arg is Aigie instance or has aigie attribute
            if args and hasattr(args[0], "__class__"):
                if isinstance(args[0], Aigie):
                    args[0]
                elif hasattr(args[0], "aigie"):
                    args[0].aigie

            # Merge tags and metadata with global context
            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            # Get parent context
            parent_ctx = get_parent_context()

            # Create run context
            run_id = str(uuid4())
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

            try:
                # Execute function
                result = await func(*args, **kwargs)

                # Serialize output
                output = _serialize_output(result)

                # TODO: Send to API if aigie_client is available
                # For now, just track in context
                run_ctx.metadata["input"] = inputs
                run_ctx.metadata["output"] = output
                run_ctx.metadata["status"] = "success"

                return result

            except Exception as e:
                # Track error
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                raise

            finally:
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

            # For sync functions, we'll track context but not send to API
            # (API calls are async)
            inputs = _extract_inputs(func, args, kwargs)
            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            parent_ctx = get_parent_context()
            run_id = str(uuid4())
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
            )

            prev_span_ctx = get_current_span_context()
            set_current_span_context(run_ctx)

            if not parent_ctx:
                prev_trace_ctx = get_current_trace_context()
                set_current_trace_context(run_ctx)
            else:
                prev_trace_ctx = None

            try:
                result = func(*args, **kwargs)
                output = _serialize_output(result)
                run_ctx.metadata["input"] = inputs
                run_ctx.metadata["output"] = output
                run_ctx.metadata["status"] = "success"
                return result

            except Exception as e:
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                raise

            finally:
                set_current_span_context(prev_span_ctx)
                if prev_trace_ctx is not None:
                    set_current_trace_context(prev_trace_ctx)

        return wrapper

    def _wrap_async_generator(self, func: Callable, name: str):
        """Wrap async generator with streaming support."""

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not is_tracing_enabled():
                async for item in func(*args, **kwargs):
                    yield item
                return

            inputs = _extract_inputs(func, args, kwargs)
            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            parent_ctx = get_parent_context()
            run_id = str(uuid4())
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

            try:
                async for item in func(*args, **kwargs):
                    outputs.append(item)
                    yield item

                # Aggregate outputs if reduce_fn is provided
                final_output = self.reduce_fn(outputs) if self.reduce_fn and outputs else outputs

                run_ctx.metadata["input"] = inputs
                run_ctx.metadata["output"] = _serialize_output(final_output)
                run_ctx.metadata["status"] = "success"
                run_ctx.metadata["stream_count"] = len(outputs)

            except Exception as e:
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                raise

            finally:
                set_current_span_context(prev_span_ctx)
                if prev_trace_ctx is not None:
                    set_current_trace_context(prev_trace_ctx)

        return wrapper

    def _wrap_generator(self, func: Callable, name: str):
        """Wrap synchronous generator."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_tracing_enabled():
                for item in func(*args, **kwargs):
                    yield item
                return

            inputs = _extract_inputs(func, args, kwargs)
            merged_tags = merge_tags(self.tags)
            merged_metadata = merge_metadata(self.metadata)

            parent_ctx = get_parent_context()
            run_id = str(uuid4())
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
            )

            prev_span_ctx = get_current_span_context()
            set_current_span_context(run_ctx)

            if not parent_ctx:
                prev_trace_ctx = get_current_trace_context()
                set_current_trace_context(run_ctx)
            else:
                prev_trace_ctx = None

            outputs = []

            try:
                for item in func(*args, **kwargs):
                    outputs.append(item)
                    yield item

                final_output = self.reduce_fn(outputs) if self.reduce_fn and outputs else outputs

                run_ctx.metadata["input"] = inputs
                run_ctx.metadata["output"] = _serialize_output(final_output)
                run_ctx.metadata["status"] = "success"
                run_ctx.metadata["stream_count"] = len(outputs)

            except Exception as e:
                run_ctx.metadata["error"] = {
                    "type": type(e).__name__,
                    "message": str(e),
                }
                run_ctx.metadata["status"] = "error"
                raise

            finally:
                set_current_span_context(prev_span_ctx)
                if prev_trace_ctx is not None:
                    set_current_trace_context(prev_trace_ctx)

        return wrapper


# Alias for compatibility
trace = traceable
