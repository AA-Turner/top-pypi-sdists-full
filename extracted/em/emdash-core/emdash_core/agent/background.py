"""Background task management for shell commands and sub-agents.

This module provides a centralized manager for tracking background tasks,
checking for completions, and generating notifications to inject into
the agent's context.

Inspired by Claude Code's background task system with notification-based
completion handling.
"""

import subprocess
import threading
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

from ..utils.logger import log


class TaskType(Enum):
    """Type of background task."""
    SHELL = "shell"
    SUBAGENT = "subagent"


class TaskStatus(Enum):
    """Status of a background task."""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"


@dataclass
class BackgroundTask:
    """Represents a background task (shell command or sub-agent)."""

    task_id: str
    task_type: TaskType
    description: str
    started_at: float = field(default_factory=time.time)

    # Shell-specific
    process: Optional[subprocess.Popen] = None
    command: Optional[str] = None

    # Sub-agent specific
    future: Optional[Future] = None
    agent_type: Optional[str] = None

    # Output capture
    output_file: Optional[Path] = None
    stdout: str = ""
    stderr: str = ""

    # Status
    status: TaskStatus = TaskStatus.RUNNING
    exit_code: Optional[int] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    completed_at: Optional[float] = None

    # Whether the agent has been notified of completion
    notified: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "description": self.description,
            "status": self.status.value,
            "exit_code": self.exit_code,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "command": self.command,
            "agent_type": self.agent_type,
            "stdout": self.stdout[-5000:] if self.stdout else "",
            "stderr": self.stderr[-2000:] if self.stderr else "",
            "error": self.error,
        }


