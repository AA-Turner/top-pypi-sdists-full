"""Tests for REST-backed Agent Tasks lifecycle classification."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import cast
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskLifecycle, AgentTaskSessionLifecycle
from agentic_devtools.cli.ci.pipeline.session_detector import (
    _classify_writer_run,
    _github_lifecycle_provider,
    classify_agent_task_inventory,
    is_copilot_session_active_via_agent_task,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory, WorkflowRun
from agentic_devtools.cli.ci.retry import ProviderRateLimitError
from tests.unit.cli.ci.pipeline.session_detector._agent_task_test_support import (
    FakeLifecycleProvider,
    _classify,
    _task,
)


def test_active_task_within_75_minutes_blocks() -> None:
    """A known young task blocks progress."""
    provider = FakeLifecycleProvider(AgentTaskInventory((_task(),)))
    assert _classify(provider) is True


def test_younger_correlated_writer_run_blocks_an_expired_task() -> None:
    """A known young Actions writer run remains a separate blocker."""
    now = datetime.now(UTC)
    run = WorkflowRun(
        id=700,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at=(now - timedelta(minutes=5)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="in_progress",
        run_started_at=(now - timedelta(minutes=5)).isoformat(),
    )
    provider = FakeLifecycleProvider(
        AgentTaskInventory((_task(created_at=now - timedelta(minutes=90)),)),
        runs=[run],
    )

    assert _classify(provider) is True
    assert provider.cancelled_runs == []


def test_younger_writer_run_blocks_when_task_inventory_is_empty() -> None:
    """An empty task inventory cannot hide a current Actions writer."""
    now = datetime.now(UTC)
    run = WorkflowRun(
        id=709,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at=(now - timedelta(minutes=5)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="in_progress",
        run_started_at=(now - timedelta(minutes=5)).isoformat(),
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()), runs=[run])

    assert _classify(provider) is True
    assert provider.cancelled_runs == []


def test_expired_writer_run_is_ignored_without_mutating_during_evaluation() -> None:
    """Classification never cancels even an expired run."""
    now = datetime.now(UTC)
    run = WorkflowRun(
        id=701,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at=(now - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="in_progress",
        run_started_at=(now - timedelta(minutes=90)).isoformat(),
    )
    provider = FakeLifecycleProvider(
        AgentTaskInventory((), complete=True),
        runs=[run],
        cancel_error=RuntimeError("cancel endpoint unavailable"),
    )

    assert _classify(provider) is False
    assert provider.cancelled_runs == []
    assert provider.invalidated_prs == []


def test_actions_run_at_exact_75_minutes_remains_blocking() -> None:
    """An Actions run does not expire until its own start is older than 75 minutes."""
    now = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)
    run = WorkflowRun(
        id=702,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at=(now - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="in_progress",
        run_started_at=(now - timedelta(minutes=75)).isoformat(),
    )

    result = _classify_writer_run(run, now=now)

    assert result is not None
    assert result.blocking is True
    assert result.expired is False


def test_task_within_75_minute_boundary_still_blocks() -> None:
    """The strict expiry boundary does not expire a recent task."""
    now = datetime.now(UTC)
    provider = FakeLifecycleProvider(AgentTaskInventory((_task(created_at=now - timedelta(minutes=74)),)))
    assert _classify(provider) is True


def test_task_over_75_minutes_old_no_longer_blocks() -> None:
    """A task whose only active lifecycle is over 75 minutes old is ignored."""
    now = datetime.now(UTC)
    provider = FakeLifecycleProvider(AgentTaskInventory((_task(created_at=now - timedelta(minutes=76)),)))
    assert _classify(provider) is False


def test_new_session_keeps_terminal_parent_task_blocking() -> None:
    """A newer session is not hidden by the terminal parent task state."""
    now = datetime.now(UTC)
    task = _task(
        state="failed",
        created_at=now - timedelta(minutes=90),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-old",
                state="failed",
                started_at=(now - timedelta(minutes=85)).isoformat(),
            ),
            AgentTaskSessionLifecycle(
                session_id="session-new",
                state="running",
                started_at=(now - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )
    assert _classify(FakeLifecycleProvider(AgentTaskInventory((task,)))) is True


def test_incomplete_detail_does_not_reblock_demonstrably_expired_task(caplog) -> None:
    """A failed detail read is audited but does not extend an identified expired task."""
    now = datetime.now(UTC)
    task = _task(state="running", created_at=now - timedelta(minutes=90))
    inventory = AgentTaskInventory((task,), complete=False, incomplete_reasons=("task-detail:task-1",))
    with caplog.at_level("WARNING"):
        assert _classify(FakeLifecycleProvider(inventory)) is False
    assert "task-detail:task-1" in caplog.text


def test_truncated_inventory_remains_unknown_when_no_active_task_is_known() -> None:
    """A page-limit gap cannot be mistaken for a clean inventory."""
    inventory = AgentTaskInventory((), complete=False, incomplete_reasons=("page-limit",))
    assert _classify(FakeLifecycleProvider(inventory)) is None


def test_known_younger_task_still_blocks_with_incomplete_inventory() -> None:
    """Incomplete corroboration does not weaken a known young task."""
    now = datetime.now(UTC)
    task = _task(state="running", created_at=now - timedelta(minutes=5))
    inventory = AgentTaskInventory((task,), complete=False, incomplete_reasons=("task-detail:other",))
    assert _classify(FakeLifecycleProvider(inventory)) is True


@pytest.mark.parametrize("reason", ["page-limit", "task-detail:task-1"])
def test_future_task_clock_keeps_incomplete_aggregate_unknown(reason: str) -> None:
    """An incomplete inventory cannot use a future task clock to authorize activity."""
    future = (datetime.now(UTC) + timedelta(days=1)).isoformat()
    inventory = AgentTaskInventory(
        (replace(_task(created_at=datetime.now(UTC) - timedelta(minutes=90)), idle_at=future),),
        complete=False,
        incomplete_reasons=(reason,),
    )

    assert _classify(FakeLifecycleProvider(inventory)) is None


@pytest.mark.parametrize(
    ("reason", "fallback_source"),
    [
        ("page-limit", "created_at"),
        ("task-detail:task-1", "created_at"),
        ("page-limit", "first_observed_at"),
        ("task-detail:task-1", "first_observed_at"),
    ],
)
def test_future_session_clock_does_not_promote_aggregate_from_bookkeeping(reason: str, fallback_source: str) -> None:
    now = datetime.now(UTC)
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at=now.isoformat() if fallback_source == "created_at" else "",
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="in_progress",
                idle_at="9999-12-31T23:59:59Z",
            ),
        ),
    )
    inventory = AgentTaskInventory((task,), complete=False, incomplete_reasons=(reason,))
    provider = FakeLifecycleProvider(
        inventory,
        first_seen=now.isoformat() if fallback_source == "first_observed_at" else None,
    )

    assert _classify(provider) is None


def test_future_incomplete_parent_does_not_hide_verified_active_session() -> None:
    """A future parent clock remains unknown without suppressing typed session activity."""
    now = datetime.now(UTC)
    task = replace(
        _task(created_at=now - timedelta(minutes=90)),
        idle_at=(now + timedelta(days=1)).isoformat(),
        sessions=(
            AgentTaskSessionLifecycle(
                session_id="session-1",
                state="running",
                started_at=(now - timedelta(minutes=5)).isoformat(),
            ),
        ),
    )
    inventory = AgentTaskInventory((task,), complete=False, incomplete_reasons=("page-limit",))

    assert _classify(FakeLifecycleProvider(inventory)) is True


def test_malformed_active_task_remains_unknown_with_diagnostics(caplog) -> None:
    inventory = AgentTaskInventory(
        (_task(),),
        complete=False,
        incomplete_reasons=("malformed-session:task-1",),
    )
    provider = FakeLifecycleProvider(inventory)

    with caplog.at_level("WARNING"):
        assert _classify(provider) is None

    assert "malformed-session:task-1" in caplog.text


def test_missing_provider_timestamps_use_durable_first_observation() -> None:
    """Reads the existing first-observed clock when task and session times are absent."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="idle",
        created_at="",
    )
    now = datetime.now(UTC)
    provider = FakeLifecycleProvider(
        AgentTaskInventory((task,)),
        first_seen=(now - timedelta(minutes=80)).isoformat(),
    )

    assert _classify(provider) is False
    assert provider.first_observed_calls == [("", "copilot/pr-42")]


