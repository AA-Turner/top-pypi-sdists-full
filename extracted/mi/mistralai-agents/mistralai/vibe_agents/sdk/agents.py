"""Public authoring API for the Unified Harness runtime."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

# The module `import mistralai.agents.testing` loads, so `agents.testing` is one object both ways. Not
# `from mistralai.agents import testing`: that form first calls the package's lazy `__getattr__`,
# which imports this module again while it is still loading.
import mistralai.agents.testing as testing
from mistralai.vibe.harness.app_server.session import (
    AudioContentBlock,
    ContentAnnotations,
    EmbeddedResourceContentBlock,
    HistoryImportEntry,
    HistoryImportMessage,
    HistoryImportReasoning,
    HistoryImportSnapshot,
    HistoryImportToolCall,
    HistoryImportToolResult,
    ImageContentBlock,
    ResourceLinkContentBlock,
    TextContentBlock,
    UnknownContentBlock,
)
from mistralai.vibe.harness.app_server.session.local_record import (
    LocalSessionProcedureError as _LocalSessionProcedureError,
)
from mistralai.vibe.harness.core.protocol import TokenUsage
from mistralai.vibe.harness.runtime.capabilities import (
    PostAgentTurnHookAccept,
    PostLlmCallHookAccept,
    PostLlmCallHookReject,
    PostLlmCallHookRetry,
    PreAgentTurnHookContinue,
    PreAgentTurnHookSkip,
    PreLlmCallHookContinue,
    PreLlmCallHookSkip,
    PreToolCallHookContinue,
    PreToolCallHookSkip,
    ReplaceAssistantContent,
)
from mistralai.vibe_agents.sdk.assembly import assemble
from mistralai.vibe_agents.sdk.authoring import determinism as sdk_determinism
from mistralai.vibe_agents.sdk.authoring import errors as _errors
from mistralai.vibe_agents.sdk.authoring import hooks as _hooks
from mistralai.vibe_agents.sdk.authoring.agent import Agent
from mistralai.vibe_agents.sdk.authoring.connector_selection import AllConnectors, all_connectors
from mistralai.vibe_agents.sdk.authoring.contracts import (
    BashkitSandbox,
    CustomSandbox,
    DangerousLocalSandbox,
    Depends,
    EgressPolicy,
    HookCallbackContext,
    LocalDockerSandbox,
    LocalSkillBundle,
    LocalSkillFile,
    MistralSandbox,
    NoSandbox,
    RemoteMCP,
    Sandbox,
    SandboxCallbackContext,
    SandboxExecutionResult,
    SandboxHook,
    SessionInput,
    State,
    ToolCallbackContext,
)
from mistralai.vibe_agents.sdk.authoring.contracts import (
    Harness as _Harness,
)
from mistralai.vibe_agents.sdk.authoring.errors import (
    AgentsError,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    ClientToolAnswerError,
    InternalServerError,
    InvalidCursorError,
    LegacySessionError,
    MistralConnectorNotFoundError,
    ObservationLost,
    OutcomeUnknownError,
    PermissionDeniedError,
    RateLimitError,
    RemoteAgentDeploymentNotFoundError,
    SdkError,
    SessionBusyError,
    SessionConfigMismatchError,
    SessionIdempotencyConflictError,
    SessionInUseError,
    SessionNotFoundError,
    SessionStartupTimeoutError,
    SessionTerminatedError,
    TurnNotFoundError,
    UnsupportedAgentFeatureError,
    UnsupportedSessionProcedureError,
)
from mistralai.vibe_agents.sdk.authoring.experimental import ExperimentalWarning
from mistralai.vibe_agents.sdk.authoring.hooks import HookDecision, PostToolCall, PreToolCall, reject, retry, skip
from mistralai.vibe_agents.sdk.authoring.permissions import PermissionPolicy, PermissionRule
from mistralai.vibe_agents.sdk.authoring.sandbox_policy import (
    GitHubBinding,
    HeaderBinding,
    MistralApiBinding,
    Network,
    WorkspaceHeaderBindings,
)
from mistralai.vibe_agents.sdk.authoring.secrets import MistralSecret
from mistralai.vibe_agents.sdk.authoring.skills import (
    AllRegistrySkills,
    RegistrySkill,
    SandboxWorkspaceSkills,
    all_registry_skills,
)
from mistralai.vibe_agents.sdk.authoring.subagent import Subagent
from mistralai.vibe_agents.sdk.authoring.tool import (
    ClientTool,
    ClientToolAnswer,
    PythonTool,
    ToolModelAccess,
    client_tool,
    tool,
)
from mistralai.vibe_agents.sdk.authoring.tool import (
    ClientToolDefinition as _ClientToolDefinition,
)
from mistralai.vibe_agents.sdk.authoring.tool_definition import ToolAnnotations, ToolDefinition
from mistralai.vibe_agents.sdk.authoring.tool_errors import ToolError
from mistralai.vibe_agents.sdk.authoring.tool_result import ToolResult
from mistralai.vibe_agents.sdk.authoring.types import Builtins, PermissionMode, ProgrammaticToolCallingConfig
from mistralai.vibe_agents.sdk.client.api_client import Client
from mistralai.vibe_agents.sdk.client.approvals import (
    AllowApproval,
    ApprovalCallbackContext,
    ApprovalHandler,
    ApprovalRequest,
    ApprovalTool,
    DenyApproval,
)
from mistralai.vibe_agents.sdk.client.entries import (
    ContextMessage,
    MessageEntry,
    ToolCallEntry,
    ToolResultEntry,
    UnknownEntry,
)
from mistralai.vibe_agents.sdk.client.events import (
    CallbackOpened,
    CallbackResolved,
    EntryAdded,
    EntryCompleted,
    Event,
    Notice,
    SessionUpdated,
    TextDelta,
    TurnEnded,
    TurnStarted,
    TurnUpdated,
    UnknownEvent,
)
from mistralai.vibe_agents.sdk.client.handles import Session, Turn
from mistralai.vibe_agents.sdk.client.listing import LocalRuntime, list_sessions, local_runtime
from mistralai.vibe_agents.sdk.client.records import (
    AlreadySettled,
    Answered,
    Blocked,
    Busy,
    CancelledTermination,
    Completed,
    CompletedTermination,
    Failed,
    FailedTermination,
    Interrupted,
    InvalidOutput,
    NotFound,
    OpenApproval,
    OpenCallback,
    OpenClientToolCall,
    OpenSignIn,
    ProtocolError,
    Running,
    SessionInfo,
    SignInRequest,
    Termination,
    TurnConflict,
    TurnState,
    UnknownOpenCallback,
    UnknownOutcome,
    UnknownTermination,
)
from mistralai.vibe_agents.sdk.client.sign_ins import SignInAnswer
from mistralai.vibe_agents.sdk.client.unknown_values import UnknownValue
from mistralai.vibe_agents.sdk.transport.client_tools import ClientToolAnswers, ClientToolCall
from mistralai.vibe_agents.sdk.transport.remote import RemoteSessionConflictError as _RemoteSessionConflictError
from mistralai.vibe_agents.sdk.transport.results import ToolCall
from mistralai.vibe_agents.sdk.transport.session_journal import JsonFileSessionJournal as _JsonFileSessionJournal
from mistralai.vibe_agents.session_workflow import SessionAgentCustomization, SubagentPolicy
from mistralai.workflows.plugins.mistralai.connectors import decorator as connector_decorator

CallbackContext = assemble.CallbackContext
CallbackSession = assemble.CallbackSession
KeepCallbackOpen = assemble.KeepCallbackOpen
Hook = assemble.Hook


class _ParentHarness(_Harness):
    """The 1.1.0rc12 `agents.ParentHarness`, which `__getattr__` returns with a warning."""

    def __init__(self) -> None:
        raise UnsupportedAgentFeatureError(
            "parent_inheritance",
            "the Unified Harness backend does not support inheriting a parent Harness",
        )


class _ParentSandbox(NoSandbox):
    """The 1.0 `agents.ParentSandbox`, which `__getattr__` returns with a warning."""

    def __init__(self) -> None:
        raise UnsupportedAgentFeatureError(
            "parent_inheritance",
            "the Unified Harness backend does not support inheriting a parent Sandbox",
        )


class hook:
    """What a Hook receives at each point, and the result models for a Hook that changes what continues.

    A Hook that only continues returns ``None``; one that stops returns ``agents.skip``,
    ``agents.retry`` or ``agents.reject``.
    """

    PreAgentTurn = _hooks.PreAgentTurn
    PreLlmCall = _hooks.PreLlmCall
    PostLlmCall = _hooks.PostLlmCall
    PostAgentTurn = _hooks.PostAgentTurn
    PreToolCall = PreToolCall
    PostToolCall = PostToolCall
    ReplaceAssistantContent = ReplaceAssistantContent
    PreAgentTurnHookContinue = PreAgentTurnHookContinue
    PreAgentTurnHookSkip = PreAgentTurnHookSkip
    PreLlmCallHookContinue = PreLlmCallHookContinue
    PreLlmCallHookSkip = PreLlmCallHookSkip
    PostLlmCallHookAccept = PostLlmCallHookAccept
    PostLlmCallHookRetry = PostLlmCallHookRetry
    PostLlmCallHookReject = PostLlmCallHookReject
    PreToolCallHookContinue = PreToolCallHookContinue
    PreToolCallHookSkip = PreToolCallHookSkip
    PostToolCallHookContinue = _hooks.PostToolCallHookContinue
    PostAgentTurnHookAccept = PostAgentTurnHookAccept


now = sdk_determinism.now
sleep = sdk_determinism.sleep
uuid4 = sdk_determinism.uuid4
random = sdk_determinism.random

Connector = connector_decorator.ConnectorSlot
connector = connector_decorator.connector

if TYPE_CHECKING:
    from pydantic import BaseModel
    from typing_extensions import deprecated

    # The 1.1.0rc12 and rc14 error names are plain aliases for type checkers, which report nothing, so that code
    # type-checks as it is. At runtime `__getattr__` returns the same classes with a `DeprecationWarning`.
    RemoteSessionNotFoundError = SessionNotFoundError
    RemoteSessionOutcomeUnknownError = OutcomeUnknownError
    RemoteSessionStartupTimeoutError = SessionStartupTimeoutError
    RemoteSessionStreamLostError = _errors.RemoteStreamLostError
    LocalSessionProcedureError = _LocalSessionProcedureError
    RemoteSessionConflictError = _RemoteSessionConflictError

    # For type checkers, each deprecated 1.1.0rc12 name of a renamed class is a subclass of the new class,
    # marked `@deprecated`, so they report each use. At runtime `__getattr__` returns the new class itself,
    # with a `DeprecationWarning`. Being a subclass, the old name is narrower than the new class: a Hook
    # method overridden with `ctx: agents.Context`, or a new object where the type is an old name, fails
    # type-checking. Running it still works.
    @deprecated("agents.Tool is deprecated: use agents.PythonTool")
    class Tool[**P, R](PythonTool[P, R]): ...

    @deprecated(
        "agents.ClientToolDefinition is deprecated: declare a client tool with agents.client_tool, "
        "or a tool with handler= with @agents.tool"
    )
    class ClientToolDefinition[ToolInput: BaseModel](_ClientToolDefinition[ToolInput]): ...

    @deprecated("agents.JsonFileSessionJournal is deprecated: use mistralai.agents.experimental.JsonFileSessionJournal")
    class JsonFileSessionJournal(_JsonFileSessionJournal): ...

    @deprecated("agents.Context is deprecated: use agents.HookCallbackContext")
    class Context(HookCallbackContext): ...

    @deprecated("agents.HookSession is deprecated: use agents.CallbackSession")
    class HookSession(CallbackSession): ...

    @deprecated("agents.SandboxHookContext is deprecated: use agents.SandboxCallbackContext")
    class SandboxHookContext(SandboxCallbackContext): ...

    # The Harness names stay plain aliases, which type checkers report nothing for.
    Harness = _Harness
    VibeHarness = _Harness
    ParentHarness = _ParentHarness
    ParentSandbox = _ParentSandbox

# 1.1.0rc12 names of the callback types and of the errors, kept working with a warning until a later release
# removes them. `mistralai.agents` serves the same names through this table.
_RENAMED = {
    **_errors._RENAMED,
    "Context": "HookCallbackContext",
    "HookSession": "CallbackSession",
    "SandboxHookContext": "SandboxCallbackContext",
}


# 1.1.0rc12 Harness names and the 1.0 `ParentSandbox`, kept working with a warning until a later release removes
# them: an Agent takes the Harness fields itself, and a subagent always uses the root's sandbox.
# `mistralai.agents` serves the same names through this table.
_DEPRECATED_HARNESS: dict[str, type[_Harness] | type[NoSandbox]] = {
    "Harness": _Harness,
    "VibeHarness": _Harness,
    "ParentHarness": _ParentHarness,
    "ParentSandbox": _ParentSandbox,
}


# 1.1.0rc12 name of a Python tool, kept working with a warning until a later release removes it.
# `mistralai.agents` serves it too.
_TOOL_WARNING = "agents.Tool is deprecated: use agents.PythonTool"


# 1.1.0 pre-release name of a client tool's declaration, handler= included, kept working with a warning until a
# later release removes it. `mistralai.agents` serves it too.
_CLIENT_TOOL_DEFINITION_WARNING = (
    "agents.ClientToolDefinition is deprecated: declare a client tool with agents.client_tool, "
    "or a tool with handler= with @agents.tool"
)


# 1.1.0rc14 name of the experimental session journal, kept working with a warning until a later release removes
# it. `mistralai.agents` serves it too.
_JSON_FILE_SESSION_JOURNAL_WARNING = (
    "agents.JsonFileSessionJournal is deprecated: use mistralai.agents.experimental.JsonFileSessionJournal"
)


# 1.1.0rc14 host-specific error names, kept working with a warning until a later release removes them: each
# host raises the same class for the same meaning, all in the `AgentsError` family. The old name stays its old
# class, so an `except` on it catches what it caught before. `mistralai.agents` serves them too.
_HOST_ERRORS: dict[str, type[Exception]] = {
    "LocalSessionProcedureError": _LocalSessionProcedureError,
    "RemoteSessionConflictError": _RemoteSessionConflictError,
}


def _host_error_warning(name: str) -> str:
    return (
        f"agents.{name} is deprecated: stable calls raise agents.AgentsError, so catch that; an event cursor that "
        "is not valid raises agents.InvalidCursorError on both hosts"
    )


def _renamed_warning(name: str) -> str:
    return f"agents.{name} is deprecated: use agents.{_RENAMED[name]}"


def _renamed_class(name: str) -> object:
    return _errors._renamed_class(name) if name in _errors._RENAMED else globals()[_RENAMED[name]]


def _harness_warning(name: str) -> str:
    if name == "ParentHarness":
        # rc12's ParentHarness always raised: there is no Harness to inherit, so point at the subagent's own fields.
        return (
            "agents.ParentHarness is deprecated: parent inheritance is not supported; set the subagent's fields "
            "(tools=, connectors=, mcps=, skills=, hooks=, sandbox_access=) on agents.Subagent"
        )
    if name == "ParentSandbox":
        # Like ParentHarness, ParentSandbox raises when built: a subagent always runs in the root's sandbox.
        return (
            "agents.ParentSandbox is deprecated: a subagent always uses the root's sandbox; set its access with "
            "sandbox_access= on agents.Subagent"
        )
    return (
        f"agents.{name} is deprecated: pass its fields (tools=, sandbox= as environment=, connectors=, mcps=, skills=, "
        "hooks=, guardrails=, secrets=) to agents.Agent"
    )


def __getattr__(name: str) -> object:
    # 1.0.x and rc12 code builds Python tools as agents.Tool(handler=...): keep that name working, with a warning.
    if name == "Tool":
        warnings.warn(_TOOL_WARNING, DeprecationWarning, stacklevel=2)
        return PythonTool
    if name in _RENAMED:
        warnings.warn(_renamed_warning(name), DeprecationWarning, stacklevel=2)
        return _renamed_class(name)
    if name in _DEPRECATED_HARNESS:
        warnings.warn(_harness_warning(name), DeprecationWarning, stacklevel=2)
        return _DEPRECATED_HARNESS[name]
    if name == "ClientToolDefinition":
        warnings.warn(_CLIENT_TOOL_DEFINITION_WARNING, DeprecationWarning, stacklevel=2)
        return _ClientToolDefinition
    if name == "JsonFileSessionJournal":
        warnings.warn(_JSON_FILE_SESSION_JOURNAL_WARNING, DeprecationWarning, stacklevel=2)
        return _JsonFileSessionJournal
    if name in _HOST_ERRORS:
        warnings.warn(_host_error_warning(name), DeprecationWarning, stacklevel=2)
        return _HOST_ERRORS[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Agent",
    "AgentsError",
    "AllConnectors",
    "AllRegistrySkills",
    "APIConnectionError",
    "APIStatusError",
    "APITimeoutError",
    "AuthenticationError",
    "AudioContentBlock",
    "AllowApproval",
    "AlreadySettled",
    "Answered",
    "ApprovalCallbackContext",
    "ApprovalHandler",
    "ApprovalRequest",
    "ApprovalTool",
    "BashkitSandbox",
    "Blocked",
    "Builtins",
    "CallbackOpened",
    "CallbackResolved",
    "Busy",
    "CallbackContext",
    "CallbackSession",
    "KeepCallbackOpen",
    "Client",
    "ClientTool",
    "ClientToolAnswer",
    "ClientToolAnswerError",
    "ClientToolAnswers",
    "ClientToolCall",
    "Completed",
    "Connector",
    "ContentAnnotations",
    "ContextMessage",
    "CustomSandbox",
    "DangerousLocalSandbox",
    "DenyApproval",
    "EgressPolicy",
    "EntryAdded",
    "EntryCompleted",
    "Event",
    "ExperimentalWarning",
    "Depends",
    "EmbeddedResourceContentBlock",
    "Failed",
    "GitHubBinding",
    "Hook",
    "HookCallbackContext",
    "HookDecision",
    "InternalServerError",
    "LegacySessionError",
    "ImageContentBlock",
    "Interrupted",
    "InvalidCursorError",
    "InvalidOutput",
    "LocalDockerSandbox",
    "LocalRuntime",
    "LocalSkillBundle",
    "LocalSkillFile",
    "MistralApiBinding",
    "MistralConnectorNotFoundError",
    "MistralSandbox",
    "MistralSecret",
    "Network",
    "NoSandbox",
    "NotFound",
    "MessageEntry",
    "Notice",
    "ObservationLost",
    "OpenApproval",
    "OpenCallback",
    "OpenClientToolCall",
    "OpenSignIn",
    "OutcomeUnknownError",
    "PermissionDeniedError",
    "PermissionPolicy",
    "PermissionRule",
    "PermissionMode",
    "ProgrammaticToolCallingConfig",
    "ProtocolError",
    "PythonTool",
    "RateLimitError",
    "RegistrySkill",
    "RemoteAgentDeploymentNotFoundError",
    "RemoteMCP",
    "ResourceLinkContentBlock",
    "Running",
    "Sandbox",
    "SandboxCallbackContext",
    "SandboxExecutionResult",
    "SandboxHook",
    "SandboxWorkspaceSkills",
    "HeaderBinding",
    "HistoryImportEntry",
    "HistoryImportMessage",
    "HistoryImportReasoning",
    "HistoryImportSnapshot",
    "HistoryImportToolCall",
    "HistoryImportToolResult",
    "SdkError",
    "Session",
    "SessionAgentCustomization",
    "SessionBusyError",
    "SessionConfigMismatchError",
    "SessionIdempotencyConflictError",
    "SessionInUseError",
    "SessionInfo",
    "SessionInput",
    "SessionNotFoundError",
    "SessionStartupTimeoutError",
    "SessionTerminatedError",
    "SessionUpdated",
    "SignInAnswer",
    "SignInRequest",
    "State",
    "Subagent",
    "SubagentPolicy",
    "Termination",
    "CompletedTermination",
    "CancelledTermination",
    "FailedTermination",
    "UnknownOutcome",
    "UnknownTermination",
    "UnknownValue",
    "TextContentBlock",
    "TextDelta",
    "TokenUsage",
    "ToolAnnotations",
    "ToolCall",
    "ToolCallEntry",
    "ToolCallbackContext",
    "ToolDefinition",
    "ToolError",
    "ToolModelAccess",
    "ToolResult",
    "ToolResultEntry",
    "Turn",
    "TurnConflict",
    "TurnEnded",
    "TurnNotFoundError",
    "TurnStarted",
    "TurnState",
    "TurnUpdated",
    "UnknownContentBlock",
    "UnknownEntry",
    "UnknownEvent",
    "UnknownOpenCallback",
    "UnsupportedAgentFeatureError",
    "UnsupportedSessionProcedureError",
    "WorkspaceHeaderBindings",
    "all_connectors",
    "all_registry_skills",
    "client_tool",
    "connector",
    "hook",
    "list_sessions",
    "local_runtime",
    "now",
    "random",
    "reject",
    "retry",
    "skip",
    "sleep",
    "testing",
    "tool",
    "uuid4",
]
