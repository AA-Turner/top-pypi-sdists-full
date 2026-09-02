"""Tests for the _normalize_bot_login() helper."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.github_provider import _normalize_bot_login


class TestNormalizeBotLogin:
    """Tests for normalizing a gh-reported author login to the REST identity."""

    @pytest.mark.parametrize(
        ("login", "expected"),
        [
            ("copilot-swe-agent", "copilot-swe-agent[bot]"),
            ("app/copilot-swe-agent", "copilot-swe-agent[bot]"),
            ("copilot-swe-agent[bot]", "copilot-swe-agent[bot]"),
        ],
    )
    def test_bot_logins_gain_the_suffix_exactly_once(self, login: str, expected: str) -> None:
        assert _normalize_bot_login(login, True) == expected

    def test_human_logins_are_left_alone(self) -> None:
        assert _normalize_bot_login("octocat", False) == "octocat"

    def test_empty_login_stays_empty(self) -> None:
        assert _normalize_bot_login("", True) == ""
