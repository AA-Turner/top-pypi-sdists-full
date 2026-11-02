"""Tests for the missed-entry parser exports consumed by recovery."""

import agentic_devtools.cli.github.ccr_finding_missed_entries as ccr_finding_missed_entries


def test_recovery_helpers_and_patterns_are_explicit_exports() -> None:
    assert set(ccr_finding_missed_entries.__all__) == {
        "_EXPLANATION_HEADING_RE",
        "_LEGACY_SEVERITY_ENTRY_RE",
        "_independent_legacy_spans",
        "_is_duplicate_picture_legacy_entry",
        "_legacy_severity_location",
    }
