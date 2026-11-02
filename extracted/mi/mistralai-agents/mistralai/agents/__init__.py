import importlib
import warnings
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mistralai.agents import pattern, redaction
    from mistralai.vibe_agents.sdk import agents
    from mistralai.vibe_agents.sdk.agents import (
        Agent,
        AgentsError,
        AllConnectors,
        AllowApproval,
        AllRegistrySkills,
        AlreadySettled,
        Answered,
        APIConnectionError,
        APIStatusError,
        APITimeoutError,
        ApprovalCallbackContext,
        ApprovalHandler,
        ApprovalRequest,
        ApprovalTool,
        AudioContentBlock,
        AuthenticationError,
        BashkitSandbox,
        Blocked,
        Builtins,
        Busy,
        CallbackContext,
        CallbackOpened,
        CallbackResolved,
        CallbackSession,
        Client,
        ClientTool,
        ClientToolAnswer,
        ClientToolAnswerError,
        ClientToolCall,
        Completed,
        Connector,
        ContentAnnotations,
        CustomSandbox,
        DangerousLocalSandbox,
        DenyApproval,
        Depends,
        EgressPolicy,
        EmbeddedResourceContentBlock,
        Event,
        ExperimentalWarning,
        Failed,
        GitHubBinding,
        HeaderBinding,
        HistoryImportEntry,
        Hook,
        HookCallbackContext,
        HookDecision,
        ImageContentBlock,
        InternalServerError,
        Interrupted,
        InvalidOutput,
        LocalDockerSandbox,
        LocalRuntime,
        LocalSessionProcedureError,
        LocalSkillBundle,
        LocalSkillFile,
        MistralConnectorNotFoundError,
        MistralSandbox,
        MistralSecret,
        Network,
        NoSandbox,
        NotFound,
        ObservationLost,
        OpenApproval,
        OpenCallback,
        OpenClientToolCall,
        OutcomeUnknownError,
        PermissionDeniedError,
        PermissionMode,
        PermissionPolicy,
        PermissionRule,
        ProgrammaticToolCallingConfig,
        ProtocolError,
        PythonTool,
        RateLimitError,
        RegistrySkill,
        RemoteAgentDeploymentNotFoundError,
        RemoteMCP,
        RemoteSessionConflictError,
        ResourceLinkContentBlock,
        Running,
        Sandbox,
        SandboxCallbackContext,
        SandboxExecutionResult,
        SandboxHook,
        SandboxWorkspaceSkills,
        SdkError,
        Session,
        SessionBusyError,
        SessionConfigMismatchError,
        SessionInfo,
        SessionInput,
        SessionInUseError,
        SessionNotFoundError,
        SessionStartupTimeoutError,
        SessionTerminatedError,
        State,
        Subagent,
        SubagentPolicy,
        Termination,
        TextContentBlock,
        ToolAnnotations,
        ToolCall,
        ToolCallbackContext,
        ToolCallEntry,
        ToolDefinition,
        ToolError,
        ToolModelAccess,
        ToolResult,
        ToolResultEntry,
        Turn,
        TurnConflict,
        TurnEnded,
        TurnNotFoundError,
        TurnStarted,
        TurnState,
        UnknownEntry,
        UnknownEvent,
        UnknownOpenCallback,
        UnsupportedAgentFeatureError,
        UnsupportedSessionProcedureError,
        WorkspaceHeaderBindings,
        all_connectors,
        all_registry_skills,
        client_tool,
        connector,
        hook,
        list_sessions,
        local_runtime,
        now,
        random,
        reject,
        retry,
        skip,
        sleep,
        testing,
        tool,
        uuid4,
    )

    # Deprecated 1.1.0rc12 names, not exported: see `_RENAMED` and `_DEPRECATED_HARNESS` below.
    from mistralai.vibe_agents.sdk.agents import ClientToolDefinition as ClientToolDefinition
    from mistralai.vibe_agents.sdk.agents import Context as Context
    from mistralai.vibe_agents.sdk.agents import Harness as Harness
    from mistralai.vibe_agents.sdk.agents import HookSession as HookSession
    from mistralai.vibe_agents.sdk.agents import JsonFileSessionJournal as JsonFileSessionJournal
    from mistralai.vibe_agents.sdk.agents import RemoteSessionNotFoundError as RemoteSessionNotFoundError
    from mistralai.vibe_agents.sdk.agents import RemoteSessionOutcomeUnknownError as RemoteSessionOutcomeUnknownError
    from mistralai.vibe_agents.sdk.agents import RemoteSessionStartupTimeoutError as RemoteSessionStartupTimeoutError
    from mistralai.vibe_agents.sdk.agents import RemoteSessionStreamLostError as RemoteSessionStreamLostError
    from mistralai.vibe_agents.sdk.agents import SandboxHookContext as SandboxHookContext


