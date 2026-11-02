"""Tests for _is_already_trusted."""

from agentic_devtools.cli.copilot.trust import _is_already_trusted, _normalize_path


class TestIsAlreadyTrusted:
    """Tests for _is_already_trusted."""

    def test_exact_match_without_subtree(self, tmp_path):
        """An exact entry counts when subtree_trust is False."""
        target = str(tmp_path)
        assert _is_already_trusted([_normalize_path(target)], target, subtree_trust=False) is True

    def test_ancestor_not_counted_without_subtree(self, tmp_path):
        """An ancestor does NOT count when subtree_trust is False."""
        folders = [_normalize_path(str(tmp_path))]
        assert _is_already_trusted(folders, str(tmp_path / "a"), subtree_trust=False) is False

    def test_ancestor_counted_with_subtree(self, tmp_path):
        """An ancestor counts when subtree_trust is True."""
        folders = [_normalize_path(str(tmp_path))]
        assert _is_already_trusted(folders, str(tmp_path / "a"), subtree_trust=True) is True

    def test_subtree_no_match_returns_false(self, tmp_path):
        """Subtree mode with no covering entry returns False."""
        folders = [_normalize_path(str(tmp_path / "other"))]
        assert _is_already_trusted(folders, str(tmp_path / "target"), subtree_trust=True) is False

    def test_non_string_entries_skipped(self, tmp_path):
        """Non-string entries are ignored."""
        target = str(tmp_path)
        folders = [123, None, _normalize_path(target)]
        assert _is_already_trusted(folders, target, subtree_trust=False) is True

    def test_empty_returns_false(self, tmp_path):
        """An empty list is never trusted."""
        assert _is_already_trusted([], str(tmp_path), subtree_trust=True) is False
