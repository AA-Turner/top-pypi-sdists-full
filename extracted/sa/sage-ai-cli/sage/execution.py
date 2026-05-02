"""Enhanced Task Execution System for SAGE.

This module provides intelligent task execution with:
- Smart retry strategies
- Parallel execution optimization
- Adaptive error recovery
- Progress tracking
- Resource management
"""

from __future__ import annotations

import re
import subprocess
import threading
import time
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, TypeVar

from sage.core.commands import execute_command

T = TypeVar("T")


class RetryStrategy(Enum):
    """Strategies for retrying failed operations."""

    NONE = "none"
    LINEAR = "linear"  # Fixed delay between retries
    EXPONENTIAL = "exponential"  # Exponential backoff
    ADAPTIVE = "adaptive"  # Adapts based on error type
    SMART = "smart"  # Uses error diagnosis to decide


class TaskPriority(Enum):
    """Task priority levels."""

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"  # Added to match swarm.py TaskStatus


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    strategy: RetryStrategy = RetryStrategy.ADAPTIVE
    max_attempts: int = 5
    initial_delay: float = 1.0
    max_delay: float = 30.0
    backoff_factor: float = 2.0
    jitter: bool = True


@dataclass
class ExecutionResult:
    """Result of task execution."""

    success: bool
    output: str
    error: str | None = None
    duration: float = 0.0
    exit_code: int = 0
    attempts: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionTask:
    """A task to be executed."""

    id: str
    description: str
    command: str | Callable[[], Any]
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: list[str] = field(default_factory=list)
    timeout: float = 120.0
    retry_config: RetryConfig | None = None
    status: TaskStatus = TaskStatus.PENDING
    result: ExecutionResult | None = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: str | None = None
    completed_at: str | None = None
    error_history: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: ExecutionTask) -> bool:
        """Compare for priority queue ordering."""
        return self.priority.value < other.priority.value


class SmartRetryHandler:
    """Intelligent retry handling with error-aware decisions."""

    # Error categories and their retry recommendations
    ERROR_CATEGORIES = {
        "transient": {
            "patterns": [
                r"timeout",
                r"connection reset",
                r"temporary failure",
                r"429",
                r"503",
                r"504",
                r"rate limit",
                r"try again",
            ],
            "should_retry": True,
            "delay_factor": 2.0,
            "max_attempts": 5,
        },
        "resource": {
            "patterns": [
                r"out of memory",
                r"disk full",
                r"resource exhausted",
                r"too many open files",
                r"cannot allocate",
            ],
            "should_retry": True,
            "delay_factor": 3.0,
            "max_attempts": 3,
        },
        "syntax": {
            "patterns": [
                r"syntax error",
                r"parse error",
                r"invalid syntax",
                r"unexpected token",
                r"unterminated",
            ],
            "should_retry": False,
            "needs_fix": True,
        },
        "logic": {
            "patterns": [
                r"assertion error",
                r"assertion failed",
                r"expected .* got",
                r"does not equal",
                r"is not equal to",
            ],
            "should_retry": False,
            "needs_fix": True,
        },
        "import": {
            "patterns": [
                r"import error",
                r"module not found",
                r"no module named",
                r"cannot find module",
            ],
            "should_retry": False,
            "needs_fix": True,
        },
        "permission": {
            "patterns": [
                r"permission denied",
                r"access denied",
                r"403",
                r"not authorized",
                r"forbidden",
            ],
            "should_retry": False,
            "needs_escalation": True,
        },
        "not_found": {
            "patterns": [
                r"file not found",
                r"no such file",
                r"404",
                r"does not exist",
                r"not found",
            ],
            "should_retry": False,
            "needs_fix": True,
        },
    }

    def __init__(self):
        self.error_history: dict[str, list[dict]] = {}
        self._lock = threading.Lock()

    def categorize_error(self, error: str) -> dict[str, Any]:
        """Categorize an error and determine retry strategy."""
        error_lower = error.lower()

        for category, info in self.ERROR_CATEGORIES.items():
            for pattern in info["patterns"]:
                if re.search(pattern, error_lower):
                    return {
                        "category": category,
                        **info,
                    }

        # Default: unknown error
        return {
            "category": "unknown",
            "should_retry": True,
            "max_attempts": 2,
            "delay_factor": 1.5,
        }

    def should_retry(
        self,
        error: str,
        attempt: int,
        config: RetryConfig,
    ) -> tuple[bool, float]:
        """Determine if we should retry and with what delay.

        Returns (should_retry, delay_seconds).
        """
        categorization = self.categorize_error(error)

        if not categorization.get("should_retry", False):
            return False, 0.0

        max_attempts = min(
            config.max_attempts,
            categorization.get("max_attempts", config.max_attempts),
        )

        if attempt >= max_attempts:
            return False, 0.0

        # Calculate delay based on strategy
        if config.strategy == RetryStrategy.NONE:
            return False, 0.0

        elif config.strategy == RetryStrategy.LINEAR:
            delay = config.initial_delay

        elif config.strategy == RetryStrategy.EXPONENTIAL:
            delay = config.initial_delay * (config.backoff_factor ** (attempt - 1))

        elif config.strategy in (RetryStrategy.ADAPTIVE, RetryStrategy.SMART):
            base_delay = config.initial_delay * (config.backoff_factor ** (attempt - 1))
            category_factor = categorization.get("delay_factor", 1.0)
            delay = base_delay * category_factor

        else:
            delay = config.initial_delay

        # Apply max delay cap
        delay = min(delay, config.max_delay)

        # Add jitter to prevent thundering herd
        if config.jitter:
            import random

            jitter = random.uniform(0.8, 1.2)
            delay *= jitter

        return True, delay

    def record_error(self, task_id: str, error: str, attempt: int) -> None:
        """Record an error for learning."""
        with self._lock:
            if task_id not in self.error_history:
                self.error_history[task_id] = []
            self.error_history[task_id].append(
                {
                    "error": error,
                    "attempt": attempt,
                    "timestamp": datetime.now().isoformat(),
                    "category": self.categorize_error(error)["category"],
                }
            )

    def get_error_summary(self, task_id: str) -> str:
        """Get a summary of errors for a task."""
        with self._lock:
            history = self.error_history.get(task_id, [])
            if not history:
                return "No errors recorded"

            categories = {}
            for entry in history:
                cat = entry["category"]
                categories[cat] = categories.get(cat, 0) + 1

            lines = [f"Total errors: {len(history)}"]
            for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
                lines.append(f"  {cat}: {count}")

            return "\n".join(lines)


