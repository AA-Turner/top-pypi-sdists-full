"""GitHub Copilot CLI MCP lookup and tool-name resolution."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterator, Mapping, cast

from runlayer_cli.hook import hook_io
from runlayer_cli.hook.mcp_types import MCPServer

GITHUB_COPILOT_CLI_BUILTIN_SOURCE = "github-copilot-cli-built-in"
GITHUB_COPILOT_CLI_MAX_TOOL_NAME_LENGTH = 64
GITHUB_COPILOT_CLI_BUILTIN_MCP_SERVERS: frozenset[str] = frozenset(
    {
        "github-mcp-server",
        "playwright",
        "fetch",
        "time",
        "computer-use",
    }
)

_GITHUB_COPILOT_CLI_INSTALLED_PLUGINS_RELATIVE = ".copilot/installed-plugins"
_GITHUB_COPILOT_CLI_PLUGIN_MANIFEST_PATHS = (
    ".plugin/plugin.json",
    "plugin.json",
    ".github/plugin/plugin.json",
    ".claude-plugin/plugin.json",
)
_GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG_FIELDS = (
    "additional_mcp_config",
    "additionalMcpConfig",
    "additional_mcp_configs",
    "additionalMcpConfigs",
)
_GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG_ENV_VARS = (
    "RUNLAYER_GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG",
    "GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG",
    "COPILOT_ADDITIONAL_MCP_CONFIG",
)


def lookup_github_copilot_cli_mcp_server(
    server_name: str,
    cwd: str,
    payload: Mapping[str, Any] | None = None,
    *,
    home_path: Path | None = None,
) -> MCPServer | None:
    """Resolve a GitHub Copilot CLI MCP server from session, project, plugin, or user config."""
    for servers in _github_copilot_cli_session_mcp_servers(payload):
        result = _search_server_map(servers, server_name)
        if result is not None:
            return result

    for path, key in _github_copilot_cli_mcp_config_paths(cwd, home_path):
        result = _search_file_key(path, server_name, key)
        if result is not None:
            return result
    return _github_copilot_cli_builtin_server(server_name)


def resolve_github_copilot_cli_mcp_tool(
    tool_name: str,
    cwd: str,
    payload: Mapping[str, Any] | None = None,
    *,
    home_path: Path | None = None,
) -> tuple[str, MCPServer] | None:
    """Resolve ``<server-name>-<tool>`` Copilot CLI MCP tool names."""
    if not is_github_copilot_cli_mcp_tool_name_shape(tool_name):
        return None

    for servers in _github_copilot_cli_session_mcp_servers(payload):
        result = _resolve_github_copilot_cli_configured_mcp_tool(tool_name, servers)
        if result is not None:
            return result

    for path, key in _github_copilot_cli_mcp_config_paths(cwd, home_path):
        servers = _read_json_servers(path, key)
        if not servers:
            continue

        result = _resolve_github_copilot_cli_configured_mcp_tool(tool_name, servers)
        if result is not None:
            return result

    for server_name in _github_copilot_cli_builtin_candidates():
        if tool_name.startswith(f"{server_name}-"):
            server = _github_copilot_cli_builtin_server(server_name)
            if server is not None:
                return server_name, server

    return None


def resolve_github_copilot_cli_mcp_source_from_payload(
    tool_name: str,
    input_data: Mapping[str, Any] | None,
    *,
    home_path: Path | None = None,
) -> tuple[str, MCPServer] | None:
    if input_data is None:
        return None
    cwd = input_data.get("cwd", "") or hook_io.getcwd()
    if not isinstance(cwd, str):
        cwd = hook_io.getcwd()
    return resolve_github_copilot_cli_mcp_tool(
        tool_name,
        cwd,
        input_data,
        home_path=home_path,
    )


def github_copilot_cli_tool_resolves_mcp_source(
    tool_name: str,
    input_data: Mapping[str, Any] | None,
    *,
    home_path: Path | None = None,
) -> bool:
    if (
        resolve_github_copilot_cli_mcp_source_from_payload(
            tool_name,
            input_data,
            home_path=home_path,
        )
        is not None
    ):
        return True
    return is_github_copilot_cli_mcp_tool_name_shape(tool_name)


def is_github_copilot_cli_mcp_tool_name_shape(tool_name: str) -> bool:
    return "-" in tool_name or _github_copilot_cli_is_truncated_tool_name(tool_name)


def github_copilot_cli_has_session_mcp_config(
    payload: Mapping[str, Any] | None = None,
) -> bool:
    return any(_github_copilot_cli_additional_mcp_config_values(payload))


def _copilot_home_root() -> Path | None:
    """``COPILOT_HOME`` as a path anchored at the request cwd, or ``None``."""
    user_root = hook_io.getenv("COPILOT_HOME")
    if not user_root:
        return None
    return Path(hook_io.abspath(user_root))


def _github_copilot_cli_mcp_config_paths(
    cwd: str,
    home_path: Path | None,
) -> Iterator[tuple[Path, str]]:
    user_root = _copilot_home_root()
    user_config = (
        user_root / "mcp-config.json"
        if user_root is not None
        else _home_path(home_path) / ".copilot" / "mcp-config.json"
    )
    yield Path(cwd) / ".mcp.json", "mcpServers"
    yield Path(cwd) / ".github" / "mcp.json", "mcpServers"
    yield Path(cwd) / ".vscode" / "mcp.json", "servers"
    yield from _github_copilot_cli_plugin_mcp_config_paths(home_path)
    yield user_config, "mcpServers"


def _github_copilot_cli_plugin_mcp_config_paths(
    home_path: Path | None,
) -> Iterator[tuple[Path, str]]:
    plugins_base = _github_copilot_cli_installed_plugins_base(home_path)
    if plugins_base is None or not plugins_base.is_dir():
        return

    plugin_dirs = tuple(_github_copilot_cli_installed_plugin_dirs(plugins_base))
    for plugin_dir in reversed(plugin_dirs):
        manifest_paths = tuple(
            _github_copilot_cli_plugin_manifest_mcp_config_paths(plugin_dir)
        )
        if manifest_paths:
            yield from manifest_paths
            continue
        yield plugin_dir / ".mcp.json", "mcpServers"
        yield plugin_dir / ".github" / "mcp.json", "mcpServers"


def _github_copilot_cli_plugin_manifest_mcp_config_paths(
    plugin_dir: Path,
) -> Iterator[tuple[Path, str]]:
    for manifest_rel in _GITHUB_COPILOT_CLI_PLUGIN_MANIFEST_PATHS:
        manifest_path = plugin_dir / manifest_rel
        manifest = _read_json_object(manifest_path)
        if manifest is None:
            continue

        mcp_servers = manifest.get("mcpServers")
        if isinstance(mcp_servers, str) and mcp_servers:
            yield (
                _github_copilot_cli_plugin_component_path(plugin_dir, mcp_servers),
                "mcpServers",
            )
        elif isinstance(mcp_servers, dict) and mcp_servers:
            yield manifest_path, "mcpServers"
        return


def _github_copilot_cli_plugin_component_path(
    plugin_dir: Path,
    component_path: str,
) -> Path:
    expanded = component_path.replace("${PLUGIN_ROOT}", str(plugin_dir))
    path = Path(expanded).expanduser()
    if path.is_absolute():
        return path
    return plugin_dir / path


def _github_copilot_cli_installed_plugins_base(home_path: Path | None) -> Path | None:
    user_root = _copilot_home_root()
    if user_root is not None:
        return user_root / "installed-plugins"
    if sys.platform == "win32":
        profile = hook_io.getenv("USERPROFILE")
        if not profile:
            return None
        return Path(profile) / _GITHUB_COPILOT_CLI_INSTALLED_PLUGINS_RELATIVE
    return _home_path(home_path) / _GITHUB_COPILOT_CLI_INSTALLED_PLUGINS_RELATIVE


def _github_copilot_cli_installed_plugin_dirs(
    plugins_base: Path,
) -> Iterator[Path]:
    for marketplace_dir in _iter_child_dirs(plugins_base):
        if marketplace_dir.name == "_direct":
            continue
        yield from _iter_child_dirs(marketplace_dir)
    yield from _iter_child_dirs(plugins_base / "_direct")


def _github_copilot_cli_server_prefix_sort_key(server_name: str) -> int:
    return max(
        len(server_name),
        len(_github_copilot_cli_sanitize_tool_name_part(server_name)),
    )


def _github_copilot_cli_tool_matches_server(tool_name: str, server_name: str) -> bool:
    prefixes = {
        f"{server_name}-",
        f"{_github_copilot_cli_sanitize_tool_name_part(server_name)}-",
    }
    return any(tool_name.startswith(prefix) for prefix in prefixes)


def _resolve_github_copilot_cli_configured_mcp_tool(
    tool_name: str,
    servers: Mapping[object, Any],
) -> tuple[str, MCPServer] | None:
    candidates = [name for name in servers if isinstance(name, str)]
    candidates.sort(key=_github_copilot_cli_server_prefix_sort_key, reverse=True)

    for server_name in candidates:
        if not _github_copilot_cli_tool_matches_server(tool_name, server_name):
            continue
        server = _extract_server_by_key(servers, server_name)
        if server is not None:
            return server_name, server

    for prefix in _github_copilot_cli_truncated_tool_prefixes(tool_name):
        matches: list[tuple[str, MCPServer]] = []
        for server_name in candidates:
            sanitized_server = _github_copilot_cli_sanitize_tool_name_part(server_name)
            if not sanitized_server.startswith(prefix):
                continue
            server = _extract_server_by_key(servers, server_name)
            if server is not None:
                matches.append((server_name, server))
        if len(matches) == 1:
            return matches[0]

    return None


def _github_copilot_cli_is_truncated_tool_name(tool_name: str) -> bool:
    return len(tool_name) == GITHUB_COPILOT_CLI_MAX_TOOL_NAME_LENGTH


def _github_copilot_cli_truncated_tool_prefixes(tool_name: str) -> tuple[str, ...]:
    if not _github_copilot_cli_is_truncated_tool_name(tool_name):
        return ()

    prefixes = [tool_name]
    stripped_suffix = tool_name.rstrip("0123456789")
    if stripped_suffix != tool_name and len(stripped_suffix) >= 60:
        prefixes.append(stripped_suffix)
    return tuple(dict.fromkeys(prefixes))


def _github_copilot_cli_sanitize_tool_name_part(name: str) -> str:
    parts: list[str] = []
    for char in name:
        if char.isascii() and (char.isalnum() or char in "-_"):
            parts.append(char)
        elif char.isascii():
            parts.append("-")
        else:
            parts.append(char.encode("punycode").decode("ascii"))
    return "".join(parts)


def _github_copilot_cli_builtin_candidates() -> list[str]:
    candidates = list(GITHUB_COPILOT_CLI_BUILTIN_MCP_SERVERS)
    candidates.sort(key=lambda server_name: len(server_name), reverse=True)
    return candidates


def _github_copilot_cli_builtin_server(server_name: str) -> MCPServer | None:
    if server_name not in GITHUB_COPILOT_CLI_BUILTIN_MCP_SERVERS:
        return None
    return {
        "name": server_name,
        "source": GITHUB_COPILOT_CLI_BUILTIN_SOURCE,
    }


def _github_copilot_cli_session_mcp_servers(
    payload: Mapping[str, Any] | None,
) -> Iterator[Mapping[object, Any]]:
    for value in _github_copilot_cli_additional_mcp_config_values(payload):
        yield from _github_copilot_cli_mcp_server_maps_from_value(value)


def _github_copilot_cli_additional_mcp_config_values(
    payload: Mapping[str, Any] | None,
) -> Iterator[object]:
    if payload is not None:
        for field in _GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG_FIELDS:
            value = payload.get(field)
            if value:
                yield value

        for tool_field in ("tool_input", "toolArgs"):
            tool_args = payload.get(tool_field)
            if isinstance(tool_args, dict):
                for field in _GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG_FIELDS:
                    value = tool_args.get(field)
                    if value:
                        yield value

    for env_var in _GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG_ENV_VARS:
        value = hook_io.getenv(env_var)
        if value:
            yield value


def _github_copilot_cli_mcp_server_maps_from_value(
    value: object,
) -> Iterator[Mapping[object, Any]]:
    if isinstance(value, list):
        for item in value:
            yield from _github_copilot_cli_mcp_server_maps_from_value(item)
        return

    if isinstance(value, dict):
        data = cast(dict[object, Any], value)
        servers = data.get("mcpServers") or data.get("servers")
        if isinstance(servers, dict):
            yield cast(Mapping[object, Any], servers)
        elif all(isinstance(item, dict) for item in data.values()):
            yield cast(Mapping[object, Any], data)
        return

    if not isinstance(value, str):
        return

    text = value.strip()
    if not text:
        return

    data: dict[str, Any] | None
    if text.startswith("@"):
        expanded_path = Path(text[1:]).expanduser()
        data = _read_json_object(Path(hook_io.abspath(str(expanded_path))))
    else:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return
        data = parsed if isinstance(parsed, dict) else None

    if data is not None:
        yield from _github_copilot_cli_mcp_server_maps_from_value(data)


def _search_file_key(path: Path, server_name: str, key: str) -> MCPServer | None:
    servers = _read_json_servers(path, key)
    return _search_server_map(servers, server_name)


def _search_server_map(
    servers: Mapping[object, Any],
    server_name: str,
) -> MCPServer | None:
    result = _extract_server(servers, server_name)
    if result is not None:
        return result

    normalized_server_name = _normalized_name(server_name)
    for candidate_name in servers:
        if (
            isinstance(candidate_name, str)
            and _normalized_name(candidate_name) == normalized_server_name
        ):
            return _extract_server_by_key(servers, candidate_name)
    return None


def _read_json_servers(path: Path, key: str) -> Mapping[object, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    servers = data.get(key, {})
    if not isinstance(servers, dict):
        return {}
    return cast(Mapping[object, Any], servers)


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
    url = server.get("url") or server.get("serverUrl") or server.get("uri")
    if url:
        return MCPServer(url=str(url))
    command = server.get("command") or server.get("cmd")
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


def _iter_child_dirs(path: Path) -> Iterator[Path]:
    try:
        children = sorted(path.iterdir())
    except OSError:
        return
    for child in children:
        if child.is_dir():
            yield child


def _home_path(home_path: Path | None) -> Path:
    return home_path if home_path is not None else Path.home()


def _normalized_name(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())
