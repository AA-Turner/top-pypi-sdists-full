"""test-config entry → configure() kwargs — the V2 build_caps port.

The V2 bundle translated a test-config entry (plus env overrides) into the
session's lt:options at run time, inside the bundled utils.py. The V4 artifact
keeps the same file contract (--test-config / ${TEST_RUN_ID}.json swapped by
forge's run.sh), but the translation lives here: platform branches, secrets
resolution and options tables are binding-side data, so the generated shim
stays platform-free and a mapping fix never touches emitted code.

Session-identity keys map onto first-class configure() kwargs (the binding
derives their LT:Options rows itself); every other cap V2's non-plugin
build_caps honored lands in the ``lt_options`` merge seam. Keys neither table
covers are logged, never silently dropped.
"""
import os
from typing import Any, Optional

#: entry key → configure() kwarg. Identity the binding derives LT:Options from.
_TO_CONFIGURE = {
    "device_name": "device_name",
    "platform_version": "platform_version",
    "app": "app",
    # The hub's appium build for the picked device (e.g. "2.11.4-kane-ai");
    # forwarded as LT:Options.appiumVersion.
    "appium_version": "appium_version",
    "tms.tc_id": "tc_id",
    "test_name": "name",
    "test_params": "test_params",
}

#: Keys read by special-case logic below, or recording bookkeeping — not "ignored".
_HANDLED = {
    "udid", "private_cloud", "test_instance_id", "test_id", "platform_name",
    "folder_name", "project_name", "code_req_name", "session_timezone",
    "driver_settings",
}

#: Entry keys _build_lt_options translates into LT:Options caps (V2 build_caps
#: parity). driver_settings is handled separately: V2 popped it OUT of
#: lt:options and applied it via driver.update_settings() — it maps onto the
#: configure() kwarg of the same name, never a hub cap.
_LT_KEYS = {
    "networkCapture", "custom_headers", "unicode_keyboard",
    "auto_grant_permissions", "auto_accept_alerts", "auto_dismiss_alerts",
    "use_json_source", "disable_app_resigning", "deviceOrientation",
    "device_orientation", "accessibility", "tunnel", "tunnel_name",
    "dedicated_proxy", "geo_location", "google_login_config", "region",
    "mobile_region", "timezone", "locationCoordinates", "passcode",
    "langLocale", "enableBiometricInjection", "enableImageInjection",
    "enableVideoInjection", "enableScreenshotUnblock", "appium_plugins",
}


def _env_bool(key: str, default: bool) -> bool:
    return os.getenv(key, str(default)).lower() == "true"


def _config_value(config: Optional[dict]) -> Optional[str]:
    """A ``{value, isSecretValue}`` pair; a secret value names the env var
    holding the real one."""
    if not config:
        return None
    value = config.get("value")
    if not value:
        return None
    if config.get("isSecretValue", False):
        value = os.environ.get(value)
        if not value:
            return None
    return str(value)


