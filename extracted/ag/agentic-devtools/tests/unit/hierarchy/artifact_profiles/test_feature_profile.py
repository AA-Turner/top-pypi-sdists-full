"""Tests for Feature artifact profile (full suite)."""

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
from agentic_devtools.hierarchy.models import HierarchyLevel


class TestFeatureProfile:
    """Tests that Feature profile includes full artifact suite."""

    def test_feature_includes_all_artifacts(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.FEATURE)
        expected = {"spec.md", "plan.md", "tasks.md", "research.md", "generated/analysis-report.md"}
        assert set(profile.included_artifacts) == expected

    def test_feature_excludes_nothing(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.FEATURE)
        assert profile.excluded_artifacts == []

    def test_feature_no_inherited_context(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.FEATURE)
        assert profile.inherited_context == []

    def test_feature_level_matches(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.FEATURE)
        assert profile.level == HierarchyLevel.FEATURE
