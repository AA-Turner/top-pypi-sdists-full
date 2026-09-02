"""Integration tests for level-aware artifact depth enforcement (US-4).

Verifies that artifact profiles match hierarchy levels correctly:
epic excludes tasks.md, task includes only tasks.md with inherited context,
feature and standalone include all artifacts.
"""

from __future__ import annotations

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
from agentic_devtools.hierarchy.models import HierarchyLevel


class TestEpicProfileFromDetectedLevel:
    """T022: Epic profile includes spec.md, plan.md, research.md, generated analysis; excludes tasks.md."""

    def test_epic_profile_artifacts(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.EPIC)

        assert "spec.md" in profile.included_artifacts
        assert "plan.md" in profile.included_artifacts
        assert "research.md" in profile.included_artifacts
        assert "generated/analysis-report.md" in profile.included_artifacts
        assert "analysis-report.md" not in profile.included_artifacts
        assert "tasks.md" not in profile.included_artifacts
        assert "tasks.md" in profile.excluded_artifacts


class TestTaskProfileFromDetectedLevel:
    """T023: Task profile includes only tasks.md; inherited context has spec.md, plan.md."""

    def test_task_profile_artifacts(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.TASK)

        assert profile.included_artifacts == ["tasks.md"]
        assert "spec.md" in profile.inherited_context
        assert "plan.md" in profile.inherited_context


class TestFeatureAndStandaloneProfiles:
    """T024: Feature and standalone profiles include all artifacts."""

    def test_feature_includes_all(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.FEATURE)
        expected = {"spec.md", "plan.md", "tasks.md", "research.md", "generated/analysis-report.md"}
        assert set(profile.included_artifacts) == expected
        assert profile.excluded_artifacts == []

    def test_standalone_includes_all(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.STANDALONE)
        expected = {"spec.md", "plan.md", "tasks.md", "research.md", "generated/analysis-report.md"}
        assert set(profile.included_artifacts) == expected
        assert profile.excluded_artifacts == []
        assert profile.inherited_context == []
