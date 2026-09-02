"""Tests for _contains_windows_cmd_metacharacters."""

import pytest

from agentic_devtools.cli.workflows.worktree_setup import _contains_windows_cmd_metacharacters


class TestContainsWindowsCmdMetacharacters:
    """Tests for the _contains_windows_cmd_metacharacters helper."""

    @pytest.mark.parametrize(
        "path",
        [
            "/repos/project&name",
            "/repos/project|name",
            "/repos/project<name",
            "/repos/project>name",
            "/repos/project^name",
            "/repos/project%name",
            "/repos/project!name",
            "/repos/project\nname",
            "/repos/project\rname",
        ],
    )
    def test_returns_true_for_metacharacter_paths(self, path):
        """Returns True when path contains any cmd.exe metacharacter."""
        assert _contains_windows_cmd_metacharacters(path) is True

    def test_returns_false_for_clean_path(self):
        """Returns False when path contains no cmd.exe metacharacters."""
        assert _contains_windows_cmd_metacharacters("/repos/normal-project/workspace") is False

    def test_returns_false_for_empty_string(self):
        """Returns False for an empty path."""
        assert _contains_windows_cmd_metacharacters("") is False
