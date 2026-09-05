"""Service layer with centralized protobuf imports for API version management."""

from typing import List, Optional, Tuple

# Centralized protobuf imports - update these when API version changes
from seltz_public_api.proto.v1.agent_pb2 import (
    AgentRun,
    AgentRunCitation,
    AgentRunGrounding,
    AgentRunOutput,
    AgentRunRequest,
    AgentRunSource,
    AgentRunStatus,
    AgentRunStopReason,
    ListAgentRunsResponse,
)
from seltz_public_api.proto.v1.agent_pb2_grpc import AgentServiceStub
from seltz_public_api.proto.v1.answer_pb2 import (
    AnswerRequest,
    AnswerResponse,
    AnswerStreamRequest,
    AnswerStreamResponse,
    Citation,
    Citations,
)
from seltz_public_api.proto.v1.answer_pb2_grpc import AnswerServiceStub
from seltz_public_api.proto.v1.fetch_pb2 import (
    FetchError,
    FetchRequest,
    FetchResponse,
    FetchResult,
    FetchStatus,
)
from seltz_public_api.proto.v1.fetch_pb2_grpc import FetchServiceStub
from seltz_public_api.proto.v1.monitor_pb2 import (
    CreateMonitorResponse,
    DeleteMonitorResponse,
    GetMonitorResponse,
    GetRunResponse,
    ListMonitorsResponse,
    ListRecordsResponse,
    ListRunRecordsResponse,
    ListRunRequestsResponse,
    ListRunsResponse,
    Monitor,
    MonitorSearchRequest,
    MonitorStatus,
    Record,
    RecordType,
    RequestStatus,
    Run,
    RunRequest,
    RunState,
    RunStatus,
    SortOrder,
    StreamRecordsResponse,
    UpdateMonitorResponse,
    Webhook,
    WebhookStatus,
)
from seltz_public_api.proto.v1.seltz_pb2 import Document, SearchRequest, SearchResponse
from seltz_public_api.proto.v1.seltz_pb2_grpc import SeltzServiceStub

# Default per-call deadline (seconds) for unary RPCs, shared by all services.
DEFAULT_TIMEOUT_SECONDS = 30


def auth_metadata(api_key: Optional[str]) -> List[Tuple[str, str]]:
    """Build the gRPC metadata carrying the bearer token, if a key is set."""
    if api_key:
        return [("authorization", f"Bearer {api_key}")]
    return []


__all__ = [
    "SeltzServiceStub",
    "AgentServiceStub",
    "AgentRun",
    "AgentRunRequest",
    "AgentRunOutput",
    "AgentRunSource",
    "AgentRunGrounding",
    "AgentRunCitation",
    "AgentRunStatus",
    "AgentRunStopReason",
    "ListAgentRunsResponse",
    "SearchRequest",
    "SearchResponse",
    "Document",
    "AnswerServiceStub",
    "AnswerRequest",
    "AnswerResponse",
    "AnswerStreamRequest",
    "AnswerStreamResponse",
    "Citation",
    "Citations",
    "FetchServiceStub",
    "FetchRequest",
    "FetchResponse",
    "FetchResult",
    "FetchError",
    "FetchStatus",
    "Monitor",
    "MonitorSearchRequest",
    "Webhook",
    "Run",
    "RunRequest",
    "Record",
    "ListRecordsResponse",
    "ListRunsResponse",
    "CreateMonitorResponse",
    "ListMonitorsResponse",
    "ListRunRecordsResponse",
    "DeleteMonitorResponse",
    "GetMonitorResponse",
    "GetRunResponse",
    "ListRunRequestsResponse",
    "StreamRecordsResponse",
    "UpdateMonitorResponse",
    "MonitorStatus",
    "RunStatus",
    "RecordType",
    "RequestStatus",
    "SortOrder",
    "RunState",
    "WebhookStatus",
    "DEFAULT_TIMEOUT_SECONDS",
    "auth_metadata",
]
