"""Tests for apply_pr_autofix_suggestions_command."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.apply_thread_autofix_suggestions import apply_pr_autofix_suggestions_command


class TestApplyPrAutofixSuggestionsCommand:
    """Tests for the CLI entry point."""

    def test_exits_when_no_pr_number(self) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch("sys.argv", ["cmd", "--platform", "github"]),
            patch(
                "agentic_devtools.cli.apply_thread_autofix_suggestions.get_value",
                return_value=None,
            ),
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_exits_when_gh_not_found(self) -> None:
        with (
            patch("sys.argv", ["cmd", "--pr", "1", "--platform", "github"]),
            patch("shutil.which", return_value=None),
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_browser_dry_run_does_not_require_gh(self, capsys) -> None:
        """--strategy browser --dry-run must succeed even when gh is absent."""
        with (
            patch("shutil.which", return_value=None),  # gh not available
            patch(
                "sys.argv",
                ["cmd", "--pr", "42", "--platform", "github", "--strategy", "browser", "--dry-run"],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github_browser") as mock_browser,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_browser.return_value = {"applied": 0, "commit": None, "dry_run": True}
            apply_pr_autofix_suggestions_command()  # must not SystemExit

        mock_browser.assert_called_once()

    def test_browser_non_dry_run_with_comment_ids_and_resolve_requires_gh(self) -> None:
        """--strategy browser without dry-run + comment-ids + resolve must require gh."""
        with (
            patch("shutil.which", return_value=None),  # gh not available
            patch(
                "sys.argv",
                [
                    "cmd",
                    "--pr",
                    "42",
                    "--platform",
                    "github",
                    "--strategy",
                    "browser",
                    "--comment-ids",
                    "123",
                ],
            ),
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_browser_non_dry_run_no_comment_ids_does_not_require_gh(self, capsys) -> None:
        """--strategy browser without comment-ids skips thread resolution so gh not required."""
        with (
            patch("shutil.which", return_value=None),  # gh not available
            patch(
                "sys.argv",
                ["cmd", "--pr", "42", "--platform", "github", "--strategy", "browser"],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github_browser") as mock_browser,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_browser.return_value = {"applied": 0, "commit": None, "dry_run": False}
            apply_pr_autofix_suggestions_command()  # must not SystemExit

        mock_browser.assert_called_once()

    def test_dispatches_to_github(self, capsys) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch(
                "sys.argv",
                ["cmd", "--pr", "42", "--platform", "github", "--no-resolve"],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github") as mock_gh,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_gh.return_value = {
                "applied": 0,
                "commit": None,
                "files_changed": [],
            }
            apply_pr_autofix_suggestions_command()

        captured = capsys.readouterr()
        assert '"applied": 0' in captured.out

    def test_dispatches_to_azure_devops(self, capsys) -> None:
        with (
            patch(
                "sys.argv",
                ["cmd", "--pr", "42", "--platform", "azure_devops"],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_azure_devops") as mock_ado,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_ado.return_value = {
                "applied": 0,
                "commit": None,
                "error": "not implemented",
            }
            apply_pr_autofix_suggestions_command()

        captured = capsys.readouterr()
        assert "not implemented" in captured.out

    def test_azure_devops_does_not_require_gh(self, capsys) -> None:
        """Azure DevOps dispatch must not require gh to be in PATH."""
        with (
            patch("shutil.which", return_value=None),  # gh not available
            patch(
                "sys.argv",
                ["cmd", "--pr", "42", "--platform", "azure_devops"],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_azure_devops") as mock_ado,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_ado.return_value = {
                "applied": 0,
                "commit": None,
                "error": "not implemented",
            }
            apply_pr_autofix_suggestions_command()  # must not SystemExit

        captured = capsys.readouterr()
        assert "not implemented" in captured.out

    def test_reads_pr_from_state(self, capsys) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch("sys.argv", ["cmd", "--platform", "github", "--no-resolve"]),
            patch(
                "agentic_devtools.cli.apply_thread_autofix_suggestions.get_value",
                return_value="99",
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github") as mock_gh,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_gh.return_value = {"applied": 0, "commit": None}
            apply_pr_autofix_suggestions_command()

        mock_gh.assert_called_once()
        assert mock_gh.call_args.kwargs["pr_number"] == 99

    def test_sets_state_on_commit(self, capsys) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch(
                "sys.argv",
                ["cmd", "--pr", "1", "--platform", "github", "--no-resolve"],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github") as mock_gh,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value") as mock_set,
        ):
            mock_gh.return_value = {"applied": 1, "commit": "sha123"}
            apply_pr_autofix_suggestions_command()

        mock_set.assert_called_once_with("github.applied_suggestions_commit", "sha123")

    def test_parses_comment_ids(self, capsys) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch(
                "sys.argv",
                [
                    "cmd",
                    "--pr",
                    "1",
                    "--platform",
                    "github",
                    "--comment-ids",
                    "100,200,300",
                    "--no-resolve",
                ],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github") as mock_gh,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_gh.return_value = {"applied": 0, "commit": None}
            apply_pr_autofix_suggestions_command()

        assert mock_gh.call_args.kwargs["comment_ids"] == [100, 200, 300]

    def test_exits_on_unsupported_platform(self) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch(
                "sys.argv",
                ["cmd", "--pr", "1", "--platform", "gitlab"],
            ),
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_exits_on_invalid_state_pr_number(self) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch("sys.argv", ["cmd", "--platform", "github"]),
            patch(
                "agentic_devtools.cli.apply_thread_autofix_suggestions.get_value",
                return_value="not-a-number",
            ),
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_exits_on_invalid_comment_ids(self) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch(
                "sys.argv",
                ["cmd", "--pr", "1", "--platform", "github", "--comment-ids", "abc,123"],
            ),
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_exits_on_empty_comment_ids(self) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch(
                "sys.argv",
                ["cmd", "--pr", "1", "--platform", "github", "--comment-ids", ","],
            ),
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_auto_detects_platform(self, capsys) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch("sys.argv", ["cmd", "--pr", "1", "--no-resolve"]),
            patch(
                "agentic_devtools.cli.apply_thread_autofix_suggestions._detect_platform",
                return_value="github",
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github") as mock_gh,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_gh.return_value = {"applied": 0, "commit": None}
            apply_pr_autofix_suggestions_command()

        mock_gh.assert_called_once()

    def test_strategy_browser_dispatches_to_browser(self, capsys) -> None:
        with (
            patch("shutil.which", return_value="/usr/bin/gh"),
            patch(
                "sys.argv",
                ["cmd", "--pr", "42", "--platform", "github", "--strategy", "browser", "--dry-run", "--no-resolve"],
            ),
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions._apply_github_browser") as mock_browser,
            patch("agentic_devtools.cli.apply_thread_autofix_suggestions.set_value"),
        ):
            mock_browser.return_value = {"applied": 0, "commit": None, "dry_run": True}
            apply_pr_autofix_suggestions_command()

        mock_browser.assert_called_once()
        assert mock_browser.call_args.kwargs["dry_run"] is True

    def test_strategy_browser_rejects_azure_devops(self) -> None:
        with patch(
            "sys.argv",
            ["cmd", "--pr", "42", "--platform", "azure_devops", "--strategy", "browser"],
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()

    def test_dry_run_rejected_with_auto_strategy(self) -> None:
        with patch(
            "sys.argv",
            ["cmd", "--pr", "42", "--platform", "github", "--dry-run"],
        ):
            with pytest.raises(SystemExit):
                apply_pr_autofix_suggestions_command()