# `import mistralai.agents as agents` reaches the SDK's public names directly;
# `from mistralai.agents import agents` keeps returning the module that holds them.
__all__ = [
    "agents",
    "pattern",
    "redaction",
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
    "Busy",
    "CallbackContext",
    "CallbackOpened",
    "CallbackResolved",
    "CallbackSession",
    "Client",
    "ClientTool",
    "ClientToolAnswer",
    "ClientToolAnswerError",
    "ClientToolCall",
    "Completed",
    "Connector",
    "ContentAnnotations",
    "CustomSandbox",
    "DangerousLocalSandbox",
    "DenyApproval",
    "Depends",
    "EgressPolicy",
    "EmbeddedResourceContentBlock",
    "Event",
    "ExperimentalWarning",
    "Failed",
    "GitHubBinding",
    "HeaderBinding",
    "HistoryImportEntry",
    "Hook",
    "HookCallbackContext",
    "HookDecision",
    "InternalServerError",
    "ImageContentBlock",
    "Interrupted",
    "InvalidOutput",
    "LocalDockerSandbox",
    "LocalRuntime",
    "LocalSessionProcedureError",
    "LocalSkillBundle",
    "LocalSkillFile",
    "MistralConnectorNotFoundError",
    "MistralSandbox",
    "MistralSecret",
    "Network",
    "NoSandbox",
    "NotFound",
    "ObservationLost",
    "OpenApproval",
    "OpenCallback",
    "OpenClientToolCall",
    "OutcomeUnknownError",
    "PermissionDeniedError",
    "PermissionMode",
    "PermissionPolicy",
    "PermissionRule",
    "ProgrammaticToolCallingConfig",
    "ProtocolError",
    "PythonTool",
    "RateLimitError",
    "RegistrySkill",
    "RemoteAgentDeploymentNotFoundError",
    "RemoteMCP",
    "RemoteSessionConflictError",
    "ResourceLinkContentBlock",
    "Running",
    "Sandbox",
    "SandboxCallbackContext",
    "SandboxExecutionResult",
    "SandboxHook",
    "SandboxWorkspaceSkills",
    "SdkError",
    "Session",
    "SessionBusyError",
    "SessionConfigMismatchError",
    "SessionInUseError",
    "SessionInfo",
    "SessionInput",
    "SessionNotFoundError",
    "SessionStartupTimeoutError",
    "SessionTerminatedError",
    "State",
    "Subagent",
    "SubagentPolicy",
    "Termination",
    "TextContentBlock",
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


# 1.1.0rc12 names of the callback types and of the errors this package exported: not exported, but still
# readable with a DeprecationWarning. The `agents` module holds the table of their new names and the warning text.
_RENAMED = frozenset(
    {
        "Context",
        "HookSession",
        "RemoteSessionNotFoundError",
        "RemoteSessionOutcomeUnknownError",
        "RemoteSessionStartupTimeoutError",
        "RemoteSessionStreamLostError",
        "SandboxHookContext",
    }
)

# The 1.1.0rc12 Harness name this package exported: not exported, but still readable with a DeprecationWarning
# that names the fields to pass to `agents.Agent`. The `agents` module holds the table of classes and the warning
# text. `VibeHarness` and `ParentHarness` stay on the `agents` module only, where rc12 had them.
_DEPRECATED_HARNESS = frozenset({"Harness"})


# Hidden from type checkers, which read the names from the imports above and so still report a
# misspelt `agents.Agnet` instead of typing every unknown attribute as `object`.
if not TYPE_CHECKING:

    def __getattr__(name: str) -> object:
        if name in _RENAMED:
            agents_module = _agents_module()
            # Not stored in the namespace, so that every read warns, at the caller's line.
            warnings.warn(agents_module._renamed_warning(name), DeprecationWarning, stacklevel=2)
            return agents_module._renamed_class(name)
        if name in _DEPRECATED_HARNESS:
            agents_module = _agents_module()
            warnings.warn(agents_module._harness_warning(name), DeprecationWarning, stacklevel=2)
            return agents_module._DEPRECATED_HARNESS[name]
        if name == "ClientToolDefinition":
            # The 1.1.0 pre-release name of a client tool's declaration: not exported, but still readable with
            # a DeprecationWarning. The `agents` module holds the class and the warning text.
            agents_module = _agents_module()
            warnings.warn(agents_module._CLIENT_TOOL_DEFINITION_WARNING, DeprecationWarning, stacklevel=2)
            return agents_module._ClientToolDefinition
        if name == "JsonFileSessionJournal":
            # The 1.1.0rc14 name of the experimental session journal: not exported, but still readable with a
            # DeprecationWarning. The `agents` module holds the class and the warning text.
            agents_module = _agents_module()
            warnings.warn(agents_module._JSON_FILE_SESSION_JOURNAL_WARNING, DeprecationWarning, stacklevel=2)
            return agents_module._JsonFileSessionJournal
        if name not in __all__:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

        module = _import(name)
        value = module if name in ("agents", "pattern", "redaction") else getattr(module, name)
        # Python calls a module's `__getattr__` on every lookup of a name its namespace lacks. Storing
        # the value makes later `agents.X` accesses plain lookups that skip the setup above.
        globals()[name] = value
        return value

    def _agents_module() -> Any:
        # The cached module once a first read resolved it, so later reads skip `_import`'s setup.
        return globals().get("agents") or __getattr__("agents")

    def _import(name: str) -> object:
        import temporalio.workflow  # noqa: PLC0415

        from mistralai.agents import _silence  # noqa: PLC0415

        # SDK consumers import this package from workflow modules. Keep the full import closure passed
        # through Temporal's sandbox, but defer it until a public SDK name is actually requested, so the
        # `agents` CLI, which lives in this package, starts without loading the SDK.
        with temporalio.workflow.unsafe.imports_passed_through():
            _silence.presilence()
            try:
                from mistralai.vibe_agents.sdk.quiet import quiet_local_sdk_logs  # noqa: PLC0415

                quiet_local_sdk_logs()
                if name in ("pattern", "redaction"):
                    module = importlib.import_module(f"mistralai.agents.{name}")
                else:
                    module = importlib.import_module("mistralai.vibe_agents.sdk.agents")
            finally:
                _silence.restore_runtime_warning_levels()
        return module

    # Lists the public names before `__getattr__` resolves them, for REPL completion and `help()`.
    def __dir__() -> list[str]:
        return sorted(set(globals()) | set(__all__))
