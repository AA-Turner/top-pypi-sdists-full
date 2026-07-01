"""Build LambdaTest webdriver capabilities dict for selenium.webdriver.Remote()."""
import base64
import os
from typing import Any

from testmu_selenium import _config as _cfg
from testmu_selenium._test_config import get_cap_value as _he_cap, load_test_config


_DEFAULT_CHROME_ARGS = [
    "--enable-logging",
    "--disable-notifications",
    "--no-sandbox",
    "--log-level=0",
    "--ignore-certificate-errors",
    "--disable-blink-features=AutomationControlled",
]

# V2-parity Chrome prefs (mirrors the capability-file format the code exporter emits).
_CHROME_PREFS = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_setting_values.geolocation": 1,
    "safebrowsing.enabled": False,
    "profile.password_manager_leak_detection": False,
    "signin.allowed_on_next_startup": False,
    "autofill.profile_enabled": False,
    "autofill.credit_card_enabled": False,
}


def _bool_he(key: str, default: bool) -> bool:
    """Resolve a bool cap: HE test_config > env var > default."""
    val = _he_cap(key, None)
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    return str(val).lower() in ("1", "true", "yes")


def _extension_b64(path: str) -> str:
    """Base64-encode a .crx for goog:chromeOptions.extensions (mirrors Selenium add_extension)."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def build_capability(
    browser: str | None = None,
    browser_version: str | None = None,
    platform: str | None = None,
    resolution: str | None = None,
    username: str = "",
    access_key: str = "",
    build: str | None = None,
    name: str | None = None,
    custom_capabilities: dict[str, Any] | None = None,
    chrome_options: list | None = None,
) -> dict[str, Any]:
    """Assemble the capability dict for webdriver.Remote().

    LT:Options carries the V2/V4-parity session + recording caps. Each cap
    resolves via configure() store > HE test-run JSON > env var > default,
    mirroring the V4 Playwright binding. The Selenium W3C shape
    (top-level browserName/browserVersion/platformName, goog:chromeOptions
    args dict) is preserved.

    Caller-passed browser/version/platform/resolution win over env; build/name
    fall back through the HE/env chain. custom_capabilities merges last as an
    escape hatch.
    """
    _browser = browser or os.getenv("LT_BROWSER", "chrome")
    _browser_version = browser_version or os.getenv("LT_BROWSER_VERSION", "latest")
    _platform = platform or os.getenv("LT_PLATFORM", "Windows 11")
    _resolution = resolution or os.getenv("LT_RESOLUTION", "1920x1080")

    cap: dict[str, Any] = {
        "browserName": _browser,
        "browserVersion": _browser_version,
        "platformName": _platform,
    }

    # build/name: configure (passed in) > HE json > env > ""
    _build = build or _he_cap("BUILD", os.getenv("BUILD", ""))
    _name = name or _he_cap("TEST_NAME", os.getenv("TEST_NAME", ""))
    _tc_id = _cfg.get("tc_id") or os.getenv("LT_TC_ID", "")

    # network is tri-state: explicit configure() value wins over env fallback.
    if _cfg.was_set("network"):
        _network = bool(_cfg.get("network"))
    else:
        _network = _bool_he("NETWORK", False)

    _video = _bool_he("VIDEO", True)
    _visual = _bool_he("VISUAL", True)
    _console = _bool_he("CONSOLE", True)
    _tunnel = _bool_he("TUNNEL", False)
    _performance = _bool_he("PERFORMANCE", False)
    _dedicated_proxy = _bool_he("DEDICATED_PROXY", False)
    _accessibility = _bool_he("ACCESSIBILITY", False)
    _idle_timeout = int(_he_cap("IDLE_TIMEOUT", os.getenv("IDLE_TIMEOUT", "1800")))
    _multiple_profiles = bool(_cfg.get("multiple_profiles"))

    lt_options: dict[str, Any] = {
        "username": username,
        "accessKey": access_key,
        "video": _video,
        "network": _network,
        "network.full.har": _network,
        "console": _console,
        "tunnel": _tunnel,
        "performance": _performance,
        "dedicatedProxy": _dedicated_proxy,
        "accessibility": _accessibility,
        "idleTimeout": _idle_timeout,
        "hideInternalCommandLogs": True,
        "dependentTestsInScenario": _multiple_profiles,
        "project": "Auteur-Code-Export",
        "plugin": "python-python",
        "w3c": True,
    }
    if _build:
        lt_options["build"] = _build
    if _name:
        lt_options["name"] = _name
    if _tc_id:
        lt_options["tms.tc_id"] = _tc_id
    if _resolution:
        lt_options["resolution"] = _resolution

    # This selenium binding runs in V3 binding-mode only. V3 runs report steps
    # independently (LTReporter / AUTOMIND), so they must NOT emit
    # kaneRun/preCmdVisual: the instance-page gate routes a v3 run to the V3 view by
    # the absence of kaneRun. This was previously emitted under KANE_NEW_VIEW_ENABLED,
    # but forge's run/scheduled paths re-set that env at run time, so a v3-only
    # binding must never emit kaneRun regardless of the env.
    lt_options["visual"] = _visual

    if os.getenv("GEO_LOCATION", ""):
        lt_options["geoLocation"] = os.getenv("GEO_LOCATION")

    # timezone: configure > HE json region > env
    _timezone = _cfg.get("timezone") or ""
    if not _timezone:
        _tc = load_test_config()
        if _tc:
            _tz_val = _tc.get("timezone", {})
            if isinstance(_tz_val, dict) and _tz_val.get("region"):
                _timezone = _tz_val["region"]
    if not _timezone:
        _timezone = os.getenv("TIMEZONE", "")
    if _timezone:
        lt_options["timezone"] = _timezone

    _custom_headers = _cfg.get("custom_headers") or {}
    if _custom_headers:
        lt_options["customHeaders"] = _custom_headers

    # Escape hatch: explicit custom_capabilities override everything above.
    if custom_capabilities:
        lt_options.update(custom_capabilities)

    cap["LT:Options"] = lt_options

    if _browser.lower() in ("chrome", "chromium"):
        args = list(_DEFAULT_CHROME_ARGS)
        _chrome_ops = chrome_options if chrome_options is not None else (_cfg.get("chrome_options") or [])
        for op in _chrome_ops:
            if isinstance(op, str):
                args.append(op)
            elif isinstance(op, dict):
                op_key = op.get("key", "")
                op_type = op.get("type", "")
                op_value = op.get("value", "")
                if op_type == "no-args":
                    args.append(f"{op_key}")
                else:
                    args.append(f"{op_key}={op_value}")
        goog: dict[str, Any] = {
            "args": args,
            "excludeSwitches": ["enable-automation"],
            "prefs": dict(_CHROME_PREFS),
        }
        cap["goog:chromeOptions"] = goog
        _ext = os.getenv("EXTENSION")
        if _ext and os.path.exists(_ext):
            goog["extensions"] = [_extension_b64(_ext)]
        cap["goog:loggingPrefs"] = {"performance": "ALL", "browser": "ALL"}
        cap["unhandledPromptBehavior"] = "ignore"

    return cap
