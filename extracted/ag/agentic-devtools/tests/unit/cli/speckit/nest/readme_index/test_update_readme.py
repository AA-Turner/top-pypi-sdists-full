"""Unit tests for :func:`update_readme`."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.nest.readme_index import (
    INDEX_END_MARKER,
    INDEX_START_MARKER,
    update_readme,
)


class TestUpdateReadme:
    """Behavior of the ``specs/README.md`` index writer."""

    def test_creates_readme_when_missing(self, tmp_path: Path) -> None:
        """A missing README is created containing only the index section."""
        readme_path = update_readme(tmp_path)

        assert readme_path == tmp_path / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert content.startswith(INDEX_START_MARKER)
        assert content.rstrip("\n").endswith(INDEX_END_MARKER)

    def test_creates_parent_directory_when_missing(self, tmp_path: Path) -> None:
        """The specs root is created when it does not exist yet."""
        specs_root = tmp_path / "specs"

        readme_path = update_readme(specs_root)

        assert readme_path.exists()

    def test_appends_section_when_markers_absent(self, tmp_path: Path) -> None:
        """An existing README without markers keeps its content and gains the section."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Specs\n\nHand-written intro.\n", encoding="utf-8")

        update_readme(tmp_path)

        content = readme_path.read_text(encoding="utf-8")
        assert content.startswith("# Specs\n\nHand-written intro.\n")
        assert INDEX_START_MARKER in content

    def test_appends_newline_when_existing_content_lacks_one(self, tmp_path: Path) -> None:
        """Content not ending in a newline is separated from the appended section."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Specs", encoding="utf-8")

        update_readme(tmp_path)

        content = readme_path.read_text(encoding="utf-8")
        assert content.startswith("# Specs\n")
        assert INDEX_START_MARKER in content

    def test_replaces_existing_section_in_place(self, tmp_path: Path) -> None:
        """An existing marker section is replaced without touching its surroundings."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text(
            f"# Specs\n\n{INDEX_START_MARKER}\nstale\n{INDEX_END_MARKER}\n\nFooter text.\n",
            encoding="utf-8",
        )
        (tmp_path / "1865").mkdir()

        update_readme(tmp_path)

        content = readme_path.read_text(encoding="utf-8")
        assert "stale" not in content
        assert "`1865`" in content
        assert content.startswith("# Specs\n")
        assert content.rstrip("\n").endswith("Footer text.")
        assert content.count(INDEX_START_MARKER) == 1

    def test_accepts_string_specs_root(self, tmp_path: Path) -> None:
        """A string path is accepted and coerced to :class:`Path`."""
        readme_path = update_readme(str(tmp_path))

        assert readme_path == tmp_path / "README.md"

    def test_honors_max_depth(self, tmp_path: Path) -> None:
        """``max_depth`` is forwarded to the section generator."""
        (tmp_path / "1" / "2").mkdir(parents=True)

        readme_path = update_readme(tmp_path, max_depth=1)

        content = readme_path.read_text(encoding="utf-8")
        assert "`1`" in content
        assert "`1/2`" not in content
