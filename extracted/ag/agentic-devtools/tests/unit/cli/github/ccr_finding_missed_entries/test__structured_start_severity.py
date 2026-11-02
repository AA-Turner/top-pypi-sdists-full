"""Tests for severity extraction from structured finding headers."""

import re

import pytest

from agentic_devtools.cli.github.ccr_finding_missed_entries import _structured_start_severity


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("### [P1] Finding", "P1"),
        ('<summary><picture alt="High severity"></picture>Finding</summary>', "HIGH"),
        ("<summary><picture></picture>[P2] Finding</summary>", "P2"),
        ('<summary><picture alt="No level"></picture>Finding</summary>', ""),
    ],
)
def test_extracts_supported_structured_header_severity(line: str, expected: str) -> None:
    assert _structured_start_severity(re.match(r".+", line)) == expected


def test_returns_empty_when_structured_header_is_missing() -> None:
    assert _structured_start_severity(None) == ""