class ParallelExecutor:
    """Executes tasks in parallel with dependency awareness."""

    def __init__(
        self,
        max_workers: int = 4,
        resource_limits: dict[str, int] | None = None,
    ):
        self.max_workers = max_workers
        self.resource_limits = resource_limits or {}
        self._executor: ThreadPoolExecutor | None = None
        self._task_futures: dict[str, Future] = {}
        self._completed_tasks: dict[str, ExecutionResult] = {}
        self._lock = threading.Lock()
        self._resource_semaphores: dict[str, threading.Semaphore] = {}

        # Initialize resource semaphores
        for resource, limit in self.resource_limits.items():
            self._resource_semaphores[resource] = threading.Semaphore(limit)

    def execute_batch(
        self,
        tasks: list[ExecutionTask],
        progress_callback: Callable[[str, TaskStatus], None] | None = None,
    ) -> dict[str, ExecutionResult]:
        """Execute a batch of tasks respecting dependencies.

        Returns dict mapping task_id to ExecutionResult.
        """
        if not tasks:
            return {}

        results: dict[str, ExecutionResult] = {}
        pending = {t.id: t for t in tasks}
        completed: set[str] = set()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while pending:
                # Find tasks that can run (dependencies met)
                ready = []
                for task_id, task in list(pending.items()):
                    if all(dep in completed for dep in task.dependencies):
                        # Check if dependencies succeeded
                        deps_failed = [
                            dep
                            for dep in task.dependencies
                            if results.get(dep) and not results[dep].success
                        ]
                        if deps_failed:
                            # Mark as blocked due to failed dependency
                            task.status = TaskStatus.BLOCKED
                            task.result = ExecutionResult(
                                success=False,
                                output="",
                                error=f"Blocked by failed dependencies: {deps_failed}",
                            )
                            results[task_id] = task.result
                            completed.add(task_id)
                            del pending[task_id]
                            if progress_callback:
                                progress_callback(task_id, TaskStatus.BLOCKED)
                        else:
                            ready.append(task)

                if not ready:
                    # No tasks ready - check for cycles or deadlock
                    if pending:
                        # Force break - mark remaining as blocked
                        for task_id, task in pending.items():
                            task.status = TaskStatus.BLOCKED
                            task.result = ExecutionResult(
                                success=False,
                                output="",
                                error="Dependency cycle or deadlock detected",
                            )
                            results[task_id] = task.result
                            if progress_callback:
                                progress_callback(task_id, TaskStatus.BLOCKED)
                    break

                # Submit ready tasks
                futures: dict[Future, ExecutionTask] = {}
                for task in ready:
                    task.status = TaskStatus.QUEUED
                    del pending[task.id]
                    future = executor.submit(self._execute_single, task)
                    futures[future] = task
                    if progress_callback:
                        progress_callback(task.id, TaskStatus.QUEUED)

                # Wait for batch to complete
                for future in as_completed(futures):
                    task = futures[future]
                    try:
                        result = future.result()
                        task.result = result
                        task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
                    except Exception as e:
                        task.result = ExecutionResult(
                            success=False,
                            output="",
                            error=str(e),
                        )
                        task.status = TaskStatus.FAILED

                    results[task.id] = task.result
                    completed.add(task.id)
                    if progress_callback:
                        progress_callback(task.id, task.status)

        return results

    def _execute_single(self, task: ExecutionTask) -> ExecutionResult:
        """Execute a single task with retry handling."""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now().isoformat()

        retry_handler = SmartRetryHandler()
        retry_config = task.retry_config or RetryConfig()

        attempt = 1
        last_error: str | None = None

        while attempt <= retry_config.max_attempts:
            try:
                start_time = time.time()

                if callable(task.command):
                    # Execute function
                    output = task.command()
                    result = ExecutionResult(
                        success=True,
                        output=str(output) if output else "",
                        duration=time.time() - start_time,
                        attempts=attempt,
                    )
                else:
                    # Execute shell command using safe execution (P0-10-15)
                    cmd_result = execute_command(
                        task.command,
                        cwd=None,  # Use default
                        timeout=task.timeout,
                        allow_shell=True,  # Task commands may need shell
                        validate=False,  # Task execution handles validation
                    )
                    result = ExecutionResult(
                        success=cmd_result.success,
                        output=cmd_result.stdout,
                        error=cmd_result.stderr if not cmd_result.success else None,
                        duration=time.time() - start_time,
                        exit_code=cmd_result.returncode,
                        attempts=attempt,
                    )

                if result.success:
                    task.completed_at = datetime.now().isoformat()
                    return result

                # Command failed - check if we should retry
                last_error = result.error or "Command failed"
                task.error_history.append(last_error)
                retry_handler.record_error(task.id, last_error, attempt)

                should_retry, delay = retry_handler.should_retry(last_error, attempt, retry_config)

                if not should_retry:
                    return result

                task.status = TaskStatus.RETRYING
                time.sleep(delay)
                attempt += 1

            except subprocess.TimeoutExpired:
                last_error = f"Command timed out after {task.timeout}s"
                task.error_history.append(last_error)
                retry_handler.record_error(task.id, last_error, attempt)

                should_retry, delay = retry_handler.should_retry(last_error, attempt, retry_config)

                if not should_retry:
                    return ExecutionResult(
                        success=False,
                        output="",
                        error=last_error,
                        duration=task.timeout,
                        attempts=attempt,
                    )

                task.status = TaskStatus.RETRYING
                time.sleep(delay)
                attempt += 1

            except Exception as e:
                last_error = str(e)
                task.error_history.append(last_error)
                retry_handler.record_error(task.id, last_error, attempt)

                should_retry, delay = retry_handler.should_retry(last_error, attempt, retry_config)

                if not should_retry:
                    return ExecutionResult(
                        success=False,
                        output="",
                        error=last_error,
                        attempts=attempt,
                    )

                task.status = TaskStatus.RETRYING
                time.sleep(delay)
                attempt += 1

        # Max retries exceeded
        return ExecutionResult(
            success=False,
            output="",
            error=f"Max retries ({retry_config.max_attempts}) exceeded. Last error: {last_error}",
            attempts=attempt - 1,
        )


