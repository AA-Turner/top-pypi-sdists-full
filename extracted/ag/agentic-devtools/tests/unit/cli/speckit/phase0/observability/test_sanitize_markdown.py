"""Tests for sanitize_markdown in speckit/phase0/observability.py (FR-012a, FR-012b)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.observability import sanitize_markdown


class TestSanitizeMarkdown:
    """Tests for the sanitize_markdown function."""

    def test_escapes_markdown_significant_characters(self) -> None:
        assert sanitize_markdown("a & b < c > d") == "a &amp; b &lt; c &gt; d"

    def test_escapes_all_mapped_characters(self) -> None:
        original = "`#*_[]()|\\~@"
        expected = "&#96;&#35;&#42;&#95;&#91;&#93;&#40;&#41;&#124;&#92;&#126;&#64;"
        assert sanitize_markdown(original) == expected

    def test_control_characters_are_sanitized_first(self) -> None:
        assert sanitize_markdown("a\nb") == "a\ufffdb"

    def test_does_not_reescape_produced_entities(self) -> None:
        # A literal '&' becomes '&amp;'; the resulting '&' inside that entity
        # must not be escaped again in a second pass.
        result = sanitize_markdown("&")
        assert result == "&amp;"
        assert "&amp;amp;" not in result

    def test_plain_text_is_unchanged(self) -> None:
        assert sanitize_markdown("hello world") == "hello world"
