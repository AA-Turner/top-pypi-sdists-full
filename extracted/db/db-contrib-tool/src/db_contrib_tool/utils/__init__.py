"""Helper functions."""

import sys


def is_windows() -> bool:
    """
    Check whether we are on Windows.

    :return: Return True if Windows
    """
    return sys.platform.startswith("win32") or sys.platform.startswith("cygwin")
