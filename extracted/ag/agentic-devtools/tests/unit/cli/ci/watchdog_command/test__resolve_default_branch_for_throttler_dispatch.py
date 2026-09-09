"""Tests for _resolve_default_branch_for_throttler_dispatch()."""

import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import _resolve_default_branch_for_throttler_dispatch


class TestResolveDefaultBranchForThrottlerDispatch:
    """Token-selection and authorization fallback for default-branch resolution."""

    def test_uses_fallback_token_when_preferred_is_absent(self) -> None:
        with (
            patch.dict(os.environ, {"GH_TOKEN": "", "FALLBACK_GH_TOKEN": "fallback"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._get_default_branch", return_value="main") as resolver,
        ):
            branch = _resolve_default_branch_for_throttler_dispatch("o/r")

        assert branch == "main"
        resolver.assert_called_once_with("o/r", token="fallback")

    def test_retries_with_fallback_token_after_authorization_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"GH_TOKEN": "preferred", "FALLBACK_GH_TOKEN": "fallback"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._get_default_branch",
                side_effect=[RuntimeError("HTTP 403"), "main"],
            ) as resolver,
        ):
            branch = _resolve_default_branch_for_throttler_dispatch("o/r")

        assert branch == "main"
        assert resolver.call_args_list[0].args == ("o/r",)
        assert resolver.call_args_list[0].kwargs == {"token": "preferred"}
        assert resolver.call_args_list[1].args == ("o/r",)
        assert resolver.call_args_list[1].kwargs == {"token": "fallback"}

    def test_does_not_retry_fallback_after_non_authorization_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"GH_TOKEN": "preferred", "FALLBACK_GH_TOKEN": "fallback"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._get_default_branch",
                side_effect=RuntimeError("network failed"),
            ) as resolver,
        ):
            with pytest.raises(RuntimeError, match="network failed"):
                _resolve_default_branch_for_throttler_dispatch("o/r")

        resolver.assert_called_once_with("o/r", token="preferred")
