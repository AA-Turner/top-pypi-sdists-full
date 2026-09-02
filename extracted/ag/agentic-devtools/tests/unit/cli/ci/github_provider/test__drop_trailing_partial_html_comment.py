"""Tests for _drop_trailing_partial_html_comment()."""

from agentic_devtools.cli.ci.github_provider import _drop_trailing_partial_html_comment


class TestDropTrailingPartialHtmlComment:
    """Tests for removing a truncated HTML comment opener from a body tail."""

    def test_returns_text_unchanged_when_no_html_comment(self) -> None:
        text = "plain prose\nwith no markers"
        assert _drop_trailing_partial_html_comment(text) == text

    def test_returns_text_unchanged_when_every_opener_is_closed(self) -> None:
        text = "@copilot\n<!-- repair-section:author-comments -->\nprose"
        assert _drop_trailing_partial_html_comment(text) == text

    def test_returns_text_unchanged_when_cut_lands_exactly_at_opener_boundary(self) -> None:
        text = "@copilot\n<!-- repair-comment-section -->\n"
        assert _drop_trailing_partial_html_comment(text) == text

    def test_drops_line_holding_a_split_opener(self) -> None:
        text = "@copilot\n<!-- repair-section:author-comments -->\n<!-- source-review-id:12"
        assert _drop_trailing_partial_html_comment(text) == "@copilot\n<!-- repair-section:author-comments -->\n"

    def test_drops_trailing_three_character_partial_opener(self) -> None:
        assert _drop_trailing_partial_html_comment("prose\n<!-") == "prose\n"

    def test_drops_trailing_two_character_partial_opener(self) -> None:
        assert _drop_trailing_partial_html_comment("prose\n<!") == "prose\n"

    def test_returns_empty_string_when_split_opener_has_no_preceding_newline(self) -> None:
        assert _drop_trailing_partial_html_comment("<!-- repair-comment-sec") == ""

    def test_keeps_unclosed_opener_inside_markdown_fence(self) -> None:
        text = "\n".join(["prefix", "```", "<!-- sample", "```", "suffix"])
        assert _drop_trailing_partial_html_comment(text) == text

    def test_keeps_unclosed_opener_inside_longer_markdown_fence(self) -> None:
        text = "\n".join(["````", "```", "<!-- sample", "````", "suffix"])
        assert _drop_trailing_partial_html_comment(text) == text

    def test_invalid_backtick_info_string_does_not_start_markdown_fence(self) -> None:
        text = "\n".join(["```python`", "<!-- sample"])
        assert _drop_trailing_partial_html_comment(text) == "```python`\n"

    def test_keeps_trailing_three_character_partial_opener_inside_markdown_fence(self) -> None:
        text = "```python\n<!-"
        assert _drop_trailing_partial_html_comment(text) == text

    def test_keeps_trailing_two_character_partial_opener_inside_markdown_fence(self) -> None:
        text = "```python\n<!"
        assert _drop_trailing_partial_html_comment(text) == text
