"""Tests for get_actionable_check_names()."""

from agentic_devtools.cli.ci.actionable_checks import DEFAULT_ACTIONABLE_CHECK_NAMES, get_actionable_check_names


class TestGetActionableCheckNames:
    """Tests for get_actionable_check_names()."""

    def test_get_actionable_check_names_defaults_when_unset(self, monkeypatch) -> None:
        monkeypatch.delenv("AI_PR_LOOP_ACTIONABLE_CHECKS", raising=False)
        assert get_actionable_check_names() == DEFAULT_ACTIONABLE_CHECK_NAMES

    def test_get_actionable_check_names_parses_environment_override(self, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_ACTIONABLE_CHECKS", " Build, Test , ,CodeQL ")
        assert get_actionable_check_names() == frozenset({"Build", "Test", "CodeQL"})

    def test_get_actionable_check_names_defaults_when_override_empty(self, monkeypatch) -> None:
        monkeypatch.setenv("AI_PR_LOOP_ACTIONABLE_CHECKS", "")
        assert get_actionable_check_names() == DEFAULT_ACTIONABLE_CHECK_NAMES
