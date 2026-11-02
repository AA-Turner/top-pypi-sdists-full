"""Tests for source-labelled supervisor session evidence output."""

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci import session_evidence_presentation as presentation
from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import LifecycleAssessment
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
from agentic_devtools.cli.ci.scheduler import EligiblePR
from agentic_devtools.cli.ci.supervisor import (
    SupervisorClassification,
    SupervisorState,
    collect_supervisor_evidence,
)
from agentic_devtools.cli.ci.supervisor_command import _candidate_to_dict, _write_step_summary, scan_supervisor

NOW = datetime(2026, 8, 31, 12, 0, tzinfo=UTC)


class HTTP404Error(RuntimeError):
    http_status = 404


class Provider:
    def __init__(
        self,
        inventory: AgentTaskInventory | None = None,
        writer_runs: tuple[WorkflowRun, ...] = (),
    ) -> None:
        self.inventory = inventory or AgentTaskInventory(())
        self.writer_runs = writer_runs

    def list_supervisor_prs(self, max_prs: int) -> list[EligiblePR]:
        return [EligiblePR(number=7, created_at="2026-08-31T08:00:00Z")]

    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        return PRMetadata(pr_number, "Example", "feature/example", "a" * 40, "main")

    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        return []

    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        return []

    def count_unresolved_review_threads(self, pr_number: int) -> int:
        return 0

    def list_issue_comments(self, pr_number: int) -> list[IssueCommentInfo]:
        return []

    def list_pr_agent_task_lifecycles(self, pr_number: int, **kwargs) -> AgentTaskInventory:
        return self.inventory

    def get_agent_task_first_observed_at(self, *args, **kwargs) -> str:
        raise HTTP404Error("session lookup unavailable")

    def list_correlated_cloud_writer_runs(self, *args, **kwargs) -> CloudWriterRunInventory:
        return CloudWriterRunInventory(runs=self.writer_runs)


def _writer_run(run_id: int, created_at: str) -> WorkflowRun:
    return WorkflowRun(
        run_id,
        "Cloud writer",
        "",
        1,
        created_at,
        "workflow_dispatch",
        "feature/example",
        pr_number=7,
        status="in_progress",
        run_started_at=created_at,
        task_id="task-1",
        session_id="session-1",
    )


def _writer_run_fixtures() -> tuple[WorkflowRun, ...]:
    return (
        _writer_run(39648257984, "2026-08-31T11:55:00Z"),
        _writer_run(39655417126, "2026-08-31T11:56:00Z"),
    )


def _active_inventory(*, task_id: str = "task-1", session_id: str = "session-1") -> AgentTaskInventory:
    return AgentTaskInventory(
        (
            AgentTaskLifecycle(
                task_id,
                "owner/repo",
                7,
                "feature/example",
                "in_progress",
                "2026-08-31T11:55:00Z",
                sessions=(
                    AgentTaskSessionLifecycle(
                        session_id,
                        "in_progress",
                        started_at="",
                    ),
                )
                if session_id
                else (),
            ),
        ),
        complete=False,
        incomplete_reasons=("session-reconciliation:task-1",),
        failure_category=FailureCategory.HTTP_NOT_FOUND,
        http_status=404,
    )


def test_scan_reports_independent_404_sources_and_verified_active_identity(tmp_path: Path, monkeypatch) -> None:
    report = scan_supervisor(
        Provider(_active_inventory(), _writer_run_fixtures()),
        tasks=[],
        now=NOW,
        repository="owner/repo",
        max_candidates=5,
    )

    observation = report["session_evidence_audit"][0]
    evidence = observation["session_evidence"]
    assert report["agent_task_lifecycle_audit"][0]["writer_run_ids"] == [39648257984, 39655417126]
    assert evidence["status"] == evidence["display_status"] == "active"
    assert evidence["session_active"] is True
    assert (evidence["task_id"], evidence["session_id"]) == ("task-1", "session-1")
    assert [(item["source"], item["failure_class"], item["http_status"]) for item in evidence["diagnostics"]] == [
        ("session-lookup", "http_not_found", 404),
        ("lifecycle-reconciliation", "http_not_found", 404),
    ]

    summary_path = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary_path))
    _write_step_summary(report)
    summary = summary_path.read_text(encoding="utf-8")
    assert "PR #7: session evidence `active`" in summary
    assert "lifecycle-reconciliation (http_not_found, HTTP 404)" in summary
    assert "session-lookup (http_not_found, HTTP 404)" in summary
    assert "task_id=task-1" in summary and "session_id=session-1" in summary

    candidate = SimpleNamespace(
        evidence=collect_supervisor_evidence(Provider(_active_inventory()), 7, tasks=[], now=NOW),
        classification=SupervisorClassification(SupervisorState.STUCK_CANDIDATE, ("stale_loop_run",)),
        fingerprint="abc",
    )
    candidate_output = _candidate_to_dict(candidate)
    assert candidate_output["session_evidence"]["display_status"] == "active"
    assert candidate_output["session_evidence"]["task_id"] == "task-1"


