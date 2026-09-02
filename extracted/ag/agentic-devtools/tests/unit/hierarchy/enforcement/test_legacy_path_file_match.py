"""Tests for legacy path lookup when glob match is a file (not directory)."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.hierarchy.enforcement import check_parent_specked


class TestLegacyPathFileMatch:
    """Cover the branch where glob matches a file, not a directory."""

    def test_glob_match_is_file_returns_false(self, tmp_path: Path):
        """If specs/10-something is a file, it should not count as specked."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        # Create a file that matches the glob pattern (not a directory)
        (specs_root / "10-some-spec").write_text("not a directory")

        found, path = check_parent_specked(10, specs_root)
        assert found is False
        assert path is None
