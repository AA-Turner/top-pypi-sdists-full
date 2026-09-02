"""Tests for ``_parse_parent_number()`` in ``request_artifact_fix``."""

from pathlib import Path

from agentic_devtools.cli.speckit.request_artifact_fix import _parse_parent_number


class TestParseParentNumber:
    """Parses the ``parent:`` entry of a ``hierarchy.yml`` file."""

    def test_returns_plain_numeric_parent(self, tmp_path: Path) -> None:
        hierarchy = tmp_path / "hierarchy.yml"
        hierarchy.write_text("level: task\nparent: 1859\n", encoding="utf-8")
        assert _parse_parent_number(hierarchy) == "1859"

    def test_strips_quotes_and_hash(self, tmp_path: Path) -> None:
        hierarchy = tmp_path / "hierarchy.yml"
        hierarchy.write_text('parent: "#1859"\n', encoding="utf-8")
        assert _parse_parent_number(hierarchy) == "1859"

    def test_strips_single_quotes(self, tmp_path: Path) -> None:
        hierarchy = tmp_path / "hierarchy.yml"
        hierarchy.write_text("parent: '1859'\n", encoding="utf-8")
        assert _parse_parent_number(hierarchy) == "1859"

    def test_tolerates_unterminated_quote(self, tmp_path: Path) -> None:
        hierarchy = tmp_path / "hierarchy.yml"
        hierarchy.write_text('parent: "1859\n', encoding="utf-8")
        assert _parse_parent_number(hierarchy) == "1859"

    def test_strips_inline_comment(self, tmp_path: Path) -> None:
        hierarchy = tmp_path / "hierarchy.yml"
        hierarchy.write_text("parent: 1859  # the feature\n", encoding="utf-8")
        assert _parse_parent_number(hierarchy) == "1859"

    def test_returns_none_for_non_numeric_parent(self, tmp_path: Path) -> None:
        hierarchy = tmp_path / "hierarchy.yml"
        hierarchy.write_text("parent: not-a-number\n", encoding="utf-8")
        assert _parse_parent_number(hierarchy) is None

    def test_returns_none_when_no_parent_entry(self, tmp_path: Path) -> None:
        hierarchy = tmp_path / "hierarchy.yml"
        hierarchy.write_text("level: feature\n", encoding="utf-8")
        assert _parse_parent_number(hierarchy) is None

    def test_returns_none_when_file_unreadable(self, tmp_path: Path) -> None:
        assert _parse_parent_number(tmp_path / "missing.yml") is None
