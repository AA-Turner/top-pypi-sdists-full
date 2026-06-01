"""v0.1.155 / #360 — gap-agent stderr UX.

Covers:
- `_emit_dispatch_line` no longer claims "typically 30-90s" (misleading
  on cache hits — customer's gap stage dropped from 1247s to 0.3s after
  the v0.1.153 cache fix but the "30-90s" line still printed).
- `_emit_batch_completion_line` renders per-batch wall-clock so cache
  hits (~0.1s) vs real LLM calls (~30-90s) are visible at a glance.
- TTY-suppression invariant preserved on all the new lines (piped/CI
  output stays clean).
"""

from __future__ import annotations

import sys
from unittest.mock import patch

from efterlev.agents.gap import (
    Batch,
    _emit_batch_completion_line,
    _emit_dispatch_line,
)


def _stub_batch(index: int = 3, total: int = 12) -> Batch:
    # Batch only needs `index` and `total` for the completion-line render —
    # detector input lists can be empty for this test.
    return Batch(index=index, total=total, indicators=[], evidence=[])


def test_dispatch_line_no_longer_promises_30_to_90_seconds(capsys) -> None:
    """The pre-v0.1.155 phrasing said "typically 30-90s" which was a flat
    lie on cache hits. New phrasing is neutral about duration; the per-
    batch completion line reveals timing accurately."""
    with patch.object(sys.stderr, "isatty", return_value=True):
        _emit_dispatch_line(attempt=1, max_attempts=3)
    err = capsys.readouterr().err
    assert "Starting analysis" in err
    assert "30-90s" not in err
    assert "typically" not in err


def test_dispatch_line_retry_attempt_also_drops_duration_claim(capsys) -> None:
    with patch.object(sys.stderr, "isatty", return_value=True):
        _emit_dispatch_line(attempt=2, max_attempts=3)
    err = capsys.readouterr().err
    assert "attempt 2/3" in err
    assert "30-90s" not in err


def test_batch_completion_line_renders_subminute_seconds(capsys) -> None:
    """Sub-minute elapsed → `[gap] Batch 3/12 done in 0.3s` (cache hit)
    or `47.3s` (real call). One decimal of precision so the cache speed-
    up (~0.1s vs ~50s) is unmistakable."""
    with patch.object(sys.stderr, "isatty", return_value=True):
        _emit_batch_completion_line(_stub_batch(3, 12), elapsed=0.34)
    err = capsys.readouterr().err
    assert err == "[gap] Batch 3/12 done in 0.3s\n"

    with patch.object(sys.stderr, "isatty", return_value=True):
        _emit_batch_completion_line(_stub_batch(8, 12), elapsed=47.27)
    err = capsys.readouterr().err
    assert err == "[gap] Batch 8/12 done in 47.3s\n"


def test_batch_completion_line_renders_minute_format_above_60s(capsys) -> None:
    with patch.object(sys.stderr, "isatty", return_value=True):
        _emit_batch_completion_line(_stub_batch(1, 12), elapsed=72.5)
    err = capsys.readouterr().err
    assert err == "[gap] Batch 1/12 done in 1m12s\n"


def test_batch_completion_line_suppressed_when_stderr_not_a_tty(capsys) -> None:
    """Pipe/CI output stays clean — same contract as the other progress
    lines (`_emit_dispatch_line`, `_emit_batch_dispatch_line`)."""
    with patch.object(sys.stderr, "isatty", return_value=False):
        _emit_batch_completion_line(_stub_batch(3, 12), elapsed=0.3)
    err = capsys.readouterr().err
    assert err == ""


def test_dispatch_line_suppressed_when_stderr_not_a_tty(capsys) -> None:
    with patch.object(sys.stderr, "isatty", return_value=False):
        _emit_dispatch_line(attempt=1, max_attempts=3)
        _emit_dispatch_line(attempt=2, max_attempts=3)
    err = capsys.readouterr().err
    assert err == ""
