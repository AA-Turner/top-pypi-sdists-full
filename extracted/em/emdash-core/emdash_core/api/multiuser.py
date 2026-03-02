"""API endpoints for multiuser shared sessions.

This module provides REST and SSE endpoints for creating, joining,
and managing shared agent sessions with multiple participants.
"""

import asyncio
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..multiuser import (
    SharedSessionManager,
    get_or_init_manager,
    SharedSession,
    SharedSessionState,
    Participant,
    ParticipantRole,
    SessionNotFoundError,
    InvalidInviteCodeError,
    NotAuthorizedError,
    UserIdentity,
    Team,
    TeamMember,
    TeamRole,
    TeamSessionInfo,
    TeamNotFoundError,
    TeamPermissionError,
)
from ..multiuser.projects import (
    Project,
    ProjectMember,
    ProjectRole,
    Task,
    TaskStatus,
    TaskPriority,
)
from ..multiuser.project_manager import (
    ProjectManager,
    get_project_manager,
    set_project_manager,
)
from ..multiuser.webhooks import get_webhook_registry
from ..sse.stream import SSEHandler, EventType
from ..utils.logger import log

router = APIRouter(prefix="/multiuser", tags=["multiuser"])


# ─────────────────────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────────────────────


class CreateSessionRequest(BaseModel):
    """Request to create a new shared session."""

    user_id: Optional[str] = Field(None, description="User ID (generated if not provided)")
    display_name: str = Field(..., description="Display name for the session owner")
    model: str = Field("", description="LLM model to use")
    plan_mode: bool = Field(False, description="Whether to run in plan mode")


class CreateSessionResponse(BaseModel):
    """Response after creating a session."""

    session_id: str
    invite_code: str
    owner_id: str
    created_at: str
    state: str
    participants: list[dict]
    use_firebase: bool = False  # True if Firebase provider is active (no host:port needed)


class JoinSessionRequest(BaseModel):
    """Request to join a session via invite code."""

    invite_code: str = Field(..., description="The invite code")
    user_id: Optional[str] = Field(None, description="User ID (generated if not provided)")
    display_name: str = Field(..., description="Display name for the joining user")


class JoinSessionResponse(BaseModel):
    """Response after joining a session."""

    session_id: str
    invite_code: str
    state: str
    participants: list[dict]
    message_count: int
    queue_length: int


class SendMessageRequest(BaseModel):
    """Request to send a message in a shared session."""

    user_id: str = Field(..., description="User sending the message")
    content: str = Field(..., description="Message content")
    images: Optional[list[dict]] = Field(None, description="Optional images")
    priority: int = Field(0, description="Message priority (higher = more urgent)")
    trigger_agent: bool = Field(True, description="Whether to trigger agent processing (False for chat-only)")


class SendMessageResponse(BaseModel):
    """Response after sending/queueing a message."""

    message_id: str
    queued_at: str
    queue_position: Optional[int]
    agent_busy: bool


class LeaveSessionRequest(BaseModel):
    """Request to leave a session."""

    user_id: str = Field(..., description="User leaving the session")


class CloseSessionRequest(BaseModel):
    """Request to close a session (owner only)."""

    user_id: str = Field(..., description="User requesting close (must be owner)")


class SessionStateResponse(BaseModel):
    """Response with session state."""

    session_id: str
    invite_code: str
    owner_id: str
    state: str
    participants: list[dict]
    queue_length: int
    agent_busy: bool
    message_count: int


class ParticipantResponse(BaseModel):
    """Response with participant info."""

    user_id: str
    display_name: str
    role: str
    joined_at: str
    last_seen: str
    is_online: bool


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────


