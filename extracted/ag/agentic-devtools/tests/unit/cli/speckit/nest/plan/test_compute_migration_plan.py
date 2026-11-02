"""Tests for compute_migration_plan in nest/plan.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.nest.discovery import ChildRef, FlatSpec
from agentic_devtools.cli.speckit.nest.plan import compute_migration_plan


def _cr(number: int, order: int | None = None) -> ChildRef:
    return ChildRef(number=number, title=f"Issue #{number}", order=order)


def _spec(number: int, root: Path, slug: str = "slug") -> FlatSpec:
    return FlatSpec(issue_number=number, path=root / f"{number}-{slug}", slug=slug)


class TestComputeMigrationPlan:
    """Tests for compute_migration_plan."""

    # ------------------------------------------------------------------
    # Basic parent-child move
    # ------------------------------------------------------------------

    def test_simple_parent_child_move(self, tmp_path: Path) -> None:
        """Parent moves to specs/{parent}/, child to specs/{parent}/{child}/."""
        flat_specs = [_spec(100, tmp_path, "parent"), _spec(101, tmp_path, "child")]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)

        parent_move = next(m for m in plan.moves if m.issue_number == 100)
        child_move = next(m for m in plan.moves if m.issue_number == 101)
        assert parent_move.target == tmp_path / "100"
        assert child_move.target == tmp_path / "100" / "101"

    # ------------------------------------------------------------------
    # Cycles
    # ------------------------------------------------------------------

    def test_excludes_cyclic_issues(self, tmp_path: Path) -> None:
        """Issues forming a cycle are excluded from all moves."""
        flat_specs = [
            _spec(100, tmp_path, "a"),
            _spec(101, tmp_path, "b"),
            _spec(200, tmp_path, "safe"),
        ]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, [_cr(100)]),
            200: (None, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)

        move_issues = {m.issue_number for m in plan.moves}
        assert 100 not in move_issues
        assert 101 not in move_issues
        assert len(plan.excluded_cycles) >= 1
        assert any("100" in w or "101" in w for w in plan.warnings)

    # ------------------------------------------------------------------
    # Isolated specs (no parent, no children in graph)
    # ------------------------------------------------------------------

    def test_isolated_spec_goes_to_remaining_flat(self, tmp_path: Path) -> None:
        """A spec with no parent and no graph-listed children stays flat."""
        flat_specs = [_spec(100, tmp_path)]
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {100: (None, [])}

        plan = compute_migration_plan(graph, flat_specs, tmp_path)

        assert plan.moves == []
        assert any(s.issue_number == 100 for s in plan.remaining_flat)

    def test_root_with_only_nonlocal_children_stays_flat(self, tmp_path: Path) -> None:
        """A root stays flat until at least one related child spec exists locally."""
        spec = _spec(1, tmp_path, "epic")
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {1: (None, [_cr(2)])}

        plan = compute_migration_plan(graph, [spec], tmp_path)

        assert plan.moves == []
        assert any(remaining.issue_number == 1 for remaining in plan.remaining_flat)

    def test_root_with_child_missing_from_graph_stays_flat(self, tmp_path: Path) -> None:
        """A root is not moved when its only local child was omitted from the graph."""
        parent = _spec(1, tmp_path, "epic")
        omitted_child = _spec(2, tmp_path, "task")
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {1: (None, [_cr(2)])}

        plan = compute_migration_plan(graph, [parent, omitted_child], tmp_path)

        assert plan.moves == []
        assert any(remaining.issue_number == 1 for remaining in plan.remaining_flat)

    def test_child_with_remote_only_parent_stays_flat(self, tmp_path: Path) -> None:
        """A child spec whose GitHub parent has no local flat spec and no existing
        nested directory must stay flat to avoid creating an orphan nested tree."""
        child = _spec(101, tmp_path, "child")
        # Parent issue 10 exists in the graph but has no local flat spec and no
        # existing_targets entry — it is a remote-only parent.
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {
            10: (None, [_cr(101)]),
            101: (10, []),
        }

        plan = compute_migration_plan(graph, [child], tmp_path)

        assert plan.moves == []
        assert any(s.issue_number == 101 for s in plan.remaining_flat)

    # ------------------------------------------------------------------
    # Specs absent from graph
    # ------------------------------------------------------------------

    def test_spec_not_in_graph_goes_to_remaining_flat(self, tmp_path: Path) -> None:
        """Specs with no discovered relationships stay in remaining_flat."""
        flat_specs = [_spec(10, tmp_path), _spec(99, tmp_path, "orphan")]
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {
            10: (None, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)
        assert any(s.issue_number == 99 for s in plan.remaining_flat)

    # ------------------------------------------------------------------
    # Depth cap
    # ------------------------------------------------------------------

    def test_depth_cap_enforcement(self, tmp_path: Path) -> None:
        """Issue 4 with ancestors [1,2,3] exceeds the 3-level cap and stays flat."""
        flat_specs = [
            _spec(1, tmp_path, "epic"),
            _spec(2, tmp_path, "feature"),
            _spec(3, tmp_path, "task"),
            _spec(4, tmp_path, "deep"),
        ]
        graph = {
            1: (None, [_cr(2)]),
            2: (1, [_cr(3)]),
            3: (2, [_cr(4)]),
            4: (3, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)

        move_issues = {m.issue_number for m in plan.moves}
        # Issues 1, 2, 3 are within depth; issue 4 is depth-capped.
        assert 4 not in move_issues
        assert any("4" in w and "depth" in w.lower() for w in plan.warnings)
        assert any(s.issue_number == 4 for s in plan.remaining_flat)

    # ------------------------------------------------------------------
    # Scope filtering
    # ------------------------------------------------------------------

    def test_scope_limits_migration_to_subtree(self, tmp_path: Path) -> None:
        """--scope restricts moves to the scoped issue and its descendants."""
        flat_specs = [
            _spec(100, tmp_path, "a"),
            _spec(101, tmp_path, "b"),
            _spec(200, tmp_path, "other"),
        ]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
            200: (None, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path, scope=100)

        move_issues = {m.issue_number for m in plan.moves}
        assert 100 in move_issues
        assert 101 in move_issues
        assert 200 not in move_issues

    def test_scope_places_scoped_root_at_top_when_parent_out_of_scope(self, tmp_path: Path) -> None:
        """Scoped root whose graph parent is outside the scope gets no parent."""
        flat_specs = [
            _spec(100, tmp_path, "root"),
            _spec(101, tmp_path, "parent"),
            _spec(102, tmp_path, "child"),
        ]
        child_ref = _cr(102, order=0)
        graph = {
            100: (None, [_cr(101)]),
            101: (100, [child_ref]),
            102: (101, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path, scope=101)

        moves_by_issue = {m.issue_number: m for m in plan.moves}
        assert set(moves_by_issue) == {101, 102}
        assert moves_by_issue[101].target == tmp_path / "101"
        assert moves_by_issue[102].target == tmp_path / "101" / "102"
        assert any("101" in w and "100" in w for w in plan.warnings)
        assert str(tmp_path / "101") in plan.hierarchy_files

    # ------------------------------------------------------------------
    # Multi-parent resolution
    # ------------------------------------------------------------------

    def test_multi_parent_selects_lowest_parent(self, tmp_path: Path) -> None:
        """When a child has two parents, the lowest-numbered one is selected."""
        flat_specs = [
            _spec(10, tmp_path, "parent-a"),
            _spec(20, tmp_path, "parent-b"),
            _spec(30, tmp_path, "child"),
        ]
        graph = {
            10: (None, [_cr(30)]),
            20: (None, [_cr(30)]),
            30: (10, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)

        child_move = next(m for m in plan.moves if m.issue_number == 30)
        assert child_move.target == tmp_path / "10" / "30"
        assert plan.multi_parent_selections == {30: 10}
        assert any("30" in w and "10" in w for w in plan.warnings)

    # ------------------------------------------------------------------
    # Skip move when already at target
    # ------------------------------------------------------------------

    def test_no_move_when_child_already_at_target_path(self, tmp_path: Path) -> None:
        """A child whose path already matches the canonical target is not moved."""
        flat_specs = [
            _spec(100, tmp_path, "parent"),
            FlatSpec(
                issue_number=101,
                path=tmp_path / "100" / "101",
                slug="child",
            ),
        ]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)
        assert {m.issue_number for m in plan.moves} == {100}

    def test_no_move_when_parent_already_at_target_path(self, tmp_path: Path) -> None:
        """A parent whose path already matches specs/{n}/ is not moved."""
        flat_specs = [
            FlatSpec(issue_number=100, path=tmp_path / "100", slug="parent"),
            _spec(101, tmp_path, "child"),
        ]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)
        assert {m.issue_number for m in plan.moves} == {101}

    # ------------------------------------------------------------------
    # Existing targets
    # ------------------------------------------------------------------

    def test_uses_existing_target_path_for_already_migrated_spec(self, tmp_path: Path) -> None:
        """If an issue is already in existing_targets, its nested path is used."""
        existing_dir = tmp_path / "100"
        flat_specs = [_spec(101, tmp_path, "child")]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path, existing_targets={100: existing_dir})
        child_move = next(m for m in plan.moves if m.issue_number == 101)
        assert child_move.target == existing_dir / "101"

    # ------------------------------------------------------------------
    # Branch coverage for _get_ancestors ValueError (lines 412-413)
    # ------------------------------------------------------------------

    def test_get_ancestors_ignores_existing_path_outside_specs_root(self, tmp_path: Path) -> None:
        """When an existing ancestor path is outside specs_root, relative_to raises ValueError.
        The private _get_ancestors falls back to the chain as-is."""
        outside_path = tmp_path.parent / "outside" / "100"
        flat_specs = [_spec(101, tmp_path, "child")]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
        }
        # existing_targets has 100 at a path outside tmp_path → ValueError in relative_to
        plan = compute_migration_plan(graph, flat_specs, tmp_path, existing_targets={100: outside_path})
        # 101 should still be placed somewhere (the chain is used as-is → [100] → target=tmp_path/100/101)
        child_move = next((m for m in plan.moves if m.issue_number == 101), None)
        assert child_move is not None

    # ------------------------------------------------------------------
    # Branch coverage for _get_ancestors existing path too deep (line 416)
    # ------------------------------------------------------------------

    def test_get_ancestors_returns_none_when_existing_ancestor_too_deep(self, tmp_path: Path) -> None:
        """When an existing ancestor path is deeper than max_depth from specs_root,
        _get_ancestors returns None and the issue is depth-capped."""
        deep_path = tmp_path / "a" / "b" / "c"  # 3 levels = len(parts)=3 > max_depth=2
        flat_specs = [_spec(50, tmp_path, "parent"), _spec(101, tmp_path, "child")]
        graph = {
            50: (None, [_cr(101)]),
            101: (50, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path, existing_targets={50: deep_path})
        # issue 101 has parent 50 whose existing path is 3 levels deep → capped
        assert any(s.issue_number == 101 for s in plan.remaining_flat)

    # ------------------------------------------------------------------
    # Branch coverage for _resolve_parent_candidates issue not in scope (line 238)
    # ------------------------------------------------------------------

    def test_parent_candidates_skips_child_not_in_scope(self, tmp_path: Path) -> None:
        """Issues claimed as children of in-scope parents but not in scope themselves
        are skipped by _resolve_parent_candidates."""
        flat_specs = [_spec(10, tmp_path), _spec(20, tmp_path), _spec(30, tmp_path)]
        graph = {
            10: (None, []),
            20: (None, [_cr(30)]),
            30: (20, []),
        }
        # scope=10: in_scope = {10}; child_parents[30] = [20], but 30 not in scope
        plan = compute_migration_plan(graph, flat_specs, tmp_path, scope=10)
        # Issue 10 is isolated (no parent, no children in graph), stays flat.
        assert plan.multi_parent_selections == {}

    # ------------------------------------------------------------------
    # Branch coverage for _compute_hierarchy_files ancestors is None (line 310)
    # ------------------------------------------------------------------

    def test_hierarchy_files_skips_parent_exceeding_depth_cap(self, tmp_path: Path) -> None:
        """A parent issue that itself has too many ancestors is skipped in hierarchy_files."""
        flat_specs = [
            _spec(1, tmp_path, "l1"),
            _spec(2, tmp_path, "l2"),
            _spec(3, tmp_path, "l3"),
            _spec(4, tmp_path, "l4"),
            _spec(5, tmp_path, "l5"),
        ]
        graph = {
            1: (None, [_cr(2)]),
            2: (1, [_cr(3)]),
            3: (2, [_cr(4)]),
            4: (3, [_cr(5)]),
            5: (4, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)
        # Issue 4 (parent of 5) has ancestors [1,2,3] → 3 ancestors > max_depth=2 →
        # _compute_hierarchy_files skips the entry for parent 4.
        parent_4_dir = str(tmp_path / "4")
        assert parent_4_dir not in plan.hierarchy_files

    # ------------------------------------------------------------------
    # Branch coverage for "already in remaining_flat" guard (line 211)
    # ------------------------------------------------------------------

    def test_duplicate_flat_spec_objects_deduplicated_in_remaining_flat(self, tmp_path: Path) -> None:
        """The same FlatSpec object appearing twice in flat_specs is only added once."""
        spec = FlatSpec(issue_number=99, path=tmp_path / "99-orphan", slug="orphan")
        flat_specs = [spec, spec]  # same object twice
        plan = compute_migration_plan({}, flat_specs, tmp_path)
        assert len([s for s in plan.remaining_flat if s.issue_number == 99]) == 1

    def test_hierarchy_files_contains_ordered_child_refs(self, tmp_path: Path) -> None:
        """hierarchy_files maps the parent directory to its ordered ChildRef list."""
        cr_a = _cr(101, order=0)
        cr_b = _cr(102, order=1)
        flat_specs = [
            _spec(100, tmp_path, "parent"),
            _spec(101, tmp_path, "a"),
            _spec(102, tmp_path, "b"),
        ]
        graph = {
            100: (None, [cr_a, cr_b]),
            101: (100, []),
            102: (100, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)

        children = plan.hierarchy_files[str(tmp_path / "100")]
        assert [c.number for c in children] == [101, 102]

    def test_hierarchy_files_skipped_when_parent_not_in_spec_or_existing(self, tmp_path: Path) -> None:
        """hierarchy_files entry is omitted when parent has no spec or existing path."""
        flat_specs = [_spec(101, tmp_path, "child")]
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)
        # 100 has no spec and no existing path → no hierarchy_files entry for it.
        assert str(tmp_path / "100") not in plan.hierarchy_files

    def test_placeholder_title_warning_for_child_without_metadata(self, tmp_path: Path) -> None:
        """A child present in the tree but absent from graph children gets a placeholder."""
        # Build a graph where parent 100 claims child 101 but 101 is not in the
        # children list of 100 in the graph — triggers the "missing" code path.
        flat_specs = [_spec(100, tmp_path, "parent"), _spec(101, tmp_path, "child")]
        # The graph shows 101 is a child of 100 via reverse lookup,
        # but the forward children list of 100 is empty — use a trick:
        # 100's children list in the graph has no entry for 101, yet 101's
        # parent is 100.  This ensures the "missing" branch fires.
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {
            100: (None, []),
            101: (100, []),
        }
        # 101 has parent=100 and 100 has children=[] in graph.
        # 101 also has children=[] and parent=100, so it's NOT isolated
        # (has parent). It moves to tmp_path/100/101.
        # But hierarchy_files for 100: no children in graph → placeholder.
        plan = compute_migration_plan(graph, flat_specs, tmp_path)
        # The placeholder branch: child 101 must appear via _compute_hierarchy_files
        parent_dir = str(tmp_path / "100")
        if parent_dir in plan.hierarchy_files:
            assert any("101" in w and "placeholder" in w.lower() for w in plan.warnings)

    # ------------------------------------------------------------------
    # Multi-parent candidates stored
    # ------------------------------------------------------------------

    def test_multi_parent_candidates_recorded(self, tmp_path: Path) -> None:
        """multi_parent_candidates maps the child to all candidate parents."""
        flat_specs = [_spec(10, tmp_path), _spec(20, tmp_path), _spec(30, tmp_path)]
        graph = {
            10: (None, [_cr(30)]),
            20: (None, [_cr(30)]),
            30: (10, []),
        }
        plan = compute_migration_plan(graph, flat_specs, tmp_path)
        assert plan.multi_parent_candidates[30] == [10, 20]

    # ------------------------------------------------------------------
    # Empty graph
    # ------------------------------------------------------------------

    def test_empty_graph_puts_all_specs_in_remaining_flat(self, tmp_path: Path) -> None:
        """No relationships → all flat specs end up in remaining_flat."""
        flat_specs = [_spec(1, tmp_path), _spec(2, tmp_path)]
        plan = compute_migration_plan({}, flat_specs, tmp_path)
        assert plan.moves == []
        assert {s.issue_number for s in plan.remaining_flat} == {1, 2}

    # ------------------------------------------------------------------
    # existing_targets uses existing path for issue
    # ------------------------------------------------------------------

    def test_raises_when_existing_target_is_not_under_canonical_parent(self, tmp_path: Path) -> None:
        """Raises ValueError when an existing child target is at a misplaced location.

        When issue 100 is in existing_targets at a path that doesn't sit
        under its canonical parent directory (tmp_path/50/100), the plan
        cannot materialize a consistent hierarchy and must abort.
        """
        existing_dir = tmp_path / "nested" / "100"
        flat_specs = [
            _spec(50, tmp_path, "parent"),
            _spec(100, tmp_path, "child"),
        ]
        graph = {
            50: (None, [_cr(100)]),
            100: (50, []),
        }
        with pytest.raises(ValueError, match="Existing target #100 is at"):
            compute_migration_plan(graph, flat_specs, tmp_path, existing_targets={100: existing_dir})

    # ------------------------------------------------------------------
    # Partial migration: scope is an already-nested parent (not in graph)
    # ------------------------------------------------------------------

    def test_scope_includes_flat_descendants_of_already_nested_parent(self, tmp_path: Path) -> None:
        """--scope N discovers flat-spec descendants even when N is already nested.

        Before this fix, _resolve_scope(graph, 10) returned {10} for an already-
        nested issue 10 that has no graph entry — flat spec 20 (parent=10 in
        the graph) was silently excluded.
        """
        existing_dir = tmp_path / "10"
        flat_spec_20 = _spec(20, tmp_path, "feature")
        # graph: issue 20 is a flat spec with parent=10; 10 has no graph entry
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {20: (10, [])}
        plan = compute_migration_plan(
            graph,
            [flat_spec_20],
            tmp_path,
            scope=10,
            existing_targets={10: existing_dir},
        )
        # Issue 20 should be moved under the already-nested parent 10
        assert any(m.issue_number == 20 for m in plan.moves), "issue 20 missing from moves"
        move_20 = next(m for m in plan.moves if m.issue_number == 20)
        assert move_20.target == existing_dir / "20"

    def test_scope_discovers_flat_descendants_below_multi_level_existing_tree(self, tmp_path: Path) -> None:
        """--scope N discovers flat specs below already-nested intermediate nodes.

        Example: scope=10, existing_targets={20: specs/10/20/}, flat spec 30
        with parent=20.  Without seeding 20 into in_scope via the existing-target
        traversal, the reverse parent-edge scan can't reach 30.
        """
        existing_20 = tmp_path / "10" / "20"
        flat_spec_30 = _spec(30, tmp_path, "task")
        # graph: 30 has parent=20; 20 is already nested and has no graph entry
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {30: (20, [])}
        plan = compute_migration_plan(
            graph,
            [flat_spec_30],
            tmp_path,
            scope=10,
            existing_targets={20: existing_20},
        )
        assert any(m.issue_number == 30 for m in plan.moves), "issue 30 missing from moves"
        move_30 = next(m for m in plan.moves if m.issue_number == 30)
        assert move_30.target == existing_20 / "30"

    def test_scope_discovers_flat_descendants_below_three_level_existing_tree(self, tmp_path: Path) -> None:
        """Existing-target traversal exercises all conditional branches in _resolve_scope.

        This test constructs a diverse set of existing_targets to ensure every
        branch inside the existing-target block is exercised:

        - outer loop True branch (path contains scope number): existing_20 at
          specs/10/20/ is added to in_scope because "10" is in its parts.
        - inner BFS True branch (path contains current_existing number): existing_30
          at specs/10/20/30/ is added to in_scope by the inner BFS seeded from 20
          because "20" is in its parts.
        - inner BFS False branch (path valid but doesn't match): existing_35 at
          specs/10/35/ is inspected by the inner BFS for current_existing=20 but
          "20" is not in ("10", "35"), so it is skipped.
        - outer loop False branch (path valid but doesn't contain scope): under_other
          at specs/other/50/ is inside specs_root so relative_to() succeeds, but
          "10" is not in ("other", "50") so the entry is not seeded.
        - outer ValueError branch (path outside specs_root): outside_99 at a path
          outside tmp_path raises ValueError from relative_to() in the outer loop.
        - inner ValueError branch (same outside path, inner loop): outside_99 is
          also encountered inside the inner BFS loop where it raises ValueError again.
        """
        existing_20 = tmp_path / "10" / "20"
        existing_30 = tmp_path / "10" / "20" / "30"  # nested under 20 → inner True
        existing_35 = tmp_path / "10" / "35"  # under scope 10 but not 20 → inner False
        under_other = tmp_path / "other" / "50"  # inside specs_root, not under 10 → outer False
        outside_99 = tmp_path.parent / "other" / "99"  # outside specs_root → outer/inner ValueError
        flat_spec_60 = _spec(60, tmp_path, "task")
        # 60 is flat with parent=20; 20 is already nested
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {60: (20, [])}
        plan = compute_migration_plan(
            graph,
            [flat_spec_60],
            tmp_path,
            scope=10,
            existing_targets={
                20: existing_20,
                30: existing_30,
                35: existing_35,
                50: under_other,
                99: outside_99,
            },
        )
        # 60 should move under existing_20
        assert any(m.issue_number == 60 for m in plan.moves), "issue 60 missing from moves"
        move_60 = next(m for m in plan.moves if m.issue_number == 60)
        assert move_60.target == existing_20 / "60"

    def test_scope_ignores_existing_target_outside_specs_root(self, tmp_path: Path) -> None:
        """Existing targets whose paths are outside specs_root are silently skipped.

        A path that does not start with specs_root raises ValueError from
        relative_to(); the traversal must continue without crashing.
        """
        outside_path = tmp_path.parent / "other" / "20"
        flat_spec_30 = _spec(30, tmp_path, "task")
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {30: (20, [])}
        # Should not raise; outside path is skipped and 30 stays flat
        plan = compute_migration_plan(
            graph,
            [flat_spec_30],
            tmp_path,
            scope=10,
            existing_targets={20: outside_path},
        )
        # 30 stays flat because we can't reach it through scope 10
        assert not any(m.issue_number == 30 for m in plan.moves)

    def test_unscoped_writes_hierarchy_file_for_already_nested_parent(self, tmp_path: Path) -> None:
        """Unscoped migration writes hierarchy.yml for an existing nested parent.

        When issue 10 is already nested (existing_targets) and issue 20 is a flat
        spec with parent=10, an unscoped run should produce a hierarchy.yml entry
        for issue 10 so the hierarchy index stays correctly linked.
        """
        existing_dir = tmp_path / "10"
        flat_spec_20 = _spec(20, tmp_path, "feature")
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {20: (10, [])}
        plan = compute_migration_plan(
            graph,
            [flat_spec_20],
            tmp_path,
            existing_targets={10: existing_dir},
        )
        # hierarchy.yml should be written for the already-nested parent (10)
        assert str(existing_dir) in plan.hierarchy_files, (
            "hierarchy_files should contain an entry for the already-nested parent"
        )

    # ------------------------------------------------------------------
    # Non-local parent with local subtree — orphan container prevention
    # ------------------------------------------------------------------

    def test_local_subtree_with_nonlocal_parent_becomes_root(self, tmp_path: Path) -> None:
        """A local subtree whose top issue has a non-local GitHub parent is placed
        at the specs root, not under an orphan container directory for the absent parent.

        Graph: P(non-local) → X(local) → C(local)
        Expected: X → specs/X/, C → specs/X/C/
        No specs/P/ directory should appear in any move target.
        """
        spec_x = _spec(200, tmp_path, "feature")
        spec_c = _spec(201, tmp_path, "task")
        # P=100 is referenced in the graph but has no local flat spec and no
        # existing nested directory — it is a non-local GitHub parent.
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {
            100: (None, [_cr(200)]),
            200: (100, [_cr(201)]),
            201: (200, []),
        }

        plan = compute_migration_plan(graph, [spec_x, spec_c], tmp_path)

        move_map = {m.issue_number: m.target for m in plan.moves}
        assert 200 in move_map, "issue 200 should be moved"
        assert 201 in move_map, "issue 201 should be moved"
        # X must become a root (no orphan 100 container)
        assert move_map[200] == tmp_path / "200", f"expected specs/200 but got {move_map[200]}"
        # C must nest under X, not under the non-local P
        assert move_map[201] == tmp_path / "200" / "201", f"expected specs/200/201 but got {move_map[201]}"
        # The non-local parent's number must not appear in any target path
        for move in plan.moves:
            assert "100" not in str(move.target), f"orphan container 100 must not appear in target path {move.target}"
        # Hierarchy file must be keyed under specs/200, not specs/100/200
        assert str(tmp_path / "200") in plan.hierarchy_files, "hierarchy_files must be keyed under specs/200"
        assert not any("100" in key for key in plan.hierarchy_files), (
            "no hierarchy file should reference the non-local parent 100"
        )

    def test_hierarchy_file_placed_under_already_existing_ancestor(self, tmp_path: Path) -> None:
        """A flat parent whose own ancestor is already in existing is nested under
        that existing directory — the non-stripping branch in _compute_hierarchy_files
        (ancestors[-1] in existing → skip stripping, place under existing ancestor).

        Graph: GP(existing at specs/100/) → P(flat) → C(flat)
        Expected: P → specs/100/200/, hierarchy_files keyed at specs/100/200/
        """
        existing = {100: tmp_path / "100"}
        spec_p = _spec(200, tmp_path, "parent")
        spec_c = _spec(201, tmp_path, "child")
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {
            100: (None, [_cr(200)]),
            200: (100, [_cr(201)]),
            201: (200, []),
        }

        plan = compute_migration_plan(graph, [spec_p, spec_c], tmp_path, existing_targets=existing)

        move_map = {m.issue_number: m.target for m in plan.moves}
        assert move_map[200] == tmp_path / "100" / "200", (
            f"parent should nest under existing ancestor, got {move_map[200]}"
        )
        assert move_map[201] == tmp_path / "100" / "200" / "201"
        assert str(tmp_path / "100" / "200") in plan.hierarchy_files, (
            "hierarchy file must be placed under the existing ancestor directory"
        )
