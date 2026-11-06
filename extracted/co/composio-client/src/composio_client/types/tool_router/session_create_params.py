# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_create_params."""

from __future__ import annotations

from typing import Dict, Iterable, Literal, Optional, TypeAlias, Union

from typing_extensions import NotRequired, Required, TypedDict
from ..._types import SequenceNotStr


class ToolkitsEnable(TypedDict, total=False):
    "Enable only specific toolkits (allowlist)"

    enable: Required[SequenceNotStr[str]]
    "Only these specific toolkits will be enabled"
    require_approval: NotRequired[SequenceNotStr[str]]


class ToolkitsDisable(TypedDict, total=False):
    "Disable specific toolkits (denylist)"

    disable: Required[SequenceNotStr[str]]
    "These specific toolkits will be disabled"
    require_approval: NotRequired[SequenceNotStr[str]]


class ToolkitsRequireApproval(TypedDict, total=False):
    require_approval: Required[SequenceNotStr[str]]
    "Tool calls matched here pause until the user approves them. A tool needs approval if its toolkit, the tool itself or any of its tags is listed. A toolkit's own lists in `tools` replace the session-wide tag list for that toolkit."


class CurrentInstantVariant1ToolkitsVariant0(TypedDict, total=False):
    "Enable only specific toolkits (allowlist)"

    enable: Required[SequenceNotStr[str]]
    "Only these specific toolkits will be enabled"


class CurrentInstantVariant1ToolkitsVariant1(TypedDict, total=False):
    "Disable specific toolkits (denylist)"

    disable: Required[SequenceNotStr[str]]
    "These specific toolkits will be disabled"


class CurrentInstantVariant1ToolsValueVariant0(TypedDict, total=False):
    enable: Required[SequenceNotStr[str]]
    "Only these specific tools will be available for this toolkit"


class CurrentInstantVariant1ToolsValueVariant1(TypedDict, total=False):
    disable: Required[SequenceNotStr[str]]
    "These specific tools will be disabled for this toolkit"


class CurrentInstantVariant1(TypedDict, total=False):
    toolkits: NotRequired[CurrentInstantVariant1ToolkitsVariant0 | CurrentInstantVariant1ToolkitsVariant1]
    "Toolkit configuration - specify either enable toolkits (allowlist) or disable toolkits (denylist). Mutually exclusive."
    tools: NotRequired[dict[str, CurrentInstantVariant1ToolsValueVariant0 | CurrentInstantVariant1ToolsValueVariant1]]
    "Per-toolkit enable or disable lists that restrict instant usage. Toolkits absent from the map have no additional tool restriction. On PATCH, a supplied map replaces all existing tool filters; an empty map clears them, and omission preserves them."
    return_instant_charge: NotRequired[bool]
    "Return the top-level instant_charge in session tool responses when a charge is available. Defaults to false on create; omission on PATCH preserves the current value. Controls response visibility only; it does not enable or disable instant usage."
    return_prices_in_search: NotRequired[bool]
    "Experimental. Show each instant tool's price in tool search results, under instant_account.prices. Defaults to false on create; omit on PATCH to keep the current value. Does not turn instant usage on or off."


class ManageConnections(TypedDict, total=False):
    "Configuration for connection management settings"

    callback_url: str
    "The URL to redirect to after a user completes authentication for a connected\naccount. This allows you to handle the auth callback in your own application."
    enable: Optional[bool]
    "Whether to enable the connection manager for automatic connection handling.\n\nIf true, we will provide a tool your agent can use to initiate connections to\ntoolkits if it doesnt exist. If set to false, then you have to manage\nconnections manually."
    enable_connection_removal: Optional[bool]
    "Enable the \"remove\" action in COMPOSIO_MANAGE_CONNECTIONS to allow deleting\nconnected accounts. Default true."
    enable_wait_for_connections: Optional[bool]
    "When true, the COMPOSIO_WAIT_FOR_CONNECTIONS tool is available for agents to\npoll connection status after sharing auth URLs. Default is false (disabled). May\nnot work reliably with GPT models."


