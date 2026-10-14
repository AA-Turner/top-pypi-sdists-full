"""DRIVER-mode app_lifecycle verb — activate / terminate / background an app.

No selector, no find, no heal: these act on the app process, not a UI element.
"""
import logging
import math
import time
from typing import Optional

from testmu_appium import _config
from testmu_appium._v4._helpers.foreground import foreground_app

_log = logging.getLogger("testmu_appium")

_KNOWN_KINDS = frozenset({"activate", "terminate", "background"})

# activate_app returns before the activated app is drawn; the verb waits for it
# to reach the foreground so a read taken right after sees the activated app.
_ACTIVATE_SETTLE_S = 5.0
_ACTIVATE_POLL_S = 0.25


def _settle_activate(driver, target: str) -> None:
    """Wait until ``target`` is the foreground app, up to ``_ACTIVATE_SETTLE_S``.

    Best-effort: a platform with no foreground identity, or a failed read, ends
    the wait at once; a target that never reaches the foreground is logged and
    the verb still returns.
    """
    deadline = time.monotonic() + _ACTIVATE_SETTLE_S
    while True:
        try:
            front = foreground_app(driver)
        except Exception as e:  # noqa: BLE001 — the identity read is best-effort
            _log.debug("app_lifecycle: foreground identity unavailable: %s", e)
            return
        if front == target:
            return
        if time.monotonic() >= deadline:
            _log.warning(
                "app_lifecycle: %s not in the foreground after %.1fs (front: %s)",
                target, _ACTIVATE_SETTLE_S, front or "unknown",
            )
            return
        time.sleep(_ACTIVATE_POLL_S)


def _background_seconds(duration_ms: Optional[int]) -> int:
    """Convert a duration in ms to whole seconds, rounded up, minimum 1.

    A missing duration means "background indefinitely", which Appium's
    background_app spells as -1.
    """
    if duration_ms is None:
        return -1
    return max(math.ceil(duration_ms / 1000), 1)


def app_lifecycle(
    driver,
    kind: str,
    *,
    app_id: str = "",
    duration_ms: Optional[int] = None,
    description: str = "",
) -> None:
    """Activate, terminate, or background an app.

    Args:
        driver: Live Appium webdriver session.
        kind: "activate", "terminate", or "background".
        app_id: Target app id for "activate" / "terminate"; defaults to the
            configured app_id.
        duration_ms: For "background", how long to background the app; omit for
            an indefinite background.
        description: Optional human-readable label for the INFO log line.

    Raises:
        ValueError: `kind` is not one of the known kinds, or "activate" /
            "terminate" has no app id to act on.
    """
    if kind not in _KNOWN_KINDS:
        raise ValueError(
            f"unknown app_lifecycle kind {kind!r}; expected one of {sorted(_KNOWN_KINDS)}"
        )

    suffix = f" — {description}" if description else ""

    if kind == "activate":
        target = app_id or _config.get("app_id") or ""
        if not target:
            raise ValueError(
                "app_lifecycle('activate') needs an app id; none was passed and no "
                "app_id is configured"
            )
        driver.activate_app(target)
        _settle_activate(driver, target)
        _log.info("app_lifecycle: activated %s%s", target, suffix)
        return

    if kind == "terminate":
        target = app_id or _config.get("app_id") or ""
        if not target:
            # terminate_app("") is not a no-op — it is a driver call with an empty
            # bundle, whose behaviour is the server's to decide.
            raise ValueError(
                "app_lifecycle('terminate') needs an app id; none was passed and no "
                "app_id is configured"
            )
        driver.terminate_app(target)
        _log.info("app_lifecycle: terminated %s%s", target, suffix)
        return

    seconds = _background_seconds(duration_ms)
    driver.background_app(seconds)
    _log.info("app_lifecycle: backgrounded for %ds%s", seconds, suffix)
