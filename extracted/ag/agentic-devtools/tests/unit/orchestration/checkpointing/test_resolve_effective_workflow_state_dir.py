"""Tests for resolve_effective_workflow_state_dir."""

from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.checkpointing import resolve_effective_workflow_state_dir


class TestResolveEffectiveWorkflowStateDir:
    """Tests for resolve_effective_workflow_state_dir()."""

    def test_returns_state_dir_unchanged_when_no_repo_root(self, tmp_path):
        """Without a repo root, the input state_dir is returned unchanged."""
        state_dir = tmp_path / "some" / "dir"
        with patch("agentic_devtools.state.get_repo_root", return_value=None):
            result = resolve_effective_workflow_state_dir(state_dir=state_dir, worktree_key="FEATURE-42")
        assert result == state_dir

    def test_returns_state_dir_unchanged_for_canonical_path(self, tmp_path):
        """A canonical scoped path is not redirected."""
        repo_root = tmp_path
        canonical_state_dir = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-42"
        canonical_state_dir.mkdir(parents=True)
        with patch("agentic_devtools.state.get_repo_root", return_value=repo_root):
            result = resolve_effective_workflow_state_dir(state_dir=canonical_state_dir, worktree_key="FEATURE-42")
        assert result == canonical_state_dir

    def test_redirects_legacy_root_alias_to_canonical_dir(self, tmp_path):
        """state_dir that aliases the legacy repo-root .agdt path is redirected."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        expected = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-42"
        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
        ):
            result = resolve_effective_workflow_state_dir(state_dir=legacy_dir, worktree_key="FEATURE-42")
        assert result == expected

    def test_redirect_raises_on_invalid_worktree_key(self, tmp_path):
        """Legacy-root redirect raises ValueError when worktree_key is invalid."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
        ):
            with pytest.raises(ValueError, match="valid worktree key"):
                resolve_effective_workflow_state_dir(state_dir=legacy_dir, worktree_key="invalid/key")

    def test_redirect_raises_when_canonical_target_aliases_legacy_db(self, tmp_path):
        """Legacy-root redirect fails closed when canonical target resolves to legacy DB."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        (legacy_dir / "orchestration.db").touch()
        canonical_dir = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-42"
        canonical_dir.parent.mkdir(parents=True, exist_ok=True)
        canonical_dir.symlink_to(legacy_dir, target_is_directory=True)
        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
        ):
            with pytest.raises(ValueError, match="resolved back to the legacy repository-root database path"):
                resolve_effective_workflow_state_dir(state_dir=legacy_dir, worktree_key="FEATURE-42")

    def test_returns_state_dir_unchanged_for_noncanonical_override(self, tmp_path):
        """A non-canonical override path that does not alias the legacy root is kept."""
        repo_root = tmp_path
        custom_dir = tmp_path / "custom" / "state"
        custom_dir.mkdir(parents=True)
        with patch("agentic_devtools.state.get_repo_root", return_value=repo_root):
            result = resolve_effective_workflow_state_dir(state_dir=custom_dir, worktree_key="FEATURE-42")
        assert result == custom_dir
