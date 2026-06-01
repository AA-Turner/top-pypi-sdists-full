"""
Pipecat voice session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a voice session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class VoiceSessionContext:
    """
    Holds shared state across all handlers in a voice conversation session.

    This enables trace_id, turn numbers, and aggregated metrics
    to persist across the conversation lifecycle.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "Voice Conversation"
    session_id: str | None = None
    user_id: str | None = None

    # Turn tracking
    total_turns: int = 0
    current_turn: int = 0
    interruption_count: int = 0

    # Token usage
    total_input_tokens: int = 0
    total_output_tokens: int = 0

    # Cost tracking
    total_cost: float = 0.0
    stt_cost: float = 0.0
    tts_cost: float = 0.0
    llm_cost: float = 0.0

    # Duration tracking (ms)
    total_duration_ms: float = 0.0
    total_user_speech_ms: float = 0.0
    total_bot_speech_ms: float = 0.0

    # Service tracking
    stt_model: str | None = None
    tts_model: str | None = None
    llm_model: str | None = None

    # State flags
    trace_created: bool = False
    conversation_active: bool = False

    # Current span tracking
    current_turn_span_id: str | None = None
    current_stt_span_id: str | None = None
    current_llm_span_id: str | None = None
    current_tts_span_id: str | None = None

    def start_turn(self) -> int:
        """Start a new turn and return the turn number."""
        self.total_turns += 1
        self.current_turn = self.total_turns
        return self.current_turn

    def end_turn(self) -> None:
        """End the current turn."""
        self.current_turn_span_id = None

    def record_interruption(self) -> int:
        """Record an interruption and return the count."""
        self.interruption_count += 1
        return self.interruption_count

    def add_tokens(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:
        """Add token counts to the session totals."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    def add_cost(
        self,
        stt_cost: float = 0.0,
        tts_cost: float = 0.0,
        llm_cost: float = 0.0,
    ) -> None:
        """Add costs to the session totals."""
        self.stt_cost += stt_cost
        self.tts_cost += tts_cost
        self.llm_cost += llm_cost
        self.total_cost += stt_cost + tts_cost + llm_cost

    def add_duration(
        self,
        user_speech_ms: float = 0.0,
        bot_speech_ms: float = 0.0,
    ) -> None:
        """Add speech durations to the session totals."""
        self.total_user_speech_ms += user_speech_ms
        self.total_bot_speech_ms += bot_speech_ms

    def set_models(
        self,
        stt_model: str | None = None,
        tts_model: str | None = None,
        llm_model: str | None = None,
    ) -> None:
        """Set the models used in this session."""
        if stt_model:
            self.stt_model = stt_model
        if tts_model:
            self.tts_model = tts_model
        if llm_model:
            self.llm_model = llm_model

    def mark_trace_created(self) -> None:
        """Mark that the trace has been created."""
        self.trace_created = True

    def start_conversation(self) -> None:
        """Mark that the conversation has started."""
        self.conversation_active = True

    def end_conversation(self) -> None:
        """Mark that the conversation has ended."""
        self.conversation_active = False

    def get_summary(self) -> dict:
        """Get session summary."""
        return {
            "trace_id": self.trace_id,
            "trace_name": self.trace_name,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "total_turns": self.total_turns,
            "interruption_count": self.interruption_count,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "stt_cost": self.stt_cost,
            "tts_cost": self.tts_cost,
            "llm_cost": self.llm_cost,
            "total_user_speech_ms": self.total_user_speech_ms,
            "total_bot_speech_ms": self.total_bot_speech_ms,
            "stt_model": self.stt_model,
            "tts_model": self.tts_model,
            "llm_model": self.llm_model,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[VoiceSessionContext | None] = (
    contextvars.ContextVar("_current_pipecat_session_context", default=None)
)


def get_session_context() -> VoiceSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current VoiceSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: VoiceSessionContext | None) -> contextvars.Token:
    """
    Set the current session context.

    Args:
        context: The session context to set, or None to clear.

    Returns:
        Token that can be used to reset to the previous value.
    """
    return _current_session_context.set(context)


def reset_session_context(token: contextvars.Token) -> None:
    """
    Reset session context to a previous value.

    Args:
        token: Token from a previous set_session_context call.
    """
    _current_session_context.reset(token)


def get_or_create_session_context(
    trace_name: str = "Voice Conversation",
    trace_id: str | None = None,
    session_id: str | None = None,
    user_id: str | None = None,
) -> VoiceSessionContext:
    """
    Get the existing session context or create a new one.

    This is the main entry point for session context management.
    If a session context exists, it returns that context (preserving
    the shared trace_id). Otherwise, it creates a new context.

    Args:
        trace_name: Name for the trace (only used if creating new).
        trace_id: Optional trace ID to use (only used if creating new).
        session_id: Optional session ID (only used if creating new).
        user_id: Optional user ID (only used if creating new).

    Returns:
        The session context (existing or newly created).
    """
    existing = _current_session_context.get()
    if existing is not None:
        return existing

    # Create new session context
    context = VoiceSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
        session_id=session_id,
        user_id=user_id,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def voice_session(
    trace_name: str = "Voice Conversation",
    trace_id: str | None = None,
    session_id: str | None = None,
    user_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a voice session
    that should share a single trace.

    Example:
        with voice_session("Customer Support Call", session_id="session-123"):
            # All pipeline operations here share the same trace
            task = PipelineTask(pipeline, observers=[observer])
            await task.run()
            # Access session metrics
            print(f"Turns: {context.total_turns}")

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.
        session_id: Optional session ID.
        user_id: Optional user ID.

    Yields:
        The session context.
    """
    context = VoiceSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
        session_id=session_id,
        user_id=user_id,
    )
    token = _current_session_context.set(context)
    try:
        yield context
    finally:
        _current_session_context.reset(token)


