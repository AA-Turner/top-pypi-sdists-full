"""Comprehensive tests for sage/core/tasks.py - Task state machine and progress tracking."""

import asyncio
import time
from unittest.mock import MagicMock, patch

import pytest

from sage.core.tasks import (
    # Enums
    TaskState,
    TaskPriority,
    TaskTransition,
    # Dataclasses
    TaskResult,
    Task,
    # Classes
    TaskManager,
    TaskProgressDisplay,
    RetryHandler,
    # Constants
    VALID_TRANSITIONS,
    # Functions
    create_task_manager,
    create_progress_display,
)


# =============================================================================
# Tests for TaskState Enum
# =============================================================================


class TestTaskState:
    """Tests for TaskState enum."""

    def test_pending(self):
        """PENDING state."""
        assert TaskState.PENDING.value == 1

    def test_queued(self):
        """QUEUED state."""
        assert TaskState.QUEUED.name == "QUEUED"

    def test_running(self):
        """RUNNING state."""
        assert TaskState.RUNNING.name == "RUNNING"

    def test_paused(self):
        """PAUSED state."""
        assert TaskState.PAUSED.name == "PAUSED"

    def test_waiting(self):
        """WAITING state."""
        assert TaskState.WAITING.name == "WAITING"

    def test_completed(self):
        """COMPLETED state."""
        assert TaskState.COMPLETED.name == "COMPLETED"

    def test_failed(self):
        """FAILED state."""
        assert TaskState.FAILED.name == "FAILED"

    def test_cancelled(self):
        """CANCELLED state."""
        assert TaskState.CANCELLED.name == "CANCELLED"

    def test_retrying(self):
        """RETRYING state."""
        assert TaskState.RETRYING.name == "RETRYING"


# =============================================================================
# Tests for TaskPriority Enum
# =============================================================================


class TestTaskPriority:
    """Tests for TaskPriority enum."""

    def test_critical(self):
        """CRITICAL is 0."""
        assert TaskPriority.CRITICAL.value == 0

    def test_high(self):
        """HIGH is 1."""
        assert TaskPriority.HIGH.value == 1

    def test_medium(self):
        """MEDIUM is 2."""
        assert TaskPriority.MEDIUM.value == 2

    def test_low(self):
        """LOW is 3."""
        assert TaskPriority.LOW.value == 3

    def test_background(self):
        """BACKGROUND is 4."""
        assert TaskPriority.BACKGROUND.value == 4


# =============================================================================
# Tests for TaskTransition Enum
# =============================================================================


class TestTaskTransition:
    """Tests for TaskTransition enum."""

    def test_start(self):
        """START transition."""
        assert TaskTransition.START.name == "START"

    def test_complete(self):
        """COMPLETE transition."""
        assert TaskTransition.COMPLETE.name == "COMPLETE"

    def test_fail(self):
        """FAIL transition."""
        assert TaskTransition.FAIL.name == "FAIL"

    def test_cancel(self):
        """CANCEL transition."""
        assert TaskTransition.CANCEL.name == "CANCEL"

    def test_pause(self):
        """PAUSE transition."""
        assert TaskTransition.PAUSE.name == "PAUSE"

    def test_resume(self):
        """RESUME transition."""
        assert TaskTransition.RESUME.name == "RESUME"

    def test_retry(self):
        """RETRY transition."""
        assert TaskTransition.RETRY.name == "RETRY"


# =============================================================================
# Tests for VALID_TRANSITIONS
# =============================================================================