class ToolsEnable(TypedDict, total=False):
    enable: Required[SequenceNotStr[str]]
    "Only these specific tools will be available for this toolkit"
    require_approval: NotRequired[SequenceNotStr[str]]


class ToolsDisable(TypedDict, total=False):
    disable: Required[SequenceNotStr[str]]
    "These specific tools will be disabled for this toolkit"
    require_approval: NotRequired[SequenceNotStr[str]]


class ToolsTagsTagsUnionMember1(TypedDict, total=False):
    disable: list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]
    enable: list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]
    require_approval: NotRequired[list[Literal["readOnlyHint", "createHint", "updateHint", "destructiveHint", "idempotentHint", "openWorldHint"]]]


class ToolsTags(TypedDict, total=False):
    tags: Required[Union[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]], ToolsTagsTagsUnionMember1]]
    "MCP tags to filter tools.\n\nArray format is treated as enabled list. Object format supports both enabled and\ndisabled lists."
    require_approval: NotRequired[SequenceNotStr[str]]


class ToolsRequireApproval(TypedDict, total=False):
    require_approval: Required[SequenceNotStr[str]]
    "Tool calls matched here pause until the user approves them. Setting this toolkit's own list, even an empty one, replaces the session-wide `tags.require_approval` for its tools."


class TagsUnionMember1(TypedDict, total=False):
    disable: list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]
    enable: list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]
    require_approval: NotRequired[list[Literal["readOnlyHint", "createHint", "updateHint", "destructiveHint", "idempotentHint", "openWorldHint"]]]


class Workbench(TypedDict, total=False):
    "Configuration for workbench behavior"

    auto_offload_threshold: float
    "Character threshold for automatic offloading.\n\nWhen workbench response exceeds this threshold, it will be automatically\noffloaded. Default is picked automatically based on the response size."
    enable: bool
    "Set to false to disable the workbench entirely.\n\nWhen disabled, no code execution tools are available in the session."
    enable_proxy_execution: bool
    "Whether proxy execution is enabled.\n\nWhen enabled, workbench can call URLs and APIs directly."
    sandbox_size: Literal['standard', 'medium', 'large', 'xlarge']
    "Sandbox compute tier: standard (1 vCPU / 1 GB), medium (2 vCPU / 2 GB), large (4\nvCPU / 4 GB), xlarge (8 vCPU / 8 GB). Defaults to standard."
    enable_tool_execution: NotRequired[bool]


class CurrentProxyExecute(TypedDict, total=False):
    "Configure proxy execute. Omitted from responses when not set. Session creation fails when enable is false and workbench.enable_proxy_execution is explicitly true."

    enable: Required[bool]
    "When true, the agent can make authenticated HTTP requests to connected app APIs outside the workbench. When false, proxy execution is also disabled inside the workbench, regardless of workbench.enable_proxy_execution. When not set, proxy execute is disabled outside the workbench."


class MultiAccount(TypedDict, total=False):
    "Configure multi-account behavior.\n\nWhen enabled, users can connect multiple accounts per toolkit."

    enable: bool
    "When true, enables multi-account mode for this session.\n\nWhen not set, falls back to org/project-level configuration."
    max_accounts_per_toolkit: int
    "Maximum number of connected accounts allowed per toolkit.\n\nMust be between 2 and 10."
    require_explicit_selection: bool
    "When true, the agent must explicitly select which account to use.\n\nWhen false (default), the first/default account is used automatically."


class ExperimentalAssistivePromptConfig(TypedDict, total=False):
    "Customize assistive prompt generation (e.g., timezone)."

    user_timezone: str
    "IANA timezone identifier (e.g., 'America/New_York', 'Europe/London').\n\nUsed to customize the system prompt with timezone-aware instructions."


class ExperimentalCustomToolkitTool(TypedDict, total=False):
    description: Required[str]
    "Used for BM25 search matching and shown to the LLM."
    input_schema: Required[Dict[str, Optional[object]]]
    "Must have type: \"object\" and a properties field."
    name: Required[str]
    "Human-readable display name"
    output_schema: Dict[str, Optional[object]]
    "Optional output schema for the tool response."
    preload: bool
    "SDK hint for direct custom-tool exposure.\n\nNot stored in session config; echoed in create/attach responses for inline\ncustom definitions."
    slug: Required[str]
    "Tool slug.\n\nCombined with toolkit slug to form LOCAL*<TOOLKIT>*<TOOL> (max 60 chars total)."


