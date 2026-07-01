"""Capability worker -- long-running background component.

A Worker is constructed at module level in a capability's ``workers/*.py`` file.
Decorator-based handlers register callables; the runtime dispatches them during
the worker's lifetime.

Example::

    from dreadnode.capabilities.worker import Worker, EventEnvelope, RuntimeClient

    worker = Worker(name="bridge")

    @worker.on_startup
    async def connect(client: RuntimeClient) -> None:
        worker.state["ws"] = await open_websocket()

    @worker.on_event("turn.completed")
    async def on_turn(event: EventEnvelope, client: RuntimeClient) -> None:
        await forward_result(worker.state["ws"], event.payload)

    @worker.every(seconds=30)
    async def heartbeat(client: RuntimeClient) -> None:
        await worker.state["ws"].ping()
"""

import asyncio
import re
import typing as t
from dataclasses import dataclass

from dreadnode.app.client.interactive import TurnCancelledError, TurnFailedError

if t.TYPE_CHECKING:
    from dreadnode.app.client.runtime_client import RuntimeClient
    from dreadnode.app.server.runtime_events import RuntimeEventEnvelope

    # Re-export for capability authors — usable as type annotations.
    EventEnvelope = RuntimeEventEnvelope
else:
    # At runtime these are just sentinels so the module can be imported
    # without pulling in the server or client packages.
    RuntimeClient = None
    EventEnvelope = None

__all__ = [
    "EventEnvelope",
    "RuntimeClient",
    "TurnCancelledError",
    "TurnFailedError",
    "Worker",
]

_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# ── Handler type aliases ─────────────────────────────────────────────────────
# These give type checkers concrete signatures for each decorator.

ClientHandler = t.Callable[["RuntimeClient"], t.Awaitable[None]]
"""Signature for on_startup, on_shutdown, every, and task handlers."""

EventHandler = t.Callable[["RuntimeEventEnvelope", "RuntimeClient"], t.Awaitable[None]]
"""Signature for on_event handlers."""


@dataclass
class ScheduleSpec:
    """Parsed schedule for an ``@worker.every(...)`` handler."""

    interval_seconds: float | None = None
    cron_expr: str | None = None


