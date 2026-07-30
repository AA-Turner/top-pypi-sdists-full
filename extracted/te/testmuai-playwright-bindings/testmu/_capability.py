"""TestMu capability builder for Playwright Python (LambdaTest grid).

Configuration is sourced from testmu.configure() data first, then falls back
to environment variables. browser/browser_version/resolution/platform additionally
fall back to sys.argv[1:5] — the positional HyperExecute test-matrix args
(browser, browser_version, resolution, platform) that the legacy/non-binding
export_mixin.py flow already relies on (see _test_config.py, which reads the
same sys.argv[4] position to select the platform's test-instance list).
"""

import json
import logging
import os
import sys
import urllib.parse
from pathlib import Path

from testmu import _configure

_log = logging.getLogger("testmu")

# KaneAI/HYE mac hub token → playwright-grid platform display name.
_MAC_PLATFORM_NAMES = {
    "mac10.15": "macOS Catalina",
    "mac11": "macOS Big Sur",
    "mac12": "macOS Monterey",
    "mac13": "macOS Ventura",
    "mac14": "macOS Sonoma",
    "mac15": "macOS Sequoia",
}

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


def _bool_he(key: str, default: bool) -> bool:
    """Resolve a boolean capability: HE test_config > env var > default.

    Module-level (not just a get_capabilities() helper) so other callers —
    e.g. testmu._session's cloud-teardown video gate — can reuse the exact
    same VIDEO/CONSOLE/etc. resolution instead of re-deriving it.
    """
    from testmu._test_config import get_cap_value

    val = get_cap_value(key, None)
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    return str(val).lower() in ("1", "true", "yes")


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

    # Resolve top-level fields: explicit param > HyperExecute matrix argv > env > default.
    # HyperExecute invokes the test script with browser/browser_version/resolution/platform
    # as sys.argv[1:5] for the discovered matrix row (e.g. "chrome 149.0 1440x900 linux") —
    # without this, every binding-mode run silently gets the hardcoded defaults below.
    _argv_browser = sys.argv[1] if len(sys.argv) > 1 else None
    _argv_browser_version = sys.argv[2] if len(sys.argv) > 2 else None
    _argv_resolution = sys.argv[3] if len(sys.argv) > 3 else None
    _argv_platform = sys.argv[4] if len(sys.argv) > 4 else None

    _browser = browser or _argv_browser or os.getenv("LT_BROWSER", "Chrome")
    _browser_version = (
        browser_version or _argv_browser_version or os.getenv("LT_BROWSER_VERSION", "latest")
    )
    _resolution = resolution or _argv_resolution or os.getenv("LT_RESOLUTION", "1920x1080")
    _platform = platform or _argv_platform or os.getenv("LT_PLATFORM", "linux")

    # KaneAI/HYE environments carry mac hub tokens (mac12, mac13, ...); the playwright
    # gateway's platform grammar is display-name style ("macOS Monterey" → parsed as
    # "macos 12.0"). An unrecognized platform is queued forever by the gateway (no 400)
    # until the client's connect timeout — grid-observed with "mac12" + pw-webkit.
    # Normalize known mac tokens; anything else passes through verbatim.
    _normalized_platform = _MAC_PLATFORM_NAMES.get(_platform.strip().lower(), _platform)
    if _normalized_platform != _platform:
        _log.info(
            "platform '%s' -> '%s' (playwright grid platform name)",
            _platform,
            _normalized_platform,
        )
        _platform = _normalized_platform

    # Safari → pw-webkit: the playwright relay has no real Safari — its browserName
    # allowlist is [chrome MicrosoftEdge pw-chromium pw-webkit pw-firefox island].
    # Map explicitly and loudly; a safari environment must never silently run Chrome.
    # pw-webkit's WebKit version tracks the Playwright driver, so a UI-selected Safari
    # version (e.g. "15.0") is meaningless — coerce to "latest".
    _is_webkit = _browser.lower() in ("safari", "webkit", "pw-webkit")
    if _is_webkit:
        _log.info(
            "browser '%s' -> 'pw-webkit' (Playwright WebKit — the relay's Safari slot)",
            _browser,
        )
        if _browser_version.lower() != "latest":
            _log.warning(
                "browserVersion '%s' ignored for pw-webkit — WebKit version tracks "
                "the Playwright driver; forcing 'latest'",
                _browser_version,
            )
        _browser = "pw-webkit"
        _browser_version = "latest"

    # Firefox → pw-firefox: the relay has no plain "firefox" — the allowlist offers only
    # pw-firefox (Playwright's bundled Firefox). Map explicitly or the grid rejects the
    # connection ("browserName firefox not supported"). Like pw-webkit, the bundled build's
    # version tracks the Playwright driver, so a UI-selected Firefox version is meaningless.
    _is_firefox = _browser.lower() in ("firefox", "pw-firefox")
    if _is_firefox:
        _log.info(
            "browser '%s' -> 'pw-firefox' (Playwright Firefox — the relay's Firefox slot)",
            _browser,
        )
        if _browser_version.lower() != "latest":
            _log.warning(
                "browserVersion '%s' ignored for pw-firefox — Firefox version tracks "
                "the Playwright driver; forcing 'latest'",
                _browser_version,
            )
        _browser = "pw-firefox"
        _browser_version = "latest"

    # Edge → MicrosoftEdge: the relay's allowlist token is the exact, case-sensitive
    # "MicrosoftEdge". LT_BROWSER arrives lowercased ("edge"), so canonicalize it here — the
    # browserName is then grid-valid without leaning on the proxy, and the ms:edgeOptions
    # branch (which keys on "microsoftedge") fires. Edge is real on the grid — keep its version.
    if _browser.lower() in ("edge", "microsoftedge", "microsoft edge"):
        if _browser != "MicrosoftEdge":
            _log.info(
                "browser '%s' -> 'MicrosoftEdge' (playwright grid browserName token)",
                _browser,
            )
        _browser = "MicrosoftEdge"

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

    # loadExtensions=[EXTENSION] (the dom-watcher) — set for every browser EXCEPT WebKit:
    # WebKit loads no extensions, and for safari the EXTENSION env carries lt_utility.js
    # (a JS file, not an extension zip), which must not be sent as loadExtensions.
    if not _is_webkit:
        capabilities["LT:Options"]["loadExtensions"] = [os.getenv("EXTENSION")]

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

    # Emit kaneRunV3 + preCmdVisual for v3-authored runs so the server distinguishes v3 from v2 and captures per-step screenshots.
    if _configure.get("kane_run_v3"):
        capabilities["LT:Options"]["kaneRunV3"] = True
        capabilities["LT:Options"]["preCmdVisual"] = True

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
