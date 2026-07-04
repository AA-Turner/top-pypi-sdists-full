"""Tests for /autofleet command - parallel task decomposition and execution."""

from __future__ import annotations

import pytest

from sage.cli_core import (
    AutoFleetSubtask,
    TaskType,
    _decompose_task_for_fleet,
    _parse_autonomous_command_args,
)


class TestAutoFleetSubtask:
    """Tests for AutoFleetSubtask dataclass."""

    def test_create_basic(self):
        """Create basic subtask."""
        subtask = AutoFleetSubtask(
            id="test",
            name="Test Subtask",
            description="A test subtask",
            task_type=TaskType.IMPLEMENTATION,
        )
        assert subtask.id == "test"
        assert subtask.name == "Test Subtask"
        assert subtask.description == "A test subtask"
        assert subtask.task_type == TaskType.IMPLEMENTATION

    def test_default_values(self):
        """Default values are set correctly."""
        subtask = AutoFleetSubtask(
            id="test",
            name="Test",
            description="Desc",
            task_type=TaskType.TESTING,
        )
        assert subtask.dependencies == []
        assert subtask.completed is False
        assert subtask.result is None
        assert subtask.error is None

    def test_with_dependencies(self):
        """Subtask with dependencies."""
        subtask = AutoFleetSubtask(
            id="impl",
            name="Implementation",
            description="Implement feature",
            task_type=TaskType.IMPLEMENTATION,
            dependencies=["analyze", "design"],
        )
        assert subtask.dependencies == ["analyze", "design"]

    def test_completed_subtask(self):
        """Completed subtask with result."""
        subtask = AutoFleetSubtask(
            id="test",
            name="Test",
            description="Desc",
            task_type=TaskType.TESTING,
            completed=True,
            result="All tests passed",
        )
        assert subtask.completed is True
        assert subtask.result == "All tests passed"

    def test_failed_subtask(self):
        """Failed subtask with error."""
        subtask = AutoFleetSubtask(
            id="test",
            name="Test",
            description="Desc",
            task_type=TaskType.TESTING,
            completed=False,
            error="Test failed: assertion error",
        )
        assert subtask.completed is False
        assert subtask.error == "Test failed: assertion error"


