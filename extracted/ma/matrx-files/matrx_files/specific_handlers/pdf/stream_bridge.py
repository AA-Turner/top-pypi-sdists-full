"""Generic sync-loop → async-stream bridge for PDF operations.

A sync extraction/analysis loop runs on ONE executor thread (PyMuPDF
thread-safety — the Document never leaves its thread) and reports progress
through an ``emit`` callback; items cross to the event loop via a queue and
are yielded live. Every streaming PDF operation (text extraction, search,
tables, classification, reading order, repeated regions) uses this one bridge.

ORDERING INVARIANT: the end-of-stream marker travels through the SAME ordered
channel as the items (``loop.call_soon_threadsafe`` from the worker thread,
posted after the work's last ``emit``). It must never be posted from the
event-loop side when the executor future resolves: the future's completion
and the thread's posted callbacks are two different channels, and the
completion can win — the consumer then reads the marker first and the stream
ends with ZERO items and no error (2026-11-16: every saved PDF could finish
"done" with no text, about 1 run in 1,500).
"""

from __future__ import annotations

import asyncio
import threading
from collections.abc import AsyncIterator, Awaitable, Callable
_DONE = object()


async def iter_sync_stream[T](
    executor: Callable[..., Awaitable[object]],
    work: Callable[[Callable[[T], None]], object],
) -> AsyncIterator[T]:
    """Run ``work(emit)`` on *executor*; yield every emitted item live, in order.

    ``work`` runs entirely on one executor worker and calls ``emit(item)``
    from its sync loop. Every emitted item is yielded before the stream ends.
    A failure inside ``work`` is re-raised here after all already-emitted
    items have been yielded.
    """
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[object] = asyncio.Queue()
    # "pending" until the worker thread starts the work; "running" once it
    # has (it then owns posting the end marker); "abandoned" if the executor
    # call failed or was cancelled before the work ever started (the event
    # loop then owns the end marker, and a late start does nothing).
    state = {"value": "pending"}
    state_lock = threading.Lock()

    def _emit(item: T) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, item)

    def _produce() -> object:
        with state_lock:
            if state["value"] == "abandoned":
                return None
            state["value"] = "running"
        try:
            return work(_emit)
        finally:
            # Same channel, after the last item: FIFO with every emit.
            if not loop.is_closed():
                loop.call_soon_threadsafe(queue.put_nowait, _DONE)

    async def _run() -> None:
        try:
            await executor(_produce)
        except BaseException:
            with state_lock:
                never_started = state["value"] == "pending"
                if never_started:
                    state["value"] = "abandoned"
            if never_started:
                queue.put_nowait(_DONE)
            raise

    worker = asyncio.ensure_future(_run())
    try:
        while True:
            item = await queue.get()
            if item is _DONE:
                break
            yield item  # type: ignore[misc]
    finally:
        # Propagate a failure (the end marker arrives only after the work
        # returned or raised; on generator abandonment this awaits the tail).
        await worker


__all__ = ["iter_sync_stream"]
