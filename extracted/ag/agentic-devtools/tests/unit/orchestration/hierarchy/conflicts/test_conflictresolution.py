"""Unit tests for FR-018 conflict detection and resolution."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.conflicts import ConflictResolution


def test_conflict_resolution_rejects_missing_contested_path_grant() -> None:
    with pytest.raises(ValueError, match="exactly one agent"):
        ConflictResolution(
            resolution_authority="feature-1",
            contested_paths=("x.py", "y.py"),
            granted_paths={"a": ("x.py",)},
            resolution_decision="bad",
        )


def test_conflict_resolution_rejects_duplicate_grant() -> None:
    with pytest.raises(ValueError, match="more than one agent"):
        ConflictResolution(
            resolution_authority="feature-1",
            contested_paths=("x.py",),
            granted_paths={"a": ("x.py",), "b": ("x.py",)},
            resolution_decision="bad",
        )