def test_missing_session_clock_uses_session_scoped_first_observation() -> None:
    """A session without provider time gets its own durable observation clock."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="failed",
        created_at="",
        sessions=(AgentTaskSessionLifecycle(session_id="session-1", state="idle"),),
    )
    now = datetime.now(UTC)
    provider = FakeLifecycleProvider(
        AgentTaskInventory((task,)),
        first_seen=(now - timedelta(minutes=80)).isoformat(),
    )

    assert _classify(provider) is False
    assert provider.first_observed_calls == [
        ("", "copilot/pr-42"),
        ("session-1", "copilot/pr-42"),
    ]


def test_recent_first_observed_session_blocks_with_terminal_parent_task() -> None:
    """A recent unclocked active session remains blocking when its task is terminal."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="completed",
        created_at="",
        sessions=(AgentTaskSessionLifecycle(session_id="session-1", state="running"),),
    )
    now = datetime.now(UTC)
    provider = FakeLifecycleProvider(
        AgentTaskInventory((task,)),
        first_seen=(now - timedelta(minutes=5)).isoformat(),
    )

    assert _classify(provider) is True
    assert provider.first_observed_calls == [
        ("", "copilot/pr-42"),
        ("session-1", "copilot/pr-42"),
    ]


def test_missing_session_observation_keeps_clock_unknown() -> None:
    """A missing persisted session marker cannot be mistaken for a fresh lifecycle."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="failed",
        created_at="",
        sessions=(AgentTaskSessionLifecycle(session_id="session-1", state="running"),),
    )
    provider = FakeLifecycleProvider(AgentTaskInventory((task,)))

    assert _classify(provider) is None
    assert provider.first_observed_calls == [
        ("", "copilot/pr-42"),
        ("session-1", "copilot/pr-42"),
    ]


def test_writer_run_lookup_failure_remains_unknown_even_with_expired_task() -> None:
    """An expired task does not prove that no younger writer run exists."""
    provider = FakeLifecycleProvider(AgentTaskInventory((_task(created_at=datetime.now(UTC) - timedelta(minutes=90)),)))
    with patch.object(provider, "list_correlated_cloud_writer_runs", side_effect=RuntimeError("Actions unavailable")):
        assert _classify(provider) is None


def test_rate_limit_is_not_silently_converted_to_clean_inventory() -> None:
    """Propagates provider rate-limit errors for the established cooldown handling."""
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with (
        patch.object(
            provider,
            "list_pr_agent_task_lifecycles",
            side_effect=ProviderRateLimitError(
                retry_after_seconds=30,
                reset_timestamp=None,
                remaining=0,
                provider="github",
                credential_identity="workflow",
                source="agent_tasks",
            ),
        ),
        pytest.raises(ProviderRateLimitError),
    ):
        _classify(provider)


def test_missing_lifecycle_clock_remains_unknown() -> None:
    """An active task without any usable clock is not treated as expired."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at="",
    )

    assessment = classify_agent_task_inventory(
        AgentTaskInventory((task,)),
        now=datetime.now(UTC),
    )

    assert assessment.blocking is None
    assert assessment.reason == "missing-clock"


