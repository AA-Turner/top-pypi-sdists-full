"""Tests for _author_opening_paragraph()."""

from agentic_devtools.cli.ci.github_provider import _author_opening_paragraph

#: The invariant tail shared by both singular and plural forms of the paragraph.
_TAIL = (
    "so I would like you to evaluate each comment against the codebase and address it with code changes only if "
    "you believe that doing so would increase the overall quality of the code changes in this PR:"
)


class TestAuthorOpeningParagraph:
    """Tests for the ``@copilot`` paragraph opening an author-comment dispatch."""

    def test_single_comment_uses_the_singular_head(self) -> None:
        assert _author_opening_paragraph(1) == (
            "@copilot - please evaluate the following comment that I had about a certain part of the code changes "
            "in this PR. I am unsure whether a change is needed here or not, " + _TAIL
        )

    def test_several_comments_name_the_count_in_the_plural_head(self) -> None:
        assert _author_opening_paragraph(3) == (
            "@copilot - please evaluate the following 3 comments that I had about certain parts of the code "
            "changes in this PR. I am unsure whether changes are needed here or not, " + _TAIL
        )

    def test_both_forms_end_with_the_identical_tail(self) -> None:
        """The shared tail is factored out, so a copy edit can never drift between the two forms."""
        assert _author_opening_paragraph(1).endswith(_TAIL)
        assert _author_opening_paragraph(4).endswith(_TAIL)

    def test_always_opens_on_the_literal_copilot_mention(self) -> None:
        """The dispatch body must begin with ``@copilot`` for reliable session triggering."""
        assert _author_opening_paragraph(1).startswith("@copilot - ")
        assert _author_opening_paragraph(2).startswith("@copilot - ")

    def test_does_not_state_where_decisions_are_recorded(self) -> None:
        """That contract now lives under the section heading, in _author_section_lead_in()."""
        assert "summary comment you post on the PR" not in _author_opening_paragraph(2)
