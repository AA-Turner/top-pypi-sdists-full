"""Driver-level URL/title accessors — no element find, no heal.

Thin readers exposed at the public surface so codegen can emit bare names.
"""
from __future__ import annotations


def get_url(driver) -> str:
    """Return the driver's current URL."""
    return driver.current_url


def get_title(driver) -> str:
    """Return the driver's current page title."""
    return driver.title
