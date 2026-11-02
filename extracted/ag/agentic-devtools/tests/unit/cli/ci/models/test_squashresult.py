"""Tests for the SquashResult model."""

from agentic_devtools.cli.ci.models import SquashResult


class TestSquashResult:
    """Tests for SquashResult and its ``tree_preserved`` property."""

    def test_defaults_are_empty_and_not_preserved(self) -> None:
        result = SquashResult()
        assert result.before_tree == ""
        assert result.after_tree == ""
        assert result.after_sha == ""
        assert result.tree_preserved is False

    def test_tree_preserved_true_when_trees_equal_and_non_empty(self) -> None:
        result = SquashResult(before_tree="tree1", after_tree="tree1")
        assert result.tree_preserved is True

    def test_tree_preserved_false_when_trees_differ(self) -> None:
        result = SquashResult(before_tree="tree1", after_tree="tree2")
        assert result.tree_preserved is False

    def test_tree_preserved_false_when_before_tree_empty(self) -> None:
        """An unresolved before-tree cannot prove preservation even if after-tree matches."""
        result = SquashResult(before_tree="", after_tree="")
        assert result.tree_preserved is False

    def test_after_sha_stored_and_accessible(self) -> None:
        """after_sha records the post-squash commit SHA for the runner's SHA-binding check."""
        result = SquashResult(before_tree="tree1", after_tree="tree1", after_sha="abc123")
        assert result.after_sha == "abc123"
        assert result.tree_preserved is True
