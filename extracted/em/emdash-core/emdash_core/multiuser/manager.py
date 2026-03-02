"""SharedSessionManager - Main coordinator for multiuser sessions.

This module provides the central manager that ties together all multiuser
components: sessions, queues, broadcasters, and sync providers.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from .protocols import (
    SharedSessionInfo,
    SharedEvent,
    SharedEventType,
    Participant,
    ParticipantRole,
    QueuedMessage,
    SharedSessionState,
    SessionNotFoundError,
    InvalidInviteCodeError,
    NotAuthorizedError,
    TeamNotFoundError,
    TeamPermissionError,
)
from .webhooks import get_webhook_registry
from .models import SharedSession, UserIdentity
from .queue import SharedMessageQueue


def _build_agent_prompt(content: str, chat_context: list[dict]) -> str:
    """Build an agent prompt that includes recent chat history.

    When chat_context is empty the raw content is returned unchanged,
    so solo / non-chat invocations are unaffected.
    """
    if not chat_context:
        return content

    lines = []
    for msg in chat_context:
        name = msg.get("display_name", msg.get("user_id", "User"))
        lines.append(f"  {name}: {msg['content']}")
    context_block = "\n".join(lines)

    return (
        f"[Team chat context — recent messages from the conversation]\n"
        f"{context_block}\n\n"
        f"[Request]\n{content}"
    )
from .broadcaster import SharedEventBroadcaster, SSESharedEventHandler
from .invites import generate_invite_code, InviteManager
from .teams import (
    Team,
    TeamMember,
    TeamRole,
    SessionVisibility,
    TeamSessionInfo,
    TeamManager,
)

log = logging.getLogger(__name__)


class SharedSessionManager:
    """Coordinates all multiuser session components.

    This is the main entry point for multiuser functionality. It manages:
    - Session creation and joining via invite codes
    - Message queueing when the agent is busy
    - Event broadcasting to all participants
    - State synchronization across machines

    Usage:
        from emdash_core.multiuser import SharedSessionManager

        manager = SharedSessionManager()

        # Create session
        session, invite_code = await manager.create_session(
            owner_id="user_123",
            display_name="Alice",
            repo_root=Path("/path/to/repo"),
        )

        # Send message (queues if agent busy)
        await manager.send_message(session.session_id, "user_123", "Hello!")

        # Another user joins
        session = await manager.join_session("ABC123", "user_456", "Bob")
    """

    def __init__(
        self,
        storage_root: Optional[Path] = None,
        sync_provider: Optional[Any] = None,
    ):
        """Initialize the session manager.

        Args:
            storage_root: Root for local storage (queues, invites). Defaults to ~/.emdash/multiuser
            sync_provider: Optional sync provider (e.g., FirebaseSyncProvider) for cross-network sharing
        """
        self._storage_root = storage_root or Path.home() / ".emdash" / "multiuser"
        self._storage_root.mkdir(parents=True, exist_ok=True)

        # Sync provider for cross-network sharing (Firebase, etc.)
        self._sync_provider = sync_provider

        # In-memory state
        self._sessions: dict[str, SharedSession] = {}
        self._invite_index: dict[str, str] = {}  # invite_code -> session_id
        self._queues: dict[str, SharedMessageQueue] = {}
        self._broadcasters: dict[str, SharedEventBroadcaster] = {}

        # SSE handlers per user per session: session_id -> user_id -> handler
        self._sse_handlers: dict[str, dict[str, Any]] = {}

        # Agent runners per session (set externally via integrate_runner)
        self._runners: dict[str, Any] = {}  # session_id -> AgentRunner

        # Processing tasks
        self._processing_tasks: dict[str, asyncio.Task] = {}

        # Invite manager
        self._invite_manager = InviteManager(
            storage_path=self._storage_root / "invites.json"
        )

        # Team manager
        self._team_manager = TeamManager(
            storage_root=self._storage_root,
        )

        # Callbacks for session events
        self._on_session_created: list[Callable] = []
        self._on_participant_joined: list[Callable] = []
        self._on_participant_left: list[Callable] = []

    def set_sync_provider(self, provider: Any) -> None:
        """Set the sync provider for cross-network sharing."""
        self._sync_provider = provider

    def has_sync_provider(self) -> bool:
        """Check if a sync provider is configured."""
        return self._sync_provider is not None

    async def create_session(
        self,
        owner_id: str,
        display_name: str,
        repo_root: Optional[Path] = None,
        model: str = "",
        plan_mode: bool = False,
        initial_messages: Optional[list[dict]] = None,
    ) -> tuple[SharedSession, str]:
        """Create a new shared session.

        Args:
            owner_id: User ID of the session creator
            display_name: Display name of the owner
            repo_root: Repository root for the agent
            model: LLM model to use
            plan_mode: Whether to run in plan mode
            initial_messages: Optional pre-existing conversation history

        Returns:
            Tuple of (SharedSession, invite_code)
        """
        session_id = str(uuid.uuid4())
        invite_code = generate_invite_code()
        now = datetime.utcnow().isoformat()

        owner = Participant(
            user_id=owner_id,
            display_name=display_name,
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
            messages=initial_messages or [],
            model=model,
            plan_mode=plan_mode,
            repo_root=str(repo_root) if repo_root else "",
        )

        # Store in memory
        self._sessions[session_id] = session
        self._invite_index[invite_code] = session_id

        # If sync provider is available, store in remote (Firebase, etc.)
        if self._sync_provider:
            try:
                await self._sync_provider.create_session(
                    session_id=session_id,
                    owner_id=owner_id,
                    initial_state={
                        "invite_code": invite_code,
                        "owner_name": display_name,
                        "messages": initial_messages or [],
                        "model": model,
                        "plan_mode": plan_mode,
                        "repo_root": str(repo_root) if repo_root else "",
                    },
                )
                log.info(f"Session {session_id} stored in sync provider")
            except Exception as e:
                log.warning(f"Failed to store session in sync provider: {e}")

        # Create queue
        queue_path = self._storage_root / "queues" / f"{session_id}.json"
        self._queues[session_id] = SharedMessageQueue(
            session_id=session_id,
            storage_path=queue_path,
            on_event=lambda t, d: self._handle_queue_event(session_id, t, d),
        )

        # Create broadcaster
        self._broadcasters[session_id] = SharedEventBroadcaster(
            session_id=session_id,
        )

        # Initialize SSE handlers dict for this session
        self._sse_handlers[session_id] = {}

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("session.created", session.to_dict())

        # Create invite token
        self._invite_manager.create_invite(
            session_id=session_id,
            created_by=owner_id,
        )

        # Notify callbacks
        for callback in self._on_session_created:
            try:
                result = callback(session)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                log.warning(f"Session created callback error: {e}")

        log.info(f"Created shared session {session_id} with invite {invite_code}")
        return session, invite_code

    async def join_session(
        self,
        invite_code: str,
        user_id: str,
        display_name: str,
    ) -> SharedSession:
        """Join an existing session via invite code.

        Args:
            invite_code: The invite code to join with
            user_id: Joining user's ID
            display_name: Joining user's display name

        Returns:
            The joined SharedSession

        Raises:
            InvalidInviteCodeError: If invite code is invalid
            SessionNotFoundError: If session not found
        """
        invite_code = invite_code.upper().strip()
        log.info(f"join_session called with invite_code={invite_code}, user_id={user_id}")

        # Find session by invite code
        # Try multiple strategies: direct lookup, base code lookup, session scan, sync provider
        session = None
        session_id = self._invite_index.get(invite_code)
        if session_id:
            session = self._sessions.get(session_id)

        # If not found, try extracting base code and lookup
        if not session and "@" in invite_code:
            base_code = invite_code.split("@")[0]
            session_id = self._invite_index.get(base_code)
            if session_id:
                session = self._sessions.get(session_id)

        # Last resort: scan sessions for matching base code
        if not session:
            session = self.get_session_by_invite(invite_code)

        # If still not found and sync provider is available, try remote lookup
        if not session and self._sync_provider:
            try:
                log.info(f"Session not found locally, trying sync provider for {invite_code}")
                # Extract base code for Firebase lookup
                base_code = invite_code.split("@")[0] if "@" in invite_code else invite_code

                # Join via sync provider (which handles Firebase lookup and join)
                session_info = await self._sync_provider.join_session(
                    invite_code=base_code,
                    user_id=user_id,
                    display_name=display_name,
                )

                # Load full session data from provider
                full_session_data = await self._sync_provider.get_full_session(session_info.session_id)

                # Create local session from provider data
                session = SharedSession.from_dict(full_session_data)

                # Store in local memory
                self._sessions[session.session_id] = session
                self._invite_index[base_code] = session.session_id

                # Set up local components
                await self._setup_session_components(session)

                log.info(f"Loaded session {session.session_id} from sync provider")

                # Skip the local participant add since provider already did it
                # Dispatch webhook
                webhooks = get_webhook_registry()
                await webhooks.dispatch("session.joined", {
                    "session_id": session.session_id,
                    "participant": {"user_id": user_id, "display_name": display_name},
                    "session_state": {
                        "participants": [p.to_dict() for p in session.participants],
                    },
                })

                # Notify callbacks
                for callback in self._on_participant_joined:
                    try:
                        result = callback(session, session.get_participant(user_id))
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception as e:
                        log.warning(f"Participant joined callback error: {e}")

                log.info(f"User {user_id} joined session {session.session_id} via sync provider")
                return session

            except Exception as e:
                log.warning(f"Sync provider lookup failed: {e}")

        if not session:
            raise InvalidInviteCodeError(f"Invalid invite code: {invite_code}")

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

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("session.joined", {
            "session_id": session.session_id,
            "participant": participant.to_dict(),
            "session_state": {
                "participants": [p.to_dict() for p in session.participants],
            },
        })

        # Broadcast join event
        broadcaster = self._broadcasters.get(session.session_id)
        if broadcaster:
            await broadcaster.broadcast_participant_joined(user_id, display_name)

        # Notify callbacks
        for callback in self._on_participant_joined:
            try:
                result = callback(session, participant)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                log.warning(f"Participant joined callback error: {e}")

        log.info(f"User {user_id} joined session {session.session_id}")
        return session

    async def leave_session(
        self,
        session_id: str,
        user_id: str,
    ) -> bool:
        """Leave a shared session.

        Args:
            session_id: Session to leave
            user_id: User leaving

        Returns:
            True if left successfully
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        # Get participant info before removal
        participant = session.get_participant(user_id)
        display_name = participant.display_name if participant else user_id

        # Remove participant
        removed = session.remove_participant(user_id)
        if not removed:
            return False

        # Remove SSE handler
        if session_id in self._sse_handlers:
            self._sse_handlers[session_id].pop(user_id, None)

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("session.left", {
            "session_id": session_id,
            "user_id": user_id,
            "session_state": {
                "participants": [p.to_dict() for p in session.participants],
            },
        })

        # Broadcast leave event
        broadcaster = self._broadcasters.get(session_id)
        if broadcaster:
            await broadcaster.broadcast_participant_left(user_id, display_name)

        # Notify callbacks
        for callback in self._on_participant_left:
            try:
                result = callback(session, user_id)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                log.warning(f"Participant left callback error: {e}")

        log.info(f"User {user_id} left session {session_id}")
        return True

    async def send_message(
        self,
        session_id: str,
        user_id: str,
        content: str,
        images: Optional[list[dict]] = None,
        priority: int = 0,
    ) -> QueuedMessage:
        """Send a message in a shared session.

        If the agent is busy, the message is queued. Otherwise,
        it's processed immediately.

        Args:
            session_id: Session to send message in
            user_id: User sending the message
            content: Message content
            images: Optional images to include
            priority: Message priority (higher = more urgent)

        Returns:
            The queued message

        Raises:
            SessionNotFoundError: If session not found
            NotAuthorizedError: If user can't send messages
        """
        log.info(f"send_message called: session_id={session_id!r}, user_id={user_id}, manager_id={id(self)}")
        log.info(f"Current sessions in memory: {list(self._sessions.keys())}")
        log.info(f"Current queues in memory: {list(self._queues.keys())}")
        # Direct debug - check queue lookup
        direct_q = self._queues.get(session_id)
        log.info(f"Direct queue lookup result: {direct_q!r}, bool: {bool(direct_q) if direct_q else 'N/A'}")

        session = self._sessions.get(session_id)
        need_setup = session is None

        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        # Check authorization
        if not session.can_send_message(user_id):
            raise NotAuthorizedError(f"User {user_id} cannot send messages")

        # Ensure queue exists - set up components if session was loaded from provider
        # or if queue is missing for any reason
        # NOTE: Use 'is None' not 'if not queue' because SharedMessageQueue.__len__
        # returns 0 for empty queues, making them falsy
        queue = self._queues.get(session_id)
        if queue is None:
            log.warning(f"Queue not found for session {session_id}, setting up components...")
            await self._setup_session_components(session)
            queue = self._queues.get(session_id)

        if queue is None:
            log.error(f"Queue still not found after setup for session {session_id}")
            raise SessionNotFoundError(f"Queue for session {session_id} not found")

        # Enqueue message
        message = await queue.enqueue(user_id, content, images, priority)

        # Update participant last_seen
        session.update_participant_presence(user_id, is_online=True)

        # Broadcast queue update
        broadcaster = self._broadcasters.get(session_id)
        if broadcaster:
            await broadcaster.broadcast_queue_update(
                queue_length=len(queue),
                current_message_id=queue.current_message_id,
                current_user_id=queue.current_user_id,
            )

        # Start processing if not already running
        if session_id not in self._processing_tasks or self._processing_tasks[session_id].done():
            task = asyncio.create_task(self._process_queue(session_id))
            self._processing_tasks[session_id] = task

        log.info(f"Message queued in session {session_id} by {user_id}")
        return message

    async def _process_queue(self, session_id: str) -> None:
        """Process messages from the queue using the agent runner.

        This runs as a background task, processing messages one at a time.
        """
        queue = self._queues.get(session_id)
        session = self._sessions.get(session_id)
        broadcaster = self._broadcasters.get(session_id)

        if queue is None or session is None:
            return

        while True:
            # Try to dequeue
            message = await queue.dequeue(timeout=None)
            if not message:
                break

            # Update session state
            old_state = session.state
            session.state = SharedSessionState.AGENT_BUSY
            if broadcaster:
                await broadcaster.broadcast_state_change(old_state.value, session.state.value)
                broadcaster.set_current_user(message.user_id)

            try:
                # Get or create runner
                runner = self._runners.get(session_id)
                if runner:
                    # Build prompt with only NEW chat messages since the
                    # last @agent invocation (cursor-based dedup).
                    cursor = session.chat_history_cursor
                    chat_context = session.chat_history[cursor:][-50:]
                    session.chat_history_cursor = len(session.chat_history)
                    prompt = _build_agent_prompt(message.content, chat_context)

                    # Add user message to conversation
                    user_msg = {"role": "user", "content": prompt}
                    if message.images:
                        user_msg["images"] = message.images

                    # Run agent
                    if runner._messages:
                        response = runner.chat(prompt, images=message.images or None)
                    else:
                        response = runner.run(prompt, images=message.images or None)

                    # Update session messages
                    session.messages = runner._messages

                else:
                    # No server-side runner - broadcast request for owner's CLI to process
                    # The owner's CLI will receive this via SSE and process with its local agent
                    log.info(f"No server-side runner for session {session_id}, broadcasting process_message_request")
                    log.info(f"  Broadcaster exists: {broadcaster is not None}")
                    if broadcaster:
                        log.info(f"  Broadcaster handler count: {broadcaster.handler_count}")
                        # Get display name for the requesting user
                        participant = session.get_participant(message.user_id)
                        display_name = participant.display_name if participant else "User"
                        # Include only NEW chat messages since the last
                        # @agent invocation (cursor-based dedup).
                        cursor = session.chat_history_cursor
                        chat_context = session.chat_history[cursor:][-50:]
                        session.chat_history_cursor = len(session.chat_history)
                        await broadcaster.broadcast(
                            SharedEventType.PROCESS_MESSAGE_REQUEST.value,
                            {
                                "message_id": message.id,
                                "user_id": message.user_id,
                                "display_name": display_name,
                                "content": message.content,
                                "images": message.images,
                                "queued_at": message.queued_at,
                                "owner_id": session.owner_id,
                                "chat_context": chat_context,
                            },
                        )
                        log.info(f"  Broadcast completed")
                    else:
                        log.warning(f"  No broadcaster for session {session_id}!")
                    # Mark message as complete since we've handed it off
                    # The owner's CLI will process and broadcast the response
                    await queue.complete(message.id)
                    session.state = SharedSessionState.ACTIVE
                    if broadcaster:
                        await broadcaster.broadcast_state_change(
                            SharedSessionState.AGENT_BUSY.value,
                            SharedSessionState.ACTIVE.value,
                        )
                    continue

                # Update session state
                session.updated_at = datetime.utcnow().isoformat()
                session.version += 1

                # Dispatch webhook
                webhooks = get_webhook_registry()
                await webhooks.dispatch("session.state_updated", session.to_dict())

            except Exception as e:
                log.error(f"Error processing message in session {session_id}: {e}")
                if broadcaster:
                    await broadcaster.broadcast(
                        SharedEventType.STATE_CHANGED.value,
                        {"error": str(e)},
                    )

            finally:
                # Complete the message
                await queue.complete(message.id)

                # Reset state
                session.state = SharedSessionState.ACTIVE
                if broadcaster:
                    await broadcaster.broadcast_state_change(
                        SharedSessionState.AGENT_BUSY.value,
                        SharedSessionState.ACTIVE.value,
                    )
                    broadcaster.set_current_user(None)

    async def _setup_session_components(self, session: SharedSession) -> None:
        """Set up local components for a session loaded from provider."""
        session_id = session.session_id

        # Create queue
        queue_path = self._storage_root / "queues" / f"{session_id}.json"
        self._queues[session_id] = SharedMessageQueue(
            session_id=session_id,
            storage_path=queue_path,
            on_event=lambda t, d: self._handle_queue_event(session_id, t, d),
        )

        # Restore queue state from session
        for msg in session.message_queue:
            await self._queues[session_id].enqueue(
                msg.user_id, msg.content, msg.images, msg.priority
            )

        # Create broadcaster
        self._broadcasters[session_id] = SharedEventBroadcaster(
            session_id=session_id,
        )

        # Initialize SSE handlers dict
        self._sse_handlers[session_id] = {}

    def _handle_queue_event(self, session_id: str, event_type: str, data: dict) -> None:
        """Handle events from the message queue."""
        broadcaster = self._broadcasters.get(session_id)
        if broadcaster:
            asyncio.create_task(broadcaster.broadcast(event_type, data))

    # ─────────────────────────────────────────────────────────────
    # Integration methods
    # ─────────────────────────────────────────────────────────────

    def integrate_runner(self, session_id: str, runner: Any) -> None:
        """Integrate an AgentRunner with a shared session.

        This wires up the runner's emitter to the broadcaster so events
        are fanned out to all participants.

        Args:
            session_id: Session to integrate with
            runner: AgentRunner instance
        """
        self._runners[session_id] = runner

        # Wire emitter to broadcaster
        broadcaster = self._broadcasters.get(session_id)
        if broadcaster and hasattr(runner, "emitter"):
            runner.emitter.add_handler(broadcaster)

        # Sync messages from runner to session
        session = self._sessions.get(session_id)
        if session and hasattr(runner, "_messages"):
            session.messages = runner._messages

        log.info(f"Integrated runner with session {session_id}")

    async def add_sse_handler_async(self, session_id: str, user_id: str, sse_handler: Any) -> None:
        """Add an SSE handler for a user in a session (async version).

        Args:
            session_id: Session ID
            user_id: User ID
            sse_handler: SSEHandler instance
        """
        log.info(f"[SSE] add_sse_handler_async called: session={session_id}, user={user_id}")
        log.info(f"[SSE] Current broadcasters: {list(self._broadcasters.keys())}")
        log.info(f"[SSE] Current sessions: {list(self._sessions.keys())}")

        if session_id not in self._sse_handlers:
            self._sse_handlers[session_id] = {}

        # Ensure broadcaster exists - set up session components if needed
        if session_id not in self._broadcasters:
            log.info(f"[SSE] Broadcaster missing for {session_id}, checking session...")
            session = self._sessions.get(session_id)
            if session:
                log.info(f"[SSE] Session found, setting up components...")
                await self._setup_session_components(session)
            else:
                log.warning(f"[SSE] Session {session_id} not found in memory!")

        # Create adapter and add to broadcaster
        adapter = SSESharedEventHandler(sse_handler)
        self._sse_handlers[session_id][user_id] = adapter

        broadcaster = self._broadcasters.get(session_id)
        if broadcaster:
            broadcaster.add_handler(adapter)
            log.info(f"[SSE] Handler added! session={session_id}, user={user_id}, total_handlers={broadcaster.handler_count}")
        else:
            log.error(f"[SSE] FAILED: No broadcaster for {session_id}!")

    def add_sse_handler(self, session_id: str, user_id: str, sse_handler: Any) -> None:
        """Add an SSE handler for a user in a session (sync wrapper).

        Args:
            session_id: Session ID
            user_id: User ID
            sse_handler: SSEHandler instance
        """
        # Try to run async version
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Schedule the async version
                asyncio.create_task(self.add_sse_handler_async(session_id, user_id, sse_handler))
            else:
                loop.run_until_complete(self.add_sse_handler_async(session_id, user_id, sse_handler))
        except RuntimeError:
            # Fallback: just do sync setup
            if session_id not in self._sse_handlers:
                self._sse_handlers[session_id] = {}

            # Ensure broadcaster exists
            if session_id not in self._broadcasters:
                session = self._sessions.get(session_id)
                if session:
                    log.info(f"Creating broadcaster for session {session_id} (sync fallback)")
                    self._broadcasters[session_id] = SharedEventBroadcaster(
                        session_id=session_id,
                    )

            adapter = SSESharedEventHandler(sse_handler)
            self._sse_handlers[session_id][user_id] = adapter

            broadcaster = self._broadcasters.get(session_id)
            if broadcaster:
                broadcaster.add_handler(adapter)
                log.info(f"SSE handler added (sync) for session {session_id}")

    def remove_sse_handler(self, session_id: str, user_id: str) -> None:
        """Remove an SSE handler for a user.

        Args:
            session_id: Session ID
            user_id: User ID
        """
        if session_id not in self._sse_handlers:
            return

        adapter = self._sse_handlers[session_id].pop(user_id, None)
        if adapter:
            broadcaster = self._broadcasters.get(session_id)
            if broadcaster:
                broadcaster.remove_handler(adapter)

    async def broadcast_event(
        self,
        session_id: str,
        event_type: str,
        data: dict,
        source_user_id: str | None = None,
    ) -> None:
        """Broadcast an event to all participants in a session.

        This is used by the owner's CLI to relay agent responses
        to all participants after processing messages locally.

        Args:
            session_id: Session ID
            event_type: Event type string
            data: Event data dict
            source_user_id: User who triggered the event (for filtering)
        """
        broadcaster = self._broadcasters.get(session_id)
        log.info(f"[BROADCAST] event={event_type}, session={session_id}, broadcaster_exists={broadcaster is not None}")
        if broadcaster:
            log.info(f"[BROADCAST] handlers={broadcaster.handler_count}, source_user={source_user_id}")
            await broadcaster.broadcast(event_type, data, source_user_id=source_user_id)
            log.info(f"[BROADCAST] Done: {event_type}")
        else:
            log.error(f"[BROADCAST] FAILED: No broadcaster for session {session_id}!")

    # ─────────────────────────────────────────────────────────────
    # Query methods
    # ─────────────────────────────────────────────────────────────

    def get_session(self, session_id: str) -> Optional[SharedSession]:
        """Get a session by ID."""
        return self._sessions.get(session_id)

    def get_session_by_invite(self, invite_code: str) -> Optional[SharedSession]:
        """Get a session by invite code.

        Handles both base codes (e.g., "ABC123") and full codes with port (e.g., "ABC123@57220").
        """
        invite_code = invite_code.upper().strip()
        # Extract base code if it has a port
        base_code = invite_code.split("@")[0] if "@" in invite_code else invite_code

        for session in self._sessions.values():
            if not session.invite_code:
                continue
            # Get base code from session's invite_code
            session_base = session.invite_code.split("@")[0].upper() if "@" in session.invite_code else session.invite_code.upper()
            # Match if base codes match OR full codes match
            if session_base == base_code or session.invite_code.upper() == invite_code:
                return session
        return None

    def get_user_sessions(self, user_id: str) -> list[SharedSession]:
        """Get all sessions a user is participating in."""
        return [
            session
            for session in self._sessions.values()
            if session.get_participant(user_id) is not None
        ]

    def get_session_participants(self, session_id: str) -> list[Participant]:
        """Get participants in a session."""
        session = self._sessions.get(session_id)
        return session.participants if session else []

    def get_queue_status(self, session_id: str) -> dict[str, Any]:
        """Get message queue status for a session."""
        queue = self._queues.get(session_id)
        if queue is None:
            return {"error": "Queue not found"}

        return {
            "length": len(queue),
            "agent_busy": queue.is_agent_busy,
            "current_message_id": queue.current_message_id,
            "current_user_id": queue.current_user_id,
        }

    # ─────────────────────────────────────────────────────────────
    # Callback registration
    # ─────────────────────────────────────────────────────────────

    def on_session_created(self, callback: Callable) -> None:
        """Register a callback for session creation."""
        self._on_session_created.append(callback)

    def on_participant_joined(self, callback: Callable) -> None:
        """Register a callback for participant joins."""
        self._on_participant_joined.append(callback)

    def on_participant_left(self, callback: Callable) -> None:
        """Register a callback for participant leaves."""
        self._on_participant_left.append(callback)

    # ─────────────────────────────────────────────────────────────
    # Team Management
    # ─────────────────────────────────────────────────────────────

    async def create_team(
        self,
        name: str,
        user_id: str,
        display_name: str,
        description: str = "",
    ) -> Team:
        """Create a new team.

        Args:
            name: Team name
            user_id: Creator's user ID (becomes admin)
            display_name: Creator's display name
            description: Optional team description

        Returns:
            The created Team
        """
        team = await self._team_manager.create_team(
            name=name,
            creator_id=user_id,
            creator_name=display_name,
            description=description,
        )
        log.info(f"Created team '{name}' with ID {team.team_id}")
        return team

    async def join_team(
        self,
        invite_code: str,
        user_id: str,
        display_name: str,
    ) -> Team:
        """Join a team using invite code.

        Args:
            invite_code: Team invite code (e.g., "T-ABC12345")
            user_id: Joining user's ID
            display_name: Joining user's display name

        Returns:
            The joined Team

        Raises:
            ValueError: If invite code is invalid
        """
        team = await self._team_manager.join_team(
            invite_code=invite_code,
            user_id=user_id,
            display_name=display_name,
        )
        log.info(f"User {user_id} joined team {team.team_id}")
        return team

    async def leave_team(self, team_id: str, user_id: str) -> bool:
        """Leave a team.

        Args:
            team_id: Team to leave
            user_id: User leaving

        Returns:
            True if left successfully
        """
        return await self._team_manager.leave_team(team_id, user_id)

    async def get_team(self, team_id: str) -> Optional[Team]:
        """Get a team by ID."""
        return await self._team_manager.get_team(team_id)

    async def get_user_teams(self, user_id: str) -> list[Team]:
        """Get all teams a user is a member of."""
        return await self._team_manager.get_user_teams(user_id)

    async def add_session_to_team(
        self,
        team_id: str,
        session_id: str,
        user_id: str,
        title: Optional[str] = None,
    ) -> bool:
        """Add a session to a team.

        The user must own the session or be a team admin.

        Args:
            team_id: Target team
            session_id: Session to add
            user_id: User adding the session
            title: Optional title for the session in team listings

        Returns:
            True if added successfully

        Raises:
            TeamNotFoundError: If team not found
            TeamPermissionError: If user lacks permission
            SessionNotFoundError: If session not found
        """
        # Verify team exists
        team = await self._team_manager.get_team(team_id)
        if not team:
            raise TeamNotFoundError(f"Team {team_id} not found")

        # Verify session exists and user has permission
        session = self._sessions.get(session_id)

        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        # Check permission: must be session owner or team admin
        if not session.is_owner(user_id) and not team.is_admin(user_id):
            raise TeamPermissionError(
                "Must be session owner or team admin to add sessions"
            )

        # Update session
        session.team_id = team_id
        session.visibility = SessionVisibility.TEAM
        if title:
            session.title = title

        # Update in memory
        self._sessions[session_id] = session

        # Add via team manager
        await self._team_manager.add_session_to_team(
            team_id=team_id,
            session_id=session_id,
            user_id=user_id,
            title=title,
        )

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("team.session_added", {
            "team_id": team_id,
            "session_id": session_id,
            "session_info": session.to_dict(),
        })

        # Broadcast event
        broadcaster = self._broadcasters.get(session_id)
        if broadcaster:
            await broadcaster.broadcast(
                SharedEventType.SESSION_ADDED_TO_TEAM.value,
                {
                    "session_id": session_id,
                    "team_id": team_id,
                    "team_name": team.name,
                    "added_by": user_id,
                },
            )

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
            user_id: User removing the session

        Returns:
            True if removed successfully
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        team_id = session.team_id
        if not team_id:
            return False  # Not in a team

        # Verify permission
        team = await self._team_manager.get_team(team_id)
        if team and not session.is_owner(user_id) and not team.is_admin(user_id):
            raise TeamPermissionError(
                "Must be session owner or team admin to remove sessions"
            )

        # Update session
        session.team_id = None
        session.visibility = SessionVisibility.PRIVATE

        # Remove via team manager
        await self._team_manager.remove_session_from_team(session_id, user_id)

        # Broadcast event
        broadcaster = self._broadcasters.get(session_id)
        if broadcaster:
            await broadcaster.broadcast(
                SharedEventType.SESSION_REMOVED_FROM_TEAM.value,
                {
                    "session_id": session_id,
                    "team_id": team_id,
                    "removed_by": user_id,
                },
            )

        log.info(f"Removed session {session_id} from team {team_id}")
        return True

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
        return await self._team_manager.list_team_sessions(team_id, user_id)

    async def join_team_session(
        self,
        team_id: str,
        session_id: str,
        user_id: str,
        display_name: str,
    ) -> SharedSession:
        """Join a session from a team (team members can join without invite).

        Args:
            team_id: Team the session belongs to
            session_id: Session to join
            user_id: User joining
            display_name: User's display name

        Returns:
            The joined SharedSession

        Raises:
            TeamPermissionError: If user is not a team member
            SessionNotFoundError: If session not found or not in team
        """
        # Verify team membership
        team = await self._team_manager.get_team(team_id)
        if not team:
            raise TeamNotFoundError(f"Team {team_id} not found")

        if not team.is_member(user_id):
            raise TeamPermissionError("Must be a team member to join team sessions")

        # Get session
        session = self._sessions.get(session_id)

        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        # Verify session is in the team
        if session.team_id != team_id:
            raise SessionNotFoundError(f"Session {session_id} is not in team {team_id}")

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

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("session.joined", {
            "session_id": session.session_id,
            "participant": participant.to_dict(),
            "session_state": {
                "participants": [p.to_dict() for p in session.participants],
            },
        })

        # Broadcast join event
        broadcaster = self._broadcasters.get(session.session_id)
        if broadcaster:
            await broadcaster.broadcast_participant_joined(user_id, display_name)

        log.info(f"User {user_id} joined team session {session_id}")
        return session

    def get_team_manager(self) -> TeamManager:
        """Get the underlying TeamManager instance."""
        return self._team_manager

    # ─────────────────────────────────────────────────────────────
    # Registry Operations
    # ─────────────────────────────────────────────────────────────

    async def get_team_registry(self, team_id: str, user_id: str):
        """Get the registry for a team.

        Args:
            team_id: Team ID
            user_id: Requesting user (must be team member)

        Returns:
            TeamRegistry for the team
        """
        return await self._team_manager.get_team_registry(team_id, user_id)

    async def save_team_registry(self, registry, user_id: str) -> bool:
        """Save the registry for a team.

        Args:
            registry: Registry to save
            user_id: User saving (must be team admin)

        Returns:
            True if saved successfully
        """
        return await self._team_manager.save_team_registry(registry, user_id)

    async def sync_team_registry(
        self,
        team_id: str,
        user_id: str,
        strategy: str = "remote_wins",
    ):
        """Sync the team registry between local and remote.

        Args:
            team_id: Team ID
            user_id: Requesting user (must be team member)
            strategy: Conflict resolution strategy

        Returns:
            Synced TeamRegistry
        """
        return await self._team_manager.sync_team_registry(team_id, user_id, strategy)

    # ─────────────────────────────────────────────────────────────
    # Sync
    # ─────────────────────────────────────────────────────────────

    def sync_sessions(self, session_dicts: list[dict]) -> int:
        """Load sessions from consumer's durable store into in-memory state.

        Called at startup by the webhook consumer to restore sessions.
        """
        count = 0
        for data in session_dicts:
            try:
                session = SharedSession.from_dict(data)
                self._sessions[session.session_id] = session
                # Index invite code by BASE code (without port) for /join lookup
                if session.invite_code:
                    invite_code = session.invite_code
                    base_code = invite_code.split("@")[0].upper() if "@" in invite_code else invite_code.upper()
                    self._invite_index[base_code] = session.session_id
                count += 1
            except Exception as e:
                log.warning(f"Failed to sync session: {e}")
        log.info(f"Synced {count} sessions into memory")
        return count

    # ─────────────────────────────────────────────────────────────
    # Project Integration
    # ─────────────────────────────────────────────────────────────

    async def link_session_to_project(
        self,
        session_id: str,
        project_id: str,
        task_id: Optional[str] = None,
        invite_code: Optional[str] = None,
    ) -> Optional["SharedSession"]:
        """Link a session to a project and optionally a task.

        Args:
            session_id: Session to link
            project_id: Project to link to
            task_id: Optional task to link to
            invite_code: Optional full invite code (with port) for joining

        Fires session.linked_to_project webhook.
        """
        session = self._sessions.get(session_id)
        if not session:
            return None

        session.project_id = project_id
        if task_id is not None:
            session.task_id = task_id
        # Update invite_code if provided (includes port for cross-instance joining)
        if invite_code:
            # Remove old index entry if exists (try both full code and base code)
            old_code = session.invite_code
            if old_code:
                # Try removing with full code
                if old_code in self._invite_index:
                    del self._invite_index[old_code]
                # Try removing base code (without port)
                old_base = old_code.split("@")[0].upper() if "@" in old_code else old_code.upper()
                if old_base in self._invite_index:
                    del self._invite_index[old_base]

            # Store full code on session (for display with port info)
            session.invite_code = invite_code

            # Index by BASE code (without port) since /join strips port before lookup
            base_code = invite_code.split("@")[0].upper() if "@" in invite_code else invite_code.upper()
            self._invite_index[base_code] = session_id
        session.updated_at = datetime.utcnow().isoformat()
        session.version += 1

        # Fire webhook for persistence (include full session for storage)
        webhooks = get_webhook_registry()
        await webhooks.dispatch("session.linked_to_project", session.to_dict())

        log.info(f"Linked session {session_id} to project {project_id}" +
                 (f" task {task_id}" if task_id else ""))
        return session

    async def unlink_session_from_project(self, session_id: str) -> Optional["SharedSession"]:
        """Remove project/task link from a session."""
        session = self._sessions.get(session_id)
        if not session:
            return None

        old_project = session.project_id
        session.project_id = None
        session.task_id = None
        session.updated_at = datetime.utcnow().isoformat()
        session.version += 1

        webhooks = get_webhook_registry()
        await webhooks.dispatch("session.unlinked_from_project", {
            "session_id": session_id,
            "project_id": old_project,
        })

        return session

    async def get_project_sessions(self, project_id: str) -> list["SharedSession"]:
        """Get all sessions linked to a project."""
        return [
            s for s in self._sessions.values()
            if s.project_id == project_id
        ]

    # ─────────────────────────────────────────────────────────────
    # Cleanup
    # ─────────────────────────────────────────────────────────────

    async def close_session(self, session_id: str, user_id: str) -> bool:
        """Close a shared session (owner only).

        Args:
            session_id: Session to close
            user_id: User attempting to close (must be owner)

        Returns:
            True if closed successfully
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        if not session.is_owner(user_id):
            raise NotAuthorizedError(f"Only the owner can close the session")

        # Cancel processing task
        if session_id in self._processing_tasks:
            self._processing_tasks[session_id].cancel()
            del self._processing_tasks[session_id]

        # Dispatch webhook
        webhooks = get_webhook_registry()
        await webhooks.dispatch("session.closed", {
            "session_id": session_id,
            "invite_code": session.invite_code,
        })

        # Broadcast close event
        broadcaster = self._broadcasters.get(session_id)
        if broadcaster:
            await broadcaster.broadcast(
                SharedEventType.SESSION_CLOSED.value,
                {"session_id": session_id, "closed_by": user_id},
            )

        # Clean up components
        self._invite_index.pop(session.invite_code, None)
        self._sessions.pop(session_id, None)
        self._queues.pop(session_id, None)
        self._broadcasters.pop(session_id, None)
        self._runners.pop(session_id, None)
        self._sse_handlers.pop(session_id, None)

        # Revoke invites
        self._invite_manager.revoke_session_invites(session_id)

        log.info(f"Closed session {session_id}")
        return True


# Global manager instance (lazily initialized)
_global_manager: Optional[SharedSessionManager] = None
_manager_initialized = False
_init_lock: asyncio.Lock = asyncio.Lock()


def _get_init_lock() -> asyncio.Lock:
    """Get the initialization lock."""
    return _init_lock


def get_shared_session_manager() -> SharedSessionManager:
    """Get the global SharedSessionManager instance (sync version).

    WARNING: This creates a manager without provider if called before
    async initialization. For API routes, use `await get_or_init_manager()` instead.
    """
    global _global_manager

    if _global_manager is None:
        log.warning("get_shared_session_manager called before async init - creating basic manager")
        _global_manager = SharedSessionManager()

    return _global_manager


async def get_or_init_manager() -> SharedSessionManager:
    """Get the global SharedSessionManager, initializing with provider if needed.

    This is the preferred way to get the manager from async contexts (API routes).
    It ensures the manager is properly initialized with the configured sync provider.
    """
    global _global_manager, _manager_initialized

    if _global_manager is not None:
        log.debug(f"Returning existing manager (id={id(_global_manager)})")
        return _global_manager

    log.info("Manager not initialized, initializing now...")

    # Use lock to prevent multiple concurrent initializations
    async with _get_init_lock():
        # Double-check after acquiring lock
        if _global_manager is not None:
            log.debug(f"Manager was initialized while waiting for lock (id={id(_global_manager)})")
            return _global_manager

        # Initialize with provider
        log.info("Calling init_shared_session_manager()...")
        manager = await init_shared_session_manager()
        if manager is None:
            # Multiuser disabled - create basic manager
            log.warning("Multiuser disabled, creating basic manager")
            _global_manager = SharedSessionManager()

        log.info(f"Manager initialized (id={id(_global_manager)})")

        # _global_manager is guaranteed to be set by init_shared_session_manager
        assert _global_manager is not None
        return _global_manager


async def init_shared_session_manager() -> Optional[SharedSessionManager]:
    """Initialize the global SharedSessionManager with configured provider.

    This should be called once at application startup. It reads the
    configuration from environment variables and creates the appropriate
    sync provider.

    Returns:
        The initialized manager, or None if multiuser is disabled

    Example:
        # At application startup
        manager = await init_shared_session_manager()
        if manager:
            print("Multiuser enabled!")
    """
    global _global_manager, _manager_initialized

    if _manager_initialized:
        return _global_manager

    from .config import (
        get_multiuser_config,
        SyncProviderType,
    )

    config = get_multiuser_config()

    if not config.enabled:
        log.info("Multiuser is disabled")
        _manager_initialized = True
        return None

    # Create sync provider if configured
    sync_provider = None
    if config.provider == SyncProviderType.FIREBASE:
        if config.firebase.is_valid():
            try:
                from .providers.firebase import FirebaseSyncProvider

                sync_provider = FirebaseSyncProvider(
                    project_id=config.firebase.project_id,
                    database_url=config.firebase.database_url,
                    credentials_path=config.firebase.credentials_path,
                    api_key=config.firebase.api_key,
                )

                # Connect to Firebase
                connected = await sync_provider.connect()
                if connected:
                    log.info("Connected to Firebase sync provider")
                else:
                    log.warning("Failed to connect to Firebase, falling back to local")
                    sync_provider = None

            except Exception as e:
                log.warning(f"Failed to initialize Firebase provider: {e}")
                sync_provider = None
        else:
            errors = config.firebase.validate()
            log.warning(f"Firebase config invalid: {errors}")

    # Create manager with sync provider
    _global_manager = SharedSessionManager(
        storage_root=config.storage_root,
        sync_provider=sync_provider,
    )

    _manager_initialized = True
    provider_name = "Firebase" if sync_provider else "local"
    log.info(f"Initialized SharedSessionManager with {provider_name} provider")

    return _global_manager


def set_shared_session_manager(manager: SharedSessionManager) -> None:
    """Set the global SharedSessionManager instance."""
    global _global_manager
    _global_manager = manager
