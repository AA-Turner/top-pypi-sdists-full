"""DRIVER-mode app_lifecycle verb — terminate / background the app under test.

No selector, no find, no heal: these act on the app process, not a UI element.
"""
import logging
import math
from typing import Optional

from testmu_appium import _config

_log = logging.getLogger("testmu_appium")

_KNOWN_KINDS = frozenset({"terminate", "background"})


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
    """Terminate or background the app under test.

    Args:
        driver: Live Appium webdriver session.
        kind: "terminate" or "background".
        app_id: Target app id for "terminate"; defaults to the configured app_id.
        duration_ms: For "background", how long to background the app; omit for
            an indefinite background.
        description: Optional human-readable label for the INFO log line.

    Raises:
        ValueError: `kind` is not one of the known kinds, or "terminate" has no
            app id to act on.
    """
    if kind not in _KNOWN_KINDS:
        raise ValueError(
            f"unknown app_lifecycle kind {kind!r}; expected one of {sorted(_KNOWN_KINDS)}"
        )

    suffix = f" — {description}" if description else ""

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
