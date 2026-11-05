"""vibe_agents sessions HTTP client.

Typed client for the control-plane sessions API.

Dependencies: httpx and the canonical Session v1 models from
mistralai-vibe-harness. Import this submodule only when you need the client;
importing the root ``mistralai.vibe_agents`` does not trigger these imports.
"""

# The types SessionsClient's methods take, and the members of the SessionWorkflowCommand and
# MessagePart unions;
# the module that defines them is internal.
from mistralai.vibe_agents.session_workflow import (
    CallbackResultCommand,
    CallbackResultPayload,
    CommandMetadata,
    IntegrationEventCommand,
    MessageCommand,
    MessageInput,
    MessagePartForm,
    MessagePartImage,
    MessagePartResourceLink,
    MessagePartText,
    SessionAgentCustomization,
    SessionWorkflowCommand,
    SessionWorkflowSubscription,
    SystemCommand,
)
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
    "CallbackResultCommand",
    "CallbackResultPayload",
    "CommandMetadata",
    "ArchiveSessionRequest",
    "CancelAgentSessionRequest",
    "DirectChildrenScopeInput",
    "IdempotencyKey",
    "IntegrationEventCommand",
    "Callback",
    "InterruptAgentSessionRequest",
    "ListSessionsResult",
    "MessageCommand",
    "MessageInput",
    "MessagePartForm",
    "MessagePartImage",
    "MessagePartResourceLink",
    "MessagePartText",
    "ObservedControllerEventResponse",
    "RenameSessionRequest",
    "RootsScopeInput",
    "SessionCatalogScopeInput",
    "RenderedSessionV1",
    "SessionAgentConfiguration",
    "SessionAgentCustomization",
    "SessionEventsHistoryResponse",
    "SessionProtocol",
    "SessionCommandRejectedError",
    "SessionsAPIError",
    "SessionsClient",
    "SessionWorkflowCommand",
    "SessionWorkflowSubscription",
    "SessionToolset",
    "StartAgentSessionRequest",
    "StartAgentSessionResponse",
    "SubmitAgentMessageRequest",
    "SubmitAgentMessageResponse",
    "SubmitCallbackResultRequest",
    "SubmitCallbackResultResponse",
    "SystemCommand",
    "TreeScopeInput",
    "parse_session_v1_event",
]