class TestValidTransitions:
    """Tests for VALID_TRANSITIONS constant."""

    def test_pending_transitions(self):
        """PENDING can go to QUEUED or CANCELLED."""
        assert TaskState.QUEUED in VALID_TRANSITIONS[TaskState.PENDING]
        assert TaskState.CANCELLED in VALID_TRANSITIONS[TaskState.PENDING]

    def test_queued_transitions(self):
        """QUEUED can go to RUNNING or CANCELLED."""
        assert TaskState.RUNNING in VALID_TRANSITIONS[TaskState.QUEUED]
        assert TaskState.CANCELLED in VALID_TRANSITIONS[TaskState.QUEUED]

    def test_running_transitions(self):
        """RUNNING can go to multiple states."""
        valid = VALID_TRANSITIONS[TaskState.RUNNING]
        assert TaskState.COMPLETED in valid
        assert TaskState.FAILED in valid
        assert TaskState.PAUSED in valid
        assert TaskState.WAITING in valid
        assert TaskState.CANCELLED in valid

    def test_completed_is_terminal(self):
        """COMPLETED is terminal state."""
        assert len(VALID_TRANSITIONS[TaskState.COMPLETED]) == 0

    def test_cancelled_is_terminal(self):
        """CANCELLED is terminal state."""
        assert len(VALID_TRANSITIONS[TaskState.CANCELLED]) == 0

    def test_failed_transitions(self):
        """FAILED can retry or cancel."""
        assert TaskState.RETRYING in VALID_TRANSITIONS[TaskState.FAILED]
        assert TaskState.CANCELLED in VALID_TRANSITIONS[TaskState.FAILED]


# =============================================================================
# Tests for TaskResult Dataclass
# =============================================================================


class TestTaskResult:
    """Tests for TaskResult dataclass."""

    def test_success(self):
        """Create successful result."""
        result = TaskResult(success=True, output="done")
        assert result.success is True
        assert result.output == "done"
        assert result.error is None

    def test_failure(self):
        """Create failed result."""
        result = TaskResult(success=False, error="failed")
        assert result.success is False
        assert result.error == "failed"

    def test_with_metadata(self):
        """Result with metadata."""
        result = TaskResult(success=True, metadata={"key": "value"})
        assert result.metadata == {"key": "value"}

    def test_default_metadata(self):
        """Default metadata is empty dict."""
        result = TaskResult(success=True)
        assert result.metadata == {}

    def test_duration(self):
        """Result with duration."""
        result = TaskResult(success=True, duration=1.5)
        assert result.duration == 1.5


# =============================================================================
# Tests for Task Dataclass
# =============================================================================


