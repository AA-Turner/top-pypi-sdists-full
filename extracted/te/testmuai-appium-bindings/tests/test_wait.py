"""DRIVER-mode wait verb: fixed sleep, ms wins over seconds."""
import logging

import pytest

from testmu_appium._helpers import wait as wait_mod
from testmu_appium._helpers.wait import wait


@pytest.fixture(autouse=True)
def _fake_sleep(monkeypatch):
    """Never actually sleep in the suite — record calls instead."""
    calls = []
    monkeypatch.setattr(wait_mod.time, "sleep", lambda seconds: calls.append(seconds))
    return calls


def test_wait_sleeps_for_seconds(_fake_sleep):
    wait(object(), 2.5)
    assert _fake_sleep == [2.5]


def test_wait_sleeps_for_ms_converted_to_seconds(_fake_sleep):
    wait(object(), ms=1500)
    assert _fake_sleep == [1.5]


def test_ms_wins_when_both_given(_fake_sleep):
    wait(object(), 10, ms=250)
    assert _fake_sleep == [0.25]


def test_neither_given_raises():
    with pytest.raises(ValueError):
        wait(object())


@pytest.mark.parametrize("seconds", [-1, -0.5])
def test_negative_seconds_raises(seconds):
    with pytest.raises(ValueError):
        wait(object(), seconds)


def test_negative_ms_raises():
    with pytest.raises(ValueError):
        wait(object(), ms=-100)


def test_zero_is_a_valid_duration(_fake_sleep):
    wait(object(), 0)
    assert _fake_sleep == [0]


def test_wait_logs_at_info(_fake_sleep, caplog):
    caplog.set_level(logging.INFO, logger="testmu_appium")
    wait(object(), 1, description="let the toast dismiss")
    assert "1" in caplog.text
    assert "let the toast dismiss" in caplog.text
