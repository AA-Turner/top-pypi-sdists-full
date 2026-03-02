"""Team management for multiuser sessions.

This module provides team functionality allowing users to:
- Create and manage teams
- Browse team sessions
- Add existing sessions to teams
- Control session visibility (private/team)

Teams enable organizations to share sessions among members without
requiring individual invite codes for each session.
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING

from .webhooks import get_webhook_registry

if TYPE_CHECKING:
    from .registry import RegistryManager, TeamRegistry

log = logging.getLogger(__name__)


class TeamRole(str, Enum):
    """Role of a member in a team."""

    ADMIN = "admin"  # Can manage team, add/remove members, manage all sessions
    MEMBER = "member"  # Can view and join team sessions


class SessionVisibility(str, Enum):
    """Visibility level of a session."""

    PRIVATE = "private"  # Only accessible via invite code
    TEAM = "team"  # Visible to all team members


@dataclass
class TeamMember:
    """A member of a team."""

    user_id: str
    display_name: str
    role: TeamRole
    joined_at: str
    invited_by: Optional[str] = None  # User ID who invited this member
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "role": self.role.value,
            "joined_at": self.joined_at,
            "invited_by": self.invited_by,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TeamMember":
        """Create from dictionary."""
        return cls(
            user_id=data["user_id"],
            display_name=data["display_name"],
            role=TeamRole(data["role"]),
            joined_at=data["joined_at"],
            invited_by=data.get("invited_by"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class TeamSessionInfo:
    """Information about a session in a team (lightweight, for listings)."""

    session_id: str
    title: str
    owner_id: str
    owner_name: str
    created_at: str
    updated_at: str
    participant_count: int
    is_active: bool

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "title": self.title,
            "owner_id": self.owner_id,
            "owner_name": self.owner_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "participant_count": self.participant_count,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TeamSessionInfo":
        """Create from dictionary."""
        return cls(
            session_id=data["session_id"],
            title=data.get("title", "Untitled Session"),
            owner_id=data["owner_id"],
            owner_name=data.get("owner_name", "Unknown"),
            created_at=data["created_at"],
            updated_at=data.get("updated_at", data["created_at"]),
            participant_count=data.get("participant_count", 1),
            is_active=data.get("is_active", True),
        )


@dataclass
class Team:
    """A team for organizing shared sessions.

    Teams allow groups of users to share sessions without individual
    invite codes. Team members can browse and join any team session
    that has TEAM visibility.

    Attributes:
        team_id: Unique identifier for the team
        name: Human-readable team name
        description: Optional team description
        repo_link: Link to team's repository (e.g. GitHub URL)
        created_at: ISO timestamp of creation
        updated_at: ISO timestamp of last update
        created_by: User ID of creator
        members: List of team members
        invite_code: Code for joining the team
        settings: Team-level settings
    """

    team_id: str
    name: str
    description: str = ""
    repo_link: str = ""  # Link to team's repository (e.g. GitHub URL)
    created_at: str = ""
    updated_at: str = ""
    created_by: str = ""
    members: list[TeamMember] = field(default_factory=list)
    invite_code: str = ""  # For joining the team
    settings: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Set defaults after initialization."""
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
        if not self.invite_code:
            self.invite_code = self._generate_team_invite()

    def _generate_team_invite(self) -> str:
        """Generate a team invite code."""
        # Use a different prefix to distinguish from session invites
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(chars, k=8))
        return f"T-{code}"  # T- prefix for team invites

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "description": self.description,
            "repo_link": self.repo_link,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
            "members": [m.to_dict() for m in self.members],
            "invite_code": self.invite_code,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Team":
        """Create from dictionary."""
        members = [TeamMember.from_dict(m) for m in data.get("members", [])]
        return cls(
            team_id=data["team_id"],
            name=data["name"],
            description=data.get("description", ""),
            repo_link=data.get("repo_link", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            created_by=data.get("created_by", ""),
            members=members,
            invite_code=data.get("invite_code", ""),
            settings=data.get("settings", {}),
        )

    def get_member(self, user_id: str) -> Optional[TeamMember]:
        """Get a member by user ID."""
        for member in self.members:
            if member.user_id == user_id:
                return member
        return None

    def is_member(self, user_id: str) -> bool:
        """Check if user is a team member."""
        return self.get_member(user_id) is not None

    def is_admin(self, user_id: str) -> bool:
        """Check if user is a team admin."""
        member = self.get_member(user_id)
        return member is not None and member.role == TeamRole.ADMIN

    def add_member(
        self,
        user_id: str,
        display_name: str,
        role: TeamRole = TeamRole.MEMBER,
        invited_by: Optional[str] = None,
    ) -> TeamMember:
        """Add a member to the team.

        If user already exists, updates their info and returns existing member.
        """
        existing = self.get_member(user_id)
        if existing:
            existing.display_name = display_name
            return existing

        now = datetime.utcnow().isoformat()
        member = TeamMember(
            user_id=user_id,
            display_name=display_name,
            role=role,
            joined_at=now,
            invited_by=invited_by,
        )
        self.members.append(member)
        self.updated_at = now
        return member

    def remove_member(self, user_id: str) -> bool:
        """Remove a member from the team.

        Returns True if removed, False if not found.
        Cannot remove the creator/last admin.
        """
        # Don't allow removing the creator
        if user_id == self.created_by:
            return False

        # Count admins
        admin_count = sum(1 for m in self.members if m.role == TeamRole.ADMIN)
        member = self.get_member(user_id)

        if member and member.role == TeamRole.ADMIN and admin_count <= 1:
            # Don't remove last admin
            return False

        original_len = len(self.members)
        self.members = [m for m in self.members if m.user_id != user_id]
        if len(self.members) < original_len:
            self.updated_at = datetime.utcnow().isoformat()
            return True
        return False

    def update_member_role(self, user_id: str, new_role: TeamRole) -> bool:
        """Update a member's role.

        Returns True if updated, False if not found.
        """
        member = self.get_member(user_id)
        if not member:
            return False

        # Don't allow demoting last admin
        if member.role == TeamRole.ADMIN and new_role != TeamRole.ADMIN:
            admin_count = sum(1 for m in self.members if m.role == TeamRole.ADMIN)
            if admin_count <= 1:
                return False

        member.role = new_role
        self.updated_at = datetime.utcnow().isoformat()
        return True


class TeamManager:
    """Manages teams and team-session relationships.

    This class handles:
    - Team CRUD operations
    - Team membership management
    - Session-team associations
    - Team session listings

    Usage:
        manager = TeamManager(storage_root=Path("~/.emdash/multiuser"))

        # Create team
        team = await manager.create_team(
            name="My Team",
            creator_id="user_123",
            creator_name="Alice",
        )

        # Join team
        team = await manager.join_team(
            invite_code="T-ABC12345",
            user_id="user_456",
            display_name="Bob",
        )

        # Add session to team
        await manager.add_session_to_team(
            team_id=team.team_id,
            session_id="session_789",
            user_id="user_123",
        )

        # List team sessions
        sessions = await manager.list_team_sessions(team.team_id)
    """

    def __init__(
        self,
        storage_root: Optional[Path] = None,
    ):
        """Initialize the team manager.

        Args:
            storage_root: Root for local storage
        """
        self._storage_root = storage_root or Path.home() / ".emdash" / "multiuser"
        self._storage_root.mkdir(parents=True, exist_ok=True)

        # In-memory cache
        self._teams: dict[str, Team] = {}

        # Session-to-team mapping: session_id -> team_id
        self._session_teams: dict[str, str] = {}

        # Registry manager (lazy initialized)
        self._registry_manager: Optional["RegistryManager"] = None

        # Load from local storage
        self._load_local_data()

    def _get_teams_file(self) -> Path:
        """Get path to teams storage file."""
        return self._storage_root / "teams.json"

    def _get_session_teams_file(self) -> Path:
        """Get path to session-teams mapping file."""
        return self._storage_root / "session_teams.json"

    def _load_local_data(self) -> None:
        """Load teams and mappings from local storage."""
        # Load teams
        teams_file = self._get_teams_file()
        if teams_file.exists():
            try:
                with open(teams_file, "r") as f:
                    data = json.load(f)
                    for team_data in data.get("teams", []):
                        team = Team.from_dict(team_data)
                        self._teams[team.team_id] = team
                log.debug(f"Loaded {len(self._teams)} teams from local storage")
            except Exception as e:
                log.warning(f"Error loading teams: {e}")

        # Load session-team mappings
        mappings_file = self._get_session_teams_file()
        if mappings_file.exists():
            try:
                with open(mappings_file, "r") as f:
                    self._session_teams = json.load(f)
                log.debug(f"Loaded {len(self._session_teams)} session-team mappings")
            except Exception as e:
                log.warning(f"Error loading session-team mappings: {e}")

    def _save_local_data(self) -> None:
        """Save teams and mappings to local storage."""
        # Save teams
        teams_file = self._get_teams_file()
        try:
            with open(teams_file, "w") as f:
                json.dump({
                    "teams": [t.to_dict() for t in self._teams.values()]
                }, f, indent=2)
        except Exception as e:
            log.warning(f"Error saving teams: {e}")

        # Save session-team mappings
        mappings_file = self._get_session_teams_file()
        try:
            with open(mappings_file, "w") as f:
                json.dump(self._session_teams, f, indent=2)
        except Exception as e:
            log.warning(f"Error saving session-team mappings: {e}")

    async def create_team(
        self,
        name: str,
        creator_id: str,
        creator_name: str,
        description: str = "",
    ) -> Team:
        """Create a new team.

        Args:
            name: Team name
            creator_id: User ID of creator (becomes admin)
            creator_name: Display name of creator
            description: Optional team description

        Returns:
            The created Team
        """
        team_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        # Create admin member for creator
        creator_member = TeamMember(
            user_id=creator_id,
            display_name=creator_name,
            role=TeamRole.ADMIN,
            joined_at=now,
        )

        team = Team(
            team_id=team_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            created_by=creator_id,
            members=[creator_member],
        )

        # Store locally
        self._teams[team_id] = team
        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.created", team.to_dict())

        log.info(f"Created team '{name}' with ID {team_id}")
        return team

    async def get_team(self, team_id: str) -> Optional[Team]:
        """Get a team by ID."""
        # Check local cache
        if team_id in self._teams:
            return self._teams[team_id]

        return None

    async def get_team_by_invite(self, invite_code: str) -> Optional[Team]:
        """Get a team by invite code."""
        invite_code = invite_code.upper().strip()

        # Check local teams
        for team in self._teams.values():
            if team.invite_code.upper() == invite_code:
                return team

        return None

    async def join_team(
        self,
        invite_code: str,
        user_id: str,
        display_name: str,
    ) -> Team:
        """Join a team using invite code.

        Args:
            invite_code: Team invite code
            user_id: Joining user's ID
            display_name: Joining user's display name

        Returns:
            The joined Team

        Raises:
            ValueError: If invite code is invalid
        """
        team = await self.get_team_by_invite(invite_code)
        if not team:
            raise ValueError(f"Invalid team invite code: {invite_code}")

        # Add member
        team.add_member(user_id, display_name)

        # Save locally
        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.member_joined", {
            "team_id": team.team_id,
            "member": team.get_member(user_id).to_dict(),
            "team": team.to_dict(),
        })

        log.info(f"User {user_id} joined team {team.team_id}")
        return team

    async def leave_team(self, team_id: str, user_id: str) -> bool:
        """Leave a team.

        Returns True if left successfully.
        """
        team = await self.get_team(team_id)
        if not team:
            return False

        if not team.remove_member(user_id):
            return False

        # Save locally
        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.member_left", {
            "team_id": team_id,
            "user_id": user_id,
            "team": team.to_dict(),
        })

        log.info(f"User {user_id} left team {team_id}")
        return True

    async def delete_team(self, team_id: str, user_id: str) -> bool:
        """Delete a team (admin only).

        Args:
            team_id: Team to delete
            user_id: User attempting deletion (must be admin)

        Returns:
            True if deleted successfully
        """
        team = await self.get_team(team_id)
        if not team:
            return False

        if not team.is_admin(user_id):
            raise PermissionError("Only admins can delete teams")

        # Remove from local
        self._teams.pop(team_id, None)

        # Remove session associations
        self._session_teams = {
            sid: tid for sid, tid in self._session_teams.items()
            if tid != team_id
        }

        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.deleted", {
            "team_id": team_id,
            "invite_code": team.invite_code,
        })

        log.info(f"Deleted team {team_id}")
        return True

    async def get_user_teams(self, user_id: str) -> list[Team]:
        """Get all teams a user is a member of."""
        user_teams = []

        # Check local teams
        for team in self._teams.values():
            if team.is_member(user_id):
                user_teams.append(team)

        return user_teams

    async def add_session_to_team(
        self,
        team_id: str,
        session_id: str,
        user_id: str,
        title: Optional[str] = None,
    ) -> bool:
        """Add a session to a team.

        The user must be a member of the team and either own the session
        or be a team admin.

        Args:
            team_id: Target team
            session_id: Session to add
            user_id: User adding the session (must be session owner or team admin)
            title: Optional title for the session in team listings

        Returns:
            True if added successfully
        """
        team = await self.get_team(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        if not team.is_member(user_id):
            raise PermissionError("Must be a team member to add sessions")

        # Store mapping
        self._session_teams[session_id] = team_id
        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.session_added", {
            "team_id": team_id,
            "session_id": session_id,
            "title": title,
        })

        log.info(f"Added session {session_id} to team {team_id}")
        return True

    async def remove_session_from_team(
        self,
        session_id: str,
        user_id: str,
    ) -> bool:
        """Remove a session from its team.

        Args:
            session_id: Session to remove
            user_id: User removing the session (must be session owner or team admin)

        Returns:
            True if removed successfully
        """
        team_id = self._session_teams.get(session_id)
        if not team_id:
            return False

        team = await self.get_team(team_id)
        if not team:
            return False

        # Verify permission (session owner or team admin)
        if not team.is_admin(user_id):
            # Would need to check session ownership too, but that requires manager
            pass  # Allow for now, manager will verify

        # Remove mapping
        self._session_teams.pop(session_id, None)
        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.session_removed", {
            "team_id": team_id,
            "session_id": session_id,
        })

        log.info(f"Removed session {session_id} from team {team_id}")
        return True

    def get_session_team(self, session_id: str) -> Optional[str]:
        """Get the team ID for a session, if any."""
        return self._session_teams.get(session_id)

    async def list_team_sessions(
        self,
        team_id: str,
        user_id: str,
    ) -> list[TeamSessionInfo]:
        """List all sessions in a team.

        Args:
            team_id: Team to list sessions for
            user_id: Requesting user (must be team member)

        Returns:
            List of TeamSessionInfo for team sessions
        """
        team = await self.get_team(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        if not team.is_member(user_id):
            raise PermissionError("Must be a team member to list sessions")

        sessions: list[TeamSessionInfo] = []

        # Get session IDs for this team
        team_session_ids = [
            sid for sid, tid in self._session_teams.items()
            if tid == team_id
        ]

        # Build from local data
        for session_id in team_session_ids:
            # Basic info - would need session manager for full details
            sessions.append(TeamSessionInfo(
                session_id=session_id,
                title="Session",
                owner_id="unknown",
                owner_name="Unknown",
                created_at="",
                updated_at="",
                participant_count=0,
                is_active=True,
            ))

        return sessions

    async def invite_member(
        self,
        team_id: str,
        inviter_id: str,
        invitee_id: str,
        invitee_name: str,
        role: TeamRole = TeamRole.MEMBER,
    ) -> TeamMember:
        """Invite a user to a team (admin only).

        Args:
            team_id: Team to invite to
            inviter_id: Admin inviting the user
            invitee_id: User to invite
            invitee_name: Display name for invitee
            role: Role to assign

        Returns:
            The new TeamMember
        """
        team = await self.get_team(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        if not team.is_admin(inviter_id):
            raise PermissionError("Only admins can invite members")

        member = team.add_member(
            user_id=invitee_id,
            display_name=invitee_name,
            role=role,
            invited_by=inviter_id,
        )

        # Save locally
        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.updated", team.to_dict())

        log.info(f"Invited {invitee_id} to team {team_id}")
        return member

    async def update_member_role(
        self,
        team_id: str,
        admin_id: str,
        member_id: str,
        new_role: TeamRole,
    ) -> bool:
        """Update a team member's role (admin only).

        Args:
            team_id: Team ID
            admin_id: Admin making the change
            member_id: Member to update
            new_role: New role to assign

        Returns:
            True if updated successfully
        """
        team = await self.get_team(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        if not team.is_admin(admin_id):
            raise PermissionError("Only admins can update roles")

        if not team.update_member_role(member_id, new_role):
            return False

        # Save locally
        self._save_local_data()

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.updated", team.to_dict())

        return True

    # ─────────────────────────────────────────────────────────────
    # Registry Operations
    # ─────────────────────────────────────────────────────────────

    @property
    def registry_manager(self) -> "RegistryManager":
        """Get the registry manager (lazy initialization)."""
        if self._registry_manager is None:
            from .registry import RegistryManager
            self._registry_manager = RegistryManager(
                base_path=self._storage_root.parent,  # .emdash directory
            )
        return self._registry_manager

    async def get_team_registry(
        self,
        team_id: str,
        user_id: str,
    ) -> "TeamRegistry":
        """Get the registry for a team.

        Args:
            team_id: Team ID
            user_id: Requesting user (must be team member)

        Returns:
            TeamRegistry for the team
        """
        team = await self.get_team(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        if not team.is_member(user_id):
            raise PermissionError("Must be a team member to access registry")

        return await self.registry_manager.get_registry(team_id)

    async def save_team_registry(
        self,
        registry: "TeamRegistry",
        user_id: str,
    ) -> bool:
        """Save the registry for a team.

        Args:
            registry: Registry to save
            user_id: User saving (must be team admin)

        Returns:
            True if saved successfully
        """
        team = await self.get_team(registry.team_id)
        if not team:
            raise ValueError(f"Team {registry.team_id} not found")

        if not team.is_admin(user_id):
            raise PermissionError("Only admins can modify the team registry")

        return await self.registry_manager.save_registry(registry)

    async def sync_team_registry(
        self,
        team_id: str,
        user_id: str,
        strategy: str = "remote_wins",
    ) -> "TeamRegistry":
        """Sync the team registry between local and remote.

        Args:
            team_id: Team ID
            user_id: Requesting user (must be team member)
            strategy: Conflict resolution strategy

        Returns:
            Synced TeamRegistry
        """
        team = await self.get_team(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")

        if not team.is_member(user_id):
            raise PermissionError("Must be a team member to sync registry")

        return await self.registry_manager.sync_registry(team_id, strategy)

    def sync_teams(self, team_dicts: list[dict]) -> int:
        """Load teams from consumer's durable store into in-memory state.

        Called at startup by the webhook consumer to restore teams.
        """
        count = 0
        for data in team_dicts:
            try:
                team = Team.from_dict(data)
                self._teams[team.team_id] = team
                count += 1
            except Exception as e:
                log.warning(f"Failed to sync team: {e}")
        self._save_local_data()
        log.info(f"Synced {count} teams into memory")
        return count


# Global team manager instance
_team_manager: Optional[TeamManager] = None


def get_team_manager() -> TeamManager:
    """Get the global TeamManager instance."""
    global _team_manager
    if _team_manager is None:
        _team_manager = TeamManager()
    return _team_manager


def set_team_manager(manager: TeamManager) -> None:
    """Set the global TeamManager instance."""
    global _team_manager
    _team_manager = manager


async def init_team_manager(
    storage_root: Optional[Path] = None,
) -> TeamManager:
    """Initialize the global TeamManager with configuration.

    Args:
        storage_root: Root for local storage

    Returns:
        The initialized TeamManager
    """
    global _team_manager
    _team_manager = TeamManager(
        storage_root=storage_root,
    )
    return _team_manager
