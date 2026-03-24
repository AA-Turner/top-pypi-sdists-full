"""Helpers for safely cancelling asyncio tasks without leaking late exceptions."""

from __future__ import annotations

import asyncio
from typing import Any


def _consume_task_result(task: asyncio.Task[Any]) -> None:
    """Drain a finished task result so late exceptions do not surface as loop noise."""
    try:
        task.result()
    except (asyncio.CancelledError, Exception):
        pass


def silence_task(task: asyncio.Task[Any] | None) -> None:
    """Consume a task result now or when it completes."""
    if task is None:
        return
    if task.done():
        _consume_task_result(task)
        return
    task.add_done_callback(_consume_task_result)


async def cancel_task(task: asyncio.Task[Any] | None, *, timeout: float = 0.2) -> None:
    """Cancel a task, wait briefly for shutdown, and consume any late exception."""
    if task is None:
        return

    silence_task(task)
    if task.done():
        return

    task.cancel()
    try:
        await asyncio.wait_for(asyncio.shield(task), timeout=timeout)
    except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
        pass
