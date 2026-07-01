"""TestMu capability builder for Playwright Python (LambdaTest grid).

Configuration is sourced from testmu.configure() data first, then falls back
to environment variables (no sys.argv / test-run JSON).
This module is the env-var-only equivalent of the capability.py template
produced by the TestMu code-export pipeline.
"""

import json
import os
import urllib.parse
from pathlib import Path

from testmu import _configure

try:
    from importlib.metadata import version as _pkg_version

    _PW_VERSION = _pkg_version("playwright")
except Exception:
    _PW_VERSION = "unknown"


# ---------------------------------------------------------------------------
# Internal helpers (match template helpers exactly)
# ---------------------------------------------------------------------------


def _get_download_folder() -> Path:
    """Return the system Downloads folder, creating it if needed."""
    if os.name == "nt":
        downloads_path = Path(
            os.path.join(os.environ.get("USERPROFILE", ""), "Downloads")
        )
    else:
        downloads_path = Path(os.path.expanduser("~/Downloads"))
    downloads_path.mkdir(parents=True, exist_ok=True)
    return downloads_path


def _get_cap_value(cap_name: str, default_value=None):
    """Return env var value or default — mirrors get_cap_value(None, ...) path."""
    return os.getenv(cap_name, default_value)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_capabilities(
    browser: str = None,
    browser_version: str = None,
    resolution: str = None,
    platform: str = None,
    *,
    # baked-in values (set at code-export time, overridable by env)
    build: str = None,
    name: str = None,
    tc_id: str = None,
    network_caps: bool = False,
    multiple_profiles: bool = False,
    chrome_options: list = None,
    custom_headers: dict = None,
) -> dict:
    """Build and return the LambdaTest capabilities dict.

    All parameters fall back to env vars when not supplied, mirroring the
    template's get_cap_value(test_config, ...) with test_config=None path.

    After building, sets smart_os / smart_os_version / smart_browser_name /
    smart_browser_version env vars (same as the template).
    """
    if chrome_options is None:
        chrome_options = _configure.get("chrome_options", [])
    if custom_headers is None:
        custom_headers = _configure.get("custom_headers", {})

    # Resolve top-level fields from env or defaults
    _browser = browser or os.getenv("LT_BROWSER", "Chrome")
    _browser_version = browser_version or os.getenv("LT_BROWSER_VERSION", "latest")
    _resolution = resolution or os.getenv("LT_RESOLUTION", "1920x1080")
    _platform = platform or os.getenv("LT_PLATFORM", "linux")

    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")

    # HE test-run config — checked after configure(), before env vars
    from testmu._test_config import get_cap_value as _he_cap

    # video/visual/console/network coerce env strings to bool-like; template
    # passes True/False from get_cap_value so booleans are fine here.
    def _bool_env(key: str, default: bool) -> bool:
        val = os.getenv(key)
        if val is None:
            return default
        return val.lower() in ("1", "true", "yes")

    def _bool_he(key: str, default: bool) -> bool:
        """Check test_config first, then env var, then default."""
        val = _he_cap(key, None)
        if val is None:
            return default
        if isinstance(val, bool):
            return val
        return str(val).lower() in ("1", "true", "yes")

    # Build + name: configure() > test_config > env > default
    _build = _configure.get("build") or _he_cap(
        "BUILD", os.getenv("BUILD", build or "")
    )
    _name = _configure.get("name") or _he_cap(
        "TEST_NAME", os.getenv("TEST_NAME", name or "")
    )
    _tc_id = _configure.get("tc_id") or tc_id or os.getenv("LT_TC_ID", "")

    # For bool fields: configure() wins when explicitly set, then test_config > env > default.
    _cfg_network = _configure.get("network")
    if _configure.was_set("network"):
        _network = bool(_cfg_network)
    else:
        _network = _bool_he("NETWORK", network_caps)

    _cfg_multiple_profiles = _configure.get("multiple_profiles")
    if _configure.was_set("multiple_profiles"):
        multiple_profiles = _cfg_multiple_profiles

    # Bool caps: configure() has no explicit setters for these, so test_config > env > default.
    _video = _bool_he("VIDEO", True)
    _console = _bool_he("CONSOLE", True)
    _tunnel = _bool_he("TUNNEL", False)
    _performance = _bool_he("PERFORMANCE", False)
    _dedicated_proxy = _bool_he("DEDICATED_PROXY", False)
    _accessibility = _bool_he("ACCESSIBILITY", False)
    _idle_timeout = int(_he_cap("IDLE_TIMEOUT", os.getenv("IDLE_TIMEOUT", "1800")))

    capabilities = {
        "browserName": _browser,
        "browserVersion": _browser_version,
        "LT:Options": {
            "platform": _platform,
            "user": username,
            "accessKey": access_key,
            "video": _video,
            "resolution": _resolution,
            "network": _network,
            "network.full.har": _network,
            "network.http2": True,
            "build": _build,
            "project": "Auteur-Code-Export",
            "name": _name,
            "w3c": True,
            "plugin": "python-python",
            "console": _console,
            "tms.tc_id": _tc_id,
            "loadExtensions": [os.getenv("EXTENSION")],
            "playwrightClientVersion": _PW_VERSION,
            "tunnel": _tunnel,
            "performance": _performance,
            "dedicatedProxy": _dedicated_proxy,
            "idleTimeout": _idle_timeout,
            "accessibility": _accessibility,
            "hideInternalCommandLogs": True,
            "dependentTestsInScenario": multiple_profiles,
        },
    }

    # Geolocation — conditional (matches: if os.getenv("GEO_LOCATION", False))
    if os.getenv("GEO_LOCATION", False):
        capabilities["LT:Options"]["geoLocation"] = os.getenv("GEO_LOCATION")

    # Timezone — configure() > test_config (dict with "region") > env var
    _timezone = _configure.get("timezone") or ""
    if not _timezone:
        from testmu._test_config import load_test_config

        _tc = load_test_config()
        if _tc:
            _tz_val = _tc.get("timezone", {})
            if isinstance(_tz_val, dict) and _tz_val.get("region"):
                _timezone = _tz_val["region"]
    if not _timezone:
        _timezone = os.getenv("TIMEZONE", "")
    if _timezone:
        capabilities["LT:Options"]["timezone"] = _timezone

    # Custom headers — conditional (resolve {{...}} so the grid never receives a literal template)
    if custom_headers:
        from testmu._vars import var
        capabilities["LT:Options"]["customHeaders"] = {k: var(v) for k, v in custom_headers.items()}

    # Browser-specific options
    if _browser.lower() in ("chrome", "pw-chromium"):
        default_args = [
            "--enable-logging",
            "--disable-notifications",
            "--no-sandbox",
            "--log-level=0",
            "--ignore-certificate-errors",
            "--disable-blink-features=AutomationControlled",
            "--password-store=basic",
            "--safebrowsing-disable-auto-update",
            "--disable-sync",
        ]
        capabilities["LT:Options"]["goog:chromeOptions"] = default_args
        for op in chrome_options:
            op_key = op.get("key", "")
            op_type = op.get("type", "")
            if op_type == "file":
                op_value = os.path.join(
                    str(_get_download_folder()), op.get("value", "")
                )
            else:
                op_value = op.get("value", "")
            if op_type == "no-args":
                capabilities["LT:Options"]["goog:chromeOptions"].append(f"{op_key}")
            else:
                capabilities["LT:Options"]["goog:chromeOptions"].append(
                    f"{op_key}={op_value}"
                )
    elif _browser.lower() == "microsoftedge":
        default_args = [
            "--enable-logging",
            "--disable-notifications",
            "--log-level=0",
            "--disable-blink-features=AutomationControlled",
            "--password-store=basic",
            "--safebrowsing-disable-auto-update",
            "--disable-sync",
        ]
        capabilities["LT:Options"]["ms:edgeOptions"] = default_args
    elif _browser.lower() in ("firefox", "pw-firefox"):
        capabilities["LT:Options"]["firefoxUserPrefs"] = {
            "dom.webnotifications.enabled": False,
            "signon.rememberSignons": False,
            "signon.autofillForms": False,
            "permissions.default.desktop-notification": 2,
        }

    # Emit kaneRunV4 + preCmdVisual only when the generated test opted in via
    # testmu.configure(kane_run_v4=True).
    if _configure.get("kane_run_v4"):
        capabilities["LT:Options"]["kaneRunV4"] = True
        capabilities["LT:Options"]["preCmdVisual"] = True

    # Emit kaneRunV3 for v3-authored runs (configure(kane_run_v3=True)) so the
    # server can distinguish v3 from v2 — the kaneai_version int is 2 for both.
    # Mirrors V4's kane_run_v4 opt-in; the code-gen sets it for V3 tests.
    if _configure.get("kane_run_v3"):
        capabilities["LT:Options"]["kaneRunV3"] = True

    # Set smart env vars (same as template)
    os.environ["smart_os"] = capabilities["LT:Options"]["platform"]
    os.environ["smart_os_version"] = "latest"
    os.environ["smart_browser_name"] = capabilities["browserName"]
    os.environ["smart_browser_version"] = capabilities["browserVersion"]

    return capabilities