def test_expired_parent_with_unusable_newer_session_is_unknown() -> None:
    """An unclocked lifecycle prevents declaring a separately expired task fully clear."""
    now = datetime.now(UTC)
    expired_task = _task(state="in_progress", created_at=now - timedelta(minutes=90))
    unknown_task = AgentTaskLifecycle(
        task_id="task-2",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at="",
    )

    assessment = classify_agent_task_inventory(
        AgentTaskInventory((expired_task, unknown_task)),
        now=now,
    )

    assert assessment.blocking is None
    assert assessment.expired is True
    assert assessment.reason == "missing-clock"


def test_default_provider_is_not_cached_between_evaluations() -> None:
    """Each independent evaluation gets fresh provider evidence."""
    from agentic_devtools.cli.ci import github_provider

    with patch.object(github_provider, "GitHubActionsProvider") as provider_factory:
        _github_lifecycle_provider("owner/repo")
        _github_lifecycle_provider("owner/repo")

    assert provider_factory.call_count == 2


def test_lifecycle_inventory_failure_is_unknown() -> None:
    """A provider inventory failure is reported as unknown, not clear."""
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with patch.object(provider, "list_pr_agent_task_lifecycles", side_effect=RuntimeError("HTTP 404")):
        assert _classify(provider) is None


