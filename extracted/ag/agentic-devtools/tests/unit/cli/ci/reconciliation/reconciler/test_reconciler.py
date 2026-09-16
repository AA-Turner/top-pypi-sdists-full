"""Tests for trusted scheduled reconciler orchestration."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from agentic_devtools.cli.ci.reconciliation.inventory import CandidateInventoryProjection, InventoryTraversal
from agentic_devtools.cli.ci.reconciliation.models import ScopeClassification, TriStateValue
from agentic_devtools.cli.ci.reconciliation.reconciler import TrustedObservationProvider, TrustedReconciler


class _Provider(TrustedObservationProvider):
    def __init__(self, pages: list[tuple[Sequence[Mapping[str, object]], str | None]]) -> None:
        self._pages = pages
        self._index = 0

    def list_pull_requests(self, *, cursor: str | None) -> tuple[Sequence[Mapping[str, object]], str | None]:
        del cursor
        page = self._pages[self._index]
        self._index += 1
        return page


def test_reconciler_updates_inventory_and_traversal() -> None:
    provider = _Provider(
        [
            ([{"repo": "owner/repo", "number": 1, "target_branch": "main", "open": True, "head_sha": "a"}], "c2"),
        ]
    )
    reconciler = TrustedReconciler(provider=provider)
    result = reconciler.reconcile(
        initial_traversal=InventoryTraversal(cursor="c1"),
        initial_inventory=CandidateInventoryProjection(records={}),
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
        candidate_filter_result=TriStateValue.TRUE,
    )
    assert result.traversal.cursor == "c2"
    assert result.processed_records == 1
    assert result.inventory.records["owner/repo#1"].scope_classification == ScopeClassification.ACTIVE
    assert result.ledgers["owner/repo#1"].observations[0].outcome.value == "trusted_observation"


def test_reconciler_marks_non_active_scope_when_filter_false() -> None:
    provider = _Provider(
        [
            ([{"repo": "owner/repo", "number": 2, "target_branch": "main", "open": True, "head_sha": "b"}], None),
        ]
    )
    reconciler = TrustedReconciler(provider=provider)
    result = reconciler.reconcile(
        initial_traversal=InventoryTraversal(cursor=None),
        initial_inventory=CandidateInventoryProjection(records={}),
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
        candidate_filter_result=TriStateValue.FALSE,
    )
    assert (
        result.inventory.records["owner/repo#2"].scope_classification == ScopeClassification.NON_ACTIONABLE_INELIGIBLE
    )


def test_reconciler_skips_non_integer_pr_numbers() -> None:
    provider = _Provider(
        [
            ([{"repo": "owner/repo", "number": "not-int", "target_branch": "main", "open": True}], None),
        ]
    )
    reconciler = TrustedReconciler(provider=provider)
    result = reconciler.reconcile(
        initial_traversal=InventoryTraversal(cursor=None),
        initial_inventory=CandidateInventoryProjection(records={}),
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
        candidate_filter_result=TriStateValue.TRUE,
    )
    assert result.inventory.records == {}


def test_reconciler_does_not_promote_partial_provider_evidence() -> None:
    provider = _Provider(
        [
            (
                [
                    {
                        "repo": "owner/repo",
                        "number": 3,
                        "target_branch": "main",
                        "open": True,
                        "head_sha": "c",
                        "partial_evidence": True,
                    }
                ],
                None,
            ),
        ]
    )

    result = TrustedReconciler(provider=provider).reconcile(
        initial_traversal=InventoryTraversal(),
        initial_inventory=CandidateInventoryProjection(records={}),
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
        candidate_filter_result=TriStateValue.TRUE,
    )

    assert result.inventory.records["owner/repo#3"].scope_classification.value == "pending_unverified"
    assert result.ledgers["owner/repo#3"].decisions == ()
    assert result.ledgers["owner/repo#3"].action_eligibility.value == "unknown"
