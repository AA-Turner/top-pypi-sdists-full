"""Capability Worker lifecycle manager.

Iterates the capability registry, evaluates worker gates, and dispatches
each worker to the appropriate runner. The manager owns registry-level
bookkeeping (``component_health``, the ``_workers`` map, restart
orchestration) and env composition for subprocess workers; the runners
own per-worker async state.

Two worker shapes (CAP-WTOP-004):

* **In-process Python workers** — imported via
  :func:`load_worker_from_def`, driven by :class:`WorkerRunner` over an
  in-process :class:`RuntimeClient`.
* **Subprocess workers** — spawned via :class:`SubprocessWorkerRunner`
  with the ``DREADNODE_RUNTIME_*`` contract injected authoritatively
  (CAP-WENV-001..003).
"""

import asyncio
import os
import time
import typing as t
from dataclasses import dataclass, field

from loguru import logger

from dreadnode.app.env import read_env_with_deprecation
from dreadnode.app.paths import worker_log_path
from dreadnode.app.server.capability_manager import CapabilityRegistry
from dreadnode.capabilities.types import (
    _expand_env_in_dict,
    _expand_env_in_list,
    _expand_env_vars,
)
from dreadnode.capabilities.worker_runner import (
    SubprocessWorkerRunner,
    WorkerRunner,
    WorkerState,
)

if t.TYPE_CHECKING:
    from dreadnode.app.client.runtime_client import RuntimeClient
    from dreadnode.app.server.runtime_events import EventBus, RuntimeEventEnvelope
    from dreadnode.capabilities.types import WorkerDef
    from dreadnode.capabilities.worker import Worker


__all__ = ["WorkerLifecycleManager", "WorkerState"]


_AnyRunner = WorkerRunner | SubprocessWorkerRunner


@dataclass
class _WorkerRuntime:
    """Registry-level bookkeeping for one worker.

    Mirrors the runner's ``state`` / ``error`` (kept in sync via the runner's
    state callback) so existing callers that read ``runtime.state`` continue
    to work. Gated-off entries (CAP-WRK-007) and import-failure ``ERROR``
    entries have no runner attached.
    """

    worker_def: "WorkerDef"
    capability_name: str
    worker: "Worker | None" = None
    client: "RuntimeClient | None" = None
    runner: _AnyRunner | None = None
    state: WorkerState = WorkerState.LOADING
    error: str | None = None

    # Retained for restart-flow tests and callers that inspect this list.
    # The runner owns the live set; this field surfaces it for introspection.
    # Empty for subprocess workers (no Python handler machinery).
    event_handler_tasks: set[asyncio.Task[None]] = field(default_factory=set)


