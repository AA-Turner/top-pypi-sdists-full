"""Tests for supervisor scan orchestration."""

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.models import CheckRunStatus, IssueCommentInfo, PRMetadata, ReviewInfo
from agentic_devtools.cli.ci.scheduler import EligiblePR
from agentic_devtools.cli.ci.supervisor import SupervisorEvidence
from agentic_devtools.cli.ci.supervisor_command import scan_supervisor

NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


class Provider:
    def list_supervisor_prs(self, max_prs=None) -> list[EligiblePR]:
        return self.list_eligible_prs(max_prs=max_prs)

    def list_eligible_prs(self, max_prs=None) -> list[EligiblePR]:
        if max_prs == 1:
            return [EligiblePR(number=7, created_at="2026-08-31T08:00:00Z")]
        return [
            EligiblePR(number=7, created_at="2026-08-31T08:00:00Z"),
            EligiblePR(number=8, created_at="2026-08-31T09:00:00Z"),
        ]

    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        return PRMetadata(
            number=pr_number,
            title="Stuck PR",
            head_branch="feature/stuck",
            head_sha="a" * 40,
            base_branch="main",
            head_repo_full_name="swai-factory/agentic-devtools",
            base_repo_full_name="swai-factory/agentic-devtools",
            labels=["ai-auto-merge-allowed"],
        )

    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        return [CheckRunStatus(id=1, name="tests", status="completed", conclusion="success")]

    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        return []

    def count_unresolved_review_threads(self, pr_number: int) -> int:
        return 1

    def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
        return []


def test_scan_supervisor_reports_candidates_and_summary_counts() -> None:
    result = scan_supervisor(Provider(), tasks=[], now=NOW, repository="o/r", max_candidates=5)

    assert result["scanned_count"] == 2
    assert result["candidate_count"] == 0
    assert result["candidates"] == []
    assert result["errors"] == []


def test_scan_supervisor_reports_stale_loop_candidate() -> None:
    class StaleProvider(Provider):
        def get_pr_metadata(self, pr_number: int) -> PRMetadata:
            return super().get_pr_metadata(pr_number)

    result = scan_supervisor(
        StaleProvider(),
        tasks=[],
        now=NOW,
        repository="o/r",
        max_candidates=5,
        evidence_overrides={
            7: {
                "loop_run_status": "in_progress",
                "loop_run_updated_at": NOW - timedelta(hours=2),
            }
        },
    )

    assert result["candidate_count"] == 1
    assert result["candidates"][0]["reasons"] == ["stale_loop_run"]


def test_scan_supervisor_passes_workflow_runs_into_evidence() -> None:
    class WorkflowProvider(Provider):
        def list_workflow_runs(self, workflow_id: str, *, window_hours: int, status: str | None):
            assert workflow_id == "ai-pr-loop.yml"
            assert window_hours == 24
            assert status is None
            return [
                type(
                    "Run",
                    (),
                    {
                        "pr_number": 7,
                        "conclusion": "",
                        "created_at": "2026-08-31T10:00:00Z",
                    },
                )()
            ]

    result = scan_supervisor(
        WorkflowProvider(),
        tasks=[],
        loop_runs=WorkflowProvider().list_workflow_runs("ai-pr-loop.yml", window_hours=24, status=None),
        now=NOW,
        repository="o/r",
        max_candidates=5,
    )

    assert result["candidate_count"] == 1
    assert result["candidates"][0]["reasons"] == ["stale_loop_run"]


def test_scan_supervisor_records_per_pr_collection_errors() -> None:
    class FailingProvider(Provider):
        def get_pr_metadata(self, pr_number: int) -> PRMetadata:
            raise RuntimeError("metadata unavailable")

    result = scan_supervisor(FailingProvider(), tasks=[], now=NOW, repository="o/r", max_candidates=5)

    assert result["scanned_count"] == 0
    assert result["candidate_count"] == 0
    assert result["errors"] == ["PR #7: metadata unavailable", "PR #8: metadata unavailable"]


def test_scan_supervisor_applies_collection_bound_before_evidence_fetch() -> None:
    result = scan_supervisor(Provider(), tasks=[], now=NOW, repository="o/r", max_candidates=1)

    assert result["scanned_count"] == 1