class TestTask:
    """Tests for Task dataclass."""

    def test_create_minimal(self):
        """Create task with minimal params."""
        task = Task(id="t1", name="Test Task")
        assert task.id == "t1"
        assert task.name == "Test Task"
        assert task.state == TaskState.PENDING
        assert task.priority == TaskPriority.MEDIUM

    def test_auto_generate_id(self):
        """ID generated if empty."""
        task = Task(id="", name="Test")
        assert len(task.id) == 8

    def test_can_transition_valid(self):
        """Valid transition check."""
        task = Task(id="t1", name="Test")
        assert task.can_transition_to(TaskState.QUEUED) is True
        assert task.can_transition_to(TaskState.CANCELLED) is True

    def test_can_transition_invalid(self):
        """Invalid transition check."""
        task = Task(id="t1", name="Test")
        assert task.can_transition_to(TaskState.COMPLETED) is False

    def test_transition_to_valid(self):
        """Valid state transition."""
        task = Task(id="t1", name="Test")
        assert task.transition_to(TaskState.QUEUED) is True
        assert task.state == TaskState.QUEUED

    def test_transition_to_invalid(self):
        """Invalid state transition."""
        task = Task(id="t1", name="Test")
        assert task.transition_to(TaskState.COMPLETED) is False
        assert task.state == TaskState.PENDING

    def test_transition_sets_started_at(self):
        """Running transition sets started_at."""
        task = Task(id="t1", name="Test")
        task.transition_to(TaskState.QUEUED)
        task.transition_to(TaskState.RUNNING)
        assert task.started_at is not None

    def test_transition_sets_completed_at(self):
        """Terminal transition sets completed_at."""
        task = Task(id="t1", name="Test")
        task.transition_to(TaskState.QUEUED)
        task.transition_to(TaskState.RUNNING)
        task.transition_to(TaskState.COMPLETED)
        assert task.completed_at is not None

    def test_duration_not_started(self):
        """Duration is None if not started."""
        task = Task(id="t1", name="Test")
        assert task.duration is None

    def test_duration_running(self):
        """Duration while running."""
        task = Task(id="t1", name="Test")
        task.transition_to(TaskState.QUEUED)
        task.transition_to(TaskState.RUNNING)
        time.sleep(0.1)
        assert task.duration is not None
        assert task.duration >= 0.1

    def test_duration_completed(self):
        """Duration after completed."""
        task = Task(id="t1", name="Test")
        task.transition_to(TaskState.QUEUED)
        task.transition_to(TaskState.RUNNING)
        time.sleep(0.1)
        task.transition_to(TaskState.COMPLETED)
        duration = task.duration
        time.sleep(0.1)
        assert task.duration == duration  # Duration fixed

    def test_is_terminal_completed(self):
        """Completed is terminal."""
        task = Task(id="t1", name="Test", state=TaskState.COMPLETED)
        assert task.is_terminal is True

    def test_is_terminal_failed(self):
        """Failed is terminal."""
        task = Task(id="t1", name="Test", state=TaskState.FAILED)
        assert task.is_terminal is True

    def test_is_terminal_cancelled(self):
        """Cancelled is terminal."""
        task = Task(id="t1", name="Test", state=TaskState.CANCELLED)
        assert task.is_terminal is True

    def test_is_terminal_running(self):
        """Running is not terminal."""
        task = Task(id="t1", name="Test", state=TaskState.RUNNING)
        assert task.is_terminal is False

    def test_is_runnable_pending(self):
        """Pending is runnable."""
        task = Task(id="t1", name="Test", state=TaskState.PENDING)
        assert task.is_runnable is True

    def test_is_runnable_queued(self):
        """Queued is runnable."""
        task = Task(id="t1", name="Test", state=TaskState.QUEUED)
        assert task.is_runnable is True

    def test_is_runnable_running(self):
        """Running is not runnable."""
        task = Task(id="t1", name="Test", state=TaskState.RUNNING)
        assert task.is_runnable is False

    def test_get_retry_delay(self):
        """Get retry delay with backoff."""
        task = Task(id="t1", name="Test", retry_delay=1.0, retry_backoff=2.0)
        delay = task.get_retry_delay()
        assert 0.8 <= delay <= 1.2  # Base delay with jitter

        task.retry_count = 1
        delay = task.get_retry_delay()
        assert 1.6 <= delay <= 2.4  # 2x with jitter

    def test_should_retry_failed(self):
        """Should retry when failed and retries left."""
        task = Task(id="t1", name="Test", max_retries=3, retry_count=0)
        task.state = TaskState.FAILED
        assert task.should_retry() is True

    def test_should_retry_max_reached(self):
        """Should not retry when max reached."""
        task = Task(id="t1", name="Test", max_retries=3, retry_count=3)
        task.state = TaskState.FAILED
        assert task.should_retry() is False

    def test_should_retry_not_failed(self):
        """Should not retry if not failed."""
        task = Task(id="t1", name="Test", max_retries=3)
        task.state = TaskState.RUNNING
        assert task.should_retry() is False


# =============================================================================
# Tests for TaskManager
# =============================================================================


