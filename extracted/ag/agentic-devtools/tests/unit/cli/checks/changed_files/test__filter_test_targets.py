"""Tests for _filter_test_targets."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.checks.changed_files import _filter_test_targets


def test_removes_covered_nested_targets_and_preserves_input_order(tmp_path: Path) -> None:
    """Keeps the selected directory while dropping covered files and child targets."""
    targets = [
        "tests/unit/other/test_app.py",
        "tests/unit/other",
        "tests/unit/other/nested",
        "tests/unit/other/nested/test_nested.py",
        "tests/unit/covered.py",
        "tests/unit/covered_dir/test_covered.py",
        "tests/unit/standalone.py",
        "tests/unit/standalone.py",
    ]

    assert _filter_test_targets(
        targets,
        cwd=tmp_path,
        covered_dirs={tmp_path / "tests/unit/covered_dir"},
        covered_files={tmp_path / "tests/unit/covered.py"},
    ) == ["tests/unit/other", "tests/unit/standalone.py"]


def test_keeps_independent_files_without_selected_directories(tmp_path: Path) -> None:
    """Keeps independent file targets when no directory covers them."""
    assert _filter_test_targets(
        ["tests/unit/a.py", "tests/unit/b.py"],
        cwd=tmp_path,
        covered_dirs=set(),
        covered_files=set(),
    ) == ["tests/unit/a.py", "tests/unit/b.py"]


def test_expands_ancestor_directory_around_coverage_and_nested_targets(tmp_path: Path) -> None:
    """Selects uncovered siblings without rerunning coverage-owned or nested tests."""
    root = tmp_path / "tests/unit/adapters"
    covered_dir = root / "base"
    covered_dir.mkdir(parents=True)
    (covered_dir / "test_base.py").touch()
    (root / "test_covered_file.py").touch()
    other = root / "other"
    other.mkdir()
    (other / "test_other.py").touch()
    sibling = root / "sibling"
    sibling.mkdir()
    (sibling / "test_sibling.py").touch()

    assert _filter_test_targets(
        [
            "tests/unit/adapters/other",
            "tests/unit/adapters",
            "tests/unit/adapters/other/test_other.py",
            "tests/unit/missing",
        ],
        cwd=tmp_path,
        covered_dirs={covered_dir},
        covered_files={root / "test_covered_file.py"},
    ) == [
        "tests/unit/adapters/other",
        "tests/unit/adapters/sibling/test_sibling.py",
        "tests/unit/missing",
    ]
