"""Multiuser chat integration for shared agent sessions.

This module enables multiple users to collaborate in a single agent
conversation with real-time synchronization.

Key Features:
- Shared conversation sessions with invite codes
- Message queue for concurrent user inputs
- Event broadcasting to all participants
- Webhook-based persistence (consumer handles durable storage)

Basic Usage:
    from emdash_core.multiuser import (
        SharedSessionManager,
        get_or_init_manager,
    )

    # Initialize manager (in-memory state, fires webhooks on mutations)
    manager = await get_or_init_manager()

    # Create shared session
    session, invite_code = await manager.create_session(
        owner_id="user_123",
        display_name="Alice",
    )
    print(f"Share this code: {invite_code}")

    # Join from another machine/process
    session = await manager.join_session(
        invite_code="ABC123",
        user_id="user_456",
        display_name="Bob",
    )

    # Send message (queues if agent busy)
    message = await manager.send_message(
        session_id=session.session_id,
        user_id="user_123",
        content="Hello agent!",
    )
"""

# Protocols and exceptions
from .protocols import (
    # Enums
    ParticipantRole,
    SharedSessionState,
    SharedEventType,
    # Data classes
    Participant,
    QueuedMessage,
    SharedSessionInfo,
    SharedEvent,
    # Protocols
    SharedEventHandler,
    # Exceptions
    MultiuserError,
    SessionNotFoundError,
    InvalidInviteCodeError,
    ConflictError,
    NotAuthorizedError,
    AgentBusyError,
    TeamNotFoundError,
    InvalidTeamInviteError,
    TeamPermissionError,
)

# Models
from .models import (
    SharedSession,
    InviteToken,
    UserIdentity,
)

# Queue
from .queue import (
    SharedMessageQueue,
    SyncedMessageQueue,
)

# Broadcaster
from .broadcaster import (
    SharedEventBroadcaster,
    SSESharedEventHandler,
    RemoteEventReceiver,
)

# Invites
from .invites import (
    generate_invite_code,
    normalize_invite_code,
    InviteManager,
    get_invite_manager,
    set_invite_manager,
)

# Teams
from .teams import (
    Team,
    TeamMember,
    TeamRole,
    SessionVisibility,
    TeamSessionInfo,
    TeamManager,
    get_team_manager,
    set_team_manager,
    init_team_manager,
)

# Registry
from .registry import (
    Rule,
    AgentConfig,
    MCPConfig,
    Skill,
    TeamRegistry,
    RegistryItemType,
    RegistryManager,
)

# Project data models (pure types, no I/O)
from .projects import (
    Project,
    ProjectMember,
    ProjectRole,
    Task,
    TaskComment,
    TaskStatus,
    TaskPriority,
)

# Project business logic (in-memory state + webhook dispatch)
from .project_manager import (
    ProjectManager,
    get_project_manager,
    set_project_manager,
)

# Webhooks (core fires events, consumer persists)
from .webhooks import (
    WebhookRegistration,
    WebhookEvent,
    WebhookRegistry,
    get_webhook_registry,
    set_webhook_registry,
)

# Manager
from .manager import (
    SharedSessionManager,
    get_shared_session_manager,
    get_or_init_manager,
    set_shared_session_manager,
    init_shared_session_manager,
)

# Config
from .config import (
    MultiuserConfig,
    FirebaseConfig,
    SyncProviderType,
    get_multiuser_config,
    set_multiuser_config,
    is_multiuser_enabled,
    print_config_help,
)

__all__ = [
    # Enums
    "ParticipantRole",
    "SharedSessionState",
    "SharedEventType",
    "TeamRole",
    "SessionVisibility",
    # Data classes
    "Participant",
    "QueuedMessage",
    "SharedSessionInfo",
    "SharedEvent",
    "TeamSessionInfo",
    # Models
    "SharedSession",
    "InviteToken",
    "UserIdentity",
    "Team",
    "TeamMember",
    # Protocols
    "SharedEventHandler",
    # Queue
    "SharedMessageQueue",
    "SyncedMessageQueue",
    # Broadcaster
    "SharedEventBroadcaster",
    "SSESharedEventHandler",
    "RemoteEventReceiver",
    # Invites
    "generate_invite_code",
    "normalize_invite_code",
    "InviteManager",
    "get_invite_manager",
    "set_invite_manager",
    # Manager
    "SharedSessionManager",
    "get_shared_session_manager",
    "get_or_init_manager",
    "set_shared_session_manager",
    "init_shared_session_manager",
    # Teams
    "TeamManager",
    "get_team_manager",
    "set_team_manager",
    "init_team_manager",
    # Registry
    "Rule",
    "AgentConfig",
    "MCPConfig",
    "Skill",
    "TeamRegistry",
    "RegistryItemType",
    "RegistryManager",
    # Config
    "MultiuserConfig",
    "FirebaseConfig",
    "SyncProviderType",
    "get_multiuser_config",
    "set_multiuser_config",
    "is_multiuser_enabled",
    "print_config_help",
    # Project data models
    "Project",
    "ProjectMember",
    "ProjectRole",
    "Task",
    "TaskComment",
    "TaskStatus",
    "TaskPriority",
    # Project business logic
    "ProjectManager",
    "get_project_manager",
    "set_project_manager",
    # Webhooks
    "WebhookRegistration",
    "WebhookEvent",
    "WebhookRegistry",
    "get_webhook_registry",
    "set_webhook_registry",
    # Exceptions
    "MultiuserError",
    "SessionNotFoundError",
    "InvalidInviteCodeError",
    "ConflictError",
    "NotAuthorizedError",
    "AgentBusyError",
    "TeamNotFoundError",
    "InvalidTeamInviteError",
    "TeamPermissionError",
]
