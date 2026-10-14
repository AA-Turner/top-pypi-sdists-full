"""DRIVER-mode smartui_screenshot verb — SDK-backed visual-regression capture.

One ``SmartUIAppSnapshot`` per binding session: the first capture resolves the
project token and calls ``start()`` (token via options, buildName carried when
configured), later captures upload into the same build, ``finalize_smartui()``
stops it. The verb returns a status dict — ``captured`` / ``skipped`` (no
token) / ``failed`` (SDK error) — and raises only for a missing SDK package.
"""
import logging
import os

from testmu_appium import _config

_log = logging.getLogger("testmu_appium")

#: The started SDK snapshot session, or None. One per binding session; reset by
#: finalize_smartui().
_active = None


def _resolve_token():
    """Project token: an explicit configure() value wins, else PROJECT_TOKEN env."""
    token = _config.get("smartui_project_token")
    if token:
        return str(token)
    env_token = os.getenv("PROJECT_TOKEN")
    if env_token and env_token.strip():
        return env_token.strip()
    return None


def _redact(text: str, token) -> str:
    """Strip the project token and LT credentials from a surfaced string."""
    secrets = [token, os.getenv("LT_USERNAME"), os.getenv("LT_ACCESS_KEY")]
    for secret in secrets:
        if secret:
            text = text.replace(secret, "***")
    return text


def _ensure_started(token):
    """Return the started SDK session, creating and start()-ing it on first use."""
    global _active
    if _active is not None:
        return _active
    from lambdatest_selenium_driver.smartui_app_snapshot import SmartUIAppSnapshot

    options = {"projectToken": token}
    build_name = _config.get("smartui_build_name")
    if build_name:
        options["buildName"] = str(build_name)
    session = SmartUIAppSnapshot()
    session.start(options)
    _active = session
    return _active


def smartui_screenshot(driver, name: str, *, description: str = "") -> dict:
    """Capture a SmartUI visual-regression screenshot into the session build.

    Args:
        driver: Live Appium webdriver session the SDK screenshots through.
        name: Snapshot name SmartUI indexes the capture under.
        description: Optional human-readable label for the INFO log line.

    Returns:
        ``{"status": "captured", "name": ...}`` on upload,
        ``{"status": "skipped", "reason": ...}`` when no project token is
        resolvable, ``{"status": "failed", "reason": ...}`` when the SDK
        errors. Reasons are redacted of the token and LT credentials.

    Raises:
        ImportError: the ``lambdatest-selenium-driver`` package is missing.
    """
    suffix = f" — {description}" if description else ""
    _log.info("smartui_screenshot: name=%s%s", name, suffix)

    token = _resolve_token()
    if not token:
        reason = (
            "no SmartUI project token resolvable (configure "
            "smartui_project_token or set PROJECT_TOKEN)"
        )
        _log.warning("smartui_screenshot skipped: name=%s — %s", name, reason)
        return {"status": "skipped", "reason": reason}

    # Import outside the try: a missing SDK is an environment problem and must
    # surface as ImportError, not a "failed" status.
    from lambdatest_selenium_driver.smartui_app_snapshot import SmartUIAppSnapshot  # noqa: F401

    try:
        session = _ensure_started(token)
        session.smartui_app_snapshot(driver, name, {})
    except Exception as e:  # noqa: BLE001 — replay must not fail over SmartUI
        reason = _redact(str(e), token)
        _log.warning("smartui_screenshot failed: name=%s — %s", name, reason)
        return {"status": "failed", "reason": reason}
    return {"status": "captured", "name": name}


def smartui_build_name():
    """Name of the active SmartUI build, or None before the first capture."""
    if _active is None:
        return None
    build = getattr(_active, "build_data", None)
    return getattr(build, "name", None)


def finalize_smartui() -> None:
    """Stop the active SmartUI build, if any. Idempotent; never raises."""
    global _active
    if _active is None:
        return
    session, _active = _active, None
    try:
        session.stop()
    except Exception as e:  # noqa: BLE001 — teardown must not replace the verdict
        _log.warning("smartui finalize failed: %s", _redact(str(e), _resolve_token()))
