"""Tests for scan_existing_targets in nest/discovery.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.nest.discovery import scan_existing_targets


class TestScanExistingTargets:
    """Tests for scan_existing_targets."""

    def test_returns_empty_for_nonexistent_root(self, tmp_path: Path) -> None:
        """Returns empty dict when specs root does not exist."""
        result = scan_existing_targets(tmp_path / "missing")
        assert result == {}

    def test_returns_empty_for_file_path(self, tmp_path: Path) -> None:
        """Returns empty dict when specs root is a file, not a directory."""
        f = tmp_path / "file"
        f.write_text("data", encoding="utf-8")
        assert scan_existing_targets(f) == {}

    def test_indexes_numeric_directories(self, tmp_path: Path) -> None:
        """Numeric directories at depth 1 are indexed."""
        (tmp_path / "100").mkdir()
        (tmp_path / "200").mkdir()

        result = scan_existing_targets(tmp_path)
        assert 100 in result
        assert 200 in result

    def test_ignores_non_numeric_directories(self, tmp_path: Path) -> None:
        """Non-numeric directory names are skipped."""
        (tmp_path / "100").mkdir()
        (tmp_path / "100-slug").mkdir()

        result = scan_existing_targets(tmp_path)
        assert list(result.keys()) == [100]

    def test_ignores_files(self, tmp_path: Path) -> None:
        """Files (not directories) are ignored even if named numerically."""
        (tmp_path / "100").write_text("data", encoding="utf-8")

        result = scan_existing_targets(tmp_path)
        assert result == {}

    def test_rejects_duplicate_nested_targets_for_same_issue_number(self, tmp_path: Path) -> None:
        """Distinct canonical numeric directories for one issue abort discovery."""
        outer = tmp_path / "100"
        outer.mkdir()
        (outer / "200").mkdir()
        (tmp_path / "200").mkdir()

        with pytest.raises(ValueError, match="duplicate nested target directories"):
            scan_existing_targets(tmp_path)

    def test_recurses_into_numeric_subdirectories(self, tmp_path: Path) -> None:
        """Nested numeric directories are indexed recursively."""
        parent = tmp_path / "100"
        parent.mkdir()
        child = parent / "101"
        child.mkdir()

        result = scan_existing_targets(tmp_path)
        assert 100 in result
        assert 101 in result

    def test_skips_numeric_directories_under_non_numeric_ancestors(self, tmp_path: Path) -> None:
        """Numeric directories under named containers are not treated as canonical targets."""
        legacy_root = tmp_path / "legacy"
        legacy_root.mkdir()
        (legacy_root / "100").mkdir()
        canonical_root = tmp_path / "200"
        canonical_root.mkdir()
        (canonical_root / "201").mkdir()

        result = scan_existing_targets(tmp_path)

        assert 100 not in result
        assert result[200] == canonical_root
        assert result[201] == canonical_root / "201"

    def test_raises_value_error_for_non_positive_max_depth(self, tmp_path: Path) -> None:
        """max_depth <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="max_depth"):
            scan_existing_targets(tmp_path, max_depth=0)

    def test_does_not_recurse_beyond_max_depth(self, tmp_path: Path) -> None:
        """Directories beyond max_depth are not traversed."""
        d1 = tmp_path / "1"
        d1.mkdir()
        d2 = d1 / "2"
        d2.mkdir()
        d3 = d2 / "3"
        d3.mkdir()

        result = scan_existing_targets(tmp_path, max_depth=2)
        assert 3 not in result

    def test_skips_symlinked_directories(self, tmp_path: Path) -> None:
        """Symlinked directories are not followed during traversal."""
        external = tmp_path / "outside"
        external.mkdir()
        (external / "42").mkdir()
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        (specs_root / "linked").symlink_to(external)

        result = scan_existing_targets(specs_root)

        assert 42 not in result

    def test_skips_symlinked_numeric_directory(self, tmp_path: Path) -> None:
        """A symlink whose name is numeric is not indexed as an existing target."""
        external = tmp_path / "outside"
        external.mkdir()
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        (specs_root / "99").symlink_to(external)

        result = scan_existing_targets(specs_root)

        assert 99 not in result
