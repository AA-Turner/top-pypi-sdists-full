"""Stateless procedures for the App Server Session Protocol."""

from collections.abc import Sequence
from typing import Literal, cast

from pydantic import Field, JsonValue

from ..models.base import SessionModel
from ..models.callbacks import CallbackResult
from ..models.common import (
    AbsolutePath,
    EventId,
    HistoryEntryId,
    ProtocolError,
    SessionId,
    TurnId,
)
from ..models.configuration import AgentConfig
from ..models.content import ContentBlock
from ..models.events import EventBatch
from ..models.history import HistoryEntry, HistoryImportEntry
from ..models.state import Page, PageRequest, SessionState, TurnState

type Capability = dict[str, JsonValue]
type PluginComponentKind = Literal[
    "skill",
    "knowledge",
    "library",
    "mcp_server",
    "connector",
    "hook",
    "agent",
    "subagent",
    "tool",
    "unknown",
]
type Procedure = Literal[
    "app_server/info",
    "app_server/session/start",
    "app_server/session/fork",
    "app_server/session/compact",
    "app_server/session/history/clear",
    "app_server/session/read",
    "app_server/session/history/list",
    "app_server/session/turns/list",
    "app_server/session/turn/start",
    "app_server/session/turn/steer",
    "app_server/session/turn/interrupt",
    "app_server/session/config/read",
    "app_server/session/config/write",
    "app_server/session/plugin/info",
    "app_server/session/plugin/reload",
    "app_server/session/callback/result",
    "app_server/session/events/read",
    "app_server/catalog/list",
    "app_server/catalog/rename",
    "app_server/catalog/archive",
    "app_server/catalog/delete",
    "app_server/branching/rewind",
    "app_server/branching/filesystem/rewind/read",
    "app_server/branching/filesystem/rewind/restoreFiles",
    "app_server/scheduling/loops/list",
    "app_server/scheduling/loops/create",
    "app_server/scheduling/loops/delete",
    "app_server/scheduling/loops/clear",
    "app_server/worker/read",
    "app_server/worker/wait",
    "app_server/worker/context/add",
    "app_server/worker/shellCommand",
    "app_server/worker/shellCommand/interrupt",
    "app_server/workspacePolicy/trust/read",
    "app_server/workspacePolicy/trust/decide",
    "app_server/workspacePolicy/trust/untrustedConfig",
    "app_server/workspacePolicy/prompt/prepare",
    "app_server/configuration/write",
    "app_server/configuration/schema/read",
    "app_server/configuration/fields/read",
    "app_server/configuration/proxy/read",
    "app_server/configuration/proxy/write",
    "app_server/configuration/reload",
    "app_server/configuration/thinking/write",
    "app_server/diagnostics/logs/read",
    "app_server/agentCatalog/switch",
    "app_server/agentCatalog/install",
    "app_server/connectorCatalog/auth/read",
    "app_server/connectorCatalog/refresh",
    "app_server/mcpManagement/read",
    "app_server/mcpManagement/refresh",
    "app_server/mcpManagement/toggle",
    "app_server/mcpManagement/add",
    "app_server/mcpManagement/logout",
    "app_server/mcpManagement/login",
    "app_server/codeReview/state",
    "app_server/codeReview/baseline",
    "app_server/codeReview/turnDiff",
    "app_server/codeReview/hunks",
    "app_server/codeReview/approve",
    "app_server/codeReview/revert",
    "app_server/vibeCodeWeb/projects/open",
    "app_server/vibeCodeWeb/projects/loadMore",
    "app_server/vibeCodeWeb/projects/create",
    "app_server/vibeCodeWeb/projects/select",
    "app_server/vibeCodeWeb/projects/unlink",
    "app_server/vibeCodeWeb/projects/cancel",
    "app_server/vibeCodeWeb/projects/recover",
    "app_server/vibeCodeWeb/teleport/start",
    "app_server/vibeCodeWeb/teleport/cancel",
    "app_server/vibeCodeWeb/teleport/push/respond",
    "app_server/account/read",
    "app_server/account/identity/read",
    "app_server/telemetry/record",
    "app_server/feedback/shouldShow",
    "app_server/feedback/record",
    "app_server/narration/summarize",
]

APP_SERVER_SESSION_IMPLEMENTED_PROCEDURES: tuple[Procedure, ...] = (
    "app_server/session/start",
    "app_server/session/fork",
    "app_server/session/history/clear",
    "app_server/session/read",
    "app_server/session/history/list",
    "app_server/session/turns/list",
    "app_server/session/turn/start",
    "app_server/session/turn/steer",
    "app_server/session/turn/interrupt",
    "app_server/session/config/read",
    "app_server/session/config/write",
    "app_server/session/callback/result",
    "app_server/session/events/read",
)

