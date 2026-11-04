# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_execute_params."""

from __future__ import annotations

from typing import Dict, Iterable, Literal, Optional

from typing_extensions import NotRequired, Required, TypedDict


class CurrentInputResponsesValue(TypedDict, total=False):
    "The user's answer to one question, in the shape of an MCP elicitation result (https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)."

    action: Required[Literal["accept", "decline", "cancel"]]
    "`accept` when the user submitted the form, `decline` when they said no, `cancel` when they dismissed it"
    content: NotRequired[dict[str, object | None]]
    "With `accept`, the user's answer: fields matching the question's `requested_schema`"


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


class Experimental(TypedDict, total=False):
    "Inline custom tools and toolkits for this request.\n\nv3.1 sessions do not persist customs — pass them on every request that needs them."

    custom_toolkits: Iterable[ExperimentalCustomToolkit]
    "Custom toolkits with grouped tools.\n\nToolkit slugs must not conflict with existing Composio toolkits. All tools are\nno-auth."
    custom_tools: Iterable[ExperimentalCustomTool]
    "Custom tools to include in search.\n\nStandalone tools need no auth. Tools with extends_toolkit inherit the Composio\ntoolkit's connection."


class SessionExecuteParams(TypedDict, total=False):
    tool_slug: Required[str]
    "The unique slug identifier of the tool to execute.\n\nSupports both meta tools and app tools exposed by the session."
    arguments: Dict[str, Optional[object]]
    "The arguments required by the tool"
    account: str
    "Account identifier to specify which connected account to use for direct tool\nexecution. Use the account ID (e.g. \"coup_hurricane_dal_analytical\") or an\nalias. When omitted with a single account, the default is used. When omitted\nwith multiple accounts, an error lists available accounts. Meta/helper tools\neither ignore this top-level field or define their own account-selection fields,\nfor example COMPOSIO_MULTI_EXECUTE_TOOL.tools[].account."
    enable_auto_workbench_offload: bool
    "When true, direct non-meta tool execution may return a workbench offload preview\nif the response exceeds the configured threshold and the session workbench is\nenabled. When omitted or false, direct tool execution returns the normal inline\nresponse. Meta/helper tools are unaffected, and COMPOSIO_MULTI_EXECUTE_TOOL uses\nsession.workbench configuration for its own batch-level offload behavior."
    input_responses: NotRequired[dict[str, CurrentInputResponsesValue]]
    request_state: NotRequired[str]
    experimental: Experimental
    "Inline custom tools and toolkits for this request.\n\nv3.1 sessions do not persist customs — pass them on every request that needs\nthem."


__all__ = [
    "SessionExecuteParams",
    "Experimental",
    "ExperimentalCustomToolkit",
    "ExperimentalCustomToolkitTool",
    "ExperimentalCustomTool",
    "CurrentInputResponsesValue",
]
