"""File-based task storage with labels and cross-session support."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from filelock import FileLock

from .models import Task, TaskList, TaskStatus, TaskEvent
from .broadcaster import TaskEventBroadcaster


class ConflictError(Exception):
    """Raised when optimistic locking detects a conflict."""

    pass


class TaskStore:
    """
    File-based task storage with labels and cross-session support.

    Tasks are stored in .emdash/tasks/ with:
    - {task-list-id}.json: Individual task list data
    - {task-list-id}.lock: File lock for concurrent access

    Example:
        store = TaskStore()
        store.add_task("feature-auth", "Build API", labels=["backend"])
        tasks = store.get_claimable_tasks("feature-auth", labels=["backend"])
    """

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = repo_root or Path.cwd()
        self.tasks_dir = self.repo_root / ".emdash" / "tasks"

    def _ensure_dir(self) -> None:
        """Ensure tasks directory exists."""
        self.tasks_dir.mkdir(parents=True, exist_ok=True)

    def _get_lock(self, task_list_id: str) -> FileLock:
        """Get file lock for a task list."""
        self._ensure_dir()
        return FileLock(self.tasks_dir / f"{task_list_id}.lock", timeout=5)

    def _task_list_path(self, task_list_id: str) -> Path:
        """Get path to task list file."""
        return self.tasks_dir / f"{task_list_id}.json"

    # ─────────────────────────────────────────────────────────────
    # Task List CRUD
    # ─────────────────────────────────────────────────────────────

    def create_task_list(self, name: str, description: str = "") -> TaskList:
        """Create a new task list."""
        self._ensure_dir()
        now = datetime.utcnow().isoformat()
        task_list = TaskList(
            id=name,  # Use name as ID for simplicity
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
        )
        self._save_task_list(task_list)
        return task_list

    def get_task_list(self, task_list_id: str) -> TaskList | None:
        """Get a task list by ID."""
        path = self._task_list_path(task_list_id)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text())
            return TaskList.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None

    def get_or_create_task_list(self, task_list_id: str) -> TaskList:
        """Get existing task list or create new one."""
        task_list = self.get_task_list(task_list_id)
        if not task_list:
            task_list = self.create_task_list(task_list_id)
        return task_list

    def _save_task_list(self, task_list: TaskList) -> None:
        """Save task list to file."""
        self._ensure_dir()
        task_list.updated_at = datetime.utcnow().isoformat()
        path = self._task_list_path(task_list.id)
        path.write_text(json.dumps(task_list.to_dict(), indent=2))

    def list_task_lists(self) -> list[dict[str, Any]]:
        """List all task lists with metadata."""
        if not self.tasks_dir.exists():
            return []

        result = []
        for path in self.tasks_dir.glob("*.json"):
            try:
                data = json.loads(path.read_text())
                result.append(
                    {
                        "id": data["id"],
                        "name": data["name"],
                        "description": data.get("description", ""),
                        "task_count": len(data.get("tasks", [])),
                        "updated_at": data.get("updated_at", ""),
                    }
                )
            except (json.JSONDecodeError, KeyError):
                continue

        return sorted(result, key=lambda x: x.get("updated_at", ""), reverse=True)

    def delete_task_list(self, task_list_id: str) -> bool:
        """Delete a task list."""
        path = self._task_list_path(task_list_id)
        lock_path = self.tasks_dir / f"{task_list_id}.lock"

        if path.exists():
            path.unlink()
        if lock_path.exists():
            lock_path.unlink()

        return True

    # ─────────────────────────────────────────────────────────────
    # Task CRUD with Labels
    # ─────────────────────────────────────────────────────────────

    def add_task(
        self,
        task_list_id: str,
        title: str,
        description: str = "",
        labels: list[str] | None = None,
        depends_on: list[str] | None = None,
        priority: int = 0,
        created_by: str = "",
    ) -> Task:
        """Add a task with labels."""
        with self._get_lock(task_list_id):
            task_list = self.get_or_create_task_list(task_list_id)
            now = datetime.utcnow().isoformat()

            task = Task(
                id=f"task-{uuid.uuid4().hex[:8]}",
                title=title,
                description=description,
                labels=labels or [],
                depends_on=depends_on or [],
                priority=priority,
                created_at=now,
                updated_at=now,
                created_by=created_by,
                order=len(task_list.tasks),
            )

            # Validate dependencies exist
            existing_ids = {t.id for t in task_list.tasks}
            for dep_id in task.depends_on:
                if dep_id not in existing_ids:
                    raise ValueError(f"Dependency '{dep_id}' does not exist")

            # Check for cycles
            if self._would_create_cycle(task_list, task.id, task.depends_on):
                raise ValueError("Adding these dependencies would create a cycle")

            task_list.tasks.append(task)
            self._save_task_list(task_list)

            # Publish event
            TaskEventBroadcaster.publish_sync(
                TaskEventBroadcaster.create_event(
                    TaskEventBroadcaster.TASK_ADDED,
                    task_list_id,
                    task.id,
                    title=task.title,
                    labels=task.labels,
                    created_by=task.created_by,
                )
            )

            return task

    def get_task(self, task_list_id: str, task_id: str) -> Task | None:
        """Get a task by ID."""
        task_list = self.get_task_list(task_list_id)
        if not task_list:
            return None
        return task_list.get_task(task_id)

    def update_task(
        self,
        task_list_id: str,
        task_id: str,
        updates: dict[str, Any],
        expected_version: int | None = None,
    ) -> Task:
        """Update task with optional optimistic locking."""
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                raise ValueError(f"Task list '{task_list_id}' not found")

            task = task_list.get_task(task_id)
            if not task:
                raise ValueError(f"Task '{task_id}' not found")

            # Optimistic locking check
            if expected_version is not None and task.version != expected_version:
                raise ConflictError(
                    f"Task modified (v{task.version} != expected v{expected_version})"
                )

            # Validate depends_on if being updated
            if "depends_on" in updates:
                new_deps = updates["depends_on"]
                # Check all dependencies exist
                existing_ids = {t.id for t in task_list.tasks}
                for dep_id in new_deps:
                    if dep_id not in existing_ids:
                        raise ValueError(f"Dependency '{dep_id}' does not exist")
                # Check for cycles
                if self._would_create_cycle(task_list, task_id, new_deps):
                    raise ValueError("Adding these dependencies would create a cycle")

            # Apply updates
            for key, value in updates.items():
                if hasattr(task, key) and key not in ("id", "version"):
                    if key == "status" and isinstance(value, str):
                        value = TaskStatus(value)
                    setattr(task, key, value)

            task.version += 1
            task.updated_at = datetime.utcnow().isoformat()
            self._save_task_list(task_list)
            return task

    def delete_task(self, task_list_id: str, task_id: str) -> bool:
        """Delete a task."""
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                return False

            # Check if task exists before deleting
            task = task_list.get_task(task_id)
            if not task:
                return False

            # Remove task
            task_list.tasks = [t for t in task_list.tasks if t.id != task_id]

            # Remove from dependencies of other tasks
            for t in task_list.tasks:
                if task_id in t.depends_on:
                    t.depends_on.remove(task_id)

            self._save_task_list(task_list)

            # Publish event (triggers TaskWaiter cleanup)
            TaskEventBroadcaster.publish_sync(
                TaskEventBroadcaster.create_event(
                    TaskEventBroadcaster.TASK_DELETED,
                    task_list_id,
                    task_id,
                    title=task.title,
                )
            )

            return True

    # ─────────────────────────────────────────────────────────────
    # Labels-Based Filtering (Core Logic)
    # ─────────────────────────────────────────────────────────────

    def get_tasks_by_labels(
        self,
        task_list_id: str,
        labels: list[str],
        match_all: bool = False,
    ) -> list[Task]:
        """
        Get tasks matching the given labels.

        Args:
            task_list_id: Task list to search
            labels: Labels to filter by
            match_all: If True, task must have ALL labels. If False, ANY label matches.
        """
        task_list = self.get_task_list(task_list_id)
        if not task_list:
            return []

        matching = []
        filter_labels = set(labels)

        for task in task_list.tasks:
            task_labels = set(task.labels)

            if match_all:
                # Task must have ALL requested labels
                if filter_labels.issubset(task_labels):
                    matching.append(task)
            else:
                # Task must have ANY requested label
                if task_labels & filter_labels:
                    matching.append(task)

        return matching

    def get_claimable_tasks(
        self,
        task_list_id: str,
        labels: list[str] | None = None,
    ) -> list[Task]:
        """
        Get tasks that can be claimed (not claimed, dependencies met).
        Optionally filter by labels.
        """
        task_list = self.get_task_list(task_list_id)
        if not task_list:
            return []

        claimable = []
        for task in task_list.tasks:
            # Skip if already claimed or completed
            if task.claimed_by or task.status == TaskStatus.COMPLETED:
                continue

            # Check dependencies are all completed
            if not self._are_dependencies_met(task, task_list):
                continue

            # Filter by labels if specified
            if labels:
                if not (set(labels) & set(task.labels)):
                    continue

            claimable.append(task)

        # Sort by priority (higher first), then order
        claimable.sort(key=lambda t: (-t.priority, t.order))
        return claimable

    def get_all_tasks(self, task_list_id: str) -> list[Task]:
        """Get all tasks in a task list."""
        task_list = self.get_task_list(task_list_id)
        if not task_list:
            return []
        return task_list.tasks

    def _are_dependencies_met(self, task: Task, task_list: TaskList) -> bool:
        """Check if all dependencies are completed."""
        for dep_id in task.depends_on:
            dep_task = task_list.get_task(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    def get_blocking_tasks(self, task_list_id: str, task_id: str) -> list[Task]:
        """Get tasks that are blocking a given task."""
        task_list = self.get_task_list(task_list_id)
        if not task_list:
            return []

        task = task_list.get_task(task_id)
        if not task:
            return []

        blocking = []
        for dep_id in task.depends_on:
            dep_task = task_list.get_task(dep_id)
            if dep_task and dep_task.status != TaskStatus.COMPLETED:
                blocking.append(dep_task)

        return blocking

    def _would_create_cycle(
        self, task_list: TaskList, task_id: str, new_deps: list[str]
    ) -> bool:
        """Check if adding dependencies would create a cycle."""
        # Build adjacency list
        graph: dict[str, list[str]] = {}
        for task in task_list.tasks:
            graph[task.id] = list(task.depends_on)

        # Add the new dependencies
        if task_id not in graph:
            graph[task_id] = []
        graph[task_id] = list(new_deps)

        # DFS to detect cycle
        visited = set()
        rec_stack = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True

        return False

    # ─────────────────────────────────────────────────────────────
    # Claiming Logic
    # ─────────────────────────────────────────────────────────────

    def claim_task(
        self,
        task_list_id: str,
        task_id: str,
        session_id: str,
    ) -> tuple[bool, str]:
        """
        Attempt to claim a task.
        Returns (success, message).
        """
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                return False, f"Task list '{task_list_id}' not found"

            task = task_list.get_task(task_id)
            if not task:
                return False, f"Task '{task_id}' not found"

            # Check if already claimed
            if task.claimed_by:
                if task.claimed_by == session_id:
                    return True, "Already claimed by you"
                return False, f"Already claimed by {task.claimed_by}"

            # Check if already completed
            if task.status == TaskStatus.COMPLETED:
                return False, "Task already completed"

            # Check dependencies
            if not self._are_dependencies_met(task, task_list):
                blocking = self.get_blocking_tasks(task_list_id, task_id)
                blocking_names = [f"'{t.title}'" for t in blocking]
                return False, f"Blocked by: {', '.join(blocking_names)}"

            # Claim it!
            task.claimed_by = session_id
            task.claimed_at = datetime.utcnow().isoformat()
            task.status = TaskStatus.IN_PROGRESS
            task.version += 1
            self._save_task_list(task_list)

            # Publish event
            TaskEventBroadcaster.publish_sync(
                TaskEventBroadcaster.create_event(
                    TaskEventBroadcaster.TASK_CLAIMED,
                    task_list_id,
                    task_id,
                    claimed_by=session_id,
                    title=task.title,
                )
            )

            return True, "Claimed successfully"

    def complete_task(
        self,
        task_list_id: str,
        task_id: str,
        session_id: str,
    ) -> tuple[bool, str]:
        """Mark a task as completed. Must be claimed by this session."""
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                return False, f"Task list '{task_list_id}' not found"

            task = task_list.get_task(task_id)
            if not task:
                return False, f"Task '{task_id}' not found"

            # Verify ownership
            if task.claimed_by != session_id:
                if task.claimed_by:
                    return False, f"Task claimed by {task.claimed_by}, not you"
                return False, "Task not claimed"

            # Complete it
            task.status = TaskStatus.COMPLETED
            task.version += 1
            task.updated_at = datetime.utcnow().isoformat()
            self._save_task_list(task_list)

            # Publish event (triggers TaskWaiter notification to wake up blocked agents)
            TaskEventBroadcaster.publish_sync(
                TaskEventBroadcaster.create_event(
                    TaskEventBroadcaster.TASK_COMPLETED,
                    task_list_id,
                    task_id,
                    completed_by=session_id,
                    title=task.title,
                )
            )

            return True, "Completed successfully"

    def release_task(
        self,
        task_list_id: str,
        task_id: str,
        session_id: str,
    ) -> tuple[bool, str]:
        """Release a claimed task back to pending."""
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                return False, f"Task list '{task_list_id}' not found"

            task = task_list.get_task(task_id)
            if not task:
                return False, f"Task '{task_id}' not found"

            if task.claimed_by != session_id:
                if task.claimed_by:
                    return False, f"Task claimed by {task.claimed_by}, not you"
                return False, "Task not claimed"

            task.claimed_by = None
            task.claimed_at = None
            task.status = TaskStatus.PENDING
            task.version += 1
            self._save_task_list(task_list)

            # Publish event
            TaskEventBroadcaster.publish_sync(
                TaskEventBroadcaster.create_event(
                    TaskEventBroadcaster.TASK_RELEASED,
                    task_list_id,
                    task_id,
                    released_by=session_id,
                    title=task.title,
                )
            )

            return True, "Released"

    # ─────────────────────────────────────────────────────────────
    # Session Management
    # ─────────────────────────────────────────────────────────────

    def join_task_list(self, task_list_id: str, session_id: str) -> None:
        """Register a session as active on a task list."""
        with self._get_lock(task_list_id):
            task_list = self.get_or_create_task_list(task_list_id)
            now = datetime.utcnow().isoformat()

            # Check if already joined
            for session in task_list.active_sessions:
                if session.get("id") == session_id:
                    session["last_heartbeat"] = now
                    self._save_task_list(task_list)
                    return

            # Add new session
            task_list.active_sessions.append(
                {
                    "id": session_id,
                    "joined_at": now,
                    "last_heartbeat": now,
                }
            )
            self._save_task_list(task_list)

    def leave_task_list(self, task_list_id: str, session_id: str) -> None:
        """Remove a session from a task list and release its tasks."""
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                return

            # Remove session
            task_list.active_sessions = [
                s for s in task_list.active_sessions if s.get("id") != session_id
            ]

            # Release tasks claimed by this session
            for task in task_list.tasks:
                if task.claimed_by == session_id:
                    task.claimed_by = None
                    task.claimed_at = None
                    if task.status == TaskStatus.IN_PROGRESS:
                        task.status = TaskStatus.PENDING

            self._save_task_list(task_list)

    def heartbeat(self, task_list_id: str, session_id: str) -> None:
        """Update session heartbeat."""
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                return

            now = datetime.utcnow().isoformat()
            for session in task_list.active_sessions:
                if session.get("id") == session_id:
                    session["last_heartbeat"] = now
                    break

            self._save_task_list(task_list)

    def get_active_sessions(self, task_list_id: str) -> list[dict[str, str]]:
        """Get list of active sessions on a task list."""
        task_list = self.get_task_list(task_list_id)
        if not task_list:
            return []
        return task_list.active_sessions

    def cleanup_stale_sessions(
        self, task_list_id: str, timeout_minutes: int = 5
    ) -> list[str]:
        """Remove stale sessions and release their tasks."""
        with self._get_lock(task_list_id):
            task_list = self.get_task_list(task_list_id)
            if not task_list:
                return []

            from datetime import timedelta

            cutoff = datetime.utcnow() - timedelta(minutes=timeout_minutes)
            cutoff_str = cutoff.isoformat()

            stale_sessions = []
            active_sessions = []

            for session in task_list.active_sessions:
                last_heartbeat = session.get("last_heartbeat", "")
                if last_heartbeat < cutoff_str:
                    stale_sessions.append(session.get("id", ""))
                else:
                    active_sessions.append(session)

            # Release tasks from stale sessions
            for session_id in stale_sessions:
                for task in task_list.tasks:
                    if task.claimed_by == session_id:
                        task.claimed_by = None
                        task.claimed_at = None
                        if task.status == TaskStatus.IN_PROGRESS:
                            task.status = TaskStatus.PENDING

            task_list.active_sessions = active_sessions
            self._save_task_list(task_list)

            return stale_sessions
