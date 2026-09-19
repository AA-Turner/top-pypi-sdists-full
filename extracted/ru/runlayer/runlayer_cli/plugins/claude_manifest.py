from __future__ import annotations

from pathlib import Path
from typing import Any

from runlayer_cli.safe_parse import parse_json, parse_json5

PLUGIN_MANIFEST = Path(".claude-plugin/plugin.json")
PLUGIN_MCP_JSON = Path(".mcp.json")


def load_plugin_manifest(manifest_path: Path) -> dict[str, Any] | None:
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except (ValueError, OSError):
        return None
    raw = parse_json(text)["value"]
    if not isinstance(raw, dict):
        return None
    return raw


def resolve_plugin_mcp_config(
    plugin_root: Path,
) -> tuple[dict[str, Any] | None, Path | None]:
    manifest_path = plugin_root / PLUGIN_MANIFEST
    manifest = load_plugin_manifest(manifest_path)
    if manifest is not None:
        mcp_servers = manifest.get("mcpServers")
        if isinstance(mcp_servers, dict) and mcp_servers:
            return {"mcpServers": mcp_servers}, manifest_path

    mcp_path = plugin_root / PLUGIN_MCP_JSON
    if not mcp_path.exists():
        return None, None

    try:
        text = mcp_path.read_text(encoding="utf-8")
    except (ValueError, OSError):
        return None, mcp_path
    raw = parse_json5(text)["value"]
    if not isinstance(raw, dict):
        return None, mcp_path
    return raw, mcp_path
