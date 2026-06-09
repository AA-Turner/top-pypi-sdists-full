# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry marker file conventions."""

from __future__ import annotations

import re
from datetime import date
from typing import Literal

PROGRESSIVE_ROLLOUT_MARKER_FILE = "progressive-rollout.yml"
YANK_MARKER_FILE = "version-yank.yml"

_VERSION_MARKER_RE = re.compile(r"^version=.+$")
_UNYANKED_MARKER_RE = re.compile(r"^version-unyanked-\d{8}\.yml$")
_INACTIVE_ROLLOUT_MARKER_RE = re.compile(
    r"^progressive-rollout-(promoted|aborted)-\d{8}\.yml$"
)


def marker_date(value: date | None = None) -> str:
    """Return a marker date suffix as `yyyymmdd`."""
    return (value or date.today()).strftime("%Y%m%d")


def unyanked_marker_file(value: date | None = None) -> str:
    """Return the inactive yank audit marker filename for a date."""
    return f"version-unyanked-{marker_date(value)}.yml"


def inactive_progressive_rollout_marker_file(
    outcome: Literal["promoted", "aborted"],
    value: date | None = None,
) -> str:
    """Return the inactive rollout audit marker filename for an outcome/date."""
    return f"progressive-rollout-{outcome}-{marker_date(value)}.yml"


def is_registry_state_marker_file(filename: str) -> bool:
    """Return whether a filename is managed registry state, not an artifact."""
    return (
        filename in (YANK_MARKER_FILE, PROGRESSIVE_ROLLOUT_MARKER_FILE)
        or _VERSION_MARKER_RE.match(filename) is not None
        or _UNYANKED_MARKER_RE.match(filename) is not None
        or _INACTIVE_ROLLOUT_MARKER_RE.match(filename) is not None
    )
