"""Tests for collecting supervisor evidence from the CI provider."""

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    CheckRunStatus,
    IssueCommentInfo,
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory, WorkflowRun
from agentic_devtools.cli.ci.supervisor import collect_supervisor_evidence

NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


class Provider:
    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        return PRMetadata(
            number=pr_number,
            title="Example",
            head_branch="feature/example",
            head_sha="a" * 40,
            base_branch="main",
            head_repo_full_name="swai-factory/agentic-devtools",
            base_repo_full_name="swai-factory/agentic-devtools",
            labels=["ai-auto-merge-allowed"],
        )

    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        return [CheckRunStatus(id=1, name="tests", status="completed", conclusion="success")]

    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        return [ReviewInfo(id=2, user="copilot-pull-request-reviewer[bot]", state="APPROVED", commit_sha="a" * 40)]

    def count_unresolved_review_threads(self, pr_number: int) -> int:
        return 0

    def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
        return []


def test_collect_supervisor_evidence_combines_provider_and_task_facts() -> None:
    tasks = [{"id": "task-1", "status": "completed", "pullRequestNumber": 7, "createdAt": "2026-08-31T11:00:00Z"}]

    evidence = collect_supervisor_evidence(Provider(), 7, tasks=tasks, now=NOW)

    assert evidence.pr_number == 7
    assert evidence.has_auto_merge_label is True
    assert evidence.ci_status == "passing"
    assert evidence.has_review_on_head is True
    assert evidence.agent_task_status == "completed"
    assert evidence.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 0, tzinfo=UTC)
    assert evidence.api_errors == ()


def test_collect_supervisor_evidence_uses_typed_newest_session_clock_not_task_heartbeat() -> None:
    class LifecycleProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            assert (pr_number, head_branch, head_sha) == (7, "feature/example", "a" * 40)
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=7,
                        head_branch="feature/example",
                        state="in_progress",
                        created_at="2026-08-31T09:00:00Z",
                        sessions=(
                            AgentTaskSessionLifecycle(
                                session_id="session-old",
                                state="in_progress",
                                started_at="2026-08-31T09:30:00Z",
                            ),
                            AgentTaskSessionLifecycle(
                                session_id="session-new",
                                state="in_progress",
                                started_at="2026-08-31T11:55:00Z",
                            ),
                        ),
                    ),
                )
            )

    evidence = collect_supervisor_evidence(
        LifecycleProvider(),
        7,
        tasks=[{"pullRequestNumber": 7, "state": "in_progress", "updatedAt": "2026-08-31T11:59:00Z"}],
        loop_runs=[
            WorkflowRun(
                id=38877358653,
                name="AI PR Loop",
                conclusion="success",
                run_attempt=1,
                created_at="2026-08-31T11:59:00Z",
                event="schedule",
                head_branch="main",
                pr_number=7,
                status="completed",
            )
        ],
        now=NOW,
    )

    assert evidence.loop_run_status == "completed"
    assert evidence.loop_run_conclusion == "success"
    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 55, tzinfo=UTC)
    assert evidence.agent_task_lifecycle_status == "blocking_with_expired_lifecycle"


def test_collect_supervisor_evidence_reads_existing_first_observed_clock_without_writing() -> None:
    class FirstObservedProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="idle",
                        created_at="",
                    ),
                )
            )

        def get_agent_task_first_observed_at(
            self,
            pr_number: int,
            *,
            task_id: str,
            session_id: str = "",
            head_branch: str = "",
            expected_head_sha: str,
        ) -> str:
            assert (pr_number, task_id, session_id, head_branch) == (7, "task-1", "", "feature/example")
            assert expected_head_sha == "a" * 40
            return "2026-08-31T11:00:00Z"

    evidence = collect_supervisor_evidence(FirstObservedProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 0, tzinfo=UTC)
    assert evidence.agent_task_lifecycle_status == "blocking"


