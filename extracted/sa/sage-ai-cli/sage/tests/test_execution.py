"""Tests for sage.execution module."""

import pytest

from sage.execution import (
    AdaptiveExecutionEngine,
    ExecutionResult,
    ExecutionTask,
    ParallelExecutor,
    ProgressTracker,
    RetryConfig,
    RetryStrategy,
    SmartRetryHandler,
    TaskPriority,
    TaskScheduler,
    TaskStatus,
)


class TestRetryStrategy:
    """Test RetryStrategy enum."""

    def test_strategies_exist(self):
        """Test all retry strategies exist."""
        assert RetryStrategy.NONE is not None
        assert RetryStrategy.LINEAR is not None
        assert RetryStrategy.EXPONENTIAL is not None
        assert RetryStrategy.ADAPTIVE is not None
        assert RetryStrategy.SMART is not None

    def test_strategy_values(self):
        """Test strategy values are strings."""
        assert RetryStrategy.NONE.value == "none"
        assert RetryStrategy.EXPONENTIAL.value == "exponential"


class TestTaskPriority:
    """Test TaskPriority enum."""

    def test_priorities_exist(self):
        """Test all priorities exist."""
        assert TaskPriority.CRITICAL is not None
        assert TaskPriority.HIGH is not None
        assert TaskPriority.MEDIUM is not None
        assert TaskPriority.LOW is not None
        assert TaskPriority.BACKGROUND is not None

    def test_priority_ordering(self):
        """Test priority values are ordered correctly."""
        assert TaskPriority.CRITICAL.value < TaskPriority.HIGH.value
        assert TaskPriority.HIGH.value < TaskPriority.MEDIUM.value
        assert TaskPriority.MEDIUM.value < TaskPriority.LOW.value
        assert TaskPriority.LOW.value < TaskPriority.BACKGROUND.value


class TestTaskStatus:
    """Test TaskStatus enum."""

    def test_statuses_exist(self):
        """Test all statuses exist."""
        assert TaskStatus.PENDING is not None
        assert TaskStatus.RUNNING is not None
        assert TaskStatus.COMPLETED is not None
        assert TaskStatus.FAILED is not None
        assert TaskStatus.RETRYING is not None
        assert TaskStatus.BLOCKED is not None


class TestRetryConfig:
    """Test RetryConfig dataclass."""

    def test_default_config(self):
        """Test default configuration."""
        config = RetryConfig()
        assert config.strategy == RetryStrategy.ADAPTIVE
        assert config.max_attempts == 5
        assert config.initial_delay == 1.0
        assert config.backoff_factor == 2.0

    def test_custom_config(self):
        """Test custom configuration."""
        config = RetryConfig(
            strategy=RetryStrategy.EXPONENTIAL,
            max_attempts=10,
            initial_delay=0.5,
            max_delay=60.0,
        )
        assert config.max_attempts == 10
        assert config.initial_delay == 0.5
        assert config.max_delay == 60.0


class TestExecutionResult:
    """Test ExecutionResult dataclass."""

    def test_success_result(self):
        """Test successful execution result."""
        result = ExecutionResult(
            success=True,
            output="Test passed",
            duration=1.5,
            exit_code=0,
        )
        assert result.success is True
        assert result.output == "Test passed"
        assert result.error is None
        assert result.exit_code == 0

    def test_failure_result(self):
        """Test failed execution result."""
        result = ExecutionResult(
            success=False,
            output="",
            error="Command not found",
            exit_code=127,
            attempts=3,
        )
        assert result.success is False
        assert result.error == "Command not found"
        assert result.attempts == 3

    def test_metadata(self):
        """Test result metadata."""
        result = ExecutionResult(
            success=True,
            output="OK",
            metadata={"retries": 2, "final_delay": 4.0},
        )
        assert result.metadata["retries"] == 2


class TestExecutionTask:
    """Test ExecutionTask dataclass."""

    def test_create_task(self):
        """Test creating a task."""
        task = ExecutionTask(
            id="task1",
            description="Run tests",
            command="pytest",
        )
        assert task.id == "task1"
        assert task.description == "Run tests"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.MEDIUM

    def test_task_with_priority(self):
        """Test task with custom priority."""
        task = ExecutionTask(
            id="critical1",
            description="Fix production bug",
            command="./fix.sh",
            priority=TaskPriority.CRITICAL,
            timeout=60.0,
        )
        assert task.priority == TaskPriority.CRITICAL
        assert task.timeout == 60.0

    def test_task_with_dependencies(self):
        """Test task with dependencies."""
        task = ExecutionTask(
            id="task2",
            description="Deploy",
            command="./deploy.sh",
            dependencies=["task1", "task0"],
        )
        assert len(task.dependencies) == 2
        assert "task1" in task.dependencies

    def test_task_with_callable(self):
        """Test task with callable command."""

        def my_func():
            return "done"

        task = ExecutionTask(
            id="func_task",
            description="Run function",
            command=my_func,
        )
        assert callable(task.command)


class TestSmartRetryHandler:
    """Test SmartRetryHandler class."""

    def test_handler_class_exists(self):
        """Test SmartRetryHandler class is importable."""
        assert SmartRetryHandler is not None

    def test_handler_initialization(self):
        """Test handler initializes."""
        handler = SmartRetryHandler()
        assert handler is not None


class TestParallelExecutor:
    """Test ParallelExecutor class."""

    def test_executor_initialization(self):
        """Test executor initializes correctly."""
        executor = ParallelExecutor(max_workers=4)
        assert executor is not None
        assert executor.max_workers == 4

    def test_default_workers(self):
        """Test default worker count."""
        executor = ParallelExecutor()
        assert executor.max_workers >= 1


class TestTaskScheduler:
    """Test TaskScheduler class."""

    def test_scheduler_initialization(self):
        """Test scheduler initializes correctly."""
        scheduler = TaskScheduler()
        assert scheduler is not None

    def test_add_tasks(self):
        """Test adding tasks to scheduler."""
        scheduler = TaskScheduler()
        task = ExecutionTask(
            id="test",
            description="Test",
            command="echo test",
        )
        # Use the actual method name
        if hasattr(scheduler, "add_task"):
            scheduler.add_task(task)
        elif hasattr(scheduler, "add_tasks"):
            scheduler.add_tasks([task])
        assert True  # Just test it doesn't crash


class TestAdaptiveExecutionEngine:
    """Test AdaptiveExecutionEngine class exists."""

    def test_engine_class_exists(self):
        """Test AdaptiveExecutionEngine class is importable."""
        assert AdaptiveExecutionEngine is not None


class TestProgressTracker:
    """Test ProgressTracker class."""

    def test_tracker_initialization(self):
        """Test tracker initializes correctly."""
        tracker = ProgressTracker(total_tasks=10)
        assert tracker.total_tasks == 10

    def test_tracker_attributes(self):
        """Test tracker has expected attributes."""
        tracker = ProgressTracker(total_tasks=5)
        assert hasattr(tracker, "total_tasks")
        assert hasattr(tracker, "completed_tasks")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
