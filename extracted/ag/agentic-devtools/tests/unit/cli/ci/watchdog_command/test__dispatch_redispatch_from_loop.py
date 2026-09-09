"""Tests for _dispatch_redispatch_from_loop()."""

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.watchdog_command import _dispatch_redispatch_from_loop


class TestDispatchRedispatchFromLoop:
    """Credential-selection policy for redispatch from ai-pr-loop.yml."""

    def test_switches_to_fallback_when_cooldown_is_active(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "GH_TOKEN": "speckit-token",
                    "FALLBACK_GH_TOKEN": "workflow-token",
                    "COOLDOWN_ACTIVE": "true",
                    "LOOP_EXIT_CODE": "0",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token", return_value=(0, "")) as dispatch,
        ):
            status = _dispatch_redispatch_from_loop("o/r", "main")

        assert status == 0
        dispatch.assert_called_once_with("ai-pr-loop-redispatch.yml", "o/r", "main", "workflow-token")

    def test_switches_to_fallback_when_loop_pauses_for_rate_limit(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "GH_TOKEN": "speckit-token",
                    "FALLBACK_GH_TOKEN": "workflow-token",
                    "COOLDOWN_ACTIVE": "false",
                    "LOOP_EXIT_CODE": "6",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token", return_value=(0, "")) as dispatch,
        ):
            status = _dispatch_redispatch_from_loop("o/r", "main")

        assert status == 0
        dispatch.assert_called_once_with("ai-pr-loop-redispatch.yml", "o/r", "main", "workflow-token")

    def test_returns_failure_when_no_dispatch_token_is_available(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"GH_TOKEN": "", "FALLBACK_GH_TOKEN": "", "COOLDOWN_ACTIVE": "false", "LOOP_EXIT_CODE": "0"},
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._dispatch_with_token") as dispatch,
        ):
            status = _dispatch_redispatch_from_loop("o/r", "main")

        assert status == 2
        dispatch.assert_not_called()
