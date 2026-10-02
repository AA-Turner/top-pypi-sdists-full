"""Foreground-app identity through the platform seam.

Every module that needs the app in the foreground resolves it through one
registry row. The android row keeps the tolerant read — a failed
``current_package`` is an empty identity, not an error — while a platform
without a row raises ``UnsupportedOnPlatform`` before any driver read, and no
call-site wrapper swallows that raise.
"""
import pathlib

import pytest

from testmu_appium import _action_web, _config
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers import _adapters, foreground
from testmu_appium._helpers.cookies import clear_cookies
from testmu_appium._helpers.foreground import foreground_app
from testmu_appium._helpers.local_storage import clear_local_storage
from testmu_appium._helpers.navigation_history import go_back
from testmu_appium._helpers.refresh import refresh


class _Driver:
    current_package = "com.android.chrome"


class _PackagelessDriver:
    current_package = None


class _BrokenDriver:
    @property
    def current_package(self):
        raise RuntimeError("current_package endpoint unavailable")


class TestAndroidRow:
    @pytest.fixture(autouse=True)
    def _android(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "android")

    def test_the_foreground_package_is_returned(self):
        assert foreground_app(_Driver()) == "com.android.chrome"

    def test_a_missing_package_is_an_empty_identity(self):
        assert foreground_app(_PackagelessDriver()) == ""

    def test_a_failed_read_is_swallowed_to_an_empty_identity(self):
        assert foreground_app(_BrokenDriver()) == ""


class TestIos:
    @pytest.fixture(autouse=True)
    def _ios(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")

    def test_the_bundle_id_comes_from_active_app_info(self):
        """Not the launched app: `mobile: activeAppInfo` reports what is actually
        in front, and the two differ the moment a test leaves the app under test —
        which is exactly when a WebView socket needs binding to its owner."""
        class _Ios:
            def execute_script(self, name, args=None):
                assert name == "mobile: activeAppInfo"
                return {"bundleId": "com.example.app"}

        assert foreground_app(_Ios()) == "com.example.app"

    def test_a_failed_read_is_swallowed_to_an_empty_identity(self):
        assert foreground_app(_BrokenDriver()) == ""


class TestPlatformMiss:
    @pytest.fixture(autouse=True)
    def _unshipped(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "tizen")

    def test_an_unshipped_platform_raises_instead_of_reading_the_driver(self):
        with pytest.raises(UnsupportedOnPlatform) as exc:
            foreground_app(_BrokenDriver())
        assert "foreground app identity" in str(exc.value)
        assert "tizen" in str(exc.value)

    @pytest.mark.parametrize("call", [
        lambda d: refresh(d, surface="web"),
        lambda d: clear_cookies(d),
        lambda d: clear_local_storage(d),
        lambda d: go_back(d, surface="web"),
    ], ids=["refresh", "cookies", "local_storage", "navigation_history"])
    def test_call_sites_surface_the_miss_before_any_channel_probe(
        self, monkeypatch, call
    ):
        monkeypatch.setattr(
            _action_web,
            "visible_channel",
            lambda package: pytest.fail("the platform miss must precede the channel"),
        )
        with pytest.raises(UnsupportedOnPlatform) as exc:
            call(_Driver())
        assert "foreground app identity" in str(exc.value)


def test_both_platform_rows_identify_the_foreground_app():
    for platform in ("android", "ios"):
        assert set(_adapters._REGISTRIES["foreground_app"][platform]) == {"identify"}


def test_current_package_is_read_by_the_foreground_row_alone():
    package_root = pathlib.Path(foreground.__file__).resolve().parents[1]
    readers = sorted(
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*.py")
        if "current_package" in path.read_text()
    )
    assert readers == ["_helpers/foreground.py"]
