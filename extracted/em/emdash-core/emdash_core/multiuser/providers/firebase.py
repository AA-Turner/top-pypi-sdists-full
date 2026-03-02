"""Firebase Realtime Database sync provider for multiuser sessions.

This provider enables real-time synchronization of shared sessions across
multiple machines using Firebase Realtime Database.

Environment Variables Required:
    FIREBASE_PROJECT_ID: Your Firebase project ID
    FIREBASE_DATABASE_URL: Your Realtime Database URL (e.g., https://your-project.firebaseio.com)
    FIREBASE_CREDENTIALS_PATH: Path to service account JSON file

    OR for simpler setup:
    FIREBASE_API_KEY: Web API key (for REST API access)

Example:
    export EMDASH_MULTIUSER_PROVIDER=firebase
    export FIREBASE_PROJECT_ID=my-project-123
    export FIREBASE_DATABASE_URL=https://my-project-123-default-rtdb.firebaseio.com
    export FIREBASE_CREDENTIALS_PATH=/path/to/service-account.json
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Awaitable, Optional

import httpx

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


class FirebaseSyncProvider(SyncProvider):
    """Firebase Realtime Database sync provider.

    Provides real-time synchronization of shared sessions using Firebase
    Realtime Database. Supports:
    - Session state persistence
    - Real-time event streaming via REST + SSE
    - Participant presence tracking
    - Optimistic locking for conflict detection

    Database Structure:
        /sessions/{session_id}/
            state: SharedSession data
            events/: Event log for real-time updates
            presence/: Participant presence data
        /invites/{invite_code}: session_id mapping
        /projects/{project_id}/
            state: Project data
            tasks/{task_id}: Task data
        /team_projects/{team_id}/{project_id}: Project-team mapping

    Usage:
        provider = FirebaseSyncProvider(
            project_id="my-project",
            database_url="https://my-project.firebaseio.com",
            credentials_path="/path/to/credentials.json",
        )
        await provider.connect()

        # Create session
        info = await provider.create_session(session_id, owner_id, state)

        # Subscribe to events
        sub_id = await provider.subscribe(session_id, handle_event)
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        database_url: Optional[str] = None,
        credentials_path: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """Initialize Firebase provider.

        Args:
            project_id: Firebase project ID (or FIREBASE_PROJECT_ID env var)
            database_url: Realtime Database URL (or FIREBASE_DATABASE_URL env var)
            credentials_path: Path to service account JSON (or FIREBASE_CREDENTIALS_PATH env var)
            api_key: Web API key for REST access (or FIREBASE_API_KEY env var)
        """
        self._project_id = project_id or os.environ.get("FIREBASE_PROJECT_ID")
        self._database_url = database_url or os.environ.get("FIREBASE_DATABASE_URL")
        self._credentials_path = credentials_path or os.environ.get("FIREBASE_CREDENTIALS_PATH")
        self._api_key = api_key or os.environ.get("FIREBASE_API_KEY")

        # Normalize database URL
        if self._database_url and not self._database_url.endswith("/"):
            self._database_url = self._database_url.rstrip("/")

        self._connected = False
        self._auth_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

        # HTTP client for REST API
        self._client: Optional[httpx.AsyncClient] = None

        # Subscriptions: sub_id -> (session_id, handler, task)
        self._subscriptions: dict[str, tuple[str, Callable, asyncio.Task]] = {}

        # Local cache for reducing API calls
        self._session_cache: dict[str, SharedSession] = {}
        self._cache_ttl = 5  # seconds

    async def connect(self) -> bool:
        """Connect to Firebase and authenticate.

        Returns:
            True if connected successfully
        """
        if not self._database_url:
            log.error("FIREBASE_DATABASE_URL not set")
            return False

        try:
            # Initialize HTTP client
            self._client = httpx.AsyncClient(timeout=30.0)

            # Authenticate if credentials provided
            if self._credentials_path:
                await self._authenticate_with_service_account()
            elif self._api_key:
                # API key auth is simpler but less secure
                log.warning("Using API key auth - consider using service account for production")

            self._connected = True
            log.info(f"FirebaseSyncProvider connected to {self._database_url}")
            return True

        except Exception as e:
            log.error(f"Failed to connect to Firebase: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Firebase."""
        self._connected = False

        # Cancel all subscription tasks
        for sub_id, (_, _, task) in list(self._subscriptions.items()):
            task.cancel()
        self._subscriptions.clear()

        # Close HTTP client
        if self._client:
            await self._client.aclose()
            self._client = None

        log.info("FirebaseSyncProvider disconnected")

    async def _authenticate_with_service_account(self) -> None:
        """Authenticate using service account credentials."""
        try:
            import google.auth
            from google.auth.transport.requests import Request
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                self._credentials_path,
                scopes=["https://www.googleapis.com/auth/firebase.database"],
            )
            credentials.refresh(Request())

            self._auth_token = credentials.token
            self._token_expiry = credentials.expiry

            log.debug("Authenticated with service account")

        except ImportError:
            log.warning("google-auth not installed, using unauthenticated access")
        except Exception as e:
            log.warning(f"Service account auth failed: {e}, using unauthenticated access")

    async def _get_auth_params(self) -> dict[str, str]:
        """Get authentication parameters for requests."""
        params = {}

        # Refresh token if expired
        if self._auth_token and self._token_expiry:
            if datetime.utcnow() >= self._token_expiry:
                await self._authenticate_with_service_account()

        if self._auth_token:
            params["auth"] = self._auth_token
        elif self._api_key:
            params["key"] = self._api_key

        return params

    def _db_url(self, path: str) -> str:
        """Build full database URL for a path."""
        path = path.lstrip("/")
        return f"{self._database_url}/{path}.json"

    async def _db_get(self, path: str) -> Any:
        """GET request to Firebase."""
        url = self._db_url(path)
        params = await self._get_auth_params()

        response = await self._client.get(url, params=params)
        response.raise_for_status()

        return response.json()

    async def _db_put(self, path: str, data: Any) -> Any:
        """PUT request to Firebase (replace)."""
        url = self._db_url(path)
        params = await self._get_auth_params()

        response = await self._client.put(url, json=data, params=params)
        response.raise_for_status()

        return response.json()

    async def _db_patch(self, path: str, data: dict) -> Any:
        """PATCH request to Firebase (update)."""
        url = self._db_url(path)
        params = await self._get_auth_params()

        response = await self._client.patch(url, json=data, params=params)
        response.raise_for_status()

        return response.json()

    async def _db_post(self, path: str, data: Any) -> str:
        """POST request to Firebase (push). Returns generated key."""
        url = self._db_url(path)
        params = await self._get_auth_params()

        response = await self._client.post(url, json=data, params=params)
        response.raise_for_status()

        result = response.json()
        return result.get("name", "")

    async def _db_delete(self, path: str) -> None:
        """DELETE request to Firebase."""
        url = self._db_url(path)
        params = await self._get_auth_params()

        response = await self._client.delete(url, params=params)
        response.raise_for_status()

    async def create_session(
        self,
        session_id: str,
        owner_id: str,
        initial_state: dict[str, Any],
    ) -> SharedSessionInfo:
        """Create a new shared session in Firebase."""
        # Use the invite code from initial_state (generated by manager) instead of creating a new one
        invite_code = initial_state.get("invite_code") or generate_invite_code()
        now = datetime.utcnow().isoformat()

        # Get owner info from initial state
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

        # Write session to Firebase
        await self._db_put(f"sessions/{session_id}/state", session.to_dict())

        # Create invite code mapping
        await self._db_put(f"invites/{invite_code}", {
            "session_id": session_id,
            "created_at": now,
            "created_by": owner_id,
        })

        # Cache locally
        self._session_cache[session_id] = session

        log.info(f"Created session {session_id} in Firebase with invite {invite_code}")
        return session.get_info()

    async def join_session(
        self,
        invite_code: str,
        user_id: str,
        display_name: str,
    ) -> SharedSessionInfo:
        """Join a session via invite code."""
        invite_code = invite_code.upper().strip()

        # Look up session ID from invite
        session_id = await self.find_session_by_invite(invite_code)
        if not session_id:
            raise InvalidInviteCodeError(f"Invalid invite code: {invite_code}")

        # Get current session
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

        # Update Firebase
        await self._db_patch(f"sessions/{session_id}/state", {
            "participants": [p.to_dict() for p in session.participants],
            "version": session.version,
            "updated_at": session.updated_at,
        })

        # Push join event
        await self._push_event_internal(session_id, {
            "type": "participant_joined",
            "user_id": user_id,
            "display_name": display_name,
            "timestamp": now,
        })

        # Update cache
        self._session_cache[session_id] = session

        log.info(f"User {user_id} joined session {session_id}")
        return session.get_info()

    async def leave_session(
        self,
        session_id: str,
        user_id: str,
    ) -> None:
        """Leave a session."""
        session = await self._load_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        # Get participant info
        participant = session.get_participant(user_id)
        display_name = participant.display_name if participant else user_id

        # Remove participant
        session.remove_participant(user_id)

        # Update Firebase
        await self._db_patch(f"sessions/{session_id}/state", {
            "participants": [p.to_dict() for p in session.participants],
            "version": session.version,
            "updated_at": session.updated_at,
        })

        # Push leave event
        await self._push_event_internal(session_id, {
            "type": "participant_left",
            "user_id": user_id,
            "display_name": display_name,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # Remove presence
        await self._db_delete(f"sessions/{session_id}/presence/{user_id}")

        # Update cache
        self._session_cache[session_id] = session

        log.info(f"User {user_id} left session {session_id}")

    async def push_event(
        self,
        session_id: str,
        event: SharedEvent,
    ) -> None:
        """Push an event to the session event log."""
        await self._push_event_internal(session_id, event.to_dict())

    async def _push_event_internal(self, session_id: str, event_data: dict) -> str:
        """Internal method to push event data."""
        # Add timestamp if not present
        if "timestamp" not in event_data:
            event_data["timestamp"] = datetime.utcnow().isoformat()

        # Push to events list
        event_key = await self._db_post(f"sessions/{session_id}/events", event_data)

        return event_key

    async def subscribe(
        self,
        session_id: str,
        handler: Callable[[SharedEvent], Awaitable[None]],
    ) -> str:
        """Subscribe to session events using Firebase REST streaming."""
        subscription_id = str(uuid.uuid4())

        # Start background task to listen for events
        task = asyncio.create_task(
            self._event_listener(session_id, handler, subscription_id)
        )

        self._subscriptions[subscription_id] = (session_id, handler, task)

        log.debug(f"Subscribed {subscription_id} to session {session_id}")
        return subscription_id

    async def _event_listener(
        self,
        session_id: str,
        handler: Callable[[SharedEvent], Awaitable[None]],
        subscription_id: str,
    ) -> None:
        """Background task to listen for Firebase events via REST streaming."""
        url = self._db_url(f"sessions/{session_id}/events")
        params = await self._get_auth_params()

        # Track last seen event to avoid duplicates
        last_event_key: Optional[str] = None

        while subscription_id in self._subscriptions:
            try:
                # Use Firebase REST streaming (Server-Sent Events)
                # Note: This requires the httpx-sse extension or manual SSE parsing

                # Fallback to polling if SSE not available
                await self._poll_events(session_id, handler, last_event_key)

                await asyncio.sleep(1)  # Poll interval

            except asyncio.CancelledError:
                log.debug(f"Event listener cancelled for {subscription_id}")
                break
            except Exception as e:
                log.warning(f"Event listener error: {e}")
                await asyncio.sleep(5)  # Back off on error

    async def _poll_events(
        self,
        session_id: str,
        handler: Callable[[SharedEvent], Awaitable[None]],
        last_key: Optional[str],
    ) -> Optional[str]:
        """Poll for new events (fallback when SSE not available)."""
        try:
            # Get events ordered by key, limited to recent
            events_data = await self._db_get(
                f"sessions/{session_id}/events?orderBy=\"$key\"&limitToLast=10"
            )

            if not events_data or not isinstance(events_data, dict):
                return last_key

            # Process new events
            for key, event_data in sorted(events_data.items()):
                if last_key and key <= last_key:
                    continue

                # Convert to SharedEvent
                event = SharedEvent(
                    id=key,
                    session_id=session_id,
                    event_type=event_data.get("type", "unknown"),
                    data=event_data,
                    timestamp=event_data.get("timestamp", ""),
                    source_user_id=event_data.get("user_id"),
                    sequence=0,
                )

                try:
                    await handler(event)
                except Exception as e:
                    log.warning(f"Event handler error: {e}")

                last_key = key

            return last_key

        except Exception as e:
            log.warning(f"Poll events error: {e}")
            return last_key

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from session events."""
        if subscription_id in self._subscriptions:
            _, _, task = self._subscriptions.pop(subscription_id)
            task.cancel()
            log.debug(f"Unsubscribed {subscription_id}")

    async def get_session_state(
        self,
        session_id: str,
    ) -> SharedSessionInfo:
        """Get current session state."""
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

    async def _load_session(self, session_id: str) -> Optional[SharedSession]:
        """Load session from Firebase."""
        try:
            data = await self._db_get(f"sessions/{session_id}/state")
            if not data:
                return None

            session = SharedSession.from_dict(data)
            self._session_cache[session_id] = session
            return session

        except Exception as e:
            log.error(f"Failed to load session {session_id}: {e}")
            return None

    async def update_session_state(
        self,
        session_id: str,
        updates: dict[str, Any],
        expected_version: Optional[int] = None,
    ) -> SharedSessionInfo:
        """Update session state with optimistic locking."""
        # Load current state
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

        # Update Firebase
        await self._db_put(f"sessions/{session_id}/state", session.to_dict())

        # Update cache
        self._session_cache[session_id] = session

        return session.get_info()

    async def heartbeat(
        self,
        session_id: str,
        user_id: str,
    ) -> None:
        """Update presence for a user."""
        now = datetime.utcnow().isoformat()

        # Update presence in Firebase
        await self._db_put(f"sessions/{session_id}/presence/{user_id}", {
            "last_seen": now,
            "online": True,
        })

        # Also update participant in session state
        session = await self._load_session(session_id)
        if session:
            session.update_participant_presence(user_id, is_online=True)
            await self._db_patch(f"sessions/{session_id}/state", {
                "participants": [p.to_dict() for p in session.participants],
            })

    async def find_session_by_invite(
        self,
        invite_code: str,
    ) -> Optional[str]:
        """Find session ID by invite code."""
        invite_code = invite_code.upper().strip()

        try:
            data = await self._db_get(f"invites/{invite_code}")
            if data and isinstance(data, dict):
                return data.get("session_id")
            return None

        except Exception as e:
            log.warning(f"Error finding session by invite: {e}")
            return None

    async def delete_session(self, session_id: str) -> None:
        """Delete a session completely from Firebase."""
        # Get session to find invite code
        session = await self._load_session(session_id)
        if session:
            # Delete invite mapping
            await self._db_delete(f"invites/{session.invite_code}")

        # Delete session data
        await self._db_delete(f"sessions/{session_id}")

        # Remove from cache
        self._session_cache.pop(session_id, None)

        log.info(f"Deleted session {session_id} from Firebase")

    # ─────────────────────────────────────────────────────────────
    # Team Operations
    # ─────────────────────────────────────────────────────────────

    async def create_team(self, team_id: str, team_data: dict[str, Any]) -> None:
        """Create a new team in Firebase.

        Database Structure:
            /teams/{team_id}: Team data
            /team_invites/{invite_code}: team_id mapping
            /team_sessions/{team_id}/{session_id}: Session metadata
        """
        # Write team data
        await self._db_put(f"teams/{team_id}", team_data)

        # Create invite code mapping
        invite_code = team_data.get("invite_code", "")
        if invite_code:
            await self._db_put(f"team_invites/{invite_code}", {
                "team_id": team_id,
                "created_at": team_data.get("created_at"),
            })

        log.info(f"Created team {team_id} in Firebase")

    async def get_team(self, team_id: str) -> Optional[dict[str, Any]]:
        """Get team data from Firebase."""
        try:
            data = await self._db_get(f"teams/{team_id}")
            return data if data else None
        except Exception as e:
            log.warning(f"Error getting team {team_id}: {e}")
            return None

    async def update_team(self, team_id: str, team_data: dict[str, Any]) -> None:
        """Update team data in Firebase."""
        await self._db_put(f"teams/{team_id}", team_data)
        log.debug(f"Updated team {team_id}")

    async def delete_team(self, team_id: str) -> None:
        """Delete a team from Firebase."""
        # Get team to find invite code
        team_data = await self.get_team(team_id)
        if team_data:
            invite_code = team_data.get("invite_code")
            if invite_code:
                await self._db_delete(f"team_invites/{invite_code}")

        # Delete team data
        await self._db_delete(f"teams/{team_id}")

        # Delete team sessions mapping
        await self._db_delete(f"team_sessions/{team_id}")

        log.info(f"Deleted team {team_id} from Firebase")

    async def find_team_by_invite(self, invite_code: str) -> Optional[str]:
        """Find team ID by invite code."""
        invite_code = invite_code.upper().strip()

        try:
            data = await self._db_get(f"team_invites/{invite_code}")
            if data and isinstance(data, dict):
                return data.get("team_id")
            return None
        except Exception as e:
            log.warning(f"Error finding team by invite: {e}")
            return None

    async def get_user_teams(self, user_id: str) -> list[dict[str, Any]]:
        """Get all teams a user is a member of.

        Note: This requires querying all teams and filtering,
        which is not efficient for large numbers of teams.
        Consider adding a user_teams index for production.
        """
        try:
            all_teams = await self._db_get("teams")
            if not all_teams or not isinstance(all_teams, dict):
                return []

            user_teams = []
            for team_id, team_data in all_teams.items():
                if not isinstance(team_data, dict):
                    continue

                members = team_data.get("members", [])
                for member in members:
                    if isinstance(member, dict) and member.get("user_id") == user_id:
                        user_teams.append(team_data)
                        break

            return user_teams

        except Exception as e:
            log.warning(f"Error getting user teams: {e}")
            return []

    async def add_session_to_team(
        self,
        team_id: str,
        session_id: str,
        title: Optional[str] = None,
    ) -> None:
        """Add a session to a team.

        Also updates the session's team_id and visibility.
        """
        # Get session info for metadata
        session = await self._load_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        # Update session with team info
        session.team_id = team_id
        session.visibility = "team"  # Will be converted to enum
        if title:
            session.title = title

        # Save session update
        await self._db_patch(f"sessions/{session_id}/state", {
            "team_id": team_id,
            "visibility": "team",
            "title": title or session.title,
        })

        # Add to team_sessions index
        now = datetime.utcnow().isoformat()
        session_info = {
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
        await self._db_put(f"team_sessions/{team_id}/{session_id}", session_info)

        # Update cache
        self._session_cache[session_id] = session

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
            session.visibility = "private"

            await self._db_patch(f"sessions/{session_id}/state", {
                "team_id": None,
                "visibility": "private",
            })

            self._session_cache[session_id] = session

        # Remove from team_sessions index
        await self._db_delete(f"team_sessions/{team_id}/{session_id}")

        log.info(f"Removed session {session_id} from team {team_id}")

    async def list_team_sessions(self, team_id: str) -> list[dict[str, Any]]:
        """List all sessions in a team."""
        try:
            data = await self._db_get(f"team_sessions/{team_id}")
            if not data or not isinstance(data, dict):
                return []

            sessions = []
            for session_id, session_info in data.items():
                if isinstance(session_info, dict):
                    session_info["session_id"] = session_id
                    sessions.append(session_info)

            # Sort by updated_at descending (most recent first)
            sessions.sort(
                key=lambda s: s.get("updated_at", ""),
                reverse=True,
            )

            return sessions

        except Exception as e:
            log.warning(f"Error listing team sessions: {e}")
            return []

    async def update_team_session_info(
        self,
        team_id: str,
        session_id: str,
        updates: dict[str, Any],
    ) -> None:
        """Update session info in team listing (e.g., title, participant count)."""
        await self._db_patch(f"team_sessions/{team_id}/{session_id}", updates)

    # ─────────────────────────────────────────────────────────────
    # Registry Operations
    # ─────────────────────────────────────────────────────────────

    async def get_registry(self, team_id: str) -> Optional[dict[str, Any]]:
        """Get registry data for a team.

        Database Structure:
            /registries/{team_id}: TeamRegistry data

        Args:
            team_id: Team ID

        Returns:
            Registry data dict or None if not found
        """
        try:
            data = await self._db_get(f"registries/{team_id}")
            return data if data else None
        except Exception as e:
            log.warning(f"Error getting registry for team {team_id}: {e}")
            return None

    async def save_registry(self, team_id: str, registry: dict[str, Any]) -> bool:
        """Save registry data for a team.

        Args:
            team_id: Team ID
            registry: Registry data dict

        Returns:
            True if save succeeded
        """
        try:
            await self._db_put(f"registries/{team_id}", registry)
            log.debug(f"Saved registry for team {team_id}")
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
        try:
            await self._db_delete(f"registries/{team_id}")
            log.info(f"Deleted registry for team {team_id}")
            return True
        except Exception as e:
            log.error(f"Failed to delete registry for team {team_id}: {e}")
            return False
