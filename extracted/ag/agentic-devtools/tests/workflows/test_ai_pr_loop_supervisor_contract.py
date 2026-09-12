"""Workflow contract tests for the report-only AI PR Loop supervisor."""

from datetime import UTC, datetime
from pathlib import Path

import yaml

from agentic_devtools.cli.ci.models import CheckRunStatus, IssueCommentInfo, PRMetadata, ReviewInfo
from agentic_devtools.cli.ci.scheduler import EligiblePR
from agentic_devtools.cli.ci.supervisor_command import scan_supervisor

WORKFLOW = Path(".github/workflows/ai-pr-loop-supervisor.yml")
SKILL = Path(".agents/skills/ai-pr-loop-supervision/SKILL.md")
AGENT = Path(".github/agents/ai-pr-loop-supervision.agent.md")


def test_ai_pr_loop_supervisor_has_scheduled_and_manual_triggers() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    triggers = workflow.get("on", workflow.get(True, {}))

    assert "schedule" in triggers
    assert "workflow_dispatch" in triggers
    assert workflow["permissions"] == {"contents": "read", "pull-requests": "read", "actions": "read"}


def test_ai_pr_loop_supervisor_is_read_only_and_bounded() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    job = workflow["jobs"]["scan"]

    assert job["timeout-minutes"] == 10
    run_step = next(step for step in job["steps"] if step.get("name") == "Run read-only supervisor scan")
    assert "agdt-ai-pr-loop-supervisor" in run_step["run"]
    assert "--max-candidates 10" in run_step["run"]


def test_ai_pr_loop_supervisor_scan_uses_only_allowlisted_read_operations() -> None:
    """The report-only scan must fail if it reaches an unapproved provider operation."""

    class StrictReadOnlyProvider:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def __getattr__(self, name: str) -> object:
            raise AssertionError(f"unexpected provider operation: {name}")

        def list_supervisor_prs(self, *, max_prs: int) -> list[EligiblePR]:
            self.calls.append("list_supervisor_prs")
            assert max_prs == 1
            return [EligiblePR(number=4056, created_at="2026-09-10T00:00:00Z")]

        def get_pr_metadata(self, pr_number: int) -> PRMetadata:
            self.calls.append("get_pr_metadata")
            assert pr_number == 4056
            return PRMetadata(
                number=4056,
                title="Example",
                head_branch="feature/example",
                head_sha="abc123",
                base_branch="main",
            )

        def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
            self.calls.append("list_check_runs")
            assert head_sha == "abc123"
            return [CheckRunStatus(id=1, name="checks", status="completed", conclusion="success")]

        def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
            self.calls.append("list_reviews")
            assert pr_number == 4056
            return []

        def count_unresolved_review_threads(self, pr_number: int) -> int:
            self.calls.append("count_unresolved_review_threads")
            assert pr_number == 4056
            return 0

        def list_issue_comments(self, pr_number: int) -> list[IssueCommentInfo]:
            self.calls.append("list_issue_comments")
            assert pr_number == 4056
            return []

    provider = StrictReadOnlyProvider()
    report = scan_supervisor(
        provider,
        tasks=[],
        now=datetime(2026, 9, 10, tzinfo=UTC),
        repository="swai-factory/agentic-devtools",
        max_candidates=1,
    )

    assert report["scanned_count"] == 1
    assert report["candidate_count"] == 0
    assert provider.calls == [
        "list_supervisor_prs",
        "get_pr_metadata",
        "list_check_runs",
        "list_reviews",
        "count_unresolved_review_threads",
        "list_issue_comments",
    ]


def test_ai_pr_loop_supervision_skill_describes_stateless_audit_scan() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert "report-only scanner" in text
    assert "intentionally\nstateless" in text
    assert (
        "Do not dispatch repair work, request review, resolve threads, mutate\n"
        "provider state, admit implementation work, merge pull requests, delete branches"
    ) in text


def test_ai_pr_loop_supervision_skill_disables_child_dispatch() -> None:
    """The report-only scanner does not dispatch child agents."""
    text = SKILL.read_text(encoding="utf-8")
    assert "Do not dispatch a workflow monitor," in text
    assert "any other child agent." in text


def test_ai_pr_loop_supervision_agent_runs_stateless_scan_skill() -> None:
    text = AGENT.read_text(encoding="utf-8")

    frontmatter = yaml.safe_load(text.split("---", 2)[1])
    assert frontmatter["tools"] == ["bash"]
    assert "AI PR Loop supervision skill" in text
    assert "../../.agents/skills/ai-pr-loop-supervision/SKILL.md" in text
    assert "agdt-ai-pr-loop-supervisor" in text
    assert "do not invoke any other" in text