class TestTaskManager:
    """Tests for TaskManager class."""

    def test_init(self):
        """Initialize manager."""
        manager = TaskManager()
        assert manager.tasks == {}
        assert manager.task_order == []

    def test_create_task(self):
        """Create a task."""
        manager = TaskManager()
        task = manager.create_task("Test Task", description="A test")
        assert task.name == "Test Task"
        assert task.description == "A test"
        assert task.id in manager.tasks

    def test_create_task_with_handler(self):
        """Create task with handler."""
        manager = TaskManager()

        def my_handler():
            return "done"

        task = manager.create_task("Test", handler=my_handler)
        assert task.handler == my_handler

    def test_create_task_with_dependencies(self):
        """Create task with dependencies."""
        manager = TaskManager()
        t1 = manager.create_task("Task 1")
        t2 = manager.create_task("Task 2", dependencies=[t1.id])
        assert t1.id in t2.dependencies
        assert t2.id in t1.dependents

    def test_get_task(self):
        """Get task by ID."""
        manager = TaskManager()
        task = manager.create_task("Test")
        assert manager.get_task(task.id) == task

    def test_get_task_not_found(self):
        """Get non-existent task."""
        manager = TaskManager()
        assert manager.get_task("unknown") is None

    def test_get_tasks_by_state(self):
        """Get tasks by state."""
        manager = TaskManager()
        t1 = manager.create_task("T1")
        t2 = manager.create_task("T2")
        t1.state = TaskState.RUNNING
        pending = manager.get_tasks_by_state(TaskState.PENDING)
        assert len(pending) == 1
        assert t2 in pending

    def test_get_runnable_tasks(self):
        """Get runnable tasks."""
        manager = TaskManager()
        t1 = manager.create_task("T1")
        t2 = manager.create_task("T2")
        t1.state = TaskState.RUNNING
        runnable = manager.get_runnable_tasks()
        assert len(runnable) == 1
        assert t2 in runnable

    def test_get_runnable_tasks_sorted_by_priority(self):
        """Runnable tasks sorted by priority."""
        manager = TaskManager()
        t1 = manager.create_task("T1", priority=TaskPriority.LOW)
        t2 = manager.create_task("T2", priority=TaskPriority.HIGH)
        runnable = manager.get_runnable_tasks()
        assert runnable[0] == t2  # HIGH first
        assert runnable[1] == t1

    def test_get_runnable_tasks_with_dependencies(self):
        """Runnable excludes tasks with unsatisfied deps."""
        manager = TaskManager()
        t1 = manager.create_task("T1")
        t2 = manager.create_task("T2", dependencies=[t1.id])
        runnable = manager.get_runnable_tasks()
        assert t1 in runnable
        assert t2 not in runnable

    def test_dependencies_satisfied(self):
        """Check dependencies satisfied."""
        manager = TaskManager()
        t1 = manager.create_task("T1")
        t2 = manager.create_task("T2", dependencies=[t1.id])
        assert manager._dependencies_satisfied(t2) is False
        t1.state = TaskState.COMPLETED
        assert manager._dependencies_satisfied(t2) is True

    def test_transition_task(self):
        """Transition task state."""
        manager = TaskManager()
        task = manager.create_task("Test")
        assert manager.transition_task(task.id, TaskState.QUEUED) is True
        assert task.state == TaskState.QUEUED

    def test_transition_task_invalid(self):
        """Invalid transition returns False."""
        manager = TaskManager()
        task = manager.create_task("Test")
        assert manager.transition_task(task.id, TaskState.COMPLETED) is False

    def test_transition_task_not_found(self):
        """Transition unknown task."""
        manager = TaskManager()
        assert manager.transition_task("unknown", TaskState.QUEUED) is False

    def test_start_task(self):
        """Start a task."""
        manager = TaskManager()
        task = manager.create_task("Test")
        assert manager.start_task(task.id) is True
        assert task.state == TaskState.RUNNING

    def test_start_task_not_found(self):
        """Start unknown task."""
        manager = TaskManager()
        assert manager.start_task("unknown") is False

    def test_complete_task(self):
        """Complete a task."""
        manager = TaskManager()
        task = manager.create_task("Test")
        manager.start_task(task.id)
        assert manager.complete_task(task.id, "result") is True
        assert task.state == TaskState.COMPLETED
        assert task.result.success is True
        assert task.result.output == "result"

    def test_complete_task_not_found(self):
        """Complete unknown task."""
        manager = TaskManager()
        assert manager.complete_task("unknown") is False

    def test_fail_task(self):
        """Fail a task."""
        manager = TaskManager()
        task = manager.create_task("Test")
        manager.start_task(task.id)
        assert manager.fail_task(task.id, "error msg") is True
        assert task.state == TaskState.FAILED
        assert task.result.success is False
        assert task.result.error == "error msg"
        assert "error msg" in task.error_history

    def test_fail_task_not_found(self):
        """Fail unknown task."""
        manager = TaskManager()
        assert manager.fail_task("unknown", "error") is False

    def test_retry_task(self):
        """Retry a failed task."""
        manager = TaskManager()
        task = manager.create_task("Test", max_retries=3)
        manager.start_task(task.id)
        manager.fail_task(task.id, "error")
        assert manager.retry_task(task.id) is True
        assert task.state == TaskState.RUNNING
        assert task.retry_count == 1

    def test_retry_task_max_reached(self):
        """Cannot retry when max reached."""
        manager = TaskManager()
        task = manager.create_task("Test")
        task.max_retries = 0  # Set directly on task
        manager.start_task(task.id)
        manager.fail_task(task.id, "error")
        assert manager.retry_task(task.id) is False

    def test_retry_task_not_found(self):
        """Retry unknown task."""
        manager = TaskManager()
        assert manager.retry_task("unknown") is False

    def test_share_data(self):
        """Share data between tasks."""
        manager = TaskManager()
        manager.share_data("key", "value")
        assert manager.get_shared_data("key") == "value"

    def test_get_shared_data_default(self):
        """Get shared data with default."""
        manager = TaskManager()
        assert manager.get_shared_data("unknown", "default") == "default"

    def test_pass_result_to_dependents(self):
        """Pass result to dependent tasks."""
        manager = TaskManager()
        t1 = manager.create_task("T1")
        t2 = manager.create_task("T2", dependencies=[t1.id])
        manager.start_task(t1.id)
        manager.complete_task(t1.id, "t1_result")
        manager.pass_result_to_dependents(t1.id)
        assert t2.shared_data.get(f"result_from_{t1.id}") == "t1_result"

    def test_pass_result_to_dependents_no_result(self):
        """Pass result when no result."""
        manager = TaskManager()
        t1 = manager.create_task("T1")
        manager.pass_result_to_dependents(t1.id)  # Should not raise

    def test_update_progress(self):
        """Update task progress."""
        manager = TaskManager()
        task = manager.create_task("Test")
        manager.update_progress(task.id, 0.5, "Halfway")
        assert task.progress == 0.5
        assert task.progress_message == "Halfway"

    def test_update_progress_clamps(self):
        """Progress clamped to 0-1."""
        manager = TaskManager()
        task = manager.create_task("Test")
        manager.update_progress(task.id, 1.5)
        assert task.progress == 1.0
        manager.update_progress(task.id, -0.5)
        assert task.progress == 0.0

    def test_get_overall_progress_empty(self):
        """Overall progress with no tasks."""
        manager = TaskManager()
        assert manager.get_overall_progress() == 0.0

    def test_get_overall_progress(self):
        """Overall progress calculation."""
        manager = TaskManager()
        t1 = manager.create_task("T1")
        t2 = manager.create_task("T2")
        t1.state = TaskState.COMPLETED
        t2.state = TaskState.RUNNING
        t2.progress = 0.5
        assert manager.get_overall_progress() == 0.75

    def test_add_listener(self):
        """Add state change listener."""
        manager = TaskManager()
        listener_called = []

        def listener(task, old, new):
            listener_called.append((task.id, old, new))

        manager.add_listener(listener)
        task = manager.create_task("Test")
        manager.transition_task(task.id, TaskState.QUEUED)
        assert len(listener_called) == 1
        assert listener_called[0][2] == TaskState.QUEUED

    def test_listener_error_ignored(self):
        """Listener errors don't affect task management."""
        manager = TaskManager()

        def bad_listener(task, old, new):
            raise Exception("Listener error")

        manager.add_listener(bad_listener)
        task = manager.create_task("Test")
        manager.transition_task(task.id, TaskState.QUEUED)
        assert task.state == TaskState.QUEUED

    @pytest.mark.asyncio
    async def test_execute_task(self):
        """Execute a task."""
        manager = TaskManager()

        def handler(**kwargs):
            return "done"

        task = manager.create_task("Test", handler=handler)
        result = await manager.execute_task(task.id)
        assert result.success is True
        assert result.output == "done"

    @pytest.mark.asyncio
    async def test_execute_task_not_found(self):
        """Execute unknown task."""
        manager = TaskManager()
        result = await manager.execute_task("unknown")
        assert result.success is False

    @pytest.mark.asyncio
    async def test_execute_task_no_handler(self):
        """Execute task without handler."""
        manager = TaskManager()
        task = manager.create_task("Test")
        result = await manager.execute_task(task.id)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_task_async_handler(self):
        """Execute task with async handler."""
        manager = TaskManager()

        async def handler(**kwargs):
            await asyncio.sleep(0.01)
            return "async done"

        task = manager.create_task("Test", handler=handler)
        result = await manager.execute_task(task.id)
        assert result.success is True
        assert result.output == "async done"

    @pytest.mark.asyncio
    async def test_execute_task_with_error(self):
        """Execute task that fails."""
        manager = TaskManager()

        def handler(**kwargs):
            raise Exception("Task error")

        task = manager.create_task("Test", handler=handler)
        task.max_retries = 0  # No retries
        result = await manager.execute_task(task.id)
        assert result.success is False
        assert "Task error" in result.error

    @pytest.mark.asyncio
    async def test_execute_all_sequential(self):
        """Execute all tasks sequentially."""
        manager = TaskManager()
        order = []

        def make_handler(name):
            def handler(**kwargs):
                order.append(name)
                return name

            return handler

        manager.create_task("T1", handler=make_handler("T1"))
        manager.create_task("T2", handler=make_handler("T2"))

        results = await manager.execute_all(parallel=False)
        assert len(results) == 2
        assert order == ["T1", "T2"]

    @pytest.mark.asyncio
    async def test_execute_all_parallel(self):
        """Execute all tasks in parallel."""
        manager = TaskManager()

        def handler(**kwargs):
            return "done"

        manager.create_task("T1", handler=handler)
        manager.create_task("T2", handler=handler)

        results = await manager.execute_all(parallel=True)
        assert len(results) == 2


