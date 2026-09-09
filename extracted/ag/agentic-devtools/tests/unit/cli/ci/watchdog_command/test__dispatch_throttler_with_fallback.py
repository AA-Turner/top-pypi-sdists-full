"""Tests for _dispatch_throttler_with_fallback()."""

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.watchdog_command import _dispatch_throttler_with_fallback


class TestDispatchThrottlerWithFallback:
    """Credential fallback policy for throttler dispatch."""

    def test_uses_fallback_when_preferred_token_is_absent(self) -> None:
        with (
            patch.dict(os.environ, {"GH_TOKEN": "", "FALLBACK_GH_TOKEN": "ambient-token"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token", return_value=(0, "")) as dispatch,
        ):
            status = _dispatch_throttler_with_fallback("o/r", "main")

        assert status == 0
        dispatch.assert_called_once_with("ai-pr-loop-throttler.yml", "o/r", "main", "ambient-token")

    def test_retries_with_fallback_after_authorization_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"GH_TOKEN": "speckit-token", "FALLBACK_GH_TOKEN": "ambient-token"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._dispatch_with_token",
                side_effect=[(1, "HTTP 403"), (0, "")],
            ) as dispatch,
        ):
            status = _dispatch_throttler_with_fallback("o/r", "main")

        assert status == 0
        assert dispatch.call_args_list[0].args == ("ai-pr-loop-throttler.yml", "o/r", "main", "speckit-token")
        assert dispatch.call_args_list[1].args == ("ai-pr-loop-throttler.yml", "o/r", "main", "ambient-token")

    def test_does_not_retry_after_non_authorization_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"GH_TOKEN": "speckit-token", "FALLBACK_GH_TOKEN": "ambient-token"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._dispatch_with_token",
                return_value=(2, "failed"),
            ) as dispatch,
        ):
            status = _dispatch_throttler_with_fallback("o/r", "main")

        assert status == 2
        dispatch.assert_called_once_with("ai-pr-loop-throttler.yml", "o/r", "main", "speckit-token")

    def test_returns_failure_when_no_dispatch_token_is_available(self) -> None:
        with (
            patch.dict(os.environ, {"GH_TOKEN": "", "FALLBACK_GH_TOKEN": ""}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token") as dispatch,
        ):
            status = _dispatch_throttler_with_fallback("o/r", "main")

        assert status == 2
        dispatch.assert_not_called()
