# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_config_history_response."""

from __future__ import annotations

import datetime
from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict
from ..._base_model import BaseModel


class ItemConfigExecute(BaseModel):
    "Execute helper configuration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable_multi_execute: Optional[bool] = None


class ItemConfigManageConnections(BaseModel):
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


class ItemConfigMultiAccount(BaseModel):
    "Multi-account configuration for this session."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable: Optional[bool] = None
    "When true, enables multi-account mode for this session.\n\nWhen not set, falls back to org/project-level configuration."
    max_accounts_per_toolkit: Optional[int] = None
    "Maximum number of connected accounts allowed per toolkit.\n\nDefaults to 5 when multi-account is enabled."
    require_explicit_selection: Optional[bool] = None
    "When true, require explicit account selection when multiple accounts are\nconnected. When false (default), use the first/default account."


class ItemConfigPreload(BaseModel):
    "Preload configuration.\n\nExplicit slugs are returned as an array; dynamic preload is returned as \"all\"."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    tools: Union[list[str], Literal['all']]
    "Explicit preloaded tool slugs, or \"all\" when the session dynamically exposes all\napp tools allowed by its filters."


class ItemConfigSearch(BaseModel):
    "Search helper configuration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable: Optional[bool] = None


class ItemConfigTags(BaseModel):
    "MCP tool annotation hints for filtering tools with enabled/disabled support.\n\nenabled: tags that the tool must have at least one of. disabled: tags that the tool must NOT have any of. Both conditions must be satisfied."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must NOT have any of"
    enabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must have at least one of"
    require_approval: list[Literal["readOnlyHint", "createHint", "updateHint", "destructiveHint", "idempotentHint", "openWorldHint"]] | None = None


class ItemConfigToolkitsEnabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]
    require_approval: list[str] | None = None


class ItemConfigToolkitsDisabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]
    require_approval: list[str] | None = None


class ItemConfigToolkitsRequireApproval(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    require_approval: list[str]
    "Tool calls matched here pause until the user approves them."


class ItemConfigToolsEnabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]
    require_approval: list[str] | None = None


class ItemConfigToolsDisabled(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]
    require_approval: list[str] | None = None


