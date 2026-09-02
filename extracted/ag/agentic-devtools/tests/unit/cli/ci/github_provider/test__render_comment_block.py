"""Tests for _render_comment_block()."""

from agentic_devtools.cli.ci.github_provider import _render_comment_block
from agentic_devtools.cli.ci.models import ReviewCommentInfo


def _comment(**overrides: object) -> ReviewCommentInfo:
    fields: dict[str, object] = {
        "id": 101,
        "path": "src/foo.py",
        "line": 214,
        "start_line": 210,
        "body": "Fix the null check here",
        "html_url": "https://github.com/owner/repo/pull/42#discussion_r101",
    }
    fields.update(overrides)
    return ReviewCommentInfo(**fields)  # type: ignore[arg-type]


class TestRenderCommentBlock:
    """Tests for the single heading-block renderer shared by both dispatch sections."""

    def test_renders_the_exact_eleven_line_block(self) -> None:
        block = _render_comment_block(
            number=2,
            comment=_comment(),
            filename="foo.py",
            fallback_review_id=456,
            emit_source_review_id=False,
        )
        assert block == [
            "",
            "<!-- repair-comment-section -->",
            "### Comment 2 - foo.py:214",
            "",
            "**Link to original comment:** https://github.com/owner/repo/pull/42#discussion_r101",
            "**File:** `src/foo.py`",
            "**Lines:** 210–214",
            "",
            "Comment:",
            "```\nFix the null check here\n```",
        ]

    def test_link_line_is_omitted_without_an_html_url(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url=""),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=False,
        )
        assert not any(line.startswith("**Link to original comment:**") for line in block)

    def test_unlinked_agent_block_emits_agent_comment_id_marker(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url="", id=101),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=False,
        )
        assert any(line == "<!-- agent-comment-id:101 -->" for line in block)

    def test_agent_comment_id_marker_not_emitted_when_html_url_present(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url="https://github.com/owner/repo/pull/42#discussion_r101", id=101),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=False,
        )
        assert not any(line.startswith("<!-- agent-comment-id:") for line in block)

    def test_agent_comment_id_marker_not_emitted_for_author_block(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url="", is_suppressed=True, id=101),
            filename="foo.py",
            fallback_review_id=456,
            emit_source_review_id=True,
        )
        assert not any(line.startswith("<!-- agent-comment-id:") for line in block)

    def test_author_block_emits_the_hidden_source_review_id_marker(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url="", is_suppressed=True),
            filename="foo.py",
            fallback_review_id=456,
            emit_source_review_id=True,
        )
        assert block[3] == "<!-- source-review-id:456 -->"

    def test_marker_prefers_the_comments_own_source_review_id(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url="", is_suppressed=True, source_review_id=123),
            filename="foo.py",
            fallback_review_id=456,
            emit_source_review_id=True,
        )
        assert "<!-- source-review-id:123 -->" in block
        assert "<!-- source-review-id:456 -->" not in block

    def test_marker_is_omitted_when_no_review_id_is_available(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url="", is_suppressed=True),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=True,
        )
        assert not any(line.startswith("<!-- source-review-id:") for line in block)

    def test_marker_is_never_emitted_for_a_code_review_agent_block(self) -> None:
        """Section membership is supplied by the caller, never derived from the block's fields."""
        block = _render_comment_block(
            number=1,
            comment=_comment(html_url="", is_suppressed=True, source_review_id=123),
            filename="foo.py",
            fallback_review_id=456,
            emit_source_review_id=False,
        )
        assert not any(line.startswith("<!-- source-review-id:") for line in block)

    def test_file_level_comment_omits_the_line_suffix_and_the_lines_header(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(line=None, start_line=None),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=False,
        )
        assert "### Comment 1 - foo.py" in block
        assert not any(line.startswith("**Lines:**") for line in block)

    def test_single_line_comment_renders_a_single_number(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(line=42, start_line=None),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=False,
        )
        assert "**Lines:** 42" in block

    def test_lines_header_is_a_single_number_when_start_equals_line(self) -> None:
        block = _render_comment_block(
            number=1,
            comment=_comment(line=42, start_line=42),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=False,
        )
        assert "**Lines:** 42" in block
        assert "**Lines:** 42–42" not in block

    def test_file_metadata_escapes_structural_characters(self) -> None:
        """The renderer applies escaping to path metadata; exact encoding is tested in
        ``test__escape_comment_metadata_text.py``."""
        block = _render_comment_block(
            number=1,
            comment=_comment(path="src/<foo>.py"),
            filename="foo.py",
            fallback_review_id=0,
            emit_source_review_id=False,
        )
        assert not any("<foo>" in line for line in block)
