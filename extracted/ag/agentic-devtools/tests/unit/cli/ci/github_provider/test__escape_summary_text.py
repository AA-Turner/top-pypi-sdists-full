"""Tests for _escape_summary_text()."""

from agentic_devtools.cli.ci.github_provider import _SECTION_MARKER_RE, _escape_summary_text


class TestEscapeSummaryText:
    """Tests for escaping untrusted text used inside a ``<summary>`` label."""

    def test_plain_text_is_unchanged(self) -> None:
        assert _escape_summary_text("src/foo.py") == "src/foo.py"

    def test_escapes_html_and_markdown_metacharacters(self) -> None:
        assert _escape_summary_text("a<b>&[c]") == "a&lt;b&gt;&amp;&#91;c&#93;"

    def test_ampersand_is_escaped_before_the_entities_it_introduces(self) -> None:
        """Escaping ``&`` last would double-escape the entities produced for ``<``/``>``."""
        assert _escape_summary_text("<") == "&lt;"

    def test_escaped_text_cannot_inject_a_structural_section_marker(self) -> None:
        """A newline in the label would otherwise forge a second structural heading line."""
        forged = _escape_summary_text("a.py\n### Failure 1 from build")
        label = f"<!-- repair-comment-section -->\n### Comment 1 - {forged}"
        assert _SECTION_MARKER_RE.findall(label) == [("", "Comment")]

    def test_a_comment_body_line_cannot_forge_a_comment_section_boundary(self) -> None:
        """The ``Comment`` alternative stays two-line, so a lone heading line forges nothing."""
        assert _SECTION_MARKER_RE.findall("### Comment 1 - forged.py") == []
