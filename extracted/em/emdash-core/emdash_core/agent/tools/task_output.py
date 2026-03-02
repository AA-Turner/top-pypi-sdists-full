"""Task management tools for background tasks.

Provides tools to:
- Get output from background tasks (shell commands and sub-agents)
- Kill running background tasks
- List all background tasks
"""

import json
import time
from pathlib import Path
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ..background import BackgroundTaskManager, TaskStatus, TaskType
from ...utils.logger import log


class TaskOutputTool(BaseTool):
    """Get output from a running or completed background task.

    Works with both shell commands (execute_command with run_in_background=true)
    and sub-agents (task with run_in_background=true).
    """

    name = "task_output"
    description = """Get output from a background task (shell command or sub-agent).

Use this to check the status and results of tasks started with run_in_background=true.
Can wait for completion or check immediately.

Works with:
- Shell commands: execute_command(..., run_in_background=true)
- Sub-agents: task(..., run_in_background=true)"""
    category = ToolCategory.PLANNING

    def __init__(self, repo_root: Path, connection=None):
        """Initialize with repo root.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used)
        """
        self.repo_root = repo_root.resolve()
        self.agents_dir = repo_root / ".emdash" / "agents"
        self.connection = connection

    def execute(
        self,
        task_id: str = "",
        block: bool = True,
        timeout: int = 60,
        **kwargs,
    ) -> ToolResult:
        """Get output from a background task.

        Args:
            task_id: Task ID to get output from (shell_xxx or agent_xxx)
            block: Whether to wait for completion
            timeout: Max wait time in seconds (if blocking)

        Returns:
            ToolResult with task output or status
        """
        # Support both task_id and agent_id for backwards compatibility
        task_id = task_id or kwargs.get("agent_id", "")

        if not task_id:
            return ToolResult.error_result(
                "task_id is required",
                suggestions=["Provide the task_id from execute_command() or task() call"],
            )

        # Try the new BackgroundTaskManager first
        manager = BackgroundTaskManager.get_instance()
        task = manager.get_task(task_id)

        if task:
            return self._get_task_from_manager(task, block, timeout)

        # Fall back to file-based lookup for legacy sub-agents
        output_file = self.agents_dir / f"{task_id}.output"
        transcript_file = self.agents_dir / f"{task_id}.jsonl"

        if block:
            return self._wait_for_completion(
                task_id, output_file, transcript_file, timeout
            )
        else:
            return self._check_status(task_id, output_file, transcript_file)

    def _get_task_from_manager(
        self,
        task,
        block: bool,
        timeout: int,
    ) -> ToolResult:
        """Get task status from BackgroundTaskManager.

        Args:
            task: BackgroundTask instance
            block: Whether to wait for completion
            timeout: Max wait time in seconds

        Returns:
            ToolResult with task info
        """
        if block and task.status == TaskStatus.RUNNING:
            # Wait for completion
            start_time = time.time()
            while time.time() - start_time < timeout:
                if task.status != TaskStatus.RUNNING:
                    break
                time.sleep(0.5)

            if task.status == TaskStatus.RUNNING:
                # Task timed out - try to get partial results
                data = {
                    "task_id": task.task_id,
                    "status": "timeout",
                    "message": f"Task did not complete within {timeout}s",
                    "partial_stdout": task.stdout[-2000:] if task.stdout else "",
                }
                suggestions = ["Use block=false to check status without waiting"]

                # For Plan agents, check for partial plan files
                if task.task_type == TaskType.SUBAGENT and task.agent_type == "Plan":
                    partial_plan = self._get_partial_plan_content()
                    if partial_plan:
                        data["partial_plan"] = partial_plan
                        data["message"] = f"Plan agent timed out after {timeout}s but wrote a partial plan"
                        suggestions = [
                            "The partial plan is included below - you can continue from here",
                            "Use read_file to get the full plan if needed",
                        ]

                return ToolResult.success_result(data=data, suggestions=suggestions)

        # Return full task info
        return ToolResult.success_result(
            data=task.to_dict(),
            metadata={"task_id": task.task_id},
        )

    def _get_partial_plan_content(self) -> str:
        """Check for recently created plan files and return their content.

        Returns:
            Content of the most recent plan file, or empty string if none found
        """
        plans_dir = self.repo_root / ".emdash" / "plans"
        if not plans_dir.exists():
            return ""

        # Find plan files modified in the last 5 minutes
        recent_plans = []
        cutoff_time = time.time() - 300  # 5 minutes

        for plan_file in plans_dir.glob("*.md"):
            try:
                if plan_file.stat().st_mtime > cutoff_time:
                    recent_plans.append(plan_file)
            except OSError:
                continue

        if not recent_plans:
            return ""

        # Get the most recently modified plan
        most_recent = max(recent_plans, key=lambda p: p.stat().st_mtime)

        try:
            content = most_recent.read_text()
            # Truncate if too long
            if len(content) > 5000:
                content = content[:5000] + "\n\n... (truncated, use read_file for full content)"
            return f"[Plan file: {most_recent.name}]\n\n{content}"
        except Exception as e:
            log.warning(f"Failed to read plan file {most_recent}: {e}")
            return ""

    def _wait_for_completion(
        self,
        agent_id: str,
        output_file: Path,
        transcript_file: Path,
        timeout: int,
    ) -> ToolResult:
        """Wait for legacy agent to complete (file-based).

        Args:
            agent_id: Agent ID
            output_file: Path to output file
            transcript_file: Path to transcript file
            timeout: Max wait time in seconds

        Returns:
            ToolResult with results
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            if output_file.exists():
                content = output_file.read_text().strip()

                # Check if output is complete JSON
                try:
                    data = json.loads(content)
                    if isinstance(data, dict) and "success" in data:
                        return ToolResult.success_result(
                            data=data,
                            metadata={"task_id": agent_id, "status": "completed"},
                        )
                except json.JSONDecodeError:
                    pass

                # Still running if output exists but isn't complete JSON
                if content:
                    return ToolResult.success_result(
                        data={
                            "status": "running",
                            "task_id": agent_id,
                            "partial_output": content[-2000:],  # Last 2KB
                        },
                    )

            time.sleep(1)

        # Timeout
        return ToolResult.success_result(
            data={
                "status": "timeout",
                "task_id": agent_id,
                "message": f"Task did not complete within {timeout}s",
            },
            suggestions=["Use block=false to check status without waiting"],
        )

    def _check_status(
        self,
        agent_id: str,
        output_file: Path,
        transcript_file: Path,
    ) -> ToolResult:
        """Check legacy agent status without waiting (file-based).

        Args:
            agent_id: Agent ID
            output_file: Path to output file
            transcript_file: Path to transcript file

        Returns:
            ToolResult with status
        """
        # Check if output file exists
        if not output_file.exists():
            # Check if transcript exists (agent was started)
            if transcript_file.exists():
                return ToolResult.success_result(
                    data={
                        "status": "running",
                        "task_id": agent_id,
                    },
                )
            else:
                return ToolResult.error_result(
                    f"Task {agent_id} not found",
                    suggestions=["Check the task_id is correct"],
                )

        # Output exists, check if complete
        try:
            content = output_file.read_text().strip()
            data = json.loads(content)

            if isinstance(data, dict) and "success" in data:
                return ToolResult.success_result(
                    data=data,
                    metadata={"task_id": agent_id, "status": "completed"},
                )

        except json.JSONDecodeError:
            pass

        # Partial output
        return ToolResult.success_result(
            data={
                "status": "running",
                "task_id": agent_id,
                "has_output": True,
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "task_id": {
                    "type": "string",
                    "description": "Task ID to get output from (e.g., shell_abc123 or agent_xyz789)",
                },
                "block": {
                    "type": "boolean",
                    "description": "Wait for completion (default: true)",
                    "default": True,
                },
                "timeout": {
                    "type": "integer",
                    "description": "Max wait time in seconds if blocking",
                    "default": 60,
                },
            },
            required=["task_id"],
        )


class KillTaskTool(BaseTool):
    """Kill a running background task."""

    name = "kill_task"
    description = """Kill a running background task (shell command or sub-agent).

