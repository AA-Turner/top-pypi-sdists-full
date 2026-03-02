"""Local file-based sync provider for multiuser sessions.

This provider stores session state in local files, enabling:
- Single-machine multi-process sync (via file watching)
- Development and testing without external dependencies
- Fallback when cloud providers are unavailable

Note: This provider does NOT support true multi-machine sync.
Use FirebaseSyncProvider or WebSocketSyncProvider for that.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Awaitable, Optional

from filelock import FileLock

from ..protocols import (
    SyncProvider,
    SharedSessionInfo,
    SharedEvent,
    Participant,
    ParticipantRole,
    QueuedMessage,
    SharedSessionState,
    SessionNotFoundError,
    InvalidInviteCodeError,
    ConflictError,
)
from ..models import SharedSession
from ..invites import generate_invite_code

log = logging.getLogger(__name__)


class LocalFileSyncProvider(SyncProvider):
    """File-based sync provider for local development and testing.

    Stores session state in JSON files with file locking for
    concurrent access. Supports file watching for change detection.

    Directory structure:
        {storage_root}/
            sessions/
                {session_id}.json     # Session state
                {session_id}.events/  # Event log (optional)
            invites.json              # Invite code mappings

    Usage:
        provider = LocalFileSyncProvider(Path("~/.emdash/multiuser"))
        await provider.connect()

        # Create session
        info = await provider.create_session(
            session_id, owner_id, initial_state
        )

        # Subscribe to events
        subscription_id = await provider.subscribe(
            session_id, handle_event
        )
    """

    def __init__(
        self,
        storage_root: Path,
        poll_interval: float = 1.0,
    ):
        """Initialize the local file provider.

        Args:
            storage_root: Root directory for storing session files
            poll_interval: Seconds between file change polls
        """
        self._storage_root = Path(storage_root).expanduser()
        self._poll_interval = poll_interval

        self._sessions_dir = self._storage_root / "sessions"
        self._invites_file = self._storage_root / "invites.json"

        self._connected = False
        self._subscriptions: dict[str, tuple[str, Callable]] = {}  # sub_id -> (session_id, handler)
        self._poll_tasks: dict[str, asyncio.Task] = {}  # session_id -> poll task
        self._last_versions: dict[str, int] = {}  # session_id -> last seen version

    async def connect(self) -> bool:
        """Establish connection (create directories).

        Returns:
            True if connected successfully
        """
        try:
            self._sessions_dir.mkdir(parents=True, exist_ok=True)
            self._connected = True
            log.info(f"LocalFileSyncProvider connected at {self._storage_root}")
            return True
        except Exception as e:
            log.error(f"Failed to connect: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect and stop all polling."""
        self._connected = False

        # Cancel all poll tasks
        for task in self._poll_tasks.values():
            task.cancel()
        self._poll_tasks.clear()
        self._subscriptions.clear()

        log.info("LocalFileSyncProvider disconnected")

    async def create_session(
        self,
        session_id: str,
        owner_id: str,
        initial_state: dict[str, Any],
    ) -> SharedSessionInfo:
        """Create a new shared session.

        Args:
            session_id: Unique session identifier
            owner_id: ID of the creating user
            initial_state: Initial session state

        Returns:
            Created session info with invite code
        """
        invite_code = generate_invite_code()
        now = datetime.utcnow().isoformat()

        # Get owner info from initial state or create default
        owner_name = initial_state.get("owner_name", "Owner")
        owner = Participant(
            user_id=owner_id,
            display_name=owner_name,
            role=ParticipantRole.OWNER,
            joined_at=now,
            last_seen=now,
            is_online=True,
        )

        session = SharedSession(
            session_id=session_id,
            invite_code=invite_code,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
            state=SharedSessionState.ACTIVE,
            version=1,
            participants=[owner],
            message_queue=[],
            messages=initial_state.get("messages", []),
            model=initial_state.get("model", ""),
            plan_mode=initial_state.get("plan_mode", False),
            repo_root=initial_state.get("repo_root", ""),
        )

        # Save session
        await self._save_session(session)

        # Save invite mapping
        await self._save_invite(invite_code, session_id)

        log.info(f"Created session {session_id} with invite {invite_code}")
        return session.get_info()

    async def join_session(
        self,
        invite_code: str,
        user_id: str,
        display_name: str,
    ) -> SharedSessionInfo:
        """Join an existing session via invite code.

        Args:
            invite_code: The session invite code
            user_id: Joining user's ID
            display_name: Display name for the user

        Returns:
            Session info

        Raises:
            InvalidInviteCodeError: If invite code is invalid
        """
        # Look up session by invite code
        session_id = await self.find_session_by_invite(invite_code)
        if not session_id:
            raise InvalidInviteCodeError(f"Invalid invite code: {invite_code}")

        # Load session
        session = await self._load_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        # Add participant
        now = datetime.utcnow().isoformat()
        participant = Participant(
            user_id=user_id,
            display_name=display_name,
            role=ParticipantRole.EDITOR,
            joined_at=now,
            last_seen=now,
            is_online=True,
        )
        session.add_participant(participant)

        # Save updated session
        await self._save_session(session)

        log.info(f"User {user_id} joined session {session_id}")
        return session.get_info()

    async def leave_session(
        self,
        session_id: str,
        user_id: str,
    ) -> None:
        """Leave a shared session."""
        session = await self._load_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        session.remove_participant(user_id)
        await self._save_session(session)

        log.info(f"User {user_id} left session {session_id}")

    async def push_event(
        self,
        session_id: str,
        event: SharedEvent,
    ) -> None:
        """Push an event to all session participants.

        For local provider, events are stored in session state
        and detected via version polling.

        Args:
            session_id: Target session
            event: Event to broadcast
        """
        # For local provider, we just bump the version
        # Subscribers will detect the change via polling
        session = await self._load_session(session_id)
        if session:
            session.version += 1
            session.updated_at = datetime.utcnow().isoformat()
            await self._save_session(session)

    async def subscribe(
        self,
        session_id: str,
        handler: Callable[[SharedEvent], Awaitable[None]],
    ) -> str:
        """Subscribe to session events.

        Args:
            session_id: Session to subscribe to
            handler: Async callback for events

        Returns:
            Subscription ID for unsubscribing
        """
        subscription_id = str(uuid.uuid4())
        self._subscriptions[subscription_id] = (session_id, handler)

        # Start polling for this session if not already
        if session_id not in self._poll_tasks:
            task = asyncio.create_task(self._poll_session(session_id))
            self._poll_tasks[session_id] = task

        log.debug(f"Subscribed {subscription_id} to session {session_id}")
        return subscription_id

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from session events."""
        if subscription_id in self._subscriptions:
            session_id, _ = self._subscriptions.pop(subscription_id)

            # Check if any subscriptions remain for this session
            remaining = [
                sid for sid, (sess_id, _) in self._subscriptions.items()
                if sess_id == session_id
            ]

            if not remaining and session_id in self._poll_tasks:
                self._poll_tasks[session_id].cancel()
                del self._poll_tasks[session_id]

            log.debug(f"Unsubscribed {subscription_id}")

    async def get_session_state(
        self,
        session_id: str,
    ) -> SharedSessionInfo:
        """Get current session state (metadata only)."""
        session = await self._load_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")
        return session.get_info()

    async def get_full_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """Get full session data including message history."""
        session = await self._load_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")
        return session.to_dict()

    async def update_session_state(
        self,
        session_id: str,
        updates: dict[str, Any],
        expected_version: Optional[int] = None,
    ) -> SharedSessionInfo:
        """Update session state with optimistic locking.

        Args:
            session_id: Session to update
            updates: State updates to apply
            expected_version: For conflict detection

        Returns:
            Updated session info

        Raises:
            ConflictError: If version mismatch
        """
        session_file = self._sessions_dir / f"{session_id}.json"
        lock_file = session_file.with_suffix(".lock")

        with FileLock(lock_file, timeout=10):
            session = await self._load_session(session_id)
            if not session:
                raise SessionNotFoundError(f"Session {session_id} not found")

            # Check version for conflict
            if expected_version is not None and session.version != expected_version:
                raise ConflictError(
                    f"Version conflict: expected {expected_version}, got {session.version}",
                    current_version=session.version,
                    expected_version=expected_version,
                )

            # Apply updates
            for key, value in updates.items():
                if key == "participants":
                    session.participants = [
                        Participant.from_dict(p) if isinstance(p, dict) else p
                        for p in value
                    ]
                elif key == "message_queue":
                    session.message_queue = [
                        QueuedMessage.from_dict(m) if isinstance(m, dict) else m
                        for m in value
                    ]
                elif key == "state":
                    session.state = SharedSessionState(value) if isinstance(value, str) else value
                elif hasattr(session, key):
                    setattr(session, key, value)

            session.version += 1
            session.updated_at = datetime.utcnow().isoformat()

            await self._save_session(session)

        return session.get_info()

    async def heartbeat(
        self,
        session_id: str,
        user_id: str,
    ) -> None:
        """Send heartbeat to indicate user is still connected."""
        session = await self._load_session(session_id)
        if session:
            session.update_participant_presence(user_id, is_online=True)
            await self._save_session(session)

    async def find_session_by_invite(
        self,
        invite_code: str,
    ) -> Optional[str]:
        """Find session ID by invite code."""
        invite_code = invite_code.upper().strip()

        invites = await self._load_invites()
        return invites.get(invite_code)

    # ─────────────────────────────────────────────────────────────
    # Private methods
    # ─────────────────────────────────────────────────────────────

    async def _load_session(self, session_id: str) -> Optional[SharedSession]:
        """Load a session from file."""
        session_file = self._sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return None

        try:
            data = json.loads(session_file.read_text())
            return SharedSession.from_dict(data)
        except Exception as e:
            log.error(f"Failed to load session {session_id}: {e}")
            return None

    async def _save_session(self, session: SharedSession) -> None:
        """Save a session to file."""
        session_file = self._sessions_dir / f"{session.session_id}.json"
        lock_file = session_file.with_suffix(".lock")

        with FileLock(lock_file, timeout=10):
            session_file.write_text(json.dumps(session.to_dict(), indent=2))

    async def _load_invites(self) -> dict[str, str]:
        """Load invite code mappings."""
        if not self._invites_file.exists():
            return {}

        try:
            return json.loads(self._invites_file.read_text())
        except Exception as e:
            log.error(f"Failed to load invites: {e}")
            return {}

    async def _save_invite(self, invite_code: str, session_id: str) -> None:
        """Save an invite code mapping."""
        invites = await self._load_invites()
        invites[invite_code] = session_id

        self._invites_file.write_text(json.dumps(invites, indent=2))

    async def _poll_session(self, session_id: str) -> None:
        """Poll a session for changes and notify subscribers."""
        log.debug(f"Starting poll for session {session_id}")

        while True:
            try:
                await asyncio.sleep(self._poll_interval)

                session = await self._load_session(session_id)
                if not session:
                    continue

                # Check if version changed
                last_version = self._last_versions.get(session_id, 0)
                if session.version > last_version:
                    self._last_versions[session_id] = session.version

                    # Create state sync event
                    event = SharedEvent(
                        id=f"{session_id}_sync_{session.version}",
                        session_id=session_id,
                        event_type="state_synced",
                        data={
                            "version": session.version,
                            "state": session.state.value,
                            "participant_count": len(session.participants),
                            "queue_length": len(session.message_queue),
                        },
                        timestamp=datetime.utcnow().isoformat(),
                        sequence=session.version,
                    )

                    # Notify subscribers
                    for sub_id, (sess_id, handler) in self._subscriptions.items():
                        if sess_id == session_id:
                            try:
                                await handler(event)
                            except Exception as e:
                                log.warning(f"Handler error for {sub_id}: {e}")

            except asyncio.CancelledError:
                log.debug(f"Poll cancelled for session {session_id}")
                break
            except Exception as e:
                log.error(f"Poll error for session {session_id}: {e}")
                await asyncio.sleep(self._poll_interval * 2)  # Back off on error

    # ─────────────────────────────────────────────────────────────
    # Team Operations
    # ─────────────────────────────────────────────────────────────

    def _get_teams_file(self) -> Path:
        """Get path to teams storage file."""
        return self._storage_root / "teams.json"

    def _get_team_invites_file(self) -> Path:
        """Get path to team invites file."""
        return self._storage_root / "team_invites.json"

    def _get_team_sessions_file(self) -> Path:
        """Get path to team-sessions mapping file."""
        return self._storage_root / "team_sessions.json"

    async def _load_teams(self) -> dict[str, dict[str, Any]]:
        """Load all teams from file."""
        teams_file = self._get_teams_file()
        if not teams_file.exists():
            return {}
        try:
            return json.loads(teams_file.read_text())
        except Exception as e:
            log.error(f"Failed to load teams: {e}")
            return {}

    async def _save_teams(self, teams: dict[str, dict[str, Any]]) -> None:
        """Save teams to file."""
        teams_file = self._get_teams_file()
        teams_file.write_text(json.dumps(teams, indent=2))

    async def _load_team_invites(self) -> dict[str, str]:
        """Load team invite mappings."""
        invites_file = self._get_team_invites_file()
        if not invites_file.exists():
            return {}
        try:
            return json.loads(invites_file.read_text())
        except Exception as e:
            log.error(f"Failed to load team invites: {e}")
            return {}

    async def _save_team_invite(self, invite_code: str, team_id: str) -> None:
        """Save a team invite mapping."""
        invites = await self._load_team_invites()
        invites[invite_code] = team_id
        invites_file = self._get_team_invites_file()
        invites_file.write_text(json.dumps(invites, indent=2))

    async def _load_team_sessions(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Load team-sessions mappings (team_id -> session_id -> session_info)."""
        file_path = self._get_team_sessions_file()
        if not file_path.exists():
            return {}
        try:
            return json.loads(file_path.read_text())
        except Exception as e:
            log.error(f"Failed to load team sessions: {e}")
            return {}

    async def _save_team_sessions(
        self, team_sessions: dict[str, dict[str, dict[str, Any]]]
    ) -> None:
        """Save team-sessions mappings."""
        file_path = self._get_team_sessions_file()
        file_path.write_text(json.dumps(team_sessions, indent=2))

    async def create_team(self, team_id: str, team_data: dict[str, Any]) -> None:
        """Create a new team."""
        teams = await self._load_teams()
        teams[team_id] = team_data
        await self._save_teams(teams)

        # Save invite mapping
        invite_code = team_data.get("invite_code", "")
        if invite_code:
            await self._save_team_invite(invite_code, team_id)

        log.info(f"Created team {team_id}")

    async def get_team(self, team_id: str) -> Optional[dict[str, Any]]:
        """Get team data."""
        teams = await self._load_teams()
        return teams.get(team_id)

    async def update_team(self, team_id: str, team_data: dict[str, Any]) -> None:
        """Update team data."""
        teams = await self._load_teams()
        teams[team_id] = team_data
        await self._save_teams(teams)
        log.debug(f"Updated team {team_id}")

    async def delete_team(self, team_id: str) -> None:
        """Delete a team."""
        teams = await self._load_teams()
        team_data = teams.pop(team_id, None)
        await self._save_teams(teams)

        # Delete invite mapping
        if team_data:
            invite_code = team_data.get("invite_code")
            if invite_code:
                invites = await self._load_team_invites()
                invites.pop(invite_code, None)
                invites_file = self._get_team_invites_file()
                invites_file.write_text(json.dumps(invites, indent=2))

        # Delete team sessions mapping
        team_sessions = await self._load_team_sessions()
        team_sessions.pop(team_id, None)
        await self._save_team_sessions(team_sessions)

        log.info(f"Deleted team {team_id}")

    async def find_team_by_invite(self, invite_code: str) -> Optional[str]:
        """Find team ID by invite code."""
        invite_code = invite_code.upper().strip()
        invites = await self._load_team_invites()
        return invites.get(invite_code)

    async def get_user_teams(self, user_id: str) -> list[dict[str, Any]]:
        """Get all teams a user is a member of."""
        teams = await self._load_teams()
        user_teams = []

        for team_id, team_data in teams.items():
            members = team_data.get("members", [])
            for member in members:
                if isinstance(member, dict) and member.get("user_id") == user_id:
                    user_teams.append(team_data)
                    break

        return user_teams

    async def add_session_to_team(
        self,
        team_id: str,
        session_id: str,
        title: Optional[str] = None,
    ) -> None:
        """Add a session to a team."""
        # Get session info
        session = await self._load_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        # Update session with team info
        session.team_id = team_id
        from ..teams import SessionVisibility
        session.visibility = SessionVisibility.TEAM
        if title:
            session.title = title
        await self._save_session(session)

        # Add to team sessions
        now = datetime.utcnow().isoformat()
        team_sessions = await self._load_team_sessions()
        if team_id not in team_sessions:
            team_sessions[team_id] = {}

        team_sessions[team_id][session_id] = {
            "session_id": session_id,
            "title": title or session.title or "Untitled Session",
            "owner_id": session.owner_id,
            "owner_name": next(
                (p.display_name for p in session.participants if p.user_id == session.owner_id),
                "Unknown"
            ),
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "added_at": now,
            "participant_count": len(session.participants),
            "is_active": session.state.value in ("active", "agent_busy"),
        }

        await self._save_team_sessions(team_sessions)
        log.info(f"Added session {session_id} to team {team_id}")

    async def remove_session_from_team(
        self,
        team_id: str,
        session_id: str,
    ) -> None:
        """Remove a session from a team."""
        # Update session
        session = await self._load_session(session_id)
        if session:
            session.team_id = None
            from ..teams import SessionVisibility
            session.visibility = SessionVisibility.PRIVATE
            await self._save_session(session)

        # Remove from team sessions
        team_sessions = await self._load_team_sessions()
        if team_id in team_sessions:
            team_sessions[team_id].pop(session_id, None)
            await self._save_team_sessions(team_sessions)

        log.info(f"Removed session {session_id} from team {team_id}")

    async def list_team_sessions(self, team_id: str) -> list[dict[str, Any]]:
        """List all sessions in a team."""
        team_sessions = await self._load_team_sessions()
        sessions = list(team_sessions.get(team_id, {}).values())

        # Sort by updated_at descending
        sessions.sort(
            key=lambda s: s.get("updated_at", ""),
            reverse=True,
        )

        return sessions

    # ─────────────────────────────────────────────────────────────
    # Registry Operations
    # ─────────────────────────────────────────────────────────────

    def _get_teams_dir(self) -> Path:
        """Get path to teams directory."""
        return self._storage_root / "teams"

    def _get_team_registry_path(self, team_id: str) -> Path:
        """Get path to a team's registry file."""
        return self._get_teams_dir() / team_id / "registry.json"

    def _ensure_team_registry_dir(self, team_id: str) -> Path:
        """Ensure the team registry directory exists."""
        team_dir = self._get_teams_dir() / team_id
        team_dir.mkdir(parents=True, exist_ok=True)
        return team_dir

    async def get_registry(self, team_id: str) -> Optional[dict[str, Any]]:
        """Get registry data for a team.

        Args:
            team_id: Team ID

        Returns:
            Registry data dict or None if not found
        """
        registry_path = self._get_team_registry_path(team_id)
        if not registry_path.exists():
            return None

        try:
            return json.loads(registry_path.read_text())
        except Exception as e:
            log.error(f"Failed to load registry for team {team_id}: {e}")
            return None

    async def save_registry(self, team_id: str, registry: dict[str, Any]) -> bool:
        """Save registry data for a team.

        Args:
            team_id: Team ID
            registry: Registry data dict

        Returns:
            True if save succeeded
        """
        self._ensure_team_registry_dir(team_id)
        registry_path = self._get_team_registry_path(team_id)
        lock_file = registry_path.with_suffix(".lock")

        try:
            with FileLock(lock_file, timeout=10):
                registry_path.write_text(json.dumps(registry, indent=2))
            return True
        except Exception as e:
            log.error(f"Failed to save registry for team {team_id}: {e}")
            return False

    async def delete_registry(self, team_id: str) -> bool:
        """Delete registry for a team.

        Args:
            team_id: Team ID

        Returns:
            True if deletion succeeded
        """
        registry_path = self._get_team_registry_path(team_id)
        if registry_path.exists():
            try:
                registry_path.unlink()
                return True
            except Exception as e:
                log.error(f"Failed to delete registry for team {team_id}: {e}")
                return False
        return True
