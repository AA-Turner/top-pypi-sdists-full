"""Tests for extracting legacy headers from suppressed sections."""

from agentic_devtools.cli.github.ccr_finding_recovery_sections import _suppressed_entry_headers


def test_explanatory_standalone_location_is_not_an_entry_header() -> None:
    block = "This location is only an example.\n`src/a.py:10`\n"

    assert _suppressed_entry_headers(block) == {}
