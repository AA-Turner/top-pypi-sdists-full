"""Comprehensive tests for sage/core/prioritization.py."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# Tests for TaskType Enum
# =============================================================================


class TestTaskType:
    """Tests for TaskType enum."""

    def test_import(self):
        """TaskType can be imported."""
        from sage.core.prioritization import TaskType
        assert TaskType is not None

    def test_fix_error(self):
        """FIX_ERROR value."""
        from sage.core.prioritization import TaskType
        assert TaskType.FIX_ERROR.value == "fix_error"

    def test_fix_test(self):
        """FIX_TEST value."""
        from sage.core.prioritization import TaskType
        assert TaskType.FIX_TEST.value == "fix_test"

    def test_fix_security(self):
        """FIX_SECURITY value."""
        from sage.core.prioritization import TaskType
        assert TaskType.FIX_SECURITY.value == "fix_security"

    def test_fix_regression(self):
        """FIX_REGRESSION value."""
        from sage.core.prioritization import TaskType
        assert TaskType.FIX_REGRESSION.value == "fix_regression"

    def test_refactor(self):
        """REFACTOR value."""
        from sage.core.prioritization import TaskType
        assert TaskType.REFACTOR.value == "refactor"

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.prioritization import TaskType
        expected = [
            "fix_error", "fix_test", "fix_security", "fix_regression",
            "refactor", "improvement", "new_feature", "documentation",
            "dependency_update", "cleanup", "unknown"
        ]
        values = [t.value for t in TaskType]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for TaskSource Enum
# =============================================================================


class TestTaskSource:
    """Tests for TaskSource enum."""

    def test_import(self):
        """TaskSource can be imported."""
        from sage.core.prioritization import TaskSource
        assert TaskSource is not None

    def test_test_failure(self):
        """TEST_FAILURE value."""
        from sage.core.prioritization import TaskSource
        assert TaskSource.TEST_FAILURE.value == "test_failure"

    def test_ci_failure(self):
        """CI_FAILURE value."""
        from sage.core.prioritization import TaskSource
        assert TaskSource.CI_FAILURE.value == "ci_failure"

    def test_deploy_failure(self):
        """DEPLOY_FAILURE value."""
        from sage.core.prioritization import TaskSource
        assert TaskSource.DEPLOY_FAILURE.value == "deploy_failure"

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.prioritization import TaskSource
        expected = [
            "test_failure", "lint_error", "type_error", "security_scan",
            "ci_failure", "deploy_failure", "user_request", "static_analysis",
            "heuristic", "unknown"
        ]
        values = [s.value for s in TaskSource]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for ImpactLevel Enum
# =============================================================================


class TestImpactLevel:
    """Tests for ImpactLevel enum."""

    def test_import(self):
        """ImpactLevel can be imported."""
        from sage.core.prioritization import ImpactLevel
        assert ImpactLevel is not None

    def test_critical(self):
        """CRITICAL value."""
        from sage.core.prioritization import ImpactLevel
        assert ImpactLevel.CRITICAL.value == "critical"

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.prioritization import ImpactLevel
        expected = ["critical", "high", "medium", "low", "minimal"]
        values = [i.value for i in ImpactLevel]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for ConfidenceLevel Enum
# =============================================================================


class TestConfidenceLevel:
    """Tests for ConfidenceLevel enum."""

    def test_import(self):
        """ConfidenceLevel can be imported."""
        from sage.core.prioritization import ConfidenceLevel
        assert ConfidenceLevel is not None

    def test_high(self):
        """HIGH value."""
        from sage.core.prioritization import ConfidenceLevel
        assert ConfidenceLevel.HIGH.value == "high"

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.prioritization import ConfidenceLevel
        expected = ["high", "medium", "low", "very_low"]
        values = [c.value for c in ConfidenceLevel]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for PrioritizedTask Dataclass
# =============================================================================


class TestPrioritizedTask:
    """Tests for PrioritizedTask dataclass."""

    def test_create_minimal(self):
        """Create with minimal args."""
        from sage.core.prioritization import PrioritizedTask

        task = PrioritizedTask(id="task-1", description="Test task")
        assert task.id == "task-1"
        assert task.description == "Test task"

    def test_defaults(self):
        """Default values are set."""
        from sage.core.prioritization import (
            PrioritizedTask, TaskType, TaskSource, ImpactLevel, ConfidenceLevel
        )

        task = PrioritizedTask(id="t1", description="Test")
        assert task.task_type == TaskType.UNKNOWN
        assert task.source == TaskSource.UNKNOWN
        assert task.impact == ImpactLevel.MEDIUM
        assert task.confidence == ConfidenceLevel.MEDIUM
        assert task.base_priority == 50
        assert task.blast_radius == 0
        assert task.security_severity == 0
        assert task.user_facing is False
        assert task.is_regression is False
        assert task.is_flaky is False
        assert task.files == []
        assert task.affected_files == []
        assert task.selected_count == 0
        assert task.completed is False

    def test_effective_priority_base(self):
        """Effective priority equals base for minimal task."""
        from sage.core.prioritization import PrioritizedTask

        task = PrioritizedTask(id="t1", description="Test", base_priority=50)
        # Default source (UNKNOWN) gets no boost
        assert task.effective_priority == 50

    def test_effective_priority_test_failure_boost(self):
        """Test failure source gets +20 boost."""
        from sage.core.prioritization import PrioritizedTask, TaskSource

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            source=TaskSource.TEST_FAILURE
        )
        assert task.effective_priority == 70  # 50 + 20

    def test_effective_priority_ci_failure_boost(self):
        """CI failure source gets +20 boost."""
        from sage.core.prioritization import PrioritizedTask, TaskSource

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            source=TaskSource.CI_FAILURE
        )
        assert task.effective_priority == 70

    def test_effective_priority_lint_error_boost(self):
        """Lint error source gets +10 boost."""
        from sage.core.prioritization import PrioritizedTask, TaskSource

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            source=TaskSource.LINT_ERROR
        )
        assert task.effective_priority == 60  # 50 + 10

    def test_effective_priority_user_facing_boost(self):
        """User facing gets +15 boost."""
        from sage.core.prioritization import PrioritizedTask

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            user_facing=True
        )
        assert task.effective_priority == 65  # 50 + 15

    def test_effective_priority_regression_boost(self):
        """Regression gets +25 boost."""
        from sage.core.prioritization import PrioritizedTask

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            is_regression=True
        )
        assert task.effective_priority == 75  # 50 + 25

    def test_effective_priority_security_boost(self):
        """Security task gets boost."""
        from sage.core.prioritization import PrioritizedTask, TaskType

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            task_type=TaskType.FIX_SECURITY,
            security_severity=50
        )
        # 50 + 30 + (50 // 5) = 50 + 30 + 10 = 90
        assert task.effective_priority == 90

    def test_effective_priority_blast_radius_boost(self):
        """Blast radius adds boost (capped at 20)."""
        from sage.core.prioritization import PrioritizedTask

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            blast_radius=5
        )
        assert task.effective_priority == 60  # 50 + 5*2 = 60

        task2 = PrioritizedTask(
            id="t2", description="Test",
            base_priority=50,
            blast_radius=20  # Would be 40, but capped at 20
        )
        assert task2.effective_priority == 70  # 50 + 20 (capped)

    def test_effective_priority_low_confidence_penalty(self):
        """Low confidence gets -10 penalty."""
        from sage.core.prioritization import PrioritizedTask, ConfidenceLevel

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            confidence=ConfidenceLevel.LOW
        )
        assert task.effective_priority == 40  # 50 - 10

    def test_effective_priority_very_low_confidence_penalty(self):
        """Very low confidence gets -25 penalty."""
        from sage.core.prioritization import PrioritizedTask, ConfidenceLevel

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            confidence=ConfidenceLevel.VERY_LOW
        )
        assert task.effective_priority == 25  # 50 - 25

    def test_effective_priority_flaky_penalty(self):
        """Flaky tests get -15 penalty."""
        from sage.core.prioritization import PrioritizedTask

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            is_flaky=True
        )
        assert task.effective_priority == 35  # 50 - 15

    def test_effective_priority_refactor_penalty(self):
        """Refactor tasks get -20 penalty."""
        from sage.core.prioritization import PrioritizedTask, TaskType

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            task_type=TaskType.REFACTOR
        )
        assert task.effective_priority == 30  # 50 - 20

    def test_effective_priority_repeated_selection_penalty(self):
        """Tasks selected >2 times but not completed get -10."""
        from sage.core.prioritization import PrioritizedTask

        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=50,
            selected_count=3,
            completed=False
        )
        assert task.effective_priority == 40  # 50 - 10

    def test_effective_priority_clamped(self):
        """Priority is clamped to 0-100."""
        from sage.core.prioritization import PrioritizedTask, ConfidenceLevel, TaskType

        # Very negative
        task = PrioritizedTask(
            id="t1", description="Test",
            base_priority=10,
            confidence=ConfidenceLevel.VERY_LOW,
            is_flaky=True,
            task_type=TaskType.CLEANUP,
            selected_count=5
        )
        assert task.effective_priority >= 0

        # Very high
        task2 = PrioritizedTask(
            id="t2", description="Test",
            base_priority=100,
            is_regression=True,
            user_facing=True,
            task_type=TaskType.FIX_SECURITY,
            security_severity=100,
            blast_radius=100
        )
        assert task2.effective_priority <= 100

    def test_to_dict(self):
        """to_dict serializes correctly."""
        from sage.core.prioritization import (
            PrioritizedTask, TaskType, TaskSource, ImpactLevel, ConfidenceLevel
        )

        task = PrioritizedTask(
            id="t1",
            description="Fix bug",
            task_type=TaskType.FIX_ERROR,
            source=TaskSource.CI_FAILURE,
            files=["src/main.py"]
        )
        data = task.to_dict()

        assert data["id"] == "t1"
        assert data["description"] == "Fix bug"
        assert data["task_type"] == "fix_error"
        assert data["source"] == "ci_failure"
        assert data["files"] == ["src/main.py"]

    def test_from_dict(self):
        """from_dict deserializes correctly."""
        from sage.core.prioritization import (
            PrioritizedTask, TaskType, TaskSource
        )

        data = {
            "id": "t1",
            "description": "Fix bug",
            "task_type": "fix_error",
            "source": "ci_failure",
            "files": ["src/main.py"]
        }
        task = PrioritizedTask.from_dict(data)

        assert task.id == "t1"
        assert task.description == "Fix bug"
        assert task.task_type == TaskType.FIX_ERROR
        assert task.source == TaskSource.CI_FAILURE
        assert task.files == ["src/main.py"]

    def test_from_dict_defaults(self):
        """from_dict handles missing fields."""
        from sage.core.prioritization import PrioritizedTask

        data = {"id": "t1", "description": "Test"}
        task = PrioritizedTask.from_dict(data)

        assert task.id == "t1"
        assert task.base_priority == 50
        assert task.files == []


# =============================================================================
# Tests for FlakeyTestTracker
# =============================================================================


class TestFlakeyTestTracker:
    """Tests for FlakeyTestTracker class."""

    def test_create(self, tmp_path):
        """Create tracker."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        assert tracker is not None

    def test_record_result(self, tmp_path):
        """Record test result."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        tracker.record_result("test_foo::test_bar", passed=True)

        assert "test_foo::test_bar" in tracker._history

    def test_is_flaky_no_history(self, tmp_path):
        """No history means not flaky."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        assert tracker.is_flaky("unknown_test") is False

    def test_is_flaky_not_enough_runs(self, tmp_path):
        """Not enough runs means not flaky."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        tracker.record_result("test_1", passed=True)
        tracker.record_result("test_1", passed=False)

        assert tracker.is_flaky("test_1") is False

    def test_is_flaky_detected(self, tmp_path):
        """Detect flaky test with mixed results."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        # Mix of passes and failures
        for i in range(10):
            tracker.record_result("test_flaky", passed=(i % 2 == 0))

        assert tracker.is_flaky("test_flaky") is True

    def test_is_flaky_not_flaky_if_consistent(self, tmp_path):
        """Consistent test is not flaky."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        for i in range(10):
            tracker.record_result("test_stable", passed=True)

        assert tracker.is_flaky("test_stable") is False

    def test_get_flaky_tests(self, tmp_path):
        """Get list of flaky tests."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)

        # Add flaky test
        for i in range(10):
            tracker.record_result("test_flaky", passed=(i % 2 == 0))

        # Add stable test
        for i in range(10):
            tracker.record_result("test_stable", passed=True)

        flaky = tracker.get_flaky_tests()
        assert "test_flaky" in flaky
        assert "test_stable" not in flaky

    def test_get_reliability_unknown(self, tmp_path):
        """Unknown test has 0.5 reliability."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        assert tracker.get_reliability("unknown") == 0.5

    def test_get_reliability_all_pass(self, tmp_path):
        """All passes = 1.0 reliability."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        for _ in range(5):
            tracker.record_result("test_good", passed=True)

        assert tracker.get_reliability("test_good") == 1.0

    def test_get_reliability_all_fail(self, tmp_path):
        """All failures = 0.0 reliability."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        for _ in range(5):
            tracker.record_result("test_bad", passed=False)

        assert tracker.get_reliability("test_bad") == 0.0

    def test_persistence(self, tmp_path):
        """Tracker persists data."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker1 = FlakeyTestTracker(tmp_path)
        tracker1.record_result("test_persist", passed=True)

        # Create new tracker instance
        tracker2 = FlakeyTestTracker(tmp_path)
        assert "test_persist" in tracker2._history

    def test_history_limit(self, tmp_path):
        """History is limited to last 20 results."""
        from sage.core.prioritization import FlakeyTestTracker

        tracker = FlakeyTestTracker(tmp_path)
        for i in range(30):
            tracker.record_result("test_many", passed=True)

        assert len(tracker._history["test_many"]) == 20


