"""Unit tests for services/async_tasks.py — silence_task and cancel_task."""

from __future__ import annotations

import asyncio

import pytest

from anteroom.services.async_tasks import cancel_task, silence_task


@pytest.mark.asyncio
async def test_silence_task_suppresses_exception() -> None:
    """A task that raises must not propagate as an unhandled exception."""

    async def _failing() -> None:
        raise RuntimeError("boom")

    task = asyncio.create_task(_failing())
    silence_task(task)
    await asyncio.sleep(0)  # let the task run
    assert task.done()
    # result() would raise, but the callback already consumed it — no warning
    with pytest.raises(RuntimeError):
        task.result()


@pytest.mark.asyncio
async def test_silence_task_passes_on_success() -> None:
    """A successful task is unaffected by silence_task."""

    async def _ok() -> int:
        return 42

    task = asyncio.create_task(_ok())
    silence_task(task)
    await asyncio.sleep(0)
    assert task.result() == 42


@pytest.mark.asyncio
async def test_silence_task_already_done_exception() -> None:
    """silence_task works even when called after the task has already completed with an error."""

    async def _failing() -> None:
        raise ValueError("already done")

    task = asyncio.create_task(_failing())
    await asyncio.sleep(0)
    assert task.done()
    silence_task(task)  # must not raise


@pytest.mark.asyncio
async def test_silence_task_already_done_success() -> None:
    """silence_task on an already-successful task is a no-op."""

    async def _ok() -> str:
        return "hi"

    task = asyncio.create_task(_ok())
    await asyncio.sleep(0)
    silence_task(task)
    assert task.result() == "hi"


@pytest.mark.asyncio
async def test_silence_task_none_is_noop() -> None:
    """silence_task(None) must not raise."""
    silence_task(None)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_cancel_task_none_is_noop() -> None:
    """cancel_task(None) must not raise."""
    await cancel_task(None)


@pytest.mark.asyncio
async def test_cancel_task_cancels_running_task() -> None:
    """cancel_task should cancel an in-flight task."""

    async def _forever() -> None:
        await asyncio.sleep(9999)

    task = asyncio.create_task(_forever())
    await cancel_task(task, timeout=0.1)
    assert task.done()