def test_collect_supervisor_evidence_audits_expired_task_detail_failure_without_blocking() -> None:
    class ExpiredTaskProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=7,
                        head_branch="feature/example",
                        state="in_progress",
                        created_at="2026-08-31T10:44:59Z",
                    ),
                ),
                complete=False,
                incomplete_reasons=("task-detail:task-1",),
            )

    evidence = collect_supervisor_evidence(ExpiredTaskProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "expired"
    assert evidence.agent_task_lifecycle_status == "expired_ignored_not_completed"
    assert evidence.agent_task_lifecycle_reason == "expired-incomplete-task"
    assert evidence.api_errors == ()


def test_collect_supervisor_evidence_keeps_younger_correlated_writer_run_blocking() -> None:
    class WriterRunProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return [
                WorkflowRun(
                    id=700,
                    name="Cloud writer",
                    conclusion="",
                    run_attempt=1,
                    created_at="2026-08-31T11:50:00Z",
                    event="workflow_dispatch",
                    head_branch=head_branch,
                    pr_number=pr_number,
                    status="in_progress",
                    run_started_at="2026-08-31T11:50:00Z",
                )
            ]

    evidence = collect_supervisor_evidence(WriterRunProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_status == "blocking"
    assert evidence.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 50, tzinfo=UTC)


def test_collect_supervisor_evidence_audits_writer_run_lookup_failure_after_expired_task() -> None:
    class IncompleteExpiredProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=7,
                        head_branch=head_branch,
                        state="in_progress",
                        created_at="2026-08-31T10:44:59Z",
                    ),
                ),
                complete=False,
                incomplete_reasons=("task-detail:task-1",),
            )

        def list_correlated_cloud_writer_runs(self, *args, **kwargs):
            raise RuntimeError("Actions inventory unavailable")

    evidence = collect_supervisor_evidence(IncompleteExpiredProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_status == "unknown"
    assert evidence.agent_task_lifecycle_at is None
    assert evidence.agent_task_lifecycle_reason == "writer-run-inventory-unavailable"
    assert evidence.agent_task_incomplete_reasons == (
        "task-detail:task-1",
        "writer-runs:Actions inventory unavailable",
    )
    assert evidence.api_errors == ("agent_task_runs: Actions inventory unavailable",)


def test_collect_supervisor_evidence_records_noncritical_provider_errors() -> None:
    class FailingProvider(Provider):
        def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
            raise RuntimeError("reviews unavailable")

        def count_unresolved_review_threads(self, pr_number: int) -> int:
            raise RuntimeError("threads unavailable")

        def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
            raise RuntimeError("comments unavailable")

    evidence = collect_supervisor_evidence(FailingProvider(), 7, tasks=[], now=NOW)

    assert evidence.has_review_on_head is False
    assert evidence.unresolved_threads == 0
    assert evidence.api_errors == (
        "reviews: reviews unavailable",
        "threads: threads unavailable",
        "issue_comments: comments unavailable",
    )


def test_collect_supervisor_evidence_records_check_errors_and_fork_state() -> None:
    class FailingChecksProvider(Provider):
        def get_pr_metadata(self, pr_number: int) -> PRMetadata:
            metadata = super().get_pr_metadata(pr_number)
            return PRMetadata(**{**metadata.__dict__, "head_repo_full_name": "someone/fork"})

        def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
            raise RuntimeError("checks unavailable")

    evidence = collect_supervisor_evidence(FailingChecksProvider(), 7, tasks=[], now=NOW)

    assert evidence.is_fork is True
    assert evidence.ci_status == "unknown"
    assert evidence.api_errors == ("checks: checks unavailable",)


def test_collect_supervisor_evidence_handles_missing_and_invalid_task_timestamps() -> None:
    missing_time = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[{"pullRequestNumber": 7}],
        now=NOW,
    )
    heartbeat_only = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[{"pullRequestNumber": 7, "updatedAt": "2026-08-31T11:00:00Z"}],
        now=NOW,
    )
    invalid_time = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[{"pullRequestNumber": 7, "createdAt": "invalid"}],
        now=NOW,
    )
    naive_time = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[{"pullRequestNumber": 7, "createdAt": "2026-08-31T11:00:00"}],
        now=NOW,
    )

    assert missing_time.agent_task_lifecycle_at is None
    assert heartbeat_only.agent_task_lifecycle_at is None
    assert invalid_time.agent_task_lifecycle_at is None
    assert naive_time.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 0, tzinfo=UTC)


def test_collect_supervisor_evidence_includes_latest_loop_run() -> None:
    evidence = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[],
        loop_runs=[
            WorkflowRun(
                id=1,
                name="AI PR Loop",
                conclusion="",
                run_attempt=1,
                created_at="2026-08-31T10:00:00Z",
                event="workflow_dispatch",
                head_branch="feature",
                pr_number=7,
            )
        ],
        now=NOW,
    )

    assert evidence.loop_run_status == "in_progress"
    assert evidence.loop_run_conclusion == ""
    assert evidence.loop_run_updated_at == datetime(2026, 8, 31, 10, 0, tzinfo=UTC)


