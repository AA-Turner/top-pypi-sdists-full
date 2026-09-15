"""Tests for _resolve_default_branch_for_redispatch_dispatch()."""

import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import _resolve_default_branch_for_redispatch_dispatch


class TestResolveDefaultBranchForRedispatchDispatch:
    """Token-selection policy for redispatch default-branch lookup."""

    def test_uses_default_workflow_token(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            branch = _resolve_default_branch_for_redispatch_dispatch("o/r")

        assert branch == "main"
        resolver.assert_called_once_with("o/r", token="workflow-token")

    def test_does_not_use_other_credentials(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token",
                    "FALLBACK_GH_TOKEN": "legacy-token",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            branch = _resolve_default_branch_for_redispatch_dispatch("o/r")

        assert branch == "main"
        resolver.assert_called_once_with("o/r", token="workflow-token")

    def test_rejects_missing_default_workflow_token(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "GH_TOKEN": "",
                    "FALLBACK_GH_TOKEN": "",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is required"):
                _resolve_default_branch_for_redispatch_dispatch("o/r")

        resolver.assert_not_called()
