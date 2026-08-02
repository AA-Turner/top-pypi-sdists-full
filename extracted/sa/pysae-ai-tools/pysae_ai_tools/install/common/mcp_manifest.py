"""Generation and inspection of Pysae plugin MCP manifests.

The native Claude and Codex plugins declare their MCP servers in a ``.mcp.json`` at
the plugin root. Every entry is the **secret-free shim** — ``pysae-ai-tools mcp run
<server>`` — which resolves secrets at launch and execs the real server. This module
is the single source of that file: it builds the manifest from the user's selected
MCP servers and reads back which servers a deployed plugin declares.
"""

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from ...config import get_tools_to_install
from ..registry import TOOLS, Category, _instance
from .base import SHIM_BINARY

MCP_MANIFEST_NAME = ".mcp.json"


def _shim_entry(server_name: str) -> dict[str, Any]:
    return {"type": "stdio", "command": SHIM_BINARY, "args": ["mcp", "run", server_name]}


def _mcp_tools() -> list[Any]:
    return [t for t in TOOLS if t.category is Category.MCP]


def selected_mcp_server_names() -> list[str]:
    """MCP server names to declare in the plugin manifest.

    Those of the MCP tools the user selected (saved selection), or — when no
    selection has been saved yet — the default-selected MCP tools. Mirrors the
    per-user opt-in the baked config used to honour: a plugin declaring every
    server would launch them all at activation (RAM)."""
    saved = get_tools_to_install()
    selected: set[str] | None = set(saved) if saved else None
    names: list[str] = []
    for t in _mcp_tools():
        if selected is None:
            if not t.default_selected:
                continue
        elif t.name not in selected:
            continue
        try:
            instance = _instance(t.module)
        except Exception:  # noqa: BLE001
            continue
        names.extend(instance.mcp_server_names())
    return names


def managed_server_names() -> list[str]:
    """Every MCP server name this package manages, regardless of selection.

    Used by migrations to strip legacy baked entries from assistant-level config
    after the native plugins take ownership."""
    names: list[str] = []
    for t in _mcp_tools():
        try:
            instance = _instance(t.module)
        except Exception:  # noqa: BLE001
            continue
        names.extend(instance.mcp_server_names())
    return names


def build_plugin_mcp_json(server_names: Iterable[str]) -> dict[str, Any]:
    """The ``.mcp.json`` document declaring ``server_names`` through the shim."""
    return {"mcpServers": {name: _shim_entry(name) for name in server_names}}


def deployed_plugin_servers(manifest_path: Path) -> set[str]:
    """Server names declared in a deployed plugin ``.mcp.json`` (empty if missing/invalid)."""
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    servers = data.get("mcpServers") if isinstance(data, dict) else None
    return set(servers) if isinstance(servers, dict) else set()
