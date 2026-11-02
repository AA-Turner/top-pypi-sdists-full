"""Tests for _token_from_env()."""

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.watchdog_command import _token_from_env


class TestTokenFromEnv:
    """Environment token normalization."""

    def test_returns_empty_string_when_variable_is_missing(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            assert _token_from_env("GH_TOKEN") == ""

    def test_strips_surrounding_whitespace_from_present_value(self) -> None:
        with patch.dict(os.environ, {"GH_TOKEN": "  token-value \n"}, clear=True):
            assert _token_from_env("GH_TOKEN") == "token-value"

    def test_returns_empty_string_when_value_contains_only_whitespace(self) -> None:
        with patch.dict(os.environ, {"GH_TOKEN": " \t\n "}, clear=True):
            assert _token_from_env("GH_TOKEN") == ""