def test_queued_task_without_sessions_is_not_reported_as_active() -> None:
    provider = Provider(
        AgentTaskInventory(
            (AgentTaskLifecycle("task-queued", "owner/repo", 7, "feature/example", "queued", "2026-08-31T11:55:00Z"),)
        )
    )

    evidence = collect_supervisor_evidence(provider, 7, tasks=[], now=NOW)

    assert evidence.session_evidence is not None
    assert evidence.session_evidence.status.value == "unknown"
    assert evidence.session_evidence.display_status.value == "unknown"
    assert evidence.session_evidence.session_active is None
    assert evidence.session_evidence.task_id is None


@pytest.mark.parametrize(
    ("status", "started_at", "attempt"),
    [
        ("queued", "2026-08-31T11:55:00Z", 1),
        ("pending", "2026-08-31T11:55:00Z", 1),
        ("unrecognized", "2026-08-31T11:55:00Z", 1),
        ("in_progress", "", 2),
    ],
)
@pytest.mark.parametrize("verified_activity", [False, True])
def test_uncertain_writer_keeps_gate_blocked_without_proving_activity(
    status: str, started_at: str, attempt: int, verified_activity: bool
) -> None:
    queued_task = AgentTaskLifecycle(
        "task-queued", "owner/repo", 7, "feature/example", "queued", "2026-08-31T11:55:00Z"
    )
    run = replace(
        _writer_run(11, "2026-08-31T11:55:00Z"),
        status=status,
        run_started_at=started_at,
        run_attempt=attempt,
        task_id="task-queued",
        session_id="",
    )
    active_task = replace(
        _active_inventory().tasks[0],
        sessions=(AgentTaskSessionLifecycle("session-1", "in_progress", started_at="2026-08-31T11:55:00Z"),),
    )
    inventory = AgentTaskInventory((active_task,)) if verified_activity else AgentTaskInventory((queued_task,))
    evidence = collect_supervisor_evidence(Provider(inventory, (run,)), 7, tasks=[], now=NOW)

    assert evidence.agent_task_lifecycle_status == "blocking"
    assert evidence.agent_task_status == "in_progress"
    assert evidence.session_evidence is not None
    projection = presentation.session_evidence_to_dict(evidence.session_evidence)
    assert projection is not None
    assert projection["session_active"] is True
    assert projection["status"] == "active"
    assert projection["display_status"] == ("active" if verified_activity else "unknown")
    assert projection["task_id"] == ("task-1" if verified_activity else None)
    assert projection["session_id"] == ("session-1" if verified_activity else None)
    if not verified_activity:
        assert projection["diagnostics"][-1]["source"] == "identity-verification"


def test_waiting_for_user_lifecycle_keeps_verified_active_identity() -> None:
    provider = Provider(
        AgentTaskInventory(
            (
                AgentTaskLifecycle(
                    "task-waiting",
                    "owner/repo",
                    7,
                    "feature/example",
                    "waiting_for_user",
                    "2026-08-31T11:55:00Z",
                ),
            )
        )
    )

    evidence = collect_supervisor_evidence(provider, 7, tasks=[], now=NOW)

    assert evidence.session_evidence is not None
    assert evidence.session_evidence.display_status.value == "active"
    assert evidence.session_evidence.task_id == "task-waiting"


def test_active_identity_skips_expired_lifecycles_in_mixed_inventory() -> None:
    provider = Provider(
        AgentTaskInventory(
            (
                AgentTaskLifecycle(
                    "task-expired",
                    "owner/repo",
                    7,
                    "feature/example",
                    "in_progress",
                    "2026-08-31T10:00:00Z",
                    sessions=(
                        AgentTaskSessionLifecycle("session-expired", "in_progress", started_at="2026-08-31T10:00:00Z"),
                    ),
                ),
                AgentTaskLifecycle(
                    "task-current",
                    "owner/repo",
                    7,
                    "feature/example",
                    "in_progress",
                    "2026-08-31T11:55:00Z",
                    sessions=(
                        AgentTaskSessionLifecycle("session-current", "in_progress", started_at="2026-08-31T11:55:00Z"),
                    ),
                ),
            )
        )
    )

    evidence = collect_supervisor_evidence(provider, 7, tasks=[], now=NOW)

    assert evidence.session_evidence is not None
    assert evidence.session_evidence.display_status.value == "active"
    assert evidence.session_evidence.task_id == "task-current"
    assert evidence.session_evidence.session_id == "session-current"


