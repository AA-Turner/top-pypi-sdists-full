"""Real-repository regression tests for the read-only PR-details preflight.

These tests prove the two safeguards from issue #4151 against an isolated
temporary git repository created inside this cloud job — never against the
original external worktree from the incident report:

1. ``agdt-get-pull-request-details --help`` dispatched through
   :func:`agentic_devtools.cli.runner.run_command` creates no background task,
   skips the post-command persistence hook, and mutates no repository file.
2. Repeated ``set_bootstrap_state()`` initialization leaves an already-canonical
   *tracked* ``.agdt/.gitignore`` byte-for-byte unchanged, so
   ``git status --short`` stays empty for both LF and CRLF checkouts.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.agdt_gitignore import ensure_agdt_gitignore
from agentic_devtools.cli import runner


def _run_git(cwd: Path, *args: str) -> str:
    """Run a git command in *cwd* and return its stripped stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _make_repo_with_tracked_gitignore(tmp_path: Path, *, crlf: bool = False) -> Path:
    """Create a temporary repo whose canonical ``.agdt/.gitignore`` is tracked."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _run_git(repo, "init", "--initial-branch=main")
    _run_git(repo, "config", "user.name", "Test User")
    _run_git(repo, "config", "user.email", "test@example.com")
    # Keep git byte-faithful so a line-ending-only rewrite would show up.
    _run_git(repo, "config", "core.autocrlf", "false")

    assert ensure_agdt_gitignore(repo) is True
    gitignore_path = repo / ".agdt" / ".gitignore"
    content = gitignore_path.read_bytes().replace(b"\r\n", b"\n")
    if crlf:
        content = content.replace(b"\n", b"\r\n")
    gitignore_path.write_bytes(content)

    _run_git(repo, "add", "--force", ".agdt/.gitignore")
    _run_git(repo, "commit", "-m", "track managed gitignore")
    assert _run_git(repo, "status", "--short") == ""
    return repo


class TestPullRequestDetailsHelpPreflight:
    """``agdt-get-pull-request-details --help`` must stay read-only."""

    @pytest.mark.parametrize("help_option", ["-h", "--help"])
    def test_help_dispatch_creates_no_task_and_leaves_repo_clean(self, tmp_path, monkeypatch, capsys, help_option):
        """Runner dispatch of help exits 0 without tasks, persistence, or mutation."""
        repo = _make_repo_with_tracked_gitignore(tmp_path)
        monkeypatch.chdir(repo)
        monkeypatch.setattr(sys, "argv", ["agdt-get-pull-request-details", help_option])

        with patch("agentic_devtools.cli.azure_devops.async_commands.run_function_in_background") as mock_background:
            with patch("agentic_devtools.cli.git.agdt_branch.persist_if_dirty") as mock_persist:
                with pytest.raises(SystemExit) as exc_info:
                    runner.run_command("agdt-get-pull-request-details")

        captured = capsys.readouterr()
        assert exc_info.value.code == 0
        assert "usage:" in captured.out
        assert "pull_request_id" in captured.out
        mock_background.assert_not_called()
        mock_persist.assert_not_called()
        assert _run_git(repo, "status", "--short") == ""


class TestBootstrapTrackedGitignoreInvariant:
    """Repeated bootstrap initialization must not dirty a tracked gitignore."""

    @pytest.mark.parametrize("crlf", [False, True])
    def test_repeated_bootstrap_keeps_tracked_gitignore_clean(self, tmp_path, monkeypatch, crlf):
        """``git status --short`` stays empty across repeated bootstrap calls."""
        repo = _make_repo_with_tracked_gitignore(tmp_path, crlf=crlf)
        monkeypatch.chdir(repo)
        gitignore_path = repo / ".agdt" / ".gitignore"
        original = gitignore_path.read_bytes()
        assert (b"\r\n" in original) is crlf

        state.set_bootstrap_state(identity="ama", worktree_key="ISSUE-4151")
        state.set_bootstrap_state(identity="ama", worktree_key="ISSUE-4151")

        assert gitignore_path.read_bytes() == original
        assert _run_git(repo, "status", "--short") == ""

    def test_bootstrap_repairs_a_materially_incorrect_tracked_gitignore(self, tmp_path, monkeypatch):
        """A corrupted tracked file is still repaired by bootstrap initialization."""
        repo = _make_repo_with_tracked_gitignore(tmp_path)
        monkeypatch.chdir(repo)
        gitignore_path = repo / ".agdt" / ".gitignore"
        gitignore_path.write_bytes(b"stale\n")

        state.set_bootstrap_state(identity="ama", worktree_key="ISSUE-4151")

        content = gitignore_path.read_bytes()
        assert b"stale" not in content
        assert b"runtime-bootstrap.json" in content
        assert _run_git(repo, "status", "--short") == ""
