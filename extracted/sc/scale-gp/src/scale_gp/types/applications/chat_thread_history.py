# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from ..chat_thread import ChatThread
from .chat_threads.chat_thread_feedback import ChatThreadFeedback

__all__ = ["ChatThreadHistory", "Message", "MessageEntry", "MessageSpan"]


class MessageEntry(BaseModel):
    id: str

    aggregated: bool
    """
    Boolean of whether this interaction has been uploaded to s3 bucket yet, default
    is false
    """

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: Dict[str, object]

    operation_status: Literal["SUCCESS", "ERROR", "CANCELED"]
    """The outcome of the operation"""

    output: Dict[str, object]

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT", "AGENTS_SERVICE"]] = None

    models: Optional[List[str]] = None
    """The models used for this interaction"""

    operation_metadata: Optional[Dict[str, object]] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """


class MessageSpan(BaseModel):
    id: str
    """Identifies the application step"""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    node_id: str
    """The id of the node in the application_variant config that emitted this insight"""

    operation_status: Literal["SUCCESS", "ERROR", "CANCELED"]
    """The outcome of the operation"""

    operation_type: Literal[
        "TEXT_INPUT",
        "TEXT_OUTPUT",
        "COMPLETION_INPUT",
        "COMPLETION",
        "KB_RETRIEVAL",
        "KB_INPUT",
        "RERANKING",
        "EXTERNAL_ENDPOINT",
        "PROMPT_ENGINEERING",
        "DOCUMENT_INPUT",
        "MAP_REDUCE",
        "DOCUMENT_SEARCH",
        "DOCUMENT_PROMPT",
        "CUSTOM",
        "CODE_EXECUTION",
        "DATA_MANIPULATION",
        "EVALUATION",
        "FILE_RETRIEVAL",
        "KB_ADD_CHUNK",
        "KB_MANAGEMENT",
        "GUARDRAIL",
        "TRACER",
        "AGENT_TRACER",
        "AGENT_WORKFLOW",
        "STANDALONE",
    ]
    """Type of the operation, e.g. RERANKING"""

    start_timestamp: datetime
    """The start time of the step"""

    account_id: Optional[str] = None
    """The ID of the account that owns the given entity."""

    application_interaction_id: Optional[str] = None
    """The interaction ID this span belongs to"""

    application_variant_id: Optional[str] = None
    """The id of the application variant this span belongs to"""

    created_by_identity_type: Optional[Literal["user", "service_account"]] = None
    """The type of identity that created the entity."""

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    end_timestamp: Optional[datetime] = None
    """
    The end time of the step, nullable, since it can be set to done at a later point
    in time.
    """

    group_id: Optional[str] = None
    """The ID of the group this span belongs to"""

    operation_expected: Optional[Dict[str, object]] = None
    """The JSON representation of the expected output for this step"""

    operation_input: Optional[Dict[str, object]] = None
    """The JSON representation of the input that this step received"""

    operation_metadata: Optional[Dict[str, object]] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    operation_output: Optional[Dict[str, object]] = None
    """The JSON representation of the output that this step emitted"""

    parent_id: Optional[str] = None
    """Who is the parent span of this current span, null if span is root parent."""

    trace_id: Optional[str] = None
    """The root-level ID where this span belongs to"""


class Message(BaseModel):
    entry: MessageEntry

    feedback: Optional[ChatThreadFeedback] = None

    spans: Optional[List[MessageSpan]] = None


class ChatThreadHistory(BaseModel):
    application_spec_id: str
    """The ID of the application spec that the thread belongs to."""

    messages: List[Message]

    thread: ChatThread
