"""Private JSON store for Claude Code's ``~/.claude.json`` MCP server config.

Implementation detail of :class:`~.mcp_targets.ClaudeMcpStore` — the only module that
imports this one. Every other consumer goes through the store / :class:`~.assistants.Assistant`
abstraction, never this module directly.
"""

import json
from pathlib import Path
from typing import Any

from .fs import atomic_write_text

# Default location of the Claude Code user config (where mcpServers lives)
DEFAULT_SETTINGS_PATH = Path.home() / ".claude.json"


def settings_path() -> Path:
    return DEFAULT_SETTINGS_PATH


def load(path: Path | None = None) -> dict[str, Any]:
    """Load the settings file, or return {} when missing/empty.

    Always reads as UTF-8 — Claude Code writes ``~/.claude.json`` in
    UTF-8, but on Windows ``Path.read_text()`` defaults to ``cp1252``
    and chokes on the first non-ASCII byte ("'charmap' codec can't
    decode byte 0x.. in position N").
    """
    p = path or settings_path()
    if not p.exists() or p.stat().st_size == 0:
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save(settings: dict[str, Any], path: Path | None = None) -> None:
    """Atomically write settings back to disk (always UTF-8)."""
    p = path or settings_path()
    atomic_write_text(p, json.dumps(settings, indent=2) + "\n")


def get_server(name: str, settings: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Return the config block for an MCP server, or None if not configured."""
    s = settings if settings is not None else load()
    servers = s.get("mcpServers", {})
    if not isinstance(servers, dict):
        return None
    server = servers.get(name)
    return server if isinstance(server, dict) else None


def upsert_server(name: str, config: dict[str, Any], path: Path | None = None) -> bool:
    """Add or update an MCP server entry. Returns True when settings changed."""
    settings = load(path)
    servers = settings.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise ValueError("settings.json `mcpServers` must be an object")
    existing = servers.get(name)
    if existing == config:
        return False
    servers[name] = config
    save(settings, path)
    return True


def remove_server(name: str, path: Path | None = None) -> bool:
    """Remove an MCP server entry. Returns True when removed."""
    settings = load(path)
    servers = settings.get("mcpServers", {})
    if not isinstance(servers, dict) or name not in servers:
        return False
    del servers[name]
    save(settings, path)
    return True
