"""Tests for audit_reap_stale_command()."""

import json
import os
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.audit.commands import audit_reap_stale_command


class TestAuditReapStaleCommand:
    """CLI entry point for agdt-audit-reap-stale."""

    def test_prints_result_with_explicit_max_age(self, capsys) -> None:
        result = {"checked": 2, "reaped": [1], "skipped": [2]}
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-audit-reap-stale", "--repo", "o/r", "--max-age-hours", "12"],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.audit.reap.reap_stale_in_progress", return_value=result) as mock_reap,
        ):
            audit_reap_stale_command()

        assert json.loads(capsys.readouterr().out) == result
        mock_reap.assert_called_once_with(mock_provider_cls.return_value, max_age_hours=12.0)

    def test_uses_default_max_age_when_omitted(self) -> None:
        from agentic_devtools.cli.audit.reap import DEFAULT_MAX_AGE_HOURS

        with (
            patch.object(sys, "argv", ["agdt-audit-reap-stale", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch("agentic_devtools.cli.audit.reap.reap_stale_in_progress", return_value={}) as mock_reap,
        ):
            audit_reap_stale_command()

        assert mock_reap.call_args.kwargs["max_age_hours"] == DEFAULT_MAX_AGE_HOURS

    def test_exits_one_on_failure(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-audit-reap-stale", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.audit.commands.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.audit.reap.reap_stale_in_progress",
                side_effect=RuntimeError("boom"),
            ),
        ):
            with pytest.raises(SystemExit) as exc_info:
                audit_reap_stale_command()

        assert exc_info.value.code == 1
