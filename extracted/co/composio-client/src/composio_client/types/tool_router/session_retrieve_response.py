# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_retrieve_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict
from ..._base_model import BaseModel


class ConfigExecute(BaseModel):
    "Execute helper configuration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable_multi_execute: Optional[bool] = None


class ConfigManageConnections(BaseModel):
    "Manage connections configuration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    callback_url: Optional[str] = None
    "Custom callback URL for connected account auth flows"
    enable_connection_removal: Optional[bool] = None
    "Enable the \"remove\" action in COMPOSIO_MANAGE_CONNECTIONS. Default true."
    enable_wait_for_connections: Optional[bool] = None
    "Enable the COMPOSIO_WAIT_FOR_CONNECTIONS tool for polling connection status.\n\nDefault false. May not work reliably with GPT models."
    enabled: Optional[bool] = None
    "Whether to enable the connection manager for automatic connection handling"


class ConfigMultiAccount(BaseModel):
    "Multi-account configuration for this session."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable: Optional[bool] = None
    "When true, enables multi-account mode for this session.\n\nWhen not set, falls back to org/project-level configuration."
    max_accounts_per_toolkit: Optional[int] = None
    "Maximum number of connected accounts allowed per toolkit.\n\nDefaults to 5 when multi-account is enabled."
    require_explicit_selection: Optional[bool] = None
    "When true, require explicit account selection when multiple accounts are\nconnected. When false (default), use the first/default account."


class ConfigPreload(BaseModel):
    "Preload configuration.\n\nExplicit slugs are returned as an array; dynamic preload is returned as \"all\"."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    tools: Union[list[str], Literal['all']]
    "Explicit preloaded tool slugs, or \"all\" when the session dynamically exposes all\napp tools allowed by its filters."


class ConfigSearch(BaseModel):
    "Search helper configuration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable: Optional[bool] = None


class ConfigTags(BaseModel):
    "MCP tool annotation hints for filtering tools with enabled/disabled support.\n\nenabled: tags that the tool must have at least one of. disabled: tags that the tool must NOT have any of. Both conditions must be satisfied."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must NOT have any of"
    enabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must have at least one of"
    require_approval: list[Literal["readOnlyHint", "createHint", "updateHint", "destructiveHint", "idempotentHint", "openWorldHint"]] | None = None


class ConfigToolkitsEnabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]
    require_approval: list[str] | None = None


class ConfigToolkitsDisabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]
    require_approval: list[str] | None = None


class ConfigToolkitsRequireApproval(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    require_approval: list[str]
    "Tool calls matched here pause until the user approves them."


class ConfigToolsEnabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]
    require_approval: list[str] | None = None


class ConfigToolsDisabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]
    require_approval: list[str] | None = None


class ConfigToolsTagsTags(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must NOT have any of"
    enabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must have at least one of"
    require_approval: list[Literal["readOnlyHint", "createHint", "updateHint", "destructiveHint", "idempotentHint", "openWorldHint"]] | None = None


class ConfigToolsTags(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    tags: ConfigToolsTagsTags
    require_approval: list[str] | None = None


class ConfigToolsRequireApproval(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    require_approval: list[str]
    "Tool calls matched here pause until the user approves them."


class ConfigWorkbench(BaseModel):
    "Workbench configuration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auto_offload_threshold: Optional[float] = None
    "Character threshold after which tool execution response are saved to a file in\nworkbench. Default is 20k."
    enable: Optional[bool] = None
    "Whether the workbench (code execution sandbox) is enabled.\n\nWhen false, COMPOSIO_REMOTE_WORKBENCH and COMPOSIO_REMOTE_BASH_TOOL are not\nexposed."
    proxy_execution_enabled: Optional[bool] = None
    "Whether proxy execution is enabled in the workbench"
    sandbox_size: Optional[Literal['standard', 'medium', 'large', 'xlarge']] = None
    "Sandbox compute tier: standard (1 vCPU / 1 GB), medium (2 vCPU / 2 GB), large (4\nvCPU / 4 GB), xlarge (8 vCPU / 8 GB). Defaults to standard."
    tool_execution_enabled: bool | None = None


class CurrentConfigInstantVariant1ToolkitsVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]


class CurrentConfigInstantVariant1ToolkitsVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]


class CurrentConfigInstantVariant1ToolsValueVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]


