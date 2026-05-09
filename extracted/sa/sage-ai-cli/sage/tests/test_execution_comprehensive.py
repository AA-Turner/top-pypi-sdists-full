"""Comprehensive tests for sage/execution.py - Task Execution System."""

import time
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from sage.execution import (
    # Enums
    RetryStrategy,
    TaskPriority,
    TaskStatus,
    # Dataclasses
    RetryConfig,
    ExecutionResult,
    ExecutionTask,
    # Classes
    SmartRetryHandler,
    ParallelExecutor,
    TaskScheduler,
    AdaptiveExecutionEngine,
    ProgressTracker,
)


# =============================================================================
# Tests for RetryStrategy Enum
# =============================================================================


class TestRetryStrategy:
    """Tests for RetryStrategy enum."""

    def test_none(self):
        """NONE is defined."""
        assert RetryStrategy.NONE.value == "none"

    def test_linear(self):
        """LINEAR is defined."""
        assert RetryStrategy.LINEAR.value == "linear"

    def test_exponential(self):
        """EXPONENTIAL is defined."""
        assert RetryStrategy.EXPONENTIAL.value == "exponential"

    def test_adaptive(self):
        """ADAPTIVE is defined."""
        assert RetryStrategy.ADAPTIVE.value == "adaptive"

    def test_smart(self):
        """SMART is defined."""
        assert RetryStrategy.SMART.value == "smart"


# =============================================================================
# Tests for TaskPriority Enum
# =============================================================================


class TestTaskPriority:
    """Tests for TaskPriority enum."""

    def test_critical(self):
        """CRITICAL has value 1."""
        assert TaskPriority.CRITICAL.value == 1

    def test_high(self):
        """HIGH has value 2."""
        assert TaskPriority.HIGH.value == 2

    def test_medium(self):
        """MEDIUM has value 3."""
        assert TaskPriority.MEDIUM.value == 3

    def test_low(self):
        """LOW has value 4."""
        assert TaskPriority.LOW.value == 4

    def test_background(self):
        """BACKGROUND has value 5."""
        assert TaskPriority.BACKGROUND.value == 5


# =============================================================================
# Tests for TaskStatus Enum
# =============================================================================


class TestTaskStatus:
    """Tests for TaskStatus enum."""

    def test_pending(self):
        """PENDING is defined."""
        assert TaskStatus.PENDING.value == "pending"

    def test_queued(self):
        """QUEUED is defined."""
        assert TaskStatus.QUEUED.value == "queued"

    def test_running(self):
        """RUNNING is defined."""
        assert TaskStatus.RUNNING.value == "running"

    def test_completed(self):
        """COMPLETED is defined."""
        assert TaskStatus.COMPLETED.value == "completed"

    def test_failed(self):
        """FAILED is defined."""
        assert TaskStatus.FAILED.value == "failed"

    def test_retrying(self):
        """RETRYING is defined."""
        assert TaskStatus.RETRYING.value == "retrying"

    def test_blocked(self):
        """BLOCKED is defined."""
        assert TaskStatus.BLOCKED.value == "blocked"

    def test_cancelled(self):
        """CANCELLED is defined."""
        assert TaskStatus.CANCELLED.value == "cancelled"


# =============================================================================
# Tests for RetryConfig Dataclass
# =============================================================================


class TestRetryConfig:
    """Tests for RetryConfig dataclass."""

    def test_defaults(self):
        """Check default values."""
        config = RetryConfig()
        assert config.strategy == RetryStrategy.ADAPTIVE
        assert config.max_attempts == 5
        assert config.initial_delay == 1.0
        assert config.max_delay == 30.0
        assert config.backoff_factor == 2.0
        assert config.jitter is True

    def test_custom_values(self):
        """Create with custom values."""
        config = RetryConfig(
            strategy=RetryStrategy.LINEAR,
            max_attempts=3,
            initial_delay=0.5,
        )
        assert config.strategy == RetryStrategy.LINEAR
        assert config.max_attempts == 3


# =============================================================================
# Tests for ExecutionResult Dataclass
# =============================================================================