APP_SERVER_SESSION_PROTOCOL_PROCEDURES: tuple[Procedure, ...] = (
    *APP_SERVER_SESSION_IMPLEMENTED_PROCEDURES,
    "app_server/session/compact",
    "app_server/session/plugin/info",
    "app_server/session/plugin/reload",
)

APP_SERVER_CAPABILITY_PROCEDURES: dict[str, tuple[Procedure, ...]] = {
    "app_server/catalog": (
        "app_server/catalog/list",
        "app_server/catalog/rename",
        "app_server/catalog/archive",
        "app_server/catalog/delete",
    ),
    "app_server/branching": ("app_server/branching/rewind",),
    "app_server/branching/filesystem": (
        "app_server/branching/filesystem/rewind/read",
        "app_server/branching/filesystem/rewind/restoreFiles",
    ),
    "app_server/scheduling": (
        "app_server/scheduling/loops/list",
        "app_server/scheduling/loops/create",
        "app_server/scheduling/loops/delete",
        "app_server/scheduling/loops/clear",
    ),
    "app_server/worker": (
        "app_server/worker/read",
        "app_server/worker/wait",
        "app_server/worker/context/add",
        "app_server/worker/shellCommand",
        "app_server/worker/shellCommand/interrupt",
    ),
    "app_server/workspacePolicy": (
        "app_server/workspacePolicy/trust/read",
        "app_server/workspacePolicy/trust/decide",
        "app_server/workspacePolicy/trust/untrustedConfig",
        "app_server/workspacePolicy/prompt/prepare",
    ),
    "app_server/configuration": (
        "app_server/configuration/write",
        "app_server/configuration/schema/read",
        "app_server/configuration/fields/read",
        "app_server/configuration/proxy/read",
        "app_server/configuration/proxy/write",
        "app_server/configuration/reload",
        "app_server/configuration/thinking/write",
    ),
    "app_server/diagnostics": ("app_server/diagnostics/logs/read",),
    "app_server/agentCatalog": (
        "app_server/agentCatalog/switch",
        "app_server/agentCatalog/install",
    ),
    "app_server/connectorCatalog": (
        "app_server/connectorCatalog/auth/read",
        "app_server/connectorCatalog/refresh",
    ),
    "app_server/mcpManagement": (
        "app_server/mcpManagement/read",
        "app_server/mcpManagement/refresh",
        "app_server/mcpManagement/toggle",
        "app_server/mcpManagement/add",
        "app_server/mcpManagement/logout",
        "app_server/mcpManagement/login",
    ),
    "app_server/codeReview": (
        "app_server/codeReview/state",
        "app_server/codeReview/baseline",
        "app_server/codeReview/turnDiff",
        "app_server/codeReview/hunks",
        "app_server/codeReview/approve",
        "app_server/codeReview/revert",
    ),
    "app_server/vibeCodeWeb": (
        "app_server/vibeCodeWeb/projects/open",
        "app_server/vibeCodeWeb/projects/loadMore",
        "app_server/vibeCodeWeb/projects/create",
        "app_server/vibeCodeWeb/projects/select",
        "app_server/vibeCodeWeb/projects/unlink",
        "app_server/vibeCodeWeb/projects/cancel",
        "app_server/vibeCodeWeb/projects/recover",
        "app_server/vibeCodeWeb/teleport/start",
        "app_server/vibeCodeWeb/teleport/cancel",
        "app_server/vibeCodeWeb/teleport/push/respond",
    ),
    "app_server/account": (
        "app_server/account/read",
        "app_server/account/identity/read",
    ),
    "app_server/telemetry": ("app_server/telemetry/record",),
    "app_server/feedback": (
        "app_server/feedback/shouldShow",
        "app_server/feedback/record",
    ),
    "app_server/narration": ("app_server/narration/summarize",),
}


def app_server_capability(procedures: Sequence[Procedure]) -> Capability:
    return {"version": 1, "procedures": cast(JsonValue, list(procedures))}


def app_server_capabilities() -> dict[str, Capability]:
    return {
        namespace: app_server_capability(procedures)
        for namespace, procedures in APP_SERVER_CAPABILITY_PROCEDURES.items()
    }


class RequestEnvelope[ParamsT: SessionModel](SessionModel):
    """Transport request whose ID only correlates its response."""

    id: str
    method: Procedure
    params: ParamsT


class ResponseEnvelope[ResultT: SessionModel](SessionModel):
    id: str
    result: ResultT | None = None
    error: ProtocolError | None = None