class TaskScheduler:
    """Schedules and manages task execution."""

    def __init__(
        self,
        max_workers: int = 4,
        executor: ParallelExecutor | None = None,
    ):
        self.max_workers = max_workers
        self.executor = executor or ParallelExecutor(max_workers=max_workers)
        self.task_queue: PriorityQueue[tuple[int, str, ExecutionTask]] = PriorityQueue()
        self.tasks: dict[str, ExecutionTask] = {}
        self.results: dict[str, ExecutionResult] = {}
        self._lock = threading.Lock()
        self._running = False
        self._worker_thread: threading.Thread | None = None

    def add_task(self, task: ExecutionTask) -> str:
        """Add a task to the scheduler."""
        with self._lock:
            self.tasks[task.id] = task
            # Priority queue entry: (priority_value, task_id, task)
            self.task_queue.put((task.priority.value, task.id, task))
        return task.id

    def add_tasks(self, tasks: list[ExecutionTask]) -> list[str]:
        """Add multiple tasks to the scheduler."""
        return [self.add_task(task) for task in tasks]

    def get_task_status(self, task_id: str) -> TaskStatus | None:
        """Get the status of a task."""
        with self._lock:
            task = self.tasks.get(task_id)
            return task.status if task else None

    def get_result(self, task_id: str) -> ExecutionResult | None:
        """Get the result of a completed task."""
        with self._lock:
            return self.results.get(task_id)

    def execute_all(
        self,
        progress_callback: Callable[[str, TaskStatus], None] | None = None,
    ) -> dict[str, ExecutionResult]:
        """Execute all pending tasks."""
        with self._lock:
            pending_tasks = [
                task
                for task in self.tasks.values()
                if task.status in (TaskStatus.PENDING, TaskStatus.QUEUED)
            ]

        if not pending_tasks:
            return {}

        # Sort by priority
        pending_tasks.sort(key=lambda t: t.priority.value)

        # Execute with dependency awareness
        results = self.executor.execute_batch(pending_tasks, progress_callback)

        with self._lock:
            self.results.update(results)

        return results

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task."""
        with self._lock:
            task = self.tasks.get(task_id)
            if task and task.status in (TaskStatus.PENDING, TaskStatus.QUEUED):
                task.status = TaskStatus.CANCELLED
                return True
        return False

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of all tasks."""
        with self._lock:
            summary = {
                "total": len(self.tasks),
                "by_status": {},
                "by_priority": {},
                "success_rate": 0.0,
            }

            for task in self.tasks.values():
                status = task.status.value
                summary["by_status"][status] = summary["by_status"].get(status, 0) + 1

                priority = task.priority.name
                summary["by_priority"][priority] = summary["by_priority"].get(priority, 0) + 1

            completed = summary["by_status"].get("completed", 0)
            failed = summary["by_status"].get("failed", 0)
            if completed + failed > 0:
                summary["success_rate"] = completed / (completed + failed)

            return summary