class ExperimentalCustomToolkit(TypedDict, total=False):
    description: Required[str]
    "Used for BM25 search matching and shown in toolkit connection statuses."
    name: Required[str]
    "Display name shown to the LLM and in search results."
    preload: bool
    "SDK hint for direct custom-tool exposure.\n\nNot stored in session config; echoed in create/attach responses for inline\ncustom definitions."
    slug: Required[str]
    "Unique slug for the toolkit.\n\nMust not conflict with existing Composio toolkit slugs. Alphanumeric,\nunderscores, and hyphens only."
    tools: Required[Iterable[ExperimentalCustomToolkitTool]]
    "Tools in this custom toolkit"


class ExperimentalCustomTool(TypedDict, total=False):
    description: Required[str]
    "Used for BM25 search matching and shown to the LLM."
    extends_toolkit: str
    "If set, must be a valid Composio toolkit slug.\n\nThe tool inherits that toolkit's auth/connection status. If omitted, the tool is\nstandalone (no-auth)."
    input_schema: Required[Dict[str, Optional[object]]]
    "Must have type: \"object\" and a properties field."
    name: Required[str]
    "Human-readable display name"
    output_schema: Dict[str, Optional[object]]
    "JSON Schema describing tool output (optional)"
    preload: bool
    "SDK hint for direct custom-tool exposure.\n\nNot stored in session config; echoed in create/attach responses for inline\ncustom definitions."
    slug: Required[str]
    "Tool slug.\n\nForms LOCAL*<TOOL> (standalone) or LOCAL*<TOOLKIT>\\__<TOOL> (extending). Max 60\nchars total."


class ExperimentalPermissions(TypedDict, total=False):
    "Per-tool elicitation permission config.\n\nDefault behavior + per-tool always_allow/always_deny overrides. Mutation via PATCH."

    default: Required[Literal['allow_all', 'ask_every_call', 'ask_once_per_session']]
    "Default elicitation behavior when no override matches.\n\n`allow_all` runs every tool without prompting; `ask_every_call` prompts on each\ninvocation; `ask_once_per_session` prompts once and remembers the answer for the\nrest of the session."
    overrides: Dict[str, Literal['always_allow', 'always_deny', 'ask_once', 'ask_always']]
    "Per-tool overrides keyed by `${toolSlug}:${connectedAccountId ?? \"__none__\"}`,\nplus account-wide overrides keyed by `*:${connectedAccountId ?? \"__none__\"}`.\nExact tool overrides take precedence over account-wide overrides. `always_allow`\nskips the prompt and runs the tool; `always_deny` blocks the tool; `ask_once`\nprompts once per session (allow/deny) and remembers; `ask_always` prompts on\nevery call with allow-once/allow-session/deny, ignoring any cached session\nallow. Overrides take precedence over `default`."


class CurrentExperimentalSubmitFeedback(TypedDict, total=False):
    "Exposes the COMPOSIO_SUBMIT_FEEDBACK helper tool in this session so the agent can report tool executions with empty, incorrect, or failed results. Defaults to false."

    enable: NotRequired[bool]
    "Set to true to expose the COMPOSIO_SUBMIT_FEEDBACK helper tool in this session. Defaults to false."


