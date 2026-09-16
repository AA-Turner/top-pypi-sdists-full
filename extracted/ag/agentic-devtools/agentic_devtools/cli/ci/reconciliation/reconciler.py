"""Trusted scheduled reconciliation orchestration service."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from agentic_devtools.cli.ci.reconciliation.inventory import (
    CandidateInventoryProjection,
    InventoryTraversal,
    classify_scope,
    schedule_retry_due,
)
from agentic_devtools.cli.ci.reconciliation.ledger import WorkLedgerService
from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    DecisionStatus,
    LifecycleState,
    PullRequestWorkLedger,
    ScopeClassification,
    TriStateValue,
)
from agentic_devtools.cli.ci.reconciliation.provider_outcomes import classify_reconciliation_outcome


class TrustedObservationProvider:
    """Protocol-like base for provider implementations used by the reconciler."""

    def list_pull_requests(self, *, cursor: str | None) -> tuple[Sequence[Mapping[str, object]], str | None]:
        raise NotImplementedError  # pragma: no cover


@dataclass(frozen=True)
class ReconcilerResult:
    """Result summary for one scheduled reconciliation run."""

    traversal: InventoryTraversal
    inventory: CandidateInventoryProjection
    processed_records: int
    ledgers: dict[str, PullRequestWorkLedger] = field(default_factory=dict)


class TrustedReconciler:
    """Runs scheduled trusted observation and durable projection updates."""

    def __init__(
        self, *, provider: TrustedObservationProvider, ledger_service: WorkLedgerService | None = None
    ) -> None:
        self._provider = provider
        self._ledger_service = ledger_service or WorkLedgerService()

    def reconcile(
        self,
        *,
        initial_traversal: InventoryTraversal,
        initial_inventory: CandidateInventoryProjection,
        observed_at_utc_z: str,
        observed_monotonic_seconds: float,
        candidate_filter_result: TriStateValue,
    ) -> ReconcilerResult:
        """Run one bounded traversal step and update inventory/ledger projections."""
        pull_requests, next_cursor = self._provider.list_pull_requests(cursor=initial_traversal.cursor)
        traversal = initial_traversal.advance(next_cursor=next_cursor)
        inventory = initial_inventory
        ledgers: dict[str, PullRequestWorkLedger] = {}
        processed_records = 0
        for pr in pull_requests:
            raw_repo = pr.get("repo")
            raw_pr_number = pr.get("number", 0)
            target_branch = pr.get("target_branch")
            open_state = pr.get("open")
            head_sha = pr.get("head_sha")
            partial_evidence = pr.get("partial_evidence", False)
            if (
                not isinstance(raw_repo, str)
                or not raw_repo.strip()
                or not isinstance(raw_pr_number, int)
                or isinstance(raw_pr_number, bool)
                or not isinstance(target_branch, str)
                or not target_branch.strip()
                or not isinstance(open_state, bool)
                or not isinstance(head_sha, str)
                or not head_sha.strip()
                or not isinstance(partial_evidence, bool)
            ):
                continue
            repo = raw_repo.strip()
            pr_number = raw_pr_number
            lifecycle = LifecycleState.NON_TERMINAL if open_state else LifecycleState.TERMINAL
            outcome = classify_reconciliation_outcome(
                record_found=True,
                partial_evidence=partial_evidence,
                terminal_state=lifecycle == LifecycleState.TERMINAL and not partial_evidence,
            )
            scope = classify_scope(
                lifecycle_state=lifecycle,
                eligibility_state=candidate_filter_result,
                observation_outcome=outcome,
            )
            record = CandidateInventoryRecord(
                record_id=f"{repo}#{pr_number}",
                repo=repo,
                pr_number=pr_number,
                target_branch=target_branch,
                lifecycle_state=lifecycle,
                scope_classification=scope,
                eligibility_state=candidate_filter_result,
                observation_outcome=outcome,
                observed_at_utc_z=observed_at_utc_z,
                observed_monotonic_seconds=observed_monotonic_seconds,
                next_due_at_utc_z=schedule_retry_due(observed_at_utc_z=observed_at_utc_z),
            )
            inventory = inventory.upsert(record)
            processed_records += 1
            ledger = self._ledger_service.ensure_ledger(record)
            ledger = self._ledger_service.record_observation(
                ledger=ledger,
                record=record,
                change_id=head_sha,
                outcome=outcome,
            )
            if scope in {
                ScopeClassification.NON_ACTIONABLE_INELIGIBLE,
                ScopeClassification.RETAINED_AUDIT_ONLY,
            }:
                ledger = self._ledger_service.record_decision(
                    ledger=ledger,
                    record=record,
                    status=DecisionStatus.BLOCKED,
                    reason="non-active scope",
                    evidence_digest="scope",
                )
            ledgers[record.record_id] = ledger
        return ReconcilerResult(
            traversal=traversal,
            inventory=inventory,
            processed_records=processed_records,
            ledgers=ledgers,
        )
