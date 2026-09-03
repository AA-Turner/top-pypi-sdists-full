"""Unit tests for the last-event timestamp parser."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.trace import _last_event_timestamp


def test_last_event_timestamp_handles_blank_lines_and_malformed_json() -> None:
    """Blank, malformed, and incomplete entries are skipped."""
    assert _last_event_timestamp("") is None
    assert _last_event_timestamp("\n\n") is None
    assert _last_event_timestamp("not-json\n") is None
    assert _last_event_timestamp('{"timestamp":"not-a-date"}\n') is None
    assert _last_event_timestamp('{"other":"x"}\n') is None
    assert _last_event_timestamp('{"timestamp":42}\n') is None
    result = _last_event_timestamp('{"timestamp":"2024-06-01T10:00:00+00:00","other":"x"}\n')
    assert result is not None
    assert result.isoformat() == "2024-06-01T10:00:00+00:00"
