"""run(fn) — session lifecycle for a single mobile device.

open_session(entry) / close_session(status) are the same lifecycle split in two for
a host process that owns the test body: the first starts the cloud session run()
would start for a test-config entry and leaves it open, the second reports the
verdict and tears it down.

Branches on _config.run_target:
- "cloud": appium.webdriver.Remote against the LambdaTest MOBILE hub (a different
  host from the selenium sibling's desktop hub — a desktop hub URL will not start a
  device session).
- "local" (default): appium.webdriver.Remote against a local Appium server, i.e. an
  attached device or emulator.

The options factory is a platform-keyed adapter row ("session_options" registry),
not a branch fork: adding iOS is filling the declared-empty ios row with the
XCUITestOptions entries, which is what makes iOS a data event rather than a code
change.

The verdict reaches the LambdaTest dashboard through the reporter's
`lambda-status=<passed|failed>` hook. Without it HyperExecute classifies the scenario
as "skipped" regardless of exit code.
"""
import contextlib
import logging
import os
import sys
import time
from typing import Callable

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from testmu_appium import _config
from testmu_appium._configure import configure
from testmu_appium._errors import TestmuConfigError
from testmu_appium._v4._helpers import _adapters, _mjpeg, _web
from testmu_appium._v4._helpers.driver import _clear_drivers, _set_driver, get_driver
from testmu_appium._v4._helpers.network_throttle import network_throttle
from testmu_appium._v4._reporter import _reset_reporter, reporter
from testmu_appium._step import _reset_step_counter
from testmu_appium._v4._test_config import test_config_overrides
from testmu_appium._test_state import (
    has_pending_failures, pending_failures_summary, reset_test_state,
)

_log = logging.getLogger("testmu_appium")


def _android_options() -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("appium:automationName", "UiAutomator2")

    # app_id is the neutral identity field: the Android package here, the iOS bundleId
    # when that row ships. Nothing Android-specific is burned into the artifact.
    if _config.get("app_id"):
        options.set_capability("appium:appPackage", _config.get("app_id"))
    # Device targeting rides LT:Options on a cloud run: the LT allocator matches
    # LT:Options.deviceName as a regex, but an appium:deviceName literally — a
    # regex there matches no device and the session dies on
    # QUEUE_TIMEOUT_DEVICE_UNAVAILABLE. Same split for app/udid/platformVersion
    # (the V2 bundle's proven contract).
    cloud = _config.run_target == "cloud"
    if _config.get("app") and not cloud:
        options.set_capability("appium:app", _config.get("app"))
    if _config.get("udid") and not cloud:
        options.set_capability("appium:udid", _config.get("udid"))
    if _config.get("device_name") and not cloud:
        options.set_capability("appium:deviceName", _config.get("device_name"))
    if _config.get("platform_version") and not cloud:
        options.set_capability("appium:platformVersion", str(_config.get("platform_version")))

    options.set_capability("appium:noReset", bool(_config.get("no_reset", True)))
    options.set_capability(
        "appium:newCommandTimeout", int(_config.get("new_command_timeout_s", 300))
    )
    # Every V2 android session ran with the Unicode IME on (build_caps defaulted
    # unicode_keyboard to True, and the export-baked fixed tier carries the
    # authored enableKeyboard choice) — without it, non-ASCII typing regresses.
    # A default, not a constant: either override tier owns the value on the hub
    # side, so the driver-level cap yields too.
    if not any("unicodeKeyboard" in (_config.get(k) or {})
               for k in ("lt_options", "lt_options_fixed")):
        options.set_capability("appium:unicodeKeyboard", True)

    # Appium forwards this host port to the on-device MJPEG broadcaster, which
    # perception reads frames off instead of paying a screencap round trip. Claimed
    # only where 127.0.0.1 can reach the forward: a cloud session's forward lives on
    # the device host, so its capability set stays untouched.
    if _mjpeg.wanted():
        options.set_capability("appium:mjpegServerPort", _mjpeg.port())
    return options