# =============================================================================
# Tests for TaskProgressDisplay
# =============================================================================


class TestTaskProgressDisplay:
    """Tests for TaskProgressDisplay class."""

    def test_init(self):
        """Initialize display."""
        display = TaskProgressDisplay()
        assert display.console is not None

    def test_init_custom_console(self):
        """Initialize with custom console."""
        mock_console = MagicMock()
        display = TaskProgressDisplay(console=mock_console)
        assert display.console == mock_console

    def test_create_progress(self):
        """Create progress display."""
        display = TaskProgressDisplay()
        progress = display.create_progress()
        assert progress is not None

    def test_start(self):
        """Start progress display."""
        display = TaskProgressDisplay()
        tasks = [
            Task(id="t1", name="Task 1"),
            Task(id="t2", name="Task 2"),
        ]
        live = display.start(tasks)
        assert live is not None
        assert "t1" in display._task_ids

    def test_update(self):
        """Update task in progress."""
        display = TaskProgressDisplay()
        task = Task(id="t1", name="Test", state=TaskState.RUNNING)
        task.progress = 0.5
        display.start([task])
        display.update(task)  # Should not raise

    def test_update_no_progress(self):
        """Update without progress started."""
        display = TaskProgressDisplay()
        task = Task(id="t1", name="Test")
        display.update(task)  # Should not raise

    def test_render_summary(self):
        """Render task summary."""
        display = TaskProgressDisplay()
        manager = TaskManager()
        t1 = manager.create_task("T1")
        t2 = manager.create_task("T2")
        manager.start_task(t1.id)
        manager.complete_task(t1.id)
        manager.start_task(t2.id)
        manager.fail_task(t2.id, "error")

        display.render_summary(manager)  # Should not raise


