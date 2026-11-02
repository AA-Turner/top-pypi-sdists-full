"""Tests for _render_suggestion."""

from agentic_devtools.cli.azure_devops.consolidated_review import _render_suggestion
from agentic_devtools.cli.azure_devops.review_state import SuggestionEntry

_BASE_URL = "https://dev.azure.com/org/proj/_git/repo/pullrequest/1"


def _make_suggestion(**kwargs) -> SuggestionEntry:
    defaults = {
        "threadId": 7,
        "commentId": 3,
        "line": 10,
        "endLine": 12,
        "severity": "high",
        "outOfScope": False,
        "linkText": "lines 10 - 12",
        "content": "Use a null check here",
    }
    defaults.update(kwargs)
    return SuggestionEntry(**defaults)  # type: ignore[arg-type]


class TestRenderSuggestion:
    """Tests for _render_suggestion."""

    def test_bullet_contains_link_text_and_first_content_line(self):
        """Bullet line links to the thread and shows the first content line."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion())
        text = "\n".join(lines)
        assert "lines 10 - 12" in text
        assert "Use a null check here" in text

    def test_out_of_scope_label_present(self):
        """Suggestions with outOfScope=True show the out-of-scope marker."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(outOfScope=True))
        text = "\n".join(lines)
        assert "*(out of scope)*" in text

    def test_out_of_scope_absent_when_false(self):
        """Suggestions with outOfScope=False omit the out-of-scope marker."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(outOfScope=False))
        text = "\n".join(lines)
        assert "out of scope" not in text

    def test_detail_block_contains_severity_and_line_label(self):
        """Detail block embeds severity and line-range label."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(severity="medium"))
        text = "\n".join(lines)
        assert "Medium" in text
        assert "lines 10" in text

    def test_single_line_label(self):
        """When line == endLine, label reads 'line N'."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(line=5, endLine=5, linkText="line 5"))
        text = "\n".join(lines)
        assert "line 5" in text

    def test_empty_content_falls_back_to_no_detail(self):
        """Empty content shows a '(no detail)' placeholder."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(content=""))
        text = "\n".join(lines)
        assert "(no detail)" in text

    def test_no_replacement_code_omits_suggestion_fence(self):
        """When replacement_code is None, no suggestion fence is rendered."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(replacement_code=None))
        text = "\n".join(lines)
        assert "```suggestion" not in text

    def test_blank_replacement_code_omits_suggestion_fence(self):
        """When replacement_code is blank/whitespace, no fence is rendered."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(replacement_code="   "))
        text = "\n".join(lines)
        assert "```suggestion" not in text

    def test_empty_string_replacement_code_omits_suggestion_fence(self):
        """When replacement_code is an empty string, no fence is rendered."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(replacement_code=""))
        text = "\n".join(lines)
        assert "```suggestion" not in text

    def test_replacement_code_renders_suggestion_fence(self):
        """When replacement_code is set, a fenced suggestion block is included."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion(replacement_code="const x = 1;\nreturn x;"))
        text = "\n".join(lines)
        assert "```suggestion" in text
        assert "const x = 1;" in text
        assert "return x;" in text

    def test_replacement_code_renders_after_content(self):
        """The suggestion fence appears after the content lines."""
        lines = _render_suggestion(
            _BASE_URL, _make_suggestion(content="Add type annotation", replacement_code="x: int = 0")
        )
        text = "\n".join(lines)
        content_idx = text.index("Add type annotation")
        fence_idx = text.index("```suggestion")
        assert content_idx < fence_idx

    def test_details_block_present(self):
        """Output always wraps in a <details> block."""
        lines = _render_suggestion(_BASE_URL, _make_suggestion())
        text = "\n".join(lines)
        assert "<details>" in text
        assert "</details>" in text
