"""Tests for the Q10 prohibition-bullet rule."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import MAX_PROHIBITION_BULLETS, check_prohibitions
from tests.unit.cli.checks.customization_quality._support import make_unit

BULLET = "- Do not edit the generated file.\n"


class TestCheckProhibitions:
    def test_accepts_up_to_two_prohibition_bullets(self) -> None:
        """Two boundaries per file is the budget, so two bullets pass."""
        assert check_prohibitions(make_unit(body=BULLET * MAX_PROHIBITION_BULLETS)) == []

    def test_flags_a_third_prohibition_bullet(self) -> None:
        """A third prohibition bullet is over the cap."""
        violations = check_prohibitions(make_unit(body="- never a\n* must not b\n1. do not c\n"))

        assert [v.rule for v in violations] == ["Q10"]
        assert "3 prohibition bullets" in violations[0].message

    def test_counts_ordered_list_items_with_parenthesis_delimiter(self) -> None:
        """CommonMark allows ``1)`` as well as ``1.`` for ordered list items."""
        violations = check_prohibitions(make_unit(body="1) must not a\n2) must not b\n3) must not c\n"))

        assert [v.rule for v in violations] == ["Q10"]
        assert "3 prohibition bullets" in violations[0].message

    def test_ignores_prohibitions_in_prose(self) -> None:
        """Only bullets count; prose prohibitions are Q8's business."""
        assert check_prohibitions(make_unit(body="Do not do this. Do not do that. Do not do the other.\n")) == []

    def test_ignores_bullets_without_a_prohibition(self) -> None:
        """A plain bullet list is not a set of boundaries."""
        assert check_prohibitions(make_unit(body="- run the check\n- push the branch\n- open the PR\n")) == []

    def test_ignores_bullets_whose_words_only_contain_a_prohibition_phrase(self) -> None:
        """Whole-phrase matching avoids false positives such as ``must notice`` and ``do nothing``."""
        body = "- You must notice the warning.\n- Do nothing until ready.\n- The task is prohibitedly hard.\n"

        assert check_prohibitions(make_unit(body=body)) == []

    def test_counts_a_multiline_bullet_when_the_prohibition_is_on_a_continuation_line(self) -> None:
        """Continuation lines belong to the same Markdown list item for Q10."""
        body = (
            "- For generated files,\n  do not edit them.\n"
            "- In the release branch,\n  do not rewrite the notes.\n"
            "- For archived prompts,\n  do not rename them.\n"
        )

        violations = check_prohibitions(make_unit(body=body))

        assert [v.rule for v in violations] == ["Q10"]
        assert "3 prohibition bullets" in violations[0].message

    def test_ignores_a_prohibition_in_a_following_outdented_paragraph(self) -> None:
        """A list item stops before a later paragraph at the same indentation."""
        body = "- Track the generated files.\n\nDo not edit them outside the release step.\n"

        assert check_prohibitions(make_unit(body=body)) == []

    def test_counts_a_multiline_bullet_across_a_blank_continuation_line(self) -> None:
        """Blank continuation lines do not terminate a Markdown list item."""
        body = (
            "- For generated files,\n\n  do not edit them.\n"
            "- For archived prompts,\n\n  do not rename them.\n"
            "- For snapshots,\n\n  do not rewrite them.\n"
        )

        violations = check_prohibitions(make_unit(body=body))

        assert [v.rule for v in violations] == ["Q10"]

    def test_ignores_prohibition_bullets_inside_a_fenced_code_block(self) -> None:
        """Fenced example code containing ``do not`` bullets does not count toward Q10."""
        body = (
            "An example showing prohibited patterns:\n\n"
            "```\n"
            "- Do not edit the generated file.\n"
            "- Do not push to main directly.\n"
            "- Do not rebase after sharing.\n"
            "```\n"
        )

        assert check_prohibitions(make_unit(body=body)) == []

    def test_counts_nested_prohibition_bullets_independently(self) -> None:
        """Each nested bullet is a separate list item; three nested prohibitions fail Q10."""
        body = (
            "- Parent item\n"
            "  - Do not edit the generated file.\n"
            "  - Do not push to main directly.\n"
            "  - Do not rebase after sharing.\n"
        )

        violations = check_prohibitions(make_unit(body=body))

        assert [v.rule for v in violations] == ["Q10"]
        assert "3 prohibition bullets" in violations[0].message
