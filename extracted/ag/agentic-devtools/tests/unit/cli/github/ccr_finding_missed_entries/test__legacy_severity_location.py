"""Tests for legacy severity-entry location parsing."""

import re

import pytest

from agentic_devtools.cli.github.ccr_finding_missed_entries import (
    _LEGACY_SEVERITY_ENTRY_RE,
    _legacy_severity_location,
)


@pytest.mark.parametrize(
    ("entry", "expected"),
    (
        (r"**`src/foo\_bar.py:42`** [P1] Guard the response", (r"src/foo\_bar.py", 42)),
        (r"**src/foo\_bar.py:42** [P1] Guard the response", ("src/foo_bar.py", 42)),
        ("**src/foo.py** [P1] Guard the response", ("src/foo.py", None)),
    ),
)
def test_legacy_severity_location(entry: str, expected: tuple[str, int | None]) -> None:
    legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match(entry)
    assert isinstance(legacy_entry, re.Match)

    assert _legacy_severity_location(legacy_entry) == expected