def test_missing_first_observed_provider_keeps_unclocked_task_unknown() -> None:
    """A provider without durable-clock support cannot age an unclocked task."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at="",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory((task,)))
    with patch.object(provider, "get_agent_task_first_observed_at", None):
        assert _classify(provider) is None


def test_first_observed_read_failure_keeps_task_unknown() -> None:
    """A failed durable-clock read does not silently clear a task with no timestamp."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at="",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory((task,)))
    with patch.object(
        provider,
        "get_agent_task_first_observed_at",
        side_effect=RuntimeError("comment API unavailable"),
    ):
        assert _classify(provider) is None


def test_first_observed_rate_limit_is_propagated() -> None:
    """A clock-read rate limit is left to the provider's established retry handling."""
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="copilot/pr-42",
        state="in_progress",
        created_at="",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory((task,)))
    with (
        patch.object(
            provider,
            "get_agent_task_first_observed_at",
            side_effect=ProviderRateLimitError(
                retry_after_seconds=30,
                reset_timestamp=None,
                remaining=0,
                provider="github",
                credential_identity="workflow",
                source="agent_tasks",
            ),
        ),
        pytest.raises(ProviderRateLimitError),
    ):
        _classify(provider)


def test_writer_run_inventory_failure_without_expired_task_is_unknown() -> None:
    """Uncorroborated active-run inventory remains unknown when no task is expired."""
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with patch.object(provider, "list_correlated_cloud_writer_runs", side_effect=RuntimeError("Actions unavailable")):
        assert _classify(provider) is None


def test_writer_run_rate_limit_keeps_inventory_unknown() -> None:
    """A rate-limited run inventory cannot be interpreted as an empty run list."""
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with (
        patch.object(
            provider,
            "list_correlated_cloud_writer_runs",
            side_effect=ProviderRateLimitError(
                retry_after_seconds=30,
                reset_timestamp=None,
                remaining=0,
                provider="github",
                credential_identity="workflow",
                source="actions",
            ),
        ),
    ):
        assert _classify(provider) is None


def test_provider_without_writer_run_inventory_preserves_task_classification() -> None:
    """Providers without the optional Actions inventory still classify task clocks."""
    provider = FakeLifecycleProvider(AgentTaskInventory((_task(),)))
    with patch.object(provider, "list_correlated_cloud_writer_runs", None):
        assert _classify(provider) is True


def test_terminal_writer_run_does_not_require_cancellation() -> None:
    """A terminal correlated writer run is ignored rather than mutated."""
    terminal_run = WorkflowRun(
        id=706,
        name="Cloud writer",
        conclusion="success",
        run_attempt=1,
        created_at="2026-10-16T08:00:00Z",
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="completed",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()), runs=[terminal_run])

    assert _classify(provider) is False
    assert provider.cancelled_runs == []


def test_expired_run_without_cancel_operation_is_ignored() -> None:
    """Lack of a supported cancellation operation does not extend an expired run."""
    now = datetime.now(UTC)
    run = WorkflowRun(
        id=707,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at=(now - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="in_progress",
        run_started_at=(now - timedelta(minutes=90)).isoformat(),
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()), runs=[run])
    with patch.object(provider, "cancel_workflow_run", None):
        assert _classify(provider) is False
    assert provider.cancelled_runs == []


def test_read_only_classification_needs_no_invalidation_or_cancellation() -> None:
    """Classification is read-only even when cache invalidation is unsupported."""
    now = datetime.now(UTC)
    run = WorkflowRun(
        id=708,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at=(now - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="in_progress",
        run_started_at=(now - timedelta(minutes=90)).isoformat(),
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()), runs=[run])
    with patch.object(provider, "invalidate_agent_task_inventory", None):
        assert _classify(provider) is False
    assert provider.cancelled_runs == []
    assert provider.invalidated_prs == []


