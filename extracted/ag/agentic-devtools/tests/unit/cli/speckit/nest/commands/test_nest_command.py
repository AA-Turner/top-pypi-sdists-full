"""Tests for nest_command in nest/commands.py."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.nest.commands import nest_command
from agentic_devtools.cli.speckit.nest.discovery import ChildRef, FlatSpec, RelationshipDiscovery
from agentic_devtools.cli.speckit.nest.plan import MigrationPlan
from agentic_devtools.cli.speckit.shared.conflict_check import Move
from agentic_devtools.cli.speckit.shared.hierarchy import ChildEntry, HierarchyLevel, HierarchyNode, save_hierarchy

_MOD = "agentic_devtools.cli.speckit.nest.commands"


def _make_discovery(warnings: list[str] | None = None) -> RelationshipDiscovery:
    d = RelationshipDiscovery()
    if warnings:
        d.warnings = warnings
    return d


class TestNestCommand:
    """Tests for the nest_command function."""

    def test_defaults_specs_root_from_current_working_directory(self, tmp_path: Path) -> None:
        """Test that specs_root defaults to cwd/specs when omitted."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()

        with (
            patch(f"{_MOD}.Path.cwd", return_value=tmp_path),
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
        ):
            nest_command(owner="owner", repo="repo")

    def test_exits_when_specs_root_does_not_exist(self, tmp_path: Path) -> None:
        """Test that a missing specs directory aborts early."""
        with pytest.raises(SystemExit, match="1"):
            nest_command(specs_root=tmp_path / "missing", owner="owner", repo="repo")

    def test_exits_when_specs_root_is_a_file(self, tmp_path: Path) -> None:
        """Test that a non-directory specs path aborts with a clear error."""
        specs_file = tmp_path / "specs"
        specs_file.write_text("not a directory", encoding="utf-8")

        with pytest.raises(SystemExit, match="1"):
            nest_command(specs_root=specs_file, owner="owner", repo="repo")

    def test_exits_when_owner_repo_cannot_be_determined(self, tmp_path: Path) -> None:
        """Test that missing repository coordinates abort execution."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()

        with patch(f"{_MOD}._detect_owner_repo", return_value=(None, None)):
            with pytest.raises(SystemExit, match="1"):
                nest_command(specs_root=specs_root)

    def test_owner_partially_detected_from_remote(self, tmp_path: Path) -> None:
        """Test that auto-detection fills in only missing owner or repo."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()

        with (
            patch(f"{_MOD}._detect_owner_repo", return_value=("auto-owner", "auto-repo")),
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
        ):
            # Provide owner only; repo should be auto-filled from detection
            nest_command(specs_root=specs_root, owner="explicit-owner")

    def test_returns_when_no_flat_specs_are_found(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that the command exits cleanly when nothing needs migrating."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo")

        assert "Nothing to migrate" in capsys.readouterr().out

    def test_no_flat_specs_can_still_materialize_hierarchy(self, tmp_path: Path) -> None:
        """Existing numeric targets are queried to materialize hierarchy files."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        existing_targets = {
            100: specs_root / "100",
            42: specs_root / "100" / "42",
        }
        plan = MigrationPlan(
            hierarchy_files={
                str(specs_root / "100"): [],
            }
        )

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
            patch(f"{_MOD}.scan_existing_targets", return_value=existing_targets),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()) as build_graph,
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
        ):
            result = nest_command(specs_root=specs_root, owner="owner", repo="repo", dry_run=True)

        assert isinstance(result, str)
        queried_specs = build_graph.call_args.args[2]
        assert [spec.issue_number for spec in queried_specs] == [42, 100]

    def test_includes_existing_targets_in_graph_sources_when_flat_specs_present(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """In a mixed repo, already-nested targets are included in relationship discovery."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        existing_targets = {42: specs_root / "99" / "42"}
        plan = MigrationPlan()
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value=existing_targets),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()) as build_graph,
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo")

        queried_specs = build_graph.call_args.args[2]
        issue_numbers = [s.issue_number for s in queried_specs]
        assert 100 in issue_numbers
        assert 42 in issue_numbers
        assert "Also including 1 already-nested issue directories" in capsys.readouterr().out

    def test_prints_discovery_warnings(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that warnings from RelationshipDiscovery are printed."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        discovery = _make_discovery(warnings=["issue #99 not found"])
        plan = MigrationPlan()
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=discovery),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo")

        assert "⚠ issue #99 not found" in capsys.readouterr().out

    def test_scope_with_no_matching_moves_returns_early(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that an empty plan with no remaining_flat/warnings prints a message and returns."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan(moves=[])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", scope=999)

        assert "No specs matched scope #999" in capsys.readouterr().out

    def test_scoped_hierarchy_only_plan_is_not_treated_as_unknown(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A scoped plan with only hierarchy writes is still a matched scope."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        existing_targets = {
            100: specs_root / "100",
            200: specs_root / "100" / "200",
        }
        plan = MigrationPlan(
            hierarchy_files={
                str(existing_targets[100]): [ChildRef(number=200, title="Child", order=0)],
            }
        )

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
            patch(f"{_MOD}.scan_existing_targets", return_value=existing_targets),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", scope=100, dry_run=True)

        out = capsys.readouterr().out
        assert "No specs matched" not in out
        assert "PLAN" in out

    def test_scope_rejects_remote_only_relationship_issue_numbers(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Scoped runs only match issues that exist locally under specs/."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        discovery = _make_discovery()
        discovery.graph = {
            100: (
                None,
                [
                    ChildRef(number=777, title="Remote child"),
                ],
            )
        }
        plan = MigrationPlan(moves=[])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=discovery),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", scope=777)

        out = capsys.readouterr().out
        assert "No specs matched scope #777" in out
        assert "PLAN" not in out

    def test_scope_with_no_moves_but_remaining_flat_renders_plan(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Scoped no-op (isolated/cyclic/depth-capped spec) still renders the plan.

        A spec that is in scope but stays flat (e.g. isolated, cyclic, depth-capped)
        has entries in remaining_flat or warnings.  The plan must be rendered so the
        user sees why the spec stays put rather than a misleading 'No specs matched'.
        """
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        spec = FlatSpec(issue_number=42, path=specs_root / "42-auth", slug="auth")
        flat_specs = [spec]
        # Plan has no moves but the spec is in remaining_flat (isolated case)
        plan = MigrationPlan(moves=[], remaining_flat=[spec])
        plan.warnings = []

        mock_format = patch(f"{_MOD}.format_migration_plan", return_value="PLAN OUTPUT")
        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            mock_format as mock_fmt,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", scope=42)

        out = capsys.readouterr().out
        assert "No specs matched" not in out
        assert "PLAN OUTPUT" in out
        assert "No executable migration changes were identified" in out
        assert "standalone or already nested" not in out
        mock_fmt.assert_called_once_with(plan)

    def test_identical_existing_hierarchy_is_treated_as_noop(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An unchanged hierarchy.yml does not keep a repeat run executable."""
        specs_root = tmp_path / "specs"
        parent_dir = specs_root / "100"
        parent_dir.mkdir(parents=True)
        save_hierarchy(
            HierarchyNode(
                title="Issue #100",
                level=HierarchyLevel.EPIC,
                children=[ChildEntry(key="42", title="Child issue", order=0)],
            ),
            parent_dir / "hierarchy.yml",
        )
        plan = MigrationPlan(
            hierarchy_files={
                str(parent_dir): [ChildRef(number=42, title="Child issue", order=0)],
            }
        )
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
            patch(f"{_MOD}.scan_existing_targets", return_value={100: parent_dir, 42: parent_dir / "42"}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN") as mock_format,
        ):
            result = nest_command(specs_root=specs_root, owner="owner", repo="repo")

        assert result is None
        assert "All specs are standalone or already nested. Nothing to migrate." in capsys.readouterr().out
        rendered_plan = mock_format.call_args.args[0]
        assert rendered_plan.hierarchy_files == {}

    def test_existing_hierarchy_missing_planned_child_stays_actionable(self, tmp_path: Path) -> None:
        """A hierarchy file that lacks a planned child still appears in the executable plan."""
        specs_root = tmp_path / "specs"
        parent_dir = specs_root / "100"
        parent_dir.mkdir(parents=True)
        save_hierarchy(
            HierarchyNode(
                title="Issue #100",
                level=HierarchyLevel.EPIC,
                children=[],
            ),
            parent_dir / "hierarchy.yml",
        )
        plan = MigrationPlan(
            hierarchy_files={
                str(parent_dir): [ChildRef(number=42, title="Child issue", order=0)],
            }
        )
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
            patch(f"{_MOD}.scan_existing_targets", return_value={100: parent_dir}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN") as mock_format,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", dry_run=True)

        rendered_plan = mock_format.call_args.args[0]
        assert rendered_plan.hierarchy_files == plan.hierarchy_files

    def test_stops_after_dry_run(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that dry-run mode prints the plan and returns without executing."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan(moves=[Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration") as mock_execute,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", dry_run=True)

        assert "DRY RUN" in capsys.readouterr().out
        mock_execute.assert_not_called()

    def test_dry_run_returns_plan_fingerprint(self, tmp_path: Path) -> None:
        """Dry-run preview returns a stable fingerprint for the computed plan."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan(moves=[Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
        ):
            fingerprint = nest_command(specs_root=specs_root, owner="owner", repo="repo", dry_run=True)

        assert isinstance(fingerprint, str)
        assert fingerprint

    def test_all_standalone_returns_none_without_prompting(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A plan with no moves, no hierarchy writes, and no crossrefs returns None cleanly."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir(exist_ok=True)
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan()
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration") as mock_execute,
        ):
            result = nest_command(specs_root=specs_root, owner="owner", repo="repo")

        assert result is None
        output = capsys.readouterr().out
        assert "standalone" in output or "Nothing to migrate" in output
        mock_execute.assert_not_called()

    def test_prints_plan_without_executing_by_default(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that plan mode stops before execution and hints at --execute."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan()
        plan.warnings = []
        crossref_updates = [
            SimpleNamespace(
                file_path=specs_root / "100-auth" / "spec.md",
                line_number=3,
                old_ref="100-auth",
                new_ref="100",
            )
        ]

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=crossref_updates),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration") as mock_execute,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo")

        output = capsys.readouterr().out
        assert "Cross-reference updates needed: 1" in output
        assert "100-auth → 100" in output
        assert "Pass --execute" in output
        mock_execute.assert_not_called()

    def test_executes_migration_successfully(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test the successful --execute path calls execute_migration and prints completion."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        move = Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)
        plan = MigrationPlan(moves=[move])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration") as mock_execute,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", execute=True, scope=100)

        mock_execute.assert_called_once()
        assert "Migration complete. 1 specs migrated" in capsys.readouterr().out

    def test_executes_with_actionable_hierarchy_files_only(self, tmp_path: Path) -> None:
        """Execution filters hierarchy writes while retaining scope relationships."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        move = Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)
        materialized = specs_root / "200"
        materialized.mkdir()
        save_hierarchy(
            HierarchyNode(
                title="Issue #200",
                level=HierarchyLevel.EPIC,
                children=[ChildEntry(key="200", title="Issue #200", order=0)],
            ),
            materialized / "hierarchy.yml",
        )
        plan = MigrationPlan(
            moves=[move],
            hierarchy_files={
                str(materialized): [ChildRef(number=200, title="Issue #200", order=0)],
            },
        )

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={200: materialized}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration") as mock_execute,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", execute=True)

        assert mock_execute.call_args.args[0].hierarchy_files == {}
        assert mock_execute.call_args.args[0].scope_hierarchy_files == plan.hierarchy_files

    def test_fingerprint_uses_filtered_hierarchy_write_set(self, tmp_path: Path) -> None:
        """Approval fingerprints cover the hierarchy files shown and executed."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        materialized = specs_root / "200"
        materialized.mkdir()
        save_hierarchy(
            HierarchyNode(
                title="Issue #200",
                level=HierarchyLevel.EPIC,
                children=[ChildEntry(key="200", title="Issue #200", order=0)],
            ),
            materialized / "hierarchy.yml",
        )
        plan = MigrationPlan(
            moves=[Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)],
            hierarchy_files={str(materialized): [ChildRef(number=200, title="Issue #200", order=0)]},
        )

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={200: materialized}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}._compute_plan_fingerprint", return_value="fingerprint") as fingerprint,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", dry_run=True)

        fingerprint.assert_called_once()
        assert fingerprint.call_args.args[0].hierarchy_files == {}
        assert fingerprint.call_args.args[0].scope_hierarchy_files == plan.hierarchy_files

    def test_exits_when_execute_migration_raises_value_error(self, tmp_path: Path) -> None:
        """Test that ValueError from execute_migration is caught and exits cleanly."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan(moves=[Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration", side_effect=ValueError("conflict")),
        ):
            with pytest.raises(SystemExit, match="1"):
                nest_command(specs_root=specs_root, owner="owner", repo="repo", execute=True, scope=100)

    def test_exits_when_execute_migration_raises_runtime_error(self, tmp_path: Path) -> None:
        """Test that RuntimeError from execute_migration is caught and exits cleanly."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan(moves=[Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration", side_effect=RuntimeError("git failed")),
        ):
            with pytest.raises(SystemExit, match="1"):
                nest_command(specs_root=specs_root, owner="owner", repo="repo", execute=True, scope=100)

    def test_execute_without_scope_still_runs(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that --execute without --scope is now allowed (scope is optional)."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan(moves=[Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration") as mock_execute,
        ):
            nest_command(specs_root=specs_root, owner="owner", repo="repo", execute=True)

        mock_execute.assert_called_once()
        assert "Migration complete" in capsys.readouterr().out

    def test_execute_aborts_when_expected_fingerprint_does_not_match(self, tmp_path: Path) -> None:
        """Execution aborts when the plan no longer matches the approved preview."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        flat_specs = [FlatSpec(issue_number=100, path=specs_root / "100-auth", slug="auth")]
        plan = MigrationPlan(moves=[Move(source=specs_root / "100-auth", target=specs_root / "100", issue_number=100)])
        plan.warnings = []

        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(f"{_MOD}.compute_migration_plan", return_value=plan),
            patch(f"{_MOD}.scan_crossrefs", return_value=[]),
            patch(f"{_MOD}.format_migration_plan", return_value="PLAN"),
            patch(f"{_MOD}.execute_migration") as mock_execute,
        ):
            with pytest.raises(SystemExit, match="1"):
                nest_command(
                    specs_root=specs_root,
                    owner="owner",
                    repo="repo",
                    execute=True,
                    expected_plan_fingerprint="stale-approved-plan",
                )

        mock_execute.assert_not_called()

    def test_exits_cleanly_when_scan_flat_specs_raises_value_error(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """ValueError from scan_flat_specs produces a clean error message, not a traceback."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        with (
            patch(f"{_MOD}.scan_flat_specs", side_effect=ValueError("duplicate spec for #42")),
            patch(f"{_MOD}._detect_owner_repo", return_value=("owner", "repo")),
        ):
            with pytest.raises(SystemExit, match="1"):
                nest_command(specs_root=specs_root, owner="owner", repo="repo")

        _, err = capsys.readouterr()
        assert "duplicate spec for #42" in err

    def test_exits_cleanly_when_scan_existing_targets_raises_value_error(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """ValueError from scan_existing_targets produces a clean error message, not a traceback."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=[]),
            patch(f"{_MOD}.scan_existing_targets", side_effect=ValueError("duplicate nested target for #100")),
            patch(f"{_MOD}._detect_owner_repo", return_value=("owner", "repo")),
        ):
            with pytest.raises(SystemExit, match="1"):
                nest_command(specs_root=specs_root, owner="owner", repo="repo")

        _, err = capsys.readouterr()
        assert "duplicate nested target for #100" in err

    def test_exits_cleanly_when_compute_migration_plan_raises_value_error(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """ValueError from compute_migration_plan produces a clean error message, not a traceback."""
        flat_specs = [FlatSpec(issue_number=2, path=tmp_path / "specs" / "2-slug", slug="2-slug")]
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        (specs_root / "2-slug").mkdir()
        with (
            patch(f"{_MOD}.scan_flat_specs", return_value=flat_specs),
            patch(f"{_MOD}.scan_existing_targets", return_value={}),
            patch(f"{_MOD}.build_relationship_graph", return_value=_make_discovery()),
            patch(
                f"{_MOD}.compute_migration_plan",
                side_effect=ValueError("child at wrong location"),
            ),
            patch(f"{_MOD}._detect_owner_repo", return_value=("owner", "repo")),
        ):
            with pytest.raises(SystemExit, match="1"):
                nest_command(specs_root=specs_root, owner="owner", repo="repo")

        _, err = capsys.readouterr()
        assert "child at wrong location" in err
