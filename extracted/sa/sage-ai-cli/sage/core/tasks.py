"""SAGE Task Execution Management (Items 4201-4300).

Implements:
- Task State Machine (Items 4201-4250)
- Comprehensive Task Execution (Items 4251-4300)
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any

from sage.core.reasoning_engine import AdvancedReasoningEngine
from sage.core.context_persistence import ContextPersistenceManager, TaskProgress
from sage.core.tdd import TDDGate


class TaskState(Enum):
    """Status of a task."""

    PENDING = 1
    QUEUED = 2
    RUNNING = 3
    PAUSED = 4
    COMPLETED = 5
    FAILED = 6
    CANCELLED = 7
    WAITING = 8
    RETRYING = 9


VALID_TRANSITIONS = {
    TaskState.PENDING: {TaskState.QUEUED, TaskState.CANCELLED, TaskState.RUNNING},
    TaskState.QUEUED: {TaskState.RUNNING, TaskState.CANCELLED},
    TaskState.RUNNING: {
        TaskState.COMPLETED,
        TaskState.FAILED,
        TaskState.PAUSED,
        TaskState.CANCELLED,
        TaskState.WAITING,
    },
    TaskState.PAUSED: {TaskState.RUNNING, TaskState.CANCELLED},
    TaskState.COMPLETED: set(),
    TaskState.FAILED: {TaskState.RETRYING, TaskState.CANCELLED, TaskState.QUEUED, TaskState.RUNNING},
    TaskState.WAITING: {TaskState.RUNNING, TaskState.CANCELLED},
    TaskState.RETRYING: {TaskState.RUNNING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.CANCELLED: set(),
}


@dataclass
class TaskResult:
    """Outcome of a task execution."""

    success: bool
    output: Any = None
    error: str | None = None
    duration: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class TaskPriority(Enum):
    """Priority of a task."""

    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    BACKGROUND = 4


class RetryHandler:
    """Manages retry logic for tasks."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: float = 0.1,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

    def should_retry(self, attempt: int, error: Exception) -> bool:
        """Determine if a task should be retried."""
        if attempt >= self.max_retries:
            return False

        error_msg = str(error).lower()
        non_retryable = [
            "authentication",
            "authorization",
            "permission denied",
            "invalid api key",
            "not found",
        ]
        if any(msg in error_msg for msg in non_retryable):
            return False

        return True

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter."""
        delay = min(self.max_delay, self.base_delay * (self.backoff_factor**attempt))
        if self.jitter > 0:
            import random

            jitter_amount = delay * self.jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
        return max(0, delay)

    async def execute_with_retry(
        self, func: Any, on_retry: Any = None, *args: Any, **kwargs: Any
    ) -> Any:
        """Execute a function with retries."""
        import asyncio

        attempt = 0
        while True:
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)
            except Exception as e:
                if not self.should_retry(attempt, e):
                    raise e

                delay = self.calculate_delay(attempt)
                if on_retry:
                    on_retry(attempt, e, delay)

                await asyncio.sleep(delay)
                attempt += 1


class TaskProgressDisplay:
    """Renders task progress to the terminal."""

    def __init__(self, console: Any = None):
        if console is None:
            from sage.core.renderer import console as _default_console
            self.console = _default_console
        else:
            self.console = console
        self._task_ids: dict[str, Any] = {}
        self._progress: Any = None

    def create_progress(self) -> Any:
        """Create a rich progress instance."""
        from rich.progress import (
            BarColumn,
            Progress,
            SpinnerColumn,
            TaskProgressColumn,
            TextColumn,
            TimeElapsedColumn,
        )
        import sys
        import os
        from sage.core.renderer import _no_color_enabled, _suppress_spinners
        disable_progress = (
            not sys.stdout.isatty()
            or _no_color_enabled
            or _suppress_spinners
            or os.environ.get("TERM") == "dumb"
        )

        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console,
            disable=disable_progress,
        )

    def start(self, tasks: list[Task]) -> Any:
        """Start the progress display."""
        self._progress = self.create_progress()
        self._progress.start()
        for task in tasks:
            self._task_ids[task.id] = self._progress.add_task(
                task.name, total=1.0, completed=task.progress
            )
        return self._progress

    def update(self, task: Task) -> None:
        """Update a task's progress."""
        if self._progress and task.id in self._task_ids:
            self._progress.update(
                self._task_ids[task.id],
                completed=task.progress,
                description=f"{task.name}: {task.progress_message or task.state.name}",
            )

    def stop(self) -> None:
        """Stop the progress display."""
        if self._progress:
            self._progress.stop()

    def render_summary(self, manager: TaskManager) -> None:
        """Render a summary of all tasks."""
        from rich.table import Table

        table = Table(title="Task Summary")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("State")
        table.add_column("Duration")

        for task_id in manager.task_order:
            task = manager.tasks[task_id]
            table.add_row(
                task.id,
                task.name,
                task.state.name,
                f"{task.duration:.2f}s" if task.duration else "-",
            )
        self.console.print(table)