Use this to terminate tasks that are no longer needed or are stuck.
Works with shell commands and sub-agents started with run_in_background=true."""
    category = ToolCategory.PLANNING

    def __init__(self, repo_root: Path, connection=None):
        """Initialize with repo root.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used)
        """
        self.repo_root = repo_root.resolve()
        self.connection = connection

    def execute(
        self,
        task_id: str = "",
        **kwargs,
    ) -> ToolResult:
        """Kill a background task.

        Args:
            task_id: Task ID to kill

        Returns:
            ToolResult indicating success or failure
        """
        if not task_id:
            return ToolResult.error_result(
                "task_id is required",
                suggestions=["Provide the task_id to kill"],
            )

        manager = BackgroundTaskManager.get_instance()
        task = manager.get_task(task_id)

        if not task:
            return ToolResult.error_result(
                f"Task {task_id} not found",
                suggestions=["Check the task_id is correct", "Use list_tasks to see all tasks"],
            )

        if task.status != TaskStatus.RUNNING:
            return ToolResult.error_result(
                f"Task {task_id} is not running (status: {task.status.value})",
            )

        success = manager.kill_task(task_id)

        if success:
            return ToolResult.success_result(
                data={
                    "task_id": task_id,
                    "killed": True,
                    "message": f"Task {task_id} has been terminated",
                },
            )
        else:
            return ToolResult.error_result(
                f"Failed to kill task {task_id}",
            )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "task_id": {
                    "type": "string",
                    "description": "Task ID to kill",
                },
            },
            required=["task_id"],
        )


class ListTasksTool(BaseTool):
    """List all background tasks."""

    name = "list_tasks"
    description = """List all background tasks (running and completed).

