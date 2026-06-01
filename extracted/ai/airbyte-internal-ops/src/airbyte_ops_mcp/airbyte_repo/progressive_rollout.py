# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Progressive rollout utilities for Airbyte connectors.

Progressive rollout setup and cleanup are now handled automatically by
`bump_connector_version` in `bump_version.py`:

- RC bump types (`patch_rc`, `minor_rc`, `major_rc`, `rc`) set
  `enableProgressiveRollout: true`.
- `promote` sets `enableProgressiveRollout` to false.

This module retains the `extract_ga_version` helper used during the
promote flow.
"""

from __future__ import annotations


def extract_ga_version(rc_version: str) -> str:
    """Extract the GA version from a version string.

    Strips known pre-release suffixes:
    - RC versions (e.g., `1.0.0-rc.1`) → `1.0.0`
    - Preview versions (e.g., `1.0.0-preview.1`) → `1.0.0`

    GA versions without a pre-release suffix are returned as-is.

    Args:
        rc_version: Version string (e.g., "1.0.0-rc.1", "1.0.0-preview.1",
            or "1.0.0")

    Returns:
        GA version string (e.g., "1.0.0")
    """
    if "-rc." in rc_version:
        return rc_version.split("-rc.")[0]
    if "-preview." in rc_version:
        return rc_version.split("-preview.")[0]
    return rc_version