def _ios_options() -> XCUITestOptions:
    options = XCUITestOptions()
    options.set_capability("platformName", "iOS")
    options.set_capability("appium:automationName", "XCUITest")

    # The Android row's counterpart: `app_id` is the neutral identity field, and it
    # lands on the capability each platform names it with — appPackage there,
    # bundleId here. The recorded artifact stays platform-portable.
    if _config.get("app_id"):
        options.set_capability("appium:bundleId", _config.get("app_id"))
    # Cloud device targeting rides LT:Options only — see _android_options.
    cloud = _config.run_target == "cloud"
    if _config.get("app") and not cloud:
        options.set_capability("appium:app", _config.get("app"))
    if _config.get("udid") and not cloud:
        options.set_capability("appium:udid", _config.get("udid"))
    if _config.get("device_name") and not cloud:
        options.set_capability("appium:deviceName", _config.get("device_name"))
    if _config.get("platform_version") and not cloud:
        options.set_capability("appium:platformVersion", str(_config.get("platform_version")))

    options.set_capability("appium:noReset", bool(_config.get("no_reset", True)))
    options.set_capability(
        "appium:newCommandTimeout", int(_config.get("new_command_timeout_s", 300))
    )

    # Two waits XCUITest inserts that an agent pays on EVERY step and needs on
    # none: quiescence blocks each command until the app reports idle (an
    # animating page never does), and the animation cool-off re-arms that wait
    # after every action. The driver-settings `waitForIdleTimeout` only covers
    # the per-step idle wait — these two are separate, session-level costs.
    options.set_capability("appium:waitForQuiescence", False)
    options.set_capability("appium:animationCoolOffTimeout", 0)

    # WebDriverAgent serves the same MJPEG broadcaster the Android row claims, on the
    # same capability, so perception reads frames instead of paying a screenshot
    # round trip. Claimed only where 127.0.0.1 can reach the forward — a cloud
    # session's forward lives on the device host, so its capabilities stay untouched.
    if _mjpeg.wanted():
        options.set_capability("appium:mjpegServerPort", _mjpeg.port())
    return options


#: platform → options operations: "derive" builds the full option set from
#: configure()'d fields; "blank" is the bare options class an explicit
#: capability dict is written onto. The ios row is declared empty.
_adapters.register("session_options", {
    "android": {"derive": _android_options, "blank": UiAutomator2Options},
    "ios": {"derive": _ios_options, "blank": XCUITestOptions},
})


def _lt_options() -> dict:
    """The LT:Options block for a cloud mobile session."""
    lt = {
        "isRealMobile": True,
        "w3c": True,
    }
    for key, cap in (
        ("build", "build"), ("name", "name"),
        ("device_name", "deviceName"), ("platform_version", "platformVersion"),
        # Cloud-side install/pin/runtime facts the appium: namespace must not
        # carry (see _android_options): the lt:// app URL the hub installs, the
        # private-cloud device pin, and the hub's appium build (V2 pins the
        # kane-ai builds, e.g. "2.11.4-kane-ai").
        ("app", "app"), ("udid", "udid"), ("appium_version", "appiumVersion"),
    ):
        if _config.get(key):
            lt[cap] = _config.get(key)
    if _config.get("username"):
        lt["user"] = _config.get("username")
    if _config.get("accesskey"):
        lt["accessKey"] = _config.get("accesskey")
    # TMS session linkage — V2 always sent it and nothing else in this binding
    # conveys it (the reporter has no tc_id field).
    if _config.get("tc_id"):
        lt["tms.tc_id"] = _config.get("tc_id")
    # V2-parity android default (see _android_options). Before the merges below,
    # so a caller-supplied value wins.
    if _config.get("platform") == "android":
        lt["unicodeKeyboard"] = True
    # V2 set this on every session (test.py __main__), unconditionally.
    lt["enableMultiWindows"] = True
    # Two override tiers, matching V2's precedence exactly:
    #   derived defaults  <  lt_options (test-config translation, swappable
    #   per run)  <  lt_options_fixed (export-baked authored settings — V2's
    #   fixed_caps, applied after build_caps so they survive the run swap).
    lt.update(_config.get("lt_options") or {})
    lt.update(_config.get("lt_options_fixed") or {})
    return lt


