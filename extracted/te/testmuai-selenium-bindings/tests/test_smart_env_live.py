"""V2-parity smart-variable env injection from the LIVE session.

``{{smart.browser_name|browser_version|os_type|os_version}}`` resolve via
``_resolve_smart`` reading the ``smart_*`` env vars. Those must be populated at
runtime from the live session, mirroring the V2 source ``add_smart_var``:

* browser fields  -> the live ``driver.capabilities`` (the actually-negotiated
  values, e.g. ``"121.0.6167.85"`` — NOT the requested ``"latest"``)
* OS fields       -> the runtime host via the ``platform`` module

Regression: on the deployed binding nothing set ``smart_*`` at all, so every
field resolved to ``""`` and was typed as an empty string.
"""

import os
import platform

import pytest

from testmu_selenium import var
from testmu_selenium._session import _export_smart_env_from_session


@pytest.fixture(autouse=True)
def _clear_smart_env(monkeypatch):
    for key in ("smart_browser_name", "smart_browser_version", "smart_os", "smart_os_version"):
        monkeypatch.delenv(key, raising=False)


class _FakeDriver:
    def __init__(self, capabilities):
        self.capabilities = capabilities


def test_browser_fields_come_from_live_caps(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "version", lambda: "#42-Ubuntu SMP")
    driver = _FakeDriver(
        {
            "browserName": "chrome",
            "browserVersion": "121.0.6167.85",  # negotiated, not "latest"
            "platformName": "Windows 11",
        }
    )

    _export_smart_env_from_session(driver)

    assert os.environ["smart_browser_name"] == "chrome"
    assert os.environ["smart_browser_version"] == "121.0.6167.85"


def test_os_fields_come_from_runtime_host(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "version", lambda: "#42-Ubuntu SMP")

    _export_smart_env_from_session(_FakeDriver({"browserName": "chrome", "browserVersion": "121"}))

    assert os.environ["smart_os"] == "Linux"
    assert os.environ["smart_os_version"] == "#42-Ubuntu SMP"


def test_missing_caps_keys_do_not_raise(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "version", lambda: "v1")

    # A driver whose capabilities lack the browser keys must degrade to "" not crash.
    _export_smart_env_from_session(_FakeDriver({}))

    assert os.environ["smart_browser_name"] == ""
    assert os.environ["smart_browser_version"] == ""
    assert os.environ["smart_os"] == "Linux"


def test_full_resolution_path_returns_live_values(monkeypatch):
    """End-to-end: helper sets env -> _resolve_smart reads it -> var() returns it."""
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "version", lambda: "23.5.0")

    _export_smart_env_from_session(
        _FakeDriver({"browserName": "firefox", "browserVersion": "126.0"})
    )

    assert var("{{smart.browser_name}}") == "firefox"
    assert var("{{smart.browser_version}}") == "126.0"
    assert var("{{smart.os_type}}") == "Darwin"
    assert var("{{smart.os_version}}") == "23.5.0"