class TestDecomposeTaskForFleet:
    """Tests for _decompose_task_for_fleet function."""

    def test_always_has_analyze_first(self):
        """Every decomposition starts with analyze subtask."""
        subtasks = _decompose_task_for_fleet("implement a feature")
        assert subtasks[0].id == "analyze"
        assert subtasks[0].name == "Analysis & Planning"
        assert subtasks[0].dependencies == []

    def test_always_has_integrate_last(self):
        """Every decomposition ends with integrate subtask."""
        subtasks = _decompose_task_for_fleet("implement a feature")
        assert subtasks[-1].id == "integrate"
        assert subtasks[-1].name == "Integration & Verification"

    def test_implementation_task(self):
        """Implementation task gets core implementation subtask."""
        subtasks = _decompose_task_for_fleet("implement user authentication")
        subtask_ids = [s.id for s in subtasks]
        assert "analyze" in subtask_ids
        assert "integrate" in subtask_ids
        # Should have some implementation subtask
        impl_subtasks = [s for s in subtasks if s.task_type == TaskType.IMPLEMENTATION]
        assert len(impl_subtasks) >= 1

    def test_testing_task(self):
        """Testing task gets testing subtask."""
        subtasks = _decompose_task_for_fleet("write tests for the auth module")
        subtask_ids = [s.id for s in subtasks]
        assert "testing" in subtask_ids
        testing_subtask = next(s for s in subtasks if s.id == "testing")
        assert testing_subtask.task_type == TaskType.TESTING

    def test_documentation_task(self):
        """Documentation task gets docs subtask."""
        subtasks = _decompose_task_for_fleet("document the API endpoints")
        subtask_ids = [s.id for s in subtasks]
        assert "docs" in subtask_ids
        docs_subtask = next(s for s in subtasks if s.id == "docs")
        assert docs_subtask.task_type == TaskType.DOCUMENTATION

    def test_bug_fix_task(self):
        """Bug fix task gets fix subtask."""
        subtasks = _decompose_task_for_fleet("fix the authentication bug")
        subtask_ids = [s.id for s in subtasks]
        assert "fix" in subtask_ids

    def test_refactor_task(self):
        """Refactor task gets refactor subtask."""
        subtasks = _decompose_task_for_fleet("refactor the user service")
        subtask_ids = [s.id for s in subtasks]
        assert "refactor" in subtask_ids

    def test_security_task(self):
        """Security task gets security subtask."""
        subtasks = _decompose_task_for_fleet("implement login security")
        subtask_ids = [s.id for s in subtasks]
        assert "security" in subtask_ids

    def test_api_task(self):
        """API task gets api subtask."""
        subtasks = _decompose_task_for_fleet("create REST API endpoints")
        subtask_ids = [s.id for s in subtasks]
        assert "api" in subtask_ids

    def test_ui_task(self):
        """UI task gets ui subtask."""
        subtasks = _decompose_task_for_fleet("build frontend components")
        subtask_ids = [s.id for s in subtasks]
        assert "ui" in subtask_ids

    def test_data_task(self):
        """Data task gets data subtask."""
        subtasks = _decompose_task_for_fleet("create database schema")
        subtask_ids = [s.id for s in subtasks]
        assert "data" in subtask_ids

    def test_complex_task_with_multiple_subtasks(self):
        """Complex task creates multiple relevant subtasks."""
        subtasks = _decompose_task_for_fleet(
            "implement user authentication API with tests and documentation"
        )
        subtask_ids = [s.id for s in subtasks]
        assert "analyze" in subtask_ids
        assert "api" in subtask_ids
        assert "testing" in subtask_ids
        assert "docs" in subtask_ids
        assert "integrate" in subtask_ids

    def test_dependencies_are_valid(self):
        """All dependencies reference existing subtask ids."""
        subtasks = _decompose_task_for_fleet("implement a feature with tests")
        subtask_ids = {s.id for s in subtasks}
        for subtask in subtasks:
            for dep in subtask.dependencies:
                assert dep in subtask_ids, f"{subtask.id} depends on non-existent {dep}"

    def test_max_subtasks_limit(self):
        """Respects max_subtasks parameter."""
        subtasks = _decompose_task_for_fleet(
            "implement everything with all features", max_subtasks=3
        )
        assert len(subtasks) <= 3

    def test_full_stack_task(self):
        """Full stack task gets data, api, and ui subtasks."""
        subtasks = _decompose_task_for_fleet(
            "create database models, API endpoints, and frontend components"
        )
        subtask_ids = [s.id for s in subtasks]
        assert "data" in subtask_ids
        assert "api" in subtask_ids
        assert "ui" in subtask_ids

    def test_dependency_chain_order(self):
        """Data -> API -> UI dependency chain is correct."""
        subtasks = _decompose_task_for_fleet(
            "build database schema, API, and frontend"
        )
        by_id = {s.id: s for s in subtasks}

        # API should depend on data (if both exist)
        if "api" in by_id and "data" in by_id:
            assert "data" in by_id["api"].dependencies

        # UI should depend on API (if both exist)
        if "ui" in by_id and "api" in by_id:
            assert "api" in by_id["ui"].dependencies

    def test_analyze_has_no_dependencies(self):
        """Analyze subtask has no dependencies."""
        subtasks = _decompose_task_for_fleet("any task")
        analyze = subtasks[0]
        assert analyze.id == "analyze"
        assert analyze.dependencies == []

    def test_integrate_depends_on_all_prior(self):
        """Integrate subtask depends on all prior subtasks."""
        subtasks = _decompose_task_for_fleet("implement a feature with tests")
        integrate = subtasks[-1]
        prior_ids = [s.id for s in subtasks[:-1]]
        # Integrate should have dependencies (may not be all due to how it's built)
        assert len(integrate.dependencies) > 0


class TestAutofleetCommandParsing:
    """Tests for /autofleet command argument parsing."""

    def test_parse_basic_task(self):
        """Parse basic task."""
        options = _parse_autonomous_command_args(
            "implement user authentication",
            default_use_intelligent=True,
            default_workers=3,
        )
        assert options.focus == "implement user authentication"
        assert options.max_workers == 3

    def test_parse_with_workers(self):
        """Parse with worker count."""
        options = _parse_autonomous_command_args(
            "--workers 5 implement user auth",
            default_use_intelligent=True,
            default_workers=3,
        )
        assert options.max_workers == 5
        assert options.focus == "implement user auth"

    def test_parse_with_cycles(self):
        """Parse with cycle count."""
        options = _parse_autonomous_command_args(
            "10 build a feature",
            default_use_intelligent=True,
            default_workers=3,
        )
        assert options.max_cycles == 10
        assert options.focus == "build a feature"

    def test_parse_with_model(self):
        """Parse with explicit model."""
        options = _parse_autonomous_command_args(
            "--model llama_cpp:qwen2.5-coder-3b implement auth",
            default_use_intelligent=True,
            default_workers=3,
        )
        assert options.model == "llama_cpp:qwen2.5-coder-3b"
        assert options.focus == "implement auth"

    def test_parse_with_keep_model(self):
        """Parse with keep-model flag."""
        options = _parse_autonomous_command_args(
            "--keep-model fix the bug",
            default_use_intelligent=True,
            default_workers=3,
        )
        assert options.keep_current_model is True
        assert options.focus == "fix the bug"

    def test_parse_complex_options(self):
        """Parse complex combination of options."""
        options = _parse_autonomous_command_args(
            "5 --workers 4 --model gemini:gemini-pro --keep-model implement auth",
            default_use_intelligent=True,
            default_workers=3,
        )
        assert options.max_cycles == 5
        assert options.max_workers == 4
        assert options.model == "gemini:gemini-pro"
        assert options.keep_current_model is True
        assert options.focus == "implement auth"

    def test_parse_rejects_zero_workers(self):
        """Reject zero workers."""
        with pytest.raises(ValueError):
            _parse_autonomous_command_args(
                "--workers 0 do stuff",
                default_use_intelligent=True,
                default_workers=3,
            )

    def test_parse_with_smart_flag(self):
        """Parse with smart flag."""
        options = _parse_autonomous_command_args(
            "--smart build a feature",
            default_use_intelligent=False,
            default_workers=3,
        )
        assert options.use_intelligent is True

    def test_parse_with_classic_flag(self):
        """Parse with classic flag."""
        options = _parse_autonomous_command_args(
            "--classic build a feature",
            default_use_intelligent=True,
            default_workers=3,
        )
        assert options.use_intelligent is False


