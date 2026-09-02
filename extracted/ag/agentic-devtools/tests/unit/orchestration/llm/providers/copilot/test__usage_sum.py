"""Tests for _usage_sum."""

from __future__ import annotations

from types import SimpleNamespace

from agentic_devtools.orchestration.llm.providers.copilot import _usage_sum


def test_sums_complete_usage_events_and_skips_invalid_ones():
    usage = _usage_sum(
        [
            SimpleNamespace(input_tokens=2, output_tokens=3, total_tokens=5),
            SimpleNamespace(input_tokens="bad"),
            SimpleNamespace(input_tokens=4, output_tokens=1, total_tokens=5),
        ]
    )

    assert usage is not None
    assert usage.input_tokens == 6
    assert usage.output_tokens == 4
    assert usage.total_tokens == 10


def test_returns_none_when_no_complete_usage_events_exist():
    assert _usage_sum([SimpleNamespace(input_tokens="bad")]) is None
