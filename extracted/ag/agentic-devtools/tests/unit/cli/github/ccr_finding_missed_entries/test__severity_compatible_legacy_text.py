"""Tests for severity-aware structured and legacy finding comparison."""

import re

import pytest

from agentic_devtools.cli.github.ccr_finding_missed_entries import _severity_compatible_legacy_text


@pytest.mark.parametrize(
    ("structured", "legacy", "expected"),
    [
        (None, "", (True, "")),
        (re.match(r".+", "### [P1] Finding"), "Finding details.", (True, "Finding details.")),
        (None, "* [P2] Finding details.", (True, "*  Finding details.")),
        (
            re.match(r".+", "### [P1] Finding"),
            "* [P2] Independent finding.",
            (False, "* [P2] Independent finding."),
        ),
        (
            re.match(r".+", "### [P1] Finding"),
            "* [High] Same-severity finding.",
            (True, "*  Same-severity finding."),
        ),
    ],
)
def test_matches_legacy_text_only_when_severity_is_compatible(
    structured: re.Match[str] | None,
    legacy: str,
    expected: tuple[bool, str],
) -> None:
    assert _severity_compatible_legacy_text(structured, legacy) == expected
