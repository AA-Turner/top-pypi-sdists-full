"""MCP server lookup for clients that expose MCP tools via PreToolUse.

Claude Code search order:
  1. ${cwd}/.mcp.json              — project-scoped servers
  2. ~/.claude.json projects[cwd]  — per-project servers in user state
  3. ~/.claude.json mcpServers     — global user-scoped servers
  4. ~/.claude/plugins/installed_plugins.json — enabled native plugins

Codex search order mirrors runlayer-hook.sh:
  1. ~/.codex/config.toml
  2. ~/.codex/managed_config.toml
  3. /etc/codex/managed_config.toml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterator, Mapping, TypedDict, cast

import yaml

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


class MCPServer(TypedDict, total=False):
    url: str
    command: str


class ClaudePluginInstallation(TypedDict):
    root: Path
    settings_cwd: str
    specificity: int


def lookup_mcp_server(server_name: str, cwd: str) -> MCPServer | None:
    """Resolve *server_name* to a URL or command string.

    Returns None if the server is not found in any config file.
    """
    project_mcp = Path(cwd) / ".mcp.json"
    result = _search_file(project_mcp, server_name)
    if result is not None:
        return result

    claude_json = Path.home() / ".claude.json"
    if claude_json.is_file():
        try:
            data = json.loads(claude_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

        project_servers = data.get("projects", {}).get(cwd, {}).get("mcpServers", {})
        result = _extract_server(project_servers, server_name)
        if result is not None:
            return result

        global_servers = data.get("mcpServers", {})
        result = _extract_server(global_servers, server_name)
        if result is not None:
            return result

    result = _search_claude_code_plugin_servers(server_name, cwd)
    if result is not None:
        return result

    return None


def lookup_codex_mcp_server(server_name: str) -> MCPServer | None:
    """Resolve a Codex MCP server name from Codex TOML config files."""
    for path in _codex_mcp_config_paths():
        result = _search_codex_toml_file(path, server_name)
        if result is not None:
            return result
    return None


def resolve_hermes_mcp_tool(tool_name: str) -> tuple[str, MCPServer] | None:
    """Resolve a Hermes MCP tool name to its configured MCP server.

    Hermes tool names use a single-underscore ``mcp_<server>_<tool>`` shape.
    Server names may contain punctuation, so match by the longest normalized
    configured server-name prefix after ``mcp_``.
    """
    if not tool_name.startswith("mcp_"):
        return None

    servers = _read_hermes_mcp_servers()
    normalized_tool_name = _normalized_name(tool_name.removeprefix("mcp_"))
    candidates = [name for name in servers if _normalized_name(str(name))]
    candidates.sort(key=lambda name: len(_normalized_name(str(name))), reverse=True)

    for candidate_name in candidates:
        normalized_candidate = _normalized_name(str(candidate_name))
        if not normalized_tool_name.startswith(normalized_candidate):
            continue
        server = _extract_server_by_key(servers, candidate_name)
        if server is not None:
            return str(candidate_name), server
    return None


def lookup_cursor_mcp_server(
    server_name: str, payload: Mapping[str, Any]
) -> MCPServer | None:
    """Resolve a Cursor beforeMCPExecution server display name.

    Cursor can send only a server display name in ``command``. Mirror the
    shell hook by searching workspace .cursor/mcp.json files, then the global
    ~/.cursor/mcp.json, with Cursor's user- prefix and normalized-name fallback.
    """
    for path in _cursor_mcp_config_paths(payload):
        result = _search_cursor_file(path, server_name)
        if result is not None:
            return result
    return None


def resolve_cursor_before_mcp_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a Cursor MCP payload with display-name command resolved if found."""
    server_name = payload.get("command")
    if not isinstance(server_name, str) or not server_name or payload.get("url"):
        return payload

    server = lookup_cursor_mcp_server(server_name, payload)
    if server is None:
        return payload

    resolved = dict(payload)
    url = server.get("url")
    command = server.get("command")
    if url:
        resolved["url"] = url
        resolved.pop("command", None)
    elif command:
        resolved["command"] = command
        resolved.pop("url", None)
    return resolved


