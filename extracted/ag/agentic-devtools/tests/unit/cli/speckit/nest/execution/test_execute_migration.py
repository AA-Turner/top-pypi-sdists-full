"""Tests for execute_migration in nest/execution.py."""

from __future__ import annotations

from contextlib import ExitStack
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.nest.crossref import CrossRefUpdate
from agentic_devtools.cli.speckit.nest.discovery import ChildRef
from agentic_devtools.cli.speckit.nest.execution import execute_migration
from agentic_devtools.cli.speckit.nest.plan import MigrationPlan
from agentic_devtools.cli.speckit.shared.conflict_check import Move
from agentic_devtools.cli.speckit.shared.hierarchy import HierarchyLevel

_CHILD_101 = ChildRef(number=101, title="Feature 101", order=0)
_CHILD_202 = ChildRef(number=202, title="Task 202", order=0)
_CHILD_301 = ChildRef(number=301, title="Sub 301", order=0)

_GIT_PATCHES: list[tuple[str, dict[str, Any]]] = [
    ("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", {"return_value": []}),
    ("agentic_devtools.cli.speckit.nest.execution.preflight_check", {}),
    ("agentic_devtools.cli.speckit.nest.execution._capture_head", {"return_value": "abc1234"}),
    ("agentic_devtools.cli.speckit.nest.execution.update_readme", {}),
    ("agentic_devtools.cli.speckit.nest.execution._stage_specs", {}),
    ("agentic_devtools.cli.speckit.nest.execution.create_commit", {}),
]


