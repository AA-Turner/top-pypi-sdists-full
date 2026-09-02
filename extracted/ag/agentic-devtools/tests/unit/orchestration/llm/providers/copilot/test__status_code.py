"""Tests for _status_code()."""

from types import SimpleNamespace

from agentic_devtools.orchestration.llm.providers.copilot import _status_code


def test_returns_none_for_exception_without_status():
    assert _status_code(RuntimeError()) is None


def test_reads_status_code_from_response_attribute():
    assert _status_code(SimpleNamespace(response=SimpleNamespace(status_code=503))) == 503


def test_reads_status_code_attribute_directly():
    assert _status_code(SimpleNamespace(status_code=429)) == 429
