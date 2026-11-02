"""Tests for on_pr_close_command()."""

import os
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.on_pr_close import on_pr_close_command


class TestOnPrCloseCommand:
    """Tests for the on_pr_close_command CLI entry point."""

    def test_exits_zero_when_threshold_met(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-audit-on-pr-close", "--threshold", "5"]),
            patch.dict(
                os.environ,
                {
                    "GITHUB_REPOSITORY": "owner/from-env",
                    "GITHUB_WORKSPACE": "/workspace/from-env",
                },
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.audit.on_pr_close.resolve_github_repo",
                return_value="owner/from-env",
            ) as mock_resolve,
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ) as mock_provider_cls,
            patch(
                "agentic_devtools.cli.audit.on_pr_close.check_threshold_and_dispatch",
                return_value=True,
            ) as mock_check,
        ):
            with pytest.raises(SystemExit) as exc_info:
                on_pr_close_command()

        assert exc_info.value.code == 0
        mock_resolve.assert_called_once_with("owner/from-env")
        mock_provider_cls.assert_called_once_with(repo="owner/from-env")
        mock_check.assert_called_once_with(
            mock_provider_cls.return_value,
            5,
            "/workspace/from-env",
        )
        assert capsys.readouterr().out.strip() == "AUDIT_THRESHOLD_MET=true"

    def test_exits_two_when_threshold_not_met(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-audit-on-pr-close", "--threshold", "7", "--repo", "owner/from-arg"],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch(
                "agentic_devtools.cli.audit.on_pr_close.resolve_github_repo",
                return_value="owner/from-arg",
            ) as mock_resolve,
            patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider",
            ) as mock_provider_cls,
            patch(
                "agentic_devtools.cli.audit.on_pr_close.check_threshold_and_dispatch",
                return_value=False,
            ) as mock_check,
            patch("os.getcwd", return_value="/cwd/fallback"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                on_pr_close_command()

        assert exc_info.value.code == 2
        mock_resolve.assert_called_once_with("owner/from-arg")
        mock_provider_cls.assert_called_once_with(repo="owner/from-arg")
        mock_check.assert_called_once_with(
            mock_provider_cls.return_value,
            7,
            "/cwd/fallback",
        )
        assert capsys.readouterr().out.strip() == "AUDIT_THRESHOLD_MET=false"

    def test_exits_one_on_error(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-audit-on-pr-close", "--threshold", "5"]),
            patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/repo"}, clear=True),
            patch(
                "agentic_devtools.cli.audit.on_pr_close.resolve_github_repo",
                return_value="owner/repo",
            ),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.audit.on_pr_close.check_threshold_and_dispatch",
                side_effect=RuntimeError("API failure"),
            ),
        ):
            with pytest.raises(SystemExit) as exc_info:
                on_pr_close_command()

        assert exc_info.value.code == 1
        assert capsys.readouterr().out.strip() == "AUDIT_THRESHOLD_MET=error"
