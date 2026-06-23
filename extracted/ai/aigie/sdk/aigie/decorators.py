"""
Decorator utilities for Aigie SDK.
"""

import asyncio
import functools
import warnings
from collections.abc import Callable
from typing import Any

warnings.warn(
    "aigie.decorators is deprecated. Use aigie.decorators_v3 or aigie.observe instead.",
    DeprecationWarning,
    stacklevel=2,
)


class TraceDecorator:
    """
    Decorator class for tracing functions.

    Supports both:
    - @aigie.trace (no parentheses)
    - @aigie.trace(name="function") (with parentheses)
    """

    def __init__(
        self,
        aigie_client,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ):
        self.aigie = aigie_client
        self.name = name
        self.metadata = metadata or {}
        self.tags = tags or []

    def __call__(
        self,
        func: Callable | None = None,
        *,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ):
        """
        Called when decorator is used.

        If func is provided, it's being used as @aigie.trace (no parentheses)
        If func is None, it's being used as @aigie.trace() (with parentheses)
        """
        # If called with keyword args, update them
        if name is not None:
            self.name = name
        if metadata is not None:
            self.metadata = metadata
        if tags is not None:
            self.tags = tags

        # If func is provided, we're decorating it directly
        if func is not None:
            return self._decorate(func)

        # Otherwise, return a decorator function
        def decorator(f):
            return self._decorate(f)

        return decorator

    def _decorate(self, func: Callable):
        """Internal method to create the decorated function."""
        trace_name = self.name or func.__name__

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                async with self.aigie.trace(
                    trace_name, metadata=self.metadata, tags=self.tags
                ) as trace:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        await trace.complete(status="failure", error=e)
                        raise

            return async_wrapper
        from aigie.decorators_v3 import traceable

        return traceable(name=self.name)(func)


class SpanDecorator:
    """
    Decorator class for creating spans.

    Usage:
        @trace.span(name="operation", type="llm")
        async def operation():
            pass
    """

    def __init__(self, trace_context, name: str | None = None, type: str = "tool"):
        self.trace = trace_context
        self.name = name
        self.span_type = type

    def __call__(
        self,
        func: Callable | None = None,
        *,
        name: str | None = None,
        type: str | None = None,
    ):
        """Called when decorator is used."""
        if name is not None:
            self.name = name
        if type is not None:
            self.span_type = type

        if func is not None:
            return self._decorate(func)

        def decorator(f):
            return self._decorate(f)

        return decorator

    def _decorate(self, func: Callable):
        """Internal method to create the decorated function."""
        span_name = self.name or func.__name__

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                async with self.trace.span(span_name, type=self.span_type):
                    try:
                        return await func(*args, **kwargs)
                    except Exception:
                        # Error will be captured in span.__aexit__
                        raise

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            raise RuntimeError(
                f"Function {func.__name__} is not async. "
                "Use async def or use span context manager directly."
            )

        return sync_wrapper
