"""Reconciliation-run metadata lifecycle management."""

from __future__ import annotations

from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.identifiers import deterministic_id
from agentic_devtools.cli.ci.reconciliation.models import ReconciliationRunRecord


class ReconciliationRunTracker:
    """Creates and transitions durable run metadata."""

    def start(self, *, mode: str, source_revision: str, started_at_utc_z: str) -> ReconciliationRunRecord:
        run_id = deterministic_id("run", mode, source_revision, started_at_utc_z, length=24)
        return ReconciliationRunRecord(
            run_id=run_id,
            mode=mode,
            source_revision=source_revision,
            started_at_utc_z=started_at_utc_z,
        )

    def checkpoint(self, run: ReconciliationRunRecord, *, checkpoint: str) -> ReconciliationRunRecord:
        return replace(run, persisted_checkpoint=checkpoint)

    def complete(
        self,
        run: ReconciliationRunRecord,
        *,
        completed_at_utc_z: str,
        outcome: str,
        processed_records: int,
        failed_records: int,
        traversal_baseline_advanced: bool,
    ) -> ReconciliationRunRecord:
        return replace(
            run,
            completed_at_utc_z=completed_at_utc_z,
            outcome=outcome,
            processed_records=processed_records,
            failed_records=failed_records,
            traversal_baseline_advanced=traversal_baseline_advanced if outcome == "success" else False,
        )
