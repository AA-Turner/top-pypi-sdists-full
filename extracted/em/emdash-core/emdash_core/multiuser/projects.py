"""Data models for project and task management.

This module contains ONLY pure data types — no I/O, no persistence,
no business logic orchestration. These types define the shape of
projects, tasks, and related entities.

Business logic lives in project_manager.py.
Storage implementations live in the consumer layer (CLI, etc.).
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


# ─────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────


class TaskStatus(str, Enum):
    """Status of a task."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Priority level of a task."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProjectRole(str, Enum):
    """Role of a member within a project."""

    LEAD = "lead"  # Can manage project settings, tasks, and members
    CONTRIBUTOR = "contributor"  # Can create/edit tasks, be assigned
    OBSERVER = "observer"  # Read-only access to project and tasks


# ─────────────────────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────────────────────


@dataclass
class TaskComment:
    """A comment on a task."""

    comment_id: str
    task_id: str
    user_id: str
    display_name: str
    content: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "comment_id": self.comment_id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "display_name": self.display_name,
            "content": self.content,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskComment":
        return cls(
            comment_id=data["comment_id"],
            task_id=data["task_id"],
            user_id=data["user_id"],
            display_name=data.get("display_name", "Unknown"),
            content=data["content"],
            created_at=data["created_at"],
        )


@dataclass
class Task:
    """A task within a project.

    Tasks represent units of work that can be assigned to team members,
    tracked through a lifecycle, and optionally linked to agent sessions.
    """

    task_id: str
    project_id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.OPEN
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: Optional[str] = None
    assignee_name: Optional[str] = None
    reporter_id: str = ""
    reporter_name: str = ""
    created_at: str = ""
    updated_at: str = ""
    due_date: Optional[str] = None
    labels: list[str] = field(default_factory=list)
    comments: list[TaskComment] = field(default_factory=list)
    linked_session_id: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "assignee_id": self.assignee_id,
            "assignee_name": self.assignee_name,
            "reporter_id": self.reporter_id,
            "reporter_name": self.reporter_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_date": self.due_date,
            "labels": self.labels,
            "comments": [c.to_dict() for c in self.comments],
            "linked_session_id": self.linked_session_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        comments = [TaskComment.from_dict(c) for c in data.get("comments", [])]

        status = TaskStatus.OPEN
        try:
            status = TaskStatus(data.get("status", "open"))
        except ValueError:
            pass

        priority = TaskPriority.MEDIUM
        try:
            priority = TaskPriority(data.get("priority", "medium"))
        except ValueError:
            pass

        return cls(
            task_id=data["task_id"],
            project_id=data["project_id"],
            title=data["title"],
            description=data.get("description", ""),
            status=status,
            priority=priority,
            assignee_id=data.get("assignee_id"),
            assignee_name=data.get("assignee_name"),
            reporter_id=data.get("reporter_id", ""),
            reporter_name=data.get("reporter_name", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            due_date=data.get("due_date"),
            labels=data.get("labels", []),
            comments=comments,
            linked_session_id=data.get("linked_session_id"),
            metadata=data.get("metadata", {}),
        )

    def assign(self, user_id: str, display_name: str) -> None:
        """Assign the task to a user."""
        self.assignee_id = user_id
        self.assignee_name = display_name
        self._touch()

    def unassign(self) -> None:
        """Remove the current assignee."""
        self.assignee_id = None
        self.assignee_name = None
        self._touch()

    def transition(self, new_status: TaskStatus) -> None:
        """Transition the task to a new status."""
        self.status = new_status
        self._touch()

    def add_comment(
        self, user_id: str, display_name: str, content: str
    ) -> TaskComment:
        """Add a comment to the task."""
        comment = TaskComment(
            comment_id=str(uuid.uuid4()),
            task_id=self.task_id,
            user_id=user_id,
            display_name=display_name,
            content=content,
            created_at=datetime.utcnow().isoformat(),
        )
        self.comments.append(comment)
        self._touch()
        return comment

    def link_session(self, session_id: str) -> None:
        """Link an agent session to this task."""
        self.linked_session_id = session_id
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.utcnow().isoformat()


@dataclass
class ProjectMember:
    """A member of a project (subset of the owning team)."""

    user_id: str
    display_name: str
    role: ProjectRole
    joined_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "role": self.role.value,
            "joined_at": self.joined_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectMember":
        role = ProjectRole.CONTRIBUTOR
        try:
            role = ProjectRole(data.get("role", "contributor"))
        except ValueError:
            pass
        return cls(
            user_id=data["user_id"],
            display_name=data["display_name"],
            role=role,
            joined_at=data["joined_at"],
            metadata=data.get("metadata", {}),
        )


@dataclass
class Project:
    """A project for organizing tasks and collaboration.

    Projects are self-contained entities with their own members,
    repository links, and tasks. No team dependency required.
    """

    project_id: str
    name: str = ""
    description: str = ""
    repo_links: list[str] = field(default_factory=list)
    created_by: str = ""
    created_at: str = ""
    updated_at: str = ""
    members: list[ProjectMember] = field(default_factory=list)
    settings: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "repo_links": self.repo_links,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "members": [m.to_dict() for m in self.members],
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Project":
        members = [ProjectMember.from_dict(m) for m in data.get("members", [])]
        # Backward compat: accept old team_id field silently
        return cls(
            project_id=data["project_id"],
            name=data.get("name", ""),
            description=data.get("description", ""),
            repo_links=data.get("repo_links", []),
            created_by=data.get("created_by", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            members=members,
            settings=data.get("settings", {}),
        )

    def get_member(self, user_id: str) -> Optional[ProjectMember]:
        for m in self.members:
            if m.user_id == user_id:
                return m
        return None

    def is_member(self, user_id: str) -> bool:
        return self.get_member(user_id) is not None

    def is_lead(self, user_id: str) -> bool:
        member = self.get_member(user_id)
        return member is not None and member.role == ProjectRole.LEAD

    def add_member(
        self,
        user_id: str,
        display_name: str,
        role: ProjectRole = ProjectRole.CONTRIBUTOR,
    ) -> ProjectMember:
        existing = self.get_member(user_id)
        if existing:
            existing.display_name = display_name
            return existing

        member = ProjectMember(
            user_id=user_id,
            display_name=display_name,
            role=role,
            joined_at=datetime.utcnow().isoformat(),
        )
        self.members.append(member)
        self.updated_at = datetime.utcnow().isoformat()
        return member

    def remove_member(self, user_id: str) -> bool:
        if user_id == self.created_by:
            return False
        original_len = len(self.members)
        self.members = [m for m in self.members if m.user_id != user_id]
        if len(self.members) < original_len:
            self.updated_at = datetime.utcnow().isoformat()
            return True
        return False
