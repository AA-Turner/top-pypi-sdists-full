"""Tests for _parse_apply_to()."""

from agentic_devtools.cli.audit.instruction_resolver import _parse_apply_to


class TestParseApplyTo:
    """Tests for _parse_apply_to() front-matter extraction."""

    def test_extracts_double_quoted_pattern(self) -> None:
        """Double-quoted applyTo value is returned unquoted."""
        result = _parse_apply_to('---\napplyTo: "**/*.py"\n---\n# content')
        assert result == ["**/*.py"]

    def test_extracts_multiple_patterns(self) -> None:
        """Comma-separated values produce multiple entries."""
        result = _parse_apply_to('---\napplyTo: "specs/**,docs/**"\n---\n')
        assert result == ["specs/**", "docs/**"]

    def test_returns_empty_list_when_no_frontmatter(self) -> None:
        """Content without front-matter returns []."""
        result = _parse_apply_to("# Just markdown, no front-matter")
        assert result == []

    def test_returns_empty_list_when_apply_to_absent(self) -> None:
        """Front-matter without applyTo key returns []."""
        result = _parse_apply_to("---\ntitle: My file\n---\n# content")
        assert result == []

    def test_returns_empty_list_when_frontmatter_not_closed(self) -> None:
        """Front-matter block that has no closing '---' returns []."""
        result = _parse_apply_to("---\napplyTo: specs/**\n")
        assert result == []

    def test_returns_empty_list_when_apply_to_value_is_empty(self) -> None:
        """Front-matter with an empty applyTo value returns []."""
        result = _parse_apply_to('---\napplyTo: ""\n---\n# content')
        assert result == []
