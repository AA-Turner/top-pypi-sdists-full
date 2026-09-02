"""Tests for the is_copilot_login helper in CI models."""

import pytest

from agentic_devtools.cli.ci.models import COPILOT_LOGINS, is_copilot_login


class TestIsCopilotLogin:
    """Tests for is_copilot_login(login) case-insensitive Copilot identity check."""

    @pytest.mark.parametrize("login", sorted(COPILOT_LOGINS))
    def test_exact_case_matches(self, login: str) -> None:
        """Every login in COPILOT_LOGINS is recognised at its canonical casing."""
        assert is_copilot_login(login) is True

    def test_uppercase_copilot_matches(self) -> None:
        """GitHub logins are case-insensitive; 'COPILOT' must be recognised."""
        assert is_copilot_login("COPILOT") is True

    def test_mixed_case_copilot_matches(self) -> None:
        """Mixed casing of a known login is still recognised."""
        assert is_copilot_login("Copilot-Pull-Request-Reviewer[bot]") is True

    def test_non_copilot_login_returns_false(self) -> None:
        """An ordinary human login must not be treated as Copilot."""
        assert is_copilot_login("octocat") is False

    def test_github_actions_bot_returns_false(self) -> None:
        """github-actions[bot] is not a Copilot identity and must return False."""
        assert is_copilot_login("github-actions[bot]") is False

    def test_empty_string_returns_false(self) -> None:
        """An empty login string is not a Copilot identity."""
        assert is_copilot_login("") is False

    @pytest.mark.parametrize("login", [None, 123, object()])
    def test_non_string_login_returns_false(self, login: object) -> None:
        """Non-string values must fail open to False instead of raising."""
        assert is_copilot_login(login) is False  # type: ignore[arg-type]
