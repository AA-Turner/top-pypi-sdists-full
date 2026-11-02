"""Tests for the PRTreeState dataclass."""

import dataclasses

import pytest

from agentic_devtools.cli.ci.models import PRTreeState


class TestPRTreeState:
    """Tests for the PRTreeState dataclass."""

    def test_fields(self) -> None:
        state = PRTreeState(merge_base_sha="base", merge_base_tree_sha="t1", head_tree_sha="t2", head_sha="head")
        assert state.merge_base_sha == "base"
        assert state.merge_base_tree_sha == "t1"
        assert state.head_tree_sha == "t2"
        assert state.head_sha == "head"

    def test_tree_identical_is_true_for_matching_trees(self) -> None:
        state = PRTreeState(merge_base_sha="base", merge_base_tree_sha="tree", head_tree_sha="tree")
        assert state.tree_identical is True

    def test_tree_identical_is_false_for_differing_trees(self) -> None:
        state = PRTreeState(merge_base_sha="base", merge_base_tree_sha="tree", head_tree_sha="other")
        assert state.tree_identical is False

    def test_tree_identical_is_false_when_trees_did_not_resolve(self) -> None:
        """Two unresolved (empty) trees must never be treated as identical."""
        state = PRTreeState(merge_base_sha="base", merge_base_tree_sha="", head_tree_sha="")
        assert state.tree_identical is False

    def test_is_frozen(self) -> None:
        state = PRTreeState(merge_base_sha="base", merge_base_tree_sha="t", head_tree_sha="t")
        with pytest.raises(dataclasses.FrozenInstanceError):
            state.merge_base_sha = "other"  # type: ignore[misc]
