"""Per-worker async lifecycle drivers.

Two driver shapes share a single :class:`WorkerState` enum:

* :class:`WorkerRunner` — for in-process Python workers. Drives a single
  :class:`Worker` instance's async topology (``on_startup``/``on_shutdown``,
  event dispatch, recurring schedules, supervised tasks). Topology-agnostic
  (CAP-WTOP-001): callers supply the :class:`RuntimeClient` and an
  event-source callable, so the same runner works both in-process (event
  source reads from the runtime :class:`EventBus`) and standalone (event
  source reads from ``RuntimeClient.subscribe`` per CAP-WCLI-018).
* :class:`SubprocessWorkerRunner` — for capability-declared subprocess
  workers (CAP-WTOP-004..009). Spawns a process, supervises its exit, and
  terminates with SIGTERM/grace/SIGKILL on stop. Handler-registry rules do
  not apply here (CAP-WTOP-009); lifecycle/health/gating rules do.

Both runners expose the same ``start()``/``stop()``/``state``/``error``
interface so :class:`WorkerLifecycleManager` can branch on manifest kind
without knowing which is which at the call site.
"""

import asyncio
import collections
import contextlib
import time
import typing as t
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from loguru import logger

from dreadnode.app.paths import rotate_log

if t.TYPE_CHECKING:
    from dreadnode.app.client.runtime_client import RuntimeClient
    from dreadnode.app.server.runtime_events import RuntimeEventEnvelope
    from dreadnode.capabilities.worker import ScheduleSpec, Worker


class WorkerState(StrEnum):
    """Worker lifecycle states (CAP-WLIF-001)."""

    LOADING = "loading"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    # CAP-WRK-007: manifest-declared but when: predicate unsatisfied; module
    # not imported, no handlers registered.
    GATED_OFF = "gated_off"


EventSource = t.Callable[[frozenset[str]], t.AsyncIterator["RuntimeEventEnvelope"]]
"""Callable that, given a set of kinds, returns an async iterator of envelopes.

In-process wiring points this at an EventBus-subscription adapter; standalone
wiring points it at ``RuntimeClient.subscribe``. The iterator's own teardown
(via ``aclose`` or consumer cancellation) is expected to release the
underlying subscription — the runner does not manage it out-of-band.
"""

StateCallback = t.Callable[[WorkerState, str | None], None]
"""Invoked on every state transition with ``(new_state, error_or_none)``."""


@dataclass
class _TaskSupervisor:
    """Supervises a single @worker.task handler with exponential backoff."""

    handler: t.Callable[..., t.Awaitable[None]]
    task: asyncio.Task[None] | None = None
    consecutive_crashes: int = 0
    last_start: float = 0.0

    # Backoff parameters (implementation detail per CAP-WLIF-008)
    BASE_DELAY: t.ClassVar[float] = 1.0
    MAX_DELAY: t.ClassVar[float] = 300.0  # 5 minutes
    STABILITY_THRESHOLD: t.ClassVar[float] = 60.0  # seconds before reset


