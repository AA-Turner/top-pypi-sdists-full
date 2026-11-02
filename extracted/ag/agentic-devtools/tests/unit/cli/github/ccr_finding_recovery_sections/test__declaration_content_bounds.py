"""Tests for bounds of declared finding section contents."""

import re

from agentic_devtools.cli.github.ccr_finding_recovery_sections import _declaration_content_bounds


def test_previously_missed_summary_without_details_has_empty_content() -> None:
    body = "<summary>Previously missed (1)</summary>\n### [P1] Finding\n"
    declaration = re.search(r"<summary>.*?</summary>", body)
    assert declaration is not None

    content_start, content_end = _declaration_content_bounds(body, body, [declaration], 0)

    assert content_start == body.index("\n", declaration.end()) + 1
    assert content_end == content_start


def test_summary_inside_details_ends_at_its_closing_details_tag() -> None:
    body = "<details>\n<summary>Previously missed (1)</summary>\nFinding\n</details>\n"
    declaration = re.search(r"<summary>.*?</summary>", body)
    assert declaration is not None

    content_start, content_end = _declaration_content_bounds(body, body, [declaration], 0)

    assert content_start == body.index("\n", declaration.end()) + 1
    assert content_end == body.index("</details>")


def test_section_heading_content_stops_at_next_heading_of_same_level() -> None:
    body = "## Suppressed comments (1)\nFinding\n## Following section\nOther text"
    declaration = re.match(r"## Suppressed comments \(1\)", body)
    assert declaration is not None

    content_start, content_end = _declaration_content_bounds(body, body, [declaration], 0)

    assert body[content_start:content_end] == "Finding\n"


def test_declaration_without_a_newline_has_empty_content() -> None:
    body = "### Suppressed comments (1)"
    declaration = re.match(r"### Suppressed comments \(1\)", body)
    assert declaration is not None

    assert _declaration_content_bounds(body, body, [declaration], 0) == (len(body), len(body))
