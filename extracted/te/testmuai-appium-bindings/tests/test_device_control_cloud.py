"""Cloud-venue behavior of the device-control registry (spec §13 addendum).

Grid-verified facts these tests encode (stage probe, 2026-08-17):
- `mobile: shell` is restricted on the LT grid and `lambda-adb` allowlists
  none of this feature's commands — shell-riding operations must refuse
  loudly on the cloud venue instead of dying on the grid's opaque error.
- `enableBluetooth: true` raises the radio, session-start only, Android 13+.
- setConnectivity works on the grid, so connectivity kinds stay untouched.
- volume up/down ride keycodes, not shell — they stay allowed on cloud.
"""
import pytest

from testmu_appium import _config
from testmu_appium._helpers.device_control import (
    KINDS,
    cloud_session_caps,
    device_control,
    device_control_query,
)


class _RefusingDriver:
    """Any driver call proves the refusal happened binding-side, not grid-side."""

    def __getattr__(self, name):
        raise AssertionError(f"driver.{name} must not be reached on the cloud venue")


@pytest.fixture
def cloud(monkeypatch):
    monkeypatch.setattr(_config, "run_target", "cloud")
    monkeypatch.setitem(_config._config, "platform", "android")
    return _RefusingDriver()


def test_bluetooth_declares_its_session_caps():
    caps = KINDS["bluetooth"].platforms["android"].session_caps
    assert caps is not None
    assert caps.caps == {"enableBluetooth": True}
    assert caps.min_android == "13"


def test_cloud_set_of_a_session_caps_kind_names_the_capability(cloud):
    with pytest.raises(RuntimeError, match=r"enableBluetooth.*session start"):
        device_control(cloud, "bluetooth", value="on")


def test_cloud_set_of_an_unallowlisted_kind_names_the_grid_gap(cloud):
    with pytest.raises(RuntimeError, match=r"no runtime channel.*lambda-adb"):
        device_control(cloud, "brightness", value="40")


def test_cloud_query_of_a_shell_backed_kind_refuses(cloud):
    with pytest.raises(RuntimeError, match=r"cannot be read.*LambdaTest grid"):
        device_control_query(cloud, "dnd")


def test_cloud_volume_keycode_values_stay_allowed(cloud, monkeypatch):
    pressed = []
    monkeypatch.setattr(
        type(cloud), "press_keycode", lambda self, code: pressed.append(code),
        raising=False,
    )
    device_control(cloud, "volume", value="up")
    assert pressed == [24]


def test_cloud_volume_level_values_refuse(cloud):
    with pytest.raises(RuntimeError, match=r"no runtime channel"):
        device_control(cloud, "volume", value="40")


def test_cloud_connectivity_kinds_are_untouched(cloud, monkeypatch):
    calls = []
    monkeypatch.setattr(
        type(cloud), "execute_script",
        lambda self, script, args: calls.append((script, args)),
        raising=False,
    )
    device_control(cloud, "wifi", value="off")
    assert calls == [("mobile: setConnectivity", {"wifi": False})]


def test_local_venue_is_unchanged(monkeypatch):
    monkeypatch.setattr(_config, "run_target", "local")
    monkeypatch.setitem(_config._config, "platform", "android")
    calls = []

    class _Driver:
        def execute_script(self, script, args):
            calls.append((script, args))

    device_control(_Driver(), "wifi", value="on")
    assert calls == [("mobile: setConnectivity", {"wifi": True})]


def test_cloud_session_caps_merges_declared_kinds():
    merged = cloud_session_caps(["bluetooth", "wifi", "orientation"])
    assert merged == {"enableBluetooth": True}


def test_cloud_session_caps_rejects_unknown_kinds():
    with pytest.raises(ValueError, match="not_a_setting"):
        cloud_session_caps(["not_a_setting"])