def get_cdp_url(capabilities: dict) -> str:
    """Build the LambdaTest CDP WebSocket URL from a capabilities dict."""
    return "wss://cdp.lambdatest.com/playwright?capabilities=" + urllib.parse.quote(
        json.dumps(capabilities)
    )


def _sanitize_lt_options(lt_options: dict) -> dict:
    """Return a copy of LT:Options with credentials masked for safe logging."""
    masked = dict(lt_options)
    if masked.get("accessKey"):
        masked["accessKey"] = "****************"
    if masked.get("user"):
        masked["user"] = "****"
    return masked


def _sanitize_capabilities(capabilities: dict) -> dict:
    """Return a copy of the full capabilities dict with LT:Options masked."""
    safe = dict(capabilities)
    if "LT:Options" in safe:
        safe["LT:Options"] = _sanitize_lt_options(safe["LT:Options"])
    return safe


def get_cdp_url_for_log(capabilities: dict) -> str:
    """Build the CDP URL with credentials masked — safe for log output."""
    return "wss://cdp.lambdatest.com/playwright?capabilities=" + urllib.parse.quote(
        json.dumps(_sanitize_capabilities(capabilities))
    )


def get_viewport(resolution: str = None) -> dict:
    """Parse a resolution string like '1920x1080' into a viewport dict."""
    _res = resolution or os.getenv("LT_RESOLUTION", "1920x1080")
    try:
        width_str, height_str = _res.lower().split("x")
        return {"width": int(width_str), "height": int(height_str)}
    except (ValueError, AttributeError):
        return {"width": 1920, "height": 1080}
