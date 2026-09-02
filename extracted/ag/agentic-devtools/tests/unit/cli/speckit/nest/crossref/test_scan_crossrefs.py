"""Tests for crossref scanning in nest/crossref.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.nest.crossref import (
    _compute_new_path_ref,
    _path_ref_contains_dir,
    _scan_file,
    scan_crossrefs,
)
from agentic_devtools.cli.speckit.shared.conflict_check import Move


class TestScanCrossrefs:
    """Tests for the scan_crossrefs function."""

    def test_detects_reference_to_moved_directory(self, tmp_path: Path) -> None:
        """Test that references to moved directories are detected.

        The CrossRefUpdate stores the full matched path reference string as
        old_ref and the correctly computed replacement as new_ref.  The
        file_path stored is the post-migration location.
        """
        specs = tmp_path / "specs"
        source = specs / "101-login"
        source.mkdir(parents=True)
        spec_file = source / "spec.md"
        spec_file.write_text("See also: 100-auth/ for details.", encoding="utf-8")

        moves = [
            Move(source=source, target=specs / "100" / "101", issue_number=101),
            Move(source=specs / "100-auth", target=specs / "100", issue_number=100),
        ]
        updates = scan_crossrefs(moves, specs)
        assert len(updates) >= 1
        # old_ref is now the full matched path reference string
        assert any(u.old_ref == "100-auth/" for u in updates)
        # file_path is the post-migration path (under move.target, not move.source)
        assert all(str(specs / "100" / "101") in str(u.file_path) for u in updates)

    def test_no_updates_for_unrelated_content(self, tmp_path: Path) -> None:
        """Test that unrelated content produces no updates."""
        specs = tmp_path / "specs"
        source = specs / "100-auth"
        source.mkdir(parents=True)
        spec_file = source / "spec.md"
        spec_file.write_text("This has no path references.", encoding="utf-8")

        moves = [
            Move(source=specs / "200-other", target=specs / "200", issue_number=200),
        ]
        updates = scan_crossrefs(moves, specs)
        assert updates == []

    def test_deduplicates_files_shared_across_nested_source_directories(self, tmp_path: Path) -> None:
        """Test that a file reachable via two source directories is only scanned once.

        This covers the scanned_files dedup branch: when two moves have source
        directories where one contains the other (parent/child), rglob on both
        would find the nested files twice without the dedup guard.
        """
        specs = tmp_path / "specs"
        parent_src = specs / "100-auth"
        child_src = parent_src / "sub"
        child_src.mkdir(parents=True)
        (child_src / "spec.md").write_text("See 200-billing/", encoding="utf-8")

        # Two moves: one for parent, one for the child subdir
        moves = [
            Move(source=parent_src, target=specs / "100", issue_number=100),
            Move(source=child_src, target=specs / "100" / "sub", issue_number=0),
            Move(source=specs / "200-billing", target=specs / "200", issue_number=200),
        ]
        with patch("agentic_devtools.cli.speckit.nest.crossref._scan_file") as mock_scan_file:
            scan_crossrefs(moves, specs)

        # The child spec.md is reachable from both parent_src and child_src rglob;
        # the dedup guard ensures _scan_file is called exactly once per unique file.
        assert mock_scan_file.call_count == 1

    def test_skips_duplicate_files_when_same_directory_is_scanned_twice(self, tmp_path: Path) -> None:
        """Test that the same file is only scanned once across repeated directories."""
        specs = tmp_path / "specs"
        source = specs / "100-auth"
        source.mkdir(parents=True)
        (source / "spec.md").write_text("See 100-auth/", encoding="utf-8")

        move = Move(source=source, target=source, issue_number=100)
        with patch("agentic_devtools.cli.speckit.nest.crossref._scan_file") as mock_scan_file:
            scan_crossrefs([move], specs)

        mock_scan_file.assert_called_once()

    def test_scan_file_raises_on_unreadable_files(self, tmp_path: Path) -> None:
        """Test that unreadable files raise OSError so migration aborts before writing."""
        file_path = tmp_path / "spec.md"
        file_path.write_text("See 100-auth/", encoding="utf-8")
        target_map = {"100-auth": (tmp_path / "100", "100")}

        with patch.object(Path, "read_text", side_effect=UnicodeDecodeError("utf-8", b"x", 0, 1, "bad")):
            with pytest.raises(OSError, match="Cannot read"):
                updates: list = []
                _scan_file(file_path, file_path, target_map, updates)

    def test_scan_file_skips_prose_reference_without_path_syntax(self, tmp_path: Path) -> None:
        """Test that plain prose without path syntax is not flagged as a cross-reference."""
        file_path = tmp_path / "spec.md"
        file_path.write_text("Reference 100-auth in plain text", encoding="utf-8")
        target_map = {"100-auth": (tmp_path / "100", "100")}

        updates: list = []
        _scan_file(file_path, file_path, target_map, updates)

        assert updates == []

    def test_scan_file_does_not_match_old_name_prefix_in_longer_directory_name(self, tmp_path: Path) -> None:
        """Test that moved-name prefixes are not matched inside longer directory names."""
        file_path = tmp_path / "spec.md"
        file_path.write_text("See specs/100-auth-module/ for implementation details.", encoding="utf-8")
        target_map = {"100-auth": (tmp_path / "100", "100")}

        updates: list = []
        _scan_file(file_path, file_path, target_map, updates)

        assert updates == []

    def test_scan_file_detects_specs_prefix_reference_without_trailing_slash(self, tmp_path: Path) -> None:
        """Test that specs/ refs without a trailing slash are detected.

        The old_ref stored is the full matched path reference string (e.g.
        ``specs/100-auth``, not just the directory name ``100-auth``).
        """
        file_path = tmp_path / "spec.md"
        # Markdown links often omit the trailing slash: [text](specs/100-auth)
        file_path.write_text("See [auth module](specs/100-auth) for details.", encoding="utf-8")
        target_map = {"100-auth": (tmp_path / "100", "100")}

        updates: list = []
        _scan_file(file_path, file_path, target_map, updates)

        assert len(updates) == 1
        # old_ref is now the full matched string, not just the directory name
        assert updates[0].old_ref == "specs/100-auth"

    def test_scan_file_detects_multiple_distinct_reference_forms_on_one_line(self, tmp_path: Path) -> None:
        """Test that distinct reference forms to the same moved dir on one line are all captured.

        A single line may contain more than one *distinct* path-reference form
        to the same moved directory (e.g. ``../100-auth/`` and ``specs/100-auth``).
        Each has a different old_ref/new_ref, so both must produce an update;
        otherwise one form is left stale after migration.
        """
        file_path = tmp_path / "spec.md"
        file_path.write_text("See ../100-auth/ and also specs/100-auth for details.", encoding="utf-8")
        target_map = {"100-auth": (tmp_path / "specs" / "100", "100")}

        updates: list = []
        _scan_file(file_path, tmp_path / "specs" / "101" / "spec.md", target_map, updates)

        old_refs = {u.old_ref for u in updates}
        assert old_refs == {"../100-auth/", "specs/100-auth"}

    def test_scan_file_deduplicates_identical_reference_form_on_one_line(self, tmp_path: Path) -> None:
        """Test that repeated identical reference forms yield a single update.

        ``apply_crossref_updates`` uses ``str.replace`` (all occurrences), so a
        single update per distinct old_ref is sufficient and duplicates are
        redundant.
        """
        file_path = tmp_path / "spec.md"
        file_path.write_text("See specs/100-auth and again specs/100-auth here.", encoding="utf-8")
        target_map = {"100-auth": (tmp_path / "specs" / "100", "100")}

        updates: list = []
        _scan_file(file_path, file_path, target_map, updates)

        assert len(updates) == 1
        assert updates[0].old_ref == "specs/100-auth"

    def test_scan_file_emits_single_update_when_one_ref_contains_two_moved_dirs(self, tmp_path: Path) -> None:
        """Test that a ref containing two moved dir names produces one update, not conflicting ones.

        ``specs/100-auth/101-login/`` matches both ``100-auth`` and ``101-login``
        as segments. Because the update is applied via ``str.replace`` on the
        whole old_ref, emitting two updates with the same old_ref but different
        new_ref would be contradictory; only one line-scoped update is created.
        """
        file_path = tmp_path / "spec.md"
        file_path.write_text("See specs/100-auth/101-login/ here.", encoding="utf-8")
        target_map = {
            "100-auth": (tmp_path / "specs" / "100", "100"),
            "101-login": (tmp_path / "specs" / "100" / "101", "100/101"),
        }

        updates: list = []
        _scan_file(file_path, file_path, target_map, updates)

        assert len(updates) == 1
        assert updates[0].old_ref == "specs/100-auth/101-login/"

    def test_path_ref_contains_dir_matches_exact_segment(self) -> None:
        """Test exact segment matching for directory names across path positions."""
        assert _path_ref_contains_dir("specs/100-auth/", "100-auth")
        assert _path_ref_contains_dir("100-auth/subdir", "100-auth")
        assert _path_ref_contains_dir("specs/100-auth", "100-auth")
        assert _path_ref_contains_dir("specs/100-auth/100-auth/file", "100-auth")
        assert _path_ref_contains_dir("specs//100-auth", "100-auth")
        assert _path_ref_contains_dir("specs/./100-auth", "100-auth")
        assert _path_ref_contains_dir("specs/../100-auth", "100-auth")
        assert not _path_ref_contains_dir("specs/100-auth-module/", "100-auth")
        assert not _path_ref_contains_dir("", "100-auth")

    def test_returns_empty_when_specs_root_does_not_exist(self, tmp_path: Path) -> None:
        """Test that a non-existent specs_root yields no updates."""
        moves = [Move(source=tmp_path / "100-auth", target=tmp_path / "100", issue_number=100)]
        updates = scan_crossrefs(moves, tmp_path / "nonexistent")
        assert updates == []

    def test_returns_empty_when_moves_list_is_empty(self, tmp_path: Path) -> None:
        """Test that an empty moves list yields no updates even when specs/ exists."""
        specs = tmp_path / "specs"
        specs.mkdir()
        (specs / "file.md").write_text("some content", encoding="utf-8")
        updates = scan_crossrefs([], specs)
        assert updates == []

    def test_deduplicates_same_file_when_rglob_yields_duplicate_paths(self, tmp_path: Path) -> None:
        """Test that the scanned_files guard prevents scanning a path twice."""
        specs = tmp_path / "specs"
        source = specs / "100-auth"
        source.mkdir(parents=True)
        spec_file = source / "spec.md"
        spec_file.write_text("See 100-auth/", encoding="utf-8")

        moves = [Move(source=source, target=specs / "100", issue_number=100)]

        # Patch rglob to return the same path twice so the dedup guard is exercised.
        with (
            patch.object(
                type(specs),
                "rglob",
                return_value=[spec_file, spec_file],
            ) as _mock_rglob,
            patch("agentic_devtools.cli.speckit.nest.crossref._scan_file") as mock_scan_file,
        ):
            scan_crossrefs(moves, specs)

        # The file should only be scanned once despite appearing twice in rglob.
        mock_scan_file.assert_called_once()


class TestComputeNewPathRef:
    """Tests for the _compute_new_path_ref helper."""

    def test_relative_ref_recomputes_relpath_with_trailing_slash(self, tmp_path: Path) -> None:
        """Test that ../dir/ refs are recomputed via relpath, preserving trailing slash.

        Moving specs/101-oauth/ → specs/100/101/ and specs/100-auth/ → specs/100/
        means ../100-auth/ in the 101 spec must become ../ (one level up from
        specs/100/101/ reaches specs/100/).
        """
        new_file_parent = tmp_path / "specs" / "100" / "101"
        new_target_dir = tmp_path / "specs" / "100"

        result = _compute_new_path_ref(
            "../100-auth/",
            "100-auth",
            "100",
            new_file_parent,
            new_target_dir,
        )

        assert result == "../"

    def test_relative_ref_recomputes_relpath_without_trailing_slash(self, tmp_path: Path) -> None:
        """Test that ../dir refs without trailing slash are recomputed without one."""
        new_file_parent = tmp_path / "specs" / "100" / "101"
        new_target_dir = tmp_path / "specs" / "100"

        result = _compute_new_path_ref(
            "../100-auth",
            "100-auth",
            "100",
            new_file_parent,
            new_target_dir,
        )

        assert result == ".."

    def test_dotslash_ref_recomputes_relpath(self, tmp_path: Path) -> None:
        """Test that ./dir/ refs are recomputed via relpath."""
        new_file_parent = tmp_path / "specs" / "100"
        new_target_dir = tmp_path / "specs" / "200"

        result = _compute_new_path_ref(
            "./200-billing/",
            "200-billing",
            "200",
            new_file_parent,
            new_target_dir,
        )

        assert result == "../200/"

    def test_specs_prefix_ref_uses_segment_substitution(self, tmp_path: Path) -> None:
        """Test that specs/ refs use segment substitution, not relpath."""
        new_file_parent = tmp_path / "specs" / "100" / "101"
        new_target_dir = tmp_path / "specs" / "100"

        result = _compute_new_path_ref(
            "specs/100-auth/",
            "100-auth",
            "100",
            new_file_parent,
            new_target_dir,
        )

        assert result == "specs/100/"

    def test_bare_name_ref_uses_segment_substitution(self, tmp_path: Path) -> None:
        """Test that bare name refs use segment substitution."""
        new_file_parent = tmp_path / "specs" / "100" / "101"
        new_target_dir = tmp_path / "specs" / "100"

        result = _compute_new_path_ref(
            "100-auth/",
            "100-auth",
            "100",
            new_file_parent,
            new_target_dir,
        )

        assert result == "100/"

    def test_segment_substitution_expands_multipart_new_rel(self, tmp_path: Path) -> None:
        """Test that segment substitution handles new_rel with path separators."""
        new_file_parent = tmp_path / "specs" / "200"
        new_target_dir = tmp_path / "specs" / "100" / "101"

        result = _compute_new_path_ref(
            "specs/101-oauth/",
            "101-oauth",
            "100/101",
            new_file_parent,
            new_target_dir,
        )

        assert result == "specs/100/101/"

    def test_relative_ref_falls_back_to_segment_substitution_when_relpath_raises(self, tmp_path: Path) -> None:
        """Test that a ValueError from os.path.relpath triggers segment substitution fallback.

        This branch handles environments (e.g. Windows cross-drive paths) where
        relpath cannot compute a relative path between the two locations.
        """
        from unittest.mock import patch

        new_file_parent = tmp_path / "specs" / "100" / "101"
        new_target_dir = tmp_path / "specs" / "100"

        with patch("agentic_devtools.cli.speckit.nest.crossref.os.path.relpath", side_effect=ValueError("cross-drive")):
            result = _compute_new_path_ref(
                "../100-auth/",
                "100-auth",
                "100",
                new_file_parent,
                new_target_dir,
            )

        # Fallback segment substitution: replaces "100-auth" with "100" in the ref
        assert result == "../100/"
