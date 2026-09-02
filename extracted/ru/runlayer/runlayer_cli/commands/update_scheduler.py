"""Privilege check shared by package-owned update schedulers."""

import os
import sys

from runlayer_cli.scan import windows_users


def is_privileged_system_scheduler() -> bool:
    """Whether this process has the package scheduler's system identity."""
    if sys.platform == "win32":
        return windows_users.is_running_as_system()
    getuid = getattr(os, "geteuid", None)
    return callable(getuid) and getuid() == 0
