"""Module-level config dictionary populated from env vars + configure() kwargs.

Public surface: testmu_appium.configure(**kwargs) writes here; runtime modules read.

Three orthogonal flags drive the run() lifecycle:
- run_target: "local" (default) or "cloud". "cloud" connects to the LambdaTest
              mobile hub; "local" connects to an Appium server (a locally
              attached device or emulator) for dev iteration.
- lt_auth:    LT credentials present. Enables ATMS variable lookups, autoheal,
              and cloud reporting regardless of run target.
- smart:      autoheal + AI-backed helpers enabled. Default "1"; run() hard-fails
              for a cloud target without lt_auth and warn-degrades locally.
"""
import os
from typing import Any

# Run-target / auth flags — read at module import; tests patch via
# `patch("testmu_appium._config.run_target", ...)` or reload with env set.
run_target = os.getenv("TESTMU_RUN_TARGET", "local").lower()
lt_auth = bool(os.getenv("LT_USERNAME")) and bool(os.getenv("LT_ACCESS_KEY"))

#: The configured smart flag. This module attribute is the single source of truth —
#: `configure(smart=...)` writes it as well as the config dict, because every gate in
#: the package reads it here rather than out of the dict.
smart = os.getenv("TESTMU_SMART", "1") == "1"

#: Set by run()'s smart gate for the duration of ONE session when smart was asked for
#: but LT credentials are absent. Kept separate from `smart` so the gate degrades this
#: run without permanently clearing a configured value for later runs in the same
#: process — run() resets it at session start.
_smart_degraded = False


#: Whether a find that FAILED may be silently recovered. A narrower question than
#: `smart`, which asks whether AI calls may happen at all: an action grounded by
#: vision is PERFORMED by an AI call rather than rescued by one, so a caller that
#: wants no silent recovery — an authoring run, whose recorded selectors must
#: describe what was actually touched — turns this off and leaves `smart` alone.
heal = os.getenv("TESTMU_HEAL", "1") == "1"


def smart_enabled() -> bool:
    """Whether smart features (autoheal, the AI-backed helpers) may run.

    The resolved read every gate goes through: the configured flag, minus any
    degrade the current session's smart gate applied.
    """
    return bool(smart) and not _smart_degraded


def heal_enabled() -> bool:
    """Whether autoheal may run. Implies smart: heal is one of the smart features."""
    return smart_enabled() and bool(heal)


def _set_smart_degraded(value: bool) -> None:
    global _smart_degraded
    _smart_degraded = value

_DEFAULT_APPIUM_URL = "http://127.0.0.1:4723"
#: Host port Appium forwards to the on-device MJPEG broadcaster when the binding sets
#: `appium:mjpegServerPort`. Perception reads frames off 127.0.0.1 on this port.
_DEFAULT_MJPEG_PORT = 7813
_PROD_LT_MOBILE_HUB_URL = "https://mobile-hub.lambdatest.com/wd/hub"
_PROD_AI_API_HOST = "https://kaneai-api.lambdatest.com/v16-server"
_PROD_AUTOMIND_URL = "https://kaneai-api.lambdatest.com"

#: Platforms the binding accepts as configuration. iOS is accepted day one so its
#: arrival is a data event (strategy column, keycode map, options row) rather than
#: a code change; the runtime tables raise UnsupportedOnPlatform until they ship.
KNOWN_PLATFORMS = ("android", "ios")

#: What a udid can name. Mirrors the runner's own vocabulary so a value can be
#: handed straight through without translation.
KNOWN_TARGET_KINDS = ("physical", "emulator", "simulator")

#: Which path serves a perception screenshot. "auto" tries the MJPEG stream where it
#: can be reachable and falls back to the Appium screencap; "mjpeg" takes the stream
#: only, with no fallback; "appium" never opens the stream.
SOURCE_AUTO = "auto"
SOURCE_MJPEG = "mjpeg"
SOURCE_APPIUM = "appium"
SCREENSHOT_SOURCES = (SOURCE_AUTO, SOURCE_MJPEG, SOURCE_APPIUM)


def _resolve_appium_url() -> str:
    """Resolve the local Appium server URL: APPIUM_URL > http://127.0.0.1:4723.

    Pure: reads env only, never writes os.environ.
    """
    return os.getenv("APPIUM_URL") or _DEFAULT_APPIUM_URL


def get_api_proxy_url() -> str | None:
    """Proxy URL for execute_api() traffic only — never the binding's own AI/LT calls.

    Same env contract as the web binding (testmu): TESTMU_API_PROXY_PORT turns it
    on, TESTMU_API_PROXY_HOST picks the host (default 127.0.0.1). Unset means no
    proxy. Unlike testmu there is no cloud default — routing is strictly opt-in
    via env, so generated tests behave as before unless the environment sets it.

    Resolved at call time, not import time: auteur sets these vars after the
    device's mitm proxy port is known, which is after this module imports.
    """
    port = os.getenv("TESTMU_API_PROXY_PORT")
    if not port:
        return None
    host = os.getenv("TESTMU_API_PROXY_HOST", "127.0.0.1")
    return f"http://{host}:{port}"


def _normalize_hub_url(url: str) -> str:
    """Widen a V2-style bare hub host to a complete WebDriver endpoint.

    Forge and code-export both export LT_HUB_URL as a bare host
    (mobile-hub.lambdatest.com) because V2's generated code composed the
    wd/hub URL itself; this binding passes the value verbatim to
    webdriver.Remote, where a bare host 404s on /session.
    """
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    if not url.rstrip("/").endswith("/wd/hub"):
        url = f"{url.rstrip('/')}/wd/hub"
    return url


