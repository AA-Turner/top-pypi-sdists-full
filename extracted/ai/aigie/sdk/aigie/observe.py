"""
Simple @observe decorator for automatic function tracing.

Provides a clean, Laminar-style API for tracing functions with minimal configuration.
Works with both sync and async functions, optionally applies metrics.

Usage (Simple - Laminar-style):
    from aigie import observe

    @observe()
    async def my_function(input: str):
        return await process(input)

    @observe(name="custom_name")
    def sync_function(x: int):
        return x * 2

Usage (With Metrics):
    from aigie import observe

    # `metrics` accepts any object exposing
    # `evaluate()`, `name`, `threshold`, and `is_successful()`.
    @observe(metrics=[MyMetric()])
    async def my_agent_function(input: str):
        result = await process(input)
        return result

Usage (With Evaluators):
    from aigie import observe
    from aigie.judges import JudgeType

    @observe(
        name="qa_function",
        judges=[JudgeType.RESPONSE_QUALITY, JudgeType.RELEVANCE],
    )
    async def qa_function(question: str):
        return await generate_answer(question)
"""

import asyncio
import functools
import inspect
import logging
from collections.abc import Callable
from datetime import datetime
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import uuid4

from aigie.context_manager import (
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
from aigie.utils.safe import dont_throw, schedule_async

if TYPE_CHECKING:
    from aigie.judges import JudgeType

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def observe(
    func: Callable | None = None,
    *,
    name: str | None = None,
    span_type: str = "default",
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    metrics: list[Any] | None = None,
    judges: list["JudgeType"] | None = None,
    capture_input: bool = True,
    capture_output: bool = True,
    user_id: str | None = None,
    session_id: str | None = None,
    project_name: str | None = None,
) -> Callable:
    """
    Simple decorator for automatic function tracing (Laminar-style API).

    Can be used with or without parentheses:
        @observe
        def my_function(): ...

        @observe()
        def my_function(): ...

        @observe(name="custom")
        def my_function(): ...

    Args:
        func: Function to decorate (when used without parentheses)
        name: Custom name for the span (defaults to function name)
        span_type: Type of span (llm, tool, agent, chain, etc.)
        tags: Tags to add to the span
        metadata: Additional metadata
        metrics: Optional list of metrics to evaluate
        judges: Optional list of judge types to run
        capture_input: Whether to capture function inputs
        capture_output: Whether to capture function outputs
        user_id: User identifier for session tracking
        session_id: Session identifier for multi-turn conversations
        project_name: Project name for grouping

    Returns:
        Decorated function with automatic tracing
    """

    def decorator(fn: Callable) -> Callable:
        fn_name = name or fn.__name__
        fn_tags = tags or []
        fn_metadata = metadata or {}

        if asyncio.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_wrapper(*args, **kwargs):
                return await _trace_async_function(
                    fn,
                    fn_name,
                    span_type,
                    fn_tags,
                    fn_metadata,
                    metrics,
                    judges,
                    capture_input,
                    capture_output,
                    user_id,
                    session_id,
                    project_name,
                    args,
                    kwargs,
                )

            return async_wrapper

        @functools.wraps(fn)
        def sync_wrapper(*args, **kwargs):
            return _trace_sync_function(
                fn,
                fn_name,
                span_type,
                fn_tags,
                fn_metadata,
                metrics,
                judges,
                capture_input,
                capture_output,
                user_id,
                session_id,
                project_name,
                args,
                kwargs,
            )

        return sync_wrapper

    # Handle both @observe and @observe() syntax
    if func is not None:
        return decorator(func)
    return decorator


async def _trace_async_function(
    func: Callable,
    name: str,
    span_type: str,
    tags: list[str],
    metadata: dict[str, Any],
    metrics: list[Any] | None,
    judges: list["JudgeType"] | None,
    capture_input: bool,
    capture_output: bool,
    user_id: str | None,
    session_id: str | None,
    project_name: str | None,
    args: tuple,
    kwargs: dict,
) -> Any:
    """Execute and trace an async function."""

    # Check if tracing is enabled
    if not is_tracing_enabled():
        return await func(*args, **kwargs)

    # Extract inputs
    inputs = {}
    if capture_input:
        inputs = _extract_inputs(func, args, kwargs)

    # Merge context
    merged_tags = merge_tags(tags)
    merged_metadata = merge_metadata(metadata)

    if user_id:
        merged_metadata["user_id"] = user_id
    if session_id:
        merged_metadata["session_id"] = session_id

    # Get parent context
    parent_ctx = get_parent_context()

    # Create run context
    run_id = str(uuid4())
    run_ctx = RunContext(
        id=run_id,
        name=name,
        type="span",
        span_type=span_type,
        parent_id=parent_ctx.id if parent_ctx else None,
        metadata=merged_metadata,
        tags=merged_tags,
        start_time=datetime.utcnow(),
        project_name=project_name or get_project_name(),
        user_id=user_id,
        session_id=session_id,
    )

    # Set as current context
    prev_span_ctx = get_current_span_context()
    set_current_span_context(run_ctx)

    if not parent_ctx:
        prev_trace_ctx = get_current_trace_context()
        set_current_trace_context(run_ctx)
    else:
        prev_trace_ctx = None

    try:
        # Execute function
        result = await func(*args, **kwargs)

        # Capture output
        output = None
        if capture_output:
            output = _serialize_output(result)

        # Store in metadata
        if capture_input:
            run_ctx.metadata["input"] = inputs
        if capture_output:
            run_ctx.metadata["output"] = output
        run_ctx.metadata["status"] = "success"

        # Run metrics if provided
        if metrics:
            await _run_metrics(metrics, inputs, result, run_ctx)

        # Run judges if provided
        if judges:
            await _run_judges(judges, inputs, result, run_ctx)

        return result

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

        # Queue events
        await _queue_events(run_ctx, parent_ctx)

        # Restore contexts
        set_current_span_context(prev_span_ctx)
        if prev_trace_ctx is not None:
            set_current_trace_context(prev_trace_ctx)


def _trace_sync_function(
    func: Callable,
    name: str,
    span_type: str,
    tags: list[str],
    metadata: dict[str, Any],
    metrics: list[Any] | None,
    judges: list["JudgeType"] | None,
    capture_input: bool,
    capture_output: bool,
    user_id: str | None,
    session_id: str | None,
    project_name: str | None,
    args: tuple,
    kwargs: dict,
) -> Any:
    """Execute and trace a sync function."""

    # Check if tracing is enabled
    if not is_tracing_enabled():
        return func(*args, **kwargs)

    # Extract inputs
    inputs = {}
    if capture_input:
        inputs = _extract_inputs(func, args, kwargs)

    # Merge context
    merged_tags = merge_tags(tags)
    merged_metadata = merge_metadata(metadata)

    if user_id:
        merged_metadata["user_id"] = user_id
    if session_id:
        merged_metadata["session_id"] = session_id

    # Get parent context
    parent_ctx = get_parent_context()

    # Create run context
    run_id = str(uuid4())
    run_ctx = RunContext(
        id=run_id,
        name=name,
        type="span",
        span_type=span_type,
        parent_id=parent_ctx.id if parent_ctx else None,
        metadata=merged_metadata,
        tags=merged_tags,
        start_time=datetime.utcnow(),
        project_name=project_name or get_project_name(),
        user_id=user_id,
        session_id=session_id,
    )

    # Set as current context
    prev_span_ctx = get_current_span_context()
    set_current_span_context(run_ctx)

    if not parent_ctx:
        prev_trace_ctx = get_current_trace_context()
        set_current_trace_context(run_ctx)
    else:
        prev_trace_ctx = None

    try:
        # Execute function
        result = func(*args, **kwargs)

        # Capture output
        output = None
        if capture_output:
            output = _serialize_output(result)

        # Store in metadata
        if capture_input:
            run_ctx.metadata["input"] = inputs
        if capture_output:
            run_ctx.metadata["output"] = output
        run_ctx.metadata["status"] = "success"

        # Note: metrics and judges require async - schedule them
        if metrics or judges:
            _schedule_async_evaluations(metrics, judges, inputs, result, run_ctx)

        return result

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

        # Queue events
        _queue_events_sync(run_ctx, parent_ctx)

        # Restore contexts
        set_current_span_context(prev_span_ctx)
        if prev_trace_ctx is not None:
            set_current_trace_context(prev_trace_ctx)


def _extract_inputs(func: Callable, args: tuple, kwargs: dict) -> dict[str, Any]:
    """Extract function inputs from args/kwargs."""
    try:
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        inputs = {}
        for name, value in bound.arguments.items():
            if name in ("self", "cls"):
                continue
            try:
                if isinstance(value, (str, int, float, bool, type(None))):
                    inputs[name] = value
                elif isinstance(value, (list, tuple)):
                    inputs[name] = list(value)
                elif isinstance(value, dict):
                    inputs[name] = value
                else:
                    inputs[name] = repr(value)[:500]
            except Exception:
                inputs[name] = f"<{type(value).__name__}>"

        return inputs
    except Exception as e:
        logger.debug(f"Input extraction failed: {e}")
        return {"args": str(args)[:200], "kwargs": str(kwargs)[:200]}


def _serialize_output(output: Any) -> Any:
    """Serialize function output."""
    try:
        if isinstance(output, (str, int, float, bool, type(None))):
            return output
        if isinstance(output, (list, tuple)):
            return list(output)
        if isinstance(output, dict):
            return output
        return repr(output)[:1000]
    except Exception:
        return f"<{type(output).__name__}>"


async def _run_metrics(
    metrics: list[Any],
    inputs: dict[str, Any],
    output: Any,
    run_ctx: RunContext,
) -> None:
    """Run metrics and store results."""
    results = []

    for metric in metrics:
        try:
            context = {
                "trace_id": run_ctx.id,
                "span_id": run_ctx.id,
                "function_name": run_ctx.name,
            }

            result = await metric.evaluate(inputs, output, context)

            results.append(
                {
                    "metric_name": metric.name,
                    "score": result.score,
                    "score_type": result.score_type.value,
                    "threshold": metric.threshold,
                    "passed": metric.is_successful(),
                    "explanation": result.explanation,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
        except Exception as e:
            logger.warning(f"Metric {metric.name} failed: {e}")
            results.append(
                {
                    "metric_name": metric.name,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

    if results:
        run_ctx.metadata["evaluations"] = results


async def _run_judges(
    judges: list["JudgeType"],
    inputs: dict[str, Any],
    output: Any,
    run_ctx: RunContext,
) -> None:
    """Run judges and store results."""
    try:
        from aigie.judges import JudgesClient

        async with JudgesClient() as client:
            results = []

            for judge_type in judges:
                try:
                    result = await client.run_judge(
                        input=inputs,
                        output=output,
                        judge_type=judge_type,
                        trace_id=run_ctx.id,
                        span_id=run_ctx.id,
                    )

                    results.append(
                        {
                            "judge_name": result.judge_name,
                            "score": result.score,
                            "passed": result.passed,
                            "reasoning": result.reasoning,
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    )
                except Exception as e:
                    logger.warning(f"Judge {judge_type.value} failed: {e}")

            if results:
                if "evaluations" not in run_ctx.metadata:
                    run_ctx.metadata["evaluations"] = []
                run_ctx.metadata["evaluations"].extend(results)

    except ImportError:
        logger.warning("Judges module not available")


@dont_throw
def _schedule_async_evaluations(
    metrics: list[Any] | None,
    judges: list["JudgeType"] | None,
    inputs: dict[str, Any],
    output: Any,
    run_ctx: RunContext,
) -> None:
    """Schedule async evaluations from sync context."""
    try:
        loop = asyncio.get_running_loop()

        async def run_evals():
            if metrics:
                await _run_metrics(metrics, inputs, output, run_ctx)
            if judges:
                await _run_judges(judges, inputs, output, run_ctx)

        loop.create_task(run_evals())
    except RuntimeError:
        # No running loop - skip evaluations in sync context
        logger.debug("No event loop available for async evaluations")


async def _queue_events(run_ctx: RunContext, parent_ctx: RunContext | None) -> None:
    """Queue trace and span events."""
    try:
        from aigie.client import get_aigie

        aigie = get_aigie()
        if not aigie or not aigie._buffer:
            return

        end_time = datetime.utcnow()

        # Determine trace_id. A root span (no parent) carries trace identity:
        # its span_id == trace_id and parent_span_id is None, so the platform
        # mints the trace row from it — no separate trace event is emitted.
        if not parent_ctx:
            trace_id = run_ctx.id
        else:
            trace_ctx = get_current_trace_context()
            trace_id = trace_ctx.id if trace_ctx else run_ctx.id

        # Queue span event
        span_payload = {
            "id": run_ctx.id,
            "name": run_ctx.name,
            "trace_id": trace_id,
            "parent_span_id": run_ctx.parent_id if run_ctx.parent_id != trace_id else None,
            "type": run_ctx.span_type or "default",
            "start_time": run_ctx.start_time.isoformat()
            if run_ctx.start_time
            else end_time.isoformat(),
            "end_time": end_time.isoformat(),
            "metadata": run_ctx.metadata,
            "tags": run_ctx.tags,
            "input": run_ctx.metadata.get("input"),
            "output": run_ctx.metadata.get("output"),
            "status": run_ctx.metadata.get("status", "success"),
        }

        if run_ctx.user_id:
            span_payload["user_id"] = run_ctx.user_id
        if run_ctx.session_id:
            span_payload["session_id"] = run_ctx.session_id
        if run_ctx.project_name:
            span_payload["project_name"] = run_ctx.project_name

        # "duration_ns" is the key the ingest mapper reads; "duration" is
        # dropped on the floor without an error.
        if run_ctx.start_time:
            duration_ns = int((end_time - run_ctx.start_time).total_seconds() * 1e9)
            span_payload["duration_ns"] = duration_ns

        await aigie._buffer.add(span_payload)

    except Exception as e:
        logger.debug(f"Failed to queue events: {e}")


@dont_throw
def _queue_events_sync(run_ctx: RunContext, parent_ctx: RunContext | None) -> None:
    """Synchronously queue events."""
    schedule_async(_queue_events(run_ctx, parent_ctx))


# Legacy ObserveDecorator class for backward compatibility
class ObserveDecorator:
    """
    Legacy decorator class for backward compatibility.

    Prefer using the simpler @observe() function instead.
    """

    def __init__(
        self,
        metrics: list[Any] | None = None,
        name: str | None = None,
        type: str | None = None,
        run_on: str = "span",
        **kwargs,
    ):
        self.metrics = metrics or []
        self.name = name
        self.span_type = type or "default"
        self.run_on = run_on
        self.metadata = kwargs

    def __call__(self, func: Callable | None = None):
        if func is None:

            def decorator(f):
                return observe(
                    f,
                    name=self.name,
                    span_type=self.span_type,
                    metrics=self.metrics,
                    metadata=self.metadata,
                )

            return decorator
        return observe(
            func,
            name=self.name,
            span_type=self.span_type,
            metrics=self.metrics,
            metadata=self.metadata,
        )
