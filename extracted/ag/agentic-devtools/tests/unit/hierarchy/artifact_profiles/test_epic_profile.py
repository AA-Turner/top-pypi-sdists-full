"""Tests for Epic artifact profile (excludes tasks.md)."""

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
from agentic_devtools.hierarchy.models import HierarchyLevel


class TestEpicProfile:
    """Tests that Epic profile excludes tasks.md."""

    def test_epic_excludes_tasks(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.EPIC)
        assert "tasks.md" in profile.excluded_artifacts
        assert "tasks.md" not in profile.included_artifacts

    def test_epic_includes_spec_and_plan(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.EPIC)
        assert "spec.md" in profile.included_artifacts
        assert "plan.md" in profile.included_artifacts
        assert "generated/analysis-report.md" in profile.included_artifacts
        assert "analysis-report.md" not in profile.included_artifacts

    def test_epic_no_inherited_context(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.EPIC)
        assert profile.inherited_context == []

    def test_epic_level_matches(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.EPIC)
        assert profile.level == HierarchyLevel.EPIC