class WorkerRunner:
    """Drive one worker's async topology from startup through stop.

    Ownership:

    * Decorator-handler orchestration (``on_startup``, ``on_shutdown``,
      ``on_event``, ``every``, ``task``).
    * Internal async tasks for event dispatch, schedules, and supervised tasks.
    * State transitions (CAP-WLIF-001, CAP-WLIF-009).

    Not owned:

    * :class:`RuntimeClient` construction and closure — callers build and close.
    * Event-source subscription lifetime — the :data:`EventSource` callable's
      async iterator owns its own subscription; the runner consumes until
      cancelled.
    * Health records — callers observe state via :meth:`state` /
      :attr:`error` or via ``on_state_change``.
    """

    def __init__(
        self,
        worker: "Worker",
        client: "RuntimeClient",
        *,
        event_source: EventSource,
        on_state_change: StateCallback | None = None,
        qualified_name: str | None = None,
    ) -> None:
        self.worker = worker
        self.client = client
        self._event_source = event_source
        self._on_state_change = on_state_change
        # Log context only — no semantic meaning.
        self._qualified = qualified_name or (worker.name or "worker")

        self._state: WorkerState = WorkerState.LOADING
        self._error: str | None = None

        self._event_stream: t.AsyncIterator[RuntimeEventEnvelope] | None = None
        self._event_dispatch_task: asyncio.Task[None] | None = None
        self._event_handler_tasks: set[asyncio.Task[None]] = set()
        self._schedule_tasks: list[asyncio.Task[None]] = []
        self._task_supervisors: list[_TaskSupervisor] = []

    @property
    def state(self) -> WorkerState:
        return self._state

    @property
    def error(self) -> str | None:
        return self._error

    def _transition(self, state: WorkerState, error: str | None = None) -> None:
        self._state = state
        self._error = error
        if self._on_state_change is not None:
            self._on_state_change(state, error)

    async def start(self) -> None:
        """Run ``on_startup`` sequentially, then spawn all handler loops.

        Transitions ``LOADING`` → ``STARTING`` → ``RUNNING`` on success. On
        any ``on_startup`` exception, transitions to ``ERROR`` (CAP-WLIF-001,
        CAP-WAPI-011) without spawning handler loops.
        """
        self._transition(WorkerState.STARTING)
        worker = self.worker
        client = self.client

        try:
            for handler in worker._startup_handlers:
                await handler(client)

            if worker._event_handlers:
                kinds = frozenset(worker._event_handlers.keys())
                self._event_stream = self._event_source(kinds)
                self._event_dispatch_task = asyncio.create_task(
                    self._event_dispatch_loop(),
                    name=f"worker-events:{self._qualified}",
                )

            for i, (spec, handler) in enumerate(worker._every_handlers):
                schedule_task = asyncio.create_task(
                    self._schedule_loop(spec, handler),
                    name=f"worker-schedule:{self._qualified}:{i}",
                )
                self._schedule_tasks.append(schedule_task)

            for i, handler in enumerate(worker._task_handlers):
                supervisor = _TaskSupervisor(handler=handler)
                self._task_supervisors.append(supervisor)
                supervisor.task = asyncio.create_task(
                    self._supervised_task_loop(supervisor),
                    name=f"worker-task:{self._qualified}:{i}",
                )

            self._transition(WorkerState.RUNNING)
        except Exception as exc:
            self._transition(WorkerState.ERROR, str(exc))
            logger.opt(exception=True).warning("Worker '{}' startup failed", self._qualified)

    async def stop(self) -> None:
        """Cancel handler loops, drain in-flight events, run ``on_shutdown``.

        The drain must precede ``on_shutdown`` and client close (CAP-WLIF-004,
        CAP-WAPI-011) so handlers do not observe torn-down state or write
        against a closed client. Shutdown handler exceptions are logged, not
        propagated.
        """
        self._transition(WorkerState.STOPPING)

        # Cancel dispatch first so no new handler tasks are spawned while
        # we're tearing down.
        all_tasks: list[asyncio.Task[None]] = []
        if self._event_dispatch_task and not self._event_dispatch_task.done():
            self._event_dispatch_task.cancel()
            all_tasks.append(self._event_dispatch_task)
        for supervisor in self._task_supervisors:
            if supervisor.task and not supervisor.task.done():
                supervisor.task.cancel()
                all_tasks.append(supervisor.task)
        for schedule_task in self._schedule_tasks:
            if not schedule_task.done():
                schedule_task.cancel()
                all_tasks.append(schedule_task)
        # Drain in-flight on_event handler invocations before running
        # on_shutdown so handlers don't observe a torn-down worker state.
        for handler_task in list(self._event_handler_tasks):
            if not handler_task.done():
                handler_task.cancel()
                all_tasks.append(handler_task)

        if all_tasks:
            await asyncio.gather(*all_tasks, return_exceptions=True)

        # Release the event-source subscription. Cancellation of the dispatch
        # task already runs the iterator's finally in most cases, but aclose()
        # is the contract-level way to signal end-of-consumption.
        if self._event_stream is not None:
            aclose = getattr(self._event_stream, "aclose", None)
            if aclose is not None:
                try:
                    await aclose()
                except Exception:
                    logger.opt(exception=True).debug(
                        "Worker '{}' event-stream close raised (ignored)", self._qualified
                    )
            self._event_stream = None

        # on_shutdown in reverse registration order (CAP-WAPI-011). Exceptions
        # are logged and surfaced via the terminal state's error message so
        # operators can see that cleanup didn't complete cleanly — the worker
        # still transitions to STOPPED (it is not coming back).
        shutdown_errors: list[str] = []
        for handler in reversed(self.worker._shutdown_handlers):
            try:
                await handler(self.client)
            except Exception as exc:
                logger.opt(exception=True).warning(
                    "Worker '{}' shutdown handler error", self._qualified
                )
                handler_name = getattr(handler, "__qualname__", None) or getattr(
                    handler, "__name__", "<handler>"
                )
                shutdown_errors.append(f"{handler_name}: {exc}")

        if shutdown_errors:
            self._transition(
                WorkerState.STOPPED,
                "shutdown errors: " + "; ".join(shutdown_errors),
            )
        else:
            self._transition(WorkerState.STOPPED)

    # ── Event dispatch ────────────────────────────────────────────

    async def _event_dispatch_loop(self) -> None:
        """Read from the event source and fan out to ``on_event`` handlers."""
        assert self._event_stream is not None
        worker = self.worker
        try:
            async for envelope in self._event_stream:
                handlers = worker._event_handlers.get(envelope.kind, [])
                for handler in handlers:
                    # CAP-WAPI-017: concurrent dispatch allowed.
                    handler_task = asyncio.create_task(
                        self._invoke_event_handler(handler, envelope),
                        name=f"worker-event-handler:{self._qualified}:{envelope.kind}",
                    )
                    self._event_handler_tasks.add(handler_task)
                    handler_task.add_done_callback(self._event_handler_tasks.discard)
        except asyncio.CancelledError:
            return

    async def _invoke_event_handler(
        self,
        handler: t.Callable[..., t.Awaitable[None]],
        envelope: "RuntimeEventEnvelope",
    ) -> None:
        """Invoke one ``on_event`` handler; swallow exceptions (CAP-WAPI-016)."""
        try:
            await handler(envelope, self.client)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.opt(exception=True).warning(
                "Worker '{}' event handler error for kind={}",
                self._qualified,
                envelope.kind,
            )

    # ── Scheduling ────────────────────────────────────────────────

    async def _schedule_loop(
        self,
        spec: "ScheduleSpec",
        handler: t.Callable[..., t.Awaitable[None]],
    ) -> None:
        """Run a scheduled handler on its configured interval."""
        while True:
            delay = self._compute_next_delay(spec)
            await asyncio.sleep(delay)
            try:
                await handler(self.client)
            except asyncio.CancelledError:
                return
            except Exception:
                # CAP-WAPI-016: swallow, remain active.
                logger.opt(exception=True).warning(
                    "Worker '{}' scheduled handler error", self._qualified
                )

    @staticmethod
    def _compute_next_delay(spec: "ScheduleSpec") -> float:
        """Compute seconds until the next scheduled invocation."""
        if spec.interval_seconds is not None:
            return spec.interval_seconds
        if spec.cron_expr is not None:
            from croniter import croniter

            cron = croniter(spec.cron_expr)
            return max(0.0, cron.get_next(float) - time.time())
        return 60.0  # fallback

    # ── Task supervision ──────────────────────────────────────────

    async def _supervised_task_loop(self, supervisor: _TaskSupervisor) -> None:
        """Supervise a @worker.task with exponential backoff (CAP-WLIF-008)."""
        while True:
            supervisor.last_start = time.monotonic()
            try:
                await supervisor.handler(self.client)
            except asyncio.CancelledError:
                return
            except Exception:
                logger.opt(exception=True).warning(
                    "Worker '{}' task crashed, will restart", self._qualified
                )

            run_duration = time.monotonic() - supervisor.last_start
            if run_duration >= _TaskSupervisor.STABILITY_THRESHOLD:
                supervisor.consecutive_crashes = 0
            else:
                supervisor.consecutive_crashes += 1

            delay = min(
                _TaskSupervisor.BASE_DELAY * (2**supervisor.consecutive_crashes),
                _TaskSupervisor.MAX_DELAY,
            )

            # CAP-WLIF-009: if every OTHER supervisor's loop has exited
            # (task.done()), the worker transitions to error. This
            # supervisor is still looping, so we only error when the rest
            # have given up.
            others = [s for s in self._task_supervisors if s is not supervisor]
            if others and all(s.task is not None and s.task.done() for s in others):
                self._transition(WorkerState.ERROR, "All tasks crashed")
                logger.warning(
                    "Worker '{}' — all tasks crashed, entering error state",
                    self._qualified,
                )
                return

            # CAP-WHLTH-005: in backoff but will retry → stay running.
            await asyncio.sleep(delay)


