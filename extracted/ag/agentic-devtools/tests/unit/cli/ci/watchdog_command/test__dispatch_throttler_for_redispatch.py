"""Tests for _dispatch_throttler_for_redispatch()."""

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.watchdog_command import _dispatch_throttler_for_redispatch


class TestDispatchThrottlerForRedispatch:
    """Credential policy for throttler dispatch."""

    def test_uses_default_workflow_token(self) -> None:
        with (
            patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token", return_value=(0, "")) as dispatch,
        ):
            status = _dispatch_throttler_for_redispatch("o/r", "main")

        assert status == 0
        dispatch.assert_called_once_with("ai-pr-loop-throttler.yml", "o/r", "main", "workflow-token")

    def test_does_not_dispatch_without_default_workflow_token(self) -> None:
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token") as dispatch,
        ):
            status = _dispatch_throttler_for_redispatch("o/r", "main")

        assert status == 2
        dispatch.assert_not_called()

    def test_returns_dispatch_failure(self) -> None:
        with (
            patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"}, clear=True),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._dispatch_with_token", return_value=(2, "failed")
            ) as dispatch,
        ):
            status = _dispatch_throttler_for_redispatch("o/r", "main")

        assert status == 2
        dispatch.assert_called_once_with("ai-pr-loop-throttler.yml", "o/r", "main", "workflow-token")
