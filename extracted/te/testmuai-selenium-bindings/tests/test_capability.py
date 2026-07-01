"""Test capability assembly for selenium webdriver.Remote()."""
import pytest
from testmu_selenium._capability import build_capability
from testmu_selenium import _config, _test_config


@pytest.fixture(autouse=True)
def _reset_caps(monkeypatch):
    # Isolate from HE JSON + env recording flags + configure store.
    for k in ("TEST_RUN_ID", "TEST_CONFIG_FILE", "TEST_INSTANCE_ID",
              "EXTENSION", "KANE_NEW_VIEW_ENABLED",
              "VIDEO", "VISUAL", "CONSOLE", "NETWORK", "TUNNEL",
              "PERFORMANCE", "DEDICATED_PROXY", "ACCESSIBILITY",
              "IDLE_TIMEOUT", "GEO_LOCATION", "TIMEZONE"):
        monkeypatch.delenv(k, raising=False)
    _test_config._reset()
    saved = dict(_config._config)
    saved_keys = set(_config._configured_keys)
    yield
    _config._config.clear(); _config._config.update(saved)
    _config._configured_keys.clear(); _config._configured_keys.update(saved_keys)
    _test_config._reset()


class TestBuildCapability:
    def test_minimal_capability(self):
        cap = build_capability(browser="chrome", browser_version="latest", platform="Windows 11")
        assert cap["browserName"] == "chrome"
        assert cap["browserVersion"] == "latest"
        assert cap["platformName"] == "Windows 11"

    def test_lt_options_block_present(self):
        cap = build_capability(browser="chrome", username="u", access_key="k", build="b1")
        assert "LT:Options" in cap
        assert cap["LT:Options"]["username"] == "u"
        assert cap["LT:Options"]["accessKey"] == "k"
        assert cap["LT:Options"]["build"] == "b1"

    def test_custom_capabilities_merged(self):
        cap = build_capability(
            browser="chrome",
            custom_capabilities={"geoLocation": "US", "console": True},
        )
        assert cap["LT:Options"]["geoLocation"] == "US"
        assert cap["LT:Options"]["console"] is True

    def test_resolution_in_lt_options(self):
        cap = build_capability(browser="chrome", resolution="1920x1080")
        assert cap["LT:Options"]["resolution"] == "1920x1080"

    def test_chrome_options_args_for_kane(self):
        """Chrome should get the standard kane args (no-sandbox, disable-blink-features, etc.)."""
        cap = build_capability(browser="chrome")
        opts = cap.get("goog:chromeOptions", {})
        args = opts.get("args", [])
        assert "--no-sandbox" in args
        assert "--disable-blink-features=AutomationControlled" in args


class TestEnvVarDefaults:
    """build_capability falls back to LT_BROWSER / LT_BROWSER_VERSION /
    LT_PLATFORM / LT_RESOLUTION env vars when the corresponding kwarg is omitted
    (or passed as None). Caller-supplied kwargs override env."""

    def test_browser_falls_back_to_env(self, monkeypatch):
        monkeypatch.setenv("LT_BROWSER", "firefox")
        cap = build_capability()
        assert cap["browserName"] == "firefox"

    def test_browser_default_when_no_env(self, monkeypatch):
        monkeypatch.delenv("LT_BROWSER", raising=False)
        cap = build_capability()
        assert cap["browserName"] == "chrome"

    def test_browser_version_falls_back_to_env(self, monkeypatch):
        monkeypatch.setenv("LT_BROWSER_VERSION", "118")
        cap = build_capability()
        assert cap["browserVersion"] == "118"

    def test_browser_version_default_when_no_env(self, monkeypatch):
        monkeypatch.delenv("LT_BROWSER_VERSION", raising=False)
        cap = build_capability()
        assert cap["browserVersion"] == "latest"

    def test_platform_falls_back_to_env(self, monkeypatch):
        monkeypatch.setenv("LT_PLATFORM", "macOS Sonoma")
        cap = build_capability()
        assert cap["platformName"] == "macOS Sonoma"

    def test_platform_default_when_no_env(self, monkeypatch):
        monkeypatch.delenv("LT_PLATFORM", raising=False)
        cap = build_capability()
        assert cap["platformName"] == "Windows 11"

    def test_resolution_falls_back_to_env(self, monkeypatch):
        monkeypatch.setenv("LT_RESOLUTION", "1366x768")
        cap = build_capability()
        assert cap["LT:Options"]["resolution"] == "1366x768"

    def test_resolution_default_when_no_env(self, monkeypatch):
        monkeypatch.delenv("LT_RESOLUTION", raising=False)
        cap = build_capability()
        assert cap["LT:Options"]["resolution"] == "1920x1080"

    def test_kwarg_overrides_env_for_browser(self, monkeypatch):
        monkeypatch.setenv("LT_BROWSER", "firefox")
        cap = build_capability(browser="chrome")
        assert cap["browserName"] == "chrome"

    def test_kwarg_overrides_env_for_platform(self, monkeypatch):
        monkeypatch.setenv("LT_PLATFORM", "linux")
        cap = build_capability(platform="Windows 11")
        assert cap["platformName"] == "Windows 11"

    def test_kwarg_overrides_env_for_resolution(self, monkeypatch):
        monkeypatch.setenv("LT_RESOLUTION", "1366x768")
        cap = build_capability(resolution="1920x1080")
        assert cap["LT:Options"]["resolution"] == "1920x1080"

    def test_kwarg_overrides_env_for_browser_version(self, monkeypatch):
        monkeypatch.setenv("LT_BROWSER_VERSION", "118")
        cap = build_capability(browser_version="latest")
        assert cap["browserVersion"] == "latest"


