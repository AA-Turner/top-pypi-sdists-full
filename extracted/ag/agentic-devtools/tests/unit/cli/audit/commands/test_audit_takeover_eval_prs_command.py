"""Tests for audit_takeover_eval_prs_command()."""

import json
import os
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.commands import audit_takeover_eval_prs_command


class TestAuditTakeoverEvalPrsCommand:
    """CLI entry point for agdt-audit-takeover-eval-prs."""

    def test_prints_result(self, capsys) -> None:
        result = {"candidates": 1, "processed": [{"pr_number": 11, "outcome": "squashed"}]}
        with (
            patch.object(sys, "argv", ["agdt-audit-takeover-eval-prs", "--repo", "o/r", "--max-prs", "2"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.audit.takeover.takeover_eval_prs", return_value=result) as mock_takeover,
        ):
            audit_takeover_eval_prs_command()

        assert json.loads(capsys.readouterr().out) == result
        mock_takeover.assert_called_once_with(mock_provider_cls.return_value, repo="o/r", max_prs=2)

    def test_defaults_max_prs_to_one(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-audit-takeover-eval-prs", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch("agentic_devtools.cli.audit.takeover.takeover_eval_prs", return_value={}) as mock_takeover,
        ):
            audit_takeover_eval_prs_command()

        assert mock_takeover.call_args.kwargs["max_prs"] == 1

    def test_exits_one_on_failure(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-audit-takeover-eval-prs", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch("agentic_devtools.cli.audit.takeover.takeover_eval_prs", side_effect=RuntimeError("boom")),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_takeover_eval_prs_command()

        assert exc_info.value.code == 1
