"""Tests for summary declaration boundaries."""

import re

from agentic_devtools.cli.github.ccr_finding_recovery_sections import _summary_declaration_bounds


def _summary_match(text: str) -> re.Match[str]:
    match = re.search(r"<summary>.*?</summary>", text)
    assert match is not None
    return match


def test_summary_in_details_ends_at_its_closing_details_tag() -> None:
    text = "<details><summary>Suppressed (1)</summary>finding</details>after"
    declaration = _summary_match(text)

    assert _summary_declaration_bounds(text, declaration, len(text)) == (text.rindex("</details>"), True)


def test_nested_details_are_skipped_until_the_containing_details_closes() -> None:
    text = "<details><summary>Outer</summary><details>inner</details>end</details>"
    declaration = _summary_match(text)

    assert _summary_declaration_bounds(text, declaration, len(text)) == (text.rindex("</details>"), True)


def test_summary_without_details_ends_at_next_declaration() -> None:
    text = "<summary>Previously missed (1)</summary>\nfinding\n"
    declaration = _summary_match(text)

    assert _summary_declaration_bounds(text, declaration, len(text)) == (len(text), False)


def test_unclosed_details_is_bounded_by_the_next_declaration() -> None:
    text = "<details><summary>Suppressed (1)</summary>\nfinding"
    declaration = _summary_match(text)
    next_declaration = len(text) - len("finding")

    assert _summary_declaration_bounds(text, declaration, next_declaration) == (next_declaration, True)
