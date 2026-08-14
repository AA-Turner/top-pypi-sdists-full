# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Helpers for matching connector versions to breaking-change declarations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from packaging.version import InvalidVersion, Version


def version_declares_breaking_change(
    version: str,
    breaking_changes: Mapping[Any, Any] | None,
) -> bool:
    """Return whether `version` matches a declared breaking-change version.

    Prerelease and build suffixes are removed before comparing versions, so
    `2.0.0-rc.1` matches a `2.0.0` breaking-change entry.
    """
    if not isinstance(breaking_changes, Mapping):
        return False

    try:
        base_version = Version(version).base_version
    except InvalidVersion:
        return False

    for declared_version in breaking_changes:
        try:
            if Version(str(declared_version)).base_version == base_version:
                return True
        except InvalidVersion:
            continue
    return False
