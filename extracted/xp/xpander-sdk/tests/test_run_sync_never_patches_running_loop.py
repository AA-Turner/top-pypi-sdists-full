"""``run_sync`` used to call ``nest_asyncio.apply()`` when the running loop was
not uvloop. That patches ``run_forever`` / ``run_until_complete`` / ``_run_once``
on the loop class and swaps ``asyncio.Task`` and ``Future`` process-wide, which
unwinds the host server's ``asyncio.run`` and kills the process mid-request
(agent-worker children died on every deep-planning task). The running loop must
be left untouched, and what the caller carries into ``run_sync`` must survive the
hop onto the private loop.
"""

from __future__ import annotations

import asyncio
import contextvars
import threading
from typing import Any, Tuple

import pytest

from xpander_sdk.utils.event_loop import run_sync

_marker: contextvars.ContextVar[str] = contextvars.ContextVar("_marker", default="unset")


async def _work(marker: str) -> str:
    await asyncio.sleep(0)
    return marker


@pytest.mark.asyncio
async def test_run_sync_from_running_loop_leaves_asyncio_untouched() -> None:
    loop = asyncio.get_running_loop()
    before = (
        asyncio.Task,
        asyncio.Future,
        asyncio.run,
        type(loop)._run_once,
        type(loop).run_until_complete,
    )

    assert run_sync(_work("done")) == "done"

    assert (
        asyncio.Task,
        asyncio.Future,
        asyncio.run,
        type(loop)._run_once,
        type(loop).run_until_complete,
    ) == before
    assert not hasattr(asyncio, "_nest_patched")
    assert not hasattr(loop, "_nest_patched")


@pytest.mark.asyncio
async def test_run_sync_does_not_re_enter_the_host_loop() -> None:
    host_loop = asyncio.get_running_loop()
    host_thread = threading.get_ident()

    async def _probe() -> Tuple[Any, int]:
        return asyncio.get_running_loop(), threading.get_ident()

    coro_loop, coro_thread = run_sync(_probe())
    assert coro_loop is not host_loop
    assert coro_thread != host_thread
    assert asyncio.get_running_loop() is host_loop


@pytest.mark.asyncio
async def test_run_sync_carries_the_callers_contextvars() -> None:
    """The tool-call id lives in a ContextVar; a blank worker thread loses the header."""

    async def _read() -> str:
        return _marker.get()

    _marker.set("tool-call-1")
    assert run_sync(_read()) == "tool-call-1"


@pytest.mark.asyncio
async def test_run_sync_rejects_loop_bound_futures() -> None:
    """A Task belongs to the loop that made it; moving it would fail obscurely."""
    task = asyncio.ensure_future(_work("bound"))
    with pytest.raises(TypeError, match="coroutine object"):
        run_sync(task)
    await task


def test_run_sync_without_a_loop_still_runs() -> None:
    assert run_sync(_work("sync")) == "sync"
