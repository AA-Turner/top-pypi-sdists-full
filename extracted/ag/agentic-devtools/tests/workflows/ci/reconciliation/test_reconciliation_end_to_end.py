"""End-to-end reconciliation tests for bounded traversal and idempotency."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.inventory import CandidateInventoryProjection, InventoryTraversal
from agentic_devtools.cli.ci.reconciliation.models import TriStateValue
from agentic_devtools.cli.ci.reconciliation.reconciler import TrustedReconciler
from tests.workflows.ci.reconciliation.fixtures import WorkflowProvider


def test_repeated_reconciliation_is_idempotent_for_same_page() -> None:
    provider = WorkflowProvider(
        [
            ([{"repo": "owner/repo", "number": 4, "target_branch": "main", "open": True, "head_sha": "sha-4"}], None),
            ([{"repo": "owner/repo", "number": 4, "target_branch": "main", "open": True, "head_sha": "sha-4"}], None),
        ]
    )
    reconciler = TrustedReconciler(provider=provider)
    first = reconciler.reconcile(
        initial_traversal=InventoryTraversal(cursor=None),
        initial_inventory=CandidateInventoryProjection(records={}),
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10,
        candidate_filter_result=TriStateValue.TRUE,
    )
    second = reconciler.reconcile(
        initial_traversal=InventoryTraversal(cursor=None),
        initial_inventory=first.inventory,
        observed_at_utc_z="2026-09-15T12:20:00Z",
        observed_monotonic_seconds=20,
        candidate_filter_result=TriStateValue.TRUE,
    )
    assert len(second.inventory.records) == 1
