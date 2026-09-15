"""Tests for get_token()."""

from unittest.mock import patch

from agentic_devtools.cli.ci.credential_roles import get_token


def test_returns_stripped_token() -> None:
    with patch.dict("os.environ", {"TOKEN": "  token-value  "}, clear=True):
        assert get_token("TOKEN") == "token-value"


def test_returns_empty_string_when_variable_is_missing() -> None:
    with patch.dict("os.environ", {}, clear=True):
        assert get_token("TOKEN") == ""
