"""Tests for _compute_plan_fingerprint in nest/commands.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.nest.commands import _compute_plan_fingerprint
from agentic_devtools.cli.speckit.nest.crossref import CrossRefUpdate
from agentic_devtools.cli.speckit.nest.discovery import ChildRef, FlatSpec
from agentic_devtools.cli.speckit.nest.plan import MigrationPlan
from agentic_devtools.cli.speckit.shared.conflict_check import Move


def _make_plan(
    *,
    moves: list[Move] | None = None,
    remaining_flat: list[FlatSpec] | None = None,
    warnings: list[str] | None = None,
) -> MigrationPlan:
    plan = MigrationPlan()
    if moves:
        plan.moves = moves
    if remaining_flat:
        plan.remaining_flat = remaining_flat
    if warnings:
        plan.warnings = warnings
    return plan


class TestComputePlanFingerprint:
    """Tests for the _compute_plan_fingerprint helper."""

    def test_returns_a_64_character_hex_string(self) -> None:
        """The fingerprint is a SHA-256 hex digest (64 chars)."""
        plan = _make_plan()
        result = _compute_plan_fingerprint(plan, [])

        assert isinstance(result, str)
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_is_deterministic_for_same_plan(self) -> None:
        """Two calls with identical plans return the same fingerprint."""
        move = Move(source=Path("specs/100-feat"), target=Path("specs/200/100-feat"), issue_number=100)
        plan = _make_plan(moves=[move], warnings=["warn"])

        fp1 = _compute_plan_fingerprint(plan, [])
        fp2 = _compute_plan_fingerprint(plan, [])

        assert fp1 == fp2

    def test_different_moves_produce_different_fingerprints(self) -> None:
        """Changing a move source changes the fingerprint."""
        move_a = Move(source=Path("specs/100-feat"), target=Path("specs/200/100-feat"), issue_number=100)
        move_b = Move(source=Path("specs/101-feat"), target=Path("specs/200/100-feat"), issue_number=100)

        fp_a = _compute_plan_fingerprint(_make_plan(moves=[move_a]), [])
        fp_b = _compute_plan_fingerprint(_make_plan(moves=[move_b]), [])

        assert fp_a != fp_b

    def test_different_target_produces_different_fingerprint(self) -> None:
        """Changing a move target changes the fingerprint."""
        move_a = Move(source=Path("specs/100-feat"), target=Path("specs/200/100-feat"), issue_number=100)
        move_b = Move(source=Path("specs/100-feat"), target=Path("specs/300/100-feat"), issue_number=100)

        fp_a = _compute_plan_fingerprint(_make_plan(moves=[move_a]), [])
        fp_b = _compute_plan_fingerprint(_make_plan(moves=[move_b]), [])

        assert fp_a != fp_b

    def test_different_crossref_updates_produce_different_fingerprints(self) -> None:
        """A change to the crossref updates changes the fingerprint."""
        plan = _make_plan()
        update_a = CrossRefUpdate(
            file_path=Path("specs/100/spec.md"), old_ref="../100-feat/", new_ref="../", line_number=5
        )
        update_b = CrossRefUpdate(
            file_path=Path("specs/200/spec.md"), old_ref="../100-feat/", new_ref="../", line_number=5
        )

        fp_a = _compute_plan_fingerprint(plan, [update_a])
        fp_b = _compute_plan_fingerprint(plan, [update_b])

        assert fp_a != fp_b

    def test_move_order_does_not_affect_fingerprint(self) -> None:
        """Moves are sorted before hashing so order does not matter."""
        move1 = Move(source=Path("specs/100-a"), target=Path("specs/200/100-a"), issue_number=100)
        move2 = Move(source=Path("specs/101-b"), target=Path("specs/200/101-b"), issue_number=101)

        fp_ab = _compute_plan_fingerprint(_make_plan(moves=[move1, move2]), [])
        fp_ba = _compute_plan_fingerprint(_make_plan(moves=[move2, move1]), [])

        assert fp_ab == fp_ba

    def test_remaining_flat_change_produces_different_fingerprint(self) -> None:
        """A different remaining_flat list produces a different fingerprint."""
        flat_a = FlatSpec(issue_number=42, slug="42-feat", path=Path("specs/42-feat"))
        flat_b = FlatSpec(issue_number=43, slug="43-feat", path=Path("specs/43-feat"))

        fp_a = _compute_plan_fingerprint(_make_plan(remaining_flat=[flat_a]), [])
        fp_b = _compute_plan_fingerprint(_make_plan(remaining_flat=[flat_b]), [])

        assert fp_a != fp_b

    def test_warnings_change_produces_different_fingerprint(self) -> None:
        """Adding a warning changes the fingerprint."""
        fp_no_warn = _compute_plan_fingerprint(_make_plan(), [])
        fp_warn = _compute_plan_fingerprint(_make_plan(warnings=["cycle detected"]), [])

        assert fp_no_warn != fp_warn

    def test_hierarchy_child_order_change_produces_different_fingerprint(self) -> None:
        """Hierarchy child order affects the fingerprint because writes preserve it."""
        child_a = ChildRef(number=100, title="A", order=1)
        child_b = ChildRef(number=101, title="B", order=1)
        plan_ab = _make_plan()
        plan_ab.hierarchy_files = {"specs/42": [child_a, child_b]}
        plan_ba = _make_plan()
        plan_ba.hierarchy_files = {"specs/42": [child_b, child_a]}

        assert _compute_plan_fingerprint(plan_ab, []) != _compute_plan_fingerprint(plan_ba, [])
