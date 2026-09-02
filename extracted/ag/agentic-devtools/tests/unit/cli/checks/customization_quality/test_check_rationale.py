"""Tests for the Q8 rationale rule."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.customization_quality import check_rationale
from tests.unit.cli.checks.customization_quality._support import make_unit


class TestCheckRationale:
    @pytest.mark.parametrize("marker", ["because", "so that", "otherwise", "Rationale:"])
    def test_accepts_a_prohibition_that_states_its_reason(self, marker: str) -> None:
        """Any of the four rationale markers satisfies the rule."""
        unit = make_unit(body=f"NEVER edit the generated file {marker} it is rewritten on every build.\n")

        assert check_rationale(unit) == []

    def test_ignores_blocks_without_a_prohibition(self) -> None:
        """A block with no MUST, NEVER or DO NOT is not a prohibition block."""
        assert check_rationale(make_unit(body="Run the check before pushing.\n")) == []

    @pytest.mark.parametrize("token", ["MUST", "NEVER", "DO NOT"])
    def test_flags_a_prohibition_without_a_reason(self, token: str) -> None:
        """Each prohibition token requires a reason in the same block."""
        violations = check_rationale(make_unit(body=f"You {token} edit the generated file.\n"))

        assert [v.rule for v in violations] == ["Q8"]

    def test_requires_the_reason_in_the_same_block(self) -> None:
        """A reason in a neighbouring block does not satisfy the rule."""
        unit = make_unit(body="You MUST edit the generated file.\n\nThis is so that the build stays green.\n")

        assert len(check_rationale(unit)) == 1

    def test_scans_frontmatter_for_prohibition_tokens(self) -> None:
        """A MUST/NEVER/DO NOT in frontmatter must also state its reason."""
        frontmatter_source = "---\ndescription: Users MUST edit the manifest.\n---\n"
        unit = make_unit(source=frontmatter_source, body="Normal prose.\n")

        violations = check_rationale(unit)

        assert [v.rule for v in violations] == ["Q8"]

    def test_accepts_frontmatter_prohibition_with_reason(self) -> None:
        """Frontmatter with a prohibition and a rationale marker passes Q8."""
        frontmatter_source = "---\ndescription: Users MUST edit the manifest because it is authoritative.\n---\n"
        unit = make_unit(source=frontmatter_source, body="Normal prose.\n")

        assert check_rationale(unit) == []

    def test_ignores_words_that_only_contain_a_prohibition_token(self) -> None:
        """Substring matches such as ``MUSTARD`` and ``DO NOTHING`` are not Q8 prohibitions."""
        unit = make_unit(body="Serve MUSTARD now.\n\nDO NOTHING until the reviewer arrives.\n")

        assert check_rationale(unit) == []

    def test_frontmatter_prohibition_cannot_borrow_rationale_from_adjacent_body(self) -> None:
        """A rationale in the first body paragraph must not satisfy a MUST in the frontmatter.

        When there is no blank line between the closing ``---`` and the first body
        heading, the old ``_blocks(unit.source)`` approach merged them into one block.
        The fix processes frontmatter and body as independent block streams so that
        the rationale in the body cannot cancel the violation in the frontmatter.
        """
        # No blank line between frontmatter and body — previously would merge them.
        frontmatter_source = "---\ndescription: Users MUST edit the manifest.\n---\n"
        body = "## When to use\nDo this because it is required.\n"
        unit = make_unit(source=frontmatter_source + body, body=body)

        violations = check_rationale(unit)

        assert [v.rule for v in violations] == ["Q8"]

    def test_truncates_a_long_block_in_the_message(self) -> None:
        """Long blocks are excerpted so the report stays readable."""
        unit = make_unit(body="You MUST " + "keep this rule in mind " * 20)

        assert check_rationale(unit)[0].message.endswith("…")
