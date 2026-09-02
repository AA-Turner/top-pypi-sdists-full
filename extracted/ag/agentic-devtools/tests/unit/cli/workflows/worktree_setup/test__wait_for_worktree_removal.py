"""Tests for _wait_for_worktree_removal."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.worktree_setup import _wait_for_worktree_removal


class TestWaitForWorktreeRemoval:
    """Tests for _wait_for_worktree_removal."""

    def test_returns_true_immediately_when_path_absent(self, tmp_path):
        """Returns True without sleeping when the path does not exist."""
        absent = str(tmp_path / "gone")
        with patch("time.sleep") as mock_sleep:
            result = _wait_for_worktree_removal(absent)
        assert result is True
        mock_sleep.assert_not_called()

    def test_returns_true_when_path_disappears_during_wait(self, tmp_path):
        """Returns True after the path is removed while polling."""
        import threading
        import time

        target = tmp_path / "worktree"
        target.mkdir()

        def remove_after_delay():
            time.sleep(0.05)
            target.rmdir()

        thread = threading.Thread(target=remove_after_delay)
        thread.start()
        result = _wait_for_worktree_removal(str(target))
        thread.join()
        assert result is True

    def test_returns_false_when_path_remains_through_deadline(self, tmp_path):
        """Returns False when the path never disappears within the timeout."""
        target = tmp_path / "worktree"
        target.mkdir()
        with patch("time.monotonic", side_effect=[0.0, 11.0]):
            result = _wait_for_worktree_removal(str(target))
        assert result is False