def _build_lt_options(entry: dict) -> dict:
    """V2 build_caps parity, minus the caps the binding already derives from
    configure() fields (deviceName/app/build/name/platformVersion/udid/
    appiumVersion/tms.tc_id/isRealMobile/w3c) — an entry here overrides the
    derived value, so duplicating identity caps would freeze them."""
    platform_name = entry.get("platform_name", "")
    network_capture = bool(entry.get("networkCapture", False))
    lt: dict[str, Any] = {}
    app = entry.get("app", "") or ""
    if app.lower() == "stock":
        lt["autoLaunch"] = False
    lt["privateCloud"] = entry.get("private_cloud", False)
    if platform_name == "android":
        # Present-key check, not truthiness: an explicit false must reach the
        # session once forge can emit one (its omitempty tag drops false today,
        # so the binding's always-true default carries V2's actual behavior).
        if "unicode_keyboard" in entry:
            lt["unicodeKeyboard"] = bool(entry["unicode_keyboard"])
        lt["autoGrantPermissions"] = bool(entry.get("auto_grant_permissions", False))
        lt["allowInvisibleElements"] = True
    else:
        lt["waitForQuiescence"] = False
        lt["useJSONSource"] = bool(entry.get("use_json_source", False))
        lt["pageSourceExcludedAttributes"] = "frame,enabled,focused"
        lt["autoAcceptAlerts"] = bool(entry.get("auto_accept_alerts", False))
        lt["autoDismissAlerts"] = bool(entry.get("auto_dismiss_alerts", False))
        # Enterprise apps ship pre-signed; re-signing breaks them.
        if entry.get("disable_app_resigning", False):
            lt["resignApp"] = False
    # Both spellings: V2's writer/readers used deviceOrientation, forge's
    # TestRunConfig emits device_orientation.
    lt["deviceOrientation"] = entry.get("deviceOrientation") \
        or entry.get("device_orientation") or "AUTO"
    if entry.get("accessibility") is not None:
        lt["accessibility"] = str(entry.get("accessibility")).lower() == "true"
    if str(os.getenv("TUNNEL", entry.get("tunnel", False))).lower() == "true":
        lt["tunnel"] = True
        lt["tunnelName"] = os.getenv("TUNNEL_NAME", entry.get("tunnel_name", "") or "")
    if str(os.getenv("DEDICATED_PROXY", entry.get("dedicated_proxy", False))).lower() == "true":
        lt["dedicatedProxy"] = True
    geo = os.getenv("GEO_LOCATION", entry.get("geo_location", "") or "")
    if geo:
        lt["geoLocation"] = geo
    if platform_name == "android":
        login = entry.get("google_login_config") or {}
        email = _config_value(login.get("email", {}))
        password = _config_value(login.get("password", {}))
        if email and password:
            lt["playStoreLogin"] = {"email": email, "password": password}
    lt["newCommandTimeout"] = 86400
    lt["idleTimeout"] = int(os.getenv("IDLE_TIMEOUT", "1500"))
    lt["queueTimeout"] = int(os.getenv("QUEUE_TIMEOUT", "900"))
    if _env_bool("KANE_NEW_VIEW_ENABLED", False):
        lt["kaneRun"] = True
        lt["preCmdVisual"] = True
    else:
        lt["visual"] = _env_bool("VISUAL", True)
    lt["video"] = _env_bool("VIDEO", True)
    lt["screenshot"] = _env_bool("SCREENSHOT", True)
    lt["network"] = _env_bool("NETWORK", False) or network_capture
    lt["mitmProxy"] = _env_bool("MITM_PROXY", False) or network_capture
    if lt["network"]:
        lt["customHeaders"] = entry.get("custom_headers", {})
    lt["appProfiling"] = _env_bool("APP_PROFILING", False)
    lt["networkProfile"] = "default"
    lt["devicelog"] = _env_bool("DEVICE_LOG", True)
    tz = entry.get("timezone")
    if isinstance(tz, dict) and tz.get("region"):
        lt["timezone"] = tz.get("region")
    coords = entry.get("locationCoordinates")
    if isinstance(coords, dict) and coords.get("latitude") and coords.get("longitude"):
        lt["location"] = {"lat": coords.get("latitude"), "long": coords.get("longitude")}
    if entry.get("passcode"):
        lt["enablePasscode"] = True
        lt["passcode"] = entry["passcode"]
    lang = entry.get("langLocale")
    if isinstance(lang, dict) and lang.get("language") and lang.get("locale"):
        lt["language"] = lang.get("language")
        lt["locale"] = lang.get("locale")
        if lang.get("script") and platform_name == "android":
            lt["localeScript"] = lang.get("script")
    if entry.get("enableBiometricInjection", False):
        lt["enableBiometricsAuthentication"] = True
    if entry.get("enableImageInjection", False):
        lt["enableImageInjection"] = True
    if entry.get("enableVideoInjection", False):
        lt["enableVideoInjection"] = True
    if entry.get("enableScreenshotUnblock", False):
        lt["enableScreenshotUnblock"] = True
    if os.getenv("APP_PACKAGE"):
        lt["appPackage"] = os.getenv("APP_PACKAGE")
    if os.getenv("APP_ACTIVITY"):
        lt["appActivity"] = os.getenv("APP_ACTIVITY")
    lt["isKaneFreemium"] = _env_bool("IS_KANE_FREEMIUM", False)
    # V2's non-plugin flow forwards user-configured appium plugins verbatim
    # (kaneai-code-runner injection is the plugin flow's concern, not ours).
    # An empty list and an absent key mean the same thing to the hub — only
    # forward a real request.
    plugins = entry.get("appium_plugins")
    if isinstance(plugins, list) and plugins:
        lt["appiumPlugins"] = plugins
    return lt


def test_config_overrides(entry: dict) -> dict:
    """The configure() kwargs a test-config entry resolves to.

    The generated shim selects its entry from the --test-config file and calls
    ``configure(**test_config_overrides(entry))`` — nothing else. Env-first
    precedence (BUILD, UDID, TUNNEL, GEO_LOCATION, …) matches V2's build_caps.
    """
    overrides = {kw: entry[key]
                 for key, kw in _TO_CONFIGURE.items() if entry.get(key)}
    # V2 get_app_name parity: an app-id env swaps the app at run time.
    if overrides.get("app"):
        app_env = "ANDROID_APP_ID" if entry.get("platform_name", "") == "android" else "IOS_APP_ID"
        overrides["app"] = os.getenv(app_env, overrides["app"])
    # V2 build_caps parity: udid pins the device only on a private cloud...
    if str(entry.get("private_cloud", "")).lower() in ("true", "1") and entry.get("udid"):
        overrides["udid"] = entry["udid"]
    # ...unless the UDID env pins one outright.
    if os.getenv("UDID"):
        overrides["udid"] = os.getenv("UDID")
    # V2 parity: BUILD env overrides the build name at run time.
    if os.getenv("BUILD"):
        overrides["build"] = os.getenv("BUILD")
    # V2 parity: the session's canonical IANA timezone rides an env var the
    # smart-variables engine reads for date/time resolution.
    if entry.get("session_timezone"):
        os.environ["KANE_SESSION_TIMEZONE"] = entry["session_timezone"]
    lt_options = _build_lt_options(entry)
    if lt_options:
        overrides["lt_options"] = lt_options
    # Applied via driver.update_settings() at session start, exactly like V2's
    # setUp — see _session._apply_driver_settings.
    if entry.get("driver_settings"):
        overrides["driver_settings"] = entry["driver_settings"]
    ignored = sorted(
        k for k in entry
        if k not in _TO_CONFIGURE and k not in _HANDLED and k not in _LT_KEYS
    )
    if ignored:
        print("[testmu] test-config keys not honored yet: %s" % ignored)
    return overrides