class Worker:
    """Capability worker -- long-running background component.

    Constructed at module level in a capability's ``workers/`` directory.
    Handler decorators register callables that the runtime dispatches during
    the worker's lifetime. Workers interact with the runtime exclusively
    through a :class:`RuntimeClient` instance passed to each handler.
    """

    def __init__(self, name: str | None = None) -> None:
        """Construct a Worker (CAP-WAPI-001).

        When loaded via a capability manifest, the manifest key is
        authoritative. If *name* is omitted, the loader assigns the key;
        if provided, it must match the key (mismatch is a validation
        error). Standalone workers (CAP-WTOP-002) must provide *name*.
        """
        if name is not None and not _NAME_PATTERN.match(name):
            raise ValueError(f"Worker name must match [a-z0-9][a-z0-9-]*, got {name!r}")
        self.name: str | None = name
        self.state: dict[str, t.Any] = {}

        # Handler registries (populated by decorators, read by WorkerLifecycleManager)
        self._startup_handlers: list[ClientHandler] = []
        self._shutdown_handlers: list[ClientHandler] = []
        self._event_handlers: dict[str, list[EventHandler]] = {}
        self._every_handlers: list[tuple[ScheduleSpec, ClientHandler]] = []
        self._task_handlers: list[ClientHandler] = []

    # ── Decorators ────────────────────────────────────────────────

    def on_startup(self, fn: ClientHandler) -> ClientHandler:
        """Register a startup handler (CAP-WAPI-003).

        Called once when the worker starts, before any other handlers
        are active. Receives the runtime client as its first argument.
        """
        _require_async(fn, "on_startup")
        self._startup_handlers.append(fn)
        return fn

    def on_shutdown(self, fn: ClientHandler) -> ClientHandler:
        """Register a shutdown handler (CAP-WAPI-004).

        Called once during worker stop, before the client is closed.
        Receives the runtime client as its first argument.
        """
        _require_async(fn, "on_shutdown")
        self._shutdown_handlers.append(fn)
        return fn

    def on_event(self, kind: str) -> t.Callable[[EventHandler], EventHandler]:
        """Register an event handler (CAP-WAPI-005).

        Returns a decorator. The decorated function is invoked for each
        broker event whose ``kind`` field matches *kind* exactly.
        Handler signature: ``async def handler(event, client) -> None``.
        """

        def decorator(fn: EventHandler) -> EventHandler:
            _require_async(fn, "on_event")
            self._event_handlers.setdefault(kind, []).append(fn)
            return fn

        return decorator

    def every(
        self,
        *,
        seconds: float | None = None,
        minutes: float | None = None,
        cron: str | None = None,
    ) -> t.Callable[[ClientHandler], ClientHandler]:
        """Register a recurring schedule handler (CAP-WAPI-006).

        Exactly one of *seconds*, *minutes*, or *cron* must be provided.
        Handler signature: ``async def handler(client) -> None``.
        """
        provided = sum(x is not None for x in (seconds, minutes, cron))
        if provided != 1:
            raise ValueError("Exactly one of seconds, minutes, or cron must be provided")

        if seconds is not None:
            spec = ScheduleSpec(interval_seconds=seconds)
        elif minutes is not None:
            spec = ScheduleSpec(interval_seconds=minutes * 60)
        else:
            spec = ScheduleSpec(cron_expr=cron)

        def decorator(fn: ClientHandler) -> ClientHandler:
            _require_async(fn, "every")
            self._every_handlers.append((spec, fn))
            return fn

        return decorator

    def task(self, fn: ClientHandler) -> ClientHandler:
        """Register a supervised long-running task (CAP-WAPI-007).

        The decorated function runs for the worker's lifetime. If it
        returns or raises (except ``CancelledError``), it is restarted
        with exponential backoff.
        Handler signature: ``async def handler(client) -> None``.
        """
        _require_async(fn, "task")
        self._task_handlers.append(fn)
        return fn

    # ── Standalone entry points (CAP-WTOP-002) ────────────────────

    def run(self) -> None:
        """Launch this worker as a standalone process (CAP-WTOP-002).

        Reads ``DREADNODE_RUNTIME_*`` env vars (CAP-WENV-001..003) via
        :class:`RuntimeClient`, runs the worker until SIGTERM/SIGINT.
        Intended use::

            if __name__ == "__main__":
                worker.run()

        Use :meth:`arun` if you already have a running event loop.
        """
        # Standalone workers ARE the dreadnode framework running in the user's
        # process — framework warnings (startup failures, runner errors) are
        # the operator's only diagnostic. The package-level ``logger.disable``
        # in ``dreadnode/__init__.py`` is for embedded/library use; flip it
        # back on for the standalone entry point so subprocess parents tee
        # something useful into the worker log.
        from loguru import logger as _loguru_logger

        _loguru_logger.enable("dreadnode")
        asyncio.run(self.arun())

    async def arun(self) -> None:
        """Async peer of :meth:`run`: install signal handlers, then drive the worker.

        Factored from :meth:`_run_until` so tests can drive the lifecycle
        without touching process-wide signal state.
        """
        stop_event = asyncio.Event()
        _install_stop_signal_handlers(stop_event)
        await self._run_until(stop_event)

    async def _run_until(self, stop_event: asyncio.Event) -> None:
        """Drive the standalone lifecycle until *stop_event* is set.

        Lifecycle order (CAP-WLIF-001..004): ``client.start()`` →
        ``runner.start()`` → wait → ``runner.stop()`` → ``client.close()``.
        If the runner enters ``ERROR`` state (startup failure or all tasks
        crashed, CAP-WLIF-009), the stop event is set so the process exits
        rather than ghosting.
        """
        from dreadnode.app.client.runtime_client import RuntimeClient as _RuntimeClient
        from dreadnode.capabilities.worker_runner import WorkerRunner, WorkerState

        if self.name is None:
            raise ValueError("Worker(name=...) is required when running standalone (CAP-WAPI-001)")

        # CAP-WCLI-022: worker-bound client auto-sets origin=worker and
        # stamps worker:<name> on every session it creates. Same shape as
        # the in-process path set up in WorkerLifecycleManager._create_worker_client.
        client = _RuntimeClient(
            default_session_origin="worker",
            default_session_labels={
                "worker": [self.name],
            },
        )

        # Capture the FIRST ERROR transition's message so we can re-raise it
        # after cleanup. ``runner.stop()`` overwrites ``runner.error`` (to
        # ``None`` or ``"shutdown errors: ..."``) so reading it post-stop
        # loses the original cause. Capturing in the callback also covers
        # both startup failures (``on_startup`` raised → ``runner.start``
        # transitions ERROR before returning) and operational failures (e.g.
        # all supervised tasks crashed → ``_supervised_task_loop`` transitions
        # ERROR while the worker was RUNNING).
        terminal_error: list[str] = []

        def _on_state_change(state: WorkerState, error: str | None) -> None:
            if state == WorkerState.ERROR and not terminal_error:
                terminal_error.append(error or "worker entered error state")
                stop_event.set()

        runner = WorkerRunner(
            self,
            client,
            event_source=lambda kinds: client.subscribe(*kinds),
            on_state_change=_on_state_change,
        )

        runner_started = False
        try:
            await client.start()
            await runner.start()
            runner_started = True
            # If startup already errored the callback set stop_event, so this
            # returns immediately — no need to special-case it here.
            await stop_event.wait()
        finally:
            if runner_started:
                await runner.stop()
            await client.close()

        # As a *standalone* entry point we have no peer workers to keep
        # running — any ERROR transition is terminal and must surface as a
        # non-zero exit. Otherwise the parent ``SubprocessWorkerRunner`` sees
        # ``state=STOPPED`` with no clue what went wrong.
        if terminal_error:
            raise RuntimeError(terminal_error[0])


def _install_stop_signal_handlers(stop_event: asyncio.Event) -> None:
    """Install SIGTERM/SIGINT handlers that flip *stop_event*.

    POSIX uses ``loop.add_signal_handler``. On Windows that call raises
    ``NotImplementedError``; fall back to ``signal.signal`` and schedule
    the set via ``call_soon_threadsafe`` (signal handlers run outside
    the loop thread).
    """
    import signal

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except NotImplementedError:
            signal.signal(sig, lambda *_: loop.call_soon_threadsafe(stop_event.set))


def _require_async(fn: t.Any, decorator_name: str) -> None:
    """CAP-WAPI-008: All handler functions must be async."""
    if not asyncio.iscoroutinefunction(fn):
        raise TypeError(f"@worker.{decorator_name} handler must be async, got {fn!r}")