class TestRecordingCapDefaults:
    def test_video_defaults_true(self):
        assert build_capability(browser="chrome")["LT:Options"]["video"] is True

    def test_visual_defaults_true(self):
        assert build_capability(browser="chrome")["LT:Options"]["visual"] is True

    def test_console_defaults_true(self):
        assert build_capability(browser="chrome")["LT:Options"]["console"] is True

    def test_network_defaults_false_and_har_mirrors(self):
        lt = build_capability(browser="chrome")["LT:Options"]
        assert lt["network"] is False
        assert lt["network.full.har"] is False

    def test_hide_internal_command_logs_true(self):
        assert build_capability(browser="chrome")["LT:Options"]["hideInternalCommandLogs"] is True

    def test_idle_timeout_default(self):
        assert build_capability(browser="chrome")["LT:Options"]["idleTimeout"] == 1800

    def test_static_caps(self):
        lt = build_capability(browser="chrome")["LT:Options"]
        assert lt["project"] == "Auteur-Code-Export"
        assert lt["plugin"] == "python-python"
        assert lt["w3c"] is True

    def test_loadextensions_absent(self):
        assert "loadExtensions" not in build_capability(browser="chrome")["LT:Options"]


class TestRecordingCapSourcing:
    def test_video_env_override(self, monkeypatch):
        monkeypatch.setenv("VIDEO", "false")
        assert build_capability(browser="chrome")["LT:Options"]["video"] is False

    def test_network_configure_true_wins_over_env(self, monkeypatch):
        monkeypatch.setenv("NETWORK", "false")
        _config.set_value("network", True)
        lt = build_capability(browser="chrome")["LT:Options"]
        assert lt["network"] is True
        assert lt["network.full.har"] is True

    def test_network_configure_false_distinct_from_unset(self, monkeypatch):
        monkeypatch.setenv("NETWORK", "true")
        _config.set_value("network", False)
        assert build_capability(browser="chrome")["LT:Options"]["network"] is False

    def test_network_env_used_when_not_configured(self, monkeypatch):
        monkeypatch.setenv("NETWORK", "true")
        assert build_capability(browser="chrome")["LT:Options"]["network"] is True


@pytest.mark.parametrize("env_key,cap_key,default", [
    ("VIDEO", "video", True),
    ("VISUAL", "visual", True),
    ("CONSOLE", "console", True),
    ("TUNNEL", "tunnel", False),
    ("PERFORMANCE", "performance", False),
    ("DEDICATED_PROXY", "dedicatedProxy", False),
    ("ACCESSIBILITY", "accessibility", False),
])
class TestBoolCapMatrix:
    def test_default(self, env_key, cap_key, default, monkeypatch):
        monkeypatch.delenv(env_key, raising=False)
        assert build_capability(browser="chrome")["LT:Options"][cap_key] is default

    def test_env_override(self, env_key, cap_key, default, monkeypatch):
        monkeypatch.setenv(env_key, str(not default).lower())
        assert build_capability(browser="chrome")["LT:Options"][cap_key] is (not default)


class TestMetadataCaps:
    def test_tc_id_from_configure(self):
        _config.set_value("tc_id", "TC-9")
        assert build_capability(browser="chrome")["LT:Options"]["tms.tc_id"] == "TC-9"

    def test_dependent_tests_from_multiple_profiles(self):
        _config.set_value("multiple_profiles", True)
        assert build_capability(browser="chrome")["LT:Options"]["dependentTestsInScenario"] is True

    def test_timezone_from_configure(self):
        _config.set_value("timezone", "Asia/Kolkata")
        assert build_capability(browser="chrome")["LT:Options"]["timezone"] == "Asia/Kolkata"

    def test_timezone_absent_when_unset(self):
        assert "timezone" not in build_capability(browser="chrome")["LT:Options"]

    def test_geolocation_from_env(self, monkeypatch):
        monkeypatch.setenv("GEO_LOCATION", "US")
        assert build_capability(browser="chrome")["LT:Options"]["geoLocation"] == "US"

    def test_custom_headers_from_configure(self):
        _config.set_value("custom_headers", {"X-A": "1"})
        assert build_capability(browser="chrome")["LT:Options"]["customHeaders"] == {"X-A": "1"}

    def test_custom_headers_absent_when_empty(self):
        assert "customHeaders" not in build_capability(browser="chrome")["LT:Options"]

    def test_configure_chrome_options_appended(self):
        _config.set_value("chrome_options", [{"key": "--proxy-server", "value": "x:1", "type": "value"}])
        args = build_capability(browser="chrome")["goog:chromeOptions"]["args"]
        assert "--proxy-server=x:1" in args


