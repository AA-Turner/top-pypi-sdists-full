"""build_capability() exports the resolved session platform/browser as the
smart.* env vars the {{smart.os_type|browser_*}} resolver reads.

V3 selenium exports are configure-based with no auteur test-file wrapper that
sets these (the Playwright export sets them in format_python_code). Without this,
{{smart.os_type}} resolves to "" at runtime and platform assertions fail. The
values MUST come from build_capability's resolved caps (the same source the
webdriver.Remote() session uses), not a re-read of an arbitrary env var.
"""
import os
import unittest

from testmu_selenium._capability import build_capability
from testmu_selenium._vars import _resolve_smart

_SMART_KEYS = ("smart_os", "smart_os_version", "smart_browser_name", "smart_browser_version")


class TestSmartEnvFromCaps(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.pop(k, None) for k in _SMART_KEYS}

    def tearDown(self):
        for k in _SMART_KEYS:
            os.environ.pop(k, None)
            if self._saved.get(k) is not None:
                os.environ[k] = self._saved[k]

    def test_explicit_caps_populate_smart_env_and_resolver(self):
        """Caller-passed platform/browser become smart.* env AND resolve via _resolve_smart."""
        cap = build_capability(
            browser="firefox", browser_version="121.0", platform="macOS Sonoma",
            username="u", access_key="k",
        )
        # caps and smart env share one source
        self.assertEqual(cap["platformName"], "macOS Sonoma")
        self.assertEqual(os.environ["smart_os"], "macOS Sonoma")
        self.assertEqual(os.environ["smart_browser_name"], "firefox")
        self.assertEqual(os.environ["smart_browser_version"], "121.0")
        # the binding's smart resolver now returns the real session values
        self.assertEqual(_resolve_smart("os_type"), "macOS Sonoma")
        self.assertEqual(_resolve_smart("os"), "macOS Sonoma")
        self.assertEqual(_resolve_smart("browser_name"), "firefox")
        self.assertEqual(_resolve_smart("browser_version"), "121.0")

    def test_smart_os_matches_the_session_platform_value(self):
        """Regression guard for the false-verify trap: smart_os equals the EXACT
        platform the caps are built with (here via the LT_PLATFORM resolution path),
        so session and smart_os can never diverge."""
        prev = os.environ.get("LT_PLATFORM")
        os.environ["LT_PLATFORM"] = "Windows 10"
        try:
            cap = build_capability(username="u", access_key="k")
            self.assertEqual(os.environ["smart_os"], cap["platformName"])
            self.assertEqual(_resolve_smart("os_type"), "Windows 10")
        finally:
            if prev is None:
                os.environ.pop("LT_PLATFORM", None)
            else:
                os.environ["LT_PLATFORM"] = prev


if __name__ == "__main__":
    unittest.main()
