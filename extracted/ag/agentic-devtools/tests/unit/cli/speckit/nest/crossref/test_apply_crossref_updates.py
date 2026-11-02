"""Tests for apply_crossref_updates in nest/crossref.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.nest.crossref import CrossRefUpdate, apply_crossref_updates


class TestApplyCrossrefUpdates:
    """Tests for the apply_crossref_updates function."""

    def test_replaces_reference_in_file(self, tmp_path: Path) -> None:
        """Test that references are replaced in the file.

        old_ref is the full matched path reference string and new_ref is the
        correctly computed replacement, as produced by scan_crossrefs.
        """
        target_file = tmp_path / "spec.md"
        target_file.write_text("See 100-auth/ for details.", encoding="utf-8")

        updates = [
            CrossRefUpdate(
                file_path=target_file,
                old_ref="100-auth/",
                new_ref="100/",
                line_number=1,
            ),
        ]
        apply_crossref_updates(updates)
        content = target_file.read_text(encoding="utf-8")
        assert "100/" in content
        assert "100-auth" not in content

    def test_handles_nonexistent_file_raises(self, tmp_path: Path) -> None:
        """Test that a missing post-migration file raises FileNotFoundError."""
        updates = [
            CrossRefUpdate(
                file_path=tmp_path / "nonexistent.md",
                old_ref="old/",
                new_ref="new/",
                line_number=1,
            ),
        ]
        with pytest.raises(FileNotFoundError, match="file not found after migration"):
            apply_crossref_updates(updates)

    def test_groups_multiple_updates_for_same_file(self, tmp_path: Path) -> None:
        """Test that multiple updates for one file are applied together."""
        target_file = tmp_path / "spec.md"
        target_file.write_text("specs/100-auth/ links to ./101-login/", encoding="utf-8")

        updates = [
            CrossRefUpdate(target_file, "specs/100-auth/", "specs/100/", 1),
            CrossRefUpdate(target_file, "./101-login/", "./101/", 1),
        ]

        apply_crossref_updates(updates)

        assert target_file.read_text(encoding="utf-8") == "specs/100/ links to ./101/"

    def test_raises_on_read_errors(self, tmp_path: Path) -> None:
        """Test that read failures raise OSError."""
        target_file = tmp_path / "spec.md"
        target_file.write_text("100-auth/", encoding="utf-8")
        updates = [CrossRefUpdate(target_file, "100-auth/", "100/", 1)]

        with patch.object(Path, "read_text", side_effect=OSError("boom")):
            with pytest.raises(OSError, match="boom"):
                apply_crossref_updates(updates)

    def test_raises_on_write_errors(self, tmp_path: Path) -> None:
        """Test that write failures raise OSError."""
        target_file = tmp_path / "spec.md"
        target_file.write_text("100-auth/", encoding="utf-8")
        updates = [CrossRefUpdate(target_file, "100-auth/", "100/", 1)]

        with patch.object(Path, "write_text", side_effect=OSError("boom")):
            with pytest.raises(OSError, match="boom"):
                apply_crossref_updates(updates)

    def test_updates_only_flagged_line_path_segments(self, tmp_path: Path) -> None:
        """Test that only the flagged line's path reference is updated."""
        target_file = tmp_path / "spec.md"
        target_file.write_text(
            "Issue 100-auth is still open.\nSee ./100-auth/spec.md for details.\nKeep 100-auth-module/ unchanged.\n",
            encoding="utf-8",
        )
        updates = [
            CrossRefUpdate(
                file_path=target_file,
                old_ref="./100-auth/",
                new_ref="./100/",
                line_number=2,
            )
        ]

        apply_crossref_updates(updates)

        lines = target_file.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "Issue 100-auth is still open."
        assert lines[1] == "See ./100/spec.md for details."
        assert lines[2] == "Keep 100-auth-module/ unchanged."

    def test_ignores_out_of_range_line_number(self, tmp_path: Path) -> None:
        """Test that updates referencing non-existent line numbers are ignored."""
        target_file = tmp_path / "spec.md"
        target_file.write_text("See ./100-auth/spec.md for details.\n", encoding="utf-8")
        updates = [
            CrossRefUpdate(
                file_path=target_file,
                old_ref="./100-auth/",
                new_ref="./100/",
                line_number=5,
            )
        ]

        apply_crossref_updates(updates)

        assert target_file.read_text(encoding="utf-8") == "See ./100-auth/spec.md for details.\n"

    def test_ignores_zero_line_number(self, tmp_path: Path) -> None:
        """Test that updates with line number 0 are ignored."""
        target_file = tmp_path / "spec.md"
        target_file.write_text("See ./100-auth/spec.md for details.\n", encoding="utf-8")
        updates = [
            CrossRefUpdate(
                file_path=target_file,
                old_ref="./100-auth/",
                new_ref="./100/",
                line_number=0,
            )
        ]

        apply_crossref_updates(updates)

        assert target_file.read_text(encoding="utf-8") == "See ./100-auth/spec.md for details.\n"