_V2_CHROME_ARGS = [
    "--enable-logging",
    "--disable-notifications",
    "--no-sandbox",
    "--log-level=0",
    "--ignore-certificate-errors",
    "--disable-blink-features=AutomationControlled",
]


class TestChromeOptionsV2Parity:
    def test_gate_is_case_insensitive(self):
        cap = build_capability(browser="Chrome")
        assert "goog:chromeOptions" in cap

    def test_chromium_alias_produces_block(self):
        cap = build_capability(browser="chromium")
        assert "goog:chromeOptions" in cap

    def test_default_args_match_v2_exactly(self):
        args = build_capability(browser="chrome")["goog:chromeOptions"]["args"]
        assert args == _V2_CHROME_ARGS

    def test_webgl_gpu_args_removed(self):
        args = build_capability(browser="chrome")["goog:chromeOptions"]["args"]
        assert "--enable-webgl" not in args
        assert "--enable-gpu" not in args
        assert "--ignore-gpu-blocklist" not in args

    def test_exclude_switches_present(self):
        goog = build_capability(browser="chrome")["goog:chromeOptions"]
        assert goog["excludeSwitches"] == ["enable-automation"]

    def test_prefs_present(self):
        prefs = build_capability(browser="chrome")["goog:chromeOptions"]["prefs"]
        assert prefs["credentials_enable_service"] is False
        assert prefs["profile.password_manager_enabled"] is False
        assert prefs["profile.default_content_setting_values.notifications"] == 2
        assert prefs["profile.default_content_setting_values.geolocation"] == 1
        assert prefs["safebrowsing.enabled"] is False
        assert prefs["autofill.profile_enabled"] is False
        assert prefs["autofill.credit_card_enabled"] is False

    def test_unhandled_prompt_behavior(self):
        assert build_capability(browser="chrome")["unhandledPromptBehavior"] == "ignore"

    def test_user_chrome_options_still_append(self):
        _config.set_value("chrome_options", [{"key": "--proxy-server", "value": "x:1", "type": "value"}])
        args = build_capability(browser="chrome")["goog:chromeOptions"]["args"]
        assert "--proxy-server=x:1" in args
        assert args[: len(_V2_CHROME_ARGS)] == _V2_CHROME_ARGS


class TestChromeExtension:
    def test_extension_added_when_env_points_at_file(self, tmp_path, monkeypatch):
        crx = tmp_path / "dom-watcher.crx"
        crx.write_bytes(b"FAKE-CRX-BYTES")
        monkeypatch.setenv("EXTENSION", str(crx))
        import base64
        goog = build_capability(browser="chrome")["goog:chromeOptions"]
        assert goog["extensions"] == [base64.b64encode(b"FAKE-CRX-BYTES").decode("ascii")]

    def test_extension_absent_when_env_unset(self):
        goog = build_capability(browser="chrome")["goog:chromeOptions"]
        assert "extensions" not in goog

    def test_extension_absent_when_file_missing(self, monkeypatch):
        monkeypatch.setenv("EXTENSION", "/no/such/path/dom-watcher.crx")
        goog = build_capability(browser="chrome")["goog:chromeOptions"]
        assert "extensions" not in goog


class TestKaneNewView:
    # This selenium binding runs in V3 binding-mode only. V3 runs report steps
    # independently (LTReporter / AUTOMIND), so they must never emit
    # kaneRun/kaneRunV3/preCmdVisual — the instance-page gate routes a v3 run to the
    # V3 view by the absence of kaneRun. The cap is the same whether or not
    # KANE_NEW_VIEW_ENABLED is set (forge may still set that env at run time).
    def test_v3_never_emits_kanerun_even_when_new_view_enabled(self, monkeypatch):
        monkeypatch.setenv("KANE_NEW_VIEW_ENABLED", "true")
        lt = build_capability(browser="chrome")["LT:Options"]
        assert "kaneRun" not in lt
        assert "kaneRunV3" not in lt
        assert "preCmdVisual" not in lt
        assert lt["visual"] is True

    def test_default_keeps_visual_no_kanerun(self, monkeypatch):
        monkeypatch.delenv("KANE_NEW_VIEW_ENABLED", raising=False)
        lt = build_capability(browser="chrome")["LT:Options"]
        assert lt["visual"] is True
        assert "kaneRun" not in lt
        assert "kaneRunV3" not in lt
        assert "preCmdVisual" not in lt
