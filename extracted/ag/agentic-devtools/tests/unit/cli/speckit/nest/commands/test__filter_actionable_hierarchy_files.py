"""Tests for _filter_actionable_hierarchy_files in nest/commands.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.hierarchy import HierarchyValidationError
from agentic_devtools.cli.speckit.nest.commands import _filter_actionable_hierarchy_files
from agentic_devtools.cli.speckit.nest.discovery import ChildRef
from agentic_devtools.cli.speckit.nest.plan import MigrationPlan

_MOD = "agentic_devtools.cli.speckit.nest.commands"


def _make_plan(hierarchy_files: dict[str, list[ChildRef]]) -> MigrationPlan:
    return MigrationPlan(
        moves=[],
        hierarchy_files=hierarchy_files,
        scope_hierarchy_files={},
        excluded_cycles=[],
        multi_parent_selections={},
        multi_parent_candidates={},
        remaining_flat=[],
        warnings=[],
        existing_root_issues=set(),
    )


class TestFilterActionableHierarchyFiles:
    """Tests for _filter_actionable_hierarchy_files."""

    def test_prints_error_and_exits_on_hierarchy_validation_error(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Malformed hierarchy.yml triggers a controlled CLI error instead of a traceback."""
        child = ChildRef(number=10, title="Child", order=1)
        plan = _make_plan({str(tmp_path): [child]})

        with (
            patch(
                f"{_MOD}._hierarchy_is_already_materialized",
                side_effect=HierarchyValidationError("file", "YAML parse error: mapping expected"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            _filter_actionable_hierarchy_files(plan)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Cannot read existing hierarchy file" in captured.err
        assert "YAML parse error" in captured.err

    def test_prints_error_and_exits_on_os_error(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """OS-level read failures also produce a controlled CLI error."""
        child = ChildRef(number=10, title="Child", order=1)
        plan = _make_plan({str(tmp_path): [child]})

        with (
            patch(
                f"{_MOD}._hierarchy_is_already_materialized",
                side_effect=OSError("permission denied"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            _filter_actionable_hierarchy_files(plan)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Cannot read existing hierarchy file" in captured.err

    def test_returns_only_actionable_entries(self, tmp_path: Path) -> None:
        """Already-materialized entries are excluded; pending ones are returned."""
        child = ChildRef(number=10, title="Child", order=1)
        path_a = str(tmp_path / "a")
        path_b = str(tmp_path / "b")
        plan = _make_plan({path_a: [child], path_b: [child]})

        with patch(
            f"{_MOD}._hierarchy_is_already_materialized",
            side_effect=[True, False],
        ):
            result = _filter_actionable_hierarchy_files(plan)

        assert path_a not in result
        assert path_b in result

    def test_rejects_symlinked_hierarchy_file(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Symlinked hierarchy files are rejected before any external file can be written."""
        child = ChildRef(number=10, title="Child", order=1)
        external = tmp_path / "external.yml"
        external.write_text("children: []\n", encoding="utf-8")
        directory = tmp_path / "target"
        directory.mkdir()
        (directory / "hierarchy.yml").symlink_to(external)

        with pytest.raises(SystemExit) as exc_info:
            _filter_actionable_hierarchy_files(_make_plan({str(directory): [child]}))

        assert exc_info.value.code == 1
        assert "Cannot read existing hierarchy file" in capsys.readouterr().err