class AdaptiveExecutionEngine:
    """Adaptive execution engine that learns from task outcomes."""

    def __init__(self, cwd: Path, max_workers: int = 4):
        self.cwd = cwd
        self.scheduler = TaskScheduler(max_workers=max_workers)
        self.retry_handler = SmartRetryHandler()
        self.execution_history: list[dict[str, Any]] = []
        self.learned_patterns: dict[str, dict] = {}
        self._lock = threading.Lock()

    def execute_task_chain(
        self,
        tasks: list[ExecutionTask],
        on_progress: Callable[[str, TaskStatus, str], None] | None = None,
        on_error: Callable[[str, str], bool] | None = None,
    ) -> dict[str, ExecutionResult]:
        """Execute a chain of tasks with adaptive error handling.

        Args:
            tasks: List of tasks to execute
            on_progress: Callback for progress updates (task_id, status, message)
            on_error: Callback for errors, returns True to retry with AI fix

        Returns:
            Dict mapping task_id to ExecutionResult
        """
        self.scheduler.add_tasks(tasks)

        def progress_wrapper(task_id: str, status: TaskStatus) -> None:
            if on_progress:
                task = self.scheduler.tasks.get(task_id)
                message = task.description if task else ""
                on_progress(task_id, status, message)

        results = self.scheduler.execute_all(progress_callback=progress_wrapper)

        # Handle failures with adaptive recovery
        failed_tasks = [
            (task_id, result) for task_id, result in results.items() if not result.success
        ]

        for task_id, result in failed_tasks:
            if on_error and result.error:
                # Check if we should attempt AI-powered fix
                should_retry = on_error(task_id, result.error)
                if should_retry:
                    # Re-execute after fix
                    task = self.scheduler.tasks.get(task_id)
                    if task:
                        task.status = TaskStatus.PENDING
                        new_result = self.scheduler.executor._execute_single(task)
                        results[task_id] = new_result

        # Record execution for learning
        self._record_execution(tasks, results)

        return results

    def _record_execution(
        self,
        tasks: list[ExecutionTask],
        results: dict[str, ExecutionResult],
    ) -> None:
        """Record execution outcomes for learning."""
        with self._lock:
            for task in tasks:
                result = results.get(task.id)
                if result:
                    self.execution_history.append(
                        {
                            "task_id": task.id,
                            "description": task.description,
                            "command": str(task.command)
                            if not callable(task.command)
                            else "<function>",
                            "success": result.success,
                            "error": result.error,
                            "attempts": result.attempts,
                            "duration": result.duration,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                    # Learn from patterns
                    if result.error:
                        error_category = self.retry_handler.categorize_error(result.error)[
                            "category"
                        ]
                        key = f"{error_category}:{task.description[:50]}"

                        if key not in self.learned_patterns:
                            self.learned_patterns[key] = {
                                "occurrences": 0,
                                "fixed_count": 0,
                                "avg_attempts": 0,
                            }

                        pattern = self.learned_patterns[key]
                        pattern["occurrences"] += 1
                        pattern["avg_attempts"] = (
                            pattern["avg_attempts"] * (pattern["occurrences"] - 1) + result.attempts
                        ) / pattern["occurrences"]
                        if result.success:
                            pattern["fixed_count"] += 1

    def get_learning_insights(self) -> dict[str, Any]:
        """Get insights from learned execution patterns."""
        with self._lock:
            if not self.execution_history:
                return {"message": "No execution history available"}

            total_executions = len(self.execution_history)
            successful = sum(1 for e in self.execution_history if e["success"])

            error_categories: dict[str, int] = {}
            for entry in self.execution_history:
                if entry.get("error"):
                    cat = self.retry_handler.categorize_error(entry["error"])["category"]
                    error_categories[cat] = error_categories.get(cat, 0) + 1

            avg_duration = sum(e["duration"] for e in self.execution_history) / total_executions
            avg_attempts = sum(e["attempts"] for e in self.execution_history) / total_executions

            return {
                "total_executions": total_executions,
                "success_rate": successful / total_executions if total_executions > 0 else 0,
                "avg_duration": avg_duration,
                "avg_attempts": avg_attempts,
                "error_distribution": error_categories,
                "learned_patterns": len(self.learned_patterns),
                "most_common_errors": sorted(error_categories.items(), key=lambda x: -x[1])[:5],
            }

    def suggest_optimizations(self) -> list[str]:
        """Suggest optimizations based on learned patterns."""
        insights = self.get_learning_insights()
        suggestions = []

        success_rate = insights.get("success_rate", 1.0)
        if success_rate < 0.8:
            suggestions.append(
                f"Success rate is {success_rate:.0%}. Consider improving error handling."
            )

        avg_attempts = insights.get("avg_attempts", 1)
        if avg_attempts > 2:
            suggestions.append(
                f"Average retry attempts is {avg_attempts:.1f}. Review retry configuration."
            )

        error_dist = insights.get("error_distribution", {})
        if "syntax" in error_dist and error_dist["syntax"] > 3:
            suggestions.append(
                "Multiple syntax errors detected. Add pre-validation before execution."
            )
        if "import" in error_dist and error_dist["import"] > 2:
            suggestions.append("Import errors are common. Verify module paths before writing code.")

        return suggestions


class ProgressTracker:
    """Tracks and displays execution progress."""

    def __init__(self, total_tasks: int = 0):
        self.total_tasks = total_tasks
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.current_task: str = ""
        self.start_time: float = time.time()
        self._lock = threading.Lock()

    def update(self, task_id: str, status: TaskStatus, message: str = "") -> None:
        """Update progress with a task status change."""
        with self._lock:
            self.current_task = message or task_id
            if status == TaskStatus.COMPLETED:
                self.completed_tasks += 1
            elif status == TaskStatus.FAILED:
                self.failed_tasks += 1

    def get_progress(self) -> dict[str, Any]:
        """Get current progress information."""
        with self._lock:
            elapsed = time.time() - self.start_time
            processed = self.completed_tasks + self.failed_tasks
            remaining = self.total_tasks - processed

            eta = None
            if processed > 0:
                avg_time = elapsed / processed
                eta = avg_time * remaining

            return {
                "total": self.total_tasks,
                "completed": self.completed_tasks,
                "failed": self.failed_tasks,
                "remaining": remaining,
                "percent": (processed / self.total_tasks * 100) if self.total_tasks > 0 else 0,
                "elapsed": elapsed,
                "eta": eta,
                "current_task": self.current_task,
            }

    def format_progress(self) -> str:
        """Format progress as a string."""
        p = self.get_progress()
        bar_width = 20
        filled = int(bar_width * p["percent"] / 100)
        bar = "█" * filled + "░" * (bar_width - filled)

        eta_str = ""
        if p["eta"]:
            eta_str = f" ETA: {p['eta']:.0f}s"

        return f"[{bar}] {p['percent']:.0f}% ({p['completed']}/{p['total']}){eta_str}"
