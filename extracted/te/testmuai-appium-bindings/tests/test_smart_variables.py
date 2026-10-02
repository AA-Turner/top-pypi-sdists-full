"""The device- and app-scoped `{{smart.*}}` names.

These are facts about the session under test — which OS, which app, which way
up — so unlike a date or a random they cannot be computed. They reach the
resolver from one of two places depending on who opened the session:

    exported test  → this binding opened it, and seeded the env at session start
    hosted runtime → the host opened it, and supplies them in the variable store

An assertion authored against one of these re-evaluates on replay, so a name
that resolves to nothing compares an empty string against the recorded value
and fails a check whose values match. That is the bug these pin.
"""
import os

import pytest

from testmu_appium import _config, _session, _vars
from testmu_appium._helpers.verify_assertion import verify_assertion

_SESSION_NAMES = ("device_name", "device_os", "device_os_version",
                  "app_package_name", "app_version")


@pytest.fixture(autouse=True)
def _clean_variable_state(monkeypatch):
    """Both supply routes are process-global; neither may leak between tests.

    conftest's `_isolate_environ` already swaps os.environ for a copy, so the
    pops below cannot escape this test.
    """
    monkeypatch.setattr(_vars, "_variable_store", {})
    for name in _SESSION_NAMES:
        os.environ.pop(_vars._SESSION_SMART_ENV[name], None)
    yield


class TestSuppliedByTheHost:
    """The host runtime owns the session, so the seeding never ran."""

    @pytest.mark.parametrize("name", _SESSION_NAMES)
    def test_the_store_answers_a_session_scoped_name(self, name):
        _vars._variable_store[f"smart.{name}"] = "supplied"
        assert _vars.var("{{smart.%s}}" % name) == "supplied"

    def test_an_assertion_over_a_supplied_name_passes(self):
        """The reported failure, end to end: the recorded check holds the raw
        template, and only the resolver can turn it back into a comparison."""
        _vars._variable_store["smart.device_os"] = "ios"
        result = verify_assertion(None, return_result=True, tree={
            "claim": "os name is {{smart.device_os}}",
            "composite_operator": "and",
            "sub_checks": [{
                "description": "os name is {{smart.device_os}}",
                "extracted_value": "{{smart.device_os}}",
                "expected_value": "ios",
                "operator": "equals",
                "transforms": ["strip", "lowercase"],
                "json_path": None,
            }],
        })
        assert result["status"] == "passed"
        assert result["sub_results"][0]["extracted_value"] == "ios"

    def test_a_supplied_name_survives_embedding(self):
        _vars._variable_store["smart.device_os"] = "ios"
        assert _vars.var("running on {{smart.device_os}} today") == "running on ios today"


class TestSeededFromTheSession:
    """This binding opened the session — the standalone/exported case."""

    @pytest.mark.parametrize("name", _SESSION_NAMES)
    def test_the_seeded_env_answers(self, name, monkeypatch):
        monkeypatch.setenv(_vars._SESSION_SMART_ENV[name], "seeded")
        assert _vars.var("{{smart.%s}}" % name) == "seeded"

    def test_the_session_wins_over_the_store(self, monkeypatch):
        """A value read off the live session outranks one handed in: the host
        supplies these only because it opened the session itself, so the two
        never disagree unless the handed-in one is stale."""
        monkeypatch.setenv("smart_device_os", "ios")
        _vars._variable_store["smart.device_os"] = "android"
        assert _vars.var("{{smart.device_os}}") == "ios"

    def test_session_start_seeds_from_config_and_capabilities(self, monkeypatch):
        monkeypatch.setitem(_session._config._config, "platform", "ios")
        monkeypatch.setitem(_session._config._config, "platform_version", "18.2")
        monkeypatch.setitem(_session._config._config, "device_name", "iPhone 15")
        monkeypatch.setitem(_session._config._config, "app_id", "com.example.app")

        class _Driver:
            capabilities = {"appVersion": "3.1.0", "platformName": "iOS"}

        _session._export_smart_env_from_session(_Driver())
        assert _vars.var("{{smart.device_os}}") == "ios"
        assert _vars.var("{{smart.device_os_version}}") == "18.2"
        assert _vars.var("{{smart.device_name}}") == "iPhone 15"
        assert _vars.var("{{smart.app_package_name}}") == "com.example.app"
        assert _vars.var("{{smart.app_version}}") == "3.1.0"

    def test_a_capability_fills_what_the_config_does_not_name(self, monkeypatch):
        monkeypatch.setitem(_session._config._config, "platform", "")
        monkeypatch.setitem(_session._config._config, "app_id", "")

        class _Driver:
            capabilities = {"platformName": "Android", "appPackage": "com.example.app"}

        _session._export_smart_env_from_session(_Driver())
        assert _vars.var("{{smart.device_os}}") == "Android"
        assert _vars.var("{{smart.app_package_name}}") == "com.example.app"


