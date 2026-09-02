"""Tests for resolve_commit_scope in nest/execution.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.nest.execution import resolve_commit_scope
from agentic_devtools.cli.speckit.nest.plan import MigrationPlan
from agentic_devtools.cli.speckit.shared.conflict_check import Move


def _plan_with_roots(root_issues: list[int]) -> MigrationPlan:
    """Build a MigrationPlan whose roots property returns the given list."""
    # roots = moved issues - children.  Use single-level moves with no hierarchy
    # so every moved issue is a root.
    moves = [
        Move(
            source=Path(f"/src/{n}"),
            target=Path(f"/dst/{n}"),
            issue_number=n,
        )
        for n in root_issues
    ]
    return MigrationPlan(moves=moves)


class TestResolveCommitScope:
    """Tests for the resolve_commit_scope function."""

    def test_returns_explicit_scope_when_provided(self) -> None:
        """Test that an explicit scope overrides plan inference and is wrapped in a list."""
        plan = _plan_with_roots([10, 20])
        assert resolve_commit_scope(plan, explicit_scope=99) == [99]

    def test_infers_scope_from_single_root(self) -> None:
        """Test that a single-root plan yields that root wrapped in a list."""
        plan = _plan_with_roots([42])
        assert resolve_commit_scope(plan) == [42]

    def test_raises_when_plan_has_no_roots(self) -> None:
        """Test that an empty plan raises ValueError when no explicit scope is given."""
        plan = MigrationPlan()
        with pytest.raises(ValueError, match="no hierarchy roots"):
            resolve_commit_scope(plan)

    def test_returns_all_roots_for_multi_root_plan(self) -> None:
        """Test that a multi-root unscoped plan returns all roots sorted."""
        plan = _plan_with_roots([20, 10])
        assert resolve_commit_scope(plan) == [10, 20]

    def test_infers_scope_from_existing_root_in_partial_migration(self) -> None:
        """Test that a partial migration with an already-nested root yields that root."""
        # In a partial migration specs/10/ already exists and flat issue 20 moves there.
        # plan.roots would be empty (20 is a child in hierarchy_files), but
        # existing_root_issues={10} is set by compute_migration_plan.
        from agentic_devtools.cli.speckit.nest.discovery import ChildRef

        plan = MigrationPlan(existing_root_issues={10})
        move = Move(source=Path("/src/20-foo"), target=Path("/dst/10/20"), issue_number=20)
        plan.moves = [move]
        plan.hierarchy_files = {"/dst/10": [ChildRef(number=20, title="child")]}
        assert resolve_commit_scope(plan) == [10]