@pytest.mark.parametrize("created_at", ["2026-08-31T09:00:00Z", "", "invalid"])
def test_collect_supervisor_evidence_uses_session_clock_for_nonblocking_task(created_at: str) -> None:
    """A completed task's newest session transition is retained as lifecycle evidence."""

    class CompletedTaskProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="completed",
                        created_at=created_at,
                        sessions=(
                            AgentTaskSessionLifecycle(
                                session_id="session-1",
                                state="completed",
                                started_at="2026-08-31T09:30:00Z",
                                idle_at="2026-08-31T11:30:00Z",
                            ),
                        ),
                    ),
                )
            )

        def get_agent_task_first_observed_at(
            self,
            pr_number: int,
            *,
            task_id: str,
            session_id: str = "",
            head_branch: str = "",
            expected_head_sha: str,
        ) -> str | None:
            raise AssertionError("provider timestamps should avoid marker reads")

    evidence = collect_supervisor_evidence(CompletedTaskProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "completed"
    assert evidence.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 30, tzinfo=UTC)
    assert evidence.agent_task_incomplete_reasons == ()


def test_collect_supervisor_evidence_reports_inventory_exception() -> None:
    """A failed lifecycle read is surfaced with incomplete lifecycle status."""

    class FailedInventoryProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            raise RuntimeError("task endpoint unavailable")

    evidence = collect_supervisor_evidence(FailedInventoryProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_lifecycle_reason == "inventory-unavailable"
    assert evidence.api_errors == ("agent_tasks: task endpoint unavailable",)


def test_collect_supervisor_evidence_reports_invalid_inventory_type() -> None:
    """An untyped inventory is reported rather than mistaken for an empty inventory."""

    class InvalidInventoryProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return "invalid"  # type: ignore[return-value]

    evidence = collect_supervisor_evidence(InvalidInventoryProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_lifecycle_reason == "invalid-inventory-type"
    assert evidence.api_errors == ("agent_tasks: lifecycle provider returned an invalid inventory",)


def test_collect_supervisor_evidence_audits_old_writer_run_without_cancelling() -> None:
    """The read-only supervisor reports expired runs without claiming completion."""

    class ExpiredWriterRunProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return [
                WorkflowRun(
                    id=701,
                    name="Cloud writer",
                    conclusion="",
                    run_attempt=1,
                    created_at="2026-08-31T10:44:59Z",
                    event="workflow_dispatch",
                    head_branch=head_branch,
                    pr_number=pr_number,
                    status="in_progress",
                    run_started_at="2026-08-31T10:44:59Z",
                )
            ]

    evidence = collect_supervisor_evidence(ExpiredWriterRunProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "expired"
    assert evidence.agent_task_lifecycle_status == "expired_ignored_not_completed"
    assert evidence.agent_task_lifecycle_reason == "expired-writer-run-not-cancelled-by-read-only-supervisor"
    assert evidence.agent_task_run_ids == (701,)


def test_collect_supervisor_evidence_audits_expired_run_detail_failure_without_blocking() -> None:
    run = WorkflowRun(
        id=700,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at="2026-08-31T10:30:00Z",
        event="workflow_dispatch",
        head_branch="feature/example",
        status="in_progress",
        run_started_at="2026-08-31T10:30:00Z",
    )

    class IncompleteRunDetailProvider(Provider):
        def get_pr_metadata(self, pr_number: int) -> PRMetadata:
            return replace(super().get_pr_metadata(pr_number), pr_id=123456)

        def list_pr_agent_task_lifecycles(
            self,
            pr_number: int,
            *,
            pr_id: int | None,
            head_branch: str,
            head_sha: str,
        ):
            assert pr_id == 123456
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return CloudWriterRunInventory(
                uncorrelated_runs=(run,),
                complete=False,
                incomplete_reasons=("dispatch-detail:700",),
                enumeration_complete=True,
                corroboration_incomplete_reasons=("dispatch-detail:700",),
            )

    evidence = collect_supervisor_evidence(IncompleteRunDetailProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "expired"
    assert evidence.agent_task_lifecycle_status == "expired_ignored_not_completed"
    assert (
        evidence.agent_task_lifecycle_reason == "expired-uncorrelated-writer-run-not-cancelled-by-read-only-supervisor"
    )
    assert evidence.agent_task_run_ids == (700,)
    assert evidence.agent_task_incomplete_reasons == ("uncorrelated-writer-run:700", "writer-runs:dispatch-detail:700")
    assert evidence.api_errors == ()


def test_unknown_writer_corroboration_reason_keeps_supervisor_lifecycle_unknown() -> None:
    run = WorkflowRun(
        id=702,
        name="Cloud writer",
        conclusion="",
        run_attempt=1,
        created_at="2026-08-31T10:30:00Z",
        event="workflow_dispatch",
        head_branch="feature/example",
        status="in_progress",
        run_started_at="2026-08-31T10:30:00Z",
    )

    class UnclassifiedRunDetailProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return CloudWriterRunInventory(
                uncorrelated_runs=(run,),
                complete=False,
                incomplete_reasons=("unclassified-detail:702",),
                enumeration_complete=True,
                corroboration_incomplete_reasons=("unclassified-detail:702",),
            )

    evidence = collect_supervisor_evidence(UnclassifiedRunDetailProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "unknown"
    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_lifecycle_reason == "writer-run-inventory-unavailable"
    assert evidence.api_errors == ("agent_task_runs: incomplete writer run inventory: unclassified-detail:702",)


def test_unknown_age_writer_dispatch_detail_failure_remains_protective() -> None:
    run = WorkflowRun(
        id=703,
        name="Cloud writer",
        conclusion="",
        run_attempt=2,
        created_at="2026-08-31T10:30:00Z",
        event="workflow_dispatch",
        head_branch="feature/example",
        status="in_progress",
    )

    class UnknownAgeRunDetailProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return CloudWriterRunInventory(
                uncorrelated_runs=(run,),
                complete=False,
                incomplete_reasons=("dispatch-detail:703",),
                enumeration_complete=True,
                corroboration_incomplete_reasons=("dispatch-detail:703",),
            )

    evidence = collect_supervisor_evidence(UnknownAgeRunDetailProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_status == "blocking"
    assert evidence.agent_task_lifecycle_reason == "uncorrelated-writer-run"
    assert evidence.api_errors == ("agent_task_runs: incomplete writer run inventory: dispatch-detail:703",)


def test_writer_run_inventory_failure_does_not_hide_known_younger_task() -> None:
    """An Actions lookup error cannot downgrade a task already known to be blocking."""

    class ActiveTaskProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="in_progress",
                        created_at="2026-08-31T11:55:00Z",
                    ),
                )
            )

        def list_correlated_cloud_writer_runs(self, *args, **kwargs):
            raise RuntimeError("Actions inventory unavailable")

    evidence = collect_supervisor_evidence(ActiveTaskProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_status == "blocking"
    assert evidence.agent_task_lifecycle_reason == "blocking-lifecycle"
    assert evidence.agent_task_incomplete_reasons == ("writer-runs:Actions inventory unavailable",)
    assert evidence.api_errors == ("agent_task_runs: Actions inventory unavailable",)


def test_unknown_writer_run_without_start_blocks_with_no_timestamp() -> None:
    """A run without a usable clock remains a protective blocker."""

    class UnknownStartProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return [
                WorkflowRun(
                    id=702,
                    name="Cloud writer",
                    conclusion="",
                    run_attempt=1,
                    created_at="invalid",
                    event="workflow_dispatch",
                    head_branch=head_branch,
                    pr_number=pr_number,
                    status="queued",
                )
            ]

    evidence = collect_supervisor_evidence(UnknownStartProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_status == "blocking"
    assert evidence.agent_task_lifecycle_at is None


def test_task_creation_time_is_fallback_for_nonblocking_lifecycle() -> None:
    """A terminal task without session clocks falls back to its creation timestamp."""

    class CompletedTaskProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="completed",
                        created_at="2026-08-31T11:00:00Z",
                    ),
                )
            )

    evidence = collect_supervisor_evidence(CompletedTaskProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "completed"
    assert evidence.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 0, tzinfo=UTC)
    assert evidence.agent_task_lifecycle_status == "no_blocking_lifecycle"


def test_clock_read_errors_are_recorded_without_claiming_clear() -> None:
    """Failed marker reads remain explicit incomplete lifecycle provenance."""

    class FailedClockProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="in_progress",
                        created_at="",
                        sessions=(AgentTaskSessionLifecycle(session_id="session-1", state="running"),),
                    ),
                )
            )

        def get_agent_task_first_observed_at(
            self,
            pr_number: int,
            *,
            task_id: str,
            session_id: str,
            head_branch: str,
            expected_head_sha: str,
        ) -> str | None:
            if session_id:
                raise RuntimeError("marker read unavailable")
            return None

    evidence = collect_supervisor_evidence(FailedClockProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_incomplete_reasons == ("clock:task-1:session-1:marker read unavailable",)
    assert evidence.api_errors == (
        "agent_tasks: incomplete lifecycle inventory: clock:task-1:session-1:marker read unavailable",
    )


def test_unknown_lifecycle_inventory_is_reported_as_an_api_error() -> None:
    """An incomplete page inventory with no known task remains unknown and auditable."""

    class TruncatedInventoryProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory((), complete=False, incomplete_reasons=("page-limit",))

    evidence = collect_supervisor_evidence(TruncatedInventoryProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_incomplete_reasons == ("page-limit",)
    assert evidence.api_errors == ("agent_tasks: incomplete lifecycle inventory: page-limit",)


def test_writer_run_inventory_failure_marks_clean_lifecycle_unknown() -> None:
    """A run inventory gap prevents treating otherwise-clean task evidence as complete."""

    class FailedWriterRunProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, *args, **kwargs):
            raise RuntimeError("Actions inventory unavailable")

    evidence = collect_supervisor_evidence(FailedWriterRunProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_lifecycle_reason == "writer-run-inventory-unavailable"
    assert evidence.agent_task_incomplete_reasons == ("writer-runs:Actions inventory unavailable",)
    assert evidence.api_errors == ("agent_task_runs: Actions inventory unavailable",)


def test_expired_writer_run_does_not_hide_younger_task_blocker() -> None:
    """An expired run cannot downgrade a task lifecycle known to be actively blocking."""

    class ActiveTaskWithExpiredRunProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="in_progress",
                        created_at="2026-08-31T11:55:00Z",
                    ),
                )
            )

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return [
                WorkflowRun(
                    id=703,
                    name="Cloud writer",
                    conclusion="",
                    run_attempt=1,
                    created_at="2026-08-31T10:44:59Z",
                    event="workflow_dispatch",
                    head_branch=head_branch,
                    pr_number=pr_number,
                    status="in_progress",
                    run_started_at="2026-08-31T10:44:59Z",
                )
            ]

    evidence = collect_supervisor_evidence(ActiveTaskWithExpiredRunProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_status == "blocking"
    assert evidence.agent_task_lifecycle_reason == "blocking-lifecycle"
    assert evidence.agent_task_run_ids == (703,)


@pytest.mark.parametrize("include_expired_session", [False, True])
def test_expired_writer_run_preserves_young_session_on_old_task(include_expired_session: bool) -> None:
    """An old writer run must preserve both pure and mixed-age session blockers."""

    class SessionProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            sessions: tuple[AgentTaskSessionLifecycle, ...] = (
                AgentTaskSessionLifecycle(session_id="young", state="in_progress", started_at="2026-08-31T11:55:00Z"),
            )
            if include_expired_session:
                sessions += (
                    AgentTaskSessionLifecycle(session_id="old", state="in_progress", started_at="2026-08-31T10:30:00Z"),
                )
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="in_progress",
                        created_at="2026-08-31T10:30:00Z",
                        sessions=sessions,
                    ),
                )
            )

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return [
                WorkflowRun(
                    id=704,
                    name="Cloud writer",
                    conclusion="",
                    run_attempt=1,
                    created_at="2026-08-31T10:30:00Z",
                    event="workflow_dispatch",
                    head_branch=head_branch,
                    pr_number=pr_number,
                    status="in_progress",
                    run_started_at="2026-08-31T10:30:00Z",
                )
            ]

    evidence = collect_supervisor_evidence(SessionProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "in_progress"
    assert evidence.agent_task_lifecycle_at == datetime(2026, 8, 31, 11, 55, tzinfo=UTC)
    assert evidence.agent_task_lifecycle_status == (
        "blocking_with_expired_lifecycle" if include_expired_session else "blocking"
    )
    assert evidence.agent_task_lifecycle_reason == "blocking-lifecycle"
    assert evidence.agent_task_run_ids == (704,)


def test_expired_writer_run_preserves_unknown_inventory() -> None:
    """An expired writer does not turn incomplete task evidence into a clear result."""

    class UnknownInventoryProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory((), complete=False, incomplete_reasons=("page-limit",))

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            return [
                WorkflowRun(
                    id=705,
                    name="Cloud writer",
                    conclusion="",
                    run_attempt=1,
                    created_at="2026-08-31T10:30:00Z",
                    event="workflow_dispatch",
                    head_branch=head_branch,
                    pr_number=pr_number,
                    status="in_progress",
                    run_started_at="2026-08-31T10:30:00Z",
                )
            ]

    evidence = collect_supervisor_evidence(UnknownInventoryProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_status == "unknown"
    assert evidence.agent_task_lifecycle_status == "unknown"
    assert evidence.agent_task_lifecycle_at is None
    assert evidence.agent_task_incomplete_reasons == ("page-limit",)
    assert evidence.api_errors == ("agent_tasks: incomplete lifecycle inventory: page-limit",)
    assert evidence.agent_task_run_ids == (705,)


@pytest.mark.parametrize("invalid_time", ["invalid", "   ", "2026-99-31T10:30:00Z"])
@pytest.mark.parametrize("with_session", [False, True])
def test_malformed_provider_clocks_use_existing_first_observed_marker(invalid_time: str, with_session: bool) -> None:
    """Nonempty unusable clocks cannot suppress a durable first-observed fallback."""
    marker_reads = []

    class InvalidClockProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="in_progress",
                        created_at=invalid_time,
                        sessions=(
                            (
                                AgentTaskSessionLifecycle(
                                    session_id="session-1",
                                    state="in_progress",
                                    started_at=invalid_time,
                                    idle_at=invalid_time,
                                ),
                            )
                            if with_session
                            else ()
                        ),
                    ),
                )
            )

        def get_agent_task_first_observed_at(
            self, pr_number: int, *, task_id: str, session_id: str, head_branch: str, expected_head_sha: str
        ) -> str:
            assert expected_head_sha == "a" * 40
            marker_reads.append(session_id)
            return "2026-08-31T10:30:00Z"

    evidence = collect_supervisor_evidence(InvalidClockProvider(), 7, tasks=[], now=NOW)

    assert marker_reads == (["", "session-1"] if with_session else [""])
    assert evidence.agent_task_status == "expired"
    assert evidence.agent_task_lifecycle_status == "expired_ignored_not_completed"
    assert evidence.api_errors == ()


