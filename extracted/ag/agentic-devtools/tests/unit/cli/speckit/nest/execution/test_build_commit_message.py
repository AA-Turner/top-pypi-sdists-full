"""Tests for build_commit_message in nest/execution.py."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.nest.execution import build_commit_message


class TestBuildCommitMessage:
    """Tests for the build_commit_message function."""

    def test_raises_when_roots_is_empty(self) -> None:
        """Test that an empty roots list raises ValueError."""
        with pytest.raises(ValueError, match="non-empty list"):
            build_commit_message([], 3)

    def test_raises_when_scope_is_zero(self) -> None:
        """Test that a root value of 0 raises ValueError."""
        with pytest.raises(ValueError, match="scope must be a positive issue number"):
            build_commit_message([0], 3)

    def test_raises_when_scope_is_negative(self) -> None:
        """Test that a negative root value raises ValueError."""
        with pytest.raises(ValueError, match="scope must be a positive issue number"):
            build_commit_message([-5], 3)

    def test_raises_when_move_count_is_negative(self) -> None:
        """Test that a negative move_count raises ValueError."""
        with pytest.raises(ValueError, match="move_count must be non-negative"):
            build_commit_message([42], -1)

    def test_returns_conventional_commit_message_single_root(self) -> None:
        """Test that a single-root call returns a commit message containing the scope and count."""
        message = build_commit_message([42], 3)
        assert "refactor" in message
        assert "#42" in message
        assert "3" in message

    def test_allows_zero_move_count(self) -> None:
        """Test that move_count=0 is valid."""
        message = build_commit_message([1], 0)
        assert "#1" in message

    def test_describes_hierarchy_only_changes_when_no_specs_move(self) -> None:
        """Zero moves produce a hierarchy-materialization commit description."""
        message = build_commit_message([1], 0)
        assert "materialize nested hierarchy for 1 root" in message
        assert "migrate 0 flat specs" not in message

    def test_pluralizes_root_count_for_multi_root_hierarchy_only_changes(self) -> None:
        """Hierarchy-only descriptions pluralize the root count when needed."""
        message = build_commit_message([10, 20], 0)

        assert "materialize nested hierarchy for 2 roots" in message

    def test_multi_root_includes_all_roots_in_scope_and_footer(self) -> None:
        """Test that a multi-root call includes all root refs in the scope and footer."""
        message = build_commit_message([10, 20], 5)
        assert "#10, #20" in message
        assert "#10 / #20" not in message
        assert "refactor" in message
        assert "5" in message
