"""Tests for _resolve_default_branch_for_throttler_dispatch()."""

import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import _resolve_default_branch_for_throttler_dispatch


class TestResolveDefaultBranchForThrottlerDispatch:
    """Token selection for default-branch resolution."""

    def test_uses_default_workflow_token(self) -> None:
        with (
            patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            branch = _resolve_default_branch_for_throttler_dispatch("o/r")

        assert branch == "main"
        resolver.assert_called_once_with("o/r", token="workflow-token")

    def test_does_not_use_other_credentials_after_authorization_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token", "FALLBACK_GH_TOKEN": "legacy-token"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._get_default_branch",
                side_effect=RuntimeError("HTTP 403"),
            ) as resolver,
        ):
            with pytest.raises(RuntimeError, match="HTTP 403"):
                _resolve_default_branch_for_throttler_dispatch("o/r")

        resolver.assert_called_once_with("o/r", token="workflow-token")

    def test_does_not_retry_fallback_after_non_authorization_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token", "FALLBACK_GH_TOKEN": "fallback"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._get_default_branch",
                side_effect=RuntimeError("network failed"),
            ) as resolver,
        ):
            with pytest.raises(RuntimeError, match="network failed"):
                _resolve_default_branch_for_throttler_dispatch("o/r")

        resolver.assert_called_once_with("o/r", token="workflow-token")
