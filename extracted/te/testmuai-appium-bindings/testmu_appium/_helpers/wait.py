"""DRIVER-mode wait verb — a fixed sleep.

No selector, no find, no heal: this is a plain timed pause the generated test
asks for explicitly, distinct from the smart/vision wait-until-condition path.
"""
import logging
import time

_log = logging.getLogger("testmu_appium")


def wait(driver, seconds: float | None = None, *, ms: int | None = None,
          description: str = "") -> None:
    """Sleep for a fixed duration.

    ``driver`` is accepted (and unused) so every DRIVER-mode verb shares the
    same ``(driver, ...)`` call shape the generator emits.

    Args:
        driver: Live Appium webdriver session (unused).
        seconds: Duration in seconds.
        ms: Duration in milliseconds; wins over `seconds` when both are given.
        description: Optional human-readable label for the INFO log line.

    Raises:
        ValueError: neither `seconds` nor `ms` was given, or the resolved
            duration is negative.
    """
    if ms is not None:
        duration = ms / 1000
    elif seconds is not None:
        duration = seconds
    else:
        raise ValueError("wait() needs seconds or ms")

    if duration < 0:
        raise ValueError(f"wait() duration must not be negative, got {duration}")

    time.sleep(duration)
    suffix = f" — {description}" if description else ""
    _log.info("wait: %.3fs%s", duration, suffix)
