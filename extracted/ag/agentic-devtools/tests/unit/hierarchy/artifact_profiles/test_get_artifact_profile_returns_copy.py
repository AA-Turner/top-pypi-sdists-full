"""Tests that get_artifact_profile returns independent copies of ArtifactProfile."""

from __future__ import annotations

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
from agentic_devtools.hierarchy.models import HierarchyLevel


class TestGetArtifactProfileReturnsCopy:
    """Ensure mutations to returned profiles do not affect the global _PROFILES dict."""

    def test_mutating_included_artifacts_does_not_affect_subsequent_calls(self) -> None:
        profile1 = get_artifact_profile(HierarchyLevel.EPIC)
        original_len = len(profile1.included_artifacts)
        profile1.included_artifacts.append("mutated.md")

        profile2 = get_artifact_profile(HierarchyLevel.EPIC)
        assert len(profile2.included_artifacts) == original_len
        assert "mutated.md" not in profile2.included_artifacts

    def test_mutating_excluded_artifacts_does_not_affect_subsequent_calls(self) -> None:
        profile1 = get_artifact_profile(HierarchyLevel.EPIC)
        assert "tasks.md" in profile1.excluded_artifacts  # confirm initial state
        profile1.excluded_artifacts.clear()

        profile2 = get_artifact_profile(HierarchyLevel.EPIC)
        assert "tasks.md" in profile2.excluded_artifacts

    def test_mutating_inherited_context_does_not_affect_subsequent_calls(self) -> None:
        profile1 = get_artifact_profile(HierarchyLevel.TASK)
        profile1.inherited_context.clear()

        profile2 = get_artifact_profile(HierarchyLevel.TASK)
        assert profile2.inherited_context == ["spec.md", "plan.md"]

    def test_successive_calls_return_distinct_objects(self) -> None:
        profile1 = get_artifact_profile(HierarchyLevel.FEATURE)
        profile2 = get_artifact_profile(HierarchyLevel.FEATURE)
        assert profile1 is not profile2
        assert profile1.included_artifacts is not profile2.included_artifacts
