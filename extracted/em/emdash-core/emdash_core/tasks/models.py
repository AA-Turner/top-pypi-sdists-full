"""Data models for Tasks v2 system."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any


class TaskStatus(Enum):
    """Status of a task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"  # Computed: has incomplete dependencies


@dataclass
class Task:
    """A task with labels and dependencies."""

    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING

    # Dependencies - task IDs that must complete first
    depends_on: list[str] = field(default_factory=list)

    # Labels for clustering/filtering (NOT assignment)
    labels: list[str] = field(default_factory=list)

    # Claiming (who IS working on it - assigned at runtime)
    claimed_by: str | None = None
    claimed_at: str | None = None

    # Metadata
    created_at: str = ""
    updated_at: str = ""
    created_by: str = ""  # Session ID that created

    # Ordering
    priority: int = 0  # Higher = more important
    order: int = 0  # Display order

    # Conflict detection
    version: int = 1  # Increments on each update

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create from dictionary."""
        data = data.copy()
        if "status" in data:
            data["status"] = TaskStatus(data["status"])
        return cls(**data)


@dataclass
class TaskList:
    """A named collection of tasks that can be shared across sessions."""

    id: str  # Unique identifier
    name: str  # Human-readable name
    description: str = ""
    tasks: list[Task] = field(default_factory=list)

    # Metadata
    created_at: str = ""
    updated_at: str = ""

    # Collaboration - list of {id, joined_at, last_heartbeat}
    active_sessions: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tasks": [t.to_dict() for t in self.tasks],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "active_sessions": self.active_sessions,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskList":
        """Create from dictionary."""
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            tasks=tasks,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            active_sessions=data.get("active_sessions", []),
        )

    def get_task(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


@dataclass
class TaskEvent:
    """Event for task updates (used for broadcasting)."""

    type: str  # task_added, task_updated, task_completed, task_list_updated
    task_list_id: str
    task_id: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
