"""run(fn) — single-driver lifecycle entrypoint.

Mirrors V4-Playwright's testmu.run() but sync. Branches on _config.run_target:
- "cloud": webdriver.Remote against the LT hub (LT_USERNAME / LT_ACCESS_KEY).
- "local" (default): direct webdriver.Chrome / webdriver.Firefox for dev iteration,
  headless per TESTMU_HEADLESS=true|false (default true). No LT hub, no creds.

Reports test status to the LambdaTest cloud session before quitting via
the `lambda-status=...` execute_script convention — without this marker
HyperExecute classifies the scenario as "skipped" regardless of exit code
(regression repro: HyperExecute heal cascade ran cleanly but no test_status was recorded,
so HE returned `total_tests:0, status:"skipped"`). Mirrors V2 Selenium's emit of
`driver.execute_script(f"lambda-status={status}")` and V4
playwright's `set_test_status(page, status, remark)` convention.

After status reporting and before `driver.quit()`, cloud runs with video
enabled get a best-effort settle window (see `_settle_before_teardown`) so
the grid's video encoder can flush the final action's frames before the
session tears down.
"""
import logging
import os
import platform
import time
from typing import Callable
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from testmu_selenium import _config
from testmu_selenium._config import _config as _config_dict
from testmu_selenium._capability import _bool_he, build_capability
from testmu_selenium._helpers.driver import _set_driver, _clear_drivers
from testmu_selenium._route_failure import (
    _has_pending_failures,
    _pending_failures_summary,
    _reset_pending_failures,
)
from testmu_selenium._step import _reset_step_counter

logger = logging.getLogger(__name__)


def _export_smart_env_from_session(driver) -> None:
    """Populate the ``smart_*`` env vars consumed by ``_resolve_smart`` from the
    LIVE session, so ``{{smart.browser_name|browser_version|os_type|os_version}}``
    resolve to real values instead of an empty string.

    Mirrors the V2 source ``add_smart_var``: the browser fields come from the live
    ``driver.capabilities`` (the negotiated values — e.g. the concrete
    ``"121.0.x"`` rather than a requested ``"latest"``), and the OS fields come
    from the runtime host via the ``platform`` module. Called once, right after
    the driver is created (so ``driver.capabilities`` is populated) and before
    any step runs.
    """
    caps = getattr(driver, "capabilities", None) or {}
    os.environ["smart_browser_name"] = str(caps.get("browserName", "") or "")
    os.environ["smart_browser_version"] = str(caps.get("browserVersion", "") or "")
    os.environ["smart_os"] = platform.system()
    os.environ["smart_os_version"] = platform.version()


def _report_lambda_status(driver, status: str, remark: str) -> None:
    """Mark the LT cloud session as passed/failed.

    No-op for the local run target — there's no cloud session to update.
    Failures here are swallowed: the test outcome already happened, and a
    reporting hiccup must not mask the real result by raising over it.

    The LambdaTest Selenium hub intercepts the WebDriver executeScript command
    by matching the SCRIPT BODY against ``lambda-status=`` — it never reads
    args[0]. Passing the marker as an argument (``execute_script("return
    arguments[0];", "lambdatest_action: ...")``) means the hub never sees it
    and the test shows "completed" instead of passed/failed. The
    ``lambdatest_action: {...JSON...}`` body form also fails: Chrome 148 parses
    it as a labeled statement + block and SyntaxErrors on the inner ``:``.
    The V2/V4-proven body form ``driver.execute_script(f"lambda-status={status}")``
    is the only reliable contract. The remark is no longer sent in the call;
    it is logged for local diagnostics instead.
    """
    if _config.run_target != "cloud":
        return
    try:
        if remark:
            logger.info("[testmu] LT test status=%s remark=%s", status, remark[:255])
        driver.execute_script(f"lambda-status={status}")
    except Exception as e:  # noqa: BLE001 — never propagate reporter errors
        logger.warning("[testmu] failed to report LT test status: %s", e)


def _settle_before_teardown(driver) -> None:
    """Best-effort settle window before ``driver.quit()`` so the grid's video
    encoder can flush the final action's frames.

    On the LambdaTest grid (capability ``video:true``), ``driver.quit()``
    firing immediately after the verdict is reported gives the grid-side
    encoder no time to flush — the session VIDEO recording blacks out before
    the last action is visible (regression repro: last steps missing from
    the recording despite the test itself passing). No-op for the local run
    target or when video recording is disabled — there's no grid-side
    encoder to protect in either case.

    Called from ``run()``'s ``finally`` block, so this must never raise or
    replace the test verdict/exception already in flight; every step here is
    best-effort and swallows its own errors.

    Args:
        driver: Selenium WebDriver instance about to be torn down.
    """
    if _config.run_target != "cloud" or not _bool_he("VIDEO", True):
        return

    idle_timeout_ms = int(os.getenv("TESTMU_TEARDOWN_IDLE_TIMEOUT_MS", "5000"))
    try:
        WebDriverWait(driver, idle_timeout_ms / 1000.0).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception as e:  # noqa: BLE001 — session may already be gone; teardown must proceed
        logger.warning("[testmu] settle wait-for-idle failed: %s", e)

    drain_ms = int(os.getenv("TESTMU_TEARDOWN_VIDEO_DRAIN_MS", "2000"))
    if drain_ms > 0:
        time.sleep(drain_ms / 1000.0)


