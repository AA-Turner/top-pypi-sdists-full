"""Protocols and interfaces for multiuser chat integration.

This module defines the core abstractions for shared sessions, enabling
multiple users to collaborate in a single agent conversation with real-time
synchronization across machines.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Protocol


# ─────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────


class ParticipantRole(str, Enum):
    """Role of a participant in a shared session."""

    OWNER = "owner"  # Can manage session, remove participants
    EDITOR = "editor"  # Can send messages
    VIEWER = "viewer"  # Read-only access


class SharedSessionState(str, Enum):
    """State of a shared session."""

    ACTIVE = "active"  # Ready for messages
    AGENT_BUSY = "agent_busy"  # Agent processing a message
    PAUSED = "paused"  # Temporarily paused
    CLOSED = "closed"  # Session ended


class SharedEventType(str, Enum):
    """Events specific to multiuser sessions."""

    # Session lifecycle
    SESSION_CREATED = "session_created"
    SESSION_JOINED = "session_joined"
    SESSION_LEFT = "session_left"
    SESSION_CLOSED = "session_closed"

    # Participant events
    PARTICIPANT_JOINED = "participant_joined"
    PARTICIPANT_LEFT = "participant_left"
    PARTICIPANT_TYPING = "participant_typing"

    # Message events
    MESSAGE_QUEUED = "message_queued"
    MESSAGE_DEQUEUED = "message_dequeued"
    MESSAGE_PROCESSING = "message_processing"

    # State events
    STATE_CHANGED = "state_changed"
    QUEUE_UPDATED = "queue_updated"

    # Sync events
    STATE_SYNCED = "state_synced"
    CONFLICT_DETECTED = "conflict_detected"
    FULL_SYNC_REQUIRED = "full_sync_required"

    # Owner processing events (for CLI-side agent execution)
    PROCESS_MESSAGE_REQUEST = "process_message_request"  # Request owner to process a queued message
    MESSAGE_RESPONSE = "message_response"  # Response from owner's agent

    # Team events
    TEAM_CREATED = "team_created"
    TEAM_MEMBER_JOINED = "team_member_joined"
    TEAM_MEMBER_LEFT = "team_member_left"
    SESSION_ADDED_TO_TEAM = "session_added_to_team"
    SESSION_REMOVED_FROM_TEAM = "session_removed_from_team"

    # Project events
    PROJECT_CREATED = "project_created"
    PROJECT_UPDATED = "project_updated"
    PROJECT_DELETED = "project_deleted"
    PROJECT_MEMBER_ADDED = "project_member_added"
    PROJECT_MEMBER_REMOVED = "project_member_removed"

    # Task events
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_ASSIGNED = "task_assigned"
    TASK_UNASSIGNED = "task_unassigned"
    TASK_STATUS_CHANGED = "task_status_changed"
    TASK_COMMENTED = "task_commented"
    TASK_SESSION_LINKED = "task_session_linked"


# ─────────────────────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────────────────────


@dataclass
class Participant:
    """A participant in a shared session."""

    user_id: str
    display_name: str
    role: ParticipantRole
    joined_at: str
    last_seen: str
    is_online: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "role": self.role.value,
            "joined_at": self.joined_at,
            "last_seen": self.last_seen,
            "is_online": self.is_online,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Participant":
        """Create from dictionary."""
        return cls(
            user_id=data["user_id"],
            display_name=data["display_name"],
            role=ParticipantRole(data["role"]),
            joined_at=data["joined_at"],
            last_seen=data["last_seen"],
            is_online=data.get("is_online", False),
            metadata=data.get("metadata", {}),
        )


@dataclass
class QueuedMessage:
    """A message waiting in the queue."""

    id: str
    user_id: str
    content: str
    images: list[dict] = field(default_factory=list)
    queued_at: str = ""
    priority: int = 0  # Higher = more urgent

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "images": self.images,
            "queued_at": self.queued_at,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QueuedMessage":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            content=data["content"],
            images=data.get("images", []),
            queued_at=data.get("queued_at", ""),
            priority=data.get("priority", 0),
        )


@dataclass
class SharedSessionInfo:
    """Lightweight metadata about a shared session (without full message history)."""

    session_id: str
    invite_code: str
    owner_id: str
    created_at: str
    state: SharedSessionState
    participants: list[Participant]
    message_queue: list[QueuedMessage]
    message_history_hash: str  # For sync verification
    version: int  # For optimistic locking

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "invite_code": self.invite_code,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "state": self.state.value,
            "participants": [p.to_dict() for p in self.participants],
            "message_queue": [m.to_dict() for m in self.message_queue],
            "message_history_hash": self.message_history_hash,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SharedSessionInfo":
        """Create from dictionary."""
        return cls(
            session_id=data["session_id"],
            invite_code=data["invite_code"],
            owner_id=data["owner_id"],
            created_at=data["created_at"],
            state=SharedSessionState(data["state"]),
            participants=[Participant.from_dict(p) for p in data.get("participants", [])],
            message_queue=[QueuedMessage.from_dict(m) for m in data.get("message_queue", [])],
            message_history_hash=data.get("message_history_hash", ""),
            version=data.get("version", 1),
        )


@dataclass
class SharedEvent:
    """An event in a shared session."""

    id: str
    session_id: str
    event_type: str  # SharedEventType or EventType value
    data: dict[str, Any]
    timestamp: str
    source_user_id: Optional[str] = None
    sequence: int = 0  # For ordering

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp,
            "source_user_id": self.source_user_id,
            "sequence": self.sequence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SharedEvent":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            session_id=data["session_id"],
            event_type=data["event_type"],
            data=data.get("data", {}),
            timestamp=data["timestamp"],
            source_user_id=data.get("source_user_id"),
            sequence=data.get("sequence", 0),
        )


# ─────────────────────────────────────────────────────────────
# PROTOCOLS
# ─────────────────────────────────────────────────────────────


class SharedEventHandler(Protocol):
    """Protocol for handling shared session events."""

    def handle(self, event: SharedEvent) -> None:
        """Handle a shared session event."""
        ...


# ─────────────────────────────────────────────────────────────
# EXCEPTIONS
# ─────────────────────────────────────────────────────────────


class MultiuserError(Exception):
    """Base exception for multiuser operations."""

    pass


class SessionNotFoundError(MultiuserError):
    """Session does not exist."""

    pass


class InvalidInviteCodeError(MultiuserError):
    """Invite code is invalid or expired."""

    pass


class ConflictError(MultiuserError):
    """State conflict during update (version mismatch)."""

    def __init__(self, message: str, current_version: int, expected_version: int):
        super().__init__(message)
        self.current_version = current_version
        self.expected_version = expected_version


class NotAuthorizedError(MultiuserError):
    """User is not authorized for this operation."""

    pass


class AgentBusyError(MultiuserError):
    """Agent is already processing a message."""

    pass


class TeamNotFoundError(MultiuserError):
    """Team does not exist."""

    pass


class InvalidTeamInviteError(MultiuserError):
    """Team invite code is invalid or expired."""

    pass


class TeamPermissionError(MultiuserError):
    """User does not have required team permissions."""

    pass