@pytest.mark.parametrize("status", ["completed", "cancelled", "success", "failed"])
def test_terminal_writer_runs_are_not_lifecycle_blockers(status: str) -> None:
    """Terminal workflow states are excluded from writer lifecycle classification."""
    run = WorkflowRun(
        id=703,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at="",
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status=status,
    )

    assert _classify_writer_run(run) is None


def test_unknown_writer_status_and_missing_start_remain_protective() -> None:
    """Unknown run states and absent clocks remain blocking rather than expiring."""
    unknown = WorkflowRun(
        id=704,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at="",
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="unknown",
    )
    missing_start = WorkflowRun(
        id=705,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at="invalid",
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        pr_number=42,
        status="in_progress",
    )

    unknown_assessment = _classify_writer_run(unknown)
    missing_start_assessment = _classify_writer_run(missing_start)

    assert unknown_assessment is not None
    assert unknown_assessment.reason == "unknown-writer-run-status"
    assert missing_start_assessment is not None
    assert missing_start_assessment.reason == "missing-writer-run-start"


def test_malformed_provider_clocks_use_existing_durable_observation() -> None:
    task = replace(
        _task(state="idle"),
        created_at="invalid",
        sessions=(AgentTaskSessionLifecycle(session_id="session-1", state="running", started_at="bad", idle_at="bad"),),
    )
    provider = FakeLifecycleProvider(
        AgentTaskInventory((task,)),
        first_seen=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
    )

    assert _classify(provider) is False
    assert provider.first_observed_calls == [("", "copilot/pr-42"), ("session-1", "copilot/pr-42")]


@pytest.mark.parametrize("complete", [False, True])
def test_typed_writer_inventory_requires_explicit_completeness(complete):
    provider = FakeLifecycleProvider(AgentTaskInventory((_task(created_at=datetime.now(UTC) - timedelta(minutes=90)),)))
    with patch.object(
        provider,
        "list_correlated_cloud_writer_runs",
        return_value=CloudWriterRunInventory(complete=complete),
    ):
        assert _classify(provider) is (False if complete else None)


