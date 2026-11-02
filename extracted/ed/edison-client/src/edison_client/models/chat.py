from datetime import datetime
from enum import StrEnum, auto
from typing import Any
from uuid import UUID

from aviary.core import Message, ToolRequestMessage, ToolResponseMessage
from pydantic import BaseModel, Field, JsonValue, TypeAdapter

AviaryMessageAdapter: TypeAdapter[Message] = TypeAdapter(
    ToolRequestMessage | ToolResponseMessage | Message
)


class ChatDispatchStatus(StrEnum):
    PENDING = auto()
    DISPATCHED = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()


class ChatMessagePayload(BaseModel):
    """Payload for sending a chat message."""

    project_id: UUID = Field(description="Project to chat within")
    session_id: UUID | None = Field(
        default=None, description="Existing session ID, or None for a new session"
    )
    message: str = Field(description="User message content")
    info: dict | None = Field(
        default=None,
        description="Optional metadata to attach to the user message",
    )
    ttl_seconds: int | None = Field(
        default=None,
        ge=60,
        le=86400,
        description="Optional sandbox TTL override in seconds",
    )
    timeout: int | None = Field(
        default=None,
        ge=30,
        le=172800,
        description="Optional execution timeout override in seconds per chat turn",
    )
    job_name: str | None = Field(
        default=None, description="Job name identifying which agent to chat with"
    )


class ChatMessageResponse(BaseModel):
    """Response from sending a chat message."""

    session_id: UUID = Field(description="Session ID (new or existing)")
    status: ChatDispatchStatus = Field(description="Dispatch lifecycle status")
    claim_name: str | None = Field(
        default=None, description="K8s SandboxClaim resource name"
    )
    pod_name: str | None = Field(
        default=None, description="K8s pod name serving this sandbox"
    )
    logs_url: str | None = Field(
        default=None, description="GKE console logs URL for the sandbox pod"
    )


class ChatRecoverPayload(BaseModel):
    """Payload for recovering a chat session."""

    project_id: UUID = Field(description="Project ID for recovery")
    job_name: str | None = Field(
        default=None,
        description="Job name for the agent (used to resolve the sandbox template on recovery) -- optional will infer recovery template from the default service template (dummy-env)",
    )


class ChatRecoverResponse(BaseModel):
    """Response from recovering a chat session."""

    session_id: UUID = Field(description="Session being recovered")
    status: ChatDispatchStatus = Field(description="Dispatch lifecycle status")
    logs_url: str | None = Field(
        default=None, description="GKE pod log URL (internal users only)"
    )


class ChatSandboxClaimResponse(BaseModel):
    """Recorded sandbox claim for a chat session, including one past its TTL."""

    claim_name: str | None = None
    pod_name: str | None = None
    created_at: datetime | None = None


class ConversationMessage(BaseModel):
    """A single message in a conversation."""

    role: str = Field(description="The role of the message sender")
    content: str | list[dict[str, JsonValue]] = Field(
        description="The content of the message"
    )
    tool_calls: list[dict] | None = Field(
        default=None, description="Tool calls for assistant tool-request messages"
    )
    tool_call_id: str | None = Field(
        default=None, description="Tool call ID for tool-response messages"
    )
    name: str | None = Field(
        default=None, description="Tool name for tool-response messages"
    )
    info: dict | None = Field(
        default=None,
        description=("The aviary `Message.info`."),
    )
    metadata: dict | None = Field(
        default=None, description="Optional metadata associated with the message"
    )
    message_id: UUID | None = Field(default=None, description="Stable message ID")
    created_at: datetime = Field(description="DB-assigned row timestamp")
    content_block_start: int | None = Field(default=None, ge=0)
    content_block_end: int | None = Field(default=None, ge=0)
    content_block_total: int | None = Field(default=None, ge=0)

    def to_aviary_message(self) -> Message:
        return AviaryMessageAdapter.validate_python(self.model_dump())


class ChatConversation(BaseModel):
    """A conversation grouped by session."""

    session_id: UUID = Field(description="The session ID for this conversation")
    created_at: datetime = Field(
        description="Timestamp when the conversation was created"
    )
    # stolen from the service side code, but we should consider a more robust schema
    messages: list[Any] = Field(description="The messages in this conversation")


class ChatConversationList(BaseModel):
    """Response listing conversations."""

    conversations: list[ChatConversation] = Field(
        description="List of conversations associated with the provided session_id if any"
    )


class ConversationContinuationCursor(BaseModel):
    message_id: UUID
    block_index: int = Field(ge=0)


class ConversationDetail(BaseModel):
    """Detailed conversation with typed messages."""

    messages: list[ConversationMessage] = Field(
        description="The messages in the conversation"
    )
    session_id: UUID = Field(
        description="The session ID to be used for follow-up messages"
    )
    has_more: bool = Field(
        default=False,
        description="True when older messages exist beyond the current page",
    )
    continuation_cursor: ConversationContinuationCursor | None = None


class StoreMessagePayload(BaseModel):
    """Payload for storing a conversation message."""

    message: dict = Field(description="Message JSON (aviary Message format)")
    metadata: dict | None = Field(
        default=None, description="Optional metadata to attach to the message"
    )


class QueueMessagePayload(BaseModel):
    """Payload for queueing a message to a running rollout's pending queue."""

    target_id: UUID = Field(description="Session ID (chat) or trajectory ID (run)")
    project_id: UUID = Field(description="Project the target belongs to")
    message: str = Field(description="User message content")


class QueueMessageResponse(BaseModel):
    """Response from the queue endpoint."""

    id: UUID = Field(description="Pending message ID")
    target_id: UUID = Field(description="Session or trajectory ID")
