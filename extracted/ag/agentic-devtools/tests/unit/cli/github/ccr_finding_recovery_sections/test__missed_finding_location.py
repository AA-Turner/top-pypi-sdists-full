"""Tests for file and line metadata in missed findings."""

from agentic_devtools.cli.github.ccr_finding_recovery_sections import _missed_finding_location


def test_standalone_backticked_location_provides_path_and_line() -> None:
    assert _missed_finding_location("`src/client.py:42`\nThe response is missing.") == ("src/client.py", 42)


def test_unquoted_file_and_separate_line_metadata_are_normalized() -> None:
    assert _missed_finding_location(r"**File:** src/foo\_bar.py" + "\n**Line:** 42") == ("src/foo_bar.py", 42)


def test_legacy_severity_entry_location_provides_path_and_line() -> None:
    assert _missed_finding_location(r"**src/foo\_bar.py:42** [P1] Guard the response") == ("src/foo_bar.py", 42)


def test_backticked_legacy_severity_location_preserves_code_span_contents() -> None:
    assert _missed_finding_location(r"**`src/foo\_bar.py:42`** [P1] Guard the response") == (
        r"src/foo\_bar.py",
        42,
    )


def test_structured_location_takes_precedence_over_later_legacy_severity_header() -> None:
    block = "**File:** `src/a.py`\n**Line:** 10\n**src/b.py:20** [P2] Other finding"

    assert _missed_finding_location(block) == ("src/a.py", 10)


def test_missing_location_uses_the_unknown_file() -> None:
    assert _missed_finding_location("The finding has no location metadata.") == ("(unknown file)", None)
