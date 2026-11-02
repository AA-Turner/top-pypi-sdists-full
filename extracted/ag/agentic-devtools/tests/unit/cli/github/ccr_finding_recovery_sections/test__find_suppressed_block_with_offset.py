"""Tests for _find_suppressed_block_with_offset()."""

from agentic_devtools.cli.github.ccr_review_format import _find_suppressed_block_with_offset


def test_finds_the_source_offset_of_repeated_heading_content() -> None:
    body = "Repeated finding.\n\n### Suppressed comments (1)\n\nRepeated finding.\n"

    result = _find_suppressed_block_with_offset(body, source_order=True)

    assert result == ("Repeated finding.", body.rindex("Repeated finding."), 1)


def test_finds_the_source_offset_of_legacy_details_content() -> None:
    body = "Repeated finding.\n\n<details><summary>Suppressed comments (1)</summary>\n\nRepeated finding.\n</details>"

    result = _find_suppressed_block_with_offset(body, source_order=True)

    assert result == ("Repeated finding.", body.rindex("Repeated finding."), 1)
