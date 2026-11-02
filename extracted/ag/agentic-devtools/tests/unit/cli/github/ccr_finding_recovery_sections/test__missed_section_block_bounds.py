"""Tests for missed-section boundaries around legacy headers."""

import re

from agentic_devtools.cli.github.ccr_finding_recovery_sections import _missed_section_block_bounds


def test_empty_gap_after_legacy_header_includes_header_in_suppressed_bounds() -> None:
    content = "intro\n**src/a.py:10**\nFinding details\n"
    header = re.search(r"\*\*src/a.py:10\*\*", content)
    assert header is not None
    start = header.end() + 1

    assert _missed_section_block_bounds(content, [0, start], 1, "suppressed", {header.start(): header}) == (
        header.start(),
        len(content),
    )


def test_nonempty_gap_after_legacy_header_keeps_the_finding_start() -> None:
    content = "intro\n**src/a.py:10**\nlegacy prose\nFinding details\n"
    header = re.search(r"\*\*src/a.py:10\*\*", content)
    assert header is not None
    start = content.index("Finding details")

    assert _missed_section_block_bounds(content, [0, start], 1, "suppressed", {header.start(): header}) == (
        start,
        len(content),
    )