def build_options(platform: str):
    """Build the session options for a platform.

    An explicit `capability=` dict wins outright — the host runtime that supplied it
    has already resolved everything, and re-deriving fields over the top would silently
    override its choices.
    """
    platform = (platform or "").lower()
    feature = f"session options for platform {platform!r}"

    explicit = _config.get("capability")
    if explicit:
        options = _adapters.adapter("session_options", "blank", feature, platform=platform)()
        for key, value in explicit.items():
            options.set_capability(key, value)
        return options

    options = _adapters.adapter("session_options", "derive", feature, platform=platform)()
    if _config.run_target == "cloud":
        options.set_capability("LT:Options", _lt_options())
    for key, value in (_config.get("custom_capabilities") or {}).items():
        options.set_capability(key, value)
    return options


def _export_smart_env_from_session(driver) -> None:
    """Populate the ``smart_*`` env vars ``_resolve_smart`` reads, from the LIVE
    session, so ``{{smart.device_os|device_os_version|device_name|
    app_package_name|app_version}}`` resolve to real values in a standalone
    generated test.

    The selenium binding does the same for its browser fields, and for the same
    reason: an exported mobile test is configure-based with no runtime around it
    to seed them, so the session — the one place that knows what it connected to
    — is where they come from. The configured value wins over the negotiated
    capability where both exist: it is what the test was written against.

    ``device_orientation`` is deliberately absent. It is the one value that
    changes mid-run, so it is asked of the driver at the moment of use instead.
    """
    caps = getattr(driver, "capabilities", None) or {}

    def _first(*values) -> str:
        for value in values:
            if value:
                return str(value)
        return ""

    exported = {
        "smart_device_os": _first(_config.get("platform"), caps.get("platformName")),
        "smart_device_os_version": _first(
            _config.get("platform_version"), caps.get("platformVersion")),
        "smart_device_name": _first(
            _config.get("device_name"), caps.get("deviceName")),
        "smart_app_package_name": _first(
            _config.get("app_id"), caps.get("appPackage"), caps.get("bundleId")),
        "smart_app_version": _first(caps.get("appVersion")),
    }
    for key, value in exported.items():
        # Cleared, not skipped, when this session cannot answer. The env is
        # process-global while a driver is per-profile, so leaving a stale key
        # in place lets a second session in the same process inherit the
        # first's device — app_version in particular is rarely a capability.
        if value:
            os.environ[key] = value
        else:
            os.environ.pop(key, None)


#: The appium settings a cloud session starts with, per platform — the ones the
#: authoring session applies. Configured driver_settings are applied over them.
#: waitForIdleTimeout is milliseconds on UiAutomator2 and seconds on XCUITest.
_CLOUD_SESSION_SETTINGS = {
    "android": {
        "allowInvisibleElements": True,
        "includeA11yActionsInPageSource": True,
        "waitForIdleTimeout": 5000,
    },
    "ios": {
        "snapshotMaxDepth": 60,
        "waitForIdleTimeout": 5.0,
    },
}


def _apply_driver_settings(driver) -> None:
    """Configured appium settings, applied once at session start — V2's setUp.

    V2 popped driver_settings out of lt:options and called
    driver.update_settings() with them (plus a fixed iOS respectSystemAlerts,
    which wins over the configured set, mirroring fixed_driver_settings).
    A cloud session starts from _CLOUD_SESSION_SETTINGS for its platform.
    Never a hub capability. A settings failure is logged, not fatal — the
    session is live and most settings only tune tree depth / idle waits.
    """
    settings: dict = {}
    if _config.run_target == "cloud":
        platform = str(_config.get("platform") or "").lower()
        settings.update(_CLOUD_SESSION_SETTINGS.get(platform, {}))
    settings.update(_config.get("driver_settings") or {})
    if _config.get("platform") == "ios":
        settings["respectSystemAlerts"] = True
    if not settings:
        return
    try:
        driver.update_settings(settings)
        _log.info("[testmu] applied driver settings: %s", settings)
    except Exception as e:  # noqa: BLE001 — session is live; settings are tuning, not identity
        _log.warning("[testmu] driver.update_settings(%s) failed: %s", settings, e)


