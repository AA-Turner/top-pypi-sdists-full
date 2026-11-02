"""Tests for writing supervisor Step Summary output."""

from pathlib import Path

from agentic_devtools.cli.ci.supervisor_command import _write_step_summary


def test_write_step_summary_does_nothing_without_environment_path(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

    _write_step_summary({"scanned_count": 0, "candidate_count": 0, "errors": [], "candidates": []})


def test_write_step_summary_writes_candidate_details(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(path))

    _write_step_summary(
        {
            "scanned_count": 2,
            "candidate_count": 1,
            "errors": ["one"],
            "candidates": [{"pr_number": 7, "reasons": ["stale_loop_run"], "fingerprint": "abc"}],
            "agent_task_lifecycle_audit": [
                {
                    "pr_number": 8,
                    "status": "expired_ignored_not_completed",
                    "reason": "expired-incomplete-task",
                    "incomplete_reasons": ["task-detail:task-1"],
                    "task_ids": ["task-1"],
                    "writer_run_ids": [],
                }
            ],
        }
    )

    content = path.read_text(encoding="utf-8")
    assert "PRs scanned | 2" in content
    assert "PR #7: stale_loop_run" in content
    assert "PR #8: agent-task lifecycle `expired_ignored_not_completed`" in content
    assert "incomplete evidence: task-detail:task-1" in content


def test_write_step_summary_omits_incomplete_note_for_complete_lifecycle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Lifecycle audit entries without evidence gaps do not claim incomplete data."""
    path = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(path))

    _write_step_summary(
        {
            "scanned_count": 1,
            "candidate_count": 0,
            "errors": [],
            "candidates": [],
            "agent_task_lifecycle_audit": [
                {
                    "pr_number": 8,
                    "status": "expired_ignored_not_completed",
                    "reason": "expired-lifecycle",
                    "incomplete_reasons": [],
                    "task_ids": ["task-1"],
                    "writer_run_ids": [],
                }
            ],
        }
    )

    content = path.read_text(encoding="utf-8")
    assert "PR #8: agent-task lifecycle `expired_ignored_not_completed`" in content
    assert "incomplete evidence" not in content
