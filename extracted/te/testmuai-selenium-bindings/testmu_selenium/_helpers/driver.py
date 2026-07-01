"""Driver registry — single-driver per session for V3 Phase A.

run() populates _drivers["default"] before invoking the test function.
get_driver(profile_id) returns it. Multi-profile support is dropped per spec
(V4 parity: single driver per test).
"""
from selenium import webdriver
from typing import Optional

# Module-level registry — populated by testmu_selenium._session.run() at session start
_drivers: dict[str, "webdriver.Remote"] = {}


def get_driver(profile_id: str = "default") -> "webdriver.Remote":
    """Return the active driver for this profile_id. Raises if no run() session active."""
    if profile_id not in _drivers:
        raise RuntimeError(
            f"no driver registered for profile_id={profile_id!r}; "
            "did you call testmu_selenium.run() to start a session?"
        )
    return _drivers[profile_id]


def _set_driver(profile_id: str, driver: "webdriver.Remote") -> None:
    """Internal — used by _session.run()."""
    _drivers[profile_id] = driver


def _clear_drivers() -> None:
    """Internal — clear registry on session teardown."""
    _drivers.clear()