def _apply_initial_network_throttle(driver) -> None:
    """Apply the advanced-settings network prerequisite, matching V2 setup.

    Skipped on a virtual device (LT:Options isRealMobile false), which has no
    network throttling.
    """
    profile = os.getenv("NETWORK_PROFILE", "default")
    if profile == "default":
        return
    if _lt_options().get("isRealMobile") is False:
        return
    network_throttle(
        driver,
        profile=profile,
        download_kbps=int(os.getenv("DOWNLOAD_SPEED", "0")),
        upload_kbps=int(os.getenv("UPLOAD_SPEED", "0")),
        latency_ms=int(os.getenv("LATENCY", "0")),
    )


def _apply_smart_gate() -> None:
    """Smart requires LT auth. Fatal for a cloud target, degraded locally.

    The local degrade is scoped to THIS session: the configured `smart` flag is left
    alone, so a later run in the same process that does have credentials still gets
    smart features.
    """
    _config._set_smart_degraded(False)
    if not _config.smart or _config.lt_auth:
        return
    if _config.run_target == "cloud":
        raise TestmuConfigError(
            "TESTMU_SMART is enabled for a cloud run but LT_USERNAME/LT_ACCESS_KEY are "
            "not set — autoheal and the AI-backed helpers cannot authenticate"
        )
    _log.warning(
        "[testmu] TESTMU_SMART is enabled but LT credentials are absent — running with "
        "smart features disabled"
    )
    _config._set_smart_degraded(True)


def _reset_session_state() -> None:
    """Clear what the previous session in this process left behind."""
    _reset_step_counter()
    reset_test_state()
    _reset_reporter()
    # The MJPEG stream's reachability is a property of the session about to start.
    _mjpeg.reset()
    # So is the device's debug channel, whose port forwards this releases.
    _web.reset()


def _start_session(profile: str):
    """Connect to the configured target and register the driver.

    Returns the driver and the reporter bound to it.
    """
    _apply_smart_gate()

    platform = _config.platform()
    _log.info(
        "Mode: run_target=%s, platform=%s, lt_auth=%s, smart=%s",
        _config.run_target, platform, _config.lt_auth, _config.smart_enabled(),
    )

    options = build_options(platform)
    if _config.run_target == "cloud":
        url = _config.resolved("lt_hub_url", _config._resolve_lt_hub_url)
        _log.info("[testmu] connecting to the LambdaTest mobile hub: %s", url)
    else:
        url = _config.resolved("appium_url", _config._resolve_appium_url)
        _log.info("[testmu] connecting to the local Appium server: %s", url)

    driver = webdriver.Remote(command_executor=url, options=options)
    _set_driver(profile, driver)
    _export_smart_env_from_session(driver)
    _apply_driver_settings(driver)
    _apply_initial_network_throttle(driver)
    rep = reporter()
    rep.set_driver(driver)
    return driver, rep


def _end_session(driver) -> None:
    """Settle, release what the session claimed, quit, clear the registry."""
    _settle_before_teardown(driver)
    # An unfinalized SmartUI build never completes server-side; never raises.
    from testmu_appium._v4._helpers.smartui import finalize_smartui
    finalize_smartui()
    # Anything we changed on the device, we change back — a leaked port
    # forward outlives the session that made it.
    _web.reset()
    try:
        driver.quit()
    except Exception as e:  # noqa: BLE001 — teardown must not replace the verdict
        _log.warning("[testmu] driver.quit() failed: %s", e)
    _clear_drivers()