def clear_session_context() -> None:
    """
    Clear the current session context.

    This forces a new trace to be created on the next conversation.
    """
    _current_session_context.set(None)


class VoiceSessionManager:
    """
    High-level session manager for voice conversations.

    Provides a convenient interface for managing session lifecycle
    and accessing session metrics.

    Example:
        manager = VoiceSessionManager()

        # Start a session
        session = manager.start_session("My Voice App", user_id="user-123")

        # Use with Pipecat
        observer = AigieObserver()
        task = PipelineTask(pipeline, observers=[observer])
        await task.run()

        # Get session summary
        print(manager.get_summary())

        # End session
        manager.end_session()
    """

    def __init__(self):
        self._session: VoiceSessionContext | None = None
        self._token: contextvars.Token | None = None

    def start_session(
        self,
        trace_name: str = "Voice Conversation",
        trace_id: str | None = None,
        session_id: str | None = None,
        user_id: str | None = None,
    ) -> VoiceSessionContext:
        """
        Start a new voice session.

        Args:
            trace_name: Name for the trace.
            trace_id: Optional trace ID to use.
            session_id: Optional session ID.
            user_id: Optional user ID.

        Returns:
            The new session context.
        """
        # End any existing session
        if self._session is not None:
            self.end_session()

        self._session = VoiceSessionContext(
            trace_id=trace_id or str(uuid.uuid4()),
            trace_name=trace_name,
            session_id=session_id,
            user_id=user_id,
        )
        self._token = set_session_context(self._session)
        return self._session

    def end_session(self) -> dict | None:
        """
        End the current session.

        Returns:
            Session summary if a session was active, None otherwise.
        """
        if self._session is None:
            return None

        summary = self._session.get_summary()

        if self._token is not None:
            reset_session_context(self._token)
            self._token = None

        self._session = None
        return summary

    @property
    def session(self) -> VoiceSessionContext | None:
        """Get the current session."""
        return self._session

    @property
    def is_active(self) -> bool:
        """Check if a session is currently active."""
        return self._session is not None

    def get_summary(self) -> dict | None:
        """Get summary of the current session."""
        if self._session is None:
            return None
        return self._session.get_summary()

    def record_turn_start(self) -> int:
        """Record the start of a new turn."""
        if self._session is None:
            return 0
        return self._session.start_turn()

    def record_turn_end(self) -> None:
        """Record the end of a turn."""
        if self._session is not None:
            self._session.end_turn()

    def record_interruption(self) -> int:
        """Record an interruption."""
        if self._session is None:
            return 0
        return self._session.record_interruption()

    def add_tokens(self, input_tokens: int = 0, output_tokens: int = 0) -> None:
        """Add token usage."""
        if self._session is not None:
            self._session.add_tokens(input_tokens, output_tokens)

    def add_cost(
        self,
        stt_cost: float = 0.0,
        tts_cost: float = 0.0,
        llm_cost: float = 0.0,
    ) -> None:
        """Add cost."""
        if self._session is not None:
            self._session.add_cost(stt_cost, tts_cost, llm_cost)
