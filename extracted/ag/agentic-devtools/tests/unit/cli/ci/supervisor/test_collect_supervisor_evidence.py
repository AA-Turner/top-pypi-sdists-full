"""Tests for collecting supervisor evidence from the CI provider."""

from datetime import UTC, datetime

from agentic_devtools.cli.ci.models import CheckRunStatus, IssueCommentInfo, PRMetadata, ReviewInfo
from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun
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
    assert evidence.agent_task_updated_at == datetime(2026, 8, 31, 11, 0, tzinfo=UTC)
    assert evidence.api_errors == ()


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
    invalid_time = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[{"pullRequestNumber": 7, "updatedAt": "invalid"}],
        now=NOW,
    )
    naive_time = collect_supervisor_evidence(
        Provider(),
        7,
        tasks=[{"pullRequestNumber": 7, "updatedAt": "2026-08-31T11:00:00"}],
        now=NOW,
    )

    assert missing_time.agent_task_updated_at is None
    assert invalid_time.agent_task_updated_at is None
    assert naive_time.agent_task_updated_at == datetime(2026, 8, 31, 11, 0, tzinfo=UTC)


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
