"""Tests for ``post_pr_comment()`` in ``request_artifact_fix``."""

import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import patch

from agentic_devtools.cli.speckit.request_artifact_fix import post_pr_comment


class TestPostPrComment:
    """Posts the rendered body through ``gh pr comment --body-file``."""

    def test_passes_the_body_through_a_temporary_file(self) -> None:
        seen: dict[str, Any] = {}

        def fake_run(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
            seen["args"] = args
            seen["kwargs"] = kwargs
            seen["body"] = Path(args[-1]).read_text(encoding="utf-8")
            return subprocess.CompletedProcess(args, 0)

        with patch("agentic_devtools.cli.speckit.request_artifact_fix.run_safe", side_effect=fake_run):
            assert post_pr_comment("42", "owner/repo", "@copilot body") == 0

        assert seen["args"][:6] == ["gh", "pr", "comment", "42", "--repo", "owner/repo"]
        assert seen["args"][6] == "--body-file"
        assert seen["body"] == "@copilot body"
        assert seen["kwargs"]["shell"] is False

    def test_removes_the_temporary_file(self) -> None:
        captured: dict[str, str] = {}

        def fake_run(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
            captured["path"] = args[-1]
            return subprocess.CompletedProcess(args, 0)

        with patch("agentic_devtools.cli.speckit.request_artifact_fix.run_safe", side_effect=fake_run):
            post_pr_comment("42", "owner/repo", "body")

        assert not Path(captured["path"]).exists()

    def test_returns_the_gh_exit_code(self) -> None:
        with patch(
            "agentic_devtools.cli.speckit.request_artifact_fix.run_safe",
            return_value=subprocess.CompletedProcess([], 1),
        ):
            assert post_pr_comment("42", "owner/repo", "body") == 1
