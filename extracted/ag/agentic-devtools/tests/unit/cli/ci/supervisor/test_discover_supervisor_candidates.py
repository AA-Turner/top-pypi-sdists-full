"""Tests for deterministic supervisor candidate discovery."""

from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.supervisor import (
    SupervisorConfig,
    SupervisorEvidence,
    SupervisorState,
    discover_supervisor_candidates,
)

NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


def _stale(pr_number: int) -> SupervisorEvidence:
    return SupervisorEvidence(
        pr_number=pr_number,
        head_sha=str(pr_number) * 40,
        loop_run_status="in_progress",
        loop_run_updated_at=NOW - timedelta(hours=2),
    )


def test_discover_supervisor_candidates_skips_non_actionable_prs_and_sorts() -> None:
    evidence = [
        _stale(9),
        SupervisorEvidence(pr_number=3, head_sha="c" * 40, ignored=True),
        SupervisorEvidence(pr_number=4, head_sha="d" * 40, is_fork=True),
        SupervisorEvidence(pr_number=5, head_sha="e" * 40),
    ]

    candidates = discover_supervisor_candidates(evidence, now=NOW)

    assert [candidate.evidence.pr_number for candidate in candidates] == [9]
    assert candidates[0].classification.state is SupervisorState.STUCK_CANDIDATE


def test_discover_supervisor_candidates_includes_unknown_and_honors_limit() -> None:
    evidence = [
        _stale(9),
        SupervisorEvidence(pr_number=7, head_sha="a" * 40, api_errors=("reviews unavailable",)),
        _stale(8),
    ]

    candidates = discover_supervisor_candidates(
        evidence,
        now=NOW,
        config=SupervisorConfig(loop_stale_seconds=60),
        max_candidates=2,
    )

    assert [candidate.evidence.pr_number for candidate in candidates] == [7, 8]
    assert candidates[0].classification.state is SupervisorState.UNKNOWN


def test_discover_supervisor_candidates_rejects_invalid_limit() -> None:
    try:
        discover_supervisor_candidates([], now=NOW, max_candidates=0)
    except ValueError as exc:
        assert str(exc) == "max_candidates must be a positive integer"
    else:
        raise AssertionError("expected invalid max_candidates to raise")
