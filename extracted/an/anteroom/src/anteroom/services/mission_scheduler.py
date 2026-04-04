"""Deterministic mission scheduler — polls sessions, launches items, polls executions (#1045).

An asyncio worker that evaluates eligible mission items, launches them via
adapters, polls active executions, and checks session completion. Follows
the WorkflowExecutorWorker pattern (backoff, start/stop, recovery).
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection
    from .mission_adapters import MissionAdapterRegistry

logger = logging.getLogger(__name__)

DEFAULT_POLL_INTERVAL = 5.0
MAX_BACKOFF_INTERVAL = 300.0
BACKOFF_MULTIPLIER = 2.0
MAX_CONSECUTIVE_FAILURES = 10

_TERMINAL_STATES = frozenset({"completed", "failed", "cancelled"})
_IN_FLIGHT_STATES = frozenset({"pending", "running"})

# V1 hardcoded concurrency group limit
_CONCURRENCY_GROUP_LIMIT = 1

# Map adapter terminal states to valid item statuses
# ("cancelled" is not a valid item status; map to "dropped")
_ADAPTER_TO_ITEM_STATUS: dict[str, str] = {
    "completed": "completed",
    "failed": "failed",
    "cancelled": "dropped",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MissionSchedulerWorker:
    """Background worker that drives mission item lifecycle."""

    def __init__(
        self,
        *,
        db: ThreadSafeConnection,
        adapter_registry: MissionAdapterRegistry,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        max_consecutive_failures: int = MAX_CONSECUTIVE_FAILURES,
    ) -> None:
        self._db = db
        self._adapter_registry = adapter_registry
        self._poll_interval = poll_interval
        self._max_consecutive_failures = max_consecutive_failures
        self._running = False
        self._task: asyncio.Task[None] | None = None
        self._consecutive_failures = 0
        self._current_interval = poll_interval

    @property
    def running(self) -> bool:
        return self._running

    # ------------------------------------------------------------------
    # Backoff
    # ------------------------------------------------------------------

    def _reset_backoff(self) -> None:
        self._consecutive_failures = 0
        self._current_interval = self._poll_interval

    def _apply_backoff(self) -> None:
        self._consecutive_failures += 1
        self._current_interval = min(
            self._poll_interval * (BACKOFF_MULTIPLIER**self._consecutive_failures),
            MAX_BACKOFF_INTERVAL,
        )
        logger.warning(
            "Mission scheduler: %d consecutive failures, next interval %.0fs",
            self._consecutive_failures,
            self._current_interval,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        self._task = asyncio.ensure_future(self.run_forever())

    def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()

    async def run_forever(self) -> None:
        self._running = True
        logger.info(
            "Mission scheduler started (poll=%.0fs)",
            self._poll_interval,
        )

        try:
            await self._recover_on_startup()
        except Exception:
            logger.exception("Mission scheduler startup recovery failed")

        while self._running:
            try:
                await self.run_once()
                if self._consecutive_failures > 0:
                    self._reset_backoff()
            except Exception:
                logger.exception("Mission scheduler poll cycle failed")
                self._apply_backoff()
                if self._consecutive_failures >= self._max_consecutive_failures:
                    logger.error(
                        "Mission scheduler disabled after %d consecutive failures",
                        self._consecutive_failures,
                    )
                    break
            await asyncio.sleep(self._current_interval)

    # ------------------------------------------------------------------
    # Core scheduling loop
    # ------------------------------------------------------------------

    async def run_once(self) -> None:
        from . import mission_storage as ms

        active_sessions = ms.list_sessions(self._db, status="active")
        for session in active_sessions:
            sid = session["id"]

            # Phase A — evaluate eligible items
            eligible = ms.list_eligible_items(self._db, sid)
            if eligible:
                lane_counts = ms.count_active_by_lane(self._db, sid)
                cg_counts = ms.count_active_by_concurrency_group(self._db, sid)
                lane_limits: dict[str, int] = session.get("lane_limits") or {}

                launchable = self._filter_by_limits(eligible, lane_limits, lane_counts, cg_counts)

                # Phase B — launch eligible items
                for item in launchable:
                    await self._launch_item(sid, item)

            # Phase C — poll active executions
            active_items = ms.list_items_by_session(self._db, sid, status="active")
            for item in active_items:
                await self._poll_item(sid, item)

            # Phase D — check session completion
            await self._check_session_completion(sid)

    # ------------------------------------------------------------------
    # Phase A helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _filter_by_limits(
        eligible: list[dict[str, Any]],
        lane_limits: dict[str, int],
        lane_counts: dict[str, int],
        cg_counts: dict[str, int],
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        # Track incremental counts as we accept items within this batch
        local_lane: dict[str, int] = dict(lane_counts)
        local_cg: dict[str, int] = dict(cg_counts)

        for item in eligible:
            lane = item.get("lane")
            if lane and lane in lane_limits:
                if local_lane.get(lane, 0) >= lane_limits[lane]:
                    continue

            cg = item.get("concurrency_group")
            if cg:
                if local_cg.get(cg, 0) >= _CONCURRENCY_GROUP_LIMIT:
                    continue

            result.append(item)
            if lane:
                local_lane[lane] = local_lane.get(lane, 0) + 1
            if cg:
                local_cg[cg] = local_cg.get(cg, 0) + 1

        return result

    # ------------------------------------------------------------------
    # Phase B — launch
    # ------------------------------------------------------------------

    async def _launch_item(self, session_id: str, item: dict[str, Any]) -> None:
        from . import mission_storage as ms

        item_id = item["id"]
        adapter_type = item.get("adapter_type", "noop")
        adapter = self._adapter_registry.get(adapter_type)

        if adapter is None:
            ms.update_item(self._db, item_id, status="blocked")
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="adapter_not_found",
                detail={"adapter_type": adapter_type},
            )
            return

        latest = ms.get_latest_execution(self._db, item_id)
        attempt_number = (latest["attempt_number"] + 1) if latest else 1
        execution = ms.create_execution(self._db, item_id=item_id, attempt_number=attempt_number)
        session = ms.get_session(self._db, session_id) or {}
        adapter_config: dict[str, Any] = item.get("adapter_config") or {}
        session_context: dict[str, Any] = {
            "session_id": session_id,
            "session": session,
            "spec_fqn": adapter_config.get("spec_fqn") or session.get("source_fqn"),
            "task_id": adapter_config.get("task_id"),
            "task_summary": item.get("summary"),
            "artifact_refs": session.get("referenced_artifacts"),
        }

        result = await adapter.create(item=item, context=session_context)

        if result.state in _TERMINAL_STATES:
            # Create-time terminal — item never becomes active
            item_status = _ADAPTER_TO_ITEM_STATUS.get(result.state, "failed")
            ms.update_execution(
                self._db,
                execution["id"],
                status=result.state,
                adapter_ref=result.adapter_ref,
                summary=result.summary,
                finished_at=_now(),
            )
            ms.update_item(self._db, item_id, status=item_status)
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type=f"item_{result.state}",
                detail={"summary": result.summary},
            )
        elif result.state in _IN_FLIGHT_STATES:
            ms.update_execution(
                self._db,
                execution["id"],
                status=result.state,
                adapter_ref=result.adapter_ref,
            )
            ms.update_item(self._db, item_id, status="active")
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="item_launched",
                detail={"adapter_ref": result.adapter_ref},
            )
        else:
            # Unrecognized state — treat as in-flight defensively
            logger.warning(
                "Adapter returned unrecognized state %r for item %s, treating as in-flight",
                result.state,
                item_id,
            )
            ms.update_execution(
                self._db,
                execution["id"],
                status="running",
                adapter_ref=result.adapter_ref,
            )
            ms.update_item(self._db, item_id, status="active")
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="item_launched",
                detail={"adapter_ref": result.adapter_ref, "original_state": result.state},
            )

    # ------------------------------------------------------------------
    # Phase C — poll
    # ------------------------------------------------------------------

    async def _poll_item(self, session_id: str, item: dict[str, Any]) -> None:
        from . import mission_storage as ms

        item_id = item["id"]
        execution = ms.get_latest_execution(self._db, item_id)
        if not execution or not execution.get("adapter_ref"):
            return

        adapter_type = item.get("adapter_type", "noop")
        adapter = self._adapter_registry.get(adapter_type)
        if not adapter:
            return

        result = await adapter.status(adapter_ref=execution["adapter_ref"])

        if result.state in _TERMINAL_STATES:
            ms.update_execution(
                self._db,
                execution["id"],
                status=result.state,
                summary=result.summary,
                finished_at=_now(),
            )

            hold = item.get("hold_requested")
            if hold:
                ms.update_item(self._db, item_id, status="blocked")
                ms.create_event(
                    self._db,
                    session_id=session_id,
                    item_id=item_id,
                    event_type="item_held_at_boundary",
                    detail={"terminal_state": result.state},
                )
            else:
                item_status = _ADAPTER_TO_ITEM_STATUS.get(result.state, "failed")
                ms.update_item(self._db, item_id, status=item_status)
                ms.create_event(
                    self._db,
                    session_id=session_id,
                    item_id=item_id,
                    event_type=f"item_{result.state}",
                    detail={"summary": result.summary},
                )
        elif result.state in _IN_FLIGHT_STATES:
            self._handle_stale_recovery(session_id, item, result)

    def _handle_stale_recovery(
        self,
        session_id: str,
        item: dict[str, Any],
        adapter_status: Any,
    ) -> None:
        """Check adapter summary/stop_reason for stale heartbeat signals and emit event."""
        from . import mission_storage as ms

        summary = getattr(adapter_status, "summary", None) or ""
        if "stale_heartbeat" not in summary:
            return

        ms.create_event(
            self._db,
            session_id=session_id,
            item_id=item["id"],
            event_type="item_stale_recovered",
            detail={"summary": summary},
        )

    # ------------------------------------------------------------------
    # Phase D — session completion
    # ------------------------------------------------------------------

    async def _check_session_completion(self, session_id: str) -> None:
        from . import mission_storage as ms

        items = ms.list_items_by_session(self._db, session_id)
        if not items:
            return

        non_dropped = [i for i in items if i["status"] != "dropped"]
        if not non_dropped:
            return

        # Before finalizing as failed, check external reality for workflow-
        # backed items whose GitHub issue may have been closed (#1306).
        failed_items = [i for i in non_dropped if i["status"] == "failed"]
        if failed_items:
            reconciled_any = await self._try_external_reconciliation(session_id, failed_items)
            if reconciled_any:
                # Re-read items after reconciliation changed statuses.
                items = ms.list_items_by_session(self._db, session_id)
                non_dropped = [i for i in items if i["status"] != "dropped"]

        if any(i["status"] == "failed" for i in non_dropped):
            ms.update_session(self._db, session_id, status="failed")
            ms.create_event(
                self._db,
                session_id=session_id,
                event_type="session_failed",
            )
            self._store_retrospective(session_id, is_draft=True)
            return

        if all(i["status"] == "completed" for i in non_dropped):
            ms.update_session(self._db, session_id, status="completed")
            ms.create_event(
                self._db,
                session_id=session_id,
                event_type="session_completed",
            )
            self._store_retrospective(session_id, is_draft=False)

    async def _try_external_reconciliation(self, session_id: str, failed_items: list[dict[str, Any]]) -> bool:
        """Check external GitHub reality for failed workflow items (#1306).

        Returns ``True`` if any item was reconciled.  Subprocess calls are
        offloaded to a thread to avoid blocking the event loop.
        """
        from . import mission_storage as ms
        from .external_checks import check_external_completion

        reconciled = False
        for item in failed_items:
            if item.get("adapter_type") != "workflow":
                continue

            issue_number = self._resolve_issue_number(item)
            if issue_number is None:
                continue

            try:
                is_complete, reason = await asyncio.to_thread(check_external_completion, issue_number)
            except Exception:
                logger.debug(
                    "External check failed for item %s (issue #%d)",
                    item["id"][:8],
                    issue_number,
                    exc_info=True,
                )
                continue

            if is_complete and reason:
                try:
                    ms.force_reconcile_item(self._db, item["id"], reason=reason)
                    logger.info(
                        "Auto-reconciled item %s: %s",
                        item["id"][:8],
                        reason,
                    )
                    reconciled = True
                except Exception:
                    logger.warning(
                        "Failed to auto-reconcile item %s",
                        item["id"][:8],
                        exc_info=True,
                    )

        return reconciled

    def _resolve_issue_number(self, item: dict[str, Any]) -> int | None:
        """Extract the issue number from the workflow run backing *item*.

        Returns ``None`` if the item has no workflow execution, the workflow
        run is not found, or the run has no ``issue_number`` in its inputs.
        """
        from . import mission_storage as ms
        from . import workflow_storage as ws

        latest = ms.get_latest_execution(self._db, item["id"])
        if latest is None or not latest.get("adapter_ref"):
            return None

        run = ws.get_workflow_run(self._db, latest["adapter_ref"])
        if run is None:
            return None

        inputs = run.get("inputs")
        if not inputs or not isinstance(inputs, dict):
            return None

        raw = inputs.get("issue_number")
        if raw is None:
            return None

        try:
            return int(raw)
        except (TypeError, ValueError):
            logger.debug("Non-integer issue_number in workflow run %s: %r", latest["adapter_ref"][:8], raw)
            return None

    def _store_retrospective(self, session_id: str, *, is_draft: bool) -> None:
        """Generate and store a retrospective, swallowing errors."""
        try:
            from .mission_summary import generate_and_store_retrospective

            generate_and_store_retrospective(self._db, session_id, is_draft=is_draft)
        except Exception:
            logger.warning(
                "Failed to generate retrospective for session %s",
                session_id[:8],
                exc_info=True,
            )

    # ------------------------------------------------------------------
    # Startup recovery
    # ------------------------------------------------------------------

    async def _recover_on_startup(self) -> None:
        from . import mission_storage as ms

        # Find items stuck in "active" and reconcile with adapter
        all_sessions = ms.list_sessions(self._db, status="active")
        for session in all_sessions:
            active_items = ms.list_items_by_session(self._db, session["id"], status="active")
            for item in active_items:
                await self._recover_item(session["id"], item)

    async def _recover_item(self, session_id: str, item: dict[str, Any]) -> None:
        from . import mission_storage as ms

        item_id = item["id"]
        execution = ms.get_latest_execution(self._db, item_id)
        if not execution or not execution.get("adapter_ref"):
            ms.update_item(self._db, item_id, status="failed")
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="recovery_failed",
                detail={"reason": "no_execution_or_adapter_ref"},
            )
            return

        adapter_type = item.get("adapter_type", "noop")
        adapter = self._adapter_registry.get(adapter_type)
        if not adapter:
            ms.update_item(self._db, item_id, status="failed")
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="recovery_failed",
                detail={"reason": "adapter_not_found", "adapter_type": adapter_type},
            )
            return

        try:
            result = await adapter.status(adapter_ref=execution["adapter_ref"])
        except Exception:
            logger.warning(
                "Recovery status check failed for item %s — treating as transient, will retry next cycle",
                item_id,
            )
            return

        if result.state in _TERMINAL_STATES:
            item_status = _ADAPTER_TO_ITEM_STATUS.get(result.state, "failed")
            ms.update_execution(
                self._db,
                execution["id"],
                status=result.state,
                finished_at=_now(),
            )
            ms.update_item(self._db, item_id, status=item_status)
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="recovery_reconciled",
                detail={"state": result.state},
            )
        elif result.state in _IN_FLIGHT_STATES:
            # Still running — leave as active, but check for stale heartbeat
            self._handle_stale_recovery(session_id, item, result)
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="recovery_still_active",
            )
        else:
            # Unknown state — mark failed
            ms.update_item(self._db, item_id, status="failed")
            ms.create_event(
                self._db,
                session_id=session_id,
                item_id=item_id,
                event_type="recovery_failed",
                detail={"reason": "unknown_state", "state": result.state},
            )
