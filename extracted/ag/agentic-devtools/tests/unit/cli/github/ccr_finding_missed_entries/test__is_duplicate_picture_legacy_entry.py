"""Tests for picture-summary and legacy-entry reconciliation."""

import re

import pytest

from agentic_devtools.cli.github.ccr_finding_missed_entries import (
    _LEGACY_SEVERITY_ENTRY_RE,
    _is_duplicate_picture_legacy_entry,
)
from agentic_devtools.cli.github.ccr_review_format import CCRFinding


@pytest.mark.parametrize(
    (
        "picture",
        "previous_severity",
        "previous_path",
        "previous_line",
        "legacy_location",
        "legacy_severity",
        "expected",
    ),
    (
        (True, "MEDIUM", "src/a.py", 10, "src/a.py:10", "P2", True),
        (True, "P2", "src/a.py", None, "src/a.py", "Medium", True),
        (True, "P2", "src/a.py", 10, "src/b.py:10", "P2", False),
        (True, "P2", "src/a.py", 10, "src/a.py:11", "P2", False),
        (True, "P2", "src/a.py", 10, "src/a.py:10", "P1", False),
        (False, "P2", "src/a.py", 10, "src/a.py:10", "P2", False),
    ),
)
def test_is_duplicate_picture_legacy_entry(
    picture: bool,
    previous_severity: str,
    previous_path: str,
    previous_line: int | None,
    legacy_location: str,
    legacy_severity: str,
    expected: bool,
) -> None:
    finding = CCRFinding(
        section="previously_missed",
        ordinal=1,
        severity=previous_severity,
        title="Guard the response",
        body="<summary><picture></picture>Guard the response</summary>" if picture else "Guard the response",
        path=previous_path,
        line=previous_line,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )
    legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match(f"**{legacy_location}** [{legacy_severity}] Guard the response")
    assert isinstance(legacy_entry, re.Match)

    assert _is_duplicate_picture_legacy_entry(finding, legacy_entry, "") is expected


def test_different_title_does_not_deduplicate_picture_finding() -> None:
    finding = CCRFinding(
        section="previously_missed",
        ordinal=1,
        severity="P1",
        title="Guard the response",
        body="<summary><picture></picture>Guard the response</summary>",
        path="src/a.py",
        line=10,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )
    legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match("**src/a.py:10** [P1] Preserve the exception")
    assert isinstance(legacy_entry, re.Match)

    assert _is_duplicate_picture_legacy_entry(finding, legacy_entry, "") is False


def test_different_explanation_does_not_deduplicate_picture_finding() -> None:
    finding = CCRFinding(
        section="previously_missed",
        ordinal=1,
        severity="P1",
        title="Guard the response",
        body="<summary><picture></picture>Guard the response</summary>\nThe response is missing.",
        path="src/a.py",
        line=10,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )
    legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match("**src/a.py:10** [P1] Guard the response")
    assert isinstance(legacy_entry, re.Match)

    assert _is_duplicate_picture_legacy_entry(finding, legacy_entry, "A different explanation.") is False


def test_zero_width_path_alias_deduplicates_picture_finding() -> None:
    finding = CCRFinding(
        section="previously_missed",
        ordinal=1,
        severity="P1",
        title="Guard the response",
        body="<summary><picture></picture>Guard the response</summary>",
        path="src/\u200ba.py",
        line=10,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )
    legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match("**src/a.py:10** [P1] Guard the response")
    assert isinstance(legacy_entry, re.Match)

    assert _is_duplicate_picture_legacy_entry(finding, legacy_entry, "") is True
