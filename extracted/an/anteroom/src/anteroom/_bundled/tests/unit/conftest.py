"""Shared fixtures and marker handling for unit tests."""

from __future__ import annotations

import sys

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Auto-skip tests based on platform markers."""
    is_windows = sys.platform == "win32"

    skip_unix = pytest.mark.skip(reason="unix_only: skipped on Windows")
    skip_win = pytest.mark.skip(reason="windows_only: skipped on non-Windows")

    for item in items:
        if "unix_only" in item.keywords and is_windows:
            item.add_marker(skip_unix)
        if "windows_only" in item.keywords and not is_windows:
            item.add_marker(skip_win)


@pytest.fixture
def is_windows() -> bool:
    """Return True when running on Windows."""
    return sys.platform == "win32"
