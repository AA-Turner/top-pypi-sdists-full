"""configure() whitelist semantics."""
import pytest

from testmu_appium import configure
from testmu_appium import _config as _config_mod
from testmu_appium import _errors

# Read config through the module, never through a bound `_config` name: test_config.py
# reloads the module, which rebinds `_config` to a fresh dict.


def test_configure_accepts_mobile_keys():
    configure(app_id="com.google.android.gm", platform="android", udid="emulator-5554",
              no_reset=True, kane_run_v4=True)
    assert _config_mod._config["app_id"] == "com.google.android.gm"
    assert _config_mod._config["platform"] == "android"
    assert _config_mod._config["udid"] == "emulator-5554"
    assert _config_mod._config["no_reset"] is True
    assert _config_mod._config["kane_run_v4"] is True
    assert _config_mod.was_set("app_id")


def test_configure_raises_on_unknown_key():
    with pytest.raises(_errors.TestmuConfigError) as exc:
        configure(bundle_id="com.apple.Preferences")
    assert "bundle_id" in str(exc.value)


def test_configure_rejects_conflicting_capability_spec():
    with pytest.raises(_errors.TestmuConfigError):
        configure(capability={"a": 1}, custom_capabilities={"b": 2})


def test_configure_populates_test_params():
    from testmu_appium._vars import _test_params

    configure(test_params={"env": "stage"})
    assert _test_params["env"] == "stage"


@pytest.mark.parametrize("platform", ["android", "ios"])
def test_configure_accepts_both_platforms(platform):
    """iOS is accepted as configuration data day one; only its runtime tables are dormant."""
    configure(platform=platform)
    assert _config_mod._config["platform"] == platform
    assert _config_mod.platform() == platform


def test_configure_rejects_unknown_platform():
    with pytest.raises(_errors.TestmuConfigError) as exc:
        configure(platform="windows")
    assert "windows" in str(exc.value)


class TestConfigureSmart:
    """configure(smart=...) has to reach the flag the gates actually read.

    Every gate reads the `_config` module attribute, so the kwarg writes that as well
    as the config dict.
    """

    @pytest.fixture(autouse=True)
    def _restore(self):
        original = _config_mod.smart
        _config_mod._set_smart_degraded(False)
        yield
        _config_mod.smart = original
        _config_mod._set_smart_degraded(False)

    def test_configure_smart_false_disables_it(self):
        configure(smart=True)
        configure(smart=False)
        assert _config_mod.smart_enabled() is False
        assert _config_mod.smart is False
        assert _config_mod._config["smart"] is False

    def test_configure_smart_true_enables_it(self):
        configure(smart=False)
        configure(smart=True)
        assert _config_mod.smart_enabled() is True
        assert _config_mod.smart is True
        assert _config_mod._config["smart"] is True

    @pytest.mark.parametrize("value", [False, 0, "", None])
    def test_every_falsy_configured_value_disables_smart(self, value):
        configure(smart=True)
        configure(smart=value)
        assert _config_mod.smart_enabled() is False

    def test_configure_smart_false_stops_the_ai_backed_helpers(self):
        """An AI-backed read must refuse once the flag is off."""
        from testmu_appium._errors import TestmuConfigError
        from testmu_appium._helpers.textual_query import textual_query

        configure(smart=False)
        with pytest.raises(TestmuConfigError):
            textual_query(None, query="anything")

    def test_configure_smart_false_stops_autoheal(self):
        from testmu_appium._heal import HealUnavailable, autoheal
        from testmu_appium._step import step

        configure(smart=False)
        with step("s"):
            assert isinstance(autoheal(None, "desc", "click"), HealUnavailable)

    def test_configuring_another_key_leaves_smart_alone(self):
        configure(smart=True)
        configure(app_id="com.example.app")
        assert _config_mod.smart_enabled() is True


class TestConfigureHeal:
    @pytest.fixture(autouse=True)
    def _restore(self):
        original = _config_mod.heal
        yield
        _config_mod.heal = original

    def test_configure_heal_false_is_the_deterministic_mode_switch(self):
        configure(heal=False)
        assert _config_mod.heal is False
        assert _config_mod._config["heal"] is False

    def test_configuring_another_key_leaves_heal_alone(self):
        configure(heal=False)
        configure(app_id="com.example.app")
        assert _config_mod.heal is False


class TestConfigureScreenshotSource:
    """Which path serves a perception screenshot, and the port it is read from."""

    @pytest.fixture(autouse=True)
    def _restore(self, monkeypatch):
        monkeypatch.setitem(_config_mod._config, "screenshot_source",
                            _config_mod.SOURCE_AUTO)
        monkeypatch.setitem(_config_mod._config, "mjpeg_port",
                            _config_mod._DEFAULT_MJPEG_PORT)

    @pytest.mark.parametrize("source", ["auto", "mjpeg", "appium"])
    def test_every_documented_source_is_accepted(self, source):
        configure(screenshot_source=source)
        assert _config_mod._config["screenshot_source"] == source

    def test_the_source_is_normalized_to_lowercase(self):
        configure(screenshot_source="MJPEG")
        assert _config_mod._config["screenshot_source"] == "mjpeg"

    def test_an_unknown_source_raises(self):
        with pytest.raises(_errors.TestmuConfigError) as exc:
            configure(screenshot_source="scrcpy")
        assert "scrcpy" in str(exc.value)

    def test_the_mjpeg_port_is_configurable(self):
        configure(mjpeg_port="7999")
        assert _config_mod._config["mjpeg_port"] == 7999

    @pytest.mark.parametrize("port", ["not-a-port", 0, 70000])
    def test_a_port_outside_the_range_raises(self, port):
        with pytest.raises(_errors.TestmuConfigError):
            configure(mjpeg_port=port)


def test_configure_rejects_non_v4_kane_version():
    """Mobile export is v4-only."""
    with pytest.raises(_errors.TestmuConfigError) as exc:
        configure(kane_version="v3")
    assert "v4-only" in str(exc.value)
    configure(kane_version="v4")