def run(fn: Callable, profile: str = "default") -> None:
    """Launch the session, invoke fn(driver), tear down.

    THE SINGLE VERDICT OWNER. Exactly one of pass_test/fail_test is emitted, on every
    path; `@testmu_appium.test` deliberately emits none.

    Raises at the end when any fail-continue step failed: those exceptions were
    swallowed at the step, so without this the process exits 0 and the dashboard
    reads PASSED despite failed steps.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    _reset_session_state()
    driver, rep = _start_session(profile)

    # EXACTLY ONE verdict call on every path. The body's own exception wins precedence
    # over the aggregate summary — its class and message are more specific — and the
    # pending-failure raise sits outside the body's except so its RuntimeError is not
    # re-caught into a second fail_test.
    try:
        try:
            fn(driver)
        except Exception as e:
            rep.fail_test(e)
            raise
        if has_pending_failures():
            message = (
                f"Test had non-fatal failures (fail-continue): "
                f"{pending_failures_summary()}"
            )
            error = RuntimeError(message)
            rep.fail_test(error)
            raise error
        rep.pass_test()
    finally:
        _end_session(driver)


#: configure() keys a test-config entry may leave out. open_session() puts each
#: back to its seed value before the entry's own values are applied.
_ENTRY_KEYS = (
    "device_name", "platform_version", "app", "appium_version", "tc_id", "udid",
    "name", "build", "lt_options", "driver_settings",
)


def open_session(entry: dict, *, username: str, access_key: str):
    """Start the cloud session a test-config entry describes and return its driver.

    The session run() would start for the same entry — capabilities, driver
    settings, initial network throttle — registered and left open. Runs no test
    body, emits no verdict and quits nothing; close_session() ends it.
    """
    if _config.run_target != "cloud":
        raise TestmuConfigError(
            "open_session needs a cloud run target — set TESTMU_RUN_TARGET=cloud "
            "before testmu_appium is imported"
        )
    if not isinstance(entry, dict):
        raise TestmuConfigError(
            f"open_session entry must be a dict; got {type(entry).__name__}"
        )
    if not username or not access_key:
        raise TestmuConfigError("open_session needs a username and an access_key")
    if get_driver() is not None:
        raise TestmuConfigError(
            "a session is already open — call close_session() first"
        )

    platform = str(entry.get("platform_name") or "").lower()
    mapped = dict(entry)
    mapped["platform_name"] = platform
    # The mapper prints the keys it does not honor; stdout belongs to the host.
    with contextlib.redirect_stdout(sys.stderr):
        overrides = test_config_overrides(mapped)

    settings = {key: _config.seed_value(key) for key in _ENTRY_KEYS}
    settings.update(overrides)
    settings.update(
        platform=platform,
        app_id=str(entry.get("app_package") or ""),
        username=username,
        accesskey=access_key,
    )
    configure(**settings)
    _config.lt_auth = True

    _reset_session_state()
    try:
        driver, _ = _start_session("default")
    except Exception:
        started = get_driver()
        if started is not None:
            _end_session(started)
        raise
    return driver


def close_session(status: str, remark: str = "") -> None:
    """Report the verdict on the session open_session() started, then end it.

    `status` is "passed" or "failed". Emits exactly one verdict, settles, quits
    and clears the registry. A no-op when no session is open.
    """
    if status not in ("passed", "failed"):
        raise ValueError(
            f"close_session status must be 'passed' or 'failed'; got {status!r}"
        )
    driver = get_driver()
    if driver is None:
        _log.info("[testmu] close_session: no open session")
        return
    _log.info("[testmu] closing the session: status=%s remark=%s", status, remark)
    try:
        rep = reporter()
        if status == "passed":
            rep.pass_test()
        else:
            rep.fail_test(RuntimeError(remark or "failed"))
    finally:
        _end_session(driver)


def _settle_before_teardown(driver) -> None:
    """Best-effort pause before quitting so a cloud session's video encoder can flush
    the final action's frames. No-op locally — there is no grid-side encoder."""
    if _config.run_target != "cloud":
        return
    import os

    drain_ms = int(os.getenv("TESTMU_TEARDOWN_VIDEO_DRAIN_MS", "2000"))
    if drain_ms > 0:
        time.sleep(drain_ms / 1000.0)
