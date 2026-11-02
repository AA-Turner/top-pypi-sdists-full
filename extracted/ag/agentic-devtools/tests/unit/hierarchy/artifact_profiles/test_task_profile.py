"""Tests for Task artifact profile (inherits parent context + scoped tasks)."""

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
from agentic_devtools.hierarchy.models import HierarchyLevel


class TestTaskProfile:
    """Tests that Task profile inherits parent spec/plan and gets scoped tasks."""

    def test_task_includes_tasks_md(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.TASK)
        assert "tasks.md" in profile.included_artifacts

    def test_task_inherits_spec_and_plan(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.TASK)
        assert "spec.md" in profile.inherited_context
        assert "plan.md" in profile.inherited_context

    def test_task_excludes_spec_plan_from_generation(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.TASK)
        assert "spec.md" in profile.excluded_artifacts
        assert "plan.md" in profile.excluded_artifacts
        assert "generated/analysis-report.md" in profile.excluded_artifacts
        assert "analysis-report.md" not in profile.excluded_artifacts

    def test_task_level_matches(self) -> None:
        profile = get_artifact_profile(HierarchyLevel.TASK)
        assert profile.level == HierarchyLevel.TASK
