"""Test testmu_selenium.configure(**kwargs)."""
import pytest
from testmu_selenium._configure import configure
from testmu_selenium._config import _config, get
from testmu_selenium._errors import TestmuConfigError


@pytest.fixture(autouse=True)
def reset_config():
    """Reset _config to a known baseline before each test."""
    saved = dict(_config)
    yield
    _config.clear()
    _config.update(saved)


class TestConfigureBasic:
    def test_configure_writes_build_to_config(self):
        configure(build="my-build-1")
        assert get("build") == "my-build-1"

    def test_configure_writes_name(self):
        configure(name="my-test-1")
        assert get("name") == "my-test-1"

    def test_configure_writes_capability_dict(self):
        configure(capability={"browserName": "firefox"})
        assert get("capability") == {"browserName": "firefox"}

    def test_configure_writes_custom_capabilities(self):
        configure(custom_capabilities={"geoLocation": "US"})
        assert get("custom_capabilities") == {"geoLocation": "US"}

    def test_configure_writes_test_metadata(self):
        configure(test_metadata={"tcId": "TC-7"})
        assert get("test_metadata") == {"tcId": "TC-7"}


class TestConfigureValidation:
    def test_configure_rejects_unknown_kwargs(self):
        with pytest.raises(TestmuConfigError, match="unknown kwarg"):
            configure(nonsense_field="oops")

    def test_configure_rejects_capability_and_custom_capabilities_together(self):
        with pytest.raises(TestmuConfigError, match="conflicting"):
            configure(capability={"X": "Y"}, custom_capabilities={"A": "B"})


class TestConfigureTestParams:
    def test_configure_populates_test_params(self):
        from testmu_selenium._vars import _test_params, clear_state
        clear_state()
        try:
            configure(test_params={"p": "zeeshan"})
            assert _test_params["p"] == "zeeshan"
        finally:
            clear_state()


class TestConfigureMultipleCalls:
    def test_configure_called_twice_overwrites(self):
        configure(build="first")
        configure(build="second")
        assert get("build") == "second"


class TestConfigureCapabilityMetadata:
    def test_configure_accepts_tc_id(self):
        configure(tc_id="TC-42")
        assert get("tc_id") == "TC-42"

    def test_configure_accepts_network(self):
        configure(network=True)
        assert get("network") is True

    def test_configure_accepts_timezone(self):
        configure(timezone="Asia/Kolkata")
        assert get("timezone") == "Asia/Kolkata"

    def test_configure_accepts_chrome_options(self):
        configure(chrome_options=[{"key": "--foo", "type": "no-args"}])
        assert get("chrome_options") == [{"key": "--foo", "type": "no-args"}]

    def test_configure_accepts_multiple_profiles(self):
        configure(multiple_profiles=True)
        assert get("multiple_profiles") is True

    def test_configure_accepts_custom_headers(self):
        configure(custom_headers={"X-Test": "1"})
        assert get("custom_headers") == {"X-Test": "1"}
