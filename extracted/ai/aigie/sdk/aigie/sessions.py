"""
Session tracking for Aigie SDK

Enhanced multi-turn conversation tracking with context management
"""

import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SessionMessage:
    """Message in a session"""

    id: str
    session_id: str
    role: str  # 'user', 'assistant', 'system', 'tool'
    content: Any
    timestamp: str
    metadata: dict[str, Any] = field(default_factory=dict)
    trace_id: str | None = None


@dataclass
class Session:
    """Conversation session"""

    id: str
    name: str
    created_at: str
    updated_at: str
    messages: list[SessionMessage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    user_id: str | None = None
    project_name: str | None = None


class SessionManager:
    """
    Session manager for tracking multi-turn conversations

    Manages conversation sessions with automatic message tracking,
    context management, and analytics

    Example:
        >>> from aigie.sessions import SessionManager
        >>>
        >>> manager = SessionManager()
        >>>
        >>> # Create session
        >>> session = await manager.create_session(
        ...     name="customer-support",
        ...     user_id="user-123"
        ... )
        >>>
        >>> # Add messages
        >>> await manager.add_message(
        ...     session_id=session.id,
        ...     role="user",
        ...     content="Hello, I need help"
        ... )
        >>>
        >>> # Use with Aigie tracing
        >>> async with manager.session_context(session.id) as session:
        ...     async with aigie.trace("agent-response") as trace:
        ...         response = await agent.run(session.get_context())
        ...         await manager.add_message(
        ...             session_id=session.id,
        ...             role="assistant",
        ...             content=response,
        ...             trace_id=trace.id
        ...         )
    """

    def __init__(self):
        """Initialize session manager"""
        self._sessions: dict[str, Session] = {}
        self._active_session: str | None = None

    async def create_session(
        self,
        name: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        project_name: str | None = None,
    ) -> Session:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        session = Session(
            id=session_id,
            name=name or f"session-{session_id[:8]}",
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
            tags=tags or [],
            user_id=user_id,
            project_name=project_name,
        )

        self._sessions[session_id] = session

        return session

    async def get_session(self, session_id: str) -> Session | None:
        """Get session by ID"""
        return self._sessions.get(session_id)

    async def list_sessions(
        self,
        user_id: str | None = None,
        tags: list[str] | None = None,
    ) -> list[Session]:
        """List all sessions"""
        sessions = list(self._sessions.values())

        # Filter by user_id
        if user_id:
            sessions = [s for s in sessions if s.user_id == user_id]

        # Filter by tags
        if tags:
            sessions = [s for s in sessions if any(tag in s.tags for tag in tags)]

        return sessions

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: Any,
        metadata: dict[str, Any] | None = None,
        trace_id: str | None = None,
    ) -> SessionMessage:
        """Add message to session"""
        session = self._sessions.get(session_id)

        if not session:
            raise ValueError(f"Session {session_id} not found")

        message = SessionMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {},
            trace_id=trace_id,
        )

        session.messages.append(message)
        session.updated_at = datetime.now().isoformat()

        return message

    async def get_messages(
        self,
        session_id: str,
        limit: int | None = None,
        role: str | None = None,
    ) -> list[SessionMessage]:
        """Get messages from session"""
        session = self._sessions.get(session_id)

        if not session:
            raise ValueError(f"Session {session_id} not found")

        messages = session.messages

        # Filter by role
        if role:
            messages = [m for m in messages if m.role == role]

        # Apply limit
        if limit:
            messages = messages[-limit:]

        return messages

    async def get_context(
        self,
        session_id: str,
        max_messages: int = 10,
        include_system: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Get conversation context for LLM

        Returns recent messages formatted for LLM input

        Args:
            session_id: Session ID
            max_messages: Maximum number of recent messages
            include_system: Include system messages

        Returns:
            List of messages in LLM format
        """
        messages = await self.get_messages(session_id, limit=max_messages)

        if not include_system:
            messages = [m for m in messages if m.role != "system"]

        return [{"role": m.role, "content": m.content} for m in messages]

    async def update_session(
        self,
        session_id: str,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> Session:
        """Update session"""
        session = self._sessions.get(session_id)

        if not session:
            raise ValueError(f"Session {session_id} not found")

        if name is not None:
            session.name = name
        if metadata is not None:
            session.metadata.update(metadata)
        if tags is not None:
            session.tags = tags

        session.updated_at = datetime.now().isoformat()

        return session

    async def delete_session(self, session_id: str) -> None:
        """Delete session"""
        if session_id in self._sessions:
            del self._sessions[session_id]

    async def clear_messages(self, session_id: str) -> None:
        """Clear all messages from session"""
        session = self._sessions.get(session_id)

        if not session:
            raise ValueError(f"Session {session_id} not found")

        session.messages = []
        session.updated_at = datetime.now().isoformat()

    def get_session_stats(self, session_id: str) -> dict[str, Any]:
        """Get session statistics"""
        session = self._sessions.get(session_id)

        if not session:
            raise ValueError(f"Session {session_id} not found")

        message_count_by_role = {}
        for message in session.messages:
            message_count_by_role[message.role] = message_count_by_role.get(message.role, 0) + 1

        total_duration = None
        if session.messages:
            first_message_time = datetime.fromisoformat(session.messages[0].timestamp)
            last_message_time = datetime.fromisoformat(session.messages[-1].timestamp)
            total_duration = (last_message_time - first_message_time).total_seconds()

        return {
            "session_id": session_id,
            "total_messages": len(session.messages),
            "messages_by_role": message_count_by_role,
            "duration_seconds": total_duration,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }

    @asynccontextmanager
    async def session_context(self, session_id: str):
        """
        Context manager for session

        Sets the active session for the duration of the context

        Example:
            >>> async with manager.session_context(session_id) as session:
            ...     # Session is active
            ...     await do_work()
        """
        previous_session = self._active_session
        self._active_session = session_id

        try:
            session = await self.get_session(session_id)
            yield session
        finally:
            self._active_session = previous_session

    def get_active_session_id(self) -> str | None:
        """Get currently active session ID"""
        return self._active_session


class SessionAnalytics:
    """Analytics for session tracking"""

    def __init__(self, manager: SessionManager):
        """Initialize analytics"""
        self.manager = manager

    async def get_user_sessions(self, user_id: str) -> list[Session]:
        """Get all sessions for a user"""
        return await self.manager.list_sessions(user_id=user_id)

    async def get_session_duration(self, session_id: str) -> float | None:
        """Get session duration in seconds"""
        stats = self.manager.get_session_stats(session_id)
        return stats.get("duration_seconds")

    async def get_average_messages_per_session(self, user_id: str | None = None) -> float:
        """Get average number of messages per session"""
        sessions = await self.manager.list_sessions(user_id=user_id)

        if not sessions:
            return 0.0

        total_messages = sum(len(s.messages) for s in sessions)
        return total_messages / len(sessions)

    async def get_most_active_sessions(self, limit: int = 10) -> list[tuple[Session, int]]:
        """Get most active sessions by message count"""
        sessions = list(self.manager._sessions.values())
        sessions_with_counts = [(s, len(s.messages)) for s in sessions]
        sessions_with_counts.sort(key=lambda x: x[1], reverse=True)

        return sessions_with_counts[:limit]

    async def get_role_distribution(self, session_id: str) -> dict[str, float]:
        """Get distribution of messages by role"""
        stats = self.manager.get_session_stats(session_id)
        messages_by_role = stats["messages_by_role"]
        total = stats["total_messages"]

        if total == 0:
            return {}

        return {role: count / total for role, count in messages_by_role.items()}


def create_session_manager() -> SessionManager:
    """Create session manager with sensible defaults"""
    return SessionManager()