def test_uncorrelated_expired_writer_is_ignored_but_incomplete_inventory_stays_unknown(caplog):
    run = WorkflowRun(
        id=900,
        name="writer",
        conclusion="",
        run_attempt=1,
        created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="running",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with (
        patch.object(
            provider,
            "list_correlated_cloud_writer_runs",
            return_value=CloudWriterRunInventory(
                uncorrelated_runs=(run,),
                complete=False,
                incomplete_reasons=("page-limit:in_progress",),
                enumeration_complete=False,
            ),
        ),
        caplog.at_level("INFO"),
    ):
        assert _classify(provider) is None
    assert "900" in caplog.text
    assert "page-limit:in_progress" in caplog.text
    assert "Ignoring expired uncorrelated writer runs" in caplog.text
    assert provider.cancelled_runs == []


def test_expired_writer_dispatch_detail_failure_does_not_block_progression(caplog):
    run = WorkflowRun(
        id=700,
        name="writer",
        conclusion="",
        run_attempt=1,
        created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="running",
        run_started_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    inventory = CloudWriterRunInventory(
        uncorrelated_runs=(run,),
        complete=False,
        incomplete_reasons=("dispatch-detail:700",),
        enumeration_complete=True,
        corroboration_incomplete_reasons=("dispatch-detail:700",),
    )
    with (
        patch.object(provider, "list_correlated_cloud_writer_runs", return_value=inventory),
        caplog.at_level("INFO"),
    ):
        assert _classify(provider) is False

    assert "dispatch-detail:700" in caplog.text
    assert "Ignoring expired uncorrelated writer runs" in caplog.text
    assert provider.cancelled_runs == []


def test_expired_correlated_writer_dispatch_detail_failure_does_not_block_progression():
    run = WorkflowRun(
        id=701,
        name="writer",
        conclusion="",
        run_attempt=1,
        created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="running",
        run_started_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    inventory = CloudWriterRunInventory(
        runs=(run,),
        complete=False,
        incomplete_reasons=("dispatch-detail:701",),
        enumeration_complete=True,
        corroboration_incomplete_reasons=("dispatch-detail:701",),
    )
    with patch.object(provider, "list_correlated_cloud_writer_runs", return_value=inventory):
        assert _classify(provider) is False
    assert provider.cancelled_runs == []


def test_unknown_writer_corroboration_reason_keeps_incomplete_inventory_unknown():
    run = WorkflowRun(
        id=702,
        name="writer",
        conclusion="",
        run_attempt=1,
        created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="running",
        run_started_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with patch.object(
        provider,
        "list_correlated_cloud_writer_runs",
        return_value=CloudWriterRunInventory(
            uncorrelated_runs=(run,),
            complete=False,
            incomplete_reasons=("unclassified-detail:702",),
            enumeration_complete=True,
            corroboration_incomplete_reasons=("unclassified-detail:702",),
        ),
    ):
        assert _classify(provider) is None


def test_unknown_age_writer_dispatch_detail_failure_remains_protective():
    run = WorkflowRun(
        id=703,
        name="writer",
        conclusion="",
        run_attempt=2,
        created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="running",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with patch.object(
        provider,
        "list_correlated_cloud_writer_runs",
        return_value=CloudWriterRunInventory(
            uncorrelated_runs=(run,),
            complete=False,
            incomplete_reasons=("dispatch-detail:703",),
            enumeration_complete=True,
            corroboration_incomplete_reasons=("dispatch-detail:703",),
        ),
    ):
        assert _classify(provider) is True
    assert provider.cancelled_runs == []


def test_inventory_consumer_passes_pull_request_database_id() -> None:
    provider = FakeLifecycleProvider(AgentTaskInventory(()))

    assert (
        is_copilot_session_active_via_agent_task(
            "owner/repo",
            42,
            head_branch="copilot/pr-42",
            pr_id=123456,
            head_sha="a" * 40,
            provider=cast(CIPlatformProvider, provider),
        )
        is False
    )
    assert provider.pr_ids == [123456]


def test_uncorrelated_expired_writer_does_not_block_complete_inventory(caplog):
    run = WorkflowRun(
        id=901,
        name="writer",
        conclusion="",
        run_attempt=1,
        created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="running",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with (
        patch.object(
            provider,
            "list_correlated_cloud_writer_runs",
            return_value=CloudWriterRunInventory(uncorrelated_runs=(run,)),
        ),
        caplog.at_level("INFO"),
    ):
        assert _classify(provider) is False
    assert "Ignoring expired uncorrelated writer runs" in caplog.text
    assert provider.cancelled_runs == []


def test_uncorrelated_terminal_writer_does_not_block_complete_inventory():
    run = WorkflowRun(
        id=904,
        name="writer",
        conclusion="success",
        run_attempt=1,
        created_at="",
        event="workflow_dispatch",
        head_branch="copilot/pr-42",
        status="completed",
    )
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with patch.object(
        provider,
        "list_correlated_cloud_writer_runs",
        return_value=CloudWriterRunInventory(uncorrelated_runs=(run,)),
    ):
        assert _classify(provider) is False


@pytest.mark.parametrize(
    "run",
    [
        WorkflowRun(
            id=902,
            name="writer",
            conclusion="",
            run_attempt=1,
            created_at=(datetime.now(UTC) - timedelta(minutes=5)).isoformat(),
            event="workflow_dispatch",
            head_branch="copilot/pr-42",
            status="running",
        ),
        WorkflowRun(
            id=903,
            name="writer",
            conclusion="",
            run_attempt=2,
            created_at=(datetime.now(UTC) - timedelta(minutes=90)).isoformat(),
            event="workflow_dispatch",
            head_branch="copilot/pr-42",
            status="running",
        ),
    ],
)
def test_uncorrelated_young_or_unknown_age_writer_remains_protective(run):
    provider = FakeLifecycleProvider(AgentTaskInventory(()))
    with patch.object(
        provider,
        "list_correlated_cloud_writer_runs",
        return_value=CloudWriterRunInventory(uncorrelated_runs=(run,)),
    ):
        assert _classify(provider) is True
