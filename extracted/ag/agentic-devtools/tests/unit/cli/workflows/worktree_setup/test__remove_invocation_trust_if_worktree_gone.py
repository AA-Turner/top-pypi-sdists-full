"""Tests for _remove_invocation_trust_if_worktree_gone."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.worktree_setup import (
    WorktreeSetupResult,
    _remove_invocation_trust_if_worktree_gone,
)


class TestRemoveInvocationTrustIfWorktreeGone:
    """Tests for _remove_invocation_trust_if_worktree_gone."""

    def test_removes_trust_when_owned_and_path_absent(self, tmp_path):
        """Calls remove_trusted_folder when this invocation added trust and the path is gone."""
        result = WorktreeSetupResult(
            success=False,
            worktree_path=str(tmp_path / "gone"),
            branch_name="feature/KEY-1",
            copilot_trust_added=True,
        )
        with patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder") as mock_remove:
            _remove_invocation_trust_if_worktree_gone(result)
        mock_remove.assert_called_once_with(str(tmp_path / "gone"))

    def test_skips_removal_when_not_owned(self, tmp_path):
        """Does not call remove_trusted_folder when this invocation did not add trust."""
        result = WorktreeSetupResult(
            success=False,
            worktree_path=str(tmp_path / "gone"),
            branch_name="feature/KEY-1",
            copilot_trust_added=False,
        )
        with patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder") as mock_remove:
            _remove_invocation_trust_if_worktree_gone(result)
        mock_remove.assert_not_called()

    def test_skips_removal_when_path_still_present(self, tmp_path):
        """Does not call remove_trusted_folder when the worktree path still exists."""
        target = tmp_path / "worktree"
        target.mkdir()
        result = WorktreeSetupResult(
            success=False,
            worktree_path=str(target),
            branch_name="feature/KEY-1",
            copilot_trust_added=True,
        )
        with patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder") as mock_remove:
            _remove_invocation_trust_if_worktree_gone(result)
        mock_remove.assert_not_called()