class TestExecuteMigration:
    """Tests for the execute_migration function."""

    def test_exits_when_target_conflicts_are_detected(self, tmp_path: Path) -> None:
        """Test that pre-existing target conflicts abort execution with ValueError (no writes)."""
        plan = MigrationPlan()

        with patch(
            "agentic_devtools.cli.speckit.nest.execution.check_target_conflicts",
            return_value=["specs/100"],
        ):
            with pytest.raises(ValueError, match="Target directory conflicts detected"):
                execute_migration(plan, tmp_path)

    def test_moves_directories_writes_hierarchy_and_applies_crossrefs(self, tmp_path: Path) -> None:
        """Test that the full migration writes hierarchy files and crossrefs."""
        source = tmp_path / "100-auth"
        source.mkdir()
        (source / "spec.md").write_text("body", encoding="utf-8")
        target = tmp_path / "100"
        updates = [CrossRefUpdate(file_path=target / "spec.md", old_ref="100-auth", new_ref="100", line_number=1)]
        plan = MigrationPlan(
            moves=[Move(source=source, target=target, issue_number=100)],
            hierarchy_files={
                str(target): [_CHILD_101],
                str(tmp_path / "100" / "feature-parent"): [_CHILD_202],
            },
        )

        mock_save: MagicMock
        mock_crossrefs: MagicMock
        with ExitStack() as stack:
            for target_path, kwargs in _GIT_PATCHES:
                stack.enter_context(patch(target_path, **kwargs))
            mock_save = stack.enter_context(patch("agentic_devtools.cli.speckit.nest.execution.save_hierarchy"))
            mock_crossrefs = stack.enter_context(
                patch("agentic_devtools.cli.speckit.nest.execution.apply_crossref_updates")
            )
            execute_migration(plan, tmp_path, crossref_updates=updates, scope=100)

        assert target.exists()
        assert not source.exists()
        assert mock_save.call_count == 2
        first_node = mock_save.call_args_list[0].args[0]
        second_node = mock_save.call_args_list[1].args[0]
        assert first_node.title == "Issue #100"
        assert second_node.title == "feature-parent"
        assert first_node.level == HierarchyLevel.EPIC
        assert second_node.level == HierarchyLevel.FEATURE
        mock_crossrefs.assert_called_once_with(updates)

    def test_merges_existing_target_hierarchy_yml(self, tmp_path: Path) -> None:
        """Test that an existing target hierarchy.yml is loaded and merged."""
        hierarchy_dir = tmp_path / "100"
        hierarchy_dir.mkdir()
        (hierarchy_dir / "hierarchy.yml").write_text("existing", encoding="utf-8")

        plan = MigrationPlan(hierarchy_files={str(hierarchy_dir): [_CHILD_101]})

        existing_node = MagicMock()
        existing_node.title = "Existing epic"
        existing_node.level = HierarchyLevel.EPIC
        existing_node.parent = None
        existing_node.processed_at = None
        existing_node.children = [MagicMock(key="99", title="Existing child", order=7)]

        with ExitStack() as stack:
            for target_path, kwargs in _GIT_PATCHES:
                stack.enter_context(patch(target_path, **kwargs))
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.speckit.nest.execution.load_hierarchy",
                    return_value=existing_node,
                )
            )
            mock_save = stack.enter_context(patch("agentic_devtools.cli.speckit.nest.execution.save_hierarchy"))
            execute_migration(plan, tmp_path, scope=100)

        merged_node = mock_save.call_args.args[0]
        assert merged_node.title == "Existing epic"
        assert [child.key for child in merged_node.children] == ["99", "101"]

    def test_rejects_conflicting_existing_target_hierarchy_entry(self, tmp_path: Path) -> None:
        """Test that a conflicting existing child entry aborts instead of overwriting metadata."""
        hierarchy_dir = tmp_path / "100"
        hierarchy_dir.mkdir()
        (hierarchy_dir / "hierarchy.yml").write_text("existing", encoding="utf-8")

        plan = MigrationPlan(hierarchy_files={str(hierarchy_dir): [_CHILD_101]})

        existing_node = MagicMock()
        existing_node.title = "Existing epic"
        existing_node.level = HierarchyLevel.EPIC
        existing_node.parent = None
        existing_node.processed_at = None
        existing_node.children = [MagicMock(key="101", title="Different title", order=7)]

        with ExitStack() as stack:
            for target_path, kwargs in _GIT_PATCHES:
                stack.enter_context(patch(target_path, **kwargs))
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.speckit.nest.execution.load_hierarchy",
                    return_value=existing_node,
                )
            )
            stack.enter_context(
                patch("agentic_devtools.cli.speckit.nest.execution.rollback_migration", return_value=True)
            )
            stack.enter_context(patch("agentic_devtools.cli.speckit.nest.execution.save_hierarchy"))
            with pytest.raises(RuntimeError, match="Conflicting child definition"):
                execute_migration(plan, tmp_path, scope=100)

    def test_keeps_matching_existing_target_hierarchy_entry_without_duplication(self, tmp_path: Path) -> None:
        """Test that an identical existing child entry is preserved without duplication."""
        hierarchy_dir = tmp_path / "100"
        hierarchy_dir.mkdir()
        (hierarchy_dir / "hierarchy.yml").write_text("existing", encoding="utf-8")

        plan = MigrationPlan(hierarchy_files={str(hierarchy_dir): [_CHILD_101]})

        existing_node = MagicMock()
        existing_node.title = "Existing epic"
        existing_node.level = HierarchyLevel.EPIC
        existing_node.parent = None
        existing_node.processed_at = None
        existing_node.children = [MagicMock(key="101", title="Feature 101", order=0)]

        with ExitStack() as stack:
            for target_path, kwargs in _GIT_PATCHES:
                stack.enter_context(patch(target_path, **kwargs))
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.speckit.nest.execution.load_hierarchy",
                    return_value=existing_node,
                )
            )
            mock_save = stack.enter_context(patch("agentic_devtools.cli.speckit.nest.execution.save_hierarchy"))
            execute_migration(plan, tmp_path, scope=100)

        merged_node = mock_save.call_args.args[0]
        assert [child.key for child in merged_node.children] == ["101"]

    def test_exits_when_moved_source_hierarchy_yml_would_be_overwritten(self, tmp_path: Path) -> None:
        """Test that a hierarchy.yml carried by a moved source dir aborts execution (no writes).

        The target dir does not exist yet at pre-check time, so the plain
        target-location check cannot detect it. Verifies the source-aware check.
        """
        source = tmp_path / "100-auth"
        source.mkdir()
        (source / "hierarchy.yml").write_text("existing", encoding="utf-8")
        target = tmp_path / "100"
        plan = MigrationPlan(
            moves=[Move(source=source, target=target, issue_number=100)],
            hierarchy_files={str(target): [_CHILD_101]},
        )

        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            pytest.raises(ValueError, match="hierarchy.yml files already exist"),
        ):
            execute_migration(plan, tmp_path)

        # No filesystem writes should have occurred: the source dir is untouched.
        assert source.exists()
        assert not target.exists()

    def test_exits_when_moved_source_has_dangling_hierarchy_yml_symlink(self, tmp_path: Path) -> None:
        """Test that a dangling hierarchy.yml symlink in a moved source dir aborts execution.

        ``.exists()`` returns False for dangling symlinks; only ``.is_symlink()`` detects
        them.  After the move ``save_hierarchy`` would follow the dangling link and could
        write outside the repository, so the pre-mutation check must reject it.
        """
        source = tmp_path / "100-auth"
        source.mkdir()
        dangling_target = tmp_path / "nonexistent-outside" / "hierarchy.yml"
        (source / "hierarchy.yml").symlink_to(dangling_target)
        assert not (source / "hierarchy.yml").exists()  # dangling — exists() is False
        assert (source / "hierarchy.yml").is_symlink()  # but is_symlink() is True

        target = tmp_path / "100"
        plan = MigrationPlan(
            moves=[Move(source=source, target=target, issue_number=100)],
            hierarchy_files={str(target): [_CHILD_101]},
        )

        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            pytest.raises(ValueError, match="hierarchy.yml files already exist"),
        ):
            execute_migration(plan, tmp_path)

        # No filesystem writes should have occurred: the source dir is untouched.
        assert source.exists()
        assert not target.exists()

    def test_aborts_when_planned_target_path_traverses_a_symlink(self, tmp_path: Path) -> None:
        """Migration is aborted when a target path ancestor is a symlinked directory.

        A symlinked parent such as ``specs/100 -> ../outside`` would cause
        ``mkdir`` and ``shutil.move`` to write outside the repository.
        ``execute_migration`` must detect this in the pre-validation phase (no
        filesystem mutations) and raise ``ValueError``.
        """
        specs = tmp_path / "specs"
        specs.mkdir()
        source = specs / "200-slug"
        source.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        symlinked_parent = specs / "100"
        symlinked_parent.symlink_to(outside)  # specs/100 -> ../outside

        target = symlinked_parent / "200"
        plan = MigrationPlan(
            moves=[Move(source=source, target=target, issue_number=200)],
        )

        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            pytest.raises(ValueError, match="Planned target paths traverse symlinked directories"),
        ):
            execute_migration(plan, specs)

        # No filesystem mutations should have occurred.
        assert source.exists()
        assert not target.exists()

    def test_aborts_hierarchy_only_plan_when_hierarchy_target_traverses_a_symlink(self, tmp_path: Path) -> None:
        """Hierarchy-only plans reject symlinked hierarchy targets before writing files."""
        specs = tmp_path / "specs"
        specs.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        symlinked_parent = specs / "100"
        symlinked_parent.symlink_to(outside)

        hierarchy_dir = symlinked_parent / "200"
        plan = MigrationPlan(hierarchy_files={str(hierarchy_dir): [_CHILD_202]})

        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            pytest.raises(ValueError, match="Planned target paths traverse symlinked directories"),
        ):
            execute_migration(plan, specs, scope=100)

        assert not (outside / "200" / "hierarchy.yml").exists()

    def test_skips_crossref_application_when_no_updates_are_provided(self, tmp_path: Path) -> None:
        """Test that crossref updates are optional."""
        source = tmp_path / "100-auth"
        source.mkdir()
        target = tmp_path / "100"
        plan = MigrationPlan(moves=[Move(source=source, target=target, issue_number=100)])

        mock_crossrefs: MagicMock
        with ExitStack() as stack:
            for target_path, kwargs in _GIT_PATCHES:
                stack.enter_context(patch(target_path, **kwargs))
            stack.enter_context(patch("agentic_devtools.cli.speckit.nest.execution.save_hierarchy"))
            mock_crossrefs = stack.enter_context(
                patch("agentic_devtools.cli.speckit.nest.execution.apply_crossref_updates")
            )
            execute_migration(plan, tmp_path, crossref_updates=None, scope=100)

        mock_crossrefs.assert_not_called()

    def test_writes_task_level_for_depth_two_hierarchy_paths(self, tmp_path: Path) -> None:
        """Test that hierarchy files nested two levels deep are written as TASK."""
        source = tmp_path / "100-auth"
        source.mkdir()
        target = tmp_path / "100"
        depth_two = tmp_path / "100" / "200" / "300"
        plan = MigrationPlan(
            moves=[Move(source=source, target=target, issue_number=100)],
            hierarchy_files={str(depth_two): [_CHILD_301]},
        )

        mock_save: MagicMock
        with ExitStack() as stack:
            for target_path, kwargs in _GIT_PATCHES:
                stack.enter_context(patch(target_path, **kwargs))
            mock_save = stack.enter_context(patch("agentic_devtools.cli.speckit.nest.execution.save_hierarchy"))
            execute_migration(plan, tmp_path, scope=100)

        node = mock_save.call_args.args[0]
        assert node.level == HierarchyLevel.TASK

    def test_rollback_is_attempted_and_runtime_error_raised_on_step_failure(self, tmp_path: Path) -> None:
        """Test that a failure during the mutating sequence triggers rollback and RuntimeError."""
        source = tmp_path / "100-auth"
        source.mkdir()
        target = tmp_path / "100"
        plan = MigrationPlan(moves=[Move(source=source, target=target, issue_number=100)])

        mock_rollback: MagicMock
        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            patch("agentic_devtools.cli.speckit.nest.execution.preflight_check"),
            patch(
                "agentic_devtools.cli.speckit.nest.execution._capture_head",
                return_value="abc1234",
            ),
            patch(
                "agentic_devtools.cli.speckit.nest.execution.update_readme",
                side_effect=RuntimeError("disk full"),
            ),
            patch("agentic_devtools.cli.speckit.nest.execution._stage_specs"),
            patch("agentic_devtools.cli.speckit.nest.execution.create_commit"),
            patch(
                "agentic_devtools.cli.speckit.nest.execution.rollback_migration",
                return_value=True,
            ) as mock_rollback,
            pytest.raises(RuntimeError, match="Migration failed and was rolled back"),
        ):
            execute_migration(plan, tmp_path, scope=100)

        mock_rollback.assert_called_once_with("abc1234", tmp_path)

    def test_rollback_warning_printed_when_rollback_fails(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that an incomplete rollback prints a warning message."""
        source = tmp_path / "100-auth"
        source.mkdir()
        target = tmp_path / "100"
        plan = MigrationPlan(moves=[Move(source=source, target=target, issue_number=100)])

        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            patch("agentic_devtools.cli.speckit.nest.execution.preflight_check"),
            patch(
                "agentic_devtools.cli.speckit.nest.execution._capture_head",
                return_value="abc1234",
            ),
            patch(
                "agentic_devtools.cli.speckit.nest.execution.update_readme",
                side_effect=RuntimeError("disk full"),
            ),
            patch("agentic_devtools.cli.speckit.nest.execution._stage_specs"),
            patch("agentic_devtools.cli.speckit.nest.execution.create_commit"),
            patch(
                "agentic_devtools.cli.speckit.nest.execution.rollback_migration",
                return_value=False,
            ),
            pytest.raises(RuntimeError),
        ):
            execute_migration(plan, tmp_path, scope=100)

        captured = capsys.readouterr()
        assert "Rollback attempted" in captured.err

    def test_raises_runtime_error_when_head_capture_subprocess_fails(self, tmp_path: Path) -> None:
        """Test that a failing git rev-parse HEAD raises RuntimeError before any writes."""
        import subprocess as _subprocess

        plan = MigrationPlan()
        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            patch("agentic_devtools.cli.speckit.nest.execution.preflight_check"),
            patch(
                "agentic_devtools.cli.speckit.nest.execution.subprocess.run",
                return_value=_subprocess.CompletedProcess([], 1, "", "fatal: not a git repo"),
            ),
            pytest.raises(RuntimeError, match="Could not determine the current HEAD SHA"),
        ):
            execute_migration(plan, tmp_path, scope=42)

    def test_full_flow_including_capture_head_and_stage_specs(self, tmp_path: Path) -> None:
        """Test that _capture_head and _stage_specs success paths are executed."""
        import subprocess as _subprocess

        plan = MigrationPlan()
        # subprocess.run calls in order:
        # 1. _capture_head: git rev-parse HEAD
        # 2. _stage_specs → _specs_repo_relative_pathspec: git rev-parse --show-toplevel
        # 3. _stage_specs: git add --all -- specs
        results = [
            _subprocess.CompletedProcess([], 0, "deadbeef\n", ""),
            _subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),
            _subprocess.CompletedProcess([], 0, "", ""),
        ]
        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            patch("agentic_devtools.cli.speckit.nest.execution.preflight_check"),
            patch("agentic_devtools.cli.speckit.nest.execution.subprocess.run", side_effect=results),
            patch("agentic_devtools.cli.speckit.nest.execution.update_readme"),
            patch("agentic_devtools.cli.speckit.nest.execution.create_commit"),
        ):
            # Should complete without error
            execute_migration(plan, tmp_path, scope=42)

    def test_stage_specs_failure_triggers_rollback_and_raises(self, tmp_path: Path) -> None:
        """Test that a failing git add in _stage_specs triggers rollback."""
        import subprocess as _subprocess

        plan = MigrationPlan()
        results = [
            _subprocess.CompletedProcess([], 0, "deadbeef\n", ""),  # HEAD
            _subprocess.CompletedProcess([], 0, f"{tmp_path}\n", ""),  # show-toplevel
            _subprocess.CompletedProcess([], 1, "", "error: outside repo"),  # git add fails
        ]
        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            patch("agentic_devtools.cli.speckit.nest.execution.preflight_check"),
            patch("agentic_devtools.cli.speckit.nest.execution.subprocess.run", side_effect=results),
            patch("agentic_devtools.cli.speckit.nest.execution.update_readme"),
            patch("agentic_devtools.cli.speckit.nest.execution.create_commit"),
            patch("agentic_devtools.cli.speckit.nest.execution.rollback_migration", return_value=True),
            pytest.raises(RuntimeError, match="Migration failed and was rolled back"),
        ):
            execute_migration(plan, tmp_path, scope=42)

    def test_rollback_triggered_on_keyboard_interrupt(self, tmp_path: Path) -> None:
        """KeyboardInterrupt in the mutating sequence triggers rollback and re-raises bare."""
        source = tmp_path / "100-auth"
        source.mkdir()
        target = tmp_path / "100"
        plan = MigrationPlan(moves=[Move(source=source, target=target, issue_number=100)])

        mock_rollback: MagicMock
        with (
            patch("agentic_devtools.cli.speckit.nest.execution.check_target_conflicts", return_value=[]),
            patch("agentic_devtools.cli.speckit.nest.execution.preflight_check"),
            patch(
                "agentic_devtools.cli.speckit.nest.execution._capture_head",
                return_value="abc1234",
            ),
            patch(
                "agentic_devtools.cli.speckit.nest.execution.update_readme",
                side_effect=KeyboardInterrupt,
            ),
            patch("agentic_devtools.cli.speckit.nest.execution._stage_specs"),
            patch("agentic_devtools.cli.speckit.nest.execution.create_commit"),
            patch(
                "agentic_devtools.cli.speckit.nest.execution.rollback_migration",
                return_value=True,
            ) as mock_rollback,
            pytest.raises(KeyboardInterrupt),
        ):
            execute_migration(plan, tmp_path, scope=100)

        mock_rollback.assert_called_once_with("abc1234", tmp_path)
