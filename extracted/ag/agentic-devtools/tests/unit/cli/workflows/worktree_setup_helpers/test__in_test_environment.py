"""Tests for _in_test_environment."""

from agentic_devtools.cli.workflows.worktree_setup_helpers import _in_test_environment


def test_detects_pytest_environment(monkeypatch):
    """A set pytest marker indicates a test environment."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "test_case")

    assert _in_test_environment() is True


def test_returns_false_without_pytest_environment(monkeypatch):
    """An unset pytest marker indicates a normal runtime."""
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    assert _in_test_environment() is False
