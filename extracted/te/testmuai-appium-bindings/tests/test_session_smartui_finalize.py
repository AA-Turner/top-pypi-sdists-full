"""run() teardown finalizes the SmartUI build.

An unfinalized build never completes on the SmartUI side, so the session
lifecycle must call finalize_smartui() on the way out — pass or fail alike.
"""
import types

import pytest

from testmu_appium import _session
from testmu_appium._helpers import smartui as smartui_mod


class _FakeDriver:
    def quit(self):
        pass


class _FakeReporter:
    def set_driver(self, driver):
        pass

    def pass_test(self):
        pass

    def fail_test(self, error):
        pass


@pytest.fixture
def _stubbed_session(monkeypatch):
    monkeypatch.setattr(
        _session, "webdriver",
        types.SimpleNamespace(Remote=lambda command_executor, options: _FakeDriver()),
    )
    monkeypatch.setattr(_session, "build_options", lambda platform: None)
    monkeypatch.setattr(_session, "reporter", lambda: _FakeReporter())
    monkeypatch.setattr(_session, "_reset_reporter", lambda: None)
    monkeypatch.setattr(_session, "_apply_smart_gate", lambda: None)
    monkeypatch.setattr(_session, "_settle_before_teardown", lambda driver: None)


def _started_fake_build():
    session = types.SimpleNamespace(stop_count=0)
    session.stop = lambda: setattr(session, "stop_count", session.stop_count + 1)
    session.build_data = types.SimpleNamespace(name="build-7", build_id="b7")
    return session


def test_run_finalizes_smartui_on_success(_stubbed_session):
    fake = _started_fake_build()
    smartui_mod._active = fake
    _session.run(lambda driver: None)
    assert fake.stop_count == 1
    assert smartui_mod._active is None


def test_run_finalizes_smartui_when_the_body_raises(_stubbed_session):
    fake = _started_fake_build()
    smartui_mod._active = fake
    with pytest.raises(RuntimeError):
        _session.run(lambda driver: (_ for _ in ()).throw(RuntimeError("body failed")))
    assert fake.stop_count == 1
    assert smartui_mod._active is None
