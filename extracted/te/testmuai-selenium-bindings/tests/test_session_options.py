"""Tests for _build_remote_options — capability dict -> ChromeOptions conversion.

Regression: feeding goog:chromeOptions through ChromeOptions.set_capability()
gets discarded by to_capabilities() (it rebuilds goog:chromeOptions from the
object's own args/experimental_options/extensions). These tests assert the
conversion preserves args/excludeSwitches/prefs/extensions on the wire.
"""
import base64

from testmu_selenium._session import _build_remote_options


def _to_caps(cap):
    return _build_remote_options(cap).to_capabilities()


class TestChromeOptionsSurviveConversion:
    def test_args_preserved(self):
        cap = {
            "browserName": "chrome",
            "goog:chromeOptions": {"args": ["--no-sandbox", "--proxy-server=1.2.3.4:8080"]},
        }
        args = _to_caps(cap)["goog:chromeOptions"]["args"]
        assert "--no-sandbox" in args
        assert "--proxy-server=1.2.3.4:8080" in args

    def test_exclude_switches_and_prefs_preserved(self):
        cap = {
            "browserName": "chrome",
            "goog:chromeOptions": {
                "args": [],
                "excludeSwitches": ["enable-automation"],
                "prefs": {"safebrowsing.enabled": False},
            },
        }
        goog = _to_caps(cap)["goog:chromeOptions"]
        assert goog["excludeSwitches"] == ["enable-automation"]
        assert goog["prefs"] == {"safebrowsing.enabled": False}

    def test_encoded_extension_preserved(self):
        b64 = base64.b64encode(b"FAKE-CRX").decode("ascii")
        cap = {"browserName": "chrome", "goog:chromeOptions": {"args": [], "extensions": [b64]}}
        assert _to_caps(cap)["goog:chromeOptions"]["extensions"] == [b64]

    def test_non_chromeoptions_keys_set_as_capabilities(self):
        cap = {
            "browserName": "chrome",
            "platformName": "Windows 11",
            "LT:Options": {"build": "b1", "video": True},
            "unhandledPromptBehavior": "ignore",
        }
        caps = _to_caps(cap)
        assert caps["platformName"] == "Windows 11"
        assert caps["LT:Options"]["build"] == "b1"
        assert caps["unhandledPromptBehavior"] == "ignore"
