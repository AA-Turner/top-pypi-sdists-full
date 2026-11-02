"""CLI tests for posting SpecKit progression failure comments."""

import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.progression_failure import progression_failure_comment_command


def _set_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ISSUE_NUMBER", "42")
    monkeypatch.setenv("NEXT_PHASE", "2")
    monkeypatch.setenv("NEXT_PHASE_NAME", "clarify")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setenv("COMMENT_ON_ISSUE", "true")


class TestProgressionFailureCommentCommand:
    def test_posts_task_restart_guard_recovery_guidance(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _set_environment(monkeypatch)
        monkeypatch.setenv("NEXT_PHASE", "3")
        monkeypatch.setenv("TASK_RESTART_GUARD_FAILED", "true")
        monkeypatch.setenv("HIERARCHY_REASON", "parent-spec-missing")
        captured: dict[str, Any] = {}

        def fake_run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            captured["body"] = Path(args[-1]).read_text(encoding="utf-8")
            return subprocess.CompletedProcess(args, 0)

        with patch(
            "agentic_devtools.cli.speckit.progression_failure.subprocess.run",
            side_effect=fake_run,
        ):
            progression_failure_comment_command()

        assert "Phase 3 Requires a Fresh Phase 1 Dispatch" in captured["body"]
        assert "standalone Feature (parent-spec-missing)" in captured["body"]

    def test_posts_comment_from_a_temporary_body_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _set_environment(monkeypatch)
        captured: dict[str, Any] = {}

        def fake_run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            captured["args"] = args
            captured["kwargs"] = kwargs
            captured["body"] = Path(args[-1]).read_text(encoding="utf-8")
            captured["body_path"] = args[-1]
            return subprocess.CompletedProcess(args, 0)

        with patch(
            "agentic_devtools.cli.speckit.progression_failure.subprocess.run",
            side_effect=fake_run,
        ):
            progression_failure_comment_command()

        assert captured["args"][:6] == ["gh", "issue", "comment", "42", "--repo", "owner/repo"]
        assert captured["kwargs"] == {"capture_output": True, "text": True, "shell": False}
        assert "Phase 2 (clarify) Failed" in captured["body"]
        assert not Path(captured["body_path"]).exists()

    def test_skips_comment_when_disabled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _set_environment(monkeypatch)
        monkeypatch.setenv("COMMENT_ON_ISSUE", "false")

        with patch("agentic_devtools.cli.speckit.progression_failure.subprocess.run") as run:
            progression_failure_comment_command()

        run.assert_not_called()

    def test_skips_comment_when_issue_number_is_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _set_environment(monkeypatch)
        monkeypatch.setenv("ISSUE_NUMBER", "")

        with patch("agentic_devtools.cli.speckit.progression_failure.subprocess.run") as run:
            progression_failure_comment_command()

        run.assert_not_called()

    @pytest.mark.parametrize("stderr", ["HTTP 403: Resource not accessible by integration\n", "", None])
    def test_reports_gh_failure(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], stderr: str | None
    ) -> None:
        _set_environment(monkeypatch)
        with (
            patch(
                "agentic_devtools.cli.speckit.progression_failure.subprocess.run",
                return_value=subprocess.CompletedProcess([], 1, stderr=stderr),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            progression_failure_comment_command()

        assert exc_info.value.code == 1
        error = capsys.readouterr().err
        assert "failed to post the SpecKit progression failure comment (gh exit 1)" in error
        if stderr:
            assert stderr.strip() in error
        else:
            assert "None" not in error
