"""Generic sync-loop → async-stream bridge for PDF operations.

A sync extraction/analysis loop runs on ONE executor thread (PyMuPDF
thread-safety — the Document never leaves its thread) and reports progress
through an ``emit`` callback; items cross to the event loop via a queue and
are yielded live. This is the pattern proven in
``extract/text.py::extract_text_pages_stream``, extracted so every per-page
analyzer (tables, classification, reading order, repeated regions) streams
the same way without re-implementing the bridge.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def iter_sync_stream(
    executor: Callable[..., Awaitable[object]],
    work: Callable[[Callable[[T], None]], object],
) -> AsyncIterator[T]:
    """Run ``work(emit)`` on *executor*; yield every emitted item live.

    ``work`` runs entirely on one executor worker and calls ``emit(item)``
    from its sync loop. A failure inside ``work`` is re-raised here after
    all already-emitted items have been yielded.
    """
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[T | None] = asyncio.Queue()

    def _emit(item: T) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, item)

    async def _run() -> None:
        try:
            await executor(work, _emit)
        finally:
            queue.put_nowait(None)  # sentinel — runs on the event loop already

    worker = asyncio.ensure_future(_run())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        # Propagate a failure (worker is guaranteed settled once the sentinel
        # arrived; on generator abandonment this awaits the tail).
        await worker


__all__ = ["iter_sync_stream"]
