"""Tests for ArtifactProfile dataclass."""

from agentic_devtools.hierarchy.models import ArtifactProfile, HierarchyLevel


class TestArtifactProfile:
    """Tests for ArtifactProfile construction."""

    def test_default_construction(self) -> None:
        profile = ArtifactProfile(level=HierarchyLevel.FEATURE)
        assert profile.level == HierarchyLevel.FEATURE
        assert profile.included_artifacts == []
        assert profile.excluded_artifacts == []
        assert profile.inherited_context == []

    def test_full_construction(self) -> None:
        profile = ArtifactProfile(
            level=HierarchyLevel.TASK,
            included_artifacts=["tasks.md"],
            excluded_artifacts=["spec.md"],
            inherited_context=["spec.md", "plan.md"],
        )
        assert profile.level == HierarchyLevel.TASK
        assert "tasks.md" in profile.included_artifacts
        assert "spec.md" in profile.excluded_artifacts
        assert "spec.md" in profile.inherited_context
        assert "plan.md" in profile.inherited_context
