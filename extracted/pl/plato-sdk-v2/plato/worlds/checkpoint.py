"""Async context manager for checkpointing around stage execution."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def checkpoint(
    fn: Callable[..., Awaitable],
    name: str,
    *,
    step: int = 0,
    interval_s: int = 0,
):
    """Checkpoint world state after the wrapped block completes.

    Usage::

        async with checkpoint(world.checkpoint, "annotate", step=2, interval_s=300):
            await annotate(...)

    Args:
        fn: Async checkpoint function (e.g. ``world.checkpoint``).
        name: Stage name for the checkpoint label.
        step: Step number. Label becomes ``step.{N}.stage.{name}``.
            Defaults to 0.
        interval_s: If > 0, run periodic background checkpoints every
            ``interval_s`` seconds while the block executes.
    """
    label = f"step.{step}.stage.{name}"

    bg_task = None
    if interval_s > 0:

        async def _periodic():
            counter = 0
            while True:
                await asyncio.sleep(interval_s)
                counter += 1
                try:
                    await fn(f"{label}.auto.{counter}")
                except Exception:
                    logger.exception("background checkpoint failed")

        bg_task = asyncio.create_task(_periodic())

    try:
        yield
    finally:
        if bg_task is not None:
            bg_task.cancel()
            try:
                await bg_task
            except asyncio.CancelledError:
                pass

    await fn(label)