class Experimental(TypedDict, total=False):
    "Experimental features - not stable, may be modified or removed in future versions."

    assistive_prompt_config: ExperimentalAssistivePromptConfig
    "Customize assistive prompt generation (e.g., timezone)."
    custom_toolkits: Iterable[ExperimentalCustomToolkit]
    "Custom toolkits with grouped tools.\n\nToolkit slugs must not conflict with existing Composio toolkits. All tools are\nno-auth."
    custom_tools: Iterable[ExperimentalCustomTool]
    "Custom tools to include in search.\n\nStandalone tools need no auth. Tools with extends_toolkit inherit the Composio\ntoolkit's connection."
    link_url_overwrite: str
    "Experimental base URL override for connection link redirects created from this\ntool-router session. When set, link creation returns\n`${link_url_overwrite}/link/{link_token}` instead of the default Composio\nConnect base URL. Use only when your integration needs links to open through a\ncustom Connect host."
    permissions: ExperimentalPermissions
    "Per-tool elicitation permission config.\n\nDefault behavior + per-tool always_allow/always_deny overrides. Mutation via\nPATCH."
    fast_mode: NotRequired[bool]
    disable_plan_search: NotRequired[bool]
    submit_feedback: NotRequired[CurrentExperimentalSubmitFeedback]
    restrict_egress_to_composio: NotRequired[bool]
    no_elicitation_support_fallback: NotRequired[Literal["deny", "allow"]]
    session_config_id: NotRequired[str]


class Preload(TypedDict, total=False):
    "Preload configuration.\n\nUse an explicit list for frequently used tool slugs, or \"all\" to dynamically expose every app tool allowed by positive toolkits/tools/tags filters."

    tools: Union[SequenceNotStr[str], str]
    "Explicit tool slugs to preload, or \"all\" to dynamically expose all current and\nfuture app tools allowed by the positive session filters. \"all\" is capped at\n1000 tools and is not supported without a positive allowlist."


class CurrentHookVariant0AppliesToVariant1(TypedDict, total=False):
    toolkits: Required[SequenceNotStr[str]]
    "Toolkit slugs"


class CurrentHookVariant0Handler(TypedDict, total=False):
    type: Required[Literal["condition_check"]]
    condition: Required[str]
    "What to block, written as a plain sentence. For example: \"Sending email to anyone outside example.org\"."
    action: Required[Literal["block"]]


class CurrentHookVariant0(TypedDict, total=False):
    type: Required[Literal["before_execute"]]
    id: Required[str]
    "Unique within the session. Shows up in results and logs."
    name: NotRequired[str]
    "A readable name. The agent sees it when this hook blocks a call."
    applies_to: Required[Literal["all"] | CurrentHookVariant0AppliesToVariant1]
    "Which tools the hook covers: \"all\" for all of them, or only the listed toolkits."
    handler: Required[CurrentHookVariant0Handler]


class CurrentHookVariant1AppliesToVariant1(TypedDict, total=False):
    toolkits: Required[SequenceNotStr[str]]
    "Toolkit slugs"


class CurrentHookVariant1HandlerVariant0(TypedDict, total=False):
    type: Required[Literal["condition_check"]]
    condition: Required[str]
    "What to block, written as a plain sentence. For example: \"Sending email to anyone outside example.org\"."
    action: Required[Literal["block"]]


class CurrentHookVariant1HandlerVariant1(TypedDict, total=False):
    "Blocks a tool response that tries to manipulate the agent: override its instructions, change its role, or make it take actions the user didn't ask for."

    type: Required[Literal["prompt_injection_check"]]
    action: Required[Literal["block"]]


class CurrentHookVariant1(TypedDict, total=False):
    type: Required[Literal["after_execute"]]
    id: Required[str]
    "Unique within the session. Shows up in results and logs."
    name: NotRequired[str]
    "A readable name. The agent sees it when this hook blocks a call."
    applies_to: Required[Literal["all"] | CurrentHookVariant1AppliesToVariant1]
    "Which tools the hook covers: \"all\" for all of them, or only the listed toolkits."
    handler: Required[CurrentHookVariant1HandlerVariant0 | CurrentHookVariant1HandlerVariant1]


class Search(TypedDict, total=False):
    enable: bool


class Execute(TypedDict, total=False):
    enable_multi_execute: bool


