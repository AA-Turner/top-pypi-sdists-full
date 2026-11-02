"""vibe_agents sessions HTTP client.

Typed client for the control-plane sessions API.

Dependencies: httpx. Import this submodule only when you need the client;
importing the root ``mistralai.vibe_agents`` does not trigger these imports.

The Session v1 names additionally need the canonical models from
mistralai-vibe-harness (the ``sessions-client`` extra). They are resolved on
first access rather than at import, so a consumer on the legacy protocol keeps
working with httpx alone.
"""

from typing import TYPE_CHECKING, Any

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
from mistralai.vibe_agents.sessions_client.rendered_session import (
    Callback,
    RenderedSession,
    SessionRenderer,
)

if TYPE_CHECKING:
    from mistralai.vibe_agents.sessions_client.rendered_session_v1 import (
        RenderedSessionV1 as RenderedSessionV1,
    )
    from mistralai.vibe_agents.sessions_client.rendered_session_v1 import (
        parse_session_v1_event as parse_session_v1_event,
    )

_SESSION_V1_NAMES = frozenset({"RenderedSessionV1", "parse_session_v1_event"})


def __getattr__(name: str) -> Any:
    if name not in _SESSION_V1_NAMES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from mistralai.vibe_agents.sessions_client import rendered_session_v1  # noqa: PLC0415

    return getattr(rendered_session_v1, name)


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
    "RenderedSession",
    "RenderedSessionV1",
    "SessionAgentConfiguration",
    "SessionEventsHistoryResponse",
    "SessionProtocol",
    "SessionRenderer",
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
