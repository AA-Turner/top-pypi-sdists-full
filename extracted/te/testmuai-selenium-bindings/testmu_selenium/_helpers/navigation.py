"""Driver-level navigation helpers — refresh, back, forward.

Maps to V3 codegen handlers:
- refresh handler — driver.refresh()
- go_back handler  — driver.back()
- go_forward handler — driver.forward()

Trivial wraps; existence here is for symmetry with the rest of the public API
and to give the codegen a single namespace (testmu_selenium.*) to emit into.
"""
from __future__ import annotations


def refresh(driver) -> None:
    """Refresh the current page (driver.refresh)."""
    driver.refresh()


def go_back(driver) -> None:
    """Navigate browser back (driver.back)."""
    driver.back()


def go_forward(driver) -> None:
    """Navigate browser forward (driver.forward)."""
    driver.forward()


__all__ = ["refresh", "go_back", "go_forward"]
