"""headers() tags AI-API calls with the test and instruction they belong to.

Mirrors playwright-python's test_http_test_id_header.py — the attribution
contract has to hold identically in both bindings or a mobile session's spend
lands unattributed.
"""
import pytest

from testmu_appium import _config
from testmu_appium._helpers._http import headers
from testmu_appium._step import StepInfo, _current_step, set_instruction_id


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    monkeypatch.delenv("TESTMUAI_TEST_ID", raising=False)
    monkeypatch.setitem(_config._config, "test_id", "")
    token = _current_step.set(None)
    instr = set_instruction_id("")
    yield
    _current_step.reset(token)
    _current_instruction_reset(instr)


def _current_instruction_reset(token):
    from testmu_appium._step import _current_instruction_id
    _current_instruction_id.reset(token)


def test_env_test_id_is_sent(monkeypatch):
    monkeypatch.setenv("TESTMUAI_TEST_ID", "env-test")
    assert headers()["x-test-id"] == "env-test"


def test_configure_wins_over_env(monkeypatch):
    monkeypatch.setenv("TESTMUAI_TEST_ID", "env-test")
    monkeypatch.setitem(_config._config, "test_id", "cfg-test")
    assert headers()["x-test-id"] == "cfg-test"


def test_header_omitted_when_neither_is_set():
    sent = headers()
    assert "x-test-id" not in sent
    assert sent["x-source"] == "local"


def test_instruction_id_is_sent():
    set_instruction_id("instr-1")
    assert headers()["x-instruction-id"] == "instr-1"


def test_instruction_header_omitted_when_unset():
    assert "x-instruction-id" not in headers()


def test_active_step_wins_over_the_ambient_id():
    """An explicit per-step id must beat leftover ambient state."""
    set_instruction_id("ambient")
    _current_step.set(StepInfo(description="s", instruction_id="from-step"))
    assert headers()["x-instruction-id"] == "from-step"
