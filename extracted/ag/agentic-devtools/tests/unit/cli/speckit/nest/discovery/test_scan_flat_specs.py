"""Tests for scan_flat_specs in nest/discovery.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.nest.discovery import scan_flat_specs


class TestScanFlatSpecs:
    """Tests for the scan_flat_specs function."""

    def test_detects_flat_spec_directories(self, tmp_path: Path) -> None:
        """Directories matching {number}-{slug}/ are detected."""
        (tmp_path / "100-auth-module").mkdir()
        (tmp_path / "101-login-flow").mkdir()
        (tmp_path / "102-session-mgmt").mkdir()

        result = scan_flat_specs(tmp_path)
        assert len(result) == 3
        assert result[0].issue_number == 100
        assert result[0].slug == "auth-module"

    def test_excludes_numeric_only_directories(self, tmp_path: Path) -> None:
        """Numeric-only dirs (already nested) are not returned as flat specs."""
        (tmp_path / "100-auth").mkdir()
        (tmp_path / "200").mkdir()

        result = scan_flat_specs(tmp_path)
        assert len(result) == 1
        assert result[0].issue_number == 100

    def test_descends_into_numeric_directories(self, tmp_path: Path) -> None:
        """Flat specs nested inside numeric parent dirs are discovered."""
        nested = tmp_path / "200"
        nested.mkdir()
        (nested / "201-child").mkdir()

        result = scan_flat_specs(tmp_path)
        assert any(s.issue_number == 201 for s in result)

    def test_scans_flat_specs_below_non_numeric_directories(self, tmp_path: Path) -> None:
        """Recursive discovery includes candidates in mixed hierarchy directories."""
        candidate = tmp_path / "legacy" / "12-feature"
        candidate.mkdir(parents=True)

        result = scan_flat_specs(tmp_path)

        assert [(spec.issue_number, spec.path) for spec in result] == [(12, candidate)]

    def test_rejects_overlapping_flat_spec_subtree(self, tmp_path: Path) -> None:
        """Nested flat candidates are rejected instead of silently omitted."""
        parent = tmp_path / "100-parent"
        child = parent / "101-child"
        child.mkdir(parents=True)

        with pytest.raises(ValueError, match="overlapping"):
            scan_flat_specs(tmp_path)

    def test_rejects_numeric_nested_target_inside_flat_spec(self, tmp_path: Path) -> None:
        """A flat spec containing nested numeric targets is rejected as ambiguous."""
        parent = tmp_path / "100-parent"
        child = parent / "200"
        child.mkdir(parents=True)

        with pytest.raises(ValueError, match="mixed flat and nested spec directories"):
            scan_flat_specs(tmp_path)

    def test_ignores_non_candidate_entries_inside_flat_spec(self, tmp_path: Path) -> None:
        """Non-candidate descendants and symlinks do not create overlap errors."""
        parent = tmp_path / "100-parent"
        nested = parent / "metadata"
        nested.mkdir(parents=True)
        (nested / "linked").symlink_to(tmp_path)

        result = scan_flat_specs(tmp_path)

        assert [(spec.issue_number, spec.path) for spec in result] == [(100, parent)]

    def test_rejects_duplicate_issue_numbers_across_distinct_directories(self, tmp_path: Path) -> None:
        """Separate flat directories mapping to the same issue number are rejected."""
        (tmp_path / "100-auth").mkdir()
        (tmp_path / "legacy" / "100-auth-copy").mkdir(parents=True)

        with pytest.raises(ValueError, match="duplicate flat spec directories"):
            scan_flat_specs(tmp_path)

    def test_does_not_scan_flat_spec_descendants_beyond_max_depth(self, tmp_path: Path) -> None:
        """Nested overlap checks honor the configured scan depth."""
        (tmp_path / "100-parent" / "metadata").mkdir(parents=True)

        result = scan_flat_specs(tmp_path, max_depth=1)

        assert [spec.issue_number for spec in result] == [100]

    def test_excludes_non_matching_directories(self, tmp_path: Path) -> None:
        """Directories not matching {number}-{slug} are silently skipped."""
        (tmp_path / "100-auth").mkdir()
        (tmp_path / "not-a-spec").mkdir()
        (tmp_path / ".hidden").mkdir()

        result = scan_flat_specs(tmp_path)
        assert len(result) == 1

    def test_returns_empty_for_missing_directory(self, tmp_path: Path) -> None:
        """An empty list is returned when the specs root does not exist."""
        result = scan_flat_specs(tmp_path / "nonexistent")
        assert result == []

    def test_returns_empty_when_specs_path_is_a_file(self, tmp_path: Path) -> None:
        """An empty list is returned when the path points to a file."""
        specs_file = tmp_path / "specs"
        specs_file.write_text("not a directory", encoding="utf-8")

        result = scan_flat_specs(specs_file)
        assert result == []

    def test_excludes_files(self, tmp_path: Path) -> None:
        """Files (not directories) are not included in results."""
        (tmp_path / "100-auth").mkdir()
        (tmp_path / "101-readme.md").touch()

        result = scan_flat_specs(tmp_path)
        assert len(result) == 1

    def test_sorted_by_directory_name(self, tmp_path: Path) -> None:
        """Results are returned in sorted order by directory name."""
        (tmp_path / "300-third").mkdir()
        (tmp_path / "100-first").mkdir()
        (tmp_path / "200-second").mkdir()

        result = scan_flat_specs(tmp_path)
        assert [s.issue_number for s in result] == [100, 200, 300]

    def test_raises_value_error_for_non_positive_max_depth(self, tmp_path: Path) -> None:
        """max_depth <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="max_depth"):
            scan_flat_specs(tmp_path, max_depth=0)

    def test_does_not_descend_beyond_max_depth(self, tmp_path: Path) -> None:
        """Directories deeper than max_depth are not traversed."""
        level1 = tmp_path / "200"
        level1.mkdir()
        level2 = level1 / "201"
        level2.mkdir()
        (level2 / "202-deep").mkdir()

        # max_depth=2 means only depth-1 and depth-2 entries are visited.
        result = scan_flat_specs(tmp_path, max_depth=2)
        assert not any(s.issue_number == 202 for s in result)

    def test_skips_symlinked_directories(self, tmp_path: Path) -> None:
        """Symlinked directories are not followed during traversal."""
        external = tmp_path / "outside"
        external.mkdir()
        (external / "42-target").mkdir()
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        (specs_root / "linked").symlink_to(external)

        result = scan_flat_specs(specs_root)

        assert not any(s.issue_number == 42 for s in result)

    def test_skips_symlinked_flat_spec_directory(self, tmp_path: Path) -> None:
        """A symlink whose name matches the flat-spec pattern is not reported."""
        external = tmp_path / "outside"
        external.mkdir()
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        (specs_root / "99-linked").symlink_to(external)

        result = scan_flat_specs(specs_root)

        assert result == []
