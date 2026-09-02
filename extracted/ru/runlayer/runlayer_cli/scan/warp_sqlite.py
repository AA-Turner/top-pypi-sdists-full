"""Read Warp's sqlite database for in-app gallery MCP server installations.

Warp stores MCP servers added through its in-app gallery / "+ Add" flow in a
sqlite database (``warp.sqlite``), table ``mcp_server_installations``. These are
not always mirrored to ``~/.warp/.mcp.json`` (parsed by the standard file-based
client definition), so this module supplements that file config with the sqlite
source and merges both into a single global ``warp`` config.

Each row holds an installation JSON blob whose ``template.json`` field is itself a
JSON string mapping server name -> server definition (standard MCP
``command``/``args``/``env`` or ``url``/``headers`` shape). String fields may
contain ``{{var}}`` placeholders resolved from a separate variable-values column.

Path templates (incl. Stable/Preview channels and WSL resolution) live on the
``warp`` ``MCPClientDefinition.sqlite_paths`` in ``clients.py`` — the single
declarative source of truth for Warp install locations.

stdlib plus the RE2 ``regex_safe`` wrapper (no
``mcp``/``fastmcp``/``anyio``/``questionary``) so the module is
safe inside the ``aiwatch`` PyInstaller bundle closure.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import structlog

from runlayer_cli import regex_safe
from runlayer_cli.scan.clients import get_client_by_name
from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    parse_server_entry,
)

logger = structlog.get_logger(__name__)

_TABLE = "mcp_server_installations"
# STDLIB_WS, not `\s`: RE2's `\s` is ASCII-only and narrowing it here fails
# OPEN. Padding a name with a non-breaking space would leave the capture as
# "\xa0NAME\xa0", miss the variable-values lookup, and emit the placeholder
# unresolved into the scanned config.
_VARIABLE_PATTERN = regex_safe.compile(
    r"\{\{" + regex_safe.STDLIB_WS + r"*([^}]+?)" + regex_safe.STDLIB_WS + r"*\}\}"
)
_INSTALLATION_COLUMN = "installation"
_VARIABLE_VALUES_COLUMN = "variable_values"


def _warp_sqlite_paths() -> list[Path]:
    """Return candidate ``warp.sqlite`` paths from the warp client definition."""
    warp = get_client_by_name("warp")
    if warp is None:
        return []
    return warp.get_resolved_sqlite_paths()


def _open_readonly(path: Path) -> sqlite3.Connection | None:
    """Open *path* read-only without locking a running Warp instance.

    ``mode=ro`` avoids creating the file; ``immutable=1`` skips locking so a live
    Warp process (WAL active) doesn't block the read. Returns None on failure.
    """
    try:
        return sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)
    except sqlite3.Error as e:
        logger.debug("Failed to open warp sqlite", path=str(path), error=str(e))
        return None


def _looks_like_installation(value: Any) -> bool:
    return isinstance(value, dict) and "template" in value


def _row_disabled(row: sqlite3.Row) -> bool:
    """True when the row carries an explicit falsy ``enabled`` flag.

    Resolved by column name (``sqlite3.Row``) rather than cell shape. A missing
    column or NULL counts as enabled, matching ``COALESCE(enabled, 1) <> 0``.
    """
    if "enabled" not in row.keys():
        return False
    value = row["enabled"]
    if value is None:
        return False
    return not value


def _looks_like_variable_values(value: Any) -> bool:
    if not isinstance(value, dict) or not value:
        return False
    return all(
        isinstance(v, dict) and "value" in v and "variable_type" in v
        for v in value.values()
    )


def _decode_cell(cell: Any) -> Any:
    """JSON-decode a row cell if it is a string, else return None."""
    if not isinstance(cell, str):
        return None
    try:
        return json.loads(cell)
    except (ValueError, TypeError):
        return None


def _build_variable_map(variable_values: dict[str, Any] | None) -> dict[str, str]:
    """Map ``{{var}}`` name -> resolved string value."""
    result: dict[str, str] = {}
    if not variable_values:
        return result
    for key, entry in variable_values.items():
        if isinstance(entry, dict):
            value = entry.get("value")
            if isinstance(value, str):
                result[key] = value
    return result


def _substitute(value: Any, variables: dict[str, str]) -> Any:
    """Recursively replace ``{{var}}`` placeholders in string fields.

    Unknown variables are left as-is so the server is still recorded.
    """
    if isinstance(value, str):
        return _VARIABLE_PATTERN.sub(
            lambda m: variables.get(m.group(1), m.group(0)), value
        )
    if isinstance(value, list):
        return [_substitute(item, variables) for item in value]
    if isinstance(value, dict):
        return {k: _substitute(v, variables) for k, v in value.items()}
    return value


def _column_or_sniff(row: sqlite3.Row, column: str, predicate: Any) -> Any:
    """Decode a row value by column name, falling back to shape sniffing.

    Prefers the named column (stable once Warp's schema settles); if it's
    absent or doesn't match *predicate*, scans every cell by shape. Sniffing is
    the fallback only, so a stray column with a similar shape can't shadow the
    real one when the named column is present and valid.
    """
    keys = row.keys()
    if column in keys:
        decoded = _decode_cell(row[column])
        if predicate(decoded):
            return decoded
    for key in keys:
        decoded = _decode_cell(row[key])
        if predicate(decoded):
            return decoded
    return None


def _parse_installation_row(row: sqlite3.Row) -> list[MCPServerConfig]:
    """Parse one ``mcp_server_installations`` row into server configs.

    Resolves the installation blob and variable-values dict by their expected
    column names (``installation`` / ``variable_values``), falling back to
    shape sniffing for schema drift. Disabled-row filtering happens in the scan
    loop (see ``_row_disabled``), so every row reaching here is treated as
    enabled.
    """
    installation = _column_or_sniff(row, _INSTALLATION_COLUMN, _looks_like_installation)
    variable_values = _column_or_sniff(
        row, _VARIABLE_VALUES_COLUMN, _looks_like_variable_values
    )

    if installation is None:
        return []

    template = installation.get("template")
    if not isinstance(template, dict):
        return []
    inner_raw = template.get("json")
    if not isinstance(inner_raw, str):
        return []
    try:
        inner = json.loads(inner_raw)
    except (ValueError, TypeError):
        return []
    if not isinstance(inner, dict):
        return []

    variables = _build_variable_map(variable_values)
    servers: list[MCPServerConfig] = []
    for name, server_def in inner.items():
        if not isinstance(server_def, dict):
            continue
        resolved = _substitute(server_def, variables)
        try:
            servers.append(parse_server_entry(str(name), resolved))
        except Exception as e:
            logger.warning(
                "Failed to parse warp sqlite server entry",
                server_name=name,
                error=str(e),
            )
    return servers


def _read_db_servers(db_path: Path) -> list[MCPServerConfig]:
    """Read enabled MCP servers from a single ``warp.sqlite`` file.

    Returns an empty list on any failure (missing table, corrupt db, locked
    file) so a scan never breaks on one bad db.
    """
    conn = _open_readonly(db_path)
    if conn is None:
        return []

    conn.row_factory = sqlite3.Row
    servers: list[MCPServerConfig] = []
    try:
        cursor = conn.execute(f"SELECT * FROM {_TABLE}")  # noqa: S608 (fixed table)
        for row in cursor.fetchall():
            if _row_disabled(row):
                continue
            servers.extend(_parse_installation_row(row))
    except sqlite3.Error as e:
        logger.debug("Failed to query warp sqlite", path=str(db_path), error=str(e))
        return []
    finally:
        conn.close()

    return servers


def scan_warp_sqlite() -> MCPClientConfig | None:
    """Scan Warp's sqlite db(s) for MCP server installations.

    Reads MCP servers from **all** existing candidate dbs (e.g. both the Stable
    and Preview channels) and merges them with ``config_hash`` dedup, so a
    gallery server present only in a second channel isn't silently dropped.
    ``config_path`` reports the first db that contributed servers.

    Returns an ``MCPClientConfig`` (client="warp", global scope) when servers are
    found, else None.
    """
    merged: list[MCPServerConfig] = []
    seen_hashes: set[str] = set()
    source_path: str | None = None

    for db_path in _warp_sqlite_paths():
        if not db_path.exists():
            continue

        db_servers = _read_db_servers(db_path)
        if not db_servers:
            continue

        if source_path is None:
            source_path = str(db_path)

        added = 0
        for server in db_servers:
            if server.config_hash not in seen_hashes:
                merged.append(server)
                seen_hashes.add(server.config_hash)
                added += 1

        logger.info(
            "Found MCP servers in Warp sqlite",
            path=str(db_path),
            server_count=len(db_servers),
            added=added,
        )

    if not merged:
        return None

    return MCPClientConfig(
        client="warp",
        config_path=source_path,
        config_scope="global",
        servers=merged,
    )


def _merge_into_global_warp(
    configurations: list[MCPClientConfig],
    sqlite_config: MCPClientConfig,
) -> None:
    """Merge sqlite-sourced Warp servers into the configurations list in place.

    If a global Warp config already exists (from ``~/.warp/.mcp.json``), append
    only the sqlite servers whose ``config_hash`` isn't already present so a
    server defined in both sources is counted once. Otherwise append the sqlite
    config as a new entry.
    """
    existing = next(
        (
            c
            for c in configurations
            if c.client == "warp" and c.config_scope == "global"
        ),
        None,
    )
    if existing is None:
        configurations.append(sqlite_config)
        return

    seen_hashes = {s.config_hash for s in existing.servers}
    for server in sqlite_config.servers:
        if server.config_hash not in seen_hashes:
            existing.servers.append(server)
            seen_hashes.add(server.config_hash)


def enrich_configurations_with_warp_sqlite(
    configurations: list[MCPClientConfig],
) -> None:
    """Supplement Warp's file config with its in-app gallery sqlite installs.

    The single orchestration entry point: scans the sqlite db(s) and merges the
    result into the global ``warp`` config in *configurations* (in place). No-op
    when no sqlite-sourced servers are found.
    """
    sqlite_config = scan_warp_sqlite()
    if sqlite_config and sqlite_config.servers:
        _merge_into_global_warp(configurations, sqlite_config)