class ItemConfigToolsTagsTags(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must NOT have any of"
    enabled: Optional[list[Literal["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", "createHint", "updateHint"]]] = None
    "Tags that the tool must have at least one of"
    require_approval: list[Literal["readOnlyHint", "createHint", "updateHint", "destructiveHint", "idempotentHint", "openWorldHint"]] | None = None


class ItemConfigToolsTags(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    tags: ItemConfigToolsTagsTags
    require_approval: list[str] | None = None


class ItemConfigToolsRequireApproval(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    require_approval: list[str]
    "Tool calls matched here pause until the user approves them."


class ItemConfigWorkbench(BaseModel):
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


class CurrentItemConfigInstantVariant1ToolkitsVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]


class CurrentItemConfigInstantVariant1ToolkitsVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]


class CurrentItemConfigInstantVariant1ToolsValueVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enabled: list[str]


class CurrentItemConfigInstantVariant1ToolsValueVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    disabled: list[str]


class CurrentItemConfigInstantVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    toolkits: CurrentItemConfigInstantVariant1ToolkitsVariant0 | CurrentItemConfigInstantVariant1ToolkitsVariant1 | None = None
    tools: dict[str, CurrentItemConfigInstantVariant1ToolsValueVariant0 | CurrentItemConfigInstantVariant1ToolsValueVariant1] | None = None
    return_instant_charge: bool
    return_prices_in_search: bool


class CurrentItemConfigProxyExecute(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    enable: bool


class CurrentItemConfigHookVariant0AppliesToVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    toolkits: list[str]


class CurrentItemConfigHookVariant0Handler(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["condition_check"]
    condition: str
    action: Literal["block"]


class CurrentItemConfigHookVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["before_execute"]
    id: str
    name: str | None = None
    applies_to: Literal["all"] | CurrentItemConfigHookVariant0AppliesToVariant1
    handler: CurrentItemConfigHookVariant0Handler


class CurrentItemConfigHookVariant1AppliesToVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    toolkits: list[str]


class CurrentItemConfigHookVariant1HandlerVariant0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["condition_check"]
    condition: str
    action: Literal["block"]


class CurrentItemConfigHookVariant1HandlerVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["prompt_injection_check"]
    action: Literal["block"]


class CurrentItemConfigHookVariant1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    type: Literal["after_execute"]
    id: str
    name: str | None = None
    applies_to: Literal["all"] | CurrentItemConfigHookVariant1AppliesToVariant1
    handler: CurrentItemConfigHookVariant1HandlerVariant0 | CurrentItemConfigHookVariant1HandlerVariant1


class ItemConfig(BaseModel):
    "The session configuration at this version"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_configs: Optional[Dict[str, str]] = None
    "Auth config overrides per toolkit"
    connected_accounts: Optional[Dict[str, list[str]]] = None
    "Per-toolkit connected account overrides (array of nano-IDs).\n\nMulti-account sessions can pin more than one account per toolkit; otherwise\nlength is 1."
    execute: ItemConfigExecute
    "Execute helper configuration"
    manage_connections: Optional[ItemConfigManageConnections] = None
    "Manage connections configuration"
    multi_account: Optional[ItemConfigMultiAccount] = None
    "Multi-account configuration for this session."
    preload: ItemConfigPreload
    "Preload configuration.\n\nExplicit slugs are returned as an array; dynamic preload is returned as \"all\"."
    search: ItemConfigSearch
    "Search helper configuration"
    tags: Optional[ItemConfigTags] = None
    "MCP tool annotation hints for filtering tools with enabled/disabled support.\n\nenabled: tags that the tool must have at least one of. disabled: tags that the\ntool must NOT have any of. Both conditions must be satisfied."
    toolkits: Union[ItemConfigToolkitsEnabled, ItemConfigToolkitsDisabled, ItemConfigToolkitsRequireApproval, None] = None
    "Toolkit configuration - either enabled list or disabled list"
    tools: Optional[Dict[str, Union[ItemConfigToolsEnabled, ItemConfigToolsDisabled, ItemConfigToolsTags, ItemConfigToolsRequireApproval]]] = None
    "Tool-level configuration per toolkit"
    user_id: str
    "User identifier for this session"
    workbench: Optional[ItemConfigWorkbench] = None
    "Workbench configuration"
    instant: Literal[False] | CurrentItemConfigInstantVariant1
    proxy_execute: CurrentItemConfigProxyExecute | None = None
    hooks: list[CurrentItemConfigHookVariant0 | CurrentItemConfigHookVariant1] | None = None


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    config: ItemConfig
    "The session configuration at this version"
    created_at: datetime.datetime
    "ISO timestamp.\n\nFor history rows, when the entry was archived (i.e. the moment the version was\nsuperseded by a PATCH)."
    is_current: bool
    "True only for the live (current) session config, present on the first page.\n\nFalse for archived history rows."
    version: int
    "The config version this entry represents"


class SessionConfigHistoryResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


ItemConfigToolkits: TypeAlias = Union[ItemConfigToolkitsEnabled, ItemConfigToolkitsDisabled, ItemConfigToolkitsRequireApproval]

ItemConfigTools: TypeAlias = Union[ItemConfigToolsEnabled, ItemConfigToolsDisabled, ItemConfigToolsTags, ItemConfigToolsRequireApproval]

__all__ = [
    "SessionConfigHistoryResponse",
    "Item",
    "ItemConfig",
    "ItemConfigExecute",
    "ItemConfigPreload",
    "ItemConfigSearch",
    "ItemConfigManageConnections",
    "ItemConfigMultiAccount",
    "ItemConfigTags",
    "ItemConfigToolkits",
    "ItemConfigToolkitsEnabled",
    "ItemConfigToolkitsDisabled",
    "ItemConfigTools",
    "ItemConfigToolsEnabled",
    "ItemConfigToolsDisabled",
    "ItemConfigToolsTags",
    "ItemConfigToolsTagsTags",
    "ItemConfigWorkbench",
    "ItemConfigToolkitsRequireApproval",
    "ItemConfigToolsRequireApproval",
    "CurrentItemConfigInstantVariant1ToolkitsVariant0",
    "CurrentItemConfigInstantVariant1ToolkitsVariant1",
    "CurrentItemConfigInstantVariant1ToolsValueVariant0",
    "CurrentItemConfigInstantVariant1ToolsValueVariant1",
    "CurrentItemConfigInstantVariant1",
    "CurrentItemConfigProxyExecute",
    "CurrentItemConfigHookVariant0AppliesToVariant1",
    "CurrentItemConfigHookVariant0Handler",
    "CurrentItemConfigHookVariant0",
    "CurrentItemConfigHookVariant1AppliesToVariant1",
    "CurrentItemConfigHookVariant1HandlerVariant0",
    "CurrentItemConfigHookVariant1HandlerVariant1",
    "CurrentItemConfigHookVariant1",
]
