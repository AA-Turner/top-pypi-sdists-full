"""clear_at_coordinate helper — V2-parity coordinate-based clear.

Driver-level helper, not _run_action-wrapped — no element to heal.
Gesture: move to (x, y), click, Ctrl+A (select all), delete.

Thin wrapper over the proven _clear_coord_runner gesture, so the implementation
lives in one place. Used by V3 codegen for the desktop-resolver coordinate-fallback
path when xpath resolution fails.

Ported from the V2 Selenium canvas-branch clear implementation.
"""
from testmu_selenium._action_clear import _clear_coord_runner


def clear_at_coordinate(driver, x, y):
    """Coordinate-based clear: move to (x, y), click, select-all, delete.

    Args:
        driver: Selenium WebDriver.
        x, y: Absolute viewport coordinates where to clear.

    Returns:
        True on success (per _clear_coord_runner contract).
    """
    return _clear_coord_runner(driver, x, y, {})
