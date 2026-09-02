"""Tests for audit_apply_command()."""

import json
import os
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.commands import audit_apply_command


class TestAuditApplyCommand:
    """Tests for the audit_apply_command CLI entry point."""

    def test_parses_pr_numbers_and_prints_result(self, capsys) -> None:
        result = {"outcome": "no_changes", "status": "applied", "branch": "audit/batch-123"}

        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-audit-apply",
                    "--batch-id",
                    "batch-123",
                    "--output-dir",
                    "/workspace/batch",
                    "--pr-numbers",
                    "1, 2,3",
                    "--repo",
                    "owner/from-arg",
                    "--tracking-issue",
                    "2029",
                    "--base-sha",
                    "abc123",
                    "--eval-pr-branch",
                    "copilot/x",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_WORKSPACE": "/workspace/from-env"}, clear=True),
            patch(
                "agentic_devtools.cli.audit.commands.resolve_github_repo",
                return_value="owner/from-arg",
            ) as mock_resolve,
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ) as mock_provider_cls,
            patch(
                "agentic_devtools.cli.audit.apply.apply_audit_results",
                return_value=result,
            ) as mock_apply,
        ):
            audit_apply_command()

        mock_resolve.assert_called_once_with("owner/from-arg")
        mock_provider_cls.assert_called_once_with(repo="owner/from-arg")
        mock_apply.assert_called_once_with(
            provider=mock_provider_cls.return_value,
            batch_id="batch-123",
            output_dir="/workspace/batch",
            pr_numbers=[1, 2, 3],
            repo_path="/workspace/from-env",
            tracking_issue=2029,
            github_repo="owner/from-arg",
            base_sha="abc123",
            eval_pr_branch="copilot/x",
        )
        assert json.loads(capsys.readouterr().out) == result

    def test_exits_one_when_apply_fails(self) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-audit-apply",
                    "--batch-id",
                    "batch-123",
                    "--output-dir",
                    "/workspace/batch",
                    "--tracking-issue",
                    "2029",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/from-env"}, clear=True),
            patch(
                "agentic_devtools.cli.audit.commands.resolve_github_repo",
                return_value="owner/from-env",
            ) as mock_resolve,
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ) as mock_provider_cls,
            patch(
                "agentic_devtools.cli.audit.apply.apply_audit_results",
                side_effect=RuntimeError("boom"),
            ),
            patch("os.getcwd", return_value="/cwd/fallback"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_apply_command()

        assert exc_info.value.code == 1
        mock_resolve.assert_called_once_with("owner/from-env")
        mock_provider_cls.assert_called_once_with(repo="owner/from-env")

    def test_exits_one_when_pr_numbers_contains_non_integer(self) -> None:
        """A non-integer value in --pr-numbers is handled gracefully and exits 1."""
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-audit-apply",
                    "--batch-id",
                    "batch-123",
                    "--output-dir",
                    "/workspace/batch",
                    "--pr-numbers",
                    "1,abc",
                    "--tracking-issue",
                    "2029",
                ],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch(
                "agentic_devtools.cli.audit.commands.resolve_github_repo",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ),
            patch("os.getcwd", return_value="/cwd/fallback"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_apply_command()

        assert exc_info.value.code == 1

    def test_exits_when_tracking_issue_missing(self) -> None:
        """Missing --tracking-issue causes argparse to exit with a usage error."""
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-audit-apply",
                    "--batch-id",
                    "batch-123",
                    "--output-dir",
                    "/workspace/batch",
                    "--repo",
                    "owner/repo",
                ],
            ),
            patch.dict(os.environ, {}, clear=True),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_apply_command()

        assert exc_info.value.code == 2

    def test_exits_one_on_failure_outcome(self, capsys) -> None:
        result = {"outcome": "pr_failed", "pr_url": ""}
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-audit-apply", "--batch-id", "b", "--output-dir", "/w", "--tracking-issue", "1"],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch("agentic_devtools.cli.audit.apply.apply_audit_results", return_value=result),
            patch("os.getcwd", return_value="/cwd"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_apply_command()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert json.loads(captured.out) == result  # JSON still printed to stdout
        assert "::error::" in captured.err

    def test_writes_step_summary_when_env_set(self, tmp_path, capsys) -> None:
        summary_file = tmp_path / "summary.md"
        result = {
            "outcome": "pr_ready",
            "pr_url": "https://github.com/o/r/pull/3",
            "files_modified": [],
            "files_created": [],
        }
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-audit-apply", "--batch-id", "b", "--output-dir", "/w", "--tracking-issue", "1"],
            ),
            patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary_file)}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch("agentic_devtools.cli.audit.apply.apply_audit_results", return_value=result),
            patch("os.getcwd", return_value="/cwd"),
        ):
            audit_apply_command()

        content = summary_file.read_text(encoding="utf-8")
        assert "Instruction-update PR" in content
        assert "https://github.com/o/r/pull/3" in content

    def test_step_summary_write_failure_is_swallowed(self, tmp_path, capsys) -> None:
        result = {"outcome": "no_changes"}
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-audit-apply", "--batch-id", "b", "--output-dir", "/w", "--tracking-issue", "1"],
            ),
            patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(tmp_path / "s.md")}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch("agentic_devtools.cli.audit.apply.apply_audit_results", return_value=result),
            patch("os.getcwd", return_value="/cwd"),
            patch("builtins.open", side_effect=OSError("disk full")),
        ):
            audit_apply_command()

        assert json.loads(capsys.readouterr().out) == result
