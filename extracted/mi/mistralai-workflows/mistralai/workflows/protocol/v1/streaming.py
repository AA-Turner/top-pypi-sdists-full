import time
from datetime import datetime, timezone
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field

from mistralai.workflows.protocol.v1.events import WorkflowEvent, WorkflowEventType

# NATS enforces a 2MB max payload per message. Both the SDK client and the
# server-side streaming service check against this limit before publishing.
MAX_EVENT_PAYLOAD_BYTES = 2 * 1024 * 1024  # 2MB


class StreamEventWriteActivityContext(BaseModel):
    activity_name: str
    activity_exec_id: str
    activity_attempt_number: int


class StreamEventReadActivityContext(BaseModel):
    activity_name: str = "*"
    activity_exec_id: str = "*"
    activity_attempt_number: int | Literal["*"] = "*"


class StreamEventWorkflowContext(BaseModel):
    namespace: str
    workflow_name: str
    workflow_exec_id: str
    parent_workflow_exec_id: str | None = None
    root_workflow_exec_id: str | None = None


class StreamEventNatsContext(BaseModel):
    nats_stream: str
    nats_subject: str


class StreamEvent(BaseModel):
    """Base class for all streaming events"""

    stream: str
    timestamp_unix_nano: int = Field(default_factory=lambda: time.time_ns())
    data: Any
    nats_context: StreamEventNatsContext | None = None  # Excluded in SSE output
    workflow_context: StreamEventWorkflowContext
    activity_context: StreamEventWriteActivityContext | None = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    broker_sequence: int | None = None  # Added by server in SSE output


class StreamEventsQueryParams(BaseModel):
    scope: Literal["activity", "workflow", "*"] = "*"
    activity_name: str = "*"
    activity_id: str = "*"
    workflow_name: str = "*"
    workflow_exec_id: str = "*"
    root_workflow_exec_id: str = "*"
    parent_workflow_exec_id: str = "*"
    stream: str = "*"
    start_seq: int = 0
    metadata_filters: Dict[str, Any] | None = None
    workflow_event_types: list[WorkflowEventType] | None = None


class StreamEventSsePayload(BaseModel):
    stream: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: WorkflowEvent
    workflow_context: StreamEventWorkflowContext
    metadata: Dict[str, Any] = Field(default_factory=dict)
    broker_sequence: int


class StreamEventSseErrorData(BaseModel):
    error: str
    reason: str


class StreamEventSse(BaseModel):
    event: str | None = None
    data: StreamEventSsePayload | StreamEventSseErrorData | None = None
    id: str | None = None
    retry: int | None = None
