"""Tests for _get_worktree_setup_stderr_capture_limit."""

from agentic_devtools.cli.workflows.worktree_setup import (
    _SETUP_STDERR_READ_LIMIT,
    _SETUP_STDERR_SANITIZE_OVERLAP,
)
from agentic_devtools.cli.workflows.worktree_setup_cleanup import _get_worktree_setup_stderr_capture_limit


def test_includes_longest_configured_secret(monkeypatch):
    """Capture space includes the longest token to allow complete redaction."""
    for name in ("AZURE_DEV_OPS_COPILOT_PAT", "GITHUB_TOKEN", "JIRA_COPILOT_PAT"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("GITHUB_TOKEN", "x" * (_SETUP_STDERR_SANITIZE_OVERLAP + 1))

    assert _get_worktree_setup_stderr_capture_limit() == _SETUP_STDERR_READ_LIMIT + _SETUP_STDERR_SANITIZE_OVERLAP + 1
