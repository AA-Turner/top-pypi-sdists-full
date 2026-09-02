"""Tests for _usage_from()."""

from types import SimpleNamespace

from agentic_devtools.orchestration.llm.providers.copilot import _usage_from


def test_normalizes_token_counts():
    usage = SimpleNamespace(input_tokens=1, output_tokens=2, total_tokens=3)
    result = _usage_from(SimpleNamespace(usage=usage))
    assert result is not None and result.total_tokens == 3


def test_accepts_direct_usage_event_shape_and_derives_total_tokens():
    result = _usage_from(SimpleNamespace(input_tokens=4, output_tokens=6))
    assert result is not None
    assert result.input_tokens == 4
    assert result.output_tokens == 6
    assert result.total_tokens == 10


def test_returns_none_when_usage_is_absent():
    assert _usage_from(SimpleNamespace(usage=None)) is None


def test_returns_none_when_value_is_none():
    assert _usage_from(None) is None


def test_returns_none_when_counts_are_missing():
    assert _usage_from(SimpleNamespace(usage=SimpleNamespace())) is None
