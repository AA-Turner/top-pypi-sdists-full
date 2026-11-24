"""Calls that arrive together become ONE batch call — the engine's read coalescing.

Workflow lane B (2026-11-12, Arman: *"a workflow system should be much more efficient at these
things. Because it can easily batch."*). Steps in one wave run as sibling tasks; three
``records.read`` steps in the same wave were three statements. An Action whose door can answer
many keys at once asks through a :class:`Coalescer` instead of directly: every call that arrives
for the same GROUP within one short window is answered by ONE call of the batch function, and
each caller gets exactly its own answer (or its own error).

It is a DataLoader, nothing more: it never changes what is asked, only how many trips it takes.

* ``group`` decides who may share a trip. Callers sharing a group must be interchangeable for the
  batch function — the same run, the same person and organization — so a batch is never asked
  under an authority one of its callers lacks. A group is the caller's statement, not a guess.
* The window (``window_s``, default 2 ms) is measured from the FIRST arrival; ``max_batch``
  flushes early. A call alone waits only the window.
* The batch function answers ``{key: value}``; a value that is an ``Exception`` is raised to that
  key's caller alone, a key missing from the answer raises ``KeyError`` naming it (never a silent
  ``None``), and a batch that raises fails every caller in it with that error.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Hashable
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

K = TypeVar("K", bound=Hashable)
R = TypeVar("R")

#: Default window, seconds, from the first call of a group to its batch.
DEFAULT_WINDOW_S = 0.002
#: Default largest batch; a full batch goes at once.
DEFAULT_MAX_BATCH = 200  # protocol-constant: in-process load-coalescing batch size; a caller passes its own max_batch, and it shapes a query not a product limit


@dataclass
class _Pending(Generic[K, R]):
    batch: Callable[[list[K]], Awaitable[dict[K, Any]]]
    waiters: dict[K, list[asyncio.Future[R]]] = field(default_factory=dict)
    flush: asyncio.TimerHandle | None = None


class Coalescer(Generic[K, R]):
    """Coalesce concurrent single-key calls into batch calls, per group."""

    def __init__(self, *, window_s: float = DEFAULT_WINDOW_S, max_batch: int = DEFAULT_MAX_BATCH) -> None:
        if window_s < 0 or max_batch < 1:
            raise ValueError("Coalescer: window_s must be >= 0 and max_batch >= 1")
        self.window_s = window_s
        self.max_batch = max_batch
        self._groups: dict[Hashable, _Pending[K, R]] = {}
        #: Batches sent, and keys answered by them (observability and tests).
        self.batches = 0
        self.keys = 0

    async def load(
        self,
        group: Hashable,
        key: K,
        batch: Callable[[list[K]], Awaitable[dict[K, Any]]],
    ) -> R:
        """Answer ``key`` through ``batch``, sharing the trip with every caller of ``group`` in the window."""
        loop = asyncio.get_running_loop()
        pending = self._groups.get(group)
        if pending is None:
            pending = _Pending(batch=batch)
            self._groups[group] = pending
            pending.flush = loop.call_later(self.window_s, self._flush, group)
        fut: asyncio.Future[R] = loop.create_future()
        pending.waiters.setdefault(key, []).append(fut)
        if len(pending.waiters) >= self.max_batch:
            self._flush(group)
        return await fut

    def _flush(self, group: Hashable) -> None:
        pending = self._groups.pop(group, None)
        if pending is None:
            return
        if pending.flush is not None:
            pending.flush.cancel()
        # error-capture-owned: every waiter future in `pending` — _run sets the batch's failure on each caller's future
        asyncio.get_running_loop().create_task(self._run(pending), name=f"coalesce:{group!r}"[:120])

    async def _run(self, pending: _Pending[K, R]) -> None:
        keys = list(pending.waiters)
        self.batches += 1
        self.keys += len(keys)
        try:
            answers = await pending.batch(keys)
        except BaseException as exc:  # noqa: BLE001 — every caller in the batch gets the batch's failure
            for futs in pending.waiters.values():
                for fut in futs:
                    if not fut.done():
                        fut.set_exception(exc)
            if not isinstance(exc, Exception):
                raise
            return
        for key, futs in pending.waiters.items():
            for fut in futs:
                if fut.done():
                    continue
                if key not in answers:
                    fut.set_exception(KeyError(f"the batch answered no value for {key!r}"))
                elif isinstance(answers[key], BaseException):
                    fut.set_exception(answers[key])
                else:
                    fut.set_result(answers[key])
