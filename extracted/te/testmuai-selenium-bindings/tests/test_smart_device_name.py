"""{{smart.device_name}} resolves to the ALLOCATED device.

A mobile-browser session is usually requested with a device-selection REGEX
("^(?!.*(Tab|Fold)).*"); the hub picks a concrete device and echoes the friendly
name back in the negotiated capabilities. An assertion on the device must compare
against what was allocated, never against the filter it was chosen by.
"""
import os

import pytest

from testmu_selenium._session import _export_smart_env_from_session
from testmu_selenium._vars import (
    device_name_from_capabilities,
    is_value_regex,
    resolve_real_device_name,
    var,
)

_DEVICE_ENV = ("device_name", "deviceName", "smart_device_name")


@pytest.fixture(autouse=True)
def _clean_device_env():
    saved = {k: os.environ.get(k) for k in _DEVICE_ENV}
    for k in _DEVICE_ENV:
        os.environ.pop(k, None)
    yield
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


class _FakeDriver:
    def __init__(self, capabilities):
        self.capabilities = capabilities


class TestIsValueRegex:
    @pytest.mark.parametrize("value", [
        "^(?!.*(Tab|Fold)).*",
        "iPhone.*",
        "^(Galaxy|Pixel)",
        ".*",
    ])
    def test_selection_filters_are_regexes(self, value):
        assert is_value_regex(value) is True

    @pytest.mark.parametrize("value", [
        "Galaxy S23", "Pixel 7", "iPhone 14 Pro", "", None, 0,
    ])
    def test_real_names_and_empties_are_not(self, value):
        assert is_value_regex(value) is False


class TestDeviceNameFromCapabilities:
    def test_reads_hub_resolved_desired_device_name(self):
        caps = {"desired": {"deviceName": "Galaxy S23"}}
        assert device_name_from_capabilities(caps) == "Galaxy S23"

    def test_rejects_a_regex_echoed_back_in_desired(self):
        caps = {"desired": {"deviceName": "^(?!.*(Tab|Fold)).*"}}
        assert device_name_from_capabilities(caps) == ""

    def test_falls_back_to_top_level_only_for_name_like_values(self):
        # A serial ("RFCW31WRCVT") or model code ("SM-S911U") is not a name.
        assert device_name_from_capabilities({"deviceName": "RFCW31WRCVT"}) == ""
        assert device_name_from_capabilities({"deviceModel": "SM-S911U"}) == ""
        assert device_name_from_capabilities({"deviceModel": "Galaxy S23 Ultra"}) == "Galaxy S23 Ultra"

    def test_desired_wins_over_top_level(self):
        caps = {"desired": {"deviceName": "Galaxy S23"}, "deviceModel": "Pixel 7 Pro"}
        assert device_name_from_capabilities(caps) == "Galaxy S23"

    @pytest.mark.parametrize("caps", [None, {}, {"desired": "not-a-dict"}, {"desired": {}}])
    def test_nothing_usable_returns_empty_and_never_raises(self, caps):
        assert device_name_from_capabilities(caps) == ""

    def test_a_hostile_capabilities_object_never_raises(self):
        class Boom:
            def get(self, *_a, **_kw):
                raise RuntimeError("caps exploded")

        assert device_name_from_capabilities(Boom()) == ""


class TestResolveRealDeviceName:
    def test_concrete_env_value_wins(self):
        os.environ["device_name"] = "Pixel 7"
        os.environ["smart_device_name"] = "Galaxy S23"
        assert resolve_real_device_name() == "Pixel 7"

    def test_camel_case_env_alias_is_honoured(self):
        os.environ["deviceName"] = "Pixel 7"
        assert resolve_real_device_name() == "Pixel 7"

    def test_session_value_beats_a_regex_env_value(self):
        os.environ["device_name"] = "^(?!.*(Tab|Fold)).*"
        os.environ["smart_device_name"] = "Galaxy S23"
        assert resolve_real_device_name() == "Galaxy S23"

    def test_regex_env_value_survives_when_nothing_better_exists(self):
        # No regression to empty: an unresolvable run keeps its previous output.
        os.environ["device_name"] = "^(?!.*(Tab|Fold)).*"
        assert resolve_real_device_name() == "^(?!.*(Tab|Fold)).*"

    def test_nothing_set_resolves_to_empty(self):
        assert resolve_real_device_name() == ""


class TestSessionExport:
    def test_export_primes_the_resolved_device(self):
        _export_smart_env_from_session(
            _FakeDriver({"browserName": "chrome", "desired": {"deviceName": "Galaxy S23"}})
        )
        assert os.environ["smart_device_name"] == "Galaxy S23"
        assert var("{{smart.device_name}}") == "Galaxy S23"

    def test_a_desktop_session_leaves_device_name_unset(self):
        _export_smart_env_from_session(_FakeDriver({"browserName": "chrome"}))
        assert "smart_device_name" not in os.environ
        assert var("{{smart.device_name}}") == ""

    def test_end_to_end_regex_request_resolves_to_the_allocated_device(self):
        # What the caller asked the hub for...
        os.environ["device_name"] = "^(?!.*(Tab|Fold)).*"
        # ...and what the hub actually allocated.
        _export_smart_env_from_session(
            _FakeDriver({"desired": {"deviceName": "Galaxy S23"}})
        )
        assert var("{{smart.device_name}}") == "Galaxy S23"

    def test_template_substitution_inside_a_sentence(self):
        _export_smart_env_from_session(_FakeDriver({"desired": {"deviceName": "Pixel 7"}}))
        assert var("running on {{smart.device_name}} today") == "running on Pixel 7 today"