# =============================================================================
# Tests for RetryHandler
# =============================================================================


class TestRetryHandler:
    """Tests for RetryHandler class."""

    def test_init(self):
        """Initialize handler."""
        handler = RetryHandler(max_retries=5)
        assert handler.max_retries == 5

    def test_init_defaults(self):
        """Default values."""
        handler = RetryHandler()
        assert handler.max_retries == 3
        assert handler.base_delay == 1.0
        assert handler.max_delay == 60.0
        assert handler.backoff_factor == 2.0

    def test_calculate_delay_first_attempt(self):
        """First attempt delay."""
        handler = RetryHandler(base_delay=1.0, jitter=0)
        delay = handler.calculate_delay(0)
        assert delay == 1.0

    def test_calculate_delay_exponential(self):
        """Exponential backoff."""
        handler = RetryHandler(base_delay=1.0, backoff_factor=2.0, jitter=0)
        assert handler.calculate_delay(0) == 1.0
        assert handler.calculate_delay(1) == 2.0
        assert handler.calculate_delay(2) == 4.0

    def test_calculate_delay_max_cap(self):
        """Delay capped at max."""
        handler = RetryHandler(base_delay=10.0, max_delay=15.0, jitter=0)
        assert handler.calculate_delay(2) == 15.0

    def test_calculate_delay_with_jitter(self):
        """Delay has jitter."""
        handler = RetryHandler(base_delay=10.0, jitter=0.2)
        delay = handler.calculate_delay(0)
        assert 8.0 <= delay <= 12.0

    def test_should_retry_under_max(self):
        """Should retry under max attempts."""
        handler = RetryHandler(max_retries=3)
        assert handler.should_retry(0, Exception("timeout")) is True
        assert handler.should_retry(2, Exception("timeout")) is True

    def test_should_retry_at_max(self):
        """Should not retry at max attempts."""
        handler = RetryHandler(max_retries=3)
        assert handler.should_retry(3, Exception("timeout")) is False

    def test_should_retry_authentication_error(self):
        """Should not retry authentication errors."""
        handler = RetryHandler(max_retries=3)
        assert handler.should_retry(0, Exception("authentication failed")) is False

    def test_should_retry_authorization_error(self):
        """Should not retry authorization errors."""
        handler = RetryHandler(max_retries=3)
        assert handler.should_retry(0, Exception("authorization required")) is False

    def test_should_retry_permission_denied(self):
        """Should not retry permission denied."""
        handler = RetryHandler(max_retries=3)
        assert handler.should_retry(0, Exception("permission denied")) is False

    def test_should_retry_invalid_api_key(self):
        """Should not retry invalid API key."""
        handler = RetryHandler(max_retries=3)
        assert handler.should_retry(0, Exception("invalid api key")) is False

    def test_should_retry_not_found(self):
        """Should not retry not found."""
        handler = RetryHandler(max_retries=3)
        assert handler.should_retry(0, Exception("resource not found")) is False

    @pytest.mark.asyncio
    async def test_execute_with_retry_success(self):
        """Execute with retry - success."""
        handler = RetryHandler()

        def func():
            return "done"

        result = await handler.execute_with_retry(func)
        assert result == "done"

    @pytest.mark.asyncio
    async def test_execute_with_retry_async(self):
        """Execute with retry - async function."""
        handler = RetryHandler()

        async def func():
            return "async done"

        result = await handler.execute_with_retry(func)
        assert result == "async done"

    @pytest.mark.asyncio
    async def test_execute_with_retry_retries(self):
        """Execute with retry - retries on failure."""
        handler = RetryHandler(max_retries=3, base_delay=0.01)
        attempts = [0]

        def func():
            attempts[0] += 1
            if attempts[0] < 3:
                raise Exception("transient error")
            return "done"

        result = await handler.execute_with_retry(func)
        assert result == "done"
        assert attempts[0] == 3

    @pytest.mark.asyncio
    async def test_execute_with_retry_callback(self):
        """Execute with retry - callback called."""
        handler = RetryHandler(max_retries=3, base_delay=0.01)
        retries = []

        def on_retry(attempt, error, delay):
            retries.append((attempt, str(error)))

        def func():
            if len(retries) < 2:
                raise Exception("transient")
            return "done"

        await handler.execute_with_retry(func, on_retry=on_retry)
        assert len(retries) == 2

    @pytest.mark.asyncio
    async def test_execute_with_retry_non_retryable(self):
        """Execute with retry - non-retryable error."""
        handler = RetryHandler(max_retries=3)

        def func():
            raise Exception("authentication failed")

        with pytest.raises(Exception) as exc:
            await handler.execute_with_retry(func)
        assert "authentication" in str(exc.value)

    @pytest.mark.asyncio
    async def test_execute_with_retry_exhausted(self):
        """Execute with retry - exhausts retries."""
        handler = RetryHandler(max_retries=2, base_delay=0.01)

        def func():
            raise Exception("transient error")

        with pytest.raises(Exception):
            await handler.execute_with_retry(func)


# =============================================================================
# Tests for Convenience Functions
# =============================================================================


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_task_manager(self):
        """Create task manager."""
        manager = create_task_manager()
        assert isinstance(manager, TaskManager)

    def test_create_progress_display(self):
        """Create progress display."""
        display = create_progress_display()
        assert isinstance(display, TaskProgressDisplay)

    def test_create_progress_display_with_console(self):
        """Create progress display with console."""
        mock_console = MagicMock()
        display = create_progress_display(mock_console)
        assert display.console == mock_console
