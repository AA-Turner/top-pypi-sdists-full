"""Register LangGraph tool catalogs at compile time."""

from __future__ import annotations

import logging
from typing import Any

from aigie.decision.tool_catalog import register_catalog

logger = logging.getLogger(__name__)

_HASH_ATTR = "_aigie_tool_registry_hash"


def _tools_from_node(spec: Any) -> list[Any]:
    """Return ToolNode tools from a graph node spec."""
    runnable = getattr(spec, "runnable", spec)
    tools_by_name = getattr(runnable, "tools_by_name", None)
    if isinstance(tools_by_name, dict):
        return list(tools_by_name.values())
    return []


def _collect_graph_tools(graph: Any) -> list[Any]:
    nodes = getattr(graph, "nodes", None)
    if not isinstance(nodes, dict):
        return []
    tools: list[Any] = []
    for spec in nodes.values():
        tools.extend(_tools_from_node(spec))
    return tools


def register_graph_tools(graph: Any, app: Any) -> None:
    """Register graph tools and stash the hash on ``app``."""
    try:
        tools = _collect_graph_tools(graph)
        if not tools:
            return
        catalog_hash = register_catalog(tools)
        if catalog_hash:
            setattr(app, _HASH_ATTR, catalog_hash)
    except Exception:  # noqa: BLE001 — never break compile
        logger.debug("langgraph tool-catalog registration failed", exc_info=True)


def stashed_hash(app: Any) -> str | None:
    """Return the tool catalog hash stashed on ``app``."""
    value = getattr(app, _HASH_ATTR, None)
    return value if isinstance(value, str) else None
