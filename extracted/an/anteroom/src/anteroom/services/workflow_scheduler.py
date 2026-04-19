"""Workflow scheduler — evaluates due schedules and enqueues runs.

Stateless service called from the executor's poll cycle. Claims due
schedules atomically, resolves workflow definitions with path confinement,
and enqueues runs via the engine's ``enqueue_run()`` method.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection
    from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)


def _confine_path(workflow_ref: str, allowed_roots: list[Path] | None = None) -> Path:
    """Resolve and confine a filesystem path to allowed roots.

    Raises ValueError if the path escapes all allowed roots.
    """
    resolved = Path(workflow_ref).resolve()
    roots = allowed_roots or [
        Path.home() / ".anteroom",
        Path.cwd(),
    ]
    # Add built-in workflow dirs
    from .workflow_resolution import builtin_workflow_dirs

    roots.extend(builtin_workflow_dirs())

    for root in roots:
        try:
            if resolved.is_relative_to(root.resolve()):
                return resolved
        except (ValueError, OSError):
            continue
    raise ValueError(f"Workflow path outside allowed roots: {resolved}")


async def check_and_enqueue(
    db: ThreadSafeConnection,
    engine: WorkflowEngine,
    worker_id: str,
    *,
    min_schedule_interval: int = 60,
) -> list[str]:
    """Check for due schedules, claim them, and enqueue runs.

    Returns a list of enqueued run IDs.
    """
    from . import workflow_storage as ws
    from .cron import parse_cron
    from .workflow_engine import load_definition

    enqueued: list[str] = []

    # First: advance schedules whose tracked run has terminated (queue policy)
    pending_advances = ws.check_pending_advances(db)
    for sched in pending_advances:
        try:
            cron = parse_cron(sched["cron_expr"])
            ref_time = datetime.fromisoformat(sched["next_run_at"])
            if ref_time.tzinfo is None:
                ref_time = ref_time.replace(tzinfo=timezone.utc)
            next_at = cron.next_occurrence(ref_time)
            ws.advance_schedule(
                db,
                sched["id"],
                next_run_at=next_at.isoformat(),
                last_run_at=sched.get("last_run_at") or datetime.now(timezone.utc).isoformat(),
                last_run_id=sched.get("advance_after_run_id") or "",
            )
            logger.info("Advanced schedule %s after tracked run completed", sched["id"])
        except Exception:
            logger.exception("Failed to advance schedule %s", sched["id"])

    # Claim due schedules
    claimed = ws.claim_due_schedules(db, worker_id, limit=5)
    if not claimed:
        return enqueued

    for sched in claimed:
        schedule_id = sched["id"]
        ref_type = sched["ref_type"]
        workflow_ref = sched["workflow_ref"]

        try:
            # Resolve workflow definition with path confinement
            if ref_type == "path":
                path = _confine_path(workflow_ref)
            else:
                from .workflow_resolution import resolve_workflow_path

                path_result = resolve_workflow_path(workflow_ref, allow_filesystem=False, db=db)
                if not path_result:
                    raise ValueError(f"Workflow not found: {workflow_ref!r}")
                path = path_result

            definition = load_definition(path)

            run = await engine.enqueue_run(
                definition,
                target_kind=sched.get("target_kind") or "generic",
                target_ref=sched["target_ref"],
                inputs=sched.get("inputs"),
                space_id=sched.get("space_id"),
                trigger_source="schedule",
                trigger_meta={"schedule_id": schedule_id, "cron": sched["cron_expr"]},
            )
            run_id = run["id"]
            enqueued.append(run_id)
            now_iso = datetime.now(timezone.utc).isoformat()

            # Advance or defer based on missed_policy
            if sched.get("missed_policy") == "queue":
                ws.set_advance_after_run(db, schedule_id, run_id)
                logger.info("Schedule %s: enqueued run %s (queue policy, waiting)", schedule_id, run_id)
            else:
                cron = parse_cron(sched["cron_expr"])
                ref_time = datetime.fromisoformat(sched["next_run_at"])
                if ref_time.tzinfo is None:
                    ref_time = ref_time.replace(tzinfo=timezone.utc)
                next_at = cron.next_occurrence(ref_time)
                ws.advance_schedule(
                    db,
                    schedule_id,
                    next_run_at=next_at.isoformat(),
                    last_run_at=now_iso,
                    last_run_id=run_id,
                )
                logger.info("Schedule %s: enqueued run %s (skip policy, next at %s)", schedule_id, run_id, next_at)

        except Exception:
            logger.exception("Failed to process schedule %s", schedule_id)
            ws.release_schedule_claim(db, schedule_id)

    return enqueued
