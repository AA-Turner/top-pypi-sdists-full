"""Ambient binding of the current execution scope via ``contextvars``."""

from collections.abc import AsyncIterator, Iterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager, contextmanager
from contextvars import ContextVar
from typing import Literal, overload

from mistralai.vibe.sdk.agent.execution.resources.errors import NoCurrentScopeError
from mistralai.vibe.sdk.agent.execution.resources.scope import ResourcesScope

_current_execution_scope: ContextVar[ResourcesScope | None] = ContextVar(
    "current_execution_scope",
    default=None,
)


@overload
def current_execution_scope(*, should_raise: Literal[True] = ...) -> ResourcesScope: ...
@overload
def current_execution_scope(*, should_raise: Literal[False]) -> ResourcesScope | None: ...
def current_execution_scope(*, should_raise: bool = True) -> ResourcesScope | None:
    """Return the execution scope bound to the current context."""
    scope = _current_execution_scope.get()
    if scope is None and should_raise:
        raise NoCurrentScopeError()

    return scope


@contextmanager
def bind_execution_scope(scope: ResourcesScope) -> Iterator[None]:
    """Bind ``scope`` as the current execution scope for the duration of the block."""
    token = _current_execution_scope.set(scope)
    try:
        yield
    finally:
        _current_execution_scope.reset(token)


@contextmanager
def stop_execution_scope() -> Iterator[None]:
    """Temporarily unbind the current execution scope for the duration of the block."""
    token = _current_execution_scope.set(None)
    try:
        yield
    finally:
        _current_execution_scope.reset(token)


@overload
def spawn_child_scope(
    *, should_raise: Literal[True] = ...
) -> AbstractAsyncContextManager[ResourcesScope]: ...
@overload
def spawn_child_scope(
    *, should_raise: Literal[False]
) -> AbstractAsyncContextManager[ResourcesScope | None]: ...
@asynccontextmanager
async def spawn_child_scope(*, should_raise: bool = True) -> AsyncIterator[ResourcesScope | None]:
    """Open a tracked child of the current execution scope, bound for the block."""
    parent = current_execution_scope(should_raise=should_raise)
    if parent is None:
        yield None
        return

    child = parent.child_scope()
    try:
        with bind_execution_scope(child):
            yield child
    finally:
        await child.aclose()


__all__ = [
    "bind_execution_scope",
    "current_execution_scope",
    "spawn_child_scope",
    "stop_execution_scope",
]