def _search_file(path: Path, server_name: str) -> MCPServer | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return _extract_server(data.get("mcpServers", {}), server_name)


def _cursor_mcp_config_paths(payload: Mapping[str, Any]) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()

    def add_path(root: object) -> None:
        if isinstance(root, str) and root:
            path = Path(root) / ".cursor" / "mcp.json"
            if path not in seen:
                seen.add(path)
                paths.append(path)

    workspace_roots = payload.get("workspace_roots")
    if isinstance(workspace_roots, list):
        for root in workspace_roots:
            add_path(root)
    add_path(payload.get("cwd"))

    home_path = Path.home() / ".cursor" / "mcp.json"
    if home_path not in seen:
        paths.append(home_path)
    return paths


def _codex_mcp_config_paths() -> tuple[Path, ...]:
    return (
        Path.home() / ".codex" / "config.toml",
        Path.home() / ".codex" / "managed_config.toml",
        Path("/etc/codex/managed_config.toml"),
    )


def _read_hermes_mcp_servers() -> dict[object, Any]:
    path = Path.home() / ".hermes" / "config.yaml"
    if not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(data, dict):
        return {}
    servers = data.get("mcp_servers", {})
    if isinstance(servers, dict):
        return cast(dict[object, Any], servers)
    return {}


def _search_codex_toml_file(path: Path, server_name: str) -> MCPServer | None:
    if not path.is_file():
        return None
    try:
        with path.open("rb") as fb:
            data = tomllib.load(fb)
    except (OSError, tomllib.TOMLDecodeError):
        return None

    servers = data.get("mcp_servers", {})
    if not isinstance(servers, dict):
        return None

    result = _extract_server(servers, server_name)
    if result is not None:
        return result

    normalized_server_name = _normalized_name(server_name)
    for candidate_name in servers:
        if (
            isinstance(candidate_name, str)
            and _normalized_name(candidate_name) == normalized_server_name
        ):
            result = _extract_server(servers, candidate_name)
            if result is not None:
                return result
    return None


def _search_cursor_file(path: Path, server_name: str) -> MCPServer | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    servers = data.get("mcpServers", {})
    if not isinstance(servers, dict):
        return None

    lookup_names = [server_name]
    if server_name.startswith("user-"):
        lookup_names.append(server_name.removeprefix("user-"))

    for lookup_name in lookup_names:
        result = _extract_server(servers, lookup_name)
        if result is not None:
            return result

    for lookup_name in lookup_names:
        normalized_lookup_name = _normalized_name(lookup_name)
        for candidate_name in servers:
            if (
                isinstance(candidate_name, str)
                and _normalized_name(candidate_name) == normalized_lookup_name
            ):
                result = _extract_server(servers, candidate_name)
                if result is not None:
                    return result

    return None