def _create_local_driver():
    """Launch a direct local webdriver based on LT_BROWSER + TESTMU_HEADLESS env."""
    browser = os.getenv("LT_BROWSER", "chrome").lower()
    headless = os.getenv("TESTMU_HEADLESS", "true").lower() == "true"

    if browser.startswith("firefox"):
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        logger.info("[testmu] launching local Firefox (headless=%s)", headless)
        return webdriver.Firefox(options=opts)

    # Default: Chrome (covers "chrome", "chromium", anything not firefox).
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    for arg in (
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-notifications",
    ):
        opts.add_argument(arg)
    logger.info("[testmu] launching local Chrome (headless=%s)", headless)
    return webdriver.Chrome(options=opts)


def _build_remote_options(cap: dict):
    """Convert a capability dict into ChromeOptions for webdriver.Remote().

    goog:chromeOptions MUST be applied through ChromeOptions' native API
    (add_argument / add_experimental_option / add_encoded_extension), NOT via
    set_capability. ChromeOptions.to_capabilities() rebuilds goog:chromeOptions
    from the object's own _arguments / experimental_options / _extensions, so a
    goog:chromeOptions set via set_capability is silently discarded — dropping
    args, excludeSwitches, prefs, and extensions on the wire. Every other key
    (LT:Options, goog:loggingPrefs, unhandledPromptBehavior, …) is a plain
    capability and is set via set_capability.
    """
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    options = ChromeOptions()
    for key, value in cap.items():
        if key == "goog:chromeOptions" and isinstance(value, dict):
            for arg in value.get("args", []):
                options.add_argument(arg)
            for ext in value.get("extensions", []):
                options.add_encoded_extension(ext)
            for exp_key, exp_val in value.items():
                if exp_key not in ("args", "extensions"):
                    options.add_experimental_option(exp_key, exp_val)
        else:
            options.set_capability(key, value)
    return options


def run(fn: Callable, profile: str = "default") -> None:
    """Launch the driver, invoke fn(driver), tear down.

    profile arg is reserved for future multi-profile use; Phase A is single-driver.
    Branches on _config.run_target ("cloud" -> LT hub, "local" -> direct driver).
    """
    # Configure logging so testmu messages reach stdout. Without this,
    # Python's default lastResort handler only surfaces WARNING+, so all the
    # `[testmu] launching driver…`, `[testmu] test start/pass/fail`,
    # and step traces disappear from the HE worker log.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Each session starts step numbering from 1 (matches Playwright reporter).
    _reset_step_counter()
    # And starts with a clean pending-failure list — stale entries from a
    # prior test in the same process must not contaminate this run.
    _reset_pending_failures()
    from testmu_selenium._helpers.navigate import _reset_hyperex
    _reset_hyperex()

    # Config dump — matches Playwright binding session parity.
    logger.info(
        "Mode: run_target=%s, lt_auth=%s, smart=%s",
        _config.run_target,
        getattr(_config, "lt_auth", False),
        getattr(_config, "smart", False),
    )

    if _config.run_target == "cloud":
        logger.info("Connecting to LT cloud...")
        cap = _config_dict.get("capability") or build_capability(
            username=_config_dict.get("username", ""),
            access_key=_config_dict.get("accesskey", ""),
            build=_config_dict.get("build"),
            name=_config_dict.get("name"),
            custom_capabilities=_config_dict.get("custom_capabilities") or {},
        )
        lt_opts = cap.get("LT:Options", {})
        logger.info(
            "Capabilities: browser=%s %s, platform=%s, build=%s, name=%s",
            cap.get("browserName", "?"), cap.get("browserVersion", "?"),
            cap.get("platformName", "?"), lt_opts.get("build", "?"),
            lt_opts.get("name", "?"),
        )

        hub_url = _config_dict.get("lt_hub_url")
        logger.info("[testmu] launching driver against hub=%s", hub_url)

        # Selenium 4 uses an options object. goog:chromeOptions must go through
        # ChromeOptions' native API (see _build_remote_options) — set_capability
        # alone drops args/excludeSwitches/prefs/extensions.
        options = _build_remote_options(cap)

        driver = webdriver.Remote(command_executor=hub_url, options=options)
    else:
        driver = _create_local_driver()

    _set_driver(profile, driver)

    # Expose the live session's browser/OS as smart.* env vars so
    # {{smart.browser_name|browser_version|os_type|os_version}} resolve (V2 parity).
    _export_smart_env_from_session(driver)

    try:
        fn(driver)
        # fn returned cleanly. If any step was wrapped in
        # `Fail but continue executing` and the wrapped op failed, the
        # exception was swallowed and recorded — surface it now so HE / CI
        # sees a non-zero exit and the LT dashboard reads FAILED instead of
        # silently passing (regression repro).
        if _has_pending_failures():
            summary = _pending_failures_summary()
            msg = f"Test had non-fatal failures (Fail but continue): {summary}"
            _report_lambda_status(driver, "failed", msg)
            raise RuntimeError(msg)
        _report_lambda_status(driver, "passed", "passed")
    except Exception as e:
        # Original fn exception (or our pending-failure RuntimeError) — same
        # path either way. If the test body raised AND pending failures were
        # also recorded, the body's exception still wins precedence (its
        # class/message is more specific than the aggregate summary).
        _report_lambda_status(driver, "failed", str(e))
        raise
    finally:
        _settle_before_teardown(driver)
        try:
            driver.quit()
        except Exception as e:
            logger.warning("[testmu] driver.quit() failed: %s", e)
        _clear_drivers()
