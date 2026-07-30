"""Tool extraction and catalog registration for query events."""

from __future__ import annotations

import logging
from typing import Any

from aigie.decision.tool_catalog import stamp_tool_registry_hash

logger = logging.getLogger(__name__)


def extract_tool_defs(tools: list[Any] | None) -> tuple[list[str], list[dict[str, Any]]]:
    """Return names and serializable definitions for every tool."""
    names: list[str] = []
    definitions: list[dict[str, Any]] = []
    for t in tools or []:
        if hasattr(t, "name"):
            names.append(t.name)
            tool_def: dict[str, Any] = {"name": t.name}
            if hasattr(t, "description"):
                tool_def["description"] = t.description
            if hasattr(t, "input_schema"):
                tool_def["input_schema"] = t.input_schema
            elif hasattr(t, "parameters"):
                tool_def["parameters"] = t.parameters
            definitions.append(tool_def)
        elif isinstance(t, dict) and "name" in t:
            names.append(t["name"])
            definitions.append(t)
    return names, definitions


def stamp_catalog(
    tool_definitions: list[dict[str, Any]],
    metadata: dict[str, Any],
    trace_id: str | None = None,
) -> None:
    """Attach available tools and their catalog hash to run metadata."""
    if not tool_definitions:
        return
    metadata["available_tools"] = tool_definitions
    stamp_tool_registry_hash(tool_definitions, metadata, trace_id)


def _sdk_server_instance(config: Any) -> Any:
    """Return the in-process MCP ``Server`` for an SDK server config, else None."""
    if isinstance(config, dict) and config.get("type") == "sdk":
        return config.get("instance")
    return None


async def _list_sdk_server_tools(instance: Any) -> list[tuple[str, str]]:
    """Return ``(name, description)`` for each tool an SDK MCP server exposes."""
    from mcp.types import ListToolsRequest

    handler = getattr(instance, "request_handlers", {}).get(ListToolsRequest)
    if handler is None:
        return []
    result = await handler(ListToolsRequest(method="tools/list"))
    tools = getattr(getattr(result, "root", None), "tools", None) or []
    return [(t.name, getattr(t, "description", "") or "") for t in tools]


async def extract_mcp_tool_defs(
    mcp_servers: Any, allowed_tools: list[str] | None
) -> list[dict[str, Any]]:
    """Build ``{name, description}`` defs from SDK MCP servers, with
    ``allowed_tools`` names as a fallback for built-ins (Task/Read/...).

    Real CAS agents define tools via ``create_sdk_mcp_server(...)`` +
    ``ClaudeAgentOptions(mcp_servers=..., allowed_tools=[...])``, leaving
    ``options.tools`` empty. Fail-open: any failure yields a partial (or
    empty) catalog rather than raising.
    """
    defs: list[dict[str, Any]] = []
    seen: set[str] = set()
    servers = mcp_servers.items() if isinstance(mcp_servers, dict) else []
    for namespace, config in servers:
        instance = _sdk_server_instance(config)
        if instance is None:
            continue
        try:
            tools = await _list_sdk_server_tools(instance)
        except Exception:  # noqa: BLE001
            logger.debug("failed to list MCP server tools for %s", namespace, exc_info=True)
            continue
        for name, description in tools:
            qualified = f"mcp__{namespace}__{name}"
            if qualified not in seen:
                seen.add(qualified)
                defs.append({"name": qualified, "description": description})
    for name in allowed_tools or []:
        if name not in seen:
            seen.add(name)
            defs.append({"name": name})
    return defs


async def resolve_tool_defs(options: Any, explicit_tools: list[Any]) -> list[Any]:
    """Return explicit tools plus MCP-server / allowed_tools defs, deduped by name."""
    try:
        mcp_defs = await extract_mcp_tool_defs(
            getattr(options, "mcp_servers", None),
            getattr(options, "allowed_tools", None),
        )
    except Exception:  # noqa: BLE001
        logger.debug("MCP tool extraction failed", exc_info=True)
        mcp_defs = []
    if not explicit_tools:
        return mcp_defs
    seen: set[str] = set()
    for tool in explicit_tools:
        if hasattr(tool, "name"):
            seen.add(tool.name)
        elif isinstance(tool, dict) and tool.get("name") is not None:
            seen.add(tool["name"])
    return explicit_tools + [d for d in mcp_defs if d.get("name") not in seen]
