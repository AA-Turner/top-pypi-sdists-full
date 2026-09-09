"""Tests for _resolve_default_branch_for_redispatch_dispatch()."""

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.watchdog_command import _resolve_default_branch_for_redispatch_dispatch


class TestResolveDefaultBranchForRedispatchDispatch:
    """Token-selection policy for redispatch default-branch lookup."""

    def test_prefers_fallback_when_cooldown_is_active(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "GH_TOKEN": "preferred",
                    "FALLBACK_GH_TOKEN": "fallback",
                    "COOLDOWN_ACTIVE": "true",
                    "LOOP_EXIT_CODE": "0",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            branch = _resolve_default_branch_for_redispatch_dispatch("o/r")

        assert branch == "main"
        resolver.assert_called_once_with("o/r", token="fallback")

    def test_prefers_fallback_when_loop_exit_code_is_rate_limit_pause(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "GH_TOKEN": "preferred",
                    "FALLBACK_GH_TOKEN": "fallback",
                    "COOLDOWN_ACTIVE": "false",
                    "LOOP_EXIT_CODE": "6",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            branch = _resolve_default_branch_for_redispatch_dispatch("o/r")

        assert branch == "main"
        resolver.assert_called_once_with("o/r", token="fallback")

    def test_uses_none_token_when_neither_token_is_available(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "GH_TOKEN": "",
                    "FALLBACK_GH_TOKEN": "",
                    "COOLDOWN_ACTIVE": "false",
                    "LOOP_EXIT_CODE": "0",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            branch = _resolve_default_branch_for_redispatch_dispatch("o/r")

        assert branch == "main"
        resolver.assert_called_once_with("o/r", token=None)
