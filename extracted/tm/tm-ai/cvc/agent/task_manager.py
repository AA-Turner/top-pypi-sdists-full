"""
cvc.agent.task_manager — Background task management (Claude Code-style).

Enables running long-running shell commands in the background while
the agent continues working. Tasks can be monitored, listed, and killed.

Usage by the LLM:
  task_create(command="npm run build")  →  task_id
  task_get(task_id="abc123")           →  status + output
  task_list()                          →  all tasks with statuses
  task_kill(task_id="abc123")          →  terminate running task
"""

from __future__ import annotations

import logging
import os
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.task_manager")

MAX_OUTPUT_CHARS = 30_000  # Truncation limit for task output


@dataclass
class Task:
    """A background task."""
    id: str
    command: str
    status: str = "running"  # running, completed, failed, killed
    output: str = ""
    error: str = ""
    exit_code: int | None = None
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    _process: subprocess.Popen | None = field(default=None, repr=False)
    _thread: threading.Thread | None = field(default=None, repr=False)

    @property
    def elapsed(self) -> float:
        end = self.end_time or time.time()
        return end - self.start_time

    @property
    def elapsed_str(self) -> str:
        e = self.elapsed
        if e < 60:
            return f"{e:.1f}s"
        return f"{e / 60:.1f}m"

    def summary(self) -> str:
        """One-line summary for task listing."""
        cmd_preview = self.command[:60]
        if len(self.command) > 60:
            cmd_preview += "..."
        return f"[{self.id[:8]}] {self.status} ({self.elapsed_str}) — {cmd_preview}"


class TaskManager:
    """Manages background tasks with output capture."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self._tasks: dict[str, Task] = {}
        self._lock = threading.Lock()

    def create(self, command: str) -> Task:
        """Start a background task running the given shell command."""
        task_id = uuid.uuid4().hex[:12]

        # Determine shell based on OS
        if os.name == "nt":
            shell_cmd = ["powershell", "-NoProfile", "-Command", command]
        else:
            shell_cmd = ["/bin/sh", "-c", command]

        proc = subprocess.Popen(
            shell_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(self.workspace),
            text=True,
            env={**os.environ},
                    **HIDDEN_KW,
        )

        task = Task(
            id=task_id,
            command=command,
            _process=proc,
        )

        def _monitor():
            try:
                stdout, stderr = proc.communicate()
                task.output = stdout or ""
                task.error = stderr or ""
                task.exit_code = proc.returncode
                task.end_time = time.time()
                task.status = "completed" if proc.returncode == 0 else "failed"
            except Exception as e:
                task.error = str(e)
                task.status = "failed"
                task.end_time = time.time()

        thread = threading.Thread(target=_monitor, daemon=True)
        thread.start()
        task._thread = thread

        with self._lock:
            self._tasks[task_id] = task

        logger.info("Task %s started: %s", task_id, command[:80])
        return task

    def get(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        with self._lock:
            return self._tasks.get(task_id)

    def list_all(self) -> list[Task]:
        """List all tasks."""
        with self._lock:
            return list(self._tasks.values())

    def kill(self, task_id: str) -> bool:
        """Kill a running task. Returns True if killed."""
        with self._lock:
            task = self._tasks.get(task_id)
        if not task:
            return False

        if task.status != "running" or task._process is None:
            return False

        try:
            task._process.terminate()
            # Give it a moment to terminate gracefully
            try:
                task._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                task._process.kill()

            task.status = "killed"
            task.end_time = time.time()
            task.exit_code = -1
            logger.info("Task %s killed", task_id)
            return True
        except Exception as e:
            logger.error("Failed to kill task %s: %s", task_id, e)
            return False

    def get_output(self, task: Task) -> str:
        """Get task output, truncating if necessary."""
        parts = []
        if task.output:
            output = task.output
            if len(output) > MAX_OUTPUT_CHARS:
                output = output[:MAX_OUTPUT_CHARS] + f"\n... (truncated, {len(task.output)} chars total)"
            parts.append(output)
        if task.error:
            parts.append(f"STDERR:\n{task.error[:5000]}")
        return "\n".join(parts) if parts else "(no output)"