def test_scan_supervisor_scans_beyond_report_limit_when_scan_budget_is_larger() -> None:
    class WideProvider(Provider):
        def list_supervisor_prs(self, max_prs=None) -> list[EligiblePR]:
            prs = [
                EligiblePR(number=7, created_at="2026-08-31T08:00:00Z"),
                EligiblePR(number=8, created_at="2026-08-31T09:00:00Z"),
                EligiblePR(number=9, created_at="2026-08-31T10:00:00Z"),
            ]
            return prs if max_prs is None else prs[:max_prs]

    result = scan_supervisor(
        WideProvider(),
        tasks=[],
        now=NOW,
        repository="o/r",
        max_candidates=1,
        max_scan_prs=3,
        evidence_overrides={
            9: {
                "loop_run_status": "in_progress",
                "loop_run_updated_at": NOW - timedelta(hours=2),
            }
        },
    )

    assert result["scanned_count"] == 3
    assert result["candidate_count"] == 1
    assert result["candidates"][0]["pr_number"] == 9


def test_scan_supervisor_uses_collected_issue_comment_signals_in_production_path() -> None:
    class SignalProvider(Provider):
        def list_supervisor_prs(self, max_prs=None) -> list[EligiblePR]:
            return [EligiblePR(number=7, created_at="2026-08-31T08:00:00Z")]

        def count_unresolved_review_threads(self, pr_number: int) -> int:
            return 1

        def list_issue_comments(self, issue_or_pr_number: int) -> list[IssueCommentInfo]:
            return [
                IssueCommentInfo(
                    id=1,
                    author="github-actions[bot]",
                    body="| request_review | ✅ all passed | **executed** |",
                    created_at="2026-08-31T09:30:00Z",
                ),
                IssueCommentInfo(
                    id=2,
                    author="github-actions[bot]",
                    body="| dispatch_repair | ✅ all passed | **executed** |",
                    created_at="2026-08-31T10:00:00Z",
                ),
            ]

    result = scan_supervisor(SignalProvider(), tasks=[], now=NOW, repository="o/r", max_candidates=5)

    assert result["candidate_count"] == 1
    assert result["candidates"][0]["reasons"] == ["unresolved_threads_after_repair"]


def test_scan_supervisor_rejects_invalid_scan_limit() -> None:
    with pytest.raises(ValueError, match="max_scan_prs must be a positive integer"):
        scan_supervisor(Provider(), tasks=[], now=NOW, repository="o/r", max_candidates=1, max_scan_prs=0)


def test_scan_supervisor_falls_back_to_scheduler_inventory() -> None:
    class LegacyProvider:
        def __init__(self) -> None:
            self.called_with: int | None = None

        def list_eligible_prs(self, max_prs=None) -> list[EligiblePR]:
            self.called_with = max_prs
            return []

    provider = LegacyProvider()

    result = scan_supervisor(provider, tasks=[], now=NOW, repository="o/r", max_candidates=2, max_scan_prs=3)

    assert result["scanned_count"] == 0
    assert provider.called_with == 3


def test_scan_supervisor_treats_propagated_auto_merge_label_as_present() -> None:
    class PropagatingProvider(Provider):
        def list_supervisor_prs(self, max_prs=None) -> list[EligiblePR]:
            return [
                EligiblePR(
                    number=7,
                    created_at="2026-08-31T08:00:00Z",
                    labels_to_propagate=("ai-auto-merge-allowed",),
                )
            ]

    provider = PropagatingProvider()

    def _collect(*_args, **_kwargs) -> SupervisorEvidence:
        return SupervisorEvidence(
            pr_number=7,
            head_sha="a" * 40,
            ci_status="passing",
            review_state="APPROVED",
            has_auto_merge_label=False,
        )

    def _discover(evidence, **_kwargs):
        assert evidence[0].has_auto_merge_label is True
        return []

    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr("agentic_devtools.cli.ci.supervisor_command.collect_supervisor_evidence", _collect)
        monkeypatch.setattr("agentic_devtools.cli.ci.supervisor_command.discover_supervisor_candidates", _discover)
        result = scan_supervisor(
            provider,
            tasks=[],
            now=NOW,
            repository="o/r",
            max_candidates=1,
            max_scan_prs=1,
        )

    assert result["candidate_count"] == 0
    assert result["errors"] == []


def test_scan_supervisor_marks_evidence_unknown_when_source_errors_exist() -> None:
    result = scan_supervisor(
        Provider(),
        tasks=[],
        now=NOW,
        repository="o/r",
        max_candidates=5,
        source_errors=("workflow_runs: unavailable",),
    )

    assert result["candidate_count"] == 2
    assert result["candidates"][0]["state"] == "unknown"
    assert result["errors"] == ["workflow_runs: unavailable"]
