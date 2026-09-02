"""Unit tests for :func:`format_migration_plan`."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.nest.discovery import ChildRef, FlatSpec
from agentic_devtools.cli.speckit.nest.display import format_migration_plan
from agentic_devtools.cli.speckit.nest.plan import MigrationPlan
from agentic_devtools.cli.speckit.shared.conflict_check import Move


def _move(number: int, slug: str, target: str) -> Move:
    """Build a :class:`Move` for the given issue number."""
    return Move(source=Path("specs") / f"{number}-{slug}", target=Path(target), issue_number=number)


class TestFormatMigrationPlan:
    """Behavior of the terminal plan renderer."""

    def test_renders_header(self) -> None:
        """Every rendering carries the command banner."""
        output = format_migration_plan(MigrationPlan())

        assert "SPECKIT NEST — Migration Plan" in output

    def test_reports_when_no_moves_are_needed(self) -> None:
        """An empty plan states that no moves are needed."""
        output = format_migration_plan(MigrationPlan())

        assert "No directory moves needed." in output

    def test_renders_moves_with_source_and_target(self) -> None:
        """Each move renders its source directory name and target path."""
        plan = MigrationPlan(moves=[_move(1865, "nest", "specs/1865")])

        output = format_migration_plan(plan)

        assert "Directory Moves (1):" in output
        assert "1865-nest/ → specs/1865/" in output

    def test_renders_hierarchy_files_with_child_titles(self) -> None:
        """hierarchy.yml previews list each child's number and exact title."""
        plan = MigrationPlan(
            hierarchy_files={"specs/1865": [ChildRef(number=42, title="Child spec", order=0)]},
        )

        output = format_migration_plan(plan)

        assert "hierarchy.yml Files to Create (1):" in output
        assert "specs/1865/hierarchy.yml:" in output
        assert "- #42 Child spec" in output

    def test_renders_remaining_flat_specs(self) -> None:
        """Specs that stay flat are listed with a stays-in-place note."""
        plan = MigrationPlan(
            remaining_flat=[FlatSpec(path=Path("specs/77-standalone"), issue_number=77, slug="standalone")],
        )

        output = format_migration_plan(plan)

        assert "Specs Remaining Flat (1):" in output
        assert "77-standalone/ (stays in place)" in output

    def test_renders_multi_parent_selection_with_candidates(self) -> None:
        """Multi-parent resolutions name every candidate and the selection."""
        plan = MigrationPlan(
            multi_parent_selections={42: 10},
            multi_parent_candidates={42: [10, 20]},
        )

        output = format_migration_plan(plan)

        assert "Multi-Parent Selections:" in output
        assert "Issue #42 candidates: #10, #20 → selected #10 (lowest-numbered)" in output

    def test_falls_back_to_selected_parent_when_candidates_missing(self) -> None:
        """A selection without a recorded candidate list still renders."""
        plan = MigrationPlan(multi_parent_selections={42: 10})

        output = format_migration_plan(plan)

        assert "Issue #42 candidates: #10 → selected #10 (lowest-numbered)" in output

    def test_renders_excluded_cycles(self) -> None:
        """Cyclic groups are reported as excluded."""
        plan = MigrationPlan(excluded_cycles=[{2, 1}])

        output = format_migration_plan(plan)

        assert "Excluded Cyclic Groups:" in output
        assert "Cycle detected: [1, 2]" in output

    def test_renders_warning_block(self) -> None:
        """Plan warnings are rendered through the shared warning block."""
        plan = MigrationPlan(warnings=["issue #42 not found"])

        output = format_migration_plan(plan)

        assert "Warnings:" in output
        assert "⚠ issue #42 not found" in output

    def test_omits_warning_block_when_there_are_no_warnings(self) -> None:
        """No warning header is emitted for a warning-free plan."""
        output = format_migration_plan(MigrationPlan())

        assert "Warnings:" not in output
