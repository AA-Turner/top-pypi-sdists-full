"""Data models for checkpoint system."""

from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class CheckpointMetadata:
    """Metadata stored in commit message and index.

    This is the lightweight metadata that can be parsed from
    commit messages and stored in the index for fast lookup.
    """
    id: str
    session_id: str
    iteration: int
    timestamp: str
    commit_sha: Optional[str] = None
    summary: str = ""
    tools_used: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    token_usage: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CheckpointMetadata":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ConversationState:
    """Full conversation state for restoration.

    This is the complete state needed to restore an agent
    session, including all messages and context.
    """
    messages: list[dict]
    model: str
    system_prompt_hash: str
    token_usage: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": "1.0",
            "messages": self.messages,
            "model": self.model,
            "system_prompt_hash": self.system_prompt_hash,
            "token_usage": self.token_usage,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConversationState":
        """Create from dictionary."""
        return cls(
            messages=data.get("messages", []),
            model=data.get("model", ""),
            system_prompt_hash=data.get("system_prompt_hash", ""),
            token_usage=data.get("token_usage", {}),
        )


@dataclass
class CheckpointIndex:
    """Index of all checkpoints for fast lookup.

    Stored at .emdash/checkpoints/index.json
    """
    version: str = "1.0"
    checkpoints: list[CheckpointMetadata] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "checkpoints": [cp.to_dict() for cp in self.checkpoints],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CheckpointIndex":
        """Create from dictionary."""
        return cls(
            version=data.get("version", "1.0"),
            checkpoints=[
                CheckpointMetadata.from_dict(cp)
                for cp in data.get("checkpoints", [])
            ],
        )

    def add(self, metadata: CheckpointMetadata) -> None:
        """Add a checkpoint to the index."""
        self.checkpoints.insert(0, metadata)  # Most recent first

    def find(self, checkpoint_id: str) -> Optional[CheckpointMetadata]:
        """Find a checkpoint by ID."""
        for cp in self.checkpoints:
            if cp.id == checkpoint_id:
                return cp
        return None

    def find_by_session(self, session_id: str) -> list[CheckpointMetadata]:
        """Find all checkpoints for a session."""
        return [cp for cp in self.checkpoints if cp.session_id == session_id]