class TestExecutionResult:
    """Tests for ExecutionResult dataclass."""

    def test_create_success(self):
        """Create successful result."""
        result = ExecutionResult(success=True, output="Done")
        assert result.success is True
        assert result.output == "Done"
        assert result.error is None
        assert result.exit_code == 0

    def test_create_failure(self):
        """Create failed result."""
        result = ExecutionResult(
            success=False,
            output="",
            error="Command failed",
            exit_code=1,
        )
        assert result.success is False
        assert result.error == "Command failed"


# =============================================================================
# Tests for ExecutionTask Dataclass
# =============================================================================


class TestExecutionTask:
    """Tests for ExecutionTask dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        task = ExecutionTask(
            id="task-1",
            description="Test task",
            command="echo hello",
        )
        assert task.id == "task-1"
        assert task.priority == TaskPriority.MEDIUM
        assert task.status == TaskStatus.PENDING

    def test_create_with_function(self):
        """Create with function command."""
        def my_func():
            return 42
        
        task = ExecutionTask(
            id="task-2",
            description="Function task",
            command=my_func,
        )
        assert callable(task.command)

    def test_comparison(self):
        """Tasks compare by priority."""
        high = ExecutionTask(
            id="high", description="High", command="echo 1",
            priority=TaskPriority.HIGH,
        )
        low = ExecutionTask(
            id="low", description="Low", command="echo 2",
            priority=TaskPriority.LOW,
        )
        assert high < low  # HIGH (2) < LOW (4)


# =============================================================================
# Tests for SmartRetryHandler
# =============================================================================


class TestSmartRetryHandler:
    """Tests for SmartRetryHandler class."""

    def test_init(self):
        """Initialize handler."""
        handler = SmartRetryHandler()
        assert handler.error_history == {}

    def test_categorize_timeout(self):
        """Categorize timeout error."""
        handler = SmartRetryHandler()
        result = handler.categorize_error("Connection timeout occurred")
        assert result["category"] == "transient"
        assert result["should_retry"] is True

    def test_categorize_rate_limit(self):
        """Categorize rate limit error."""
        handler = SmartRetryHandler()
        result = handler.categorize_error("Error 429: Rate limit exceeded")
        assert result["category"] == "transient"

    def test_categorize_syntax_error(self):
        """Categorize syntax error."""
        handler = SmartRetryHandler()
        result = handler.categorize_error("SyntaxError: invalid syntax")
        assert result["category"] == "syntax"
        assert result["should_retry"] is False

    def test_categorize_import_error(self):
        """Categorize import error."""
        handler = SmartRetryHandler()
        result = handler.categorize_error("ModuleNotFoundError: No module named 'foo'")
        assert result["category"] == "import"
        assert result["should_retry"] is False

    def test_categorize_permission_error(self):
        """Categorize permission error."""
        handler = SmartRetryHandler()
        result = handler.categorize_error("Permission denied: /root/file")
        assert result["category"] == "permission"
        assert result["should_retry"] is False

    def test_categorize_unknown(self):
        """Categorize unknown error."""
        handler = SmartRetryHandler()
        result = handler.categorize_error("Some random error")
        assert result["category"] == "unknown"
        assert result["should_retry"] is True

    def test_should_retry_transient(self):
        """Should retry transient error."""
        handler = SmartRetryHandler()
        config = RetryConfig(max_attempts=3)
        should_retry, delay = handler.should_retry("Connection timeout", 1, config)
        assert should_retry is True
        assert delay > 0

    def test_should_retry_permanent(self):
        """Should not retry permanent error."""
        handler = SmartRetryHandler()
        config = RetryConfig()
        # Use "invalid syntax" which matches the syntax category pattern
        should_retry, delay = handler.should_retry("invalid syntax in line 5", 1, config)
        assert should_retry is False

    def test_should_retry_max_attempts(self):
        """Should not retry when max attempts reached."""
        handler = SmartRetryHandler()
        config = RetryConfig(max_attempts=3)
        should_retry, delay = handler.should_retry("timeout", 3, config)
        assert should_retry is False

    def test_should_retry_strategy_none(self):
        """No retry with NONE strategy."""
        handler = SmartRetryHandler()
        config = RetryConfig(strategy=RetryStrategy.NONE)
        should_retry, delay = handler.should_retry("timeout", 1, config)
        assert should_retry is False

    def test_record_error(self):
        """Record error for learning."""
        handler = SmartRetryHandler()
        handler.record_error("task-1", "Connection timeout", 1)
        assert "task-1" in handler.error_history
        assert len(handler.error_history["task-1"]) == 1

    def test_get_error_summary(self):
        """Get error summary."""
        handler = SmartRetryHandler()
        handler.record_error("task-1", "timeout", 1)
        handler.record_error("task-1", "timeout", 2)
        summary = handler.get_error_summary("task-1")
        assert "Total errors: 2" in summary

    def test_get_error_summary_no_errors(self):
        """Get empty error summary."""
        handler = SmartRetryHandler()
        summary = handler.get_error_summary("unknown")
        assert "No errors recorded" in summary


# =============================================================================
# Tests for ParallelExecutor
# =============================================================================


class TestParallelExecutor:
    """Tests for ParallelExecutor class."""

    def test_init(self):
        """Initialize executor."""
        executor = ParallelExecutor(max_workers=2)
        assert executor.max_workers == 2

    def test_execute_batch_empty(self):
        """Execute empty batch."""
        executor = ParallelExecutor()
        results = executor.execute_batch([])
        assert results == {}

    def test_execute_batch_function_tasks(self):
        """Execute batch with function tasks."""
        executor = ParallelExecutor(max_workers=2)
        
        def task_func():
            return "result"
        
        tasks = [
            ExecutionTask(id="t1", description="Task 1", command=task_func),
            ExecutionTask(id="t2", description="Task 2", command=task_func),
        ]
        
        results = executor.execute_batch(tasks)
        
        assert len(results) == 2
        assert results["t1"].success is True
        assert results["t2"].success is True

    def test_execute_batch_with_dependencies(self):
        """Execute batch respecting dependencies."""
        executor = ParallelExecutor(max_workers=1)
        
        results_order = []
        
        def make_task(name):
            def func():
                results_order.append(name)
                return name
            return func
        
        tasks = [
            ExecutionTask(
                id="t2", description="Task 2", command=make_task("t2"),
                dependencies=["t1"],
            ),
            ExecutionTask(
                id="t1", description="Task 1", command=make_task("t1"),
            ),
        ]
        
        executor.execute_batch(tasks)
        
        # t1 should execute before t2 due to dependency
        assert results_order.index("t1") < results_order.index("t2")


# =============================================================================
# Tests for TaskScheduler
# =============================================================================


class TestTaskScheduler:
    """Tests for TaskScheduler class."""

    def test_init(self):
        """Initialize scheduler."""
        scheduler = TaskScheduler(max_workers=4)
        assert scheduler.max_workers == 4

    def test_add_task(self):
        """Add task to scheduler."""
        scheduler = TaskScheduler()
        task = ExecutionTask(id="t1", description="Test", command="echo")
        task_id = scheduler.add_task(task)
        assert task_id == "t1"
        assert "t1" in scheduler.tasks

    def test_add_tasks(self):
        """Add multiple tasks."""
        scheduler = TaskScheduler()
        tasks = [
            ExecutionTask(id="t1", description="T1", command="echo 1"),
            ExecutionTask(id="t2", description="T2", command="echo 2"),
        ]
        ids = scheduler.add_tasks(tasks)
        assert ids == ["t1", "t2"]

    def test_get_task_status(self):
        """Get task status."""
        scheduler = TaskScheduler()
        task = ExecutionTask(id="t1", description="Test", command="echo")
        scheduler.add_task(task)
        status = scheduler.get_task_status("t1")
        assert status == TaskStatus.PENDING

    def test_get_task_status_unknown(self):
        """Get status of unknown task."""
        scheduler = TaskScheduler()
        status = scheduler.get_task_status("unknown")
        assert status is None

    def test_cancel_task(self):
        """Cancel a pending task."""
        scheduler = TaskScheduler()
        task = ExecutionTask(id="t1", description="Test", command="echo")
        scheduler.add_task(task)
        result = scheduler.cancel_task("t1")
        assert result is True
        assert scheduler.tasks["t1"].status == TaskStatus.CANCELLED

    def test_cancel_unknown_task(self):
        """Cancel unknown task returns False."""
        scheduler = TaskScheduler()
        result = scheduler.cancel_task("unknown")
        assert result is False

    def test_get_summary(self):
        """Get task summary."""
        scheduler = TaskScheduler()
        tasks = [
            ExecutionTask(id="t1", description="T1", command="echo 1", priority=TaskPriority.HIGH),
            ExecutionTask(id="t2", description="T2", command="echo 2", priority=TaskPriority.LOW),
        ]
        scheduler.add_tasks(tasks)
        summary = scheduler.get_summary()
        assert summary["total"] == 2
        assert "pending" in summary["by_status"]
        assert "HIGH" in summary["by_priority"]


# =============================================================================
# Tests for ProgressTracker
# =============================================================================


class TestProgressTracker:
    """Tests for ProgressTracker class."""

    def test_init(self):
        """Initialize tracker."""
        tracker = ProgressTracker(total_tasks=10)
        assert tracker.total_tasks == 10
        assert tracker.completed_tasks == 0

    def test_update_completed(self):
        """Update with completed task."""
        tracker = ProgressTracker(total_tasks=10)
        tracker.update("t1", TaskStatus.COMPLETED, "Task 1")
        assert tracker.completed_tasks == 1

    def test_update_failed(self):
        """Update with failed task."""
        tracker = ProgressTracker(total_tasks=10)
        tracker.update("t1", TaskStatus.FAILED, "Task 1")
        assert tracker.failed_tasks == 1

    def test_get_progress(self):
        """Get progress information."""
        tracker = ProgressTracker(total_tasks=4)
        tracker.update("t1", TaskStatus.COMPLETED)
        tracker.update("t2", TaskStatus.COMPLETED)
        progress = tracker.get_progress()
        assert progress["total"] == 4
        assert progress["completed"] == 2
        assert progress["remaining"] == 2
        assert progress["percent"] == 50.0

    def test_format_progress(self):
        """Format progress as string."""
        tracker = ProgressTracker(total_tasks=10)
        tracker.update("t1", TaskStatus.COMPLETED)
        formatted = tracker.format_progress()
        assert "10%" in formatted
        assert "1/10" in formatted


# =============================================================================
# Tests for AdaptiveExecutionEngine
# =============================================================================


class TestAdaptiveExecutionEngine:
    """Tests for AdaptiveExecutionEngine class."""

    def test_init(self):
        """Initialize engine."""
        engine = AdaptiveExecutionEngine(cwd=Path("/tmp"), max_workers=2)
        assert engine.cwd == Path("/tmp")

    def test_get_learning_insights_empty(self):
        """Get insights with no history."""
        engine = AdaptiveExecutionEngine(cwd=Path("/tmp"))
        insights = engine.get_learning_insights()
        assert "No execution history" in insights["message"]

    def test_suggest_optimizations_empty(self):
        """Get suggestions with no history."""
        engine = AdaptiveExecutionEngine(cwd=Path("/tmp"))
        suggestions = engine.suggest_optimizations()
        assert isinstance(suggestions, list)


# =============================================================================
# Integration Tests
# =============================================================================


class TestExecutionIntegration:
    """Integration tests for execution system."""

    def test_full_execution_flow(self):
        """Full task execution flow."""
        scheduler = TaskScheduler(max_workers=2)
        
        results_collected = []
        
        def task_a():
            results_collected.append("a")
            return "A done"
        
        def task_b():
            results_collected.append("b")
            return "B done"
        
        tasks = [
            ExecutionTask(id="a", description="Task A", command=task_a),
            ExecutionTask(id="b", description="Task B", command=task_b),
        ]
        
        scheduler.add_tasks(tasks)
        results = scheduler.execute_all()
        
        assert len(results) == 2
        assert results["a"].success is True
        assert results["b"].success is True
        assert "a" in results_collected
        assert "b" in results_collected

    def test_retry_flow(self):
        """Test retry with eventually succeeding task."""
        attempt_count = [0]
        
        def flaky_task():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise Exception("Transient timeout error")
            return "success"
        
        task = ExecutionTask(
            id="flaky",
            description="Flaky task",
            command=flaky_task,
            retry_config=RetryConfig(
                strategy=RetryStrategy.LINEAR,
                max_attempts=5,
                initial_delay=0.01,
            ),
        )
        
        executor = ParallelExecutor(max_workers=1)
        result = executor._execute_single(task)
        
        assert result.success is True
        assert result.attempts == 3
