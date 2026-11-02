"""Tests for consuming a complete unified-diff hunk."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _consume_hunk


def test_returns_named_hunk_result() -> None:
    result = _consume_hunk(["@@ -1 +1 @@", "-old", "+new"], 0)

    assert result is not None
    assert result.next_index == 3
    assert result.changed_line_count == 2


def test_rejects_malformed_or_truncated_hunks() -> None:
    assert _consume_hunk(["@@ malformed"], 0) is None
    assert _consume_hunk(["@@ -1 +1 @@", "-old"], 0) is None