def _normalized_name(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def _extract_server(servers: object, server_name: str) -> MCPServer | None:
    if not isinstance(servers, dict):
        return None
    entry = cast(dict[object, Any], servers).get(server_name)
    return _extract_server_entry(entry)


def _extract_server_by_key(servers: object, server_key: object) -> MCPServer | None:
    if not isinstance(servers, dict):
        return None
    entry = cast(dict[object, Any], servers).get(server_key)
    return _extract_server_entry(entry)


def _extract_server_entry(entry: object) -> MCPServer | None:
    if not entry or not isinstance(entry, dict):
        return None
    server = cast(dict[str, Any], entry)
    # Different MCP clients spell the remote endpoint differently:
    #   url        — Claude Code, Cursor, .mcp.json spec
    #   serverUrl  — Windsurf
    #   uri        — Goose
    # Match the bash hook (runlayer-hook.sh) so Python and shell agree.
    url = server.get("url") or server.get("serverUrl") or server.get("uri")
    if url:
        return MCPServer(url=str(url))
    command = server.get("command")
    if command:
        args = server.get("args", [])
        full = f"{command} {' '.join(str(a) for a in args)}".strip()
        return MCPServer(command=full)
    return None


def _read_json_object(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _claude_plugin_lookup_names(server_name: str, plugin_name: str) -> list[str]:
    prefix = f"plugin_{plugin_name}_"
    if server_name.startswith("plugin_"):
        if not server_name.startswith(prefix):
            return []
        names = []
        suffix = server_name.removeprefix(prefix)
        if suffix:
            names.append(suffix)
        names.append(server_name)
        return names
    return [server_name]


def _claude_enabled_plugins(settings_cwd: str) -> dict[str, bool]:
    enabled_plugins: dict[str, bool] = {}
    for path in (
        Path.home() / ".claude" / "settings.json",
        Path(settings_cwd) / ".claude" / "settings.json",
        Path(settings_cwd) / ".claude" / "settings.local.json",
    ):
        settings = _read_json_object(path) or {}
        enabled = settings.get("enabledPlugins")
        if isinstance(enabled, dict):
            enabled_plugins.update(
                {
                    str(key): value if isinstance(value, bool) else True
                    for key, value in enabled.items()
                }
            )
    return enabled_plugins


def _claude_settings_cwd(cwd: str) -> str:
    path = Path(cwd).resolve()
    for candidate in (path, *path.parents):
        claude_dir = candidate / ".claude"
        if (claude_dir / "settings.json").is_file() or (
            claude_dir / "settings.local.json"
        ).is_file():
            return str(candidate)
    return cwd


def _search_claude_plugin_root(
    plugin_root: Path, server_name: str, plugin_name: str
) -> MCPServer | None:
    manifest = _read_json_object(plugin_root / ".claude-plugin" / "plugin.json") or {}
    manifest_mcp_servers = manifest.get("mcpServers")

    for lookup_name in _claude_plugin_lookup_names(server_name, plugin_name):
        if isinstance(manifest_mcp_servers, dict):
            result = _extract_server(manifest_mcp_servers, lookup_name)
            if result is not None:
                return result
        elif isinstance(manifest_mcp_servers, str):
            path = Path(manifest_mcp_servers)
            if not path.is_absolute():
                path = plugin_root / path
            result = _search_file(path, lookup_name)
            if result is not None:
                return result

        result = _search_file(plugin_root / ".mcp.json", lookup_name)
        if result is not None:
            return result

    return None


def _search_claude_code_plugin_servers(server_name: str, cwd: str) -> MCPServer | None:
    for plugin_root, plugin_name in _claude_plugin_roots(cwd):
        result = _search_claude_plugin_root(plugin_root, server_name, plugin_name)
        if result is not None:
            return result
    return None


def _claude_plugin_roots(cwd: str) -> Iterator[tuple[Path, str]]:
    registry = _read_json_object(
        Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    )
    if registry is None:
        return
    plugins = registry.get("plugins")
    if not isinstance(plugins, dict):
        return

    for plugin_key, raw_installations in plugins.items():
        if isinstance(plugin_key, str) and isinstance(raw_installations, list):
            plugin_name = plugin_key.rsplit("@", 1)[0]
            installations = []
            for raw_installation in raw_installations:
                installation = _claude_plugin_installation(raw_installation, cwd)
                if installation is not None:
                    installations.append(installation)

            for installation in sorted(
                installations,
                key=lambda candidate: candidate["specificity"],
                reverse=True,
            ):
                enabled = _claude_enabled_plugins(installation["settings_cwd"])
                if enabled.get(plugin_key) is not False:
                    yield installation["root"], plugin_name


def _claude_plugin_installation(
    raw_installation: object, cwd: str
) -> ClaudePluginInstallation | None:
    if not isinstance(raw_installation, dict):
        return None
    installation = cast(dict[str, Any], raw_installation)
    settings_cwd = _claude_settings_cwd(cwd)
    specificity = 0
    scope = installation.get("scope")
    project_path = installation.get("projectPath")
    if isinstance(project_path, str) and project_path:
        project_root = Path(project_path).resolve()
        if not Path(cwd).resolve().is_relative_to(project_root):
            return None
        settings_cwd = str(project_root)
        specificity = 2 if scope == "local" else 1
    install_path = installation.get("installPath")
    if not isinstance(install_path, str) or not install_path:
        return None
    return {
        "root": Path(install_path),
        "settings_cwd": settings_cwd,
        "specificity": specificity,
    }
