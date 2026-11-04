"""vibe_agents sessions HTTP client.

Typed client for the control-plane sessions API.

Dependencies: httpx and the canonical Session v1 models from
mistralai-vibe-harness. Import this submodule only when you need the client;
importing the root ``mistralai.vibe_agents`` does not trigger these imports.
"""

from mistralai.vibe_agents.sessions_client.api_models import (
    AgentSessionResponse,
    AgentSessionStatus,
    ArchiveSessionRequest,
    CancelAgentSessionRequest,
    DirectChildrenScopeInput,
    IdempotencyKey,
    InterruptAgentSessionRequest,
    ListSessionsResult,
    ObservedControllerEventResponse,
    RenameSessionRequest,
    RootsScopeInput,
    SessionAgentConfiguration,
    SessionCatalogScopeInput,
    SessionEventsHistoryResponse,
    SessionProtocol,
    SessionToolset,
    StartAgentSessionRequest,
    StartAgentSessionResponse,
    SubmitAgentMessageRequest,
    SubmitAgentMessageResponse,
    SubmitCallbackResultRequest,
    SubmitCallbackResultResponse,
    TreeScopeInput,
)
from mistralai.vibe_agents.sessions_client.client import SessionCommandRejectedError, SessionsAPIError, SessionsClient
from mistralai.vibe_agents.sessions_client.rendered_session_v1 import (
    Callback,
    RenderedSessionV1,
    parse_session_v1_event,
)

__all__ = [
    "AgentSessionResponse",
    "AgentSessionStatus",
    "ArchiveSessionRequest",
    "CancelAgentSessionRequest",
    "DirectChildrenScopeInput",
    "IdempotencyKey",
    "Callback",
    "InterruptAgentSessionRequest",
    "ListSessionsResult",
    "ObservedControllerEventResponse",
    "RenameSessionRequest",
    "RootsScopeInput",
    "SessionCatalogScopeInput",
    "RenderedSessionV1",
    "SessionAgentConfiguration",
    "SessionEventsHistoryResponse",
    "SessionProtocol",
    "SessionCommandRejectedError",
    "SessionsAPIError",
    "SessionsClient",
    "SessionToolset",
    "StartAgentSessionRequest",
    "StartAgentSessionResponse",
    "SubmitAgentMessageRequest",
    "SubmitAgentMessageResponse",
    "SubmitCallbackResultRequest",
    "SubmitCallbackResultResponse",
    "TreeScopeInput",
    "parse_session_v1_event",
]
