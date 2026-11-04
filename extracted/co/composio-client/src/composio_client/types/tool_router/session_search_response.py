# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_search_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import ConfigDict, Field
from ..._base_model import BaseModel


class ResultReferenceWorkbenchSnippet(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    code: str
    "Python code snippet for the workbench"
    description: str
    "Description of what the code snippet does"


class Result(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    difficulty: Optional[str] = None
    "Task difficulty assessment (e.g., \"easy - Simple single-tool operation with\nknown parameters\")"
    error: Optional[str] = None
    "Error message if the search for this query failed, null otherwise.\n\nAlways present for failed queries."
    execution_guidance: Optional[str] = None
    "Guidance message about the search results, particularly when a cached plan is\navailable"
    index: float
    "1-based index of the query in the request"
    known_pitfalls: Optional[list[str]] = None
    "Common pitfalls and considerations (only present when cached plan is available)"
    memory: Optional[Dict[str, list[str]]] = None
    "Memory data relevant to this query, grouped by app.\n\nOnly present for non-cached search results."
    plan_id: Optional[str] = None
    "ID of cached plan if available"
    primary_tool_slugs: list[str]
    "List of main tool slugs matching the search criteria"
    recommended_plan_steps: Optional[list[str]] = None
    "Workflow steps from cached plan (only present when cached plan is available)"
    reference_workbench_snippets: Optional[list[ResultReferenceWorkbenchSnippet]] = None
    "Reference Python code snippets for processing tool responses in the workbench\n(only present when cached plan is available)"
    related_tool_slugs: list[str]
    "List of related tool slugs that might be useful"
    toolkits: list[str]
    "List of unique toolkit slugs used by tools in this query"
    use_case: str
    "The use case that was searched"
    cached_plan_usecase: str | None = None


class Session(BaseModel):
    "Session info for correlating meta tool calls"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    generate_id: bool
    "Whether a fresh session id was generated in this call."
    id: str
    "Session identifier to be passed to subsequent meta tool calls as session_id."
    instructions: str
    "LLM-facing guidance on how to reuse this session id"


class TimeInfo(BaseModel):
    "Time information for the query"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_time_utc: str
    "Current time in ISO format (UTC)"
    current_time_utc_epoch_seconds: float
    "Current time as Unix epoch timestamp in seconds"
    message: str
    "Important message about time handling and timezone considerations"


class ToolSchemasSchemaRefArgs(BaseModel):
    "Arguments to pass to the tool"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    tool_slugs: list[str]
    "Tool slugs to fetch schemas for"


class ToolSchemasSchemaRef(BaseModel):
    "Reference to fetch full schema when hasFullSchema is false"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    args: ToolSchemasSchemaRefArgs
    "Arguments to pass to the tool"
    message: Optional[str] = None
    "Instruction message for the LLM"
    tool: Literal['COMPOSIO_GET_TOOL_SCHEMAS']
    "Tool to call"


class ToolSchemas(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    description: Optional[str] = None
    "Description of the tool"
    has_full_schema: Optional[bool] = Field(default=None, alias="hasFullSchema")
    "Whether the full input_schema is included in this response"
    input_schema: Optional[Dict[str, Optional[object]]] = None
    "Input schema for the tool (only present when hasFullSchema is true)"
    output_schema: Optional[Dict[str, Optional[object]]] = None
    "Output/response schema for the tool.\n\nOnly included when include_output_schemas is true."
    schema_ref: Optional[ToolSchemasSchemaRef] = Field(default=None, alias="schemaRef")
    "Reference to fetch full schema when hasFullSchema is false"
    tool_slug: str
    "The slug of the tool"
    toolkit: str
    "The slug of the toolkit that provides this tool"


class ToolkitConnectionStatusAccount(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_type: Optional[Literal['PRIVATE', 'SHARED']] = None
    "Sharing model for this connected account.\n\nPRIVATE is owner-only; SHARED is reachable from a tool-router session only when\nexplicitly pinned."
    alias: Optional[str] = None
    "User-assigned alias for this account"
    created_at: str
    "ISO 8601 timestamp of when the account was connected"
    id: str
    "Unique identifier for this account"
    is_default: bool
    "Whether this is the default account for the toolkit"
    status: str
    "Connection status (e.g., \"active\")"
    user_info: Optional[Dict[str, Optional[object]]] = None
    "Information about the connected user (email, name, etc.)"


class CurrentToolkitConnectionStatusInstantAccountPricesValue(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    description: str | None = None
    discount: str | None = None


class CurrentToolkitConnectionStatusInstantAccount(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allowed_tool_slugs: list[str]
    prices: dict[str, CurrentToolkitConnectionStatusInstantAccountPricesValue] | None = None


class ToolkitConnectionStatus(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_selection: Optional[Literal['required']] = None
    "When \"required\", the agent must specify which account to use.\n\nPresent only when multiple accounts exist."
    account_type: Optional[Literal['PRIVATE', 'SHARED']] = None
    "Sharing model for the connected account when has_active_connection is true.\n\nPRIVATE is owner-only; SHARED is reachable only when explicitly pinned to the\nsession."
    accounts: Optional[list[ToolkitConnectionStatusAccount]] = None
    "List of connected accounts for this toolkit.\n\nPresent when multi-account is enabled."
    connection_details: Optional[Dict[str, Optional[object]]] = None
    "Connection details including auth config and connected account IDs.\n\nOnly present when has_active_connection is true."
    current_user_info: Optional[Dict[str, Optional[object]]] = None
    "Information about the currently connected user (email, name, etc.)"
    description: str
    "Description of what the toolkit does and its capabilities"
    has_active_connection: bool
    "Whether an active connection exists for this toolkit"
    status_message: str
    "Human-readable message about the connection status and next steps"
    toolkit: str
    "The toolkit slug identifier (e.g., \"gmail\", \"slack\")"
    instant_account: CurrentToolkitConnectionStatusInstantAccount | None = None


class SessionSearchResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    error: Optional[str] = None
    "Error message if any searches failed, null if all succeeded.\n\nFormat: \"X out of Y searches failed, reasons: <details>\""
    next_steps_guidance: list[str]
    "Combined workflow guidance covering connections, planner, and memory usage.\n\nEach element is a step instruction."
    results: list[Result]
    "Per-query search results with tools, reasoning, and memory.\n\nOne entry per query in request order."
    session: Session
    "Session info for correlating meta tool calls"
    success: bool
    "Whether all searches completed successfully. False if any query failed."
    time_info: TimeInfo
    "Time information for the query"
    tool_schemas: Dict[str, ToolSchemas]
    "Deduplicated tool definitions keyed by tool_slug for O(1) lookup.\n\nEach tool appears once even if used in multiple queries."
    toolkit_connection_statuses: list[ToolkitConnectionStatus]
    "Connection status for all toolkits mentioned across all queries, with\ndescriptions merged in."


__all__ = [
    "SessionSearchResponse",
    "Result",
    "ResultReferenceWorkbenchSnippet",
    "Session",
    "TimeInfo",
    "ToolSchemas",
    "ToolSchemasSchemaRef",
    "ToolSchemasSchemaRefArgs",
    "ToolkitConnectionStatus",
    "ToolkitConnectionStatusAccount",
    "CurrentToolkitConnectionStatusInstantAccountPricesValue",
    "CurrentToolkitConnectionStatusInstantAccount",
]
