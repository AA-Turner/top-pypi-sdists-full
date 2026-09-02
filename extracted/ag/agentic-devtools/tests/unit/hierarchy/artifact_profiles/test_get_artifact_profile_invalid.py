"""Tests for get_artifact_profile with invalid input."""

from __future__ import annotations

import pytest

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile


class TestGetArtifactProfileInvalid:
    """Cover ValueError branch for invalid level."""

    def test_raises_for_non_hierarchy_level(self):
        with pytest.raises(ValueError, match="Expected HierarchyLevel"):
            get_artifact_profile("not-a-level")  # type: ignore[arg-type]

    def test_raises_for_none(self):
        with pytest.raises(ValueError, match="Expected HierarchyLevel"):
            get_artifact_profile(None)  # type: ignore[arg-type]