def validate_request[ModelT: SessionModel](model: type[ModelT], value: object) -> ModelT:
    """Validate client wire data with strict server-side extra-field handling."""

    return model.model_validate(
        value,
        by_alias=True,
        by_name=False,
        extra="forbid",
    )


class ClientInfo(SessionModel):
    name: str
    version: str
    title: str | None = None


class ServerInfo(SessionModel):
    name: str
    version: str


class PluginComponent(SessionModel):
    kind: PluginComponentKind
    name: str
    source_path: AbsolutePath | None = None
    config: dict[str, JsonValue] = Field(default_factory=dict)


class PluginInfo(SessionModel):
    workdir: AbsolutePath | None = None
    components: list[PluginComponent] = Field(default_factory=list)
    raw: dict[str, JsonValue] = Field(default_factory=dict)


class InfoParams(SessionModel):
    client_info: ClientInfo | None = None
    capabilities: dict[str, Capability] = Field(default_factory=dict)


class InfoResponse(SessionModel):
    server_info: ServerInfo
    capabilities: dict[str, Capability] = Field(default_factory=dict)


class SessionStartParams(SessionModel):
    idempotency_key: str | None = None
    agent_config: AgentConfig
    history: list[HistoryImportEntry] = Field(default_factory=list)


class SessionStartResponse(SessionModel):
    state: SessionState
    last_event_id: EventId


class SessionForkParams(SessionModel):
    idempotency_key: str | None = None
    source_session_id: SessionId
    agent_config: AgentConfig | None = None
    after_turn_id: TurnId | None = None


class SessionForkResponse(SessionModel):
    state: SessionState
    last_event_id: EventId


class SessionCompactParams(SessionModel):
    session_id: SessionId
    instructions: str | None = None


class SessionCompactResponse(SessionModel):
    state: SessionState
    last_event_id: EventId
    summary: str | None = None


class SessionHistoryClearParams(SessionModel):
    idempotency_key: str | None = None
    session_id: SessionId


class SessionHistoryClearResponse(SessionModel):
    source_session_id: SessionId
    state: SessionState
    last_event_id: EventId


class SessionReadParams(SessionModel):
    session_id: SessionId
    history: PageRequest | None = None
    turns: PageRequest | None = None


class SessionReadResponse(SessionModel):
    state: SessionState
    last_event_id: EventId


class SessionHistoryListParams(SessionModel):
    session_id: SessionId
    turn_id: TurnId | None = None
    page: PageRequest = Field(default_factory=PageRequest)


class SessionHistoryListResponse(SessionModel):
    page: Page[HistoryEntry]


class SessionTurnsListParams(SessionModel):
    session_id: SessionId
    page: PageRequest = Field(default_factory=PageRequest)


class SessionTurnsListResponse(SessionModel):
    page: Page[TurnState]


class TurnStartParams(SessionModel):
    idempotency_key: str | None = None
    session_id: SessionId
    message_entry_id: HistoryEntryId | None = None
    message: list[ContentBlock] = Field(default_factory=list)


class TurnStartResponse(SessionModel):
    turn: TurnState
    last_event_id: EventId


class TurnSteerParams(SessionModel):
    idempotency_key: str | None = None
    session_id: SessionId
    expected_turn_id: TurnId
    message_entry_id: HistoryEntryId | None = None
    message: list[ContentBlock] = Field(default_factory=list)


class TurnSteerResponse(SessionModel):
    accepted: Literal[True] = True
    last_event_id: EventId


class TurnInterruptParams(SessionModel):
    session_id: SessionId
    expected_turn_id: TurnId


class TurnInterruptResponse(SessionModel):
    accepted: Literal[True] = True
    last_event_id: EventId


class ConfigReadParams(SessionModel):
    session_id: SessionId


class ConfigReadResponse(SessionModel):
    config: AgentConfig


class ConfigWriteParams(SessionModel):
    session_id: SessionId
    config: AgentConfig


class ConfigWriteResponse(SessionModel):
    config: AgentConfig
    last_event_id: EventId


class PluginInfoParams(SessionModel):
    session_id: SessionId


class PluginInfoResponse(SessionModel):
    info: PluginInfo


class PluginReloadParams(SessionModel):
    session_id: SessionId


class PluginReloadResponse(SessionModel):
    info: PluginInfo
    last_event_id: EventId


class CallbackResultParams(SessionModel):
    session_id: SessionId
    result: CallbackResult


class CallbackResultResponse(SessionModel):
    accepted: Literal[True] = True
    last_event_id: EventId


class EventsReadParams(SessionModel):
    """Read one Session strictly after an opaque event ID, then follow its live tail."""

    session_id: SessionId
    after_event_id: EventId | None = None
    batch_size: int = Field(default=100, ge=1)


class EventsReadResponse(SessionModel):
    batch: EventBatch
