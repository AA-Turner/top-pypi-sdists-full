"""Business logic for project and task management.

Core owns the actions (API endpoints) and business logic (validation,
permissions, state transitions). State is held in-memory for fast reads.
On every mutation, core fires a webhook so the consumer can persist
to whatever backend they choose.

The consumer is responsible for:
- Durable storage (Firebase, SQLite, etc.)
- Syncing initial state to core on startup via the sync endpoint
- Receiving webhooks for ongoing mutations

Core is responsible for:
- Validation and permission checks
- In-memory state (source of truth during runtime)
- Firing webhooks on every mutation
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Optional

from .projects import (
    Project,
    ProjectMember,
    ProjectRole,
    Task,
    TaskComment,
    TaskStatus,
    TaskPriority,
)
from .webhooks import WebhookRegistry, get_webhook_registry

log = logging.getLogger(__name__)


class ProjectManager:
    """Orchestrates project and task operations with in-memory state.

    All reads come from in-memory state (fast, no I/O).
    All writes mutate in-memory state AND fire webhooks.

    Usage:
        manager = ProjectManager()

        # Consumer syncs initial state from their store
        await manager.sync_projects([{...}, {...}])
        await manager.sync_tasks([{...}, {...}])

        # Operations mutate state + fire webhooks
        project = await manager.create_project(...)
        task = await manager.create_task(...)
    """

    def __init__(self, webhook_registry: Optional[WebhookRegistry] = None):
        self._webhooks = webhook_registry or get_webhook_registry()

        # In-memory state
        self._projects: dict[str, Project] = {}
        self._tasks: dict[str, Task] = {}

        # Indexes
        self._project_tasks: dict[str, set[str]] = {}  # project_id -> task_ids
        self._user_tasks: dict[str, set[str]] = {}  # user_id -> task_ids

    # ─────────────────────────────────────────────────────────
    # Sync (consumer pushes initial state on startup)
    # ─────────────────────────────────────────────────────────

    def sync_projects(self, project_dicts: list[dict[str, Any]]) -> int:
        """Load projects into in-memory state from consumer's store.

        Called at startup so core has data to serve reads from.
        Returns count of projects loaded.
        """
        count = 0
        for d in project_dicts:
            project = Project.from_dict(d)
            self._projects[project.project_id] = project
            count += 1
        log.info(f"Synced {count} projects into memory")
        return count

    def sync_tasks(self, task_dicts: list[dict[str, Any]]) -> int:
        """Load tasks into in-memory state from consumer's store.

        Called at startup so core has data to serve reads from.
        Returns count of tasks loaded.
        """
        count = 0
        for d in task_dicts:
            task = Task.from_dict(d)
            self._tasks[task.task_id] = task
            self._project_tasks.setdefault(task.project_id, set()).add(
                task.task_id
            )
            if task.assignee_id:
                self._user_tasks.setdefault(task.assignee_id, set()).add(
                    task.task_id
                )
            count += 1
        log.info(f"Synced {count} tasks into memory")
        return count

    # ─────────────────────────────────────────────────────────
    # Project Operations
    # ─────────────────────────────────────────────────────────

    async def create_project(
        self,
        name: str,
        creator_id: str,
        creator_name: str,
        description: str = "",
        repo_links: Optional[list[str]] = None,
    ) -> Project:
        """Create a new project. Fires project.created webhook."""
        project_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        lead = ProjectMember(
            user_id=creator_id,
            display_name=creator_name,
            role=ProjectRole.LEAD,
            joined_at=now,
        )

        project = Project(
            project_id=project_id,
            name=name,
            description=description,
            repo_links=repo_links or [],
            created_by=creator_id,
            created_at=now,
            updated_at=now,
            members=[lead],
        )

        # Store in memory
        self._projects[project_id] = project

        # Fire webhook
        await self._webhooks.dispatch("project.created", project.to_dict())

        log.info(f"Created project '{name}' ({project_id})")
        return project

    async def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID (from memory)."""
        return self._projects.get(project_id)

    async def list_projects(self) -> list[Project]:
        """List all projects (from memory)."""
        return list(self._projects.values())

    async def update_project(
        self, project_id: str, updates: dict[str, Any]
    ) -> Optional[Project]:
        """Update project fields. Fires project.updated webhook."""
        project = self._projects.get(project_id)
        if not project:
            return None

        if "name" in updates:
            project.name = updates["name"]
        if "description" in updates:
            project.description = updates["description"]
        if "repo_links" in updates:
            project.repo_links = updates["repo_links"]
        if "settings" in updates:
            project.settings.update(updates["settings"])

        project.updated_at = datetime.utcnow().isoformat()

        await self._webhooks.dispatch("project.updated", project.to_dict())
        return project

    async def delete_project(self, project_id: str, user_id: str) -> bool:
        """Delete project + tasks. Fires project.deleted webhook."""
        project = self._projects.get(project_id)
        if not project:
            return False

        if not project.is_lead(user_id):
            raise PermissionError("Only project leads can delete projects")

        # Remove tasks
        task_ids = list(self._project_tasks.get(project_id, set()))
        for tid in task_ids:
            task = self._tasks.pop(tid, None)
            if task and task.assignee_id:
                self._user_tasks.get(task.assignee_id, set()).discard(tid)
        self._project_tasks.pop(project_id, None)

        # Remove project
        self._projects.pop(project_id, None)

        await self._webhooks.dispatch(
            "project.deleted", {"project_id": project_id}
        )

        log.info(f"Deleted project {project_id}")
        return True

    async def add_project_member(
        self,
        project_id: str,
        user_id: str,
        display_name: str,
        role: ProjectRole = ProjectRole.CONTRIBUTOR,
    ) -> Optional[ProjectMember]:
        """Add member. Fires project.member_added webhook."""
        project = self._projects.get(project_id)
        if not project:
            return None

        member = project.add_member(user_id, display_name, role)

        await self._webhooks.dispatch(
            "project.member_added",
            {"project_id": project_id, "member": member.to_dict()},
        )
        return member

    async def remove_project_member(
        self, project_id: str, user_id: str
    ) -> bool:
        """Remove member. Fires project.member_removed webhook."""
        project = self._projects.get(project_id)
        if not project:
            return False

        if not project.remove_member(user_id):
            return False

        await self._webhooks.dispatch(
            "project.member_removed",
            {"project_id": project_id, "user_id": user_id},
        )
        return True

    # ─────────────────────────────────────────────────────────
    # Task Operations
    # ─────────────────────────────────────────────────────────

    async def create_task(
        self,
        project_id: str,
        title: str,
        reporter_id: str,
        reporter_name: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        assignee_id: Optional[str] = None,
        assignee_name: Optional[str] = None,
        due_date: Optional[str] = None,
        labels: Optional[list[str]] = None,
        linked_session_id: Optional[str] = None,
    ) -> Task:
        """Create a task. Fires task.created webhook."""
        task_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        task = Task(
            task_id=task_id,
            project_id=project_id,
            title=title,
            description=description,
            status=TaskStatus.OPEN,
            priority=priority,
            assignee_id=assignee_id,
            assignee_name=assignee_name,
            reporter_id=reporter_id,
            reporter_name=reporter_name,
            created_at=now,
            updated_at=now,
            due_date=due_date,
            labels=labels or [],
            linked_session_id=linked_session_id,
        )

        # Store in memory + index
        self._tasks[task_id] = task
        self._project_tasks.setdefault(project_id, set()).add(task_id)
        if assignee_id:
            self._user_tasks.setdefault(assignee_id, set()).add(task_id)

        await self._webhooks.dispatch("task.created", task.to_dict())

        log.info(f"Created task '{title}' ({task_id}) in project {project_id}")
        return task

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID (from memory)."""
        return self._tasks.get(task_id)

    async def list_project_tasks(
        self,
        project_id: str,
        status: Optional[TaskStatus] = None,
        assignee_id: Optional[str] = None,
    ) -> list[Task]:
        """List tasks in a project (from memory), optionally filtered."""
        task_ids = self._project_tasks.get(project_id, set())
        tasks = [self._tasks[tid] for tid in task_ids if tid in self._tasks]

        if status:
            tasks = [t for t in tasks if t.status == status]
        if assignee_id:
            tasks = [t for t in tasks if t.assignee_id == assignee_id]

        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3,
        }
        tasks.sort(key=lambda t: (priority_order.get(t.priority, 2), t.created_at))
        return tasks

    async def update_task(
        self, task_id: str, updates: dict[str, Any]
    ) -> Optional[Task]:
        """Update task fields. Fires task.updated webhook."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        if "title" in updates:
            task.title = updates["title"]
        if "description" in updates:
            task.description = updates["description"]
        if "priority" in updates:
            task.priority = TaskPriority(updates["priority"])
        if "due_date" in updates:
            task.due_date = updates["due_date"]
        if "labels" in updates:
            task.labels = updates["labels"]
        if "linked_session_id" in updates:
            task.linked_session_id = updates["linked_session_id"]
        if "metadata" in updates:
            task.metadata.update(updates["metadata"])

        task._touch()

        await self._webhooks.dispatch("task.updated", task.to_dict())
        return task

    async def assign_task(
        self, task_id: str, assignee_id: str, assignee_name: str
    ) -> Optional[Task]:
        """Assign task. Fires task.assigned webhook."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        # Update user_tasks index
        if task.assignee_id:
            self._user_tasks.get(task.assignee_id, set()).discard(task_id)

        task.assign(assignee_id, assignee_name)
        self._user_tasks.setdefault(assignee_id, set()).add(task_id)

        await self._webhooks.dispatch("task.assigned", task.to_dict())

        log.info(f"Assigned task {task_id} to {assignee_name} ({assignee_id})")
        return task

    async def unassign_task(self, task_id: str) -> Optional[Task]:
        """Unassign task. Fires task.unassigned webhook."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        if task.assignee_id:
            self._user_tasks.get(task.assignee_id, set()).discard(task_id)

        task.unassign()

        await self._webhooks.dispatch("task.unassigned", task.to_dict())
        return task

    async def transition_task(
        self, task_id: str, new_status: TaskStatus
    ) -> Optional[Task]:
        """Transition task status. Fires task.status_changed webhook."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        old_status = task.status.value
        task.transition(new_status)

        await self._webhooks.dispatch(
            "task.status_changed",
            {**task.to_dict(), "old_status": old_status},
        )

        log.info(f"Task {task_id} transitioned to {new_status.value}")
        return task

    async def add_task_comment(
        self, task_id: str, user_id: str, display_name: str, content: str
    ) -> Optional[TaskComment]:
        """Add comment. Fires task.commented webhook."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        comment = task.add_comment(user_id, display_name, content)

        await self._webhooks.dispatch(
            "task.commented",
            {"task_id": task_id, "comment": comment.to_dict()},
        )
        return comment

    async def delete_task(self, task_id: str) -> bool:
        """Delete task. Fires task.deleted webhook."""
        task = self._tasks.pop(task_id, None)
        if not task:
            return False

        self._project_tasks.get(task.project_id, set()).discard(task_id)
        if task.assignee_id:
            self._user_tasks.get(task.assignee_id, set()).discard(task_id)

        await self._webhooks.dispatch(
            "task.deleted",
            {"task_id": task_id, "project_id": task.project_id},
        )

        log.info(f"Deleted task {task_id}")
        return True

    async def get_user_tasks(
        self, user_id: str, status: Optional[TaskStatus] = None
    ) -> list[Task]:
        """Get all tasks assigned to a user (from memory)."""
        task_ids = self._user_tasks.get(user_id, set())
        tasks = [self._tasks[tid] for tid in task_ids if tid in self._tasks]

        if status:
            tasks = [t for t in tasks if t.status == status]

        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3,
        }
        tasks.sort(key=lambda t: (priority_order.get(t.priority, 2), t.created_at))
        return tasks

    async def link_task_to_session(
        self, task_id: str, session_id: str
    ) -> Optional[Task]:
        """Link session. Fires task.session_linked webhook."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        task.link_session(session_id)

        await self._webhooks.dispatch("task.session_linked", task.to_dict())
        return task


# ─────────────────────────────────────────────────────────────
# Global Instance
# ─────────────────────────────────────────────────────────────

_project_manager: Optional[ProjectManager] = None


def get_project_manager() -> ProjectManager:
    """Get the global ProjectManager instance.

    Auto-creates one if not set — unlike the store-based version,
    webhooks don't require upfront registration to function.
    """
    global _project_manager
    if _project_manager is None:
        _project_manager = ProjectManager()
    return _project_manager


def set_project_manager(manager: ProjectManager) -> None:
    """Set the global ProjectManager instance."""
    global _project_manager
    _project_manager = manager
