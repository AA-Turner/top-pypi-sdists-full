"""Chrome only moves forward on a person's profile (owner ruling 16).

Chrome writes its own version into ``<user-data-dir>/Last Version`` on every
launch. A build whose Chrome is OLDER than that version opens a profile written
by a newer Chrome: Chrome warns, and data written in the newer format (cookies,
logins, extension state) can be unreadable or lost. The release carry-over check
refuses such a build; the worker flags it loudly if one ever launches.
"""

from __future__ import annotations

import os
import re

_DIGITS = re.compile(r"\d+(?:\.\d+)*")


def parse_version(text: str | None) -> tuple[int, ...] | None:
    """``"131.0.6778.85"`` (or ``"HeadlessChrome/131.0.6778.85"``) -> a tuple; None when absent."""
    if not text:
        return None
    match = _DIGITS.search(text)
    return tuple(int(p) for p in match.group(0).split(".")) if match else None


def read_profile_last_version(user_data_dir: str | None) -> str | None:
    """The Chrome version that last opened this profile, or None (first run)."""
    if not user_data_dir:
        return None
    try:
        with open(os.path.join(user_data_dir, "Last Version"), encoding="utf-8") as f:
            return f.read().strip() or None
    except OSError:
        return None


def is_downgrade(profile_version: str | None, binary_version: str | None) -> bool:
    """True only when both are known and the binary is older than the profile."""
    profile, binary = parse_version(profile_version), parse_version(binary_version)
    if profile is None or binary is None:
        return False
    return binary < profile
