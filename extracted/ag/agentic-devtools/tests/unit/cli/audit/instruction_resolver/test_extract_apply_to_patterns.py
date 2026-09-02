"""Tests for extract_apply_to_patterns."""

from agentic_devtools.cli.audit.instruction_resolver import extract_apply_to_patterns


class TestExtractApplyToPatterns:
    """Tests for extract_apply_to_patterns()."""

    def test_returns_patterns_from_valid_frontmatter(self) -> None:
        content = "---\napplyTo: '**/*.py'\n---\n# body"
        assert extract_apply_to_patterns(content) == ["**/*.py"]

    def test_returns_empty_list_for_missing_frontmatter(self) -> None:
        assert extract_apply_to_patterns("# no frontmatter") == []