class SubprocessWorkerRunner:
    """Drive a capability-declared subprocess worker (CAP-WTOP-004..009).

    Spawns the process on :meth:`start`, watches its lifetime via an
    exit-watcher task, and terminates with SIGTERM → grace period →
    SIGKILL on :meth:`stop`. State transitions match the in-process
    runner's enum so :class:`WorkerLifecycleManager` can treat both
    runner shapes uniformly.

    Ownership:

    * Subprocess lifetime and termination.
    * State transitions (CAP-WLIF-001 mapped to process state per
      CAP-WTOP-007).

    Not owned:

    * Manifest parsing / ``${CAPABILITY_ROOT}`` interpolation
      (done at parse time in :func:`parse_workers`).
    * Env composition — the caller builds the full env including
      inherited :data:`os.environ`, flag env vars, manifest env, and
      the authoritative ``DREADNODE_RUNTIME_*`` contract (CAP-WENV-001..003).
    * ``component_health`` bookkeeping — callers observe state via
      :attr:`state` / :attr:`error` or via ``on_state_change``.
    """

    # Default grace window between SIGTERM and SIGKILL (CAP-WTOP-007).
    DEFAULT_GRACE_PERIOD_S: t.ClassVar[float] = 5.0
    # Combined stdout+stderr lines retained in memory for the detail view
    # and for attaching a tail to the exit error message.
    OUTPUT_BUFFER_LINES: t.ClassVar[int] = 200
    # Lines appended to the error message when the process exits non-zero.
    ERROR_TAIL_LINES: t.ClassVar[int] = 20
    # Marker that separates the exit message from the captured output tail
    # in the error string. The TUI splits on this to render a styled block.
    OUTPUT_ERROR_MARKER: t.ClassVar[str] = "\n\nWorker output:\n"

    def __init__(
        self,
        command: str,
        args: list[str],
        *,
        env: dict[str, str],
        cwd: Path,
        log_path: Path | None = None,
        on_state_change: StateCallback | None = None,
        qualified_name: str | None = None,
        grace_period_s: float | None = None,
    ) -> None:
        self._command = command
        self._args = list(args)
        self._env = dict(env)
        self._cwd = cwd
        self._log_path = log_path
        self._on_state_change = on_state_change
        self._qualified = qualified_name or "worker"
        self._grace_period_s = (
            grace_period_s if grace_period_s is not None else self.DEFAULT_GRACE_PERIOD_S
        )

        self._state: WorkerState = WorkerState.LOADING
        self._error: str | None = None
        self._proc: asyncio.subprocess.Process | None = None
        self._exit_task: asyncio.Task[None] | None = None
        self._tee_task: asyncio.Task[None] | None = None
        self._log_file: t.IO[bytes] | None = None
        self._output_buffer: collections.deque[str] = collections.deque(
            maxlen=self.OUTPUT_BUFFER_LINES
        )

    @property
    def state(self) -> WorkerState:
        return self._state

    @property
    def error(self) -> str | None:
        return self._error

    @property
    def pid(self) -> int | None:
        """OS process id, or ``None`` if the worker hasn't spawned (or has exited)."""
        if self._proc is None:
            return None
        return self._proc.pid

    @property
    def log_path(self) -> Path | None:
        """Path that stdout/stderr is redirected to, or ``None`` if not configured."""
        return self._log_path

    @property
    def recent_output(self) -> list[str]:
        """Tail of combined stdout+stderr lines captured from the subprocess.

        Bounded by :attr:`OUTPUT_BUFFER_LINES`. Mirrors what was written to
        the log file (when configured) and drives the TUI's recent-output
        block so operators can troubleshoot a failed worker without having
        to open the log file by hand.
        """
        return list(self._output_buffer)

    def _transition(self, state: WorkerState, error: str | None = None) -> None:
        self._state = state
        self._error = error
        if self._on_state_change is not None:
            self._on_state_change(state, error)

    async def start(self) -> None:
        """Spawn the subprocess and transition to ``RUNNING`` on success.

        On spawn failure, transitions to ``ERROR`` with the spawn error
        message (CAP-WTOP-008) and returns without raising — aligning
        with the in-process runner's non-raising startup and letting
        :class:`WorkerLifecycleManager` continue starting other workers
        (CAP-WLIF-007).

        Combined stdout+stderr is streamed through a pipe so a background
        tee task can both persist to the log file and retain the tail in
        memory for the detail view (:attr:`recent_output`). This keeps
        parity with :class:`MCPClient`'s stderr-capture behaviour so
        operators can troubleshoot a failed worker from the TUI without
        opening the log file by hand.
        """
        self._transition(WorkerState.STARTING)
        self._output_buffer.clear()
        self._log_file = self._open_log_file()
        try:
            self._proc = await asyncio.create_subprocess_exec(
                self._command,
                *self._args,
                env=self._env,
                cwd=str(self._cwd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
        except (OSError, ValueError) as exc:
            self._transition(WorkerState.ERROR, f"spawn failed: {exc}")
            self._close_log_file()
            logger.opt(exception=True).warning(
                "Subprocess worker '{}' failed to spawn", self._qualified
            )
            return

        self._tee_task = asyncio.create_task(
            self._tee_output(),
            name=f"worker-tee:{self._qualified}",
        )
        self._exit_task = asyncio.create_task(
            self._watch_exit(),
            name=f"worker-exit:{self._qualified}",
        )
        self._transition(WorkerState.RUNNING)
        logger.debug("Subprocess worker '{}' running (pid={})", self._qualified, self._proc.pid)

    def _open_log_file(self) -> t.IO[bytes] | None:
        """Open the log file for appending subprocess output, or ``None``.

        Rotates any prior log to ``<path>.prev`` so operators retain one
        level of history across restarts without accumulating an unbounded
        archive. Returns ``None`` when no log path is configured or the
        file cannot be opened (permission / OS error). The in-memory ring
        buffer still captures output even when no log file is available,
        so the TUI can surface recent lines either way.
        """
        if self._log_path is None:
            return None
        rotate_log(self._log_path)
        try:
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
            return self._log_path.open("wb")
        except OSError as exc:
            logger.warning(
                "Subprocess worker '{}': failed to open log file '{}' ({}); keeping in-memory buffer only",
                self._qualified,
                self._log_path,
                exc,
            )
            return None

    def _close_log_file(self) -> None:
        if self._log_file is not None:
            with contextlib.suppress(OSError):
                self._log_file.close()
            self._log_file = None

    async def _tee_output(self) -> None:
        """Tee combined stdout+stderr to the log file and the ring buffer.

        Runs until the child closes its stdout (EOF on the pipe) or the
        task is cancelled. Closes the log file in ``finally`` so a crashed
        tee loop does not leak a handle across restarts.
        """
        assert self._proc is not None
        assert self._proc.stdout is not None
        try:
            async for raw in self._proc.stdout:
                if self._log_file is not None:
                    try:
                        self._log_file.write(raw)
                        self._log_file.flush()
                    except OSError:
                        # A full disk / closed handle mid-write shouldn't stop
                        # the in-memory buffer from working — operators still
                        # see output in the TUI even if the file is gone.
                        pass
                line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                if line:
                    self._output_buffer.append(line)
        except asyncio.CancelledError:
            return
        finally:
            self._close_log_file()

    async def _drain_tee(self) -> None:
        """Await the tee task so the buffer reflects everything the child wrote.

        Called after ``proc.wait()`` returns but before we build the error
        message, so the appended tail isn't racing the final stderr flush.
        """
        task = self._tee_task
        if task is None or task.done():
            return
        with contextlib.suppress(asyncio.CancelledError, Exception):
            await task

    def _build_exit_error(self, returncode: int) -> str:
        """Format the ERROR-state message with a tail of recent output.

        Mirrors :class:`MCPClient`'s ``Server stderr:`` pattern so the TUI
        has a predictable marker to split on.
        """
        base = f"exited with code {returncode}"
        if not self._output_buffer:
            return base
        tail = "\n".join(list(self._output_buffer)[-self.ERROR_TAIL_LINES :])
        return f"{base}{self.OUTPUT_ERROR_MARKER}{tail}"

    async def _watch_exit(self) -> None:
        """Observe the subprocess exit and transition to a terminal state.

        :meth:`stop` drives the terminal transition when it is the one
        ending the process (state is ``STOPPING`` when the exit is seen).
        An exit observed while the runner is still ``RUNNING`` is
        unexpected and maps to ``STOPPED`` (clean) or ``ERROR`` (non-zero)
        per CAP-WTOP-007.
        """
        assert self._proc is not None
        try:
            returncode = await self._proc.wait()
        except asyncio.CancelledError:
            return
        # Drain tee before we decide the terminal message so the buffer
        # reflects any final stderr/stdout the child flushed on its way out.
        await self._drain_tee()
        if self._state == WorkerState.STOPPING:
            return  # stop() owns the final transition
        if returncode == 0:
            self._transition(WorkerState.STOPPED)
            logger.info("Subprocess worker '{}' exited cleanly (code=0)", self._qualified)
        else:
            self._transition(WorkerState.ERROR, self._build_exit_error(returncode))
            logger.warning(
                "Subprocess worker '{}' exited unexpectedly with code {}",
                self._qualified,
                returncode,
            )

    async def stop(self) -> None:
        """Terminate the subprocess with SIGTERM, escalating to SIGKILL after grace.

        Idempotent: calling :meth:`stop` when the subprocess has already
        exited (watcher already ran) reaps the watcher task and leaves
        the terminal state (``STOPPED`` or ``ERROR``) as-is.
        """
        proc = self._proc
        if proc is None:
            # Never spawned (start() hit a spawn error) — ensure terminal state.
            if self._state not in (WorkerState.ERROR, WorkerState.STOPPED):
                self._transition(WorkerState.STOPPED)
            return

        # If the watcher has already observed the exit, just reap it.
        if self._state in (WorkerState.STOPPED, WorkerState.ERROR):
            await self._reap_exit_task()
            return

        self._transition(WorkerState.STOPPING)
        if proc.returncode is None:
            with contextlib.suppress(ProcessLookupError):
                proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=self._grace_period_s)
            except TimeoutError:
                logger.warning(
                    "Subprocess worker '{}' did not exit within {}s; sending SIGKILL",
                    self._qualified,
                    self._grace_period_s,
                )
                with contextlib.suppress(ProcessLookupError):
                    proc.kill()
                await proc.wait()

        await self._reap_exit_task()
        self._transition(WorkerState.STOPPED)
        logger.debug("Subprocess worker '{}' stopped", self._qualified)

    async def _reap_exit_task(self) -> None:
        task = self._exit_task
        if task is None or task.done():
            return
        try:
            await task
        except Exception:
            logger.opt(exception=True).debug(
                "Subprocess worker '{}' exit watcher raised (ignored)", self._qualified
            )
