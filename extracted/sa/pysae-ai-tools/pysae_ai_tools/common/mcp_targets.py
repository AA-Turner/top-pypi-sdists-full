"""Per-assistant MCP config stores (Claude JSON + Codex TOML).

Every ``McpTool.build_config()`` returns a single canonical stdio dict —
``{"command": ..., "args": [...], "env": {...}}``. Each assistant CLI persists that
same information in its own file and format:

- Claude Code → ``mcpServers.<name>`` in ``~/.claude.json`` (JSON)
- Codex       → ``[mcp_servers.<name>]`` in ``~/.codex/config.toml`` (TOML)

An :class:`McpStore` knows only how to upsert, read and remove a server from its own
file given that canonical dict. Assistant identity (name, CLI binary, presence,
which store belongs to which assistant) lives on :class:`~.assistants.Assistant`;
:func:`~.assistants.active_assistants` selects the assistants present on the machine.
"""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import tomlkit
from tomlkit.exceptions import TOMLKitError

from . import mcp
from .fs import atomic_write_text

# Keys of the canonical build_config() dict that every stdio MCP server carries. Anything
# else (e.g. Claude's ``type: "stdio"``) is target-specific and dropped when serializing
# to a store that infers the transport from ``command``.
_STDIO_KEYS = ("command", "args", "env")

# Codex groups its MCP servers under this top-level TOML table.
_CODEX_SERVERS_TABLE = "mcp_servers"


class McpStore(ABC):
    """One assistant's MCP config store (Claude's JSON, Codex's TOML, …)."""

    @abstractmethod
    def config_path(self) -> Path:
        """Absolute path of the config file this store writes to."""

    @abstractmethod
    def upsert(self, server_name: str, config: dict[str, Any]) -> bool:
        """Add or update ``server_name`` from a canonical config dict. True when changed."""

    @abstractmethod
    def get(self, server_name: str) -> dict[str, Any] | None:
        """Return the stored config for ``server_name`` as a plain dict, or None."""

    @abstractmethod
    def remove(self, server_name: str) -> bool:
        """Remove ``server_name``. True when it was present and removed."""


class ClaudeMcpStore(McpStore):
    """Claude Code's ``mcpServers`` block in ``~/.claude.json`` (canonical source format).

    Thin adapter over :mod:`.mcp`, the private JSON store implementation — the only module
    that imports :mod:`.mcp` directly.
    """

    def config_path(self) -> Path:
        return mcp.settings_path()

    def upsert(self, server_name: str, config: dict[str, Any]) -> bool:
        return mcp.upsert_server(server_name, config)

    def get(self, server_name: str) -> dict[str, Any] | None:
        return mcp.get_server(server_name)

    def remove(self, server_name: str) -> bool:
        return mcp.remove_server(server_name)


def codex_config_path() -> Path:
    """Codex reads its config from ``$CODEX_HOME/config.toml`` (default ``~/.codex``)."""
    home = os.environ.get("CODEX_HOME")
    base = Path(home) if home else Path.home() / ".codex"
    return base / "config.toml"


class CodexMcpStore(McpStore):
    """Codex's ``[mcp_servers.<name>]`` tables in ``~/.codex/config.toml``.

    Only the stdio triplet ``command``/``args``/``env`` is written — Codex infers the stdio
    transport from ``command`` and has no ``type`` key. Reads and writes go through
    ``tomlkit`` so existing tables and comments in the file are preserved.
    """

    def config_path(self) -> Path:
        return codex_config_path()

    def _payload(self, config: dict[str, Any]) -> dict[str, Any]:
        return {key: config[key] for key in _STDIO_KEYS if key in config}

    def _load(self) -> tomlkit.TOMLDocument:
        path = self.config_path()
        if not path.exists() or path.stat().st_size == 0:
            return tomlkit.document()
        try:
            return tomlkit.parse(path.read_text(encoding="utf-8"))
        except TOMLKitError as exc:
            raise ValueError(f"{path} is not valid TOML: {exc}") from exc

    def _servers(self, doc: tomlkit.TOMLDocument) -> Any:
        table = doc.get(_CODEX_SERVERS_TABLE)
        return table if isinstance(table, dict) else None

    def get(self, server_name: str) -> dict[str, Any] | None:
        servers = self._servers(self._load())
        if servers is None:
            return None
        entry = servers.get(server_name)
        if entry is None:
            return None
        unwrapped = entry.unwrap() if hasattr(entry, "unwrap") else entry
        return dict(unwrapped) if isinstance(unwrapped, dict) else None

    def upsert(self, server_name: str, config: dict[str, Any]) -> bool:
        payload = self._payload(config)
        doc = self._load()
        servers = self._servers(doc)
        if servers is None:
            servers = tomlkit.table(is_super_table=True)
            doc[_CODEX_SERVERS_TABLE] = servers
        existing = servers.get(server_name)
        if existing is not None:
            current = existing.unwrap() if hasattr(existing, "unwrap") else existing
            if current == payload:
                return False
        servers[server_name] = payload
        atomic_write_text(self.config_path(), tomlkit.dumps(doc))
        return True

    def remove(self, server_name: str) -> bool:
        doc = self._load()
        servers = self._servers(doc)
        if servers is None or server_name not in servers:
            return False
        del servers[server_name]
        atomic_write_text(self.config_path(), tomlkit.dumps(doc))
        return True
