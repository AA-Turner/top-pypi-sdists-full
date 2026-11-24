"""A host parks the RUNNING tool call on a person from below the tool function.

``ask_person`` and the spend ask park their own call and return ``delegated_pending``. A host
check deeper in the call — the Action apply gate, which raises the person's approval card itself
under their "ask" setting — runs below every door's converter and cannot hand a ``ToolResult``
back through them. It parks the call in the host's ledger and marks it here
(:func:`mark_parked`); the executor's one dispatch edge (``ToolExecutor._dispatch``) opens a scope
per call (:func:`tool_call_scope`) and turns a marked call's answer into ``delegated_pending``
(:func:`settle_parked`) — the same end of turn every parked call takes, so the model never reads
a refusal for a call that is waiting on the person.

Outside the executor (a step, an api call, a test) there is no scope: :func:`current_tool_call`
is ``None`` and :func:`mark_parked` returns ``False``, so the host keeps its plain refusal.

ONE STEP, ONE ASK. The calls one model response makes run together (``execute_batch``), which
opens a :class:`ToolBatch` over them (:func:`tool_batch_scope`). A host that asks the person about
several of them can gather the step's asks into one: each call that reaches the host's gate says
so (:meth:`ToolBatch.arrive`), every call marks itself settled when it ends, and the first asker
waits (:meth:`ToolBatch.wait_for_siblings`) until every sibling has either reached the gate or
finished, then asks once. ``shared`` is the host's per-step storage.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

from matrx_ai.tools.models import ToolResult


@dataclass
class ToolCallScope:
    """One tool call in flight: its context, and the parked answer a host marked, if any."""

    ctx: Any
    parked: dict[str, Any] | None = None


@dataclass
class ToolBatch:
    """The calls of ONE model response, run together. A host gathers their asks into one."""

    call_ids: frozenset[str]
    settled: set[str] = field(default_factory=set)
    at_gate: set[str] = field(default_factory=set)
    shared: dict[str, Any] = field(default_factory=dict)

    def arrive(self, call_id: str) -> None:
        """This call reached the host's gate and waits on the step's one ask."""
        self.at_gate.add(str(call_id))

    def settle(self, call_id: str) -> None:
        """This call ended (ran, failed, or was refused)."""
        self.settled.add(str(call_id))

    def siblings_accounted_for(self) -> bool:
        return self.call_ids <= (self.settled | self.at_gate)

    async def wait_for_siblings(self, *, timeout: float, poll: float = 0.02) -> bool:
        """Wait until every call of the step has reached the gate or ended, at most ``timeout``
        seconds. ``True`` when all are accounted for, ``False`` when the wait ran out (a slow
        sibling then gets its own ask)."""
        deadline = time.monotonic() + max(0.0, timeout)
        while not self.siblings_accounted_for():
            if time.monotonic() >= deadline:
                return False
            await asyncio.sleep(poll)
        return True


_SCOPE: ContextVar[ToolCallScope | None] = ContextVar("matrx_tool_call_scope", default=None)
_BATCH: ContextVar[ToolBatch | None] = ContextVar("matrx_tool_batch", default=None)


@contextmanager
def tool_batch_scope(call_ids: Any) -> Iterator[ToolBatch]:
    """Open the scope of one step's calls (``ToolExecutor.execute_batch``); each call's task
    inherits it."""
    batch = ToolBatch(call_ids=frozenset(str(c) for c in call_ids if c))
    token = _BATCH.set(batch)
    try:
        yield batch
    finally:
        _BATCH.reset(token)


def current_tool_batch() -> ToolBatch | None:
    """The step the running call belongs to; ``None`` for a call run on its own."""
    return _BATCH.get()


@contextmanager
def tool_call_scope(ctx: Any) -> Iterator[ToolCallScope]:
    """Open the scope of one tool call (the executor's dispatch edge)."""
    scope = ToolCallScope(ctx=ctx)
    token = _SCOPE.set(scope)
    try:
        yield scope
    finally:
        _SCOPE.reset(token)
        batch = _BATCH.get()
        call_id = str(getattr(ctx, "call_id", "") or "")
        if batch is not None and call_id:
            batch.settle(call_id)


def current_tool_call() -> Any | None:
    """The ``ToolContext`` of the tool call running now; ``None`` outside the executor."""
    scope = _SCOPE.get()
    return scope.ctx if scope is not None else None


def mark_parked(output: dict[str, Any]) -> bool:
    """The host parked the running call on a person (its ledger row is already ``delegated``).
    ``output`` is what a parked call's record shows (never the model). ``False`` when no tool
    call is running, so the caller keeps its own answer."""
    scope = _SCOPE.get()
    if scope is None:
        return False
    scope.parked = dict(output)
    return True


def settle_parked(scope: ToolCallScope, result: ToolResult) -> ToolResult:
    """The call's answer, or — when a host parked it — the ``delegated_pending`` marker that ends
    the turn until the person answers."""
    if scope.parked is None or result.delegated_pending:
        return result
    ctx = scope.ctx
    return ToolResult(
        success=False,
        delegated_pending=True,
        output=scope.parked,
        started_at=result.started_at or time.time(),
        completed_at=time.time(),
        tool_name=result.tool_name or str(getattr(ctx, "tool_name", "") or ""),
        call_id=str(getattr(ctx, "call_id", "") or result.call_id or ""),
    )


__all__ = [
    "ToolBatch",
    "ToolCallScope",
    "current_tool_batch",
    "current_tool_call",
    "mark_parked",
    "settle_parked",
    "tool_batch_scope",
    "tool_call_scope",
]
