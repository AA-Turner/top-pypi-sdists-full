"""Serve Trio ASGI applications from uvicorn.

Uvicorn runs on asyncio, and Trio runs as a guest on the same event loop via
`trio.lowlevel.start_guest_run`. Everything stays on one thread, and Trio's
run context remains active there between guest ticks, so each side calls the
other directly: asyncio starts each application call as a task in a Trio
nursery, and the application's `receive` and `send` run as asyncio tasks
whose completion wakes Trio.

This module imports Trio, so import it only once the application's
dependencies are on `sys.path`.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

import trio

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    import outcome

type _Scope = dict[str, Any]
type _Message = dict[str, Any]
type _Receive = Callable[[], Awaitable[_Message]]
type _Send = Callable[[_Message], Awaitable[None]]
type _App = Callable[[_Scope, _Receive, _Send], Awaitable[None]]


def _call_into_asyncio[*Args, T](
    loop: asyncio.AbstractEventLoop,
    fn: Callable[[*Args], Awaitable[T]],
) -> Callable[[*Args], Awaitable[T]]:
    async def wrapper(*args: *Args) -> T:
        done = trio.Event()
        task = asyncio.ensure_future(fn(*args), loop=loop)
        task.add_done_callback(lambda _: done.set())
        try:
            await done.wait()
        except trio.Cancelled:
            task.cancel()
            raise
        return task.result()

    return wrapper


class TrioGuestASGI:
    """Run a Trio ASGI application under an asyncio ASGI server.

    The guest run starts on the first ASGI call. It shuts down when
    `asyncio.run` cancels the tasks left over at exit, so it finishes before
    the loop closes whether or not the server runs the lifespan protocol.
    """

    def __init__(self, app: _App) -> None:
        self._app = app
        self._started: asyncio.Future[None] | None = None
        self._nursery: trio.Nursery | None = None
        self._stopper: asyncio.Task[None] | None = None

    async def __call__(
        self, scope: _Scope, receive: _Receive, send: _Send
    ) -> None:
        await self._ensure_started()
        assert self._nursery is not None
        loop = asyncio.get_running_loop()
        fut: asyncio.Future[None] = loop.create_future()
        cancel_scope = trio.CancelScope()

        async def run_app() -> None:
            with cancel_scope:
                try:
                    await self._app(
                        scope,
                        _call_into_asyncio(loop, receive),
                        _call_into_asyncio(loop, send),
                    )
                except trio.Cancelled:
                    fut.cancel()
                    raise
                except BaseException as exc:
                    if not fut.done():
                        fut.set_exception(exc)
                else:
                    if not fut.done():
                        fut.set_result(None)

        self._nursery.start_soon(run_app)
        try:
            await fut
        except asyncio.CancelledError:
            cancel_scope.cancel()
            raise

    async def _ensure_started(self) -> None:
        if self._started is None:
            loop = asyncio.get_running_loop()
            self._started = loop.create_future()
            done: asyncio.Future[outcome.Outcome[None]] = loop.create_future()

            def on_done(result: outcome.Outcome[None]) -> None:
                done.set_result(result)
                if self._started is not None and not self._started.done():
                    self._started.set_exception(
                        RuntimeError("trio guest run exited before it started")
                    )

            trio.lowlevel.start_guest_run(
                self._trio_main,
                run_sync_soon_threadsafe=loop.call_soon_threadsafe,
                run_sync_soon_not_threadsafe=loop.call_soon,
                done_callback=on_done,
                host_uses_signal_set_wakeup_fd=True,
            )
            self._stopper = loop.create_task(self._stop_at_exit(done))
        await self._started

    async def _trio_main(self) -> None:
        async with trio.open_nursery() as nursery:
            self._nursery = nursery
            assert self._started is not None
            self._started.set_result(None)
            await trio.sleep_forever()

    async def _stop_at_exit(
        self, done: asyncio.Future[outcome.Outcome[None]]
    ) -> None:
        # Runs until `asyncio.run` cancels it at exit, which then runs the
        # loop until this task finishes.
        try:
            await asyncio.shield(done)
        except asyncio.CancelledError:
            if self._nursery is not None:
                self._nursery.cancel_scope.cancel()
        (await done).unwrap()