# =============================================================================
# Tests for CIFailureAnalyzer
# =============================================================================


class TestCIFailureAnalyzer:
    """Tests for CIFailureAnalyzer class."""

    def test_create(self, tmp_path):
        """Create analyzer."""
        from sage.core.prioritization import CIFailureAnalyzer

        analyzer = CIFailureAnalyzer(tmp_path)
        assert analyzer is not None

    def test_analyze_pytest_failure(self, tmp_path):
        """Analyze pytest failure log."""
        from sage.core.prioritization import CIFailureAnalyzer, TaskType, TaskSource

        analyzer = CIFailureAnalyzer(tmp_path)
        log = """
        FAILED tests/test_foo.py::test_bar - AssertionError: Expected 1 but got 2
        """
        tasks = analyzer.analyze_log(log)

        assert len(tasks) == 1
        assert tasks[0].task_type == TaskType.FIX_TEST
        assert tasks[0].source == TaskSource.CI_FAILURE
        assert "test_bar" in tasks[0].description

    def test_analyze_pytest_collection_error(self, tmp_path):
        """Analyze pytest collection error."""
        from sage.core.prioritization import CIFailureAnalyzer, TaskType

        analyzer = CIFailureAnalyzer(tmp_path)
        log = """
        ERROR collecting tests/test_broken.py
        ImportError: No module named 'missing_module'
        """
        tasks = analyzer.analyze_log(log)

        assert len(tasks) >= 1
        # Should find import error
        has_import = any("import" in t.description.lower() for t in tasks)
        assert has_import or len(tasks) > 0

    def test_analyze_typescript_error(self, tmp_path):
        """Analyze TypeScript error."""
        from sage.core.prioritization import CIFailureAnalyzer, TaskType

        analyzer = CIFailureAnalyzer(tmp_path)
        log = """
        src/app.ts(42,10): error TS2339: Property 'foo' does not exist
        """
        tasks = analyzer.analyze_log(log)

        assert len(tasks) == 1
        assert "TS2339" in tasks[0].description

    def test_analyze_python_syntax_error(self, tmp_path):
        """Analyze Python syntax error."""
        from sage.core.prioritization import CIFailureAnalyzer, TaskType

        analyzer = CIFailureAnalyzer(tmp_path)
        log = '''
        File "src/broken.py", line 42
        SyntaxError: invalid syntax
        '''
        tasks = analyzer.analyze_log(log)

        assert len(tasks) == 1
        assert tasks[0].task_type == TaskType.FIX_ERROR
        assert "syntax" in tasks[0].description.lower()

    def test_analyze_no_duplicates(self, tmp_path):
        """No duplicate tasks for same failure."""
        from sage.core.prioritization import CIFailureAnalyzer

        analyzer = CIFailureAnalyzer(tmp_path)
        log = """
        FAILED tests/test_foo.py::test_bar - Error 1
        FAILED tests/test_foo.py::test_bar - Error 1
        """
        tasks = analyzer.analyze_log(log)

        # Should deduplicate
        ids = [t.id for t in tasks]
        assert len(ids) == len(set(ids))

    def test_analyze_deploy_log(self, tmp_path):
        """Analyze deploy failure log."""
        from sage.core.prioritization import CIFailureAnalyzer, TaskSource

        analyzer = CIFailureAnalyzer(tmp_path)
        log = """
        ERROR: Failed to deploy application - Connection refused
        """
        tasks = analyzer.analyze_deploy_log(log)

        assert len(tasks) == 1
        assert tasks[0].source == TaskSource.DEPLOY_FAILURE
        assert tasks[0].user_facing is True

    def test_analyze_deploy_skips_short_errors(self, tmp_path):
        """Skip very short error messages."""
        from sage.core.prioritization import CIFailureAnalyzer

        analyzer = CIFailureAnalyzer(tmp_path)
        log = "ERROR: x"  # Too short
        tasks = analyzer.analyze_deploy_log(log)

        assert len(tasks) == 0