@router.post("/session/create", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    """Create a new shared session.

    Returns the session info including an invite code that can be
    shared with other users to join the session.
    """
    manager = await get_or_init_manager()

    # Generate user ID if not provided
    user_id = request.user_id
    if not user_id:
        identity = UserIdentity.from_machine()
        user_id = identity.user_id

    try:
        session, invite_code = await manager.create_session(
            owner_id=user_id,
            display_name=request.display_name,
            model=request.model,
            plan_mode=request.plan_mode,
        )

        return CreateSessionResponse(
            session_id=session.session_id,
            invite_code=invite_code,
            owner_id=session.owner_id,
            created_at=session.created_at,
            state=session.state.value,
            participants=[p.to_dict() for p in session.participants],
            use_firebase=manager.has_sync_provider(),
        )

    except Exception as e:
        log.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/join", response_model=JoinSessionResponse)
async def join_session(request: JoinSessionRequest):
    """Join an existing session via invite code.

    The invite code is case-insensitive and ignores spaces/dashes.
    """
    manager = await get_or_init_manager()

    # Generate user ID if not provided
    user_id = request.user_id
    if not user_id:
        identity = UserIdentity.from_machine()
        user_id = identity.user_id

    try:
        session = await manager.join_session(
            invite_code=request.invite_code,
            user_id=user_id,
            display_name=request.display_name,
        )

        queue_status = manager.get_queue_status(session.session_id)

        return JoinSessionResponse(
            session_id=session.session_id,
            invite_code=session.invite_code,
            state=session.state.value,
            participants=[p.to_dict() for p in session.participants],
            message_count=len(session.messages),
            queue_length=queue_status.get("length", 0),
        )

    except InvalidInviteCodeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        log.error(f"Failed to join session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{session_id}/message", response_model=SendMessageResponse)
async def send_message(session_id: str, request: SendMessageRequest):
    """Send a message in a shared session.

    If trigger_agent is True and the agent is busy processing another message,
    this message will be queued and processed in order.
    If trigger_agent is False, the message is only broadcast to participants (chat-only).
    """
    manager = await get_or_init_manager()

    try:
        # Get session first to get participant info
        session = manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Broadcast the user message immediately so all participants see it right away
        participant = session.get_participant(request.user_id)
        display_name = participant.display_name if participant else "User"
        await manager.broadcast_event(
            session_id,
            "user_message",
            {
                "user_id": request.user_id,
                "content": request.content,
                "display_name": display_name,
            },
            source_user_id=request.user_id,
        )

        # If trigger_agent is False, just return without queueing for agent
        if not request.trigger_agent:
            from datetime import datetime
            return SendMessageResponse(
                message_id=f"chat-{datetime.utcnow().isoformat()}",
                queued_at=datetime.utcnow().isoformat(),
                queue_position=None,
                agent_busy=False,
            )

        # Queue for agent processing
        message = await manager.send_message(
            session_id=session_id,
            user_id=request.user_id,
            content=request.content,
            images=request.images,
            priority=request.priority,
        )

        queue_status = manager.get_queue_status(session_id)

        return SendMessageResponse(
            message_id=message.id,
            queued_at=message.queued_at,
            queue_position=queue_status.get("length", 1) - 1 if queue_status.get("agent_busy") else None,
            agent_busy=queue_status.get("agent_busy", False),
        )

    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        log.error(f"Failed to send message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}/state", response_model=SessionStateResponse)
async def get_session_state(session_id: str):
    """Get current state of a shared session."""
    manager = await get_or_init_manager()

    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    queue_status = manager.get_queue_status(session_id)

    return SessionStateResponse(
        session_id=session.session_id,
        invite_code=session.invite_code,
        owner_id=session.owner_id,
        state=session.state.value,
        participants=[p.to_dict() for p in session.participants],
        queue_length=queue_status.get("length", 0),
        agent_busy=queue_status.get("agent_busy", False),
        message_count=len(session.messages),
    )


@router.get("/session/{session_id}/participants")
async def get_participants(session_id: str) -> list[ParticipantResponse]:
    """Get list of participants in a session."""
    manager = await get_or_init_manager()

    participants = manager.get_session_participants(session_id)
    if not participants:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return [
        ParticipantResponse(
            user_id=p.user_id,
            display_name=p.display_name,
            role=p.role.value,
            joined_at=p.joined_at,
            last_seen=p.last_seen,
            is_online=p.is_online,
        )
        for p in participants
    ]


@router.post("/session/{session_id}/leave")
async def leave_session(session_id: str, request: LeaveSessionRequest):
    """Leave a shared session."""
    manager = await get_or_init_manager()

    try:
        success = await manager.leave_session(session_id, request.user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session or user not found")

        return {"success": True, "message": f"Left session {session_id}"}

    except Exception as e:
        log.error(f"Failed to leave session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/session/{session_id}")
async def close_session(session_id: str, request: CloseSessionRequest):
    """Close a shared session (owner only).

    This removes all participants and cleans up session resources.
    """
    manager = await get_or_init_manager()

    try:
        success = await manager.close_session(session_id, request.user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"success": True, "message": f"Closed session {session_id}"}

    except NotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        log.error(f"Failed to close session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{session_id}/heartbeat")
async def heartbeat(session_id: str, user_id: str = Query(...)):
    """Send a heartbeat to indicate the user is still connected.

    Should be called periodically (e.g., every 30 seconds) to maintain
    online presence status.
    """
    manager = await get_or_init_manager()

    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.update_participant_presence(user_id, is_online=True)

    return {"success": True}


@router.get("/session/{session_id}/stream")
async def stream_session(
    session_id: str,
    user_id: str = Query(..., description="User ID for this connection"),
):
    """Stream session events via Server-Sent Events (SSE).

    This endpoint provides real-time updates for:
    - Agent responses and tool calls
    - Participant joins/leaves
    - Queue status changes
    - State changes

    The stream should be kept open for the duration of the session.
    """
    manager = await get_or_init_manager()

    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Verify user is a participant
    if not session.get_participant(user_id):
        raise HTTPException(status_code=403, detail="User is not a participant")

    # Create SSE handler for this user
    sse_handler = SSEHandler(agent_name="Emdash Multiuser")

    # Register with manager (async to ensure broadcaster is set up)
    await manager.add_sse_handler_async(session_id, user_id, sse_handler)

    # Send initial state
    sse_handler.emit(EventType.SESSION_START, {
        "session_id": session_id,
        "participants": [p.to_dict() for p in session.participants],
        "message_count": len(session.messages),
        "state": session.state.value,
    })

    async def event_generator():
        """Generate SSE events."""
        try:
            async for event in sse_handler:
                yield event
        finally:
            # Cleanup on disconnect
            manager.remove_sse_handler(session_id, user_id)
            log.info(f"SSE stream closed for user {user_id} in session {session_id}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/session/{session_id}/messages")
async def get_messages(
    session_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Get conversation messages from a session.

    Returns messages in chronological order, most recent last.
    """
    manager = await get_or_init_manager()

    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = session.messages[offset : offset + limit]

    return {
        "session_id": session_id,
        "total": len(session.messages),
        "offset": offset,
        "limit": limit,
        "messages": messages,
    }


class ConversationMessageRequest(BaseModel):
    """Request to send a message via the unified conversation endpoint."""

    user_id: str = Field(..., description="User sending the message")
    content: str = Field(..., description="Message content")
    trigger_agent: bool = Field(False, description="Whether this message should trigger agent processing")


@router.post("/conversation/{session_id}/message")
async def conversation_message(session_id: str, request: ConversationMessageRequest):
    """Unified message endpoint for shared sessions.

    This is the single source of truth for message handling in shared mode:
    - ALL participants (including owner) receive events via SSE only
    - No local display, no filtering needed

    Flow:
    1. Broadcasts user_message to all participants via SSE
    2. If trigger_agent:
       - If owner sent the message: returns signal for owner to process locally
       - If joiner sent the message: sends process_message_request to owner via SSE
    """
    import re
    from datetime import datetime

    manager = await get_or_init_manager()

    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Verify user is a participant
    participant = session.get_participant(request.user_id)
    if not participant:
        raise HTTPException(status_code=403, detail="User is not a participant")

    display_name = participant.display_name

    log.info(f"[CONVERSATION] Broadcasting user_message: user_id={request.user_id}, display_name={display_name}, content={request.content[:50]}...")

    # Accumulate every user message in chat_history so the agent
    # can see the full human discussion when invoked via @agent.
    session.chat_history.append({
        "user_id": request.user_id,
        "display_name": display_name,
        "content": request.content,
        "timestamp": datetime.utcnow().isoformat(),
    })

    # 1. Broadcast user message to all participants
    await manager.broadcast_event(
        session_id,
        "user_message",
        {
            "user_id": request.user_id,
            "content": request.content,
            "display_name": display_name,
        },
        source_user_id=request.user_id,
    )

    # 2. Handle agent triggering
    if request.trigger_agent:
        is_owner = session.owner_id == request.user_id

        # Strip @agent/@emdash from content for agent processing
        agent_content = re.sub(r'@agent|@emdash', '', request.content, flags=re.IGNORECASE).strip()
        if not agent_content:
            agent_content = request.content

        # Collect only NEW chat messages since the last @agent invocation.
        # The cursor points to where the agent last consumed, so we slice
        # from there up to (but not including) the current @agent message.
        cursor = session.chat_history_cursor
        chat_context = session.chat_history[cursor:-1][-50:]

        # Advance cursor past the current @agent message so the next
        # invocation won't resend these messages.
        session.chat_history_cursor = len(session.chat_history)

        if is_owner:
            # Owner will process locally - return signal with chat context
            return {
                "status": "process_locally",
                "content": agent_content,
                "chat_context": chat_context,
                "message": "Owner should process this message through their local agent",
            }
        else:
            # Non-owner: send process_message_request to owner via SSE
            await manager.broadcast_event(
                session_id,
                "process_message_request",
                {
                    "user_id": request.user_id,
                    "content": agent_content,
                    "display_name": display_name,
                    "chat_context": chat_context,
                },
                source_user_id=request.user_id,
            )
            return {
                "status": "queued",
                "message": "Message sent to session owner for processing",
            }

    # Chat-only message (no agent trigger)
    return {
        "status": "broadcast",
        "message": "Message broadcast to all participants",
    }


class BroadcastResponseRequest(BaseModel):
    """Request to broadcast an agent response to all participants."""

    user_id: str = Field(..., description="Owner's user ID (must be session owner)")
    original_message_id: Optional[str] = Field(None, description="ID of the message being responded to")
    original_user_id: Optional[str] = Field(None, description="User ID who sent the original message")
    original_content: str = Field(..., description="Original message content")
    response_content: str = Field(..., description="Agent's response content")


class BroadcastEventRequest(BaseModel):
    """Request to broadcast a generic event to all participants."""

    user_id: str = Field(..., description="User sending the event")
    event_type: str = Field(..., description="Event type (e.g., user_typing, tool_start)")
    data: dict = Field(default_factory=dict, description="Event data payload")


@router.post("/session/{session_id}/broadcast_response")
async def broadcast_response(session_id: str, request: BroadcastResponseRequest):
    """Broadcast an agent response to all participants in a shared session.

    This endpoint is used by the session owner's CLI to broadcast responses
    after processing messages locally. The owner processes messages with their
    local agent and uses this endpoint to relay responses to all participants.
    """
    manager = await get_or_init_manager()

    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Verify caller is the owner
    if session.owner_id != request.user_id:
        raise HTTPException(status_code=403, detail="Only session owner can broadcast responses")

    try:
        # Determine who sent the original message
        msg_user_id = request.original_user_id or request.user_id

        # Only broadcast user_message for owner's messages here.
        # Joiner messages are already broadcast immediately via /message endpoint.
        is_owner_message = (request.original_user_id is None or
                           request.original_user_id == request.user_id)

        if is_owner_message:
            participant = session.get_participant(msg_user_id)
            display_name = participant.display_name if participant else "User"
            await manager.broadcast_event(
                session_id,
                "user_message",
                {
                    "user_id": msg_user_id,
                    "content": request.original_content,
                    "display_name": display_name,
                },
                source_user_id=msg_user_id,
            )

        # Broadcast the agent response (no source user - it's from the agent)
        await manager.broadcast_event(
            session_id,
            "assistant_text",
            {
                "text": request.response_content,
                "complete": True,
            },
        )

        # Update session messages
        session.messages.append({"role": "user", "content": request.original_content})
        session.messages.append({"role": "assistant", "content": request.response_content})

        return {"success": True, "message": "Response broadcast to all participants"}

    except Exception as e:
        log.error(f"Failed to broadcast response: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{session_id}/broadcast_event")
async def broadcast_event(session_id: str, request: BroadcastEventRequest):
    """Broadcast a generic event to all participants in a shared session.

    Used for typing indicators, tool events, thinking, etc.
    """
    manager = await get_or_init_manager()

    session = manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Verify user is a participant
    if not session.get_participant(request.user_id):
        raise HTTPException(status_code=403, detail="User is not a participant")

    try:
        # Add user info to event data
        participant = session.get_participant(request.user_id)
        event_data = {
            **request.data,
            "user_id": request.user_id,
            "display_name": participant.display_name if participant else "User",
        }

        await manager.broadcast_event(
            session_id,
            request.event_type,
            event_data,
            source_user_id=request.user_id,  # Pass source user for filtering
        )

        return {"success": True}

    except Exception as e:
        log.error(f"Failed to broadcast event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/by-invite/{invite_code}")
async def get_session_by_invite(invite_code: str):
    """Look up session info by invite code (without joining).

    Useful for previewing a session before joining.
    """
    manager = await get_or_init_manager()

    session = manager.get_session_by_invite(invite_code)
    if not session:
        raise HTTPException(status_code=404, detail="Invalid invite code")

    return {
        "session_id": session.session_id,
        "owner_id": session.owner_id,
        "created_at": session.created_at,
        "state": session.state.value,
        "participant_count": len(session.participants),
        "message_count": len(session.messages),
    }


@router.get("/sessions")
async def list_user_sessions(user_id: str = Query(...)):
    """List all sessions a user is participating in."""
    manager = await get_or_init_manager()

    sessions = manager.get_user_sessions(user_id)

    return {
        "user_id": user_id,
        "sessions": [
            {
                "session_id": s.session_id,
                "invite_code": s.invite_code,
                "owner_id": s.owner_id,
                "state": s.state.value,
                "participant_count": len(s.participants),
                "created_at": s.created_at,
                "is_owner": s.owner_id == user_id,
            }
            for s in sessions
        ],
    }


# ─────────────────────────────────────────────────────────────
# Share Request/Response Models
# ─────────────────────────────────────────────────────────────


class ShareRequest(BaseModel):
    """Request to create a shareable session."""

    user_id: str = Field(..., description="User creating the share")
    display_name: str = Field(..., description="Display name for the session owner")
    board_id: Optional[str] = Field(None, description="Link to a board")
    project_id: Optional[str] = Field(None, description="Link to a project")
    expires_hours: int = Field(24, description="Invite expiry in hours")


class ShareResponse(BaseModel):
    """Response with share information."""

    session_id: str
    invite_code: str
    share_url: str  # emdash://join/{invite_code}
    expires_at: str
    created_at: str
    owner_id: str


# ─────────────────────────────────────────────────────────────
# Share Endpoints
# ─────────────────────────────────────────────────────────────


@router.post("/share", response_model=ShareResponse)
async def create_share(request: ShareRequest):
    """Create a shareable link for collaboration.

    This is a convenience endpoint that:
    1. Creates a new shared session
    2. Links it to a board/project if provided
    3. Generates an invite code with configurable expiry
    4. Returns a deep link URL for joining

    The share_url can be used to join the session via the desktop app
    using the emdash:// protocol handler.
    """
    from datetime import datetime, timedelta

    manager = await get_or_init_manager()

    try:
        # Create a new session
        session, invite_code = await manager.create_session(
            owner_id=request.user_id,
            display_name=request.display_name,
            model="",  # Use default model
            plan_mode=False,
        )

        # Calculate expiry
        expires_at = datetime.utcnow() + timedelta(hours=request.expires_hours)

        # Store metadata about the share (board_id, project_id)
        if request.board_id or request.project_id:
            # Store in session metadata (could be extended later)
            session.metadata = {
                "board_id": request.board_id,
                "project_id": request.project_id,
                "expires_at": expires_at.isoformat(),
            }

        # Generate deep link URL
        share_url = f"emdash://join/{invite_code}"

        return ShareResponse(
            session_id=session.session_id,
            invite_code=invite_code,
            share_url=share_url,
            expires_at=expires_at.isoformat(),
            created_at=session.created_at,
            owner_id=session.owner_id,
        )

    except Exception as e:
        log.error(f"Failed to create share: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Team Request/Response Models
# ─────────────────────────────────────────────────────────────


class CreateTeamRequest(BaseModel):
    """Request to create a new team."""

    name: str = Field(..., description="Team name")
    user_id: str = Field(..., description="Creator's user ID")
    display_name: str = Field(..., description="Creator's display name")
    description: str = Field("", description="Optional team description")


class CreateTeamResponse(BaseModel):
    """Response after creating a team."""

    team_id: str
    name: str
    invite_code: str
    created_at: str
    member_count: int


class JoinTeamRequest(BaseModel):
    """Request to join a team."""

    invite_code: str = Field(..., description="Team invite code")
    user_id: str = Field(..., description="Joining user's ID")
    display_name: str = Field(..., description="Joining user's display name")


class JoinTeamResponse(BaseModel):
    """Response after joining a team."""

    team_id: str
    name: str
    member_count: int
    your_role: str


class LeaveTeamRequest(BaseModel):
    """Request to leave a team."""

    user_id: str = Field(..., description="User leaving the team")


class AddSessionToTeamRequest(BaseModel):
    """Request to add a session to a team."""

    session_id: str = Field(..., description="Session to add")
    user_id: str = Field(..., description="User adding the session")
    title: Optional[str] = Field(None, description="Optional title for the session")


class JoinTeamSessionRequest(BaseModel):
    """Request to join a team session."""

    session_id: str = Field(..., description="Session to join")
    user_id: str = Field(..., description="User joining")
    display_name: str = Field(..., description="User's display name")


# ─────────────────────────────────────────────────────────────
# Team Endpoints
# ─────────────────────────────────────────────────────────────


@router.post("/team/create", response_model=CreateTeamResponse)
async def create_team(request: CreateTeamRequest):
    """Create a new team.

    The creating user becomes an admin of the team.
    Returns an invite code that can be shared with others to join.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.create_team(
            name=request.name,
            user_id=request.user_id,
            display_name=request.display_name,
            description=request.description,
        )

        return CreateTeamResponse(
            team_id=team.team_id,
            name=team.name,
            invite_code=team.invite_code,
            created_at=team.created_at,
            member_count=len(team.members),
        )

    except Exception as e:
        log.error(f"Failed to create team: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/join", response_model=JoinTeamResponse)
async def join_team(request: JoinTeamRequest):
    """Join a team using invite code.

    Team invite codes start with 'T-' prefix.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.join_team(
            invite_code=request.invite_code,
            user_id=request.user_id,
            display_name=request.display_name,
        )

        member = team.get_member(request.user_id)
        your_role = member.role.value if member else "member"

        return JoinTeamResponse(
            team_id=team.team_id,
            name=team.name,
            member_count=len(team.members),
            your_role=your_role,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        log.error(f"Failed to join team: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}")
async def get_team(team_id: str, user_id: str = Query(...)):
    """Get team information.

    Only team members can view team details.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        # Check membership
        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        member = team.get_member(user_id)
        your_role = member.role.value if member else "member"

        # Get session count
        team_sessions = await manager.list_team_sessions(team_id, user_id)

        return {
            "team_id": team.team_id,
            "name": team.name,
            "description": team.description,
            "invite_code": team.invite_code,
            "created_at": team.created_at,
            "created_by": team.created_by,
            "members": [m.to_dict() for m in team.members],
            "session_count": len(team_sessions),
            "your_role": your_role,
        }

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get team: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/leave")
async def leave_team(team_id: str, request: LeaveTeamRequest):
    """Leave a team."""
    manager = await get_or_init_manager()

    try:
        success = await manager.leave_team(team_id, request.user_id)
        if not success:
            raise HTTPException(status_code=400, detail="Could not leave team")

        return {"success": True}

    except Exception as e:
        log.error(f"Failed to leave team: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams")
async def list_user_teams(user_id: str = Query(...)):
    """List all teams a user is a member of."""
    manager = await get_or_init_manager()

    try:
        teams = await manager.get_user_teams(user_id)

        return [
            {
                "team_id": t.team_id,
                "name": t.name,
                "invite_code": t.invite_code,
                "member_count": len(t.members),
                "your_role": t.get_member(user_id).role.value if t.get_member(user_id) else "member",
            }
            for t in teams
        ]

    except Exception as e:
        log.error(f"Failed to list teams: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}/sessions")
async def list_team_sessions(team_id: str, user_id: str = Query(...)):
    """List all sessions in a team.

    Only team members can view team sessions.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        sessions = await manager.list_team_sessions(team_id, user_id)

        return {
            "team_id": team_id,
            "team_name": team.name,
            "sessions": [s.to_dict() for s in sessions],
        }

    except HTTPException:
        raise
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        log.error(f"Failed to list team sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/add-session")
async def add_session_to_team(team_id: str, request: AddSessionToTeamRequest):
    """Add a session to a team.

    The user must be the session owner or a team admin.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        success = await manager.add_session_to_team(
            team_id=team_id,
            session_id=request.session_id,
            user_id=request.user_id,
            title=request.title,
        )

        return {
            "success": success,
            "team_name": team.name,
        }

    except TeamNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TeamPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        log.error(f"Failed to add session to team: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/join-session")
async def join_team_session(team_id: str, request: JoinTeamSessionRequest):
    """Join a session as a team member.

    Team members can join any team session without needing an invite code.
    """
    manager = await get_or_init_manager()

    try:
        session = await manager.join_team_session(
            team_id=team_id,
            session_id=request.session_id,
            user_id=request.user_id,
            display_name=request.display_name,
        )

        return {
            "session_id": session.session_id,
            "title": session.title,
            "participants": [p.to_dict() for p in session.participants],
            "message_count": len(session.messages),
            "state": session.state.value,
        }

    except TeamNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TeamPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        log.error(f"Failed to join team session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Registry Request/Response Models
# ─────────────────────────────────────────────────────────────


class AddRuleRequest(BaseModel):
    """Request to add a rule to team registry."""

    user_id: str = Field(..., description="User adding the rule (must be admin)")
    name: str = Field(..., description="Rule name")
    content: str = Field(..., description="Rule content (prompt text)")
    description: str = Field("", description="Optional description")
    priority: int = Field(0, description="Rule priority (higher = applied first)")
    tags: list[str] = Field(default_factory=list, description="Optional tags")


class AddAgentRequest(BaseModel):
    """Request to add an agent config to team registry."""

    user_id: str = Field(..., description="User adding the agent (must be admin)")
    name: str = Field(..., description="Agent name")
    description: str = Field("", description="Optional description")
    model: str = Field("", description="LLM model identifier")
    system_prompt: str = Field("", description="Custom system prompt")
    tools: list[str] = Field(default_factory=list, description="Enabled tool names")
    settings: dict = Field(default_factory=dict, description="Additional settings")


class AddMCPRequest(BaseModel):
    """Request to add an MCP config to team registry."""

    user_id: str = Field(..., description="User adding the MCP (must be admin)")
    name: str = Field(..., description="MCP name")
    description: str = Field("", description="Optional description")
    command: str = Field(..., description="Command to launch MCP server")
    args: list[str] = Field(default_factory=list, description="Command arguments")
    env: dict = Field(default_factory=dict, description="Environment variables")
    auto_start: bool = Field(False, description="Auto-start with sessions")


class AddSkillRequest(BaseModel):
    """Request to add a skill to team registry."""

    user_id: str = Field(..., description="User adding the skill (must be admin)")
    name: str = Field(..., description="Skill name")
    description: str = Field("", description="Optional description")
    prompt_template: str = Field(..., description="Prompt template with {{var}} placeholders")
    tags: list[str] = Field(default_factory=list, description="Optional tags")


class SyncRegistryRequest(BaseModel):
    """Request to sync registry."""

    user_id: str = Field(..., description="User requesting sync")
    strategy: str = Field("remote_wins", description="Conflict strategy: remote_wins, local_wins, merge")


class ImportRegistryRequest(BaseModel):
    """Request to import registry data."""

    user_id: str = Field(..., description="User importing (must be admin)")
    registry: dict = Field(..., description="Registry data to import")
    merge: bool = Field(True, description="Whether to merge with existing")


# ─────────────────────────────────────────────────────────────
# Registry Endpoints
# ─────────────────────────────────────────────────────────────


@router.get("/team/{team_id}/registry")
async def get_team_registry(team_id: str, user_id: str = Query(...)):
    """Get the full team registry.

    Only team members can access the registry.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        return registry.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get registry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Rules Endpoints
# ─────────────────────────────────────────────────────────────


@router.get("/team/{team_id}/registry/rules")
async def list_registry_rules(team_id: str, user_id: str = Query(...)):
    """List all rules in the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        return [r.to_dict() for r in registry.rules]

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to list rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}/registry/rules/{rule_name}")
async def get_registry_rule(team_id: str, rule_name: str, user_id: str = Query(...)):
    """Get a specific rule by name or ID."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        # Try by name first, then by ID
        rule = registry.get_rule_by_name(rule_name)
        if not rule:
            rule = registry.get_rule(rule_name)

        if not rule:
            raise HTTPException(status_code=404, detail=f"Rule '{rule_name}' not found")

        return rule.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/registry/rules")
async def add_registry_rule(team_id: str, request: AddRuleRequest):
    """Add a rule to the team registry.

    Only team admins can add rules.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(request.user_id):
            raise HTTPException(status_code=403, detail="Only admins can add rules")

        from ..multiuser.registry import Rule

        rule = Rule(
            rule_id="",  # Will be auto-generated
            name=request.name,
            content=request.content,
            description=request.description,
            priority=request.priority,
            tags=request.tags,
            created_by=request.user_id,
        )

        registry = await manager.get_team_registry(team_id, request.user_id)
        registry.add_rule(rule)
        await manager.save_team_registry(registry, request.user_id)

        return rule.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to add rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/team/{team_id}/registry/rules/{rule_id}")
async def remove_registry_rule(team_id: str, rule_id: str, user_id: str = Query(...)):
    """Remove a rule from the team registry.

    Only team admins can remove rules.
    """
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(user_id):
            raise HTTPException(status_code=403, detail="Only admins can remove rules")

        registry = await manager.get_team_registry(team_id, user_id)

        # Try to find and remove by name or ID
        rule = registry.get_rule_by_name(rule_id)
        target_id = rule.rule_id if rule else rule_id

        if not registry.remove_rule(target_id):
            raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found")

        await manager.save_team_registry(registry, user_id)

        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to remove rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Agents Endpoints
# ─────────────────────────────────────────────────────────────


@router.get("/team/{team_id}/registry/agents")
async def list_registry_agents(team_id: str, user_id: str = Query(...)):
    """List all agent configs in the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        return [a.to_dict() for a in registry.agents]

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}/registry/agents/{agent_name}")
async def get_registry_agent(team_id: str, agent_name: str, user_id: str = Query(...)):
    """Get a specific agent config by name or ID."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        agent = registry.get_agent_by_name(agent_name)
        if not agent:
            agent = registry.get_agent(agent_name)

        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

        return agent.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/registry/agents")
async def add_registry_agent(team_id: str, request: AddAgentRequest):
    """Add an agent config to the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(request.user_id):
            raise HTTPException(status_code=403, detail="Only admins can add agents")

        from ..multiuser.registry import AgentConfig

        agent = AgentConfig(
            agent_id="",
            name=request.name,
            description=request.description,
            model=request.model,
            system_prompt=request.system_prompt,
            tools=request.tools,
            settings=request.settings,
            created_by=request.user_id,
        )

        registry = await manager.get_team_registry(team_id, request.user_id)
        registry.add_agent(agent)
        await manager.save_team_registry(registry, request.user_id)

        return agent.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to add agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/team/{team_id}/registry/agents/{agent_id}")
async def remove_registry_agent(team_id: str, agent_id: str, user_id: str = Query(...)):
    """Remove an agent config from the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(user_id):
            raise HTTPException(status_code=403, detail="Only admins can remove agents")

        registry = await manager.get_team_registry(team_id, user_id)

        agent = registry.get_agent_by_name(agent_id)
        target_id = agent.agent_id if agent else agent_id

        if not registry.remove_agent(target_id):
            raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")

        await manager.save_team_registry(registry, user_id)

        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to remove agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# MCPs Endpoints
# ─────────────────────────────────────────────────────────────


@router.get("/team/{team_id}/registry/mcps")
async def list_registry_mcps(team_id: str, user_id: str = Query(...)):
    """List all MCP configs in the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        return [m.to_dict() for m in registry.mcps]

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to list MCPs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}/registry/mcps/{mcp_name}")
async def get_registry_mcp(team_id: str, mcp_name: str, user_id: str = Query(...)):
    """Get a specific MCP config by name or ID."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        mcp = registry.get_mcp_by_name(mcp_name)
        if not mcp:
            mcp = registry.get_mcp(mcp_name)

        if not mcp:
            raise HTTPException(status_code=404, detail=f"MCP '{mcp_name}' not found")

        return mcp.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/registry/mcps")
async def add_registry_mcp(team_id: str, request: AddMCPRequest):
    """Add an MCP config to the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(request.user_id):
            raise HTTPException(status_code=403, detail="Only admins can add MCPs")

        from ..multiuser.registry import MCPConfig

        mcp = MCPConfig(
            mcp_id="",
            name=request.name,
            description=request.description,
            command=request.command,
            args=request.args,
            env=request.env,
            auto_start=request.auto_start,
            created_by=request.user_id,
        )

        registry = await manager.get_team_registry(team_id, request.user_id)
        registry.add_mcp(mcp)
        await manager.save_team_registry(registry, request.user_id)

        return mcp.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to add MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/team/{team_id}/registry/mcps/{mcp_id}")
async def remove_registry_mcp(team_id: str, mcp_id: str, user_id: str = Query(...)):
    """Remove an MCP config from the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(user_id):
            raise HTTPException(status_code=403, detail="Only admins can remove MCPs")

        registry = await manager.get_team_registry(team_id, user_id)

        mcp = registry.get_mcp_by_name(mcp_id)
        target_id = mcp.mcp_id if mcp else mcp_id

        if not registry.remove_mcp(target_id):
            raise HTTPException(status_code=404, detail=f"MCP '{mcp_id}' not found")

        await manager.save_team_registry(registry, user_id)

        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to remove MCP: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Skills Endpoints
# ─────────────────────────────────────────────────────────────


@router.get("/team/{team_id}/registry/skills")
async def list_registry_skills(team_id: str, user_id: str = Query(...)):
    """List all skills in the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        return [s.to_dict() for s in registry.skills]

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to list skills: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}/registry/skills/{skill_name}")
async def get_registry_skill(team_id: str, skill_name: str, user_id: str = Query(...)):
    """Get a specific skill by name or ID."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.get_team_registry(team_id, user_id)

        skill = registry.get_skill_by_name(skill_name)
        if not skill:
            skill = registry.get_skill(skill_name)

        if not skill:
            raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")

        return skill.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get skill: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/registry/skills")
async def add_registry_skill(team_id: str, request: AddSkillRequest):
    """Add a skill to the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(request.user_id):
            raise HTTPException(status_code=403, detail="Only admins can add skills")

        from ..multiuser.registry import Skill

        skill = Skill(
            skill_id="",
            name=request.name,
            description=request.description,
            prompt_template=request.prompt_template,
            tags=request.tags,
            created_by=request.user_id,
        )

        registry = await manager.get_team_registry(team_id, request.user_id)
        registry.add_skill(skill)
        await manager.save_team_registry(registry, request.user_id)

        return skill.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to add skill: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/team/{team_id}/registry/skills/{skill_id}")
async def remove_registry_skill(team_id: str, skill_id: str, user_id: str = Query(...)):
    """Remove a skill from the team registry."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(user_id):
            raise HTTPException(status_code=403, detail="Only admins can remove skills")

        registry = await manager.get_team_registry(team_id, user_id)

        skill = registry.get_skill_by_name(skill_id)
        target_id = skill.skill_id if skill else skill_id

        if not registry.remove_skill(target_id):
            raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")

        await manager.save_team_registry(registry, user_id)

        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to remove skill: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Registry Sync/Import/Export
# ─────────────────────────────────────────────────────────────


@router.post("/team/{team_id}/registry/sync")
async def sync_team_registry(team_id: str, request: SyncRegistryRequest):
    """Sync team registry between local and remote storage."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_member(request.user_id):
            raise HTTPException(status_code=403, detail="Not a team member")

        registry = await manager.sync_team_registry(
            team_id, request.user_id, request.strategy
        )

        return {
            "success": True,
            "rules_count": len(registry.rules),
            "agents_count": len(registry.agents),
            "mcps_count": len(registry.mcps),
            "skills_count": len(registry.skills),
            "version": registry.version,
        }

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to sync registry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/{team_id}/registry/import")
async def import_team_registry(team_id: str, request: ImportRegistryRequest):
    """Import registry data from JSON."""
    manager = await get_or_init_manager()

    try:
        team = await manager.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        if not team.is_admin(request.user_id):
            raise HTTPException(status_code=403, detail="Only admins can import registry")

        from ..multiuser.registry import TeamRegistry

        imported = TeamRegistry.from_dict({"team_id": team_id, **request.registry})

        if request.merge:
            existing = await manager.get_team_registry(team_id, request.user_id)
            # Merge logic - add items that don't exist
            for rule in imported.rules:
                if not existing.get_rule_by_name(rule.name):
                    existing.add_rule(rule)
            for agent in imported.agents:
                if not existing.get_agent_by_name(agent.name):
                    existing.add_agent(agent)
            for mcp in imported.mcps:
                if not existing.get_mcp_by_name(mcp.name):
                    existing.add_mcp(mcp)
            for skill in imported.skills:
                if not existing.get_skill_by_name(skill.name):
                    existing.add_skill(skill)
            registry = existing
        else:
            registry = imported

        await manager.save_team_registry(registry, request.user_id)

        return {
            "success": True,
            "rules_count": len(registry.rules),
            "agents_count": len(registry.agents),
            "mcps_count": len(registry.mcps),
            "skills_count": len(registry.skills),
        }

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to import registry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Webhooks
# ─────────────────────────────────────────────────────────────


class RegisterWebhookRequest(BaseModel):
    """Register a webhook to receive project/task events."""

    url: str = Field(..., description="HTTP endpoint to POST events to")
    events: list[str] = Field(
        ...,
        description=(
            "Event glob patterns to subscribe to. "
            'Examples: ["project.*"], ["task.assigned", "task.status_changed"], ["*"]'
        ),
    )
    secret: Optional[str] = Field(None, description="Shared secret for X-Webhook-Secret header")


@router.post("/webhooks/register")
async def register_webhook(request: RegisterWebhookRequest):
    """Register a webhook to receive project/task mutation events.

    Core holds in-memory state and fires webhooks on every mutation.
    The consumer receives these events and persists to whatever
    backend they choose (Firebase, SQLite, etc.).

    Events fired:
        project.created, project.updated, project.deleted
        project.member_added, project.member_removed
        task.created, task.updated, task.deleted
        task.assigned, task.unassigned, task.status_changed
        task.commented, task.session_linked

    Webhook payload format:
        {
            "event_id": "uuid",
            "event": "task.assigned",
            "data": { ... full object dict ... },
            "timestamp": "ISO-8601"
        }
    """
    registry = get_webhook_registry()
    hook_id = registry.register(
        url=request.url,
        events=request.events,
        secret=request.secret,
    )
    log.info(f"Registered webhook {hook_id} → {request.url}")
    return {"hook_id": hook_id, "url": request.url, "events": request.events}


@router.delete("/webhooks/{hook_id}")
async def unregister_webhook(hook_id: str):
    """Unregister a webhook."""
    registry = get_webhook_registry()
    if not registry.unregister(hook_id):
        raise HTTPException(status_code=404, detail="Webhook not found")
    return {"status": "unregistered", "hook_id": hook_id}


@router.get("/webhooks")
async def list_webhooks():
    """List all registered webhooks."""
    registry = get_webhook_registry()
    return {"webhooks": registry.list_hooks()}


# ─────────────────────────────────────────────────────────────
# Sync (consumer pushes initial state)
# ─────────────────────────────────────────────────────────────


class SyncProjectsRequest(BaseModel):
    """Push projects from consumer's durable store into core's memory."""

    projects: list[dict] = Field(..., description="List of project dicts")


class SyncTasksRequest(BaseModel):
    """Push tasks from consumer's durable store into core's memory."""

    tasks: list[dict] = Field(..., description="List of task dicts")


@router.post("/sync/projects")
async def sync_projects(request: SyncProjectsRequest):
    """Sync projects from consumer's store into core's in-memory state.

    Call this at startup after registering webhooks. Core needs
    initial data to serve reads from. The consumer loads from
    their durable store (Firebase, etc.) and pushes here.
    """
    pm = get_project_manager()
    count = pm.sync_projects(request.projects)
    return {"synced": count}


@router.post("/sync/tasks")
async def sync_tasks(request: SyncTasksRequest):
    """Sync tasks from consumer's store into core's in-memory state.

    Call this at startup after registering webhooks and syncing projects.
    """
    pm = get_project_manager()
    count = pm.sync_tasks(request.tasks)
    return {"synced": count}


class SyncSessionsRequest(BaseModel):
    """Push sessions from consumer's durable store into core's memory."""

    sessions: list[dict] = Field(..., description="List of session dicts")


class SyncTeamsRequest(BaseModel):
    """Push teams from consumer's durable store into core's memory."""

    teams: list[dict] = Field(..., description="List of team dicts")


class SyncRegistriesRequest(BaseModel):
    """Push registries from consumer's durable store into core's memory."""

    registries: list[dict] = Field(
        ..., description="List of registry dicts (each must include team_id)"
    )


@router.post("/sync/sessions")
async def sync_sessions(request: SyncSessionsRequest):
    """Sync sessions from consumer's store into core's in-memory state.

    Call this at startup after registering webhooks. Restores sessions
    so core can serve reads and manage participants.
    """
    manager = await get_or_init_manager()
    count = manager.sync_sessions(request.sessions)
    return {"synced": count}


@router.post("/sync/teams")
async def sync_teams(request: SyncTeamsRequest):
    """Sync teams from consumer's store into core's in-memory state.

    Call this at startup after registering webhooks. Restores teams
    so core can manage membership and team sessions.
    """
    manager = await get_or_init_manager()
    tm = manager.get_team_manager()
    count = tm.sync_teams(request.teams)
    return {"synced": count}


@router.post("/sync/registries")
async def sync_registries(request: SyncRegistriesRequest):
    """Sync team registries from consumer's store into core's memory.

    Each registry dict must include a 'team_id' field.
    """
    manager = await get_or_init_manager()
    tm = manager.get_team_manager()
    count = 0
    for reg_data in request.registries:
        team_id = reg_data.get("team_id")
        if team_id:
            try:
                await tm.registry_manager.load_registry_data(team_id, reg_data)
                count += 1
            except Exception as e:
                log.warning(f"Failed to sync registry for team {team_id}: {e}")
    return {"synced": count}


# ─────────────────────────────────────────────────────────────
# Project Request/Response Models
# ─────────────────────────────────────────────────────────────


class CreateProjectRequest(BaseModel):
    """Request to create a new project."""

    name: str = Field(..., description="Project name")
    user_id: str = Field(..., description="Creator's user ID")
    display_name: str = Field(..., description="Creator's display name")
    description: str = Field("", description="Optional project description")
    repo_links: list[str] = Field(default_factory=list, description="Repository links")


class CreateProjectResponse(BaseModel):
    """Response after creating a project."""

    project_id: str
    name: str
    created_at: str
    member_count: int


class UpdateProjectRequest(BaseModel):
    """Request to update a project."""

    name: Optional[str] = None
    description: Optional[str] = None
    repo_links: Optional[list[str]] = None
    settings: Optional[dict] = None


class AddProjectMemberRequest(BaseModel):
    """Request to add a member to a project."""

    user_id: str = Field(..., description="User to add")
    display_name: str = Field(..., description="User's display name")
    role: str = Field("contributor", description="Project role: lead, contributor, observer")


class CreateTaskRequest(BaseModel):
    """Request to create a task."""

    title: str = Field(..., description="Task title")
    reporter_id: str = Field(..., description="Reporter's user ID")
    reporter_name: str = Field(..., description="Reporter's display name")
    description: str = Field("", description="Task description")
    priority: str = Field("medium", description="Priority: low, medium, high, critical")
    assignee_id: Optional[str] = Field(None, description="Assignee's user ID")
    assignee_name: Optional[str] = Field(None, description="Assignee's display name")
    due_date: Optional[str] = Field(None, description="Due date (ISO format)")
    labels: list[str] = Field(default_factory=list, description="Labels/tags")
    linked_session_id: Optional[str] = Field(None, description="Linked agent session ID")


class CreateTaskResponse(BaseModel):
    """Response after creating a task."""

    task_id: str
    project_id: str
    title: str
    status: str
    priority: str
    assignee_id: Optional[str]
    created_at: str


class UpdateTaskRequest(BaseModel):
    """Request to update a task."""

    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    labels: Optional[list[str]] = None
    linked_session_id: Optional[str] = None


class AssignTaskRequest(BaseModel):
    """Request to assign a task."""

    assignee_id: str = Field(..., description="User to assign")
    assignee_name: str = Field(..., description="Assignee's display name")


class TransitionTaskRequest(BaseModel):
    """Request to transition a task's status."""

    status: str = Field(..., description="New status: open, in_progress, in_review, done, cancelled")


class AddTaskCommentRequest(BaseModel):
    """Request to add a comment to a task."""

    user_id: str = Field(..., description="Commenter's user ID")
    display_name: str = Field(..., description="Commenter's display name")
    content: str = Field(..., description="Comment content")


class LinkTaskSessionRequest(BaseModel):
    """Request to link a session to a task."""

    session_id: str = Field(..., description="Session to link")
    invite_code: Optional[str] = Field(None, description="Full invite code with port for joining")


class LinkSessionToProjectRequest(BaseModel):
    """Request to link a session to a project (and optionally a task)."""

    session_id: str = Field(..., description="Session to link")
    task_id: Optional[str] = Field(None, description="Optional task to link to")
    invite_code: Optional[str] = Field(None, description="Invite code for joining the session")


# ─────────────────────────────────────────────────────────────
# Project Endpoints
# ─────────────────────────────────────────────────────────────


@router.post("/project/create", response_model=CreateProjectResponse)
async def create_project(request: CreateProjectRequest):
    """Create a new project.

    The creator becomes the project lead.
    """
    pm = get_project_manager()

    try:
        project = await pm.create_project(
            name=request.name,
            creator_id=request.user_id,
            creator_name=request.display_name,
            description=request.description,
            repo_links=request.repo_links,
        )

        return CreateProjectResponse(
            project_id=project.project_id,
            name=project.name,
            created_at=project.created_at,
            member_count=len(project.members),
        )

    except Exception as e:
        log.error(f"Failed to create project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project/{project_id}")
async def get_project(project_id: str):
    """Get project details."""
    pm = get_project_manager()

    project = await pm.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project.to_dict()


@router.patch("/project/{project_id}")
async def update_project(project_id: str, request: UpdateProjectRequest):
    """Update project fields."""
    pm = get_project_manager()

    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    project = await pm.update_project(project_id, updates)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project.to_dict()


@router.delete("/project/{project_id}")
async def delete_project(project_id: str, user_id: str = Query(...)):
    """Delete a project and all its tasks (lead only)."""
    pm = get_project_manager()

    try:
        success = await pm.delete_project(project_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"success": True}

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        log.error(f"Failed to delete project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects")
async def list_projects():
    """List all projects."""
    pm = get_project_manager()

    projects = await pm.list_projects()
    return {
        "projects": [p.to_dict() for p in projects],
    }


@router.get("/team/{team_id}/projects")
async def list_team_projects(team_id: str):
    """List all projects (kept for backward compat, ignores team_id)."""
    pm = get_project_manager()

    projects = await pm.list_projects()
    return {
        "projects": [p.to_dict() for p in projects],
    }


@router.post("/project/{project_id}/members")
async def add_project_member(project_id: str, request: AddProjectMemberRequest):
    """Add a member to a project."""
    pm = get_project_manager()

    try:
        role = ProjectRole(request.role)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role: {request.role}")

    member = await pm.add_project_member(
        project_id, request.user_id, request.display_name, role
    )
    if not member:
        raise HTTPException(status_code=404, detail="Project not found")

    return member.to_dict()


@router.delete("/project/{project_id}/members/{user_id}")
async def remove_project_member(project_id: str, user_id: str):
    """Remove a member from a project."""
    pm = get_project_manager()

    success = await pm.remove_project_member(project_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project or member not found")

    return {"success": True}


# ─────────────────────────────────────────────────────────────
# Task Endpoints
# ─────────────────────────────────────────────────────────────


@router.post("/project/{project_id}/tasks", response_model=CreateTaskResponse)
async def create_task(project_id: str, request: CreateTaskRequest):
    """Create a new task in a project."""
    pm = get_project_manager()

    try:
        priority = TaskPriority(request.priority)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid priority: {request.priority}")

    task = await pm.create_task(
        project_id=project_id,
        title=request.title,
        reporter_id=request.reporter_id,
        reporter_name=request.reporter_name,
        description=request.description,
        priority=priority,
        assignee_id=request.assignee_id,
        assignee_name=request.assignee_name,
        due_date=request.due_date,
        labels=request.labels,
        linked_session_id=request.linked_session_id,
    )

    return CreateTaskResponse(
        task_id=task.task_id,
        project_id=task.project_id,
        title=task.title,
        status=task.status.value,
        priority=task.priority.value,
        assignee_id=task.assignee_id,
        created_at=task.created_at,
    )


@router.get("/project/{project_id}/tasks")
async def list_project_tasks(
    project_id: str,
    status: Optional[str] = Query(None, description="Filter by status"),
    assignee_id: Optional[str] = Query(None, description="Filter by assignee"),
):
    """List tasks in a project with optional filters."""
    pm = get_project_manager()

    task_status = None
    if status:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    tasks = await pm.list_project_tasks(project_id, status=task_status, assignee_id=assignee_id)

    return {
        "project_id": project_id,
        "tasks": [t.to_dict() for t in tasks],
        "total": len(tasks),
    }


@router.get("/task/{task_id}")
async def get_task(task_id: str):
    """Get a task by ID."""
    pm = get_project_manager()

    task = await pm.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.to_dict()


@router.patch("/task/{task_id}")
async def update_task(task_id: str, request: UpdateTaskRequest):
    """Update task fields."""
    pm = get_project_manager()

    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    task = await pm.update_task(task_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.to_dict()


@router.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    pm = get_project_manager()

    success = await pm.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"success": True}


@router.post("/task/{task_id}/assign")
async def assign_task(task_id: str, request: AssignTaskRequest):
    """Assign a task to a user."""
    pm = get_project_manager()

    task = await pm.assign_task(task_id, request.assignee_id, request.assignee_name)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.to_dict()


@router.post("/task/{task_id}/unassign")
async def unassign_task(task_id: str):
    """Remove the assignee from a task."""
    pm = get_project_manager()

    task = await pm.unassign_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.to_dict()


@router.post("/task/{task_id}/transition")
async def transition_task(task_id: str, request: TransitionTaskRequest):
    """Transition a task to a new status."""
    pm = get_project_manager()

    try:
        new_status = TaskStatus(request.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {request.status}")

    task = await pm.transition_task(task_id, new_status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.to_dict()


@router.post("/task/{task_id}/comment")
async def add_task_comment(task_id: str, request: AddTaskCommentRequest):
    """Add a comment to a task."""
    pm = get_project_manager()

    comment = await pm.add_task_comment(
        task_id, request.user_id, request.display_name, request.content
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Task not found")

    return comment.to_dict()


@router.post("/task/{task_id}/link-session")
async def link_task_session(task_id: str, request: LinkTaskSessionRequest):
    """Link an agent session to a task.

    Also links the session to the task's project so it appears in project sessions.
    """
    pm = get_project_manager()

    # Get the task to find its project_id
    task = await pm.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Link session to the project (so it shows up in get_project_sessions)
    manager = await get_or_init_manager()
    await manager.link_session_to_project(
        session_id=request.session_id,
        project_id=task.project_id,
        task_id=task_id,
        invite_code=request.invite_code,
    )

    # Also link on the task side
    updated_task = await pm.link_task_to_session(task_id, request.session_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task.to_dict()


@router.get("/user/{user_id}/tasks")
async def get_user_tasks(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter by status"),
):
    """Get all tasks assigned to a user across all projects."""
    pm = get_project_manager()

    task_status = None
    if status:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    tasks = await pm.get_user_tasks(user_id, status=task_status)

    return {
        "user_id": user_id,
        "tasks": [t.to_dict() for t in tasks],
        "total": len(tasks),
    }


# ─────────────────────────────────────────────────────────────
# Session-Project Linking
# ─────────────────────────────────────────────────────────────


@router.post("/project/{project_id}/link-session")
async def link_session_to_project(project_id: str, request: LinkSessionToProjectRequest):
    """Link a multiuser session to a project (and optionally a task)."""
    pm = get_project_manager()

    # Verify project exists
    project = await pm.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Verify task belongs to project if specified
    if request.task_id:
        task = await pm.get_task(request.task_id)
        if not task or task.project_id != project_id:
            raise HTTPException(status_code=404, detail="Task not found in this project")

    # Link session to project (with invite_code for joining)
    manager = await get_or_init_manager()
    session = await manager.link_session_to_project(
        session_id=request.session_id,
        project_id=project_id,
        task_id=request.task_id,
        invite_code=request.invite_code,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Also link session on the task side if task specified
    if request.task_id:
        await pm.link_task_to_session(request.task_id, request.session_id)

    return {
        "success": True,
        "session_id": request.session_id,
        "project_id": project_id,
        "task_id": request.task_id,
    }


@router.delete("/project/{project_id}/unlink-session/{session_id}")
async def unlink_session_from_project(project_id: str, session_id: str):
    """Remove a session's link to a project."""
    manager = await get_or_init_manager()
    session = await manager.unlink_session_from_project(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True}


@router.get("/project/{project_id}/sessions")
async def get_project_sessions(project_id: str):
    """List all sessions linked to a project."""
    manager = await get_or_init_manager()
    sessions = await manager.get_project_sessions(project_id)
    return {
        "project_id": project_id,
        "sessions": [
            {
                "session_id": s.session_id,
                "title": s.title or f"Session {s.invite_code}",
                "invite_code": s.invite_code,
                "owner_id": s.owner_id,
                "state": s.state.value,
                "task_id": s.task_id,
                "participant_count": len(s.participants),
                "created_at": s.created_at,
                "updated_at": s.updated_at,
            }
            for s in sessions
        ],
        "total": len(sessions),
    }
