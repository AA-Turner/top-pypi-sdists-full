"""Tests for _reject_configured_parent_matching_git_root."""

import pytest

from agentic_devtools.cli.git import worktree_paths


class TestRejectConfiguredParentMatchingGitRoot:
    """Tests for _reject_configured_parent_matching_git_root."""

    def test_noop_when_git_root_is_none(self) -> None:
        """Without a git_root, the collision check cannot run and does nothing."""
        worktree_paths._reject_configured_parent_matching_git_root("/repos/acme", "acme", None)

    def test_noop_when_configured_parent_differs_from_git_root(self) -> None:
        """A configured parent that differs from git_root is accepted."""
        worktree_paths._reject_configured_parent_matching_git_root("/repos/wt", "wt", "/repos/acme")

    def test_rejects_when_configured_parent_equals_git_root(self) -> None:
        """A configured parent equal to git_root nests the worktree inside the main checkout."""
        with pytest.raises(ValueError, match="resolves to the main checkout directory"):
            worktree_paths._reject_configured_parent_matching_git_root("/repos/acme", "acme", "/repos/acme")

    def test_rejects_case_insensitively_on_windows_style_paths(self) -> None:
        """Windows-style comparisons fold case, so 'ACME' still collides with 'acme'."""
        with pytest.raises(ValueError, match="resolves to the main checkout directory"):
            worktree_paths._reject_configured_parent_matching_git_root(r"C:\repos\ACME", "ACME", r"C:\repos\acme")

    def test_rejects_unresolvable_symlink_loop(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A symlink loop is reported as a configuration error."""
        monkeypatch.setattr(worktree_paths.Path, "resolve", lambda _path: (_ for _ in ()).throw(RuntimeError("loop")))

        with pytest.raises(ValueError, match="could not be resolved"):
            worktree_paths._reject_configured_parent_matching_git_root("/repos/wt", "wt", "/repos/acme")