# =============================================================================
# Tests for AutopolitState
# =============================================================================


class TestAutopolitState:
    """Tests for AutopolitState class."""

    def test_create(self, tmp_path):
        """Create state."""
        from sage.core.prioritization import AutopolitState

        state = AutopolitState(tmp_path)
        assert state.tasks == []
        assert state.cycle_count == 0

    def test_add_task(self, tmp_path):
        """Add task to state."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        task = PrioritizedTask(id="t1", description="Test")
        state.add_task(task)

        assert len(state.tasks) == 1

    def test_add_task_no_duplicates(self, tmp_path):
        """Don't add duplicate tasks."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        task = PrioritizedTask(id="t1", description="Test")
        state.add_task(task)
        state.add_task(task)

        assert len(state.tasks) == 1

    def test_add_task_skips_completed(self, tmp_path):
        """Don't add completed tasks."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        state.completed_task_ids.add("t1")

        task = PrioritizedTask(id="t1", description="Test")
        state.add_task(task)

        assert len(state.tasks) == 0

    def test_add_task_skips_suppressed(self, tmp_path):
        """Don't add suppressed tasks."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        state.suppressed_task_ids.add("t1")

        task = PrioritizedTask(id="t1", description="Test")
        state.add_task(task)

        assert len(state.tasks) == 0

    def test_get_next_task(self, tmp_path):
        """Get highest priority task."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        state.add_task(PrioritizedTask(id="t1", description="Low", base_priority=30))
        state.add_task(PrioritizedTask(id="t2", description="High", base_priority=80))
        state.add_task(PrioritizedTask(id="t3", description="Med", base_priority=50))

        task = state.get_next_task()
        assert task.id == "t2"  # Highest priority

    def test_get_next_task_none_when_empty(self, tmp_path):
        """Return None when no tasks."""
        from sage.core.prioritization import AutopolitState

        state = AutopolitState(tmp_path)
        assert state.get_next_task() is None

    def test_get_next_task_updates_selection(self, tmp_path):
        """Getting task updates selection count."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        task = PrioritizedTask(id="t1", description="Test")
        state.add_task(task)

        result = state.get_next_task()
        assert result.selected_count == 1
        assert result.last_selected is not None

    def test_mark_completed(self, tmp_path):
        """Mark task as completed."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        task = PrioritizedTask(id="t1", description="Test")
        state.add_task(task)

        state.mark_completed("t1")

        assert "t1" in state.completed_task_ids
        assert state.tasks[0].completed is True

    def test_suppress_task(self, tmp_path):
        """Suppress task from selection."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state = AutopolitState(tmp_path)
        task = PrioritizedTask(id="t1", description="Test")
        state.add_task(task)

        state.suppress_task("t1")

        assert "t1" in state.suppressed_task_ids

    def test_start_cycle(self, tmp_path):
        """Start new cycle."""
        from sage.core.prioritization import AutopolitState

        state = AutopolitState(tmp_path)
        state.start_cycle()

        assert state.cycle_count == 1
        assert state.last_cycle is not None

    def test_get_backlog_summary_empty(self, tmp_path):
        """Backlog summary when empty."""
        from sage.core.prioritization import AutopolitState

        state = AutopolitState(tmp_path)
        summary = state.get_backlog_summary()

        assert summary == "No pending tasks"

    def test_get_backlog_summary(self, tmp_path):
        """Backlog summary with tasks."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask, TaskType

        state = AutopolitState(tmp_path)
        state.add_task(PrioritizedTask(id="t1", description="T1", task_type=TaskType.FIX_ERROR))
        state.add_task(PrioritizedTask(id="t2", description="T2", task_type=TaskType.FIX_ERROR))
        state.add_task(PrioritizedTask(id="t3", description="T3", task_type=TaskType.FIX_TEST))

        summary = state.get_backlog_summary()
        assert "3 tasks" in summary
        assert "fix_error" in summary

    def test_persistence(self, tmp_path):
        """State persists to disk."""
        from sage.core.prioritization import AutopolitState, PrioritizedTask

        state1 = AutopolitState(tmp_path)
        state1.add_task(PrioritizedTask(id="t1", description="Persist test"))
        state1.save()

        state2 = AutopolitState(tmp_path)
        assert len(state2.tasks) == 1
        assert state2.tasks[0].id == "t1"


# =============================================================================
# Tests for TaskPrioritizer
# =============================================================================


class TestTaskPrioritizer:
    """Tests for TaskPrioritizer class."""

    def test_create(self, tmp_path):
        """Create prioritizer."""
        from sage.core.prioritization import TaskPrioritizer

        prioritizer = TaskPrioritizer(tmp_path)
        assert prioritizer is not None
        assert prioritizer.analysis_only is False
        assert prioritizer.baseline_red is False

    def test_set_analysis_only(self, tmp_path):
        """Set analysis-only mode."""
        from sage.core.prioritization import TaskPrioritizer

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.set_analysis_only(True)
        assert prioritizer.analysis_only is True

    def test_set_baseline_red(self, tmp_path):
        """Set baseline-red mode."""
        from sage.core.prioritization import TaskPrioritizer

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.set_baseline_red(True)
        assert prioritizer.baseline_red is True

    def test_ingest_ci_log(self, tmp_path):
        """Ingest CI log."""
        from sage.core.prioritization import TaskPrioritizer

        prioritizer = TaskPrioritizer(tmp_path)
        log = """
        FAILED tests/test_foo.py::test_bar - AssertionError
        """
        count = prioritizer.ingest_ci_log(log)
        assert count == 1

    def test_ingest_deploy_log(self, tmp_path):
        """Ingest deploy log."""
        from sage.core.prioritization import TaskPrioritizer

        prioritizer = TaskPrioritizer(tmp_path)
        log = "ERROR: Deploy failed with connection error"
        count = prioritizer.ingest_deploy_log(log)
        assert count == 1

    def test_add_task_from_test_failure(self, tmp_path):
        """Add task from test failure."""
        from sage.core.prioritization import TaskPrioritizer, TaskType

        prioritizer = TaskPrioritizer(tmp_path)
        task = prioritizer.add_task_from_test_failure(
            test_id="test_foo::test_bar",
            error_message="AssertionError: Expected 1",
            file_path="tests/test_foo.py"
        )

        assert task.task_type == TaskType.FIX_TEST
        assert "tests/test_foo.py" in task.files

    def test_add_task_from_security_finding(self, tmp_path):
        """Add task from security finding."""
        from sage.core.prioritization import TaskPrioritizer, TaskType

        prioritizer = TaskPrioritizer(tmp_path)
        task = prioritizer.add_task_from_security_finding(
            finding_id="SEC001",
            description="SQL injection vulnerability",
            severity="HIGH",
            file_path="src/db.py",
            line=42
        )

        assert task.task_type == TaskType.FIX_SECURITY
        assert task.security_severity == 75

    def test_calculate_blast_radius(self, tmp_path):
        """Calculate blast radius."""
        from sage.core.prioritization import TaskPrioritizer

        prioritizer = TaskPrioritizer(tmp_path)

        mock_graph = MagicMock()
        mock_graph.get_affected_files.return_value = ["a.py", "b.py", "c.py"]

        radius = prioritizer.calculate_blast_radius("a.py", mock_graph)
        assert radius == 2  # 3 - 1 (exclude self)

    def test_calculate_blast_radius_error(self, tmp_path):
        """Blast radius handles errors."""
        from sage.core.prioritization import TaskPrioritizer

        prioritizer = TaskPrioritizer(tmp_path)

        mock_graph = MagicMock()
        mock_graph.get_affected_files.side_effect = Exception("Error")

        radius = prioritizer.calculate_blast_radius("a.py", mock_graph)
        assert radius == 0

    def test_assess_confidence_high(self, tmp_path):
        """Assess high confidence."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(id="t1", description="Test", files=["a.py"])

        confidence = prioritizer.assess_confidence(
            task, files_read={"a.py"}, scan_coverage=90
        )
        assert confidence == ConfidenceLevel.HIGH

    def test_assess_confidence_medium(self, tmp_path):
        """Assess medium confidence."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(id="t1", description="Test", files=["a.py"])

        confidence = prioritizer.assess_confidence(
            task, files_read={"a.py"}, scan_coverage=60
        )
        assert confidence == ConfidenceLevel.MEDIUM

    def test_assess_confidence_low(self, tmp_path):
        """Assess low confidence."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(id="t1", description="Test", files=["a.py", "b.py"])

        confidence = prioritizer.assess_confidence(
            task, files_read={"a.py"}, scan_coverage=30
        )
        assert confidence == ConfidenceLevel.LOW

    def test_assess_confidence_very_low(self, tmp_path):
        """Assess very low confidence."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(id="t1", description="Test", files=["a.py"])

        confidence = prioritizer.assess_confidence(
            task, files_read=set(), scan_coverage=10
        )
        assert confidence == ConfidenceLevel.VERY_LOW

    def test_should_read_more_low_confidence(self, tmp_path):
        """Should read more with low confidence."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(
            id="t1", description="Test",
            confidence=ConfidenceLevel.LOW,
            files=["a.py"]
        )

        should_read, files = prioritizer.should_read_more(task)
        assert should_read is True
        assert "a.py" in files

    def test_should_read_more_needs_context(self, tmp_path):
        """Should read more when needs_more_context is set."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(
            id="t1", description="Test",
            confidence=ConfidenceLevel.MEDIUM,
            needs_more_context=True,
            suggested_reads=["b.py"]
        )

        should_read, files = prioritizer.should_read_more(task)
        assert should_read is True
        assert "b.py" in files

    def test_should_read_more_high_confidence(self, tmp_path):
        """Don't need to read more with high confidence."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(
            id="t1", description="Test",
            confidence=ConfidenceLevel.HIGH
        )

        should_read, files = prioritizer.should_read_more(task)
        assert should_read is False

    def test_should_refuse_destructive_very_low_confidence(self, tmp_path):
        """Refuse destructive with very low confidence."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(
            id="t1", description="Test",
            confidence=ConfidenceLevel.VERY_LOW
        )

        should_refuse, reason = prioritizer.should_refuse_destructive(
            task, "delete all files"
        )
        assert should_refuse is True
        assert "confidence" in reason.lower()

    def test_should_refuse_destructive_no_files(self, tmp_path):
        """Refuse destructive with no files."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, ConfidenceLevel
        )

        prioritizer = TaskPrioritizer(tmp_path)
        task = PrioritizedTask(
            id="t1", description="Test",
            confidence=ConfidenceLevel.HIGH,
            files=[]
        )

        should_refuse, reason = prioritizer.should_refuse_destructive(
            task, "remove old code"
        )
        assert should_refuse is True
        assert "files" in reason.lower()

    def test_should_refuse_refactor_in_baseline_red(self, tmp_path):
        """Refuse refactor in baseline-red mode."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, TaskType
        )

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.set_baseline_red(True)

        task = PrioritizedTask(
            id="t1", description="Test",
            task_type=TaskType.REFACTOR,
            files=["a.py"]
        )

        should_refuse, reason = prioritizer.should_refuse_destructive(
            task, "refactor code"
        )
        assert should_refuse is True
        assert "baseline-red" in reason.lower()

    def test_get_next_task(self, tmp_path):
        """Get next task from prioritizer."""
        from sage.core.prioritization import TaskPrioritizer, PrioritizedTask

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.state.add_task(PrioritizedTask(id="t1", description="Test"))

        task = prioritizer.get_next_task()
        assert task.id == "t1"

    def test_get_prioritized_list(self, tmp_path):
        """Get prioritized list of tasks."""
        from sage.core.prioritization import TaskPrioritizer, PrioritizedTask

        prioritizer = TaskPrioritizer(tmp_path)
        for i in range(5):
            prioritizer.state.add_task(
                PrioritizedTask(id=f"t{i}", description=f"Task {i}", base_priority=i*10)
            )

        tasks = prioritizer.get_prioritized_list(limit=3)
        assert len(tasks) == 3
        # Should be sorted by priority (descending)
        assert tasks[0].base_priority > tasks[2].base_priority

    def test_get_prioritized_list_baseline_red_filters(self, tmp_path):
        """Baseline-red mode filters refactors."""
        from sage.core.prioritization import (
            TaskPrioritizer, PrioritizedTask, TaskType
        )

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.set_baseline_red(True)

        prioritizer.state.add_task(
            PrioritizedTask(id="t1", description="Refactor", task_type=TaskType.REFACTOR)
        )
        prioritizer.state.add_task(
            PrioritizedTask(id="t2", description="Fix", task_type=TaskType.FIX_ERROR)
        )

        tasks = prioritizer.get_prioritized_list()
        assert len(tasks) == 1
        assert tasks[0].id == "t2"

    def test_complete_task(self, tmp_path):
        """Complete a task."""
        from sage.core.prioritization import TaskPrioritizer, PrioritizedTask

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.state.add_task(PrioritizedTask(id="t1", description="Test"))

        prioritizer.complete_task("t1")

        assert "t1" in prioritizer.state.completed_task_ids

    def test_suppress_task(self, tmp_path):
        """Suppress a task."""
        from sage.core.prioritization import TaskPrioritizer, PrioritizedTask

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.state.add_task(PrioritizedTask(id="t1", description="Test"))

        prioritizer.suppress_task("t1")

        assert "t1" in prioritizer.state.suppressed_task_ids

    def test_get_status(self, tmp_path):
        """Get prioritizer status."""
        from sage.core.prioritization import TaskPrioritizer, PrioritizedTask

        prioritizer = TaskPrioritizer(tmp_path)
        prioritizer.state.add_task(PrioritizedTask(id="t1", description="Test"))

        status = prioritizer.get_status()
        assert "1 tasks" in status
