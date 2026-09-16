"""Direct record fixtures for isolated foundation symbol tests (no controller setup)."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.reconciliation.models import (
    AttemptKind,
    AttemptStatus,
    Evidence,
    FindingRecord,
    MigrationRecord,
    PRControlEnvelope,
    QueueState,
    RepairAttempt,
    RepairRound,
    SemanticObligation,
    WorkItem,
    WorkItemStatus,
)

NOW = datetime(2026, 9, 14, 12, tzinfo=UTC)


@pytest.fixture
def foundation():
    """Build typed records directly, independently of the transitions being tested."""

    def build(statuses=(AttemptStatus.AUTHORIZED,), phase="prepublication", round_count=1):
        state = QueueState("owner/repo", 10, {}, [], [], migration_status="active")

        def proof(kind="observation", subject="42", **changes):
            values = dict(
                evidence_id="",
                repo=state.repo,
                pr_number=42,
                head_sha="a" * 40,
                base_sha="b" * 40,
                policy_version="policy",
                kind=kind,
                subject=subject,
                before="none",
                after="actionable",
                source_digest="c" * 64,
                source_revision="source",
                issuer="verifier",
                producer="worker",
                observed_at=NOW,
                valid_until=NOW + timedelta(minutes=5),
                complete=True,
                inventory=("comment",),
            )
            values.update(changes)
            result = Evidence(**values)
            return replace(result, evidence_id=result.digest())

        def add(kind="observation", subject="42", **changes):
            result = proof(kind, subject, **changes)
            state.evidence[result.evidence_id] = result
            return result.evidence_id

        migration = add("migration", "inventory", pr_number=0, before="legacy", after="history")
        state.migration = MigrationRecord(0, 1, "legacy", "history", migration)
        observation = add()
        history = add("history", after="empty")
        finding = add("finding", "comment", related_id="problem")
        state.findings["finding"] = FindingRecord("finding", 42, "problem", "comment", finding, ("a" * 40,))
        state.obligations["problem"] = SemanticObligation(
            "problem",
            42,
            "canonical",
            ("finding",),
            tuple(f"attempt-{i}" for i in range(len(statuses))),
            status="in_progress" if statuses else "pending",
        )
        state.pr_envelopes[42] = PRControlEnvelope(
            42,
            state.repo,
            "a" * 40,
            "b" * 40,
            "policy",
            observation,
            history,
            rounds_used=1,
            round_ids=("batch",),
            obligation_ids=("problem",),
            active_batch_id="batch",
        )
        state.rounds["batch"] = RepairRound("batch", 42, 1, "problem", observation, "bootstrap", None)
        previous = None
        for index, status in enumerate(statuses):
            identity = f"attempt-{index}"
            kind = tuple(AttemptKind)[index]
            authorization = previous
            if kind == AttemptKind.REMEDIATION:
                remediation = add("remediation", "problem", before="broken", after="fixed")
                state.obligations["problem"] = replace(state.obligations["problem"], remediation_id=remediation)
                authorization = add("verification", "problem", after="repair_required", related_id=remediation)
            accepted = status in {AttemptStatus.ACCEPTED, AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}
            acceptance = (
                add(
                    "acceptance",
                    identity,
                    before=f"provider:{identity}",
                    after="gpt-6-astra" if kind == AttemptKind.ASTRA else "gpt-5.6-luna",
                    related_id=observation,
                )
                if accepted
                else None
            )
            outcome = None
            if status in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}:
                outcome = add(
                    "failure" if status == AttemptStatus.FAILED else "success",
                    identity,
                    before="terminal",
                    after="unresolved" if status == AttemptStatus.FAILED else "satisfied",
                    related_id=acceptance,
                )
            state.attempts[identity] = RepairAttempt(
                identity,
                42,
                "problem",
                "batch",
                kind,
                index + 1,
                observation,
                authorization,
                status,
                acceptance,
                outcome,
            )
            previous = outcome
        if phase in {"published", "reviewed"}:
            publication = add("publication", "batch", related_id=observation, after="a" * 40)
            review = add("review", "batch", related_id=publication) if phase == "reviewed" else None
            state.rounds["batch"] = replace(
                state.rounds["batch"],
                phase=phase,
                publication_id=publication,
                review_id=review,
            )
        else:
            state.rounds["batch"] = replace(state.rounds["batch"], phase=phase)
        for ordinal in range(2, round_count + 1):
            previous_batch = state.pr_envelopes[42].active_batch_id
            state.rounds[previous_batch] = replace(state.rounds[previous_batch], phase="invalidated")
            batch_id = f"batch-{ordinal}"
            state.rounds[batch_id] = RepairRound(
                batch_id,
                42,
                ordinal,
                "problem",
                observation,
                "replan",
                previous_batch,
            )
            state.pr_envelopes[42] = replace(
                state.pr_envelopes[42],
                rounds_used=ordinal,
                round_ids=(*state.pr_envelopes[42].round_ids, batch_id),
                active_batch_id=batch_id,
            )
        return SimpleNamespace(state=state, proof=proof, add=add, now=NOW)

    return build


@pytest.fixture
def github_paginated_pull_request_pages() -> list[tuple[list[dict[str, object]], str | None]]:
    """Provide deterministic paginated pull-request inventory payloads."""
    return [
        (
            [
                {"repo": "owner/repo", "number": 1, "target_branch": "main", "open": True, "head_sha": "sha-1"},
                {"repo": "owner/repo", "number": 2, "target_branch": "main", "open": True, "head_sha": "sha-2"},
            ],
            "cursor-2",
        ),
        ([{"repo": "owner/repo", "number": 3, "target_branch": "release", "open": False, "head_sha": "sha-3"}], None),
    ]


@pytest.fixture(autouse=True)
def clear_repository_context(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep command tests independent from the runner's repository environment."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)


@pytest.fixture
def provider_failure_exception() -> RuntimeError:
    """Provide a representative transient provider failure."""
    return RuntimeError("503 service unavailable")


@pytest.fixture
def deterministic_trusted_clock():
    """Provide deterministic trusted control-plane clock."""
    from agentic_devtools.cli.ci.reconciliation.clock import DeterministicTrustedControlPlaneClock

    return DeterministicTrustedControlPlaneClock(utc_now=datetime(2026, 9, 15, 12, tzinfo=UTC), monotonic_now=100.0)


@pytest.fixture
def persisted_queue_state() -> QueueState:
    """Provide a persisted queue-state sample with one in-scope candidate."""
    now = datetime(2026, 9, 15, 12, tzinfo=UTC)
    item = WorkItem(
        1,
        "owner/repo",
        "sha-1",
        "eligible",
        now,
        WorkItemStatus.QUEUED,
        last_observed_at=now,
        observation_watermark="sha-1",
    )
    return QueueState("owner/repo", 7, {1: item}, [], [], last_updated_at=now)


@pytest.fixture
def overlapping_worker_identities() -> tuple[str, str]:
    """Provide deterministic overlapping-worker identities."""
    return ("worker-a", "worker-b")