def test_collect_supervisor_evidence_preserves_terminal_loop_conclusion() -> None:
    evidence = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[],
        loop_runs=[
            WorkflowRun(
                id=1,
                name="AI PR Loop",
                conclusion="failure",
                run_attempt=1,
                created_at="2026-08-31T10:00:00Z",
                event="workflow_dispatch",
                head_branch="feature",
                pr_number=7,
            )
        ],
        now=NOW,
    )

    assert evidence.loop_run_status == "completed"
    assert evidence.loop_run_conclusion == "failure"


@pytest.mark.parametrize("correlated", [True, False])
@pytest.mark.parametrize("run_status", ["in_progress", "completed"])
def test_typed_writer_inventory_distinguishes_uncorrelated_expiry(correlated: bool, run_status: str) -> None:
    """Only verified associations can expire; active uncorrelated runs stay protective."""

    class TypedRunProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(())

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            run = WorkflowRun(
                id=706,
                name="Cloud writer",
                conclusion="",
                run_attempt=1,
                created_at="2026-08-31T10:30:00Z",
                event="workflow_dispatch",
                head_branch=head_branch,
                pr_number=pr_number,
                status=run_status,
                run_started_at="2026-08-31T10:30:00Z",
            )
            return CloudWriterRunInventory(
                runs=(run,) if correlated else (),
                uncorrelated_runs=() if correlated else (run,),
            )

    evidence = collect_supervisor_evidence(TypedRunProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_run_ids == (706,)
    if run_status == "completed":
        assert evidence.agent_task_lifecycle_status == "no_blocking_lifecycle"
    elif correlated:
        assert evidence.agent_task_lifecycle_status == "expired_ignored_not_completed"
    else:
        assert evidence.agent_task_status == "expired"
        assert evidence.agent_task_lifecycle_status == "expired_ignored_not_completed"
        assert (
            evidence.agent_task_lifecycle_reason
            == "expired-uncorrelated-writer-run-not-cancelled-by-read-only-supervisor"
        )
        assert evidence.agent_task_lifecycle_at is None
        assert evidence.agent_task_incomplete_reasons == ("uncorrelated-writer-run:706",)


@pytest.mark.parametrize("blocker", ["none", "task", "run", "uncorrelated"])
@pytest.mark.parametrize("reasons", [(), ("page-limit",)])
def test_incomplete_writer_inventory_never_clears_without_known_blocker(blocker: str, reasons: tuple[str, ...]) -> None:
    """Incomplete writer evidence remains unknown unless a task or run already blocks."""

    class IncompleteRunProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
            return AgentTaskInventory(
                (
                    AgentTaskLifecycle(
                        task_id="task-1",
                        repository="swai-factory/agentic-devtools",
                        pr_number=pr_number,
                        head_branch=head_branch,
                        state="in_progress",
                        created_at="2026-08-31T11:55:00Z" if blocker == "task" else "2026-08-31T10:30:00Z",
                    ),
                )
            )

        def list_correlated_cloud_writer_runs(self, pr_number: int, *, head_branch: str, tasks, head_sha: str):
            run = WorkflowRun(
                id=707,
                name="Cloud writer",
                conclusion="",
                run_attempt=1,
                created_at="2026-08-31T11:55:00Z" if blocker in {"run", "uncorrelated"} else "2026-08-31T10:30:00Z",
                event="workflow_dispatch",
                head_branch=head_branch,
                pr_number=pr_number,
                status="in_progress",
            )
            return CloudWriterRunInventory(
                runs=() if blocker == "uncorrelated" else (run,),
                uncorrelated_runs=(run,) if blocker == "uncorrelated" else (),
                complete=False,
                incomplete_reasons=reasons,
            )

    evidence = collect_supervisor_evidence(IncompleteRunProvider(), 7, tasks=[], now=NOW)

    assert evidence.agent_task_run_ids == (707,)
    assert evidence.api_errors == (
        "agent_task_runs: incomplete writer run inventory: " + (", ".join(reasons) or "incomplete-inventory"),
    )
    if blocker == "none":
        assert evidence.agent_task_status == "unknown"
        assert evidence.agent_task_lifecycle_status == "unknown"
        assert evidence.agent_task_lifecycle_at is None
        assert evidence.agent_task_lifecycle_reason == "writer-run-inventory-unavailable"
    else:
        assert evidence.agent_task_status == "in_progress"
        assert evidence.agent_task_lifecycle_status in {"blocking", "blocking_with_expired_lifecycle"}
    for reason in reasons or ("incomplete-inventory",):
        assert f"writer-runs:{reason}" in evidence.agent_task_incomplete_reasons


def test_collect_supervisor_evidence_derives_action_markers_from_issue_comments() -> None:
    class ActionProvider(Provider):
        def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
            return [
                IssueCommentInfo(
                    id=1,
                    author="github-actions[bot]",
                    body="| request_review | ✅ all passed | **executed** |",
                    created_at="2026-08-31T10:30:00Z",
                ),
                IssueCommentInfo(
                    id=3,
                    author="github-actions[bot]",
                    body="",
                    created_at="2026-08-31T10:45:00Z",
                ),
                IssueCommentInfo(
                    id=2,
                    author="github-actions[bot]",
                    body="| dispatch_repair | ✅ all passed | **executed** |",
                    created_at="2026-08-31T11:00:00Z",
                ),
            ]

    evidence = collect_supervisor_evidence(ActionProvider(), 7, tasks=[], now=NOW)

    assert evidence.review_requested_at == datetime(2026, 8, 31, 10, 30, tzinfo=UTC)
    assert evidence.last_action == "repair_dispatched"
    assert evidence.last_action_at == datetime(2026, 8, 31, 11, 0, tzinfo=UTC)


def test_collect_supervisor_evidence_ignores_action_markers_from_unauthorized_author() -> None:
    class UnauthorizedProvider(Provider):
        def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
            return [
                IssueCommentInfo(
                    id=1,
                    author="some-contributor",
                    body="| request_review | fake | **executed** |",
                    created_at="2026-08-31T10:30:00Z",
                ),
            ]

    evidence = collect_supervisor_evidence(UnauthorizedProvider(), 7, tasks=[], now=NOW)

    assert evidence.review_requested_at is None
    assert evidence.last_action == ""
    assert evidence.last_action_at is None