class SessionCreateParams(TypedDict, total=False):
    user_id: Required[str]
    "The identifier of the user who is initiating the session, ideally a unique\nidentifier from your database like a user ID or email address"
    toolkits: Union[ToolkitsEnable, ToolkitsDisable, ToolkitsRequireApproval]
    "Toolkit configuration - specify either enable toolkits (allowlist) or disable\ntoolkits (denylist). Mutually exclusive."
    auth_configs: Dict[str, str]
    "The auth configs to use for the session.\n\nThis will override the default behavior and use the given auth config when\nspecific toolkits are being executed"
    connected_accounts: Dict[str, SequenceNotStr[str]]
    "The connected accounts to use for the session, as an array of nano-IDs per\ntoolkit. This overrides the default behaviour and pins specific connected\naccounts when toolkits are executed. Each account must exist (not deleted or\ndisabled) and belong to the same `user_id` as the session. Multi-account\nsessions can pin multiple; non-multi-account sessions are capped at length 1."
    instant: NotRequired[Literal[False] | CurrentInstantVariant1]
    manage_connections: ManageConnections
    "Configuration for connection management settings"
    tools: Dict[str, Union[ToolsEnable, ToolsDisable, ToolsTags, ToolsRequireApproval]]
    "Tool-level configuration per toolkit.\n\nAllows you to enable, disable, or filter by tags for specific tools within each\ntoolkit. Every slug passed in `enable` / `disable` must be a valid Composio tool\nslug for that toolkit — invalid or typo'd slugs fail session creation with a\nclear error listing which ones didn't match."
    tags: Union[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]], TagsUnionMember1]
    "Global MCP tool annotation hints for filtering.\n\nArray format is treated as enabled list. Object format supports both enabled\n(tool must have at least one) and disabled (tool must NOT have any) lists.\nToolkit-level tags override this. Toolkit enabled/disabled lists take precedence\nover tag filtering."
    workbench: Workbench
    "Configuration for workbench behavior"
    proxy_execute: NotRequired[CurrentProxyExecute]
    multi_account: MultiAccount
    "Configure multi-account behavior.\n\nWhen enabled, users can connect multiple accounts per toolkit."
    experimental: Experimental
    "Experimental features - not stable, may be modified or removed in future\nversions."
    preload: Preload
    "Preload configuration.\n\nUse an explicit list for frequently used tool slugs, or \"all\" to dynamically\nexpose every app tool allowed by positive toolkits/tools/tags filters."
    hooks: NotRequired[Iterable[CurrentHookVariant0 | CurrentHookVariant1]]
    search: Search
    execute: Execute


Tags: TypeAlias = Union[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]], TagsUnionMember1]

Toolkits: TypeAlias = Union[ToolkitsEnable, ToolkitsDisable, ToolkitsRequireApproval]

Tools: TypeAlias = Union[ToolsEnable, ToolsDisable, ToolsTags, ToolsRequireApproval]

ToolsTagsTags: TypeAlias = Union[list[Literal['readOnlyHint', 'destructiveHint', 'idempotentHint', 'openWorldHint']], ToolsTagsTagsUnionMember1]

__all__ = [
    "SessionCreateParams",
    "Execute",
    "Experimental",
    "ExperimentalAssistivePromptConfig",
    "ExperimentalCustomToolkit",
    "ExperimentalCustomToolkitTool",
    "ExperimentalCustomTool",
    "ExperimentalPermissions",
    "ManageConnections",
    "MultiAccount",
    "Preload",
    "Search",
    "Tags",
    "TagsUnionMember1",
    "Toolkits",
    "ToolkitsEnable",
    "ToolkitsDisable",
    "Tools",
    "ToolsEnable",
    "ToolsDisable",
    "ToolsTags",
    "ToolsTagsTags",
    "ToolsTagsTagsUnionMember1",
    "Workbench",
    "CurrentInstantVariant1ToolkitsVariant0",
    "CurrentInstantVariant1ToolkitsVariant1",
    "CurrentInstantVariant1ToolsValueVariant0",
    "CurrentInstantVariant1ToolsValueVariant1",
    "CurrentInstantVariant1",
    "CurrentProxyExecute",
    "CurrentHookVariant0AppliesToVariant1",
    "CurrentHookVariant0Handler",
    "CurrentHookVariant0",
    "CurrentHookVariant1AppliesToVariant1",
    "CurrentHookVariant1HandlerVariant0",
    "CurrentHookVariant1HandlerVariant1",
    "CurrentHookVariant1",
    "ToolkitsRequireApproval",
    "ToolsRequireApproval",
    "CurrentExperimentalSubmitFeedback",
]
