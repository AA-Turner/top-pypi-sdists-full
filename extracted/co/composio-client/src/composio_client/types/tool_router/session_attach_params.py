# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_attach_params."""

from __future__ import annotations

from typing import Dict, Iterable, Optional

from typing_extensions import Required, TypedDict


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


class SessionAttachParams(TypedDict, total=False):
    experimental: Experimental
    "Inline custom tools and toolkits for this request.\n\nv3.1 sessions do not persist customs — pass them on every request that needs\nthem."


__all__ = [
    "SessionAttachParams",
    "Experimental",
    "ExperimentalCustomToolkit",
    "ExperimentalCustomToolkitTool",
    "ExperimentalCustomTool",
]
