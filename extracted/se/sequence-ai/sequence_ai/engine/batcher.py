# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The calls waiting for a model, batched into one call to it.

    from sequence_ai.engine.batcher import Batcher

    batcher = Batcher(model_on_a_list, sizes=[1, 2, 4, 8], wait_ms=2.0)     # model_on_a_list(inputs: list) -> list
    output = await batcher(observation)                                      # in each request's handler

In one sentence: a call joins the open batch → the batch is dispatched to the model as soon as it reaches its largest
size, or `wait_ms` after its first call arrived while the model is free → the model is called ONCE with a list and
returns a list → each call gets its own element back. A batch in which the model raised is re-run call by call, so
only a call that fails by itself fails.

How long a batch that is not full waits, and which of its calls go first, can be decided for each call instead:

    batcher = Batcher(model_on_a_list, sizes=[1, 2, 4], hold=hold, first=first)
    output = await batcher(observation, key="robot-1")

`hold(keys)` returns how many seconds the open batch may still wait for more calls - `keys` are its calls' keys, in the
order they arrived - and 0 to dispatch it now. It is asked as each call arrives while a runner is free, and as a
runner frees with calls waiting; `wait_ms` is not used. `first(keys, free)` returns the indexes of the open calls to
dispatch first, apart from the rest, or None to dispatch the open calls as one batch; it is asked as a batch is
dispatched, and `free` says whether another runner is free besides the one this batch takes. Indexes whose number is not
a listed size are ignored. serve() passes slack.Aligner's hold_s and split (engine/slack.py) with each robot's name as
its requests' key, so a request waits only as long as its own robot's chunk leaves it time.

WHY the open batch keeps accumulating while the model is busy, and is dispatched as soon as it is free: calls that
arrive during a forward pass would wait for it anyway, so they wait together and are served in one forward pass instead
of one each. When the batch was cut every `wait_ms` instead, calls that reached the server over tens of milliseconds
made a series of small batches queued behind each other.
WHY only the sizes listed: a model is traced, compiled or graphed for the shapes it has seen, and a batch of a size it
has not seen is a new shape. The waiting calls are dispatched in the largest listed size they fill, in arrival order,
and the remainder is dispatched the same way: 3 calls with sizes [1, 2, 4] are dispatched as 2, then 1. So 1 is always
listed.
WHY it helps: on one GPU a policy measured 68.1 ms at batch 1 and 39.6 ms per sample at batch 16 (1.72x), because the
GPU is already near its compute limit at batch 1.

`run` may be a plain function or an async one. A plain one runs on a thread, so a forward pass never blocks the
server's event loop. `runners` is how many batches may run concurrently: one per replica of the model.

