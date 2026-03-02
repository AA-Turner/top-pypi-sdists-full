"""Data models for multiuser shared sessions.

This module contains the full SharedSession model and related classes
for managing collaborative agent conversations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
import hashlib
import json

from .protocols import (
    ParticipantRole,
    SharedSessionState,
    Participant,
    QueuedMessage,
    SharedSessionInfo,
)
from .teams import SessionVisibility


@dataclass
class SharedSession:
    """Full shared session state including conversation history.

    This extends SharedSessionInfo with the actual conversation data
    and is used for full state synchronization.

    Attributes:
        session_id: Unique identifier for this session
        invite_code: Human-readable code for inviting others
        owner_id: User ID of the session creator
        created_at: ISO timestamp of creation
        updated_at: ISO timestamp of last update
        state: Current session state
        version: Monotonic version for conflict detection
        participants: List of active participants
        message_queue: Pending messages when agent is busy
        messages: Full conversation history (same format as AgentRunner._messages)
        model: LLM model identifier
        plan_mode: Whether agent is in plan mode
        last_sync_at: When state was last synced
        sync_source: Machine ID that last synced
        title: Human-readable session title
        team_id: Optional team this session belongs to
        visibility: Session visibility (PRIVATE or TEAM)
    """

    # Core identity
    session_id: str
    invite_code: str
    owner_id: str

    # Timestamps
    created_at: str
    updated_at: str

    # State
    state: SharedSessionState = SharedSessionState.ACTIVE
    version: int = 1

    # Participants
    participants: list[Participant] = field(default_factory=list)

    # Message queue (pending messages when agent is busy)
    message_queue: list[QueuedMessage] = field(default_factory=list)

    # Conversation history (same format as AgentRunner._messages)
    messages: list[dict[str, Any]] = field(default_factory=list)

    # Human chat history — all user_message events (including chat-only).
    # Used to give the agent context about the team discussion when
    # invoked via @agent.  Each entry: {"user_id", "display_name", "content", "timestamp"}
    chat_history: list[dict[str, Any]] = field(default_factory=list)

    # Index into chat_history where the agent last consumed context.
    # On the next @agent invocation only chat_history[cursor:] is sent,
    # avoiding duplicate context the agent already has in its memory.
    chat_history_cursor: int = 0

    # Agent configuration
    model: str = ""
    plan_mode: bool = False
    repo_root: str = ""

    # Sync metadata
    last_sync_at: Optional[str] = None
    sync_source: Optional[str] = None  # Machine ID that last synced

    # Team integration
    title: str = ""  # Human-readable session title
    team_id: Optional[str] = None  # Team this session belongs to
    visibility: SessionVisibility = SessionVisibility.PRIVATE  # Default to private

    # Project integration
    project_id: Optional[str] = None  # Project this session is linked to
    task_id: Optional[str] = None  # Specific task this session is linked to

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "invite_code": self.invite_code,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "state": self.state.value,
            "version": self.version,
            "participants": [p.to_dict() for p in self.participants],
            "message_queue": [m.to_dict() for m in self.message_queue],
            "messages": self.messages,
            "chat_history": self.chat_history,
            "chat_history_cursor": self.chat_history_cursor,
            "model": self.model,
            "plan_mode": self.plan_mode,
            "repo_root": self.repo_root,
            "last_sync_at": self.last_sync_at,
            "sync_source": self.sync_source,
            "title": self.title,
            "team_id": self.team_id,
            "visibility": self.visibility.value,
            "project_id": self.project_id,
            "task_id": self.task_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SharedSession":
        """Create from dictionary."""
        participants = [
            Participant.from_dict(p) for p in data.get("participants", [])
        ]

        message_queue = [
            QueuedMessage.from_dict(m) for m in data.get("message_queue", [])
        ]

        # Parse visibility
        visibility_str = data.get("visibility", "private")
        try:
            visibility = SessionVisibility(visibility_str)
        except ValueError:
            visibility = SessionVisibility.PRIVATE

        return cls(
            session_id=data["session_id"],
            invite_code=data["invite_code"],
            owner_id=data["owner_id"],
            created_at=data["created_at"],
            updated_at=data.get("updated_at", data["created_at"]),
            state=SharedSessionState(data.get("state", "active")),
            version=data.get("version", 1),
            participants=participants,
            message_queue=message_queue,
            messages=data.get("messages", []),
            chat_history=data.get("chat_history", []),
            chat_history_cursor=data.get("chat_history_cursor", 0),
            model=data.get("model", ""),
            plan_mode=data.get("plan_mode", False),
            repo_root=data.get("repo_root", ""),
            last_sync_at=data.get("last_sync_at"),
            sync_source=data.get("sync_source"),
            title=data.get("title", ""),
            team_id=data.get("team_id"),
            visibility=visibility,
            project_id=data.get("project_id"),
            task_id=data.get("task_id"),
        )

    def get_info(self) -> SharedSessionInfo:
        """Get lightweight session info (without message history)."""
        return SharedSessionInfo(
            session_id=self.session_id,
            invite_code=self.invite_code,
            owner_id=self.owner_id,
            created_at=self.created_at,
            state=self.state,
            participants=self.participants,
            message_queue=self.message_queue,
            message_history_hash=self.compute_message_hash(),
            version=self.version,
        )

    def compute_message_hash(self) -> str:
        """Compute hash of message history for sync verification."""
        content = json.dumps(self.messages, sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_participant(self, user_id: str) -> Optional[Participant]:
        """Get a participant by user ID."""
        for p in self.participants:
            if p.user_id == user_id:
                return p
        return None

    def add_participant(self, participant: Participant) -> None:
        """Add a participant to the session."""
        # Remove if already exists (rejoin)
        self.participants = [p for p in self.participants if p.user_id != participant.user_id]
        self.participants.append(participant)
        self._touch()

    def remove_participant(self, user_id: str) -> bool:
        """Remove a participant from the session.

        Returns:
            True if participant was removed, False if not found
        """
        original_len = len(self.participants)
        self.participants = [p for p in self.participants if p.user_id != user_id]
        if len(self.participants) < original_len:
            self._touch()
            return True
        return False

    def update_participant_presence(self, user_id: str, is_online: bool) -> None:
        """Update participant online status."""
        for p in self.participants:
            if p.user_id == user_id:
                p.is_online = is_online
                p.last_seen = datetime.utcnow().isoformat()
                self._touch()
                break

    def enqueue_message(self, message: QueuedMessage) -> int:
        """Add a message to the queue.

        Returns:
            Position in queue (0-indexed)
        """
        # Insert by priority (higher first), then by time
        inserted = False
        for i, existing in enumerate(self.message_queue):
            if message.priority > existing.priority:
                self.message_queue.insert(i, message)
                inserted = True
                break

        if not inserted:
            self.message_queue.append(message)

        self._touch()
        return self.get_queue_position(message.id) or 0

    def dequeue_message(self) -> Optional[QueuedMessage]:
        """Remove and return the next message from queue."""
        if not self.message_queue:
            return None

        message = self.message_queue.pop(0)
        self.state = SharedSessionState.AGENT_BUSY
        self._touch()
        return message

    def get_queue_position(self, message_id: str) -> Optional[int]:
        """Get position of a message in queue (0-indexed)."""
        for i, msg in enumerate(self.message_queue):
            if msg.id == message_id:
                return i
        return None

    def is_owner(self, user_id: str) -> bool:
        """Check if user is the session owner."""
        return self.owner_id == user_id

    def can_send_message(self, user_id: str) -> bool:
        """Check if user can send messages."""
        participant = self.get_participant(user_id)
        if not participant:
            return False
        return participant.role in (ParticipantRole.OWNER, ParticipantRole.EDITOR)

    def _touch(self) -> None:
        """Update timestamps and version."""
        self.updated_at = datetime.utcnow().isoformat()
        self.version += 1


@dataclass
class InviteToken:
    """Invite token for joining a session.

    Invite codes are human-readable and can have expiration and usage limits.
    """

    code: str
    session_id: str
    created_by: str
    created_at: str
    expires_at: str
    max_uses: int = 10
    use_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "code": self.code,
            "session_id": self.session_id,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "max_uses": self.max_uses,
            "use_count": self.use_count,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InviteToken":
        """Create from dictionary."""
        return cls(
            code=data["code"],
            session_id=data["session_id"],
            created_by=data["created_by"],
            created_at=data["created_at"],
            expires_at=data["expires_at"],
            max_uses=data.get("max_uses", 10),
            use_count=data.get("use_count", 0),
        )

    def is_valid(self) -> bool:
        """Check if invite is still valid."""
        now = datetime.utcnow().isoformat()
        return self.use_count < self.max_uses and now < self.expires_at

    def use(self) -> bool:
        """Attempt to use the invite.

        Returns:
            True if used successfully, False if invalid
        """
        if not self.is_valid():
            return False
        self.use_count += 1
        return True


@dataclass
class UserIdentity:
    """Identity of a user in the multiuser system.

    This provides a consistent way to identify users across sessions,
    supporting various identity sources.
    """

    user_id: str  # Unique identifier
    display_name: str  # Human-readable name
    source: str = "local"  # Identity source: local, github, etc.
    avatar_url: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "source": self.source,
            "avatar_url": self.avatar_url,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserIdentity":
        """Create from dictionary."""
        return cls(
            user_id=data["user_id"],
            display_name=data["display_name"],
            source=data.get("source", "local"),
            avatar_url=data.get("avatar_url"),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def anonymous(cls, display_name: str) -> "UserIdentity":
        """Create an anonymous user identity."""
        import uuid
        return cls(
            user_id=f"anon_{uuid.uuid4().hex[:12]}",
            display_name=display_name,
            source="anonymous",
        )

    @classmethod
    def from_machine(cls) -> "UserIdentity":
        """Create identity from machine info."""
        import uuid
        import socket
        import os

        # Try to get a stable machine ID
        try:
            hostname = socket.gethostname()
            username = os.environ.get("USER", os.environ.get("USERNAME", "user"))
            machine_id = hashlib.sha256(f"{hostname}:{username}".encode()).hexdigest()[:12]
            display_name = f"{username}@{hostname}"
        except Exception:
            machine_id = uuid.uuid4().hex[:12]
            display_name = "Unknown User"

        return cls(
            user_id=f"machine_{machine_id}",
            display_name=display_name,
            source="machine",
        )
