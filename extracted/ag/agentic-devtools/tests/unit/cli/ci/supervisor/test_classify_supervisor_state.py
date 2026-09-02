"""Tests for deterministic AI PR Loop supervisor candidate classification."""

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.supervisor import (
    SupervisorEvidence,
    SupervisorState,
    classify_supervisor_state,
)

NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


def test_classify_supervisor_state_returns_healthy_for_green_pr() -> None:
    result = classify_supervisor_state(SupervisorEvidence(pr_number=7, head_sha="a" * 40), now=NOW)

    assert result.state is SupervisorState.HEALTHY
    assert result.reasons == ()


def test_classify_supervisor_state_returns_active_for_recent_task() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        agent_task_status="in_progress",
        agent_task_updated_at=NOW - timedelta(minutes=2),
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.ACTIVE
    assert result.reasons == ("active_agent_task",)


def test_classify_supervisor_state_detects_stale_active_task() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        agent_task_status="in_progress",
        agent_task_updated_at=NOW - timedelta(hours=2),
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.STUCK_CANDIDATE
    assert result.reasons == ("stale_active_agent_task",)


def test_classify_supervisor_state_returns_human_blocked_for_missing_opt_in() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        ci_status="passing",
        review_state="APPROVED",
        has_auto_merge_label=False,
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.BLOCKED_HUMAN
    assert result.reasons == ("missing_auto_merge_permission",)


def test_classify_supervisor_state_detects_stale_loop_and_unresolved_threads() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        loop_run_status="in_progress",
        loop_run_updated_at=NOW - timedelta(minutes=45),
        unresolved_threads=2,
        last_action="repair_dispatched",
        last_action_at=NOW - timedelta(minutes=30),
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.STUCK_CANDIDATE
    assert result.reasons == (
        "stale_loop_run",
        "unresolved_threads_after_repair",
    )


def test_classify_supervisor_state_marks_failed_loop_as_external_error() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        loop_run_status="completed",
        loop_run_conclusion="failure",
        loop_run_updated_at=NOW - timedelta(minutes=10),
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.EXTERNAL_ERROR
    assert result.reasons == ("failed_loop_run",)


def test_classify_supervisor_state_detects_review_waiting_without_evaluation() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        ci_status="passing",
        review_requested_at=NOW - timedelta(hours=2),
        has_review_on_head=False,
        unresolved_threads=0,
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.STUCK_CANDIDATE
    assert result.reasons == ("review_waiting_without_evaluation",)


def test_classify_supervisor_state_preserves_api_errors_as_unknown() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        api_errors=("reviews: permission denied",),
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.UNKNOWN
    assert result.reasons == ("required_evidence_unavailable",)


def test_classify_supervisor_state_rejects_naive_now() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        classify_supervisor_state(SupervisorEvidence(pr_number=7, head_sha="a" * 40), now=datetime(2026, 8, 31))


def test_classify_supervisor_state_returns_waiting_for_recent_review_request() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        review_requested_at=NOW - timedelta(minutes=5),
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.WAITING_EXPECTED
    assert result.reasons == ("waiting_for_review",)


def test_classify_supervisor_state_detects_completed_task_without_review() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        agent_task_status="completed",
        agent_task_updated_at=NOW - timedelta(hours=2),
    )

    result = classify_supervisor_state(evidence, now=NOW)

    assert result.state is SupervisorState.STUCK_CANDIDATE
    assert result.reasons == ("completed_task_without_review",)


def test_classify_supervisor_state_rejects_naive_evidence_timestamp() -> None:
    evidence = SupervisorEvidence(
        pr_number=7,
        head_sha="a" * 40,
        agent_task_status="completed",
        agent_task_updated_at=datetime(2026, 8, 31, 11, 0),
    )

    with pytest.raises(ValueError, match="timezone-aware"):
        classify_supervisor_state(evidence, now=NOW)
