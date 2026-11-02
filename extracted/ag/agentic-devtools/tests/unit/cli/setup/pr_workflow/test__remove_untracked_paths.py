"""Tests for _remove_untracked_paths."""

from unittest.mock import patch

from agentic_devtools.cli.setup.pr_workflow import _remove_untracked_paths


class TestRemoveUntrackedPaths:
    """Tests for _remove_untracked_paths."""

    def test_removes_directories_and_files(self) -> None:
        """Removes untracked paths in depth-first order and returns True."""
        with (
            patch("agentic_devtools.cli.setup.pr_workflow.Path.is_dir", side_effect=[True, False]),
            patch("agentic_devtools.cli.setup.pr_workflow.Path.is_symlink", return_value=False),
            patch("agentic_devtools.cli.setup.pr_workflow.Path.exists", return_value=True),
            patch("agentic_devtools.cli.setup.pr_workflow.Path.unlink") as mock_unlink,
            patch("agentic_devtools.cli.setup.pr_workflow.shutil.rmtree") as mock_rmtree,
        ):
            assert _remove_untracked_paths({"a/b", "a/c.txt"}) is True
            assert mock_rmtree.called
            assert mock_unlink.called

    def test_returns_false_on_os_error(self) -> None:
        """Returns False when filesystem removal fails."""
        with (
            patch("agentic_devtools.cli.setup.pr_workflow.Path.is_dir", return_value=False),
            patch("agentic_devtools.cli.setup.pr_workflow.Path.is_symlink", return_value=False),
            patch("agentic_devtools.cli.setup.pr_workflow.Path.exists", return_value=True),
            patch("agentic_devtools.cli.setup.pr_workflow.Path.unlink", side_effect=OSError("denied")),
        ):
            assert _remove_untracked_paths({"a/d.txt"}) is False