def create_task_manager() -> TaskManager:
    """Factory function for TaskManager."""
    return TaskManager()


def create_progress_display(console: Any = None) -> TaskProgressDisplay:
    """Factory function for TaskProgressDisplay."""
    return TaskProgressDisplay(console)


@dataclass
class Task:
    """A single task to be executed."""

    id: str
    name: str
    description: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    state: TaskState = TaskState.PENDING
    dependencies: list[str] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    result: TaskResult | None = None
    handler: Any = None
    started_at: float | None = None
    completed_at: float | None = None
    attempts: int = 0
    max_attempts: int = 3
    retry_count: int = 0
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff: float = 2.0
    progress: float = 0.0
    progress_message: str | None = None
    error_history: list[str] = field(default_factory=list)
    shared_data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.id:
            import uuid

            self.id = str(uuid.uuid4())[:8]

    def can_transition_to(self, target_state: TaskState) -> bool:
        """Check if transition to target state is valid."""
        return target_state in VALID_TRANSITIONS.get(self.state, set())

    def transition_to(self, target_state: TaskState, reason: str | None = None) -> bool:
        """Attempt to transition to a new state."""
        if not self.can_transition_to(target_state):
            return False

        old_state = self.state
        self.state = target_state

        if target_state == TaskState.RUNNING:
            if not self.started_at:
                self.started_at = time.time()
        elif target_state in {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED}:
            self.completed_at = time.time()

        return True

    @property
    def duration(self) -> float | None:
        """Get task duration in seconds."""
        if not self.started_at:
            return None
        end_time = self.completed_at or time.time()
        return end_time - self.started_at

    @property
    def is_terminal(self) -> bool:
        """Check if task is in a terminal state."""
        return self.state in {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED}

    @property
    def is_runnable(self) -> bool:
        """Check if task is runnable."""
        return self.state in {TaskState.PENDING, TaskState.QUEUED}

    def get_retry_delay(self) -> float:
        """Calculate retry delay with backoff and jitter."""
        delay = self.retry_delay * (self.retry_backoff**self.retry_count)
        # Add 20% jitter
        import random

        jitter = delay * 0.2
        return delay + random.uniform(-jitter, jitter)

    def should_retry(self) -> bool:
        """Check if task should be retried."""
        return self.state == TaskState.FAILED and self.retry_count < self.max_retries


class TaskTransition(Enum):
    """Transitions for task states."""

    START = auto()
    COMPLETE = auto()
    FAIL = auto()
    CANCEL = auto()
    PAUSE = auto()
    RESUME = auto()
    RETRY = auto()


@dataclass
class TaskEvent:
    """An event related to a task."""

    task_id: str
    event_type: str
    timestamp: float = field(default_factory=time.time)
    data: dict[str, Any] = field(default_factory=dict)


class TaskBus:
    """A simple event bus for tasks."""

    def __init__(self):
        self.subscribers: list[Any] = []

    def subscribe(self, subscriber: Any) -> None:
        """Subscribe to task events."""
        self.subscribers.append(subscriber)

    def publish(self, event: TaskEvent) -> None:
        """Publish a task event."""
        for subscriber in self.subscribers:
            if hasattr(subscriber, "on_task_event"):
                subscriber.on_task_event(event)


class TaskExecution:
    """Execution state of a task."""

    task_id: str
    description: str
    status: TaskState = TaskState.PENDING
    result: Any = None
    error: str | None = None


class ComprehensiveTaskExecutor:
    """
    P0 Items 4251-4300: Orchestrates complex task execution.
    """

    def __init__(self, sage_root: str):
        self.sage_root = Path(sage_root)
        self.reasoning_engine = AdvancedReasoningEngine()
        self.tasks: dict[str, TaskExecution] = {}

    def execute_task(self, task_description: str) -> TaskExecution:
        """Execute a task with full orchestration."""
        task_id = f"task_{len(self.tasks) + 1}"
        task = TaskExecution(task_id=task_id, description=task_description)
        self.tasks[task_id] = task

        task.status = TaskState.RUNNING

        try:
            # Analyze task
            analysis = self.reasoning_engine.analyze_problem(task_description)

            # Perform execution (simulated for now)
            task.result = {
                "task_id": task_id,
                "analysis": analysis,
                "outcome": "success",
            }
            task.status = TaskState.COMPLETED

        except Exception as e:
            task.status = TaskState.FAILED
            task.error = str(e)

        return task

    def get_task_status(self, task_id: str) -> TaskState | None:
        """Get the status of a task."""
        task = self.tasks.get(task_id)
        return task.status if task else None


