"""Tests for _in_test_environment."""

from agentic_devtools.cli.copilot.trust import _in_test_environment


class TestInTestEnvironment:
    """Tests for _in_test_environment."""

    def test_true_when_pytest_current_test_set(self, monkeypatch):
        """Returns True when PYTEST_CURRENT_TEST is set."""
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "x")
        assert _in_test_environment() is True

    def test_false_when_pytest_current_test_absent(self, monkeypatch):
        """Returns False when PYTEST_CURRENT_TEST is not set."""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        assert _in_test_environment() is False