class WorkerLifecycleManager:
    """Manages lifecycle for all capability workers.

    Mirrors MCPLifecycleManager's role. Per-worker async state lives in
    :class:`WorkerRunner`; this class only iterates, gates, and reports.
    """

    def __init__(self, event_bus: "EventBus", app: t.Any) -> None:
        self._event_bus = event_bus
        self._app = app  # FastAPI app instance for ASGI transport
        self._workers: dict[str, _WorkerRuntime] = {}  # "cap:name" -> runtime
        self._registry: CapabilityRegistry | None = None

    async def start(self, registry: CapabilityRegistry) -> None:
        """Start all workers from all capabilities.

        Called after MCP servers have started (CAP-WLIF-002). Workers start
        in parallel via TaskGroup; individual failures don't block others
        (CAP-WLIF-007). Gated-off workers (CAP-WRK-007) are registered with
        ``GATED_OFF`` state and their modules are not imported.
        """
        from dreadnode.capabilities.flags import evaluate_when

        self._registry = registry
        started_at = time.perf_counter()
        started_count = 0
        failed_count = 0
        gated_count = 0

        async def _start_one(cap_name: str, worker_def: "WorkerDef") -> None:
            nonlocal started_count, failed_count
            qualified = f"{cap_name}:{worker_def.name}"
            try:
                await self._start_worker(cap_name, worker_def, qualified)
                runtime = self._workers.get(qualified)
                if runtime and runtime.state == WorkerState.RUNNING:
                    started_count += 1
                else:
                    failed_count += 1
            except Exception:
                failed_count += 1
                logger.opt(exception=True).warning("Worker '{}' failed to start", qualified)

        async with asyncio.TaskGroup() as tg:
            for cap_name, cap in registry.capabilities.items():
                resolved = cap.resolved_flags
                for worker_def in cap.worker_defs:
                    qualified = f"{cap_name}:{worker_def.name}"
                    # CAP-WRK-007: evaluate gate before importing anything.
                    if not evaluate_when(worker_def.when, resolved):
                        gated_count += 1
                        self._register_gated_off(cap, worker_def, qualified)
                        continue
                    tg.create_task(_start_one(cap_name, worker_def))

        logger.info(
            "Worker start complete | started={} | failed={} | gated_off={} | total_ms={}",
            started_count,
            failed_count,
            gated_count,
            round((time.perf_counter() - started_at) * 1000),
        )

    def _register_gated_off(self, cap: t.Any, worker_def: "WorkerDef", qualified: str) -> None:
        """Record a gated-off worker runtime (CAP-WRK-007)."""
        runtime = _WorkerRuntime(
            worker_def=worker_def,
            capability_name=cap.name,
            state=WorkerState.GATED_OFF,
        )
        self._workers[qualified] = runtime
        logger.debug("Worker gated off: {}", qualified)

        cap_health = getattr(cap, "component_health", None)
        if cap_health is not None:
            when_names = ", ".join(worker_def.when or [])
            for entry in cap_health:
                if entry.get("kind") == "worker" and entry.get("name") == worker_def.name:
                    entry["status"] = "gated_off"
                    entry["qualified_name"] = qualified
                    entry["capability"] = cap.name
                    entry["error"] = None
                    entry["detail"] = f"Requires flag: {when_names}" if when_names else None
                    entry["when"] = list(worker_def.when or [])
                    break

    async def stop(self) -> None:
        """Stop all workers. Called before MCP teardown."""
        started_at = time.perf_counter()
        stop_targets = [
            (qualified, runtime)
            for qualified, runtime in self._workers.items()
            if runtime.state in (WorkerState.RUNNING, WorkerState.ERROR, WorkerState.STARTING)
        ]

        async with asyncio.TaskGroup() as tg:
            for qualified, runtime in stop_targets:
                tg.create_task(self._stop_worker(qualified, runtime))

        logger.info(
            "Worker stop complete | stopped={} | total_ms={}",
            len(stop_targets),
            round((time.perf_counter() - started_at) * 1000),
        )
        self._workers.clear()

    async def restart_worker(self, capability: str, worker_name: str) -> dict[str, t.Any] | None:
        """Restart a worker (CAP-WLIF-006).

        If the worker is already running, this is a no-op (``restarted=False``).
        If the worker is gated off, returns a structured error identifying the
        gating flag(s); the caller maps this to HTTP 409. Returns ``None`` if
        the worker is not found.

        The returned dict is the full :meth:`get_worker_detail` shape plus a
        ``restarted`` flag (and ``gated_off`` when applicable). The TUI
        detail pane uses this to repaint the page post-action without
        issuing a second fetch — a minimal stub left fields like
        ``process`` and ``handlers`` undefined and the UI would silently
        drop the PID / log path / recent output sections.
        """
        qualified = f"{capability}:{worker_name}"
        runtime = self._workers.get(qualified)
        if runtime is None:
            return None

        # CAP-WLIF-006: gated-off workers cannot be restarted through this
        # endpoint; the operator must flip the flag state instead.
        if runtime.state == WorkerState.GATED_OFF:
            return self._restart_response(capability, worker_name, restarted=False, gated_off=True)

        if runtime.state == WorkerState.RUNNING:
            return self._restart_response(capability, worker_name, restarted=False)

        # Stop if needed, then re-start. Gate is re-evaluated to handle the
        # case where flag state changed while the worker was in error state.
        await self._stop_worker(qualified, runtime)

        from dreadnode.capabilities.flags import evaluate_when

        cap = self._registry.capabilities.get(capability) if self._registry else None
        if cap is not None and not evaluate_when(runtime.worker_def.when, cap.resolved_flags):
            self._register_gated_off(cap, runtime.worker_def, qualified)
            return self._restart_response(capability, worker_name, restarted=False, gated_off=True)

        # CAP-WAPI-002: restarts get fresh state. Clear AFTER _stop_worker
        # drains in-flight handlers so they observe the pre-clear state.
        if runtime.worker is not None:
            runtime.worker.state.clear()
        # Cold restart — drop old runtime entry so _start_worker creates a new one.
        self._workers.pop(qualified, None)
        await self._start_worker(capability, runtime.worker_def, qualified)

        return self._restart_response(capability, worker_name, restarted=True)

    def _restart_response(
        self,
        capability: str,
        worker_name: str,
        *,
        restarted: bool,
        gated_off: bool = False,
    ) -> dict[str, t.Any]:
        """Build a restart response by layering flags onto the worker detail.

        Returning the same shape as :meth:`get_worker_detail` lets the TUI
        (and other callers) render the fresh state in place without a
        second round-trip.
        """
        detail = self.get_worker_detail(capability, worker_name)
        if detail is None:
            fallback: dict[str, t.Any] = {
                "name": worker_name,
                "capability": capability,
                "state": "unknown",
                "error": None,
                "when": [],
            }
            detail = fallback
        detail["restarted"] = restarted
        if gated_off:
            detail["gated_off"] = True
        return detail

    def get_worker_detail(self, capability: str, worker_name: str) -> dict[str, t.Any] | None:
        """Return status dict for a worker, or None if not found."""
        qualified = f"{capability}:{worker_name}"
        runtime = self._workers.get(qualified)
        if runtime is None:
            return None

        worker = runtime.worker
        worker_def = runtime.worker_def
        base: dict[str, t.Any] = {
            "name": worker.name if worker is not None else worker_def.name,
            "qualified_name": qualified,
            "capability": runtime.capability_name,
            "state": runtime.state.value,
            "error": runtime.error,
            "when": list(worker_def.when or []),
            "kind": "subprocess" if worker_def.is_subprocess else "inprocess",
        }
        if worker_def.is_subprocess:
            # Subprocess workers have no Python handler registry (CAP-WTOP-009).
            runner = runtime.runner
            pid = getattr(runner, "pid", None) if runner is not None else None
            log_path = getattr(runner, "log_path", None) if runner is not None else None
            recent_output = list(getattr(runner, "recent_output", [])) if runner is not None else []
            return {
                **base,
                "handlers": None,
                "process": {
                    "command": worker_def.command,
                    "args": list(worker_def.args),
                    "pid": pid,
                    "log_path": str(log_path) if log_path is not None else None,
                    "recent_output": recent_output,
                },
            }
        if worker is None:
            # GATED_OFF or import-failure ERROR — no handler counts available.
            return {**base, "handlers": None}
        return {
            **base,
            "handlers": {
                "startup": len(worker._startup_handlers),
                "shutdown": len(worker._shutdown_handlers),
                "event_kinds": list(worker._event_handlers.keys()),
                "schedules": len(worker._every_handlers),
                "tasks": len(worker._task_handlers),
            },
        }

    # ── Internal lifecycle ────────────────────────────────────────

    async def _start_worker(self, cap_name: str, worker_def: "WorkerDef", qualified: str) -> None:
        """Drive a gated-on worker through its full start sequence.

        Branches on ``worker_def.is_subprocess``: in-process workers import the
        Python module and hand off to :class:`WorkerRunner`; subprocess workers
        go through :class:`SubprocessWorkerRunner` with the ``DREADNODE_RUNTIME_*``
        env contract (CAP-WENV-001..003) injected authoritatively.
        """
        runtime = _WorkerRuntime(
            worker_def=worker_def,
            capability_name=cap_name,
            state=WorkerState.LOADING,
        )
        self._workers[qualified] = runtime

        cap = self._registry.capabilities.get(cap_name) if self._registry else None
        if cap is None:
            runtime.state = WorkerState.ERROR
            runtime.error = f"Capability '{cap_name}' missing from registry"
            self._update_health(runtime, "error", runtime.error)
            return

        if worker_def.is_subprocess:
            await self._start_subprocess_worker(cap, worker_def, runtime, qualified)
        else:
            await self._start_inprocess_worker(cap, worker_def, runtime, qualified)

    async def _start_inprocess_worker(
        self,
        cap: t.Any,
        worker_def: "WorkerDef",
        runtime: _WorkerRuntime,
        qualified: str,
    ) -> None:
        """Start a Python in-process worker via :class:`WorkerRunner`."""
        from dreadnode.capabilities.loader import load_worker_from_def

        try:
            worker = load_worker_from_def(worker_def, cap.path, cap.name)
        except Exception as exc:
            # CAP-WRK-003: module import / structure failure → error state.
            runtime.state = WorkerState.ERROR
            runtime.error = str(exc)
            self._update_health(runtime, "error", str(exc))
            logger.opt(exception=True).warning("Worker '{}' module failed to load", qualified)
            return

        runtime.worker = worker
        client = self._create_worker_client(cap, worker.name)
        runtime.client = client

        runner = WorkerRunner(
            worker,
            client,
            event_source=self._event_bus_source,
            on_state_change=self._make_mirror_state(runtime),
            qualified_name=qualified,
        )
        runtime.runner = runner
        # Expose the runner's live event-handler task set for introspection.
        runtime.event_handler_tasks = runner._event_handler_tasks

        await runner.start()
        if runner.state == WorkerState.RUNNING:
            logger.info("Worker started: {}", qualified)

    async def _start_subprocess_worker(
        self,
        cap: t.Any,
        worker_def: "WorkerDef",
        runtime: _WorkerRuntime,
        qualified: str,
    ) -> None:
        """Spawn a subprocess worker and hand off to :class:`SubprocessWorkerRunner`."""
        assert worker_def.command is not None  # parse-time invariant (CAP-WTOP-004)
        env = self._build_subprocess_env(cap, worker_def)
        log_path = worker_log_path(cap.name, worker_def.name)
        runner = SubprocessWorkerRunner(
            _expand_env_vars(worker_def.command),
            _expand_env_in_list(worker_def.args),
            env=env,
            cwd=cap.path,
            log_path=log_path,
            on_state_change=self._make_mirror_state(runtime),
            qualified_name=qualified,
        )
        runtime.runner = runner
        await runner.start()
        if runner.state == WorkerState.RUNNING:
            logger.info("Subprocess worker started: {} (pid={})", qualified, runner.pid)

    def _make_mirror_state(
        self, runtime: _WorkerRuntime
    ) -> t.Callable[[WorkerState, str | None], None]:
        """Closure that mirrors runner state onto the registry + component_health."""

        def _mirror(state: WorkerState, error: str | None) -> None:
            runtime.state = state
            runtime.error = error
            if state == WorkerState.RUNNING:
                self._update_health(runtime, "ok", None)
            elif state == WorkerState.ERROR:
                self._update_health(runtime, "error", error)
            elif state == WorkerState.STOPPED:
                # STOPPED with an error means clean shutdown path raised a
                # shutdown-handler exception (CAP-WAPI-011). Surface it so
                # operators can see cleanup didn't complete cleanly.
                self._update_health(runtime, "stopped", error)

        return _mirror

    def _build_subprocess_env(self, cap: t.Any, worker_def: "WorkerDef") -> dict[str, str]:
        """Compose the env passed to a subprocess worker.

        Layering (lowest to highest precedence, CAP-WTOP-005/006, CAP-WENV-002):

        1. :data:`os.environ` — the runtime's own process environment is
           inherited so workers see the same base as other capability subprocesses
           (mirrors CAP-MCP-005).
        2. ``CAPABILITY_FLAG__*`` convention env vars (CAP-FLAG-020).
        3. Manifest ``env:`` entries (``${CAPABILITY_ROOT}`` is resolved at
           parse time; ``${VAR}`` / ``${VAR:-default}`` placeholders are
           resolved here against the merged base env, mirroring
           :meth:`MCPServerDef.to_server_config`).
        4. ``DREADNODE_RUNTIME_{URL,TOKEN,ID}`` and worker/session context —
           authoritative; overrides any of the previous layers so the runtime
           owns the connection identity and platform session metadata.
        """
        flag_env = cap.flag_env_vars() if hasattr(cap, "flag_env_vars") else {}
        env = {**os.environ, **flag_env, **_expand_env_in_dict(worker_def.env)}
        env.update(self._runtime_contract_env())
        env["DREADNODE_SESSION_ORIGIN"] = "worker"
        env["DREADNODE_WORKER_NAME"] = worker_def.name
        session_group_id = os.environ.get("DREADNODE_SESSION_GROUP_ID", "").strip()
        if session_group_id:
            env["DREADNODE_SESSION_GROUP_ID"] = session_group_id
        if getattr(cap, "name", None):
            env["DREADNODE_CAPABILITY_NAME"] = str(cap.name)
            org = os.environ.get("DREADNODE_ORG") or os.environ.get("DREADNODE_ORGANIZATION")
            env["DREADNODE_CAPABILITY_LABEL"] = (
                str(cap.name) if "/" in str(cap.name) or not org else f"{org}/{cap.name}"
            )
        if getattr(cap, "version", None):
            env["DREADNODE_CAPABILITY_VERSION"] = str(cap.version)
        return env

    @staticmethod
    def _runtime_contract_env() -> dict[str, str]:
        """Build the authoritative ``DREADNODE_RUNTIME_*`` layer.

        Primary source of truth is :class:`ServerState` — populated by whoever
        owns the bound socket (``ManagedRuntimeClient`` for the TUI's
        in-process runtime, ``run_server()`` for ``dn serve``). When state
        isn't populated (e.g. a sandbox-hosted worker that never ran through
        either of those paths), fall back to env vars; in that path
        ``DREADNODE_RUNTIME_URL`` is always composed against ``127.0.0.1``
        because the bind host may be ``0.0.0.0`` and unreachable as a connect
        target.
        """
        from dreadnode.app.server.app import get_state

        state = get_state()
        env: dict[str, str] = {}

        if state.runtime_url is not None:
            env["DREADNODE_RUNTIME_URL"] = state.runtime_url
        else:
            port = read_env_with_deprecation(
                "DREADNODE_RUNTIME_PORT", "DREADNODE_SERVER_PORT", "8787"
            )
            env["DREADNODE_RUNTIME_URL"] = f"http://127.0.0.1:{port}"

        token = state.runtime_token or read_env_with_deprecation(
            "DREADNODE_RUNTIME_TOKEN", "SANDBOX_AUTH_TOKEN"
        )
        if token is not None:
            env["DREADNODE_RUNTIME_TOKEN"] = token

        runtime_id = state.runtime_id or os.environ.get("DREADNODE_RUNTIME_ID")
        if runtime_id is not None:
            env["DREADNODE_RUNTIME_ID"] = runtime_id

        return env

    async def _stop_worker(self, qualified: str, runtime: _WorkerRuntime) -> None:
        """Stop a single worker through its full stopping sequence."""
        runner = runtime.runner
        if runner is not None:
            await runner.stop()
        else:
            # Import-failure ERROR runtime: no runner was ever attached.
            runtime.state = WorkerState.STOPPED
            self._update_health(runtime, "stopped", None)

        # Close client (CAP-WCLI-002). The manager owns client construction,
        # so it also owns close — the runner doesn't know how the transport
        # was wired.
        if runtime.client is not None:
            await runtime.client.close()

        logger.debug("Worker stopped: {}", qualified)

    def _create_worker_client(self, cap: t.Any, worker_name: str) -> "RuntimeClient":
        """Construct an in-process RuntimeClient for a worker.

        Uses StreamingASGITransport pointed at the running app to keep
        workers topology-agnostic (CAP-WTOP-001). The client's
        ``default_notify_source`` is set to ``capability.<name>`` so
        :meth:`RuntimeClient.notify` attributes emissions to the hosting
        capability by default (CAP-WCLI-014). ``default_session_origin``
        sets ``origin=worker`` (SES-ORG-003) and ``default_session_labels``
        stamps ``worker:<name>`` (SES-LBL-024) on every session the worker
        creates (CAP-WCLI-022) — capability authors do not pass these
        values explicitly.
        """
        from dreadnode.app.client.runtime_client import RuntimeClient
        from dreadnode.app.client.transports import StreamingASGITransport

        transport = StreamingASGITransport(app=self._app)
        client = RuntimeClient(
            server_url="http://localhost",
            transport=transport,
            default_notify_source=f"capability.{cap.name}",
            default_session_origin="worker",
            default_session_labels={
                "worker": [worker_name],
            },
        )
        # Skip health check for in-process — server is already running.
        client._started = True
        return client

    async def _event_bus_source(
        self, kinds: frozenset[str]
    ) -> t.AsyncIterator["RuntimeEventEnvelope"]:
        """In-process event source: subscribe to the runtime bus and yield envelopes.

        Passed to :class:`WorkerRunner` via ``event_source=``. The async
        generator's ``finally`` unsubscribes when the consumer exits or is
        cancelled, so the bus doesn't accumulate stale subscriptions.
        """
        subscription = await self._event_bus.subscribe(kinds=kinds, include_runtime=True)
        try:
            while True:
                yield await subscription.queue.get()
        finally:
            await self._event_bus.unsubscribe(subscription)

    # ── Health ────────────────────────────────────────────────────

    def _update_health(self, runtime: _WorkerRuntime, status: str, error: str | None) -> None:
        """Update the component_health entry for this worker.

        Also publishes a ``component.state_changed`` runtime event so
        subscribers (the TUI in particular) can patch their cached
        ``runtime_info`` snapshots in place instead of polling. Publish
        is fire-and-forget — health bookkeeping is not on the runtime
        critical path and we never want a bus failure to mask a state
        change to the registry.
        """
        if self._registry is None:
            return
        cap = self._registry.capabilities.get(runtime.capability_name)
        if cap is None:
            return
        # Worker.name is Optional; worker_def.name is not — fall back so the
        # event payload and health lookup always see a concrete string.
        name = (
            runtime.worker.name
            if runtime.worker is not None and runtime.worker.name
            else runtime.worker_def.name
        )
        detail: str | None = None
        for entry in getattr(cap, "component_health", []):
            if entry.get("kind") == "worker" and entry.get("name") == name:
                entry["status"] = status
                entry["error"] = error
                detail = entry.get("detail")
                break
        self._publish_state_changed(
            capability=runtime.capability_name,
            name=name,
            kind="worker",
            status=status,
            error=error,
            detail=detail,
        )

    def _publish_state_changed(
        self,
        *,
        capability: str,
        name: str,
        kind: str,
        status: str,
        error: str | None,
        detail: str | None,
        tool_count: int | None = None,
    ) -> None:
        """Schedule a ``component.state_changed`` publish on the bus."""
        from dreadnode.app.server import runtime_events

        payload: dict[str, t.Any] = {
            "capability": capability,
            "name": name,
            "kind": kind,
            "status": status,
            "error": error,
            "detail": detail,
        }
        if tool_count is not None:
            payload["tool_count"] = tool_count
        try:
            asyncio.create_task(  # noqa: RUF006
                self._event_bus.publish(
                    kind=runtime_events.EVENT_COMPONENT_STATE_CHANGED,
                    payload=payload,
                ),
                name=f"component-state-publish:{capability}:{name}",
            )
        except RuntimeError:
            # No running loop (test teardown / sync caller); drop the publish
            # rather than crash — the registry mutation already happened.
            logger.debug(
                "component.state_changed: no running loop, skipping publish | {}:{}",
                capability,
                name,
            )
