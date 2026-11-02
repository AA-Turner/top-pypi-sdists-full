"""Tests for get_ancestors in nest/plan.py."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.nest.plan import get_ancestors


class TestGetAncestors:
    """Tests for the public get_ancestors function."""

    def test_returns_root_first_ancestor_chain(self) -> None:
        """Ancestors are returned in root-first order (with max_depth large enough)."""
        canonical_parent = {4: 3, 3: 2, 2: 1, 1: None}
        assert get_ancestors(canonical_parent, 4, max_depth=3) == [1, 2, 3]

    def test_returns_empty_for_root_issue(self) -> None:
        """A root issue (parent=None) has an empty ancestor chain."""
        assert get_ancestors({1: None}, 1) == []

    def test_returns_none_when_chain_exceeds_max_depth(self) -> None:
        """Returns None when the ancestor chain length exceeds max_depth."""
        canonical_parent = {4: 3, 3: 2, 2: 1, 1: None}
        # max_depth=2 allows at most 2 ancestors; chain [1,2,3] is length 3.
        assert get_ancestors(canonical_parent, 4, max_depth=2) is None

    def test_returns_chain_at_exact_max_depth(self) -> None:
        """Returns the chain when its length exactly equals max_depth."""
        canonical_parent = {3: 2, 2: 1, 1: None}
        # max_depth=2: chain [1, 2] has length 2 — exactly at cap.
        assert get_ancestors(canonical_parent, 3, max_depth=2) == [1, 2]

    def test_raises_for_negative_max_depth(self) -> None:
        """max_depth < 0 raises ValueError."""
        with pytest.raises(ValueError, match="max_depth"):
            get_ancestors({}, 1, max_depth=-1)

    def test_breaks_on_cycle_in_canonical_parent(self) -> None:
        """A cycle in canonical_parent is broken by the seen-set guard."""
        canonical_parent: dict[int, int | None] = {1: 2, 2: 1}
        # Should not loop forever; returns None because len grows past max_depth,
        # or an incomplete chain if the cycle is broken early.
        result = get_ancestors(canonical_parent, 1, max_depth=10)
        # The important thing is that it terminates (no infinite loop).
        assert result is None or isinstance(result, list)

    def test_issue_not_in_canonical_parent_has_no_ancestors(self) -> None:
        """An issue absent from canonical_parent returns an empty chain."""
        assert get_ancestors({}, 42) == []
