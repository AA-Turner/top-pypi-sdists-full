"""Tests for _dispatch_redispatch_from_loop()."""

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.watchdog_command import _dispatch_redispatch_from_loop


class TestDispatchRedispatchFromLoop:
    """Credential-selection policy for redispatch from ai-pr-loop.yml."""

    def test_uses_default_workflow_token(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token", return_value=(0, "")) as dispatch,
        ):
            status = _dispatch_redispatch_from_loop("o/r", "main")

        assert status == 0
        dispatch.assert_called_once_with("ai-pr-loop-redispatch.yml", "o/r", "main", "workflow-token")

    def test_does_not_use_other_credentials(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "GH_TOKEN": "ambient-token",
                    "SPECKIT_PR_TOKEN": "legacy-token",
                    "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token", return_value=(0, "")) as dispatch,
        ):
            status = _dispatch_redispatch_from_loop("o/r", "main")

        assert status == 0
        dispatch.assert_called_once_with("ai-pr-loop-redispatch.yml", "o/r", "main", "workflow-token")

    def test_reports_missing_default_workflow_token(self, capsys) -> None:
        with (
            patch.dict(
                os.environ,
                {"GH_TOKEN": "", "SPECKIT_PR_TOKEN": ""},
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token") as dispatch,
        ):
            status = _dispatch_redispatch_from_loop("o/r", "main")

        assert status == 2
        dispatch.assert_not_called()
        assert "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is required" in capsys.readouterr().out

    def test_reports_dispatch_failure(self, capsys) -> None:
        with (
            patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"}, clear=True),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._dispatch_with_token",
                return_value=(1, "authorization failed"),
            ) as dispatch,
        ):
            status = _dispatch_redispatch_from_loop("o/r", "main")

        assert status == 1
        dispatch.assert_called_once_with("ai-pr-loop-redispatch.yml", "o/r", "main", "workflow-token")
        assert "Default repository-workflow credential dispatch failed: authorization failed" in capsys.readouterr().out
