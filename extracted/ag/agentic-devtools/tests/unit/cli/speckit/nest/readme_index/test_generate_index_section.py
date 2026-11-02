"""Unit tests for :func:`generate_index_section`."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.nest.readme_index import (
    INDEX_END_MARKER,
    INDEX_START_MARKER,
    generate_index_section,
)


class TestGenerateIndexSection:
    """Behavior of the marker-delimited index section generator."""

    def test_wraps_output_in_markers(self, tmp_path: Path) -> None:
        """The generated section starts and ends with the index markers."""
        section = generate_index_section(tmp_path)

        assert section.startswith(INDEX_START_MARKER)
        assert section.endswith(INDEX_END_MARKER)

    def test_reports_placeholder_when_no_nested_specs(self, tmp_path: Path) -> None:
        """An empty specs tree renders the no-nested-specs placeholder."""
        section = generate_index_section(tmp_path)

        assert "_No nested specs yet._" in section

    def test_ignores_non_numeric_directories(self, tmp_path: Path) -> None:
        """Directories whose names are not pure digits are skipped."""
        (tmp_path / "1865-flat-slug").mkdir()
        (tmp_path / "notes").mkdir()

        section = generate_index_section(tmp_path)

        assert "_No nested specs yet._" in section
        assert "1865-flat-slug" not in section

    def test_ignores_files(self, tmp_path: Path) -> None:
        """Regular files are not treated as hierarchy entries."""
        (tmp_path / "42").write_text("not a directory", encoding="utf-8")

        section = generate_index_section(tmp_path)

        assert "_No nested specs yet._" in section

    def test_renders_entries_in_numeric_order(self, tmp_path: Path) -> None:
        """Sibling directories are ordered numerically, not lexicographically."""
        for name in ("10", "9", "100"):
            (tmp_path / name).mkdir()

        section = generate_index_section(tmp_path)

        assert section.index("`9`") < section.index("`10`") < section.index("`100`")

    def test_indents_nested_entries_by_depth(self, tmp_path: Path) -> None:
        """Nested directories are indented two spaces per depth level."""
        (tmp_path / "1" / "2" / "3").mkdir(parents=True)

        section = generate_index_section(tmp_path)

        assert "- [`1`](1/)" in section
        assert "  - [`1/2`](1/2/)" in section
        assert "    - [`1/2/3`](1/2/3/)" in section

    def test_stops_descending_at_max_depth(self, tmp_path: Path) -> None:
        """Directories deeper than ``max_depth`` are not listed."""
        (tmp_path / "1" / "2" / "3").mkdir(parents=True)

        section = generate_index_section(tmp_path, max_depth=2)

        assert "`1/2`" in section
        assert "`1/2/3`" not in section

    def test_returns_placeholder_when_specs_root_missing(self, tmp_path: Path) -> None:
        """A non-existent specs root yields the placeholder rather than raising."""
        section = generate_index_section(tmp_path / "missing")

        assert "_No nested specs yet._" in section

    def test_accepts_string_specs_root(self, tmp_path: Path) -> None:
        """A string path is accepted and coerced to :class:`Path`."""
        (tmp_path / "7").mkdir()

        section = generate_index_section(str(tmp_path))

        assert "`7`" in section

    @pytest.mark.parametrize("max_depth", [0, -1])
    def test_rejects_non_positive_max_depth(self, tmp_path: Path, max_depth: int) -> None:
        """A non-positive ``max_depth`` raises :class:`ValueError`."""
        with pytest.raises(ValueError, match="max_depth must be a positive integer"):
            generate_index_section(tmp_path, max_depth=max_depth)