class BackgroundTaskManager:
    """Manages background tasks with notification-based completion.

    This is a singleton that tracks all background tasks (shell commands
    and sub-agents), monitors their completion, and provides notifications
    to inject into the agent's context.

    Usage:
        manager = BackgroundTaskManager.get_instance()

        # Start a shell command
        task_id = manager.start_shell("npm test", description="Run tests")

        # Check for completed tasks to notify agent
        notifications = manager.get_pending_notifications()

        # Get task status
        task = manager.get_task(task_id)

        # Kill a task
        manager.kill_task(task_id)
    """

    _instance: Optional["BackgroundTaskManager"] = None
    _lock = threading.Lock()

    def __init__(self):
        """Initialize the manager."""
        self._tasks: dict[str, BackgroundTask] = {}
        self._executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="bg-task-")
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_monitor = threading.Event()
        self._start_monitor()

    @classmethod
    def get_instance(cls) -> "BackgroundTaskManager":
        """Get the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton (for testing)."""
        with cls._lock:
            if cls._instance is not None:
                cls._instance.shutdown()
                cls._instance = None

    def _start_monitor(self) -> None:
        """Start the background monitor thread."""
        if self._monitor_thread is not None and self._monitor_thread.is_alive():
            return

        self._stop_monitor.clear()
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            name="bg-task-monitor",
            daemon=True,
        )
        self._monitor_thread.start()

    def _monitor_loop(self) -> None:
        """Monitor running tasks for completion."""
        while not self._stop_monitor.is_set():
            try:
                self._check_tasks()
            except Exception as e:
                log.warning(f"Error in background task monitor: {e}")

            # Check every 500ms
            self._stop_monitor.wait(0.5)

    def _check_tasks(self) -> None:
        """Check all running tasks for completion."""
        for task in list(self._tasks.values()):
            if task.status != TaskStatus.RUNNING:
                continue

            if task.task_type == TaskType.SHELL:
                self._check_shell_task(task)
            elif task.task_type == TaskType.SUBAGENT:
                self._check_subagent_task(task)

    def _check_shell_task(self, task: BackgroundTask) -> None:
        """Check if a shell task has completed."""
        if task.process is None:
            return

        poll = task.process.poll()
        if poll is not None:
            # Process completed
            task.exit_code = poll
            task.completed_at = time.time()

            # Capture any remaining output
            try:
                stdout, stderr = task.process.communicate(timeout=1)
                task.stdout += stdout
                task.stderr += stderr
            except Exception:
                pass

            if poll == 0:
                task.status = TaskStatus.COMPLETED
            else:
                task.status = TaskStatus.FAILED
                task.error = f"Command exited with code {poll}"

            log.info(f"Shell task {task.task_id} completed with exit code {poll}")

    def _check_subagent_task(self, task: BackgroundTask) -> None:
        """Check if a sub-agent task has completed."""
        if task.future is None:
            return

        if task.future.done():
            task.completed_at = time.time()

            try:
                result = task.future.result(timeout=0)
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.exit_code = 0
                log.info(f"Sub-agent task {task.task_id} completed successfully")
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.exit_code = 1
                log.warning(f"Sub-agent task {task.task_id} failed: {e}")

    def start_shell(
        self,
        command: str,
        description: str = "",
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> str:
        """Start a shell command in the background.

        Args:
            command: Shell command to execute
            description: Human-readable description
            cwd: Working directory (defaults to current)
            timeout: Optional timeout in seconds (not enforced, just metadata)

        Returns:
            Task ID for tracking
        """
        task_id = f"shell_{uuid.uuid4().hex[:8]}"

        log.info(f"Starting background shell task {task_id}: {command[:50]}...")

        # Inject GitHub token into git clone URLs for authentication
        import os
        import re
        github_token = os.environ.get("GITHUB_TOKEN")
        actual_command = command

        if github_token and "git clone" in command:
            pattern = r'https://github\.com/([^/\s]+/[^/\s]+?)(?:\.git)?(?=\s|$)'
            def inject_token(match):
                repo_path = match.group(1)
                if repo_path.endswith('.git'):
                    repo_path = repo_path[:-4]
                return f'https://x-access-token:{github_token}@github.com/{repo_path}.git'
            actual_command = re.sub(pattern, inject_token, command)
            log.debug(f"Injected GitHub token into background clone command")

        # Start process with pipes for output capture
        process = subprocess.Popen(
            actual_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            env=os.environ.copy(),
        )

        task = BackgroundTask(
            task_id=task_id,
            task_type=TaskType.SHELL,
            description=description or command[:50],
            process=process,
            command=command,
        )

        # Start output reader threads
        self._start_output_reader(task)

        self._tasks[task_id] = task
        return task_id

    def _start_output_reader(self, task: BackgroundTask) -> None:
        """Start threads to read stdout/stderr without blocking."""
        def read_stream(stream, attr_name):
            try:
                for line in stream:
                    current = getattr(task, attr_name)
                    setattr(task, attr_name, current + line)
            except Exception:
                pass

        if task.process and task.process.stdout:
            threading.Thread(
                target=read_stream,
                args=(task.process.stdout, "stdout"),
                daemon=True,
            ).start()

        if task.process and task.process.stderr:
            threading.Thread(
                target=read_stream,
                args=(task.process.stderr, "stderr"),
                daemon=True,
            ).start()

    def start_subagent(
        self,
        future: Future,
        agent_type: str,
        description: str = "",
    ) -> str:
        """Register a sub-agent task for tracking.

        Args:
            future: Future from async sub-agent execution
            agent_type: Type of sub-agent (Explore, Plan, etc.)
            description: Human-readable description

        Returns:
            Task ID for tracking
        """
        task_id = f"agent_{uuid.uuid4().hex[:8]}"

        log.info(f"Registering background sub-agent {task_id}: {agent_type}")

        task = BackgroundTask(
            task_id=task_id,
            task_type=TaskType.SUBAGENT,
            description=description,
            future=future,
            agent_type=agent_type,
        )

        self._tasks[task_id] = task
        return task_id

    def get_task(self, task_id: str) -> Optional[BackgroundTask]:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[BackgroundTask]:
        """Get all tasks."""
        return list(self._tasks.values())

    def get_running_tasks(self) -> list[BackgroundTask]:
        """Get all currently running tasks."""
        return [t for t in self._tasks.values() if t.status == TaskStatus.RUNNING]

    def get_pending_notifications(self) -> list[BackgroundTask]:
        """Get completed tasks that haven't been notified yet.

        Returns:
            List of tasks that completed since last check.
            Marks them as notified so they won't be returned again.
        """
        notifications = []

        for task in self._tasks.values():
            if task.status != TaskStatus.RUNNING and not task.notified:
                notifications.append(task)
                task.notified = True

        return notifications

    def format_notification(self, task: BackgroundTask) -> str:
        """Format a task completion as a notification message.

        Args:
            task: Completed task

        Returns:
            Formatted notification string for injection into context
        """
        status_str = "completed successfully" if task.status == TaskStatus.COMPLETED else "failed"

        if task.task_type == TaskType.SHELL:
            msg = f"[Background shell task {task.task_id} {status_str}]"
            msg += f"\nCommand: {task.command}"
            msg += f"\nExit code: {task.exit_code}"

            if task.stdout:
                # Truncate long output
                stdout = task.stdout[-3000:] if len(task.stdout) > 3000 else task.stdout
                if len(task.stdout) > 3000:
                    stdout = "...(truncated)\n" + stdout
                msg += f"\n\nStdout:\n{stdout}"

            if task.stderr:
                stderr = task.stderr[-1500:] if len(task.stderr) > 1500 else task.stderr
                if len(task.stderr) > 1500:
                    stderr = "...(truncated)\n" + stderr
                msg += f"\n\nStderr:\n{stderr}"

        else:  # SUBAGENT
            msg = f"[Background sub-agent {task.task_id} ({task.agent_type}) {status_str}]"

            if task.error:
                msg += f"\nError: {task.error}"
            elif task.result:
                # Include summary from sub-agent result
                if hasattr(task.result, "summary"):
                    msg += f"\n\nSummary:\n{task.result.summary}"
                elif isinstance(task.result, dict) and "summary" in task.result:
                    msg += f"\n\nSummary:\n{task.result['summary']}"

        msg += f"\n\nUse task_output(task_id='{task.task_id}') for full details."

        return msg

    def kill_task(self, task_id: str) -> bool:
        """Kill a running task.

        Args:
            task_id: Task to kill

        Returns:
            True if task was killed, False if not found or already completed
        """
        task = self._tasks.get(task_id)
        if task is None:
            return False

        if task.status != TaskStatus.RUNNING:
            return False

        log.info(f"Killing background task {task_id}")

        if task.task_type == TaskType.SHELL and task.process:
            try:
                task.process.terminate()
                # Give it a moment to terminate gracefully
                try:
                    task.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    task.process.kill()

                task.status = TaskStatus.KILLED
                task.exit_code = -15  # SIGTERM
                task.completed_at = time.time()
                return True
            except Exception as e:
                log.warning(f"Failed to kill shell task {task_id}: {e}")
                return False

        elif task.task_type == TaskType.SUBAGENT and task.future:
            # Can't really kill a future, but we can mark it
            task.future.cancel()
            task.status = TaskStatus.KILLED
            task.completed_at = time.time()
            return True

        return False

    def cleanup_old_tasks(self, max_age_seconds: int = 3600) -> int:
        """Remove old completed tasks.

        Args:
            max_age_seconds: Remove tasks older than this (default 1 hour)

        Returns:
            Number of tasks removed
        """
        now = time.time()
        to_remove = []

        for task_id, task in self._tasks.items():
            if task.status == TaskStatus.RUNNING:
                continue

            if task.completed_at and (now - task.completed_at) > max_age_seconds:
                to_remove.append(task_id)

        for task_id in to_remove:
            del self._tasks[task_id]

        if to_remove:
            log.debug(f"Cleaned up {len(to_remove)} old background tasks")

        return len(to_remove)

    def shutdown(self) -> None:
        """Shutdown the manager and clean up resources."""
        log.info("Shutting down BackgroundTaskManager")

        # Stop monitor thread
        self._stop_monitor.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)

        # Kill any running tasks
        for task in list(self._tasks.values()):
            if task.status == TaskStatus.RUNNING:
                self.kill_task(task.task_id)

        # Shutdown executor
        self._executor.shutdown(wait=False)