@pytest.mark.parametrize("source", ["lifecycle", "writer", "mixed"])
def test_output_never_attributes_another_tasks_session(source: str, tmp_path: Path, monkeypatch) -> None:
    task_b = replace(
        _active_inventory(task_id="task-b").tasks[0],
        sessions=(AgentTaskSessionLifecycle("session-b", "in_progress", started_at="2026-08-31T11:55:00Z"),),
    )
    task_a = replace(task_b, task_id="task-a", sessions=())
    run_a = replace(_writer_run(11, "2026-08-31T11:55:00Z"), task_id="task-a", session_id="")
    run_b = replace(run_a, id=12, task_id="task-b", session_id="session-b")
    tasks = (task_a, task_b) if source == "lifecycle" else (task_a,) if source == "mixed" else ()
    runs = () if source == "lifecycle" else (run_b,) if source == "mixed" else (run_a, run_b)

    report = scan_supervisor(
        Provider(AgentTaskInventory(tasks), runs), tasks=[], now=NOW, repository="owner/repo", max_candidates=5
    )
    projection = report["session_evidence_audit"][0]["session_evidence"]

    assert projection["display_status"] == "active"
    assert (projection["task_id"], projection["session_id"]) == ("task-b", "session-b")
    summary_path = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary_path))
    _write_step_summary(report)
    summary = summary_path.read_text(encoding="utf-8")
    assert "task_id=task-b" in summary and "session_id=session-b" in summary
    assert "task_id=task-a" not in summary


def test_active_evidence_without_verified_identity_is_displayed_as_unknown() -> None:
    evidence = collect_supervisor_evidence(Provider(_active_inventory(task_id="", session_id="")), 7, tasks=[], now=NOW)

    assert evidence.session_evidence is not None
    assert evidence.session_evidence.status.value == "active"
    assert evidence.session_evidence.display_status.value == "unknown"
    assert evidence.session_evidence.session_active is True
    assert evidence.session_evidence.task_id is None
    assert evidence.session_evidence.session_id is None


def test_lifecycle_reconciliation_failure_is_reported_without_session_lookup_failure() -> None:
    class FailingLifecycleProvider(Provider):
        def list_pr_agent_task_lifecycles(self, pr_number: int, **kwargs) -> AgentTaskInventory:
            raise HTTP404Error("lifecycle reconciliation unavailable")

    report = scan_supervisor(FailingLifecycleProvider(), tasks=[], now=NOW, repository="owner/repo", max_candidates=5)
    diagnostics = report["session_evidence_audit"][0]["session_evidence"]["diagnostics"]

    assert [(item["source"], item["failure_class"], item["http_status"]) for item in diagnostics] == [
        ("lifecycle-reconciliation", "http_not_found", 404)
    ]


def test_session_lookup_failure_is_reported_without_lifecycle_failure() -> None:
    inventory = AgentTaskInventory(_active_inventory().tasks)
    report = scan_supervisor(Provider(inventory), tasks=[], now=NOW, repository="owner/repo", max_candidates=5)
    evidence = report["session_evidence_audit"][0]["session_evidence"]

    assert evidence["display_status"] == "active"
    assert [(item["source"], item["failure_class"], item["http_status"]) for item in evidence["diagnostics"]] == [
        ("session-lookup", "http_not_found", 404)
    ]


def test_presentation_helpers_keep_unknown_evidence_and_failure_details() -> None:
    builder = presentation.SessionEvidenceBuilder()
    error = HTTP404Error("lookup unavailable")
    builder.record_exception("session-lookup", error)
    assert builder.record_clock_exception("task-1", "", error) == "clock:task-1:task:lookup unavailable"
    terminal_task = AgentTaskLifecycle("done", "owner/repo", 7, "feature/example", "completed", "")
    builder.record_lifecycle_inventory(
        AgentTaskInventory((terminal_task,)),
        LifecycleAssessment(True, False, None, "uncorrelated-writer-run"),
        NOW,
        {},
    )
    evidence = builder.build("blocking", "")

    assert evidence.session_active is True
    assert evidence.display_status.value == "unknown"
    assert presentation.session_evidence_to_dict(None) is None
    assert presentation.render_session_evidence_observation({"session_evidence": None}) == ""
    assert "unknown-source (unclassified)" in presentation.render_session_evidence({"diagnostics": [{}]})
    with patch.object(presentation, "inventory_failure_result", side_effect=RuntimeError("typed failure unavailable")):
        fallback = presentation.diagnostic_from_exception("fallback", error)
    assert fallback.http_status == 404
