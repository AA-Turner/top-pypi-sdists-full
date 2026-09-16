"""Workflow tests for scheduled trusted reconciliation cadence."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.inventory import CandidateInventoryProjection, InventoryTraversal
from agentic_devtools.cli.ci.reconciliation.models import TriStateValue
from agentic_devtools.cli.ci.reconciliation.reconciler import TrustedReconciler
from tests.workflows.ci.reconciliation.fixtures import WorkflowProvider


def test_scheduled_reconciliation_runs_without_events() -> None:
    provider = WorkflowProvider(
        [
            ([{"repo": "owner/repo", "number": 1, "target_branch": "main", "open": True, "head_sha": "sha-1"}], None),
        ]
    )
    result = TrustedReconciler(provider=provider).reconcile(
        initial_traversal=InventoryTraversal(cursor=None),
        initial_inventory=CandidateInventoryProjection(records={}),
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
        candidate_filter_result=TriStateValue.TRUE,
    )
    assert result.processed_records == 1
