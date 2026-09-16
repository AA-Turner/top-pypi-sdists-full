"""Workflow integration tests for candidate inventory reconciliation."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.inventory import CandidateInventoryProjection, InventoryTraversal
from agentic_devtools.cli.ci.reconciliation.models import ScopeClassification, TriStateValue
from agentic_devtools.cli.ci.reconciliation.reconciler import TrustedReconciler
from tests.workflows.ci.reconciliation.fixtures import WorkflowProvider


def test_inventory_workflow_discovers_later_page_records() -> None:
    provider = WorkflowProvider(
        [
            ([{"repo": "owner/repo", "number": 1, "target_branch": "main", "open": True, "head_sha": "sha-1"}], "next"),
            ([{"repo": "owner/repo", "number": 2, "target_branch": "main", "open": True, "head_sha": "sha-2"}], None),
        ]
    )
    reconciler = TrustedReconciler(provider=provider)
    state = CandidateInventoryProjection(records={})
    traversal = InventoryTraversal(cursor=None)
    first = reconciler.reconcile(
        initial_traversal=traversal,
        initial_inventory=state,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10,
        candidate_filter_result=TriStateValue.TRUE,
    )
    second = reconciler.reconcile(
        initial_traversal=first.traversal,
        initial_inventory=first.inventory,
        observed_at_utc_z="2026-09-15T12:20:00Z",
        observed_monotonic_seconds=1200,
        candidate_filter_result=TriStateValue.TRUE,
    )
    assert set(second.inventory.records) == {"owner/repo#1", "owner/repo#2"}
    assert second.inventory.records["owner/repo#2"].scope_classification == ScopeClassification.ACTIVE
