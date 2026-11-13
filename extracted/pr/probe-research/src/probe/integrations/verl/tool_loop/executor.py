"""Probe's own threads for the work that waits on uploads (a loop's export, a reward worker's `collect_files`), never
the event loop's default executor: verl decodes there (`tool_parser.py:110`, `naive.py:54`), and an upload stalled
for up to 60 s would starve it. Bounded (32 threads, `PROBE_VERL_WAIT_THREADS`); made on first use, made again after a
fork."""

from __future__ import annotations

import asyncio
import concurrent.futures
import contextvars
import functools
import os
import threading
from collections.abc import Callable
from typing import Any

#: Threads Probe's waits share per process (env `PROBE_VERL_WAIT_THREADS`): they mostly wait on uploads, so as many
#: as asyncio's default; a stall delays loop ends, never verl's own executor work.
MAX_THREADS = 32


def get_max_threads() -> int:
    """`PROBE_VERL_WAIT_THREADS` when it is a positive integer, else `MAX_THREADS`."""
    try:
        value = int(os.environ.get("PROBE_VERL_WAIT_THREADS", ""))
    except ValueError:
        return MAX_THREADS
    return value if value > 0 else MAX_THREADS


_EXECUTOR: concurrent.futures.ThreadPoolExecutor | None = None
_LOCK = threading.Lock()


def get_executor() -> concurrent.futures.ThreadPoolExecutor:
    global _EXECUTOR
    with _LOCK:
        if _EXECUTOR is None:
            _EXECUTOR = concurrent.futures.ThreadPoolExecutor(get_max_threads(), thread_name_prefix="probe-verl-wait")
        return _EXECUTOR


async def run_in_executor(function: Callable[..., Any], *args: Any) -> Any:
    """``function(*args)`` on Probe's threads, in a copy of the caller's context (as `asyncio.to_thread`)."""
    context = contextvars.copy_context()
    call = functools.partial(context.run, function, *args)
    return await asyncio.get_running_loop().run_in_executor(get_executor(), call)


def _reset_after_fork() -> None:
    """A forked child has none of the parent's threads: it makes its own pool on first use."""
    global _EXECUTOR, _LOCK
    _EXECUTOR, _LOCK = None, threading.Lock()


if hasattr(os, "register_at_fork"):  # POSIX only
    os.register_at_fork(after_in_child=_reset_after_fork)
