"""Tests for consuming one unified-diff hunk line."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _consume_hunk_line


def test_returns_named_hunk_line_state_for_content() -> None:
    state = _consume_hunk_line("-old", 1, 0, 0, False)

    assert state is not None
    assert state.old_remaining == 0
    assert state.new_remaining == 0
    assert state.changed_line_count == 1
    assert state.previous_content


def test_rejects_orphan_marker_and_overconsumed_line() -> None:
    assert _consume_hunk_line(r"\ No newline at end of file", 1, 1, 0, False) is None
    assert _consume_hunk_line("-old", 0, 1, 0, False) is None