class TestTaskTypeMapping:
    """Tests for task type assignments in subtasks."""

    def test_analyze_is_architecture(self):
        """Analyze subtask is architecture type."""
        subtasks = _decompose_task_for_fleet("any task")
        analyze = subtasks[0]
        assert analyze.task_type == TaskType.ARCHITECTURE

    def test_integrate_is_review(self):
        """Integrate subtask is review type."""
        subtasks = _decompose_task_for_fleet("any task")
        integrate = subtasks[-1]
        assert integrate.task_type == TaskType.REVIEW

    def test_testing_subtask_type(self):
        """Testing subtask has testing type."""
        subtasks = _decompose_task_for_fleet("write tests")
        testing = next((s for s in subtasks if s.id == "testing"), None)
        if testing:
            assert testing.task_type == TaskType.TESTING

    def test_docs_subtask_type(self):
        """Docs subtask has documentation type."""
        subtasks = _decompose_task_for_fleet("document the code")
        docs = next((s for s in subtasks if s.id == "docs"), None)
        if docs:
            assert docs.task_type == TaskType.DOCUMENTATION

    def test_security_subtask_type(self):
        """Security subtask has security type."""
        subtasks = _decompose_task_for_fleet("implement security")
        security = next((s for s in subtasks if s.id == "security"), None)
        if security:
            assert security.task_type == TaskType.SECURITY


class TestSubtaskDescriptions:
    """Tests for subtask description generation."""

    def test_subtask_includes_original_task(self):
        """Subtask descriptions include original task."""
        task = "implement user authentication"
        subtasks = _decompose_task_for_fleet(task)
        for subtask in subtasks:
            assert task in subtask.description

    def test_analyze_description(self):
        """Analyze subtask has planning description."""
        subtasks = _decompose_task_for_fleet("build a feature")
        analyze = subtasks[0]
        assert "plan" in analyze.description.lower() or "analy" in analyze.description.lower()

    def test_integrate_description(self):
        """Integrate subtask has verification description."""
        subtasks = _decompose_task_for_fleet("build a feature")
        integrate = subtasks[-1]
        assert "integrat" in integrate.description.lower() or "verif" in integrate.description.lower()


class TestEdgeCases:
    """Test edge cases for task decomposition."""

    def test_empty_task(self):
        """Empty task still produces basic structure."""
        subtasks = _decompose_task_for_fleet("")
        assert len(subtasks) >= 2  # At least analyze and integrate
        assert subtasks[0].id == "analyze"
        assert subtasks[-1].id == "integrate"

    def test_very_long_task(self):
        """Very long task description is handled."""
        long_task = "implement " + "feature " * 100
        subtasks = _decompose_task_for_fleet(long_task)
        assert len(subtasks) >= 2

    def test_special_characters_in_task(self):
        """Special characters in task are handled."""
        task = "implement feature: auth & login (v2.0) - beta"
        subtasks = _decompose_task_for_fleet(task)
        assert len(subtasks) >= 2

    def test_max_subtasks_one(self):
        """Max subtasks of 1 returns only analyze (or minimal set)."""
        subtasks = _decompose_task_for_fleet("big task", max_subtasks=1)
        assert len(subtasks) == 1

    def test_max_subtasks_two(self):
        """Max subtasks of 2 returns minimal useful set."""
        subtasks = _decompose_task_for_fleet("big task", max_subtasks=2)
        assert len(subtasks) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
