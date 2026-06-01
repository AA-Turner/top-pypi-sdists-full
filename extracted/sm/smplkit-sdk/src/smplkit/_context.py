"""Per-request context stash for context-sensitive evaluation (flags today,
likely more later).

Backed by :class:`contextvars.ContextVar` so per-request isolation works for
both ``asyncio`` (each task gets its own value) and threaded sync code (each
thread gets its own value).
"""

from __future__ import annotations

import contextvars
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from smplkit.flags.types import Context


_request_context: contextvars.ContextVar[list["Context"]] = contextvars.ContextVar(
    "smplkit_request_context",
    default=[],
)


class ContextScope:
    """Returned by :func:`set_context`.

    Optional to use — bare ``client.set_context([...])`` is fire-and-forget
    (typical middleware pattern).  Holding the return value as a context
    manager (``with client.set_context([...]):``) auto-reverts to the prior
    context on exit, useful for scoped overrides like impersonation.
    """

    __slots__ = ("_token",)

    def __init__(self, token: contextvars.Token) -> None:
        self._token = token

    def __enter__(self) -> ContextScope:
        return self

    def __exit__(self, *args: object) -> None:
        _request_context.reset(self._token)

    async def __aenter__(self) -> ContextScope:
        return self

    async def __aexit__(self, *args: object) -> None:
        _request_context.reset(self._token)


def set_context(contexts: list["Context"]) -> ContextScope:
    """Stash *contexts* as the current per-request context.

    Returns a :class:`ContextScope` that can be used as a ``with`` /
    ``async with`` block to revert to the prior context on exit, or
    ignored for fire-and-forget middleware use.
    """
    token = _request_context.set(list(contexts))
    return ContextScope(token)


def get_context() -> list["Context"]:
    """Return the current per-request context (empty list if unset)."""
    return _request_context.get()