def _fake_driver(module, **attrs):
    """A stand-in driver. ``module`` is what decides whether it is asked at all
    — a desktop WebDriver carries an `orientation` property too."""
    return type("_Driver", (), {"__module__": module, **attrs})()


class TestOrientation:
    """The one session fact that moves while the run is in progress."""

    def test_it_is_read_from_the_live_driver(self, monkeypatch):
        monkeypatch.setattr(
            "testmu_appium._helpers.driver.get_driver",
            lambda *a, **k: _fake_driver("appium.webdriver", orientation="LANDSCAPE"))
        assert _vars.var("{{smart.device_orientation}}") == "LANDSCAPE"

    def test_it_is_never_frozen_at_session_start(self, monkeypatch):
        """A rotate-then-assert test has to see the rotation, so the driver is
        asked again on every resolution rather than once."""
        facing = {"now": "PORTRAIT"}
        monkeypatch.setattr(
            "testmu_appium._helpers.driver.get_driver",
            lambda *a, **k: _fake_driver(
                "appium.webdriver",
                orientation=property(lambda self: facing["now"])))
        assert _vars.var("{{smart.device_orientation}}") == "PORTRAIT"
        facing["now"] = "LANDSCAPE"
        assert _vars.var("{{smart.device_orientation}}") == "LANDSCAPE"

    def test_a_desktop_driver_is_never_asked(self, monkeypatch):
        """Selenium's WebDriver carries the same property, and asking costs a
        round trip every browser rejects. The desktop copy of this file must
        stay free of that."""
        asked = []

        class _Web:
            @property
            def orientation(self):
                asked.append(True)
                return "PORTRAIT"

        _Web.__module__ = "selenium.webdriver.remote.webdriver"
        monkeypatch.setattr(
            "testmu_appium._helpers.driver.get_driver", lambda *a, **k: _Web())
        assert _vars.var("{{smart.device_orientation}}") == ""
        assert asked == [], "a browser session was asked for its orientation"

    def test_a_driverless_session_falls_back_to_the_store(self, monkeypatch):
        monkeypatch.setattr(
            "testmu_appium._helpers.driver.get_driver",
            lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no session")))
        _vars._variable_store["smart.device_orientation"] = "PORTRAIT"
        assert _vars.var("{{smart.device_orientation}}") == "PORTRAIT"


class TestNothingElseMoved:
    """The desktop binding keeps this file byte-identical (see
    test_canonical_copy_parity), so every name it already answered has to
    answer exactly as it did."""

    def test_a_computed_name_is_untouched(self):
        assert _vars.var("{{smart.current_year}}").isdigit()
        assert _vars.var("{{smart.country}}") == "India"

    def test_an_unknown_name_still_resolves_to_empty(self):
        assert _vars.var("{{smart.no_such_variable}}") == ""

    def test_a_session_name_with_no_source_still_resolves_to_empty(self):
        """What a desktop session sees: nothing seeds these and nothing
        supplies them, so they answer exactly as they did before they were
        named here."""
        for name in _SESSION_NAMES:
            assert _vars.var("{{smart.%s}}" % name) == ""


class TestSessionHygiene:
    """The env outlives a driver — see also
    test_session.py::TestSmartVariableSeeding, which pins that `run()` calls
    the exporter at all (every test here calls it directly)."""

    def test_a_session_does_not_inherit_the_previous_one(self, monkeypatch):
        """The env outlives a driver, so a field the second session cannot
        answer must go empty rather than keep the first session's value."""
        class _Driver:
            capabilities = {"appVersion": "1.0"}

        monkeypatch.setitem(_config._config, "platform", "android")
        _session._export_smart_env_from_session(_Driver())
        assert _vars.var("{{smart.app_version}}") == "1.0"

        class _Next:
            capabilities = {}

        _session._export_smart_env_from_session(_Next())
        assert _vars.var("{{smart.app_version}}") == ""