class CurrentConfigInstantVariant1ToolsValueVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]


class CurrentConfigInstantVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    toolkits: CurrentConfigInstantVariant1ToolkitsVariant0 | CurrentConfigInstantVariant1ToolkitsVariant1 | None = None
    tools: dict[str, CurrentConfigInstantVariant1ToolsValueVariant0 | CurrentConfigInstantVariant1ToolsValueVariant1] | None = None
    return_instant_charge: bool
    return_prices_in_search: bool


class CurrentConfigProxyExecute(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable: bool


class CurrentConfigHookVariant0AppliesToVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    toolkits: list[str]


class CurrentConfigHookVariant0Handler(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["condition_check"]
    condition: str
    action: Literal["block"]


class CurrentConfigHookVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["before_execute"]
    id: str
    name: str | None = None
    applies_to: Literal["all"] | CurrentConfigHookVariant0AppliesToVariant1
    handler: CurrentConfigHookVariant0Handler


class CurrentConfigHookVariant1AppliesToVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    toolkits: list[str]


class CurrentConfigHookVariant1HandlerVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["condition_check"]
    condition: str
    action: Literal["block"]


class CurrentConfigHookVariant1HandlerVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["prompt_injection_check"]
    action: Literal["block"]


class CurrentConfigHookVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["after_execute"]
    id: str
    name: str | None = None
    applies_to: Literal["all"] | CurrentConfigHookVariant1AppliesToVariant1
    handler: CurrentConfigHookVariant1HandlerVariant0 | CurrentConfigHookVariant1HandlerVariant1


class Config(BaseModel):
    "The configuration used to create this session"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_configs: Optional[Dict[str, str]] = None
    "Auth config overrides per toolkit"
    connected_accounts: Optional[Dict[str, list[str]]] = None
    "Per-toolkit connected account overrides (array of nano-IDs).\n\nMulti-account sessions can pin more than one account per toolkit; otherwise\nlength is 1."
    execute: ConfigExecute
    "Execute helper configuration"
    manage_connections: Optional[ConfigManageConnections] = None
    "Manage connections configuration"
    multi_account: Optional[ConfigMultiAccount] = None
    "Multi-account configuration for this session."
    preload: ConfigPreload
    "Preload configuration.\n\nExplicit slugs are returned as an array; dynamic preload is returned as \"all\"."
    search: ConfigSearch
    "Search helper configuration"
    tags: Optional[ConfigTags] = None
    "MCP tool annotation hints for filtering tools with enabled/disabled support.\n\nenabled: tags that the tool must have at least one of. disabled: tags that the\ntool must NOT have any of. Both conditions must be satisfied."
    toolkits: Union[ConfigToolkitsEnabled, ConfigToolkitsDisabled, ConfigToolkitsRequireApproval, None] = None
    "Toolkit configuration - either enabled list or disabled list"
    tools: Optional[Dict[str, Union[ConfigToolsEnabled, ConfigToolsDisabled, ConfigToolsTags, ConfigToolsRequireApproval]]] = None
    "Tool-level configuration per toolkit"
    user_id: str
    "User identifier for this session"
    workbench: Optional[ConfigWorkbench] = None
    "Workbench configuration"
    instant: Literal[False] | CurrentConfigInstantVariant1
    proxy_execute: CurrentConfigProxyExecute | None = None
    hooks: list[CurrentConfigHookVariant0 | CurrentConfigHookVariant1] | None = None


class ExperimentalCustomToolkitTool(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    description: str
    input_schema: Dict[str, Optional[object]]
    name: str
    original_slug: str
    "Original tool slug as provided by the user"
    output_schema: Optional[Dict[str, Optional[object]]] = None
    slug: str
    "Prefixed tool slug (e.g. LOCAL_CRM_FIND_CUSTOMER)"
    preload: bool | None = None


class ExperimentalCustomToolkit(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    description: str
    name: str
    slug: str
    tools: list[ExperimentalCustomToolkitTool]
    preload: bool | None = None


class ExperimentalCustomTool(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    description: str
    extends_toolkit: Optional[str] = None
    input_schema: Dict[str, Optional[object]]
    name: str
    original_slug: str
    "Original tool slug as provided by the user"
    output_schema: Optional[Dict[str, Optional[object]]] = None
    slug: str
    "Prefixed tool slug (e.g. LOCAL_GMAIL_GET_IMPORTANT_EMAILS)"
    preload: bool | None = None


class CurrentExperimentalSourceSessionConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str


class Experimental(BaseModel):
    "Experimental features"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    assistive_prompt: Optional[str] = None
    "The assistive system prompt for the tool router session"
    custom_toolkits: Optional[list[ExperimentalCustomToolkit]] = None
    "User-defined custom toolkits with grouped tools (no-auth)"
    custom_tools: Optional[list[ExperimentalCustomTool]] = None
    "Custom tools — standalone or extending Composio toolkits"
    no_elicitation_support_fallback: Literal["deny", "allow"] | None = None
    source_session_config: CurrentExperimentalSourceSessionConfig | None = None


class Mcp(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal['http']
    "The type of the MCP server. Can be http"
    url: str
    "The URL of the MCP server"


class Warning(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    code: Literal['PRELOAD_TOOLS_HIGH_CONTEXT_USAGE']
    "Stable machine code identifying the advisory. Safe to switch on in client code."
    message: str
    "Human-readable description of the advisory.\n\nSuitable for logging or surfacing to end users."


class SessionRetrieveResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    config: Config
    "The configuration used to create this session"
    config_version: int
    "Monotonic version of the config.\n\nIncremented on each PATCH. Use for optimistic concurrency control."
    experimental: Optional[Experimental] = None
    "Experimental features"
    mcp: Mcp
    session_id: str
    "The identifier of the session"
    tool_router_tools: list[str]
    "List of available tools in this session"
    warnings: Optional[list[Warning]] = None
    "Advisory list — the session exists and is usable, but the listed issues may\nwarrant attention."


ConfigToolkits: TypeAlias = Union[ConfigToolkitsEnabled, ConfigToolkitsDisabled, ConfigToolkitsRequireApproval]

ConfigTools: TypeAlias = Union[ConfigToolsEnabled, ConfigToolsDisabled, ConfigToolsTags, ConfigToolsRequireApproval]

__all__ = [
    "SessionRetrieveResponse",
    "Config",
    "ConfigExecute",
    "ConfigPreload",
    "ConfigSearch",
    "ConfigManageConnections",
    "ConfigMultiAccount",
    "ConfigTags",
    "ConfigToolkits",
    "ConfigToolkitsEnabled",
    "ConfigToolkitsDisabled",
    "ConfigTools",
    "ConfigToolsEnabled",
    "ConfigToolsDisabled",
    "ConfigToolsTags",
    "ConfigToolsTagsTags",
    "ConfigWorkbench",
    "Mcp",
    "Experimental",
    "ExperimentalCustomToolkit",
    "ExperimentalCustomToolkitTool",
    "ExperimentalCustomTool",
    "Warning",
    "ConfigToolkitsRequireApproval",
    "ConfigToolsRequireApproval",
    "CurrentConfigInstantVariant1ToolkitsVariant0",
    "CurrentConfigInstantVariant1ToolkitsVariant1",
    "CurrentConfigInstantVariant1ToolsValueVariant0",
    "CurrentConfigInstantVariant1ToolsValueVariant1",
    "CurrentConfigInstantVariant1",
    "CurrentConfigProxyExecute",
    "CurrentConfigHookVariant0AppliesToVariant1",
    "CurrentConfigHookVariant0Handler",
    "CurrentConfigHookVariant0",
    "CurrentConfigHookVariant1AppliesToVariant1",
    "CurrentConfigHookVariant1HandlerVariant0",
    "CurrentConfigHookVariant1HandlerVariant1",
    "CurrentConfigHookVariant1",
    "CurrentExperimentalSourceSessionConfig",
]
