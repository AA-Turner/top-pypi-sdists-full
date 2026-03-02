"""Data models for Agent Teams.

All persistent team state is stored as JSON files under:
  ~/.emdash/teams/{team-name}/config.json   — team configuration
  ~/.emdash/teams/{team-name}/tasks.json    — shared task list (delegates to Tasks v2)
  ~/.emdash/teams/{team-name}/mailbox/      — inter-agent messages
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


# ─────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────


class TeamStatus(str, Enum):
    """Lifecycle status of an agent team."""

    CREATING = "creating"      # Lead is spawning teammates
    ACTIVE = "active"          # Team is working
    WINDING_DOWN = "winding_down"  # Shutting down teammates
    CLEANED_UP = "cleaned_up"  # Resources removed


class TeammateStatus(str, Enum):
    """Status of an individual teammate."""

    SPAWNING = "spawning"      # Being initialized
    IDLE = "idle"              # Waiting for work
    WORKING = "working"        # Processing a task
    PLAN_MODE = "plan_mode"    # Planning before implementation
    SHUTTING_DOWN = "shutting_down"  # Graceful shutdown requested
    STOPPED = "stopped"        # Session ended


class TeammateRole(str, Enum):
    """Role in the team hierarchy."""

    LEAD = "lead"              # Coordinator — spawns, assigns, synthesizes
    TEAMMATE = "teammate"      # Worker — claims tasks, reports findings


class MessageType(str, Enum):
    """Types of inter-agent messages."""

    # Direct communication
    MESSAGE = "message"                # One-to-one message
    BROADCAST = "broadcast"            # One-to-all from lead

    # Lifecycle signals
    SPAWN_PROMPT = "spawn_prompt"      # Initial instructions from lead
    SHUTDOWN_REQUEST = "shutdown_request"
    SHUTDOWN_ACK = "shutdown_ack"
    SHUTDOWN_REJECT = "shutdown_reject"

    # Task coordination
    TASK_ASSIGNED = "task_assigned"     # Lead assigns a task
    TASK_UPDATE = "task_update"         # Progress report
    TASK_COMPLETED = "task_completed"   # Task done notification
    FINDINGS_REPORT = "findings_report" # Teammate shares findings

    # Plan mode
    PLAN_SUBMITTED = "plan_submitted"   # Teammate submits plan for approval
    PLAN_APPROVED = "plan_approved"     # Lead approves plan
    PLAN_REJECTED = "plan_rejected"     # Lead rejects with feedback

    # Status
    IDLE_NOTIFICATION = "idle_notification"  # Teammate went idle


class TeamEventType(str, Enum):
    """Events emitted by the team system (extends EventType)."""

    # Team lifecycle
    TEAM_CREATED = "team_created"
    TEAM_CLEANED_UP = "team_cleaned_up"

    # Teammate lifecycle
    TEAMMATE_SPAWNED = "teammate_spawned"
    TEAMMATE_IDLE = "teammate_idle"
    TEAMMATE_STOPPED = "teammate_stopped"

    # Messaging
    TEAM_MESSAGE_SENT = "team_message_sent"
    TEAM_MESSAGE_DELIVERED = "team_message_delivered"

    # Tasks
    TEAM_TASK_CREATED = "team_task_created"
    TEAM_TASK_CLAIMED = "team_task_claimed"
    TEAM_TASK_COMPLETED = "team_task_completed"
    TEAM_TASK_BLOCKED = "team_task_blocked"

    # Delegate mode
    DELEGATE_MODE_CHANGED = "delegate_mode_changed"


# ─────────────────────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────────────────────


@dataclass
class TeammateConfig:
    """Configuration for a single teammate in the team.

    Stored in config.json and used to spawn/reconnect agents.
    """

    name: str                           # Human-readable name (e.g., "security-reviewer")
    agent_id: str                       # Unique session/agent ID
    role: TeammateRole                  # lead or teammate
    model: str = ""                     # LLM model override (empty = use lead's model)
    status: TeammateStatus = TeammateStatus.SPAWNING
    spawn_prompt: str = ""              # Instructions given at spawn
    require_plan_approval: bool = False # Must plan before implementing
    labels: list[str] = field(default_factory=list)  # Labels for task filtering
    worktree_path: str | None = None   # Git worktree path (if isolated)
    spawned_at: str = ""
    stopped_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "agent_id": self.agent_id,
            "role": self.role.value,
            "model": self.model,
            "status": self.status.value,
            "spawn_prompt": self.spawn_prompt,
            "require_plan_approval": self.require_plan_approval,
            "labels": self.labels,
            "worktree_path": self.worktree_path,
            "spawned_at": self.spawned_at,
            "stopped_at": self.stopped_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TeammateConfig":
        return cls(
            name=data["name"],
            agent_id=data["agent_id"],
            role=TeammateRole(data["role"]),
            model=data.get("model", ""),
            status=TeammateStatus(data.get("status", "spawning")),
            spawn_prompt=data.get("spawn_prompt", ""),
            require_plan_approval=data.get("require_plan_approval", False),
            labels=data.get("labels", []),
            worktree_path=data.get("worktree_path"),
            spawned_at=data.get("spawned_at", ""),
            stopped_at=data.get("stopped_at", ""),
        )


@dataclass
class TeamConfig:
    """Top-level team configuration stored at ~/.emdash/teams/{name}/config.json.

    This is the persistent representation of a team.
    TeamManager loads this to reconstruct team state.
    """

    name: str                                  # Team name (also directory name)
    status: TeamStatus = TeamStatus.CREATING
    lead: TeammateConfig | None = None         # The lead's config
    members: list[TeammateConfig] = field(default_factory=list)
    task_list_id: str = ""                     # Tasks v2 task list ID
    delegate_mode: bool = False                # Lead restricted to coordination
    repo_root: str = ""                        # Working directory
    created_at: str = ""
    updated_at: str = ""

    # Settings
    settings: dict[str, Any] = field(default_factory=lambda: {
        "default_model": "",                   # Default model for teammates
        "max_teammates": 10,                   # Safety limit
        "auto_cleanup": True,                  # Clean up when lead exits
    })

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "lead": self.lead.to_dict() if self.lead else None,
            "members": [m.to_dict() for m in self.members],
            "task_list_id": self.task_list_id,
            "delegate_mode": self.delegate_mode,
            "repo_root": self.repo_root,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TeamConfig":
        return cls(
            name=data["name"],
            status=TeamStatus(data.get("status", "creating")),
            lead=TeammateConfig.from_dict(data["lead"]) if data.get("lead") else None,
            members=[TeammateConfig.from_dict(m) for m in data.get("members", [])],
            task_list_id=data.get("task_list_id", ""),
            delegate_mode=data.get("delegate_mode", False),
            repo_root=data.get("repo_root", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            settings=data.get("settings", {}),
        )

    def get_member(self, name: str) -> TeammateConfig | None:
        """Find a member by name."""
        for m in self.members:
            if m.name == name:
                return m
        return None

    def get_member_by_id(self, agent_id: str) -> TeammateConfig | None:
        """Find a member by agent ID."""
        if self.lead and self.lead.agent_id == agent_id:
            return self.lead
        for m in self.members:
            if m.agent_id == agent_id:
                return m
        return None

    def get_active_members(self) -> list[TeammateConfig]:
        """Get members that are still running."""
        active = {TeammateStatus.IDLE, TeammateStatus.WORKING, TeammateStatus.PLAN_MODE}
        return [m for m in self.members if m.status in active]


@dataclass
class TeamMessage:
    """A message in the inter-agent mailbox.

    Stored at: ~/.emdash/teams/{name}/mailbox/{to}/{timestamp}-{id}.json
    """

    id: str
    from_agent: str                    # Sender name (or "lead", "user")
    to_agent: str                      # Recipient name (or "lead", "all")
    message_type: MessageType
    content: str                       # Message body (markdown)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    delivered: bool = False
    delivered_at: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message_type": self.message_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "delivered": self.delivered,
            "delivered_at": self.delivered_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TeamMessage":
        return cls(
            id=data["id"],
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            message_type=MessageType(data["message_type"]),
            content=data["content"],
            metadata=data.get("metadata", {}),
            timestamp=data.get("timestamp", ""),
            delivered=data.get("delivered", False),
            delivered_at=data.get("delivered_at", ""),
        )


@dataclass
class TokenUsageSnapshot:
    """Token usage for a single teammate at a point in time."""

    agent_name: str
    input_tokens: int = 0
    output_tokens: int = 0
    thinking_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0
    estimated_cost_usd: float = 0.0
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "thinking_tokens": self.thinking_tokens,
            "cache_creation_tokens": self.cache_creation_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "estimated_cost_usd": self.estimated_cost_usd,
            "timestamp": self.timestamp,
        }