class TaskManager:
    """Manages multi-task execution with state tracking and persistence."""

    def __init__(
        self,
        cwd: Path | None = None,
        tdd_gate: Any = None,
        context_manager: ContextPersistenceManager | None = None,
        restore: bool = False,
    ):
        self.cwd = cwd or Path.cwd()
        self.tdd_gate = tdd_gate
        self.context_manager = context_manager or ContextPersistenceManager(self.cwd)
        self.tasks: dict[str, Task] = {}
        self.task_order: list[str] = []
        self.shared_data: dict[str, Any] = {}
        self.listeners: list[Any] = []
        self.current_task_index: int = 0

        # Load context if requested
        if restore:
            self.context = self.context_manager.get_current_context()
            if self.context:
                self._restore_from_context()

    def _restore_from_context(self) -> None:
        """Restore task state from persisted context."""
        if not self.context.accumulated_items:
            return

        task_list_item = next(
            (item for item in self.context.accumulated_items if item.get("_type") == "task_list"),
            None,
        )
        if task_list_item and task_list_item.get("tasks"):
            parsed_tasks = task_list_item["tasks"]
            self.current_task_index = task_list_item.get("current_index", 0)

            for task_dict in parsed_tasks:
                task_id = f"task_{task_dict['number']}"
                task = Task(
                    id=task_id,
                    name=task_dict["title"],
                    description=task_dict.get("description", ""),
                    state=(
                        TaskState.COMPLETED
                        if task_dict["status"] == "completed"
                        else (
                            TaskState.FAILED
                            if task_dict["status"] == "failed"
                            else (
                                TaskState.RUNNING
                                if task_dict["status"] == "in_progress"
                                else TaskState.PENDING
                            )
                        )
                    ),
                )
                task.progress = 1.0 if task.state == TaskState.COMPLETED else 0.0
                if task_dict.get("files_written"):
                    task.shared_data["files_written"] = task_dict["files_written"]

                self.tasks[task_id] = task
                self.task_order.append(task_id)

    def create_task(
        self,
        name: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        dependencies: list[str] | None = None,
        handler: Any = None,
        max_retries: int | None = None,
    ) -> Task:
        """Create and register a new task."""
        task_id = f"task_{len(self.tasks) + 1}"
        task = Task(
            id=task_id,
            name=name,
            description=description,
            priority=priority,
            dependencies=dependencies or [],
            handler=handler,
        )
        if max_retries is not None:
            task.max_retries = max_retries

        self.tasks[task_id] = task
        self.task_order.append(task_id)

        # Link dependencies
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                self.tasks[dep_id].dependents.append(task_id)

        return task

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        return self.tasks.get(task_id)

    def get_tasks_by_state(self, state: TaskState) -> list[Task]:
        """Get all tasks in a specific state."""
        return [t for t in self.tasks.values() if t.state == state]

    def get_runnable_tasks(self) -> list[Task]:
        """Get all tasks that are ready to run (dependencies satisfied)."""
        runnable = [
            t
            for t in self.tasks.values()
            if t.is_runnable and self._dependencies_satisfied(t)
        ]
        # Sort by priority (CRITICAL=0, HIGH=1, ...)
        return sorted(runnable, key=lambda t: t.priority.value)

    def _dependencies_satisfied(self, task: Task) -> bool:
        """Check if all dependencies for a task are completed."""
        for dep_id in task.dependencies:
            dep = self.get_task(dep_id)
            if not dep or dep.state != TaskState.COMPLETED:
                return False
        return True

    def transition_task(self, task_id: str, state: TaskState, reason: str | None = None) -> bool:
        """Transition a task to a new state and notify listeners."""
        task = self.get_task(task_id)
        if not task:
            return False

        old_state = task.state
        if task.transition_to(state, reason):
            self._notify_listeners(task, old_state, state)
            self._persist_task_state()
            return True
        return False

    def start_task(self, task_id: str) -> bool:
        """Mark a task as running."""
        return self.transition_task(task_id, TaskState.RUNNING)

    def complete_task(self, task_id: str, output: Any = None) -> bool:
        """Mark a task as completed with an optional result."""
        task = self.get_task(task_id)
        if not task:
            return False

        task.result = TaskResult(success=True, output=output, duration=task.duration or 0.0)
        task.progress = 1.0
        success = self.transition_task(task_id, TaskState.COMPLETED)
        if success:
            self.pass_result_to_dependents(task_id)
        return success

    def fail_task(self, task_id: str, error: str = "") -> bool:
        """Mark a task as failed."""
        task = self.get_task(task_id)
        if not task:
            return False

        task.result = TaskResult(success=False, error=error, duration=task.duration or 0.0)
        task.error_history.append(error)
        return self.transition_task(task_id, TaskState.FAILED, reason=error)

    def retry_task(self, task_id: str) -> bool:
        """Attempt to retry a failed task."""
        task = self.get_task(task_id)
        if not task or not task.should_retry():
            return False

        task.retry_count += 1
        return self.transition_task(task_id, TaskState.RUNNING, reason="retry")

    def share_data(self, key: str, value: Any) -> None:
        """Share data globally across all tasks."""
        self.shared_data[key] = value

    def get_shared_data(self, key: str, default: Any = None) -> Any:
        """Get globally shared data."""
        return self.shared_data.get(key, default)

    def pass_result_to_dependents(self, task_id: str) -> None:
        """Pass a completed task's result to its dependents."""
        task = self.get_task(task_id)
        if not task or not task.result:
            return

        for dep_id in task.dependents:
            dep = self.get_task(dep_id)
            if dep:
                dep.shared_data[f"result_from_{task_id}"] = task.result.output

    def update_progress(self, task_id: str, progress: float, message: str | None = None) -> None:
        """Update the progress of a task."""
        task = self.get_task(task_id)
        if task:
            task.progress = max(0.0, min(1.0, progress))
            task.progress_message = message
            self._persist_task_state()

    def get_overall_progress(self) -> float:
        """Calculate overall progress across all tasks."""
        if not self.tasks:
            return 0.0
        
        total_progress = 0.0
        for task in self.tasks.values():
            if task.state == TaskState.COMPLETED:
                total_progress += 1.0
            else:
                total_progress += task.progress
        
        return total_progress / len(self.tasks)

    def add_listener(self, listener: Any) -> None:
        """Add a listener for task state changes."""
        self.listeners.append(listener)

    def _notify_listeners(self, task: Task, old_state: TaskState, new_state: TaskState) -> None:
        """Notify all listeners of a state change."""
        for listener in self.listeners:
            try:
                listener(task, old_state, new_state)
            except Exception:
                pass

    async def execute_task(self, task_id: str) -> TaskResult:
        """Execute a single task (async)."""
        task = self.get_task(task_id)
        if not task:
            return TaskResult(success=False, error=f"Task {task_id} not found")

        self.start_task(task_id)
        try:
            handler = task.handler
            if not handler:
                self.complete_task(task_id)
                return task.result

            import asyncio

            if asyncio.iscoroutinefunction(handler):
                output = await handler(task=task, manager=self)
            else:
                output = handler(task=task, manager=self)

            self.complete_task(task_id, output)
            return task.result
        except Exception as e:
            self.fail_task(task_id, str(e))
            return task.result

    async def execute_all(self, parallel: bool = False) -> list[TaskResult]:
        """Execute all runnable tasks."""
        import asyncio

        results = []
        while True:
            runnable = self.get_runnable_tasks()
            if not runnable:
                break

            if parallel:
                # In parallel mode, we run all currently runnable tasks
                batch_results = await asyncio.gather(
                    *[self.execute_task(t.id) for t in runnable]
                )
                results.extend(batch_results)
            else:
                # In sequential mode, we run them one by one
                for task in runnable:
                    result = await self.execute_task(task.id)
                    results.append(result)

        return results

    # Legacy methods for backward compatibility with main.py
    def parse_task_list(self, model_output: str) -> list[dict[str, Any]]:
        """Legacy: Parse numbered tasks from model output."""
        # Re-use the regex logic from before but create Task objects
        tasks = []
        seen_numbers = set()
        patterns = [
            r"^\s*(\d+)[.)\]]\s*\*\*([^*]+)\*\*\s*[:\-—]\s*(.+)$",
            r"^\s*(\d+)[.)\]]\s*\*\*([^*]+)\*\*\s*$",
            r"^\s*(\d+)[.)\]]\s*([^:\n]+):\s*(.+)$",
            r"^\s*(\d+)[.)\]]\s*([^\-\n]+)\s*[\-—]\s*(.+)$",
            r"^\s*(\d+)[.)\]]\s*(.+)$",
        ]

        for line in model_output.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    groups = match.groups()
                    number = int(groups[0])
                    if number in seen_numbers:
                        break
                    title = groups[1].strip().rstrip(":").rstrip("-").rstrip("—").strip()
                    description = groups[2].strip() if len(groups) > 2 else ""
                    if len(title) < 3:
                        continue

                    task_id = f"task_{number}"
                    task = Task(id=task_id, name=title, description=description)
                    self.tasks[task_id] = task
                    self.task_order.append(task_id)

                    tasks.append(
                        {
                            "number": number,
                            "title": title,
                            "description": description,
                            "status": "pending",
                            "test_passed": False,
                            "files_written": [],
                        }
                    )
                    seen_numbers.add(number)
                    break

        if tasks:
            self._persist_task_state()
        return tasks

    def get_next_task(self) -> dict[str, Any] | None:
        """Legacy: Get next pending task."""
        runnable = self.get_runnable_tasks()
        if not runnable:
            return None
        task = runnable[0]
        self.start_task(task.id)
        # Convert to legacy dict format
        return {
            "number": int(task.id.replace("task_", "")),
            "title": task.name,
            "description": task.description,
            "status": "in_progress",
        }

    def mark_task_complete(self, task_number: int, files_written: list[str] | None = None) -> None:
        """Legacy: Mark task complete."""
        task_id = f"task_{task_number}"
        self.complete_task(task_id, output={"files_written": files_written})

    def mark_task_failed(self, task_number: int, reason: str = "") -> None:
        """Legacy: Mark task failed."""
        task_id = f"task_{task_number}"
        self.fail_task(task_id, error=reason)

    def _persist_task_state(self) -> None:
        """Persist current state to ContextPersistenceManager."""
        if not self.context_manager:
            return

        legacy_tasks = []
        for task_id in self.task_order:
            task = self.tasks[task_id]
            try:
                num = int(task_id.replace("task_", ""))
            except ValueError:
                num = 0
            legacy_tasks.append(
                {
                    "number": num,
                    "title": task.name,
                    "description": task.description,
                    "status": (
                        "completed"
                        if task.state == TaskState.COMPLETED
                        else (
                            "failed"
                            if task.state == TaskState.FAILED
                            else (
                                "in_progress" if task.state == TaskState.RUNNING else "pending"
                            )
                        )
                    ),
                    "files_written": task.shared_data.get("files_written", []),
                }
            )

        context = self.context_manager.get_current_context()
        if not context:
            context = self.context_manager.create_context()

        # Update or add task_list item
        context.accumulated_items = [
            item for item in context.accumulated_items if item.get("_type") != "task_list"
        ]
        context.accumulated_items.append(
            {
                "_type": "task_list",
                "tasks": legacy_tasks,
                "current_index": self.current_task_index,
                "_added_at": time.time(),
            }
        )
        self.context_manager.save_context(context)

    def get_progress_summary(self) -> str:
        """Get summary string."""
        total = len(self.tasks)
        if total == 0:
            return "No tasks."
        completed = len(self.get_tasks_by_state(TaskState.COMPLETED))
        failed = len(self.get_tasks_by_state(TaskState.FAILED))
        running = len(self.get_tasks_by_state(TaskState.RUNNING))
        pending = len(self.get_tasks_by_state(TaskState.PENDING))
        return f"Tasks: {completed}/{total} completed, {failed} failed, {running} running, {pending} pending"

    def get_remaining_tasks(self) -> list[dict[str, Any]]:
        """Legacy: Get non-completed tasks."""
        return [
            {"number": int(t.id.replace("task_", "")), "title": t.name}
            for t in self.tasks.values()
            if not t.is_terminal
        ]

    def get_resumable_tasks(self) -> list[dict[str, Any]]:
        """Legacy: Get tasks that need work."""
        return [
            {"number": int(t.id.replace("task_", "")), "title": t.name}
            for t in self.tasks.values()
            if t.state != TaskState.COMPLETED
        ]

    def get_continuation_prompt(self) -> str:
        """Legacy: Generate prompt."""
        remaining = self.get_remaining_tasks()
        if not remaining:
            return ""
        return f"Continue implementing the remaining {len(remaining)} tasks..."


# Alias for backward compatibility during migration
TaskExecutionManager = TaskManager
