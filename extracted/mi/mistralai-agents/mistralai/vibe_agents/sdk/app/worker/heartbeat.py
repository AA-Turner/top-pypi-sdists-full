import asyncio
import contextlib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import temporalio.activity

import mistralai.workflows as workflows


@asynccontextmanager
async def heartbeat_while_running() -> AsyncIterator[None]:
    """Heartbeat for as long as the body runs, so a lost worker is detected before the activity timeout."""

    if not temporalio.activity.in_activity():
        yield
        return
    heartbeat_timeout = temporalio.activity.info().heartbeat_timeout
    if heartbeat_timeout is None:
        yield
        return

    async def beat() -> None:
        while True:
            workflows.activity_heartbeat()
            await asyncio.sleep(heartbeat_timeout.total_seconds() / 3)

    beating = asyncio.create_task(beat())
    try:
        yield
    finally:
        beating.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await beating
