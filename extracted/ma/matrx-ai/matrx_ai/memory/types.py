"""
Types and dataclasses for Mastra Observational Memory (Python port).

Mirrors: packages/memory/src/processors/observational-memory/types.ts
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Literal, Optional, Union


# ---------------------------------------------------------------------------
# Scope / Config enumerations
# ---------------------------------------------------------------------------

class MemoryScope(str, Enum):
    THREAD = "thread"
    RESOURCE = "resource"


# ---------------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------------

@dataclass
class ModelConfig:
    """Configuration for an LLM used by Observer or Reflector."""
    model: str
    temperature: float = 0.0
    max_tokens: int = 100_000
    # Thinking budget (for models that support it, e.g. Gemini Flash)
    thinking_budget: Optional[int] = None


# ---------------------------------------------------------------------------
# Threshold config
# ---------------------------------------------------------------------------

@dataclass
class ThresholdRange:
    """
    Dynamic shared-budget threshold.
    The effective threshold = max(max - current_other_tokens, min).
    """
    min: int
    max: int


# Token threshold can be a fixed int or a dynamic range (shared budget mode)
TokenThreshold = Union[int, ThresholdRange]


# ---------------------------------------------------------------------------
# Observation / Reflection sub-configs
# ---------------------------------------------------------------------------

@dataclass
class ObservationConfig:
    """
    Configuration for the Observer agent.
    
    token_threshold: When unobserved message tokens exceed this, trigger observation.
    model: LLM model config.
    instruction: Additional instruction appended to the system prompt.
    previous_observer_tokens: Token budget for passing prior observations back to Observer.
    """
    token_threshold: TokenThreshold = 30_000
    model: ModelConfig = field(default_factory=lambda: ModelConfig(
        model="gemini-2.5-flash",
        temperature=0.3,
        max_tokens=100_000,
        thinking_budget=215,
    ))
    instruction: Optional[str] = None
    previous_observer_tokens: Optional[int] = None
    # Buffer: fraction (<1.0) or absolute token count >0
    buffer_tokens: float = 0.2        # 0.2 = 20% of token_threshold
    # blockAfter: fraction (>1.0) of threshold beyond which sync observation is forced
    block_after: float = 1.2


@dataclass
class ReflectionConfig:
    """
    Configuration for the Reflector agent.
    
    token_threshold: When observation tokens exceed this, trigger reflection.
    """
    token_threshold: TokenThreshold = 40_000
    model: ModelConfig = field(default_factory=lambda: ModelConfig(
        model="gemini-2.5-flash",
        temperature=0.0,
        max_tokens=100_000,
        thinking_budget=1024,
    ))
    instruction: Optional[str] = None
    # Buffer similar to observation buffering
    buffer_activation: float = 0.5
    block_after: float = 1.2


# ---------------------------------------------------------------------------
# Retrieval config
# ---------------------------------------------------------------------------

@dataclass
class RetrievalConfig:
    """Configuration for retrieval mode (recall tool)."""
    enabled: bool = False
    # How many token chars of raw message history to make available
    token_budget: int = 20_000


# ---------------------------------------------------------------------------
# Top-level ObservationalMemory config
# ---------------------------------------------------------------------------

@dataclass
class ObservationalMemoryConfig:
    """
    Top-level configuration for ObservationalMemory.
    
    scope: 'thread' (default) or 'resource' (cross-thread memory for a user).
    share_token_budget: If True, observations + messages share a combined budget.
    activate_after_idle: Seconds of idle before buffered observations are auto-activated.
    """
    observation: ObservationConfig = field(default_factory=ObservationConfig)
    reflection: ReflectionConfig = field(default_factory=ReflectionConfig)
    scope: MemoryScope = MemoryScope.THREAD
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    share_token_budget: bool = False
    activate_after_idle: Optional[int] = None
    # UI: whether to obscure thread IDs in output (privacy)
    obscure_thread_ids: bool = False
    # Called for debug events during processing
    on_debug_event: Optional[Callable[[dict], None]] = None


# ---------------------------------------------------------------------------
# Message types
# ---------------------------------------------------------------------------

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


@dataclass
class ToolCallPart:
    tool_call_id: str
    tool_name: str
    args: dict[str, Any]


@dataclass
class ToolResultPart:
    tool_call_id: str
    tool_name: str
    result: Any
    is_error: bool = False


@dataclass
class TextPart:
    text: str


@dataclass
class ImagePart:
    url: Optional[str] = None
    base64: Optional[str] = None
    media_type: Optional[str] = None
    filename: Optional[str] = None


# A message content part
MessagePart = Union[TextPart, ToolCallPart, ToolResultPart, ImagePart]


@dataclass
class Message:
    """Single message in a conversation thread."""
    id: str
    thread_id: str
    resource_id: str
    role: MessageRole
    content: Union[str, list[MessagePart]]
    created_at: datetime = field(default_factory=datetime.utcnow)
    # Optional: set to True once this message has been included in an observation
    observed: bool = False
    # Token count of this message (cached after first calculation)
    token_count: Optional[int] = None

    def get_text(self) -> str:
        """Return the text content of this message."""
        if isinstance(self.content, str):
            return self.content
        parts = []
        for part in self.content:
            if isinstance(part, TextPart):
                parts.append(part.text)
            elif isinstance(part, ToolCallPart):
                import json
                parts.append(f"[Tool Call: {part.tool_name}({json.dumps(part.args)})]")
            elif isinstance(part, ToolResultPart):
                parts.append(f"[Tool Result: {part.tool_name}: {part.result}]")
        return "\n".join(parts)


# ---------------------------------------------------------------------------
# Observer / Reflector results
# ---------------------------------------------------------------------------

@dataclass
class ObserverResult:
    """Parsed output from the Observer LLM."""
    observations: str
    current_task: Optional[str] = None
    suggested_response: Optional[str] = None
    thread_title: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class ReflectorResult:
    """Parsed output from the Reflector LLM."""
    reflections: str
    input_tokens: int = 0
    output_tokens: int = 0


# ---------------------------------------------------------------------------
# Storage record types
# ---------------------------------------------------------------------------

@dataclass
class BufferedObservationChunk:
    """A pre-computed observation chunk from async buffering."""
    cycle_id: str
    observations: str
    message_tokens: int       # Tokens of messages this chunk observed
    observation_tokens: int   # Tokens in the resulting observations
    message_count: int
    message_ids: list[str]
    message_range: str        # "firstId:lastId"
    current_task: Optional[str] = None
    suggested_continuation: Optional[str] = None
    thread_title: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ObservationalMemoryRecord:
    """
    Persisted state for one observation context (per thread or per resource).
    
    Mirrors the DB table record in the TS implementation.
    """
    id: str
    resource_id: str
    scope: MemoryScope

    # Thread-scoped: set for THREAD scope, None for RESOURCE scope
    thread_id: Optional[str] = None

    # ---- Core memory ----
    active_observations: Optional[str] = None         # The current observation text
    observation_token_count: int = 0                  # Tokens in active_observations
    current_task: Optional[str] = None                # What the agent is currently doing
    suggested_response: Optional[str] = None          # Hint for actor's next message

    # ---- Cursors ----
    last_observed_at: Optional[datetime] = None       # Timestamp of last observed message
    observed_message_ids: list[str] = field(default_factory=list)
    pending_message_tokens: int = 0                   # Cached pending token count

    # ---- Async buffering state ----
    buffered_observations: list[BufferedObservationChunk] = field(default_factory=list)
    is_buffering_observation: bool = False
    last_buffered_at_tokens: int = 0                  # DB-persisted boundary
    last_buffered_at_time: Optional[datetime] = None  # Timestamp cursor

    # ---- Async reflection state ----
    buffered_reflection: Optional[str] = None
    buffered_reflection_input_tokens: int = 0
    buffered_reflection_tokens: int = 0
    is_buffering_reflection: bool = False
    reflected_observation_line_count: int = 0

    # ---- Generation tracking ----
    generation_count: int = 0

    # ---- Metadata ----
    observed_timezone: str = "UTC"
    config: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Status / introspection
# ---------------------------------------------------------------------------

@dataclass
class ObservationalMemoryStatus:
    """
    Result of getStatus() — what actions are pending this turn.
    
    Pure read — does not modify any state.
    """
    should_observe: bool
    should_buffer: bool
    should_reflect: bool
    message_tokens: int
    observation_tokens: int
    unobserved_message_tokens: int
    pending_buffered_tokens: int
    message_token_threshold: int
    observation_token_threshold: int
    buffer_token_threshold: int
    has_buffered_chunks: bool
    buffered_chunk_count: int
