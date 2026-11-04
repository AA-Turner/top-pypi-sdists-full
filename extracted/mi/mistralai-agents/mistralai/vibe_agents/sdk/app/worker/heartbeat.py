import asyncio
import contextlib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import timedelta

import temporalio.activity
from temporalio.client import AsyncActivityCancelledError
from temporalio.service import RPCError, RPCStatusCode

import mistralai.workflows as workflows

# The worker sends at most one heartbeat per 0.8 x the heartbeat timeout, and a cancel reaches the
# activity only in a heartbeat answer: 48 s for a 60 s timeout. Asking the server directly is faster.
_CANCEL_CHECK_INTERVAL = timedelta(seconds=1)
# Bounds each attempt of one check while the server is slow to answer; the client retries some errors.
_CANCEL_CHECK_RPC_TIMEOUT = timedelta(seconds=5)


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


@asynccontextmanager
async def stop_when_cancelled() -> AsyncIterator[None]:
    """Cancel the body within about a second of a cancel request, and end the activity as cancelled.

    It asks the server every second on the worker's own client, so it adds no connection. It also stops
    the body when the server no longer knows the activity, for example after its Workflow ended.
    """

    # A local activity has no task on the server to ask about.
    if not temporalio.activity.in_activity() or temporalio.activity.info().is_local:
        yield
        return
    activity = temporalio.activity.client().get_async_activity_handle(task_token=temporalio.activity.info().task_token)
    body = asyncio.current_task()
    if body is None:
        raise RuntimeError("An async activity runs in an asyncio task")
    stopped = False

    async def check() -> None:
        nonlocal stopped
        logged = False
        while True:
            await asyncio.sleep(_CANCEL_CHECK_INTERVAL.total_seconds())
            try:
                await activity.heartbeat(rpc_timeout=_CANCEL_CHECK_RPC_TIMEOUT)
            except AsyncActivityCancelledError as error:
                # A pause also raises this; the worker's own heartbeat handles it, as before.
                if error.details is None or error.details.cancel_requested:
                    break
            except Exception as error:
                if isinstance(error, RPCError) and error.status == RPCStatusCode.NOT_FOUND:
                    break
                # Keep checking: the worker's own heartbeat still delivers the cancel, only later.
                if not logged:
                    temporalio.activity.logger.warning("Checking for a cancel failed, retrying", exc_info=True)
                    logged = True
        stopped = True
        body.cancel()

    checking = asyncio.create_task(check())
    try:
        yield
    except asyncio.CancelledError:
        if not stopped:
            raise
        # The worker has not seen the cancel and would record a failure, so report the cancel here and
        # tell the worker the activity is completed elsewhere.
        try:
            await activity.report_cancellation()
        except RPCError as error:
            # The server no longer knows the activity; otherwise let the worker record the failure.
            if error.status != RPCStatusCode.NOT_FOUND:
                raise
        # The cancel was ours and is handled here, so later awaits in this task run normally.
        body.uncancel()
        temporalio.activity.raise_complete_async()
    finally:
        checking.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await checking