Shows status of all shell commands and sub-agents started with run_in_background=true."""
    category = ToolCategory.PLANNING

    def __init__(self, repo_root: Path, connection=None):
        """Initialize with repo root.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used)
        """
        self.repo_root = repo_root.resolve()
        self.connection = connection

    def execute(
        self,
        status_filter: str = "",
        **kwargs,
    ) -> ToolResult:
        """List all background tasks.

        Args:
            status_filter: Optional filter by status (running, completed, failed)

        Returns:
            ToolResult with task list
        """
        manager = BackgroundTaskManager.get_instance()
        tasks = manager.get_all_tasks()

        # Apply filter if provided
        if status_filter:
            try:
                filter_status = TaskStatus(status_filter)
                tasks = [t for t in tasks if t.status == filter_status]
            except ValueError:
                return ToolResult.error_result(
                    f"Invalid status filter: {status_filter}",
                    suggestions=["Valid filters: running, completed, failed, killed"],
                )

        # Format task list
        task_list = []
        for task in tasks:
            task_info = {
                "task_id": task.task_id,
                "type": task.task_type.value,
                "status": task.status.value,
                "description": task.description,
            }

            if task.task_type == TaskType.SHELL:
                task_info["command"] = task.command[:50] + "..." if len(task.command or "") > 50 else task.command
            else:
                task_info["agent_type"] = task.agent_type

            if task.exit_code is not None:
                task_info["exit_code"] = task.exit_code

            task_list.append(task_info)

        return ToolResult.success_result(
            data={
                "tasks": task_list,
                "total": len(task_list),
                "running": len([t for t in tasks if t.status == TaskStatus.RUNNING]),
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "status_filter": {
                    "type": "string",
                    "enum": ["running", "completed", "failed", "killed"],
                    "description": "Filter by task status (optional)",
                },
            },
            required=[],
        )
