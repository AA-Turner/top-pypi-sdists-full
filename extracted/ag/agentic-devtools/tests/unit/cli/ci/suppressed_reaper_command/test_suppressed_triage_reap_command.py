"""Tests for suppressed_triage_reap_command()."""

import json
import os
from unittest.mock import patch

from agentic_devtools.cli.ci.suppressed_reaper_command import suppressed_triage_reap_command


class TestSuppressedTriageReapCommand:
    """CLI entry point for agdt-suppressed-triage-reap."""

    def test_prints_result_and_returns_zero(self, capsys) -> None:
        result = {"checked": 2, "closed": [{"pr": 1, "issue": 1240}], "skipped": [], "dry_run": False}
        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "agentic_devtools.cli.ci.suppressed_reaper_command.resolve_github_repo",
                return_value="o/r",
            ),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider") as mock_provider_cls,
            patch(
                "agentic_devtools.cli.ci.suppressed_reaper.reap_no_change_prs",
                return_value=result,
            ) as mock_reap,
        ):
            exit_code = suppressed_triage_reap_command(["--repo", "o/r"])

        assert exit_code == 0
        assert json.loads(capsys.readouterr().out) == result
        mock_reap.assert_called_once_with(mock_provider_cls.return_value, max_prs=None, dry_run=False)

    def test_forwards_max_prs_and_dry_run(self) -> None:
        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "agentic_devtools.cli.ci.suppressed_reaper_command.resolve_github_repo",
                return_value="o/r",
            ),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.ci.suppressed_reaper.reap_no_change_prs",
                return_value={},
            ) as mock_reap,
        ):
            exit_code = suppressed_triage_reap_command(["--repo", "o/r", "--max-prs", "5", "--dry-run"])

        assert exit_code == 0
        assert mock_reap.call_args.kwargs == {"max_prs": 5, "dry_run": True}

    def test_falls_back_to_the_github_repository_environment_variable(self) -> None:
        with (
            patch.dict(os.environ, {"GITHUB_REPOSITORY": "env/repo"}, clear=True),
            patch(
                "agentic_devtools.cli.ci.suppressed_reaper_command.resolve_github_repo",
                return_value="env/repo",
            ) as mock_resolve,
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.suppressed_reaper.reap_no_change_prs", return_value={}),
        ):
            assert suppressed_triage_reap_command([]) == 0

        mock_resolve.assert_called_once_with("env/repo")
        assert mock_provider_cls.call_args.kwargs == {"repo": "env/repo"}

    def test_returns_one_on_failure(self) -> None:
        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "agentic_devtools.cli.ci.suppressed_reaper_command.resolve_github_repo",
                return_value="o/r",
            ),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.ci.suppressed_reaper.reap_no_change_prs",
                side_effect=RuntimeError("boom"),
            ),
        ):
            assert suppressed_triage_reap_command(["--repo", "o/r"]) == 1
