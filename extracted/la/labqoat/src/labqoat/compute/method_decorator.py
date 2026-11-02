"""Capture a context-first method while preserving its authored caller argument types."""

from collections.abc import Awaitable, Callable
from typing import Concatenate, ParamSpec, TypeVar, overload

from labqoat.compute.method_descriptor import MethodDescriptor
from labqoat.run_context import RunContext

P = ParamSpec("P")
R = TypeVar("R")
S = TypeVar("S")


class MethodDecorator:
    """Keep the method body inert until a service-owned worker claims its invocation."""

    @overload
    def __call__(self, function: Callable[Concatenate[S, RunContext, P], Awaitable[R]]) -> MethodDescriptor[P, R]: ...

    @overload
    def __call__(self, function: Callable[Concatenate[S, RunContext, P], R]) -> MethodDescriptor[P, R]: ...

    def __call__(self, function: Callable[Concatenate[S, RunContext, P], object]) -> MethodDescriptor[P, object]:
        """Expose the bound method as a Function accepting only its public arguments."""
        return MethodDescriptor(function)
