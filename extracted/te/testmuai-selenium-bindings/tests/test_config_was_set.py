"""Test _config explicit-set tracking and new capability-metadata defaults."""
import pytest
from testmu_selenium import _config
from testmu_selenium._config import get, set_value, was_set


@pytest.fixture(autouse=True)
def _restore_config():
    saved = dict(_config._config)
    saved_keys = set(_config._configured_keys)
    yield
    _config._config.clear()
    _config._config.update(saved)
    _config._configured_keys.clear()
    _config._configured_keys.update(saved_keys)


class TestNewDefaults:
    def test_network_defaults_false(self):
        assert get("network") is False

    def test_tc_id_defaults_empty(self):
        assert get("tc_id") == ""

    def test_timezone_defaults_empty(self):
        assert get("timezone") == ""

    def test_chrome_options_defaults_empty_list(self):
        assert get("chrome_options") == []

    def test_multiple_profiles_defaults_false(self):
        assert get("multiple_profiles") is False

    def test_custom_headers_defaults_empty_dict(self):
        assert get("custom_headers") == {}


class TestWasSet:
    def test_unset_key_returns_false(self):
        assert was_set("network") is False

    def test_set_value_marks_key(self):
        set_value("network", False)
        assert was_set("network") is True

    def test_set_value_distinguishes_false_from_unset(self):
        assert was_set("network") is False
        set_value("network", False)
        assert was_set("network") is True
        assert get("network") is False