Standard library only. Written for this package after the batcher General Sequences serves with, which is bound to its
own router; the rules above are that one's.
"""
from __future__ import annotations

import asyncio
import collections
import inspect
from typing import Any, Callable, Iterable, Optional


class Batcher:
    """Calls batched in the sizes a model lists (the module's docstring). `await batcher(item)` returns the item's own
    element of its batch's output, or raises what the model raised for it; `await batcher(item, key=...)` passes the
    call's key to `hold` and `first`.

    sent      how many batches were dispatched, by size
    reruns    how many batches the model raised in, and were re-run call by call"""

    def __init__(self, run: Callable[[list], Any], *, sizes: Iterable[int] = (1, 2, 4, 8), wait_ms: float = 2.0,
                 runners: int = 1, hold: Optional[Callable[[list], float]] = None,
                 first: Optional[Callable[[list, bool], Optional[list]]] = None) -> None:
        self._sizes = sorted({int(n) for n in sizes})
        if not self._sizes or self._sizes[0] != 1:
            raise ValueError(f"sizes {sorted(self._sizes)} must include 1: a call that waits alone is a batch of 1, "
                             "and a batch in which the model raised is re-run call by call")
        self._run, self._is_async = run, inspect.iscoroutinefunction(run)
        self._max, self._wait_s, self._runners = self._sizes[-1], max(0.0, wait_ms) / 1000.0, max(1, int(runners))
        self._hold, self._first = hold, first
        self._open: list[tuple[Any, asyncio.Future, Any]] = []        # (item, its future, its key)
        self._running = 0
        self._timer: Optional[asyncio.TimerHandle] = None
        self._tasks: set[asyncio.Task] = set()
        self.sent: collections.Counter = collections.Counter()
        self.reruns = 0

    async def __call__(self, item: Any, key: Any = None) -> Any:
        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        self._open.append((item, future, key))
        if len(self._open) >= self._max:
            self._send()                       # full: dispatched now, or as soon as the model is free
        elif self._hold is not None:
            if self._running < self._runners:
                self._held()                   # asked again as each call arrives, which can end the wait
        elif self._timer is None:
            self._timer = loop.call_later(self._wait_s, self._due)
        return await future

    def _keys(self) -> list:
        return [key for _, _, key in self._open]

    def _held(self) -> None:
        """With `hold`: the open batch dispatched now, or a timer set for when it may wait no longer."""
        wait = self._hold(self._keys())
        if wait <= 0:
            self._send()
            return
        if self._timer is not None:
            self._timer.cancel()
        self._timer = asyncio.get_running_loop().call_later(wait, self._due)

    def _due(self) -> None:
        self._timer = None
        self._send()

    def _send(self) -> None:
        """Dispatch every batch the open calls make, while a runner is free: the calls `first` names, else the largest
        listed size they fill, in arrival order. What is left while none is free is dispatched as soon as one is free
        (_answer); what is left after calls went first, while a runner is free, waits on as `hold` says."""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        while self._open and self._running < self._runners:
            batch, apart = self._take()
            self._running += 1
            self.sent[len(batch)] += 1
            task = asyncio.ensure_future(self._answer(batch))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
            if (apart and self._hold is not None and self._open and len(self._open) < self._max
                    and self._running < self._runners):
                wait = self._hold(self._keys())
                if wait > 0:                   # the calls left are not due yet: they wait on, by their own keys
                    self._timer = asyncio.get_running_loop().call_later(wait, self._due)
                    return

    def _take(self) -> tuple[list, bool]:
        """The next batch of the open calls, and whether it went first, apart from the rest (`first`)."""
        if self._first is not None:
            picked = self._first(self._keys(), self._running + 1 < self._runners)
            going = {i for i in picked or () if 0 <= i < len(self._open)}
            if going and len(going) in self._sizes and len(going) < len(self._open):
                batch = [entry for i, entry in enumerate(self._open) if i in going]
                self._open = [entry for i, entry in enumerate(self._open) if i not in going]
                return batch, True
        size = max(n for n in self._sizes if n <= len(self._open))
        batch, self._open = self._open[:size], self._open[size:]
        return batch, False

    async def _call(self, items: list) -> list:
        if self._is_async:
            out = await self._run(items)
        else:
            out = await asyncio.get_running_loop().run_in_executor(None, self._run, items)
        out = list(out)
        if len(out) != len(items):
            raise ValueError(f"the model returned {len(out)} outputs for a batch of {len(items)}")
        return out

    async def _answer(self, batch: list) -> None:
        try:
            try:
                outputs = await self._call([item for item, _, _ in batch])
            except Exception as exc:  # noqa: BLE001 (any error: re-running each call by itself shows whose it is)
                if len(batch) == 1:
                    _settle(batch[0][1], error=exc)
                    return
                self.reruns += 1
                for item, future, _ in batch:
                    try:
                        _settle(future, value=(await self._call([item]))[0])
                    except Exception as own:  # noqa: BLE001
                        _settle(future, error=own)
                return
            for (_, future, _), value in zip(batch, outputs):
                _settle(future, value=value)
        finally:
            self._running -= 1
            if self._open:
                if self._hold is not None and len(self._open) < self._max:
                    self._held()               # what accumulated meanwhile may still wait for the rest
                else:
                    self._send()               # the model is free again: dispatch what accumulated meanwhile, as one


def _settle(future: asyncio.Future, *, value: Any = None, error: Optional[BaseException] = None) -> None:
    """Set a call's result or its error, unless its caller has gone away (a request cancelled while its batch ran)."""
    if future.done():
        return
    if error is not None:
        future.set_exception(error)
    else:
        future.set_result(value)
