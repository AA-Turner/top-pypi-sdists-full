"""Background workflow executor — claims and dispatches pending runs.

An asyncio worker that polls for pending workflow runs, claims them via
atomic CAS, and dispatches each to a WorkflowEngine instance. Follows
the RetentionWorker/PackRefreshWorker pattern.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ..config import WorkflowConfig
    from ..db import ThreadSafeConnection
    from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)

DEFAULT_POLL_INTERVAL = 5.0
MAX_BACKOFF_INTERVAL = 300.0
BACKOFF_MULTIPLIER = 2.0
MAX_CONSECUTIVE_FAILURES = 10


class WorkflowExecutorWorker:
    """Background worker that claims and dispatches pending workflow runs."""

    def __init__(
        self,
        config: WorkflowConfig,
        engine_factory: Callable[[], WorkflowEngine],
        db: ThreadSafeConnection,
    ) -> None:
        self._config = config
        self._engine_factory = engine_factory
        self._db = db
        self._worker_id = str(uuid.uuid4())
        self._running = False
        self._task: asyncio.Task[None] | None = None
        self._active_tasks: set[asyncio.Task[None]] = set()
        self._consecutive_failures = 0
        self._current_interval = float(config.executor_poll_interval)

    @property
    def worker_id(self) -> str:
        return self._worker_id

    @property
    def running(self) -> bool:
        return self._running

    @property
    def active_run_count(self) -> int:
        return len(self._active_tasks)

    async def wait_for_idle(self) -> None:
        """Wait for all currently dispatched runs to finish."""
        if not self._active_tasks:
            return
        await asyncio.gather(*list(self._active_tasks), return_exceptions=True)

    def _reset_backoff(self) -> None:
        self._consecutive_failures = 0
        self._current_interval = float(self._config.executor_poll_interval)

    def _apply_backoff(self) -> None:
        self._consecutive_failures += 1
        self._current_interval = min(
            float(self._config.executor_poll_interval) * (BACKOFF_MULTIPLIER**self._consecutive_failures),
            MAX_BACKOFF_INTERVAL,
        )
        logger.warning(
            "Workflow executor: %d consecutive failures, next interval %.0fs",
            self._consecutive_failures,
            self._current_interval,
        )

    async def run_once(self) -> int:
        """Run a single poll cycle. Returns number of runs dispatched."""
        from . import workflow_storage as ws

        # Reclaim stale locks each poll cycle (#1257)
        threshold = getattr(self._config, "lock_reclaim_threshold", 120)
        reclaimed = ws.reclaim_stale_locks(self._db, threshold)
        for run_id, target_ref, _was_comp in reclaimed:
            logger.info("Poll: reclaimed stale lock run=%s target=%s", run_id, target_ref)

        # Clean up completed tasks
        done = {t for t in self._active_tasks if t.done()}
        for t in done:
            self._active_tasks.discard(t)
            # Surface exceptions for logging
            if t.exception() is not None:
                logger.error("Dispatch task failed: %s", t.exception())

        available_slots = self._config.max_concurrent_runs - len(self._active_tasks)
        if available_slots <= 0:
            return 0

        claimed = ws.claim_pending_runs(self._db, self._worker_id, limit=available_slots)
        dispatched = 0
        for run in claimed:
            task = asyncio.create_task(self._dispatch_run(run))
            self._active_tasks.add(task)
            dispatched += 1

        # Run scheduler to enqueue due schedules (#969)
        if self._config.scheduler_enabled:
            try:
                from .workflow_scheduler import check_and_enqueue

                engine = self._engine_factory()
                enqueued = await check_and_enqueue(
                    self._db,
                    engine,
                    self._worker_id,
                    min_schedule_interval=self._config.min_schedule_interval,
                )
                if enqueued:
                    logger.debug("Scheduler enqueued %d run(s)", len(enqueued))
            except Exception:
                logger.exception("Scheduler check_and_enqueue failed")

        return dispatched

    async def _dispatch_run(self, run: dict[str, Any]) -> None:
        """Dispatch a single claimed run to a fresh engine instance."""
        from ..workflows.gates import register_builtin_gates
        from .workflow_engine import load_definition

        run_id = run["id"]
        workflow_id = run.get("workflow_id", "unknown")
        logger.info("Dispatching workflow run %s (workflow=%s)", run_id, workflow_id)

        try:
            # Load definition from stored content or resolve by ID
            definition_content = run.get("definition_content")
            if definition_content:
                definition = load_definition(definition_content)
            else:
                from .workflow_resolution import resolve_workflow_path

                path = resolve_workflow_path(workflow_id)
                if not path:
                    from . import workflow_storage as ws

                    ws.update_workflow_run(
                        self._db,
                        run_id,
                        status="failed",
                        stop_reason=f"workflow_not_found:{workflow_id}",
                    )
                    logger.error("Workflow %r not found for run %s", workflow_id, run_id)
                    return
                definition = load_definition(path)

            register_builtin_gates()
            engine = self._engine_factory()
            await engine.execute_enqueued_run(run_id, definition)
            logger.info("Workflow run %s completed", run_id)
        except Exception:
            logger.exception("Workflow run %s dispatch failed", run_id)
            try:
                from . import workflow_storage as ws

                current = ws.get_workflow_run(self._db, run_id)
                if current and current["status"] in ("claimed", "running"):
                    ws.update_workflow_run(
                        self._db,
                        run_id,
                        status="failed",
                        stop_reason="dispatch_exception",
                    )
            except Exception:
                logger.exception("Failed to mark run %s as failed", run_id)

    async def _recover_on_startup(self) -> None:
        """Recovery actions on first poll cycle."""
        from . import workflow_storage as ws

        # Reset stale claims from crashed workers
        stale_threshold = self._config.executor_poll_interval * 10
        reset_count = ws.reset_stale_claims(self._db, stale_threshold_seconds=stale_threshold)
        if reset_count:
            logger.info("Reset %d stale claimed runs back to pending", reset_count)

        # Reset stale schedule claims (#969)
        if self._config.scheduler_enabled:
            sched_reset = ws.reset_stale_schedule_claims(self._db, stale_threshold_seconds=stale_threshold)
            if sched_reset:
                logger.info("Reset %d stale schedule claims", sched_reset)

        # Reclaim stale locks (#1257)
        threshold = getattr(self._config, "lock_reclaim_threshold", 120)
        reclaimed = ws.reclaim_stale_locks(self._db, threshold)
        for run_id, target_ref, was_compensating in reclaimed:
            logger.info(
                "Reclaimed stale lock: run=%s target=%s compensating=%s",
                run_id,
                target_ref,
                was_compensating,
            )

    async def run_forever(self) -> None:
        """Main poll loop."""
        self._running = True
        logger.info(
            "Workflow executor started (worker=%s, poll=%ds, max_concurrent=%d)",
            self._worker_id,
            self._config.executor_poll_interval,
            self._config.max_concurrent_runs,
        )

        # First iteration: recovery
        try:
            await self._recover_on_startup()
        except Exception:
            logger.exception("Executor startup recovery failed")

        while self._running:
            try:
                dispatched = await self.run_once()
                if dispatched > 0:
                    logger.debug("Dispatched %d run(s)", dispatched)
                if self._consecutive_failures > 0:
                    self._reset_backoff()
            except Exception:
                logger.exception("Executor poll cycle failed")
                self._apply_backoff()
                if self._consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    logger.error(
                        "Workflow executor disabled after %d consecutive failures",
                        self._consecutive_failures,
                    )
                    break
            await asyncio.sleep(self._current_interval)

    def start(self) -> None:
        """Start the background executor loop."""
        self._task = asyncio.ensure_future(self.run_forever())

    def stop(self) -> None:
        """Stop the background executor loop."""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
