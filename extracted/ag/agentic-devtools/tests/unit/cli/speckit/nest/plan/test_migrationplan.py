"""Tests for MigrationPlan dataclass in nest/plan.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.nest.discovery import ChildRef, FlatSpec
from agentic_devtools.cli.speckit.nest.plan import MigrationPlan
from agentic_devtools.cli.speckit.shared.conflict_check import Move


class TestMigrationPlan:
    """Tests for the MigrationPlan dataclass and its properties."""

    def test_defaults_produce_empty_collections(self) -> None:
        """Default-constructed MigrationPlan has all-empty collections."""
        plan = MigrationPlan()
        assert plan.moves == []
        assert plan.hierarchy_files == {}
        assert plan.scope_hierarchy_files is None
        assert plan.excluded_cycles == []
        assert plan.multi_parent_selections == {}
        assert plan.multi_parent_candidates == {}
        assert plan.remaining_flat == []
        assert plan.warnings == []
        assert plan.existing_root_issues == set()

    def test_roots_includes_existing_root_issues_for_partial_migration(self, tmp_path: Path) -> None:
        """roots includes existing_root_issues so partial migrations yield the nested parent."""
        child_ref = ChildRef(number=20, title="child")
        plan = MigrationPlan(
            moves=[
                Move(source=tmp_path / "20-foo", target=tmp_path / "10" / "20", issue_number=20),
            ],
            hierarchy_files={str(tmp_path / "10"): [child_ref]},
            existing_root_issues={10},
        )
        # Issue 20 is a child; 10 is an existing-target root → root is [10].
        assert plan.roots == [10]

    def test_roots_returns_moved_issues_not_referenced_as_children(self, tmp_path: Path) -> None:
        """roots property returns moved issues that are not children of any other moved issue."""
        child_ref = ChildRef(number=101, title="child")
        plan = MigrationPlan(
            moves=[
                Move(source=tmp_path / "100-a", target=tmp_path / "100", issue_number=100),
                Move(source=tmp_path / "101-b", target=tmp_path / "100" / "101", issue_number=101),
            ],
            hierarchy_files={str(tmp_path / "100"): [child_ref]},
        )
        # Issue 101 is a child → only 100 is a root.
        assert plan.roots == [100]

    def test_roots_returns_empty_when_no_moves(self) -> None:
        """roots is empty when there are no moves."""
        assert MigrationPlan().roots == []

    def test_roots_uses_full_relationships_when_hierarchy_writes_are_filtered(self, tmp_path: Path) -> None:
        """Filtered hierarchy writes do not make an existing parent look like a second root."""
        child_ref = ChildRef(number=20, title="child")
        plan = MigrationPlan(
            moves=[
                Move(source=tmp_path / "20-foo", target=tmp_path / "10" / "20", issue_number=20),
            ],
            hierarchy_files={},
            scope_hierarchy_files={str(tmp_path / "10"): [child_ref]},
            existing_root_issues={10},
        )

        assert plan.roots == [10]

    def test_roots_excludes_nested_existing_children(self, tmp_path: Path) -> None:
        """Only the top-level existing issue is a root in a multi-level hierarchy."""
        plan = MigrationPlan(
            moves=[
                Move(source=tmp_path / "300-flat", target=tmp_path / "100" / "200" / "300", issue_number=300),
            ],
            hierarchy_files={
                str(tmp_path / "100"): [ChildRef(number=200, title="middle")],
                str(tmp_path / "100" / "200"): [ChildRef(number=300, title="leaf")],
            },
            existing_root_issues={100, 200},
        )

        assert plan.roots == [100]

    def test_roots_returns_all_when_no_hierarchy_files(self, tmp_path: Path) -> None:
        """All moved issues are roots when hierarchy_files is empty."""
        plan = MigrationPlan(
            moves=[
                Move(source=tmp_path / "1-a", target=tmp_path / "1", issue_number=1),
                Move(source=tmp_path / "2-b", target=tmp_path / "2", issue_number=2),
            ]
        )
        assert plan.roots == [1, 2]

    def test_remaining_flat_accepts_flat_spec(self, tmp_path: Path) -> None:
        """remaining_flat stores FlatSpec objects."""
        spec = FlatSpec(issue_number=99, path=tmp_path / "99-x", slug="x")
        plan = MigrationPlan(remaining_flat=[spec])
        assert plan.remaining_flat[0].issue_number == 99