def _resolve_lt_hub_url() -> str:
    """Resolve the LambdaTest mobile hub URL: LT_HUB_URL > prod mobile hub.

    Note the mobile hub host differs from the selenium sibling's desktop hub
    (hub.lambdatest.com); a desktop hub URL will not start a device session.
    """
    return _normalize_hub_url(os.getenv("LT_HUB_URL") or _PROD_LT_MOBILE_HUB_URL)


def _resolve_ai_api_host() -> str:
    """Resolve the v16-server host serving /api/v1/autoheal and the query helpers."""
    return os.getenv("TESTMU_AI_API_HOST") or _PROD_AI_API_HOST


def _resolve_automind_url() -> str:
    """Resolve the automind host: AUTEUR_AUTOMIND > AUTOMIND_URL > prod default.

    A different host family from the AI API above — automind serves the DB proxy;
    v16-server serves autoheal and the query helpers. Do not conflate them.
    """
    return (
        os.getenv("AUTEUR_AUTOMIND")
        or os.getenv("AUTOMIND_URL")
        or _PROD_AUTOMIND_URL
    )


# Module-level config dict — populated by configure() at module-import time of
# the generated test.py.
_config: dict[str, Any] = {
    # Session identity / app under test
    "app_id": "",           # Android package now, iOS bundleId later — neutral by design
    "platform": "android",
    "udid": "",
    # What KIND of target the udid names: "physical" | "emulator" | "simulator".
    # The caller resolved this from real discovery (simctl lists simulators, an
    # emulator-NNNN serial names an emulator), so it is authoritative where it is
    # set. Empty means "not told" — the iOS web surface then resolves the kind
    # itself, which is what keeps a standalone generated test correct.
    "target_kind": "",
    "device_name": "",
    "platform_version": "",
    "no_reset": True,
    "app": "",              # cloud app URL (lt://...) when the app is uploaded
    "appium_version": "",   # LT:Options appiumVersion (e.g. "2.11.4-kane-ai"); hub default when empty

    # Test-manager identity + recorded data bags
    "tc_id": "",
    "environment_id": "",
    "uploaded_files": {},

    # Public run metadata
    "build": None,
    "name": None,
    "capability": None,
    "custom_capabilities": {},
    # Extra LT:Options entries merged over the derived block (explicit wins) —
    # the seam the generated shim feeds test-config caps through.
    "lt_options": {},
    # The authored-settings tier, baked at export time (V2's fixed_caps):
    # merged AFTER lt_options, so authoring-session choices survive a forge
    # test-run config swap — V2's exact precedence.
    "lt_options_fixed": {},
    # Appium settings applied via driver.update_settings() at session start —
    # V2 popped these OUT of lt:options and applied them the same way; they
    # are never a hub capability.
    "driver_settings": {},
    "test_metadata": {},

    # Version gates
    "kane_version": "v4",
    "kane_run_v4": True,

    # Timeouts (ms)
    # Named for web testmu.configure() parity — the generator emits this key.
    "default_action_timeout_ms": int(os.getenv("TESTMU_ACTION_TIMEOUT_MS", "10000")),
    "settle_timeout_ms": int(os.getenv("TESTMU_SETTLE_TIMEOUT_MS", "3000")),
    "heal_timeout_ms": int(os.getenv("TESTMU_HEAL_TIMEOUT_MS", "60000")),
    "new_command_timeout_s": int(os.getenv("TESTMU_NEW_COMMAND_TIMEOUT_S", "300")),

    # Identity (env-driven; the host runtime can override at run() time)
    "username": os.getenv("LT_USERNAME", ""),
    "accesskey": os.getenv("LT_ACCESS_KEY", ""),
    "test_id": os.getenv("TEST_ID", ""),
    "commit_id": os.getenv("COMMIT_ID", ""),
    "org_id": int(os.getenv("ORG_ID", "0") or "0"),
    "appium_url": _resolve_appium_url(),
    "lt_hub_url": _resolve_lt_hub_url(),
    "ai_api_host": _resolve_ai_api_host(),
    "automind_url": _resolve_automind_url(),

    # Feature flags
    "smart": os.getenv("TESTMU_SMART", "1") == "1",

    # Perception screenshot path
    "screenshot_source": os.getenv("TESTMU_SCREENSHOT_SOURCE", SOURCE_AUTO).lower(),
    "mjpeg_port": int(os.getenv("TESTMU_MJPEG_PORT", str(_DEFAULT_MJPEG_PORT))),
}


# Keys explicitly set via configure()/set_value() — distinguishes "configured to a
# falsy value" from "left at default" (needed for bool caps).
_configured_keys: set = set()


def get(key: str, default=None):
    """Read a config value. Used by other modules; not in __all__."""
    return _config.get(key, default)


def set_value(key: str, value):
    """Write a config value. Used by configure(); not public."""
    _config[key] = value
    _configured_keys.add(key)


def was_set(key: str) -> bool:
    """Return True if key was explicitly written via set_value()/configure()."""
    return key in _configured_keys


def platform() -> str:
    """The configured platform, normalized to lowercase."""
    return str(_config.get("platform") or "android").lower()


def resolved(key: str, resolver):
    """A URL/host value: an explicit configure() setting wins, else resolve live.

    The dict's seed value is a snapshot taken at import. Falling back to the
    resolver rather than that snapshot means a host runtime that publishes its env
    after importing the binding is still honoured, while an explicit configure()
    call still takes precedence over the environment.
    """
    if was_set(key):
        return _config[key]
    return resolver()
