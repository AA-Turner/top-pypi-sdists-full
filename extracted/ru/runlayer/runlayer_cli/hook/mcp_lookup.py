"""MCP server lookup for clients that expose MCP tools via PreToolUse."""

from __future__ import annotations

import json
import os
import platform
import sys
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, TypedDict, cast

import yaml

from runlayer_cli import regex_safe
from runlayer_cli.hook import hook_io
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    GITHUB_COPILOT_CLI_BUILTIN_MCP_SERVERS as GITHUB_COPILOT_CLI_BUILTIN_MCP_SERVERS,
)
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    GITHUB_COPILOT_CLI_BUILTIN_SOURCE as GITHUB_COPILOT_CLI_BUILTIN_SOURCE,
)
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    github_copilot_cli_has_session_mcp_config as _github_copilot_cli_has_session_mcp_config,
)
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    github_copilot_cli_tool_resolves_mcp_source as _github_copilot_cli_tool_resolves_mcp_source,
)
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    is_github_copilot_cli_mcp_tool_name_shape as is_github_copilot_cli_mcp_tool_name_shape,
)
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    lookup_github_copilot_cli_mcp_server as _lookup_github_copilot_cli_mcp_server,
)
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    resolve_github_copilot_cli_mcp_source_from_payload as _resolve_github_copilot_cli_mcp_source_from_payload,
)
from runlayer_cli.hook.copilot_cli_mcp_lookup import (
    resolve_github_copilot_cli_mcp_tool as _resolve_github_copilot_cli_mcp_tool,
)
from runlayer_cli.hook.mcp_types import MCPServer

# Top-level leaf (closure: ``json`` + ``regex_safe``). Deliberately NOT
# ``hook_install.tolerant_json`` -- that import runs ``hook_install/__init__.py``
# and pulls the MDM install stack into every hook process.
from runlayer_cli.tolerant_json import loads as tolerant_json_loads

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


_GOOSE_MCP_TRANSPORT_TYPES = frozenset({"stdio", "sse", "streamable_http"})
_GOOSE_LOCAL_EXTENSION_TYPES = frozenset({"platform", "builtin"})

# Claude Code claude.ai account connectors (Anthropic-hosted) carry no local
# URL/command -- the PreToolUse hook only exposes the tool name. Older
# ``mcp__claude_ai_<name>_<index>__<tool>`` namespaces are recorded (by display
# name) in ``~/.claude.json`` under ``claudeAiMcpEverConnected``. Resolve them
# to a source-tagged server the hook forwards as-is. Unlike the
# GitHub Copilot CLI built-in path (backend re-checks a frozenset), the backend
# has no connector registry to re-verify against, so this local resolution is
# the only gate. Keep aligned with backend hooks/cursor/router.py.
_CLAUDE_AI_CONNECTOR_SOURCE = "claude-ai-connector"
_CLAUDE_AI_CONNECTOR_PREFIX = "claude_ai_"


class ClaudePluginInstallation(TypedDict):
    root: Path
    settings_cwd: str
    specificity: int


def lookup_mcp_server(server_name: str, cwd: str) -> MCPServer | None:
    """Resolve *server_name* to a URL, command, or trusted source marker.

    Returns None when the server is not found or its source cannot be verified.
    """
    result = _search_file(_claude_managed_mcp_config_path(), server_name)
    if result is not None:
        return result

    claude_data = _read_json_object(Path.home() / ".claude.json")

    for root in _candidate_project_roots(cwd):
        result = _search_file(Path(root) / ".mcp.json", server_name)
        if result is not None:
            return result
        if claude_data is not None:
            project_servers = (
                claude_data.get("projects", {}).get(root, {}).get("mcpServers", {})
            )
            result = _extract_server(project_servers, server_name)
            if result is not None:
                return result

    if claude_data is not None:
        global_servers = claude_data.get("mcpServers", {})
        result = _extract_server(global_servers, server_name)
        if result is not None:
            return result

    result = _search_claude_code_plugin_servers(server_name, cwd)
    if result is not None:
        return result

    return _lookup_claude_ai_connector(server_name, claude_data)


def _lookup_claude_ai_connector(
    server_name: str, claude_data: dict[str, Any] | None
) -> MCPServer | None:
    """Resolve a claude.ai account-connector tool namespace to a source-tagged server.

    ``claude_ai_*`` namespaces are matched against the display names in
      ``~/.claude.json`` -> ``claudeAiMcpEverConnected``; an unlisted name
      fails closed.

    Returns a source-only ``MCPServer`` (no url/command). The hook forwards
    name + source, and the backend allows on that client-attested marker alone
    (claude_code client + source + non-empty name, see hooks/cursor/router.py
    ``_is_claude_ai_connector_mcp``) -- it does NOT re-verify the connector,
    so this resolution is the entire gate.
    """
    if not server_name.startswith(_CLAUDE_AI_CONNECTOR_PREFIX):
        return None

    if claude_data is None:
        return None
    connected = claude_data.get("claudeAiMcpEverConnected")
    if not isinstance(connected, list):
        return None

    candidates = {_normalized_name(server_name)}
    # Claude Code appends a ``_<index>`` disambiguation suffix (e.g. ``linear_2``);
    # match with it stripped too, but keep the un-stripped form for connectors whose
    # real name genuinely ends in a digit.
    base, sep, suffix = server_name.rpartition("_")
    if sep and suffix.isdigit() and base:
        candidates.add(_normalized_name(base))

    for entry in connected:
        if isinstance(entry, str) and _normalized_name(entry) in candidates:
            return MCPServer(name=entry, source=_CLAUDE_AI_CONNECTOR_SOURCE)
    return None


def lookup_vscode_mcp_server(server_name: str, cwd: str) -> MCPServer | None:
    """Resolve a VS Code MCP server from project or user mcp.json files."""
    for path in _vscode_mcp_config_paths(cwd):
        result = _search_file_key(path, server_name, "servers")
        if result is not None:
            return result
    return None


def lookup_github_copilot_cli_mcp_server(
    server_name: str, cwd: str, payload: Mapping[str, Any] | None = None
) -> MCPServer | None:
    return _lookup_github_copilot_cli_mcp_server(
        server_name,
        cwd,
        payload,
        home_path=Path.home(),
    )


def resolve_github_copilot_cli_mcp_tool(
    tool_name: str, cwd: str, payload: Mapping[str, Any] | None = None
) -> tuple[str, MCPServer] | None:
    return _resolve_github_copilot_cli_mcp_tool(
        tool_name,
        cwd,
        payload,
        home_path=Path.home(),
    )


def resolve_github_copilot_cli_mcp_source_from_payload(
    tool_name: str,
    input_data: Mapping[str, Any] | None,
) -> tuple[str, MCPServer] | None:
    return _resolve_github_copilot_cli_mcp_source_from_payload(
        tool_name,
        input_data,
        home_path=Path.home(),
    )


def github_copilot_cli_tool_resolves_mcp_source(
    tool_name: str,
    input_data: Mapping[str, Any] | None,
) -> bool:
    return _github_copilot_cli_tool_resolves_mcp_source(
        tool_name,
        input_data,
        home_path=Path.home(),
    )


def github_copilot_cli_has_session_mcp_config(
    payload: Mapping[str, Any] | None = None,
) -> bool:
    return _github_copilot_cli_has_session_mcp_config(payload)


def lookup_windsurf_mcp_server(server_name: str, cwd: str) -> MCPServer | None:
    """Resolve a Windsurf MCP server from workspace or Codeium-profile config."""
    for path in _windsurf_mcp_config_paths(cwd):
        result = _search_file(path, server_name)
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


def lookup_grok_cli_mcp_server(server_name: str, cwd: str) -> MCPServer | None:
    """Resolve Grok's ``<server>__<tool>`` namespace from native TOML config."""
    configured_home = hook_io.getenv("GROK_HOME")
    grok_home = (
        Path(configured_home).expanduser() if configured_home else Path.home() / ".grok"
    )
    paths = [Path("/etc/grok/requirements.toml"), grok_home / "requirements.toml"]
    paths.extend(
        Path(root) / ".grok" / "config.toml" for root in _candidate_project_roots(cwd)
    )
    paths.extend(
        (
            grok_home / "config.toml",
            grok_home / "managed_config.toml",
            Path("/etc/grok/managed_config.toml"),
        )
    )
    for path in paths:
        result = _search_codex_toml_file(path, server_name)
        if result is not None:
            return result
    # Grok imports Claude-compatible MCP configuration as a fallback.
    return lookup_mcp_server(server_name, cwd)


def lookup_devin_cli_mcp_server(server_name: str, cwd: str) -> MCPServer | None:
    """Resolve a Devin CLI MCP server: native config, then enabled imports.

    Devin also serves MCP servers imported from other tools, gated per source by
    ``read_config_from`` (every source enabled unless explicitly ``false``).
    Both halves of that matter here: searching only Devin's own files fails
    closed on an imported server -- a hard deny under Enforce -- while an
    unconditional Claude fallback would resolve a same-named server Devin is not
    actually serving when that import is switched off.
    """
    for path in _devin_cli_mcp_config_paths(cwd):
        result = _search_jsonc_file(path, server_name)
        if result is not None:
            return result

    enabled = _devin_cli_enabled_import_sources(cwd)
    if "claude" in enabled:
        result = lookup_mcp_server(server_name, cwd)
        if result is not None:
            return result
    if "cursor" in enabled:
        for path in _devin_cursor_import_paths(cwd):
            result = _search_jsonc_file(path, server_name)
            if result is not None:
                return result
    if "windsurf" in enabled:
        for path in _devin_windsurf_import_paths(cwd):
            result = _search_jsonc_file(path, server_name)
            if result is not None:
                return result
    if "opencode" in enabled:
        for path in _devin_opencode_import_paths(cwd):
            result = _search_keyed_file(
                path, "mcp", server_name, _extract_opencode_server
            )
            if result is not None:
                return result
    if "zed" in enabled:
        for path in _devin_zed_import_paths(cwd):
            result = _search_keyed_file(
                path, "context_servers", server_name, _extract_toggleable_server
            )
            if result is not None:
                return result
    return None


def lookup_goose_mcp_server(server_name: str) -> MCPServer | None:
    """Resolve a Goose MCP extension from Goose YAML config files."""
    entry = _lookup_goose_extension_entry(server_name)
    if entry is None or not _goose_extension_is_mcp(entry):
        return None
    return _extract_server_entry(entry)


def is_goose_mcp_extension(server_name: str) -> bool | None:
    """Return whether a Goose extension is MCP-backed.

    ``None`` means the extension was not found in Goose config. Callers use that
    as fail-closed MCP enforcement for unknown extension-prefixed tool names.
    """
    entry = _lookup_goose_extension_entry(server_name)
    if entry is None:
        return None
    return _goose_extension_is_mcp(entry)


def _cline_cli_mcp_settings_paths() -> tuple[Path, ...]:
    """Cline MCP settings locations, honoring ``CLINE_DIR``."""
    cline_dir = hook_io.getenv("CLINE_DIR")
    roots = (
        [Path(hook_io.abspath(str(Path(cline_dir).expanduser())))] if cline_dir else []
    )
    roots.append(Path.home() / ".cline")
    return tuple(
        root / "data" / "settings" / "cline_mcp_settings.json" for root in roots
    )


def _read_cline_cli_mcp_servers() -> Mapping[object, Any]:
    for path in _cline_cli_mcp_settings_paths():
        servers = _read_json_servers(path, "mcpServers")
        if servers:
            return servers
    return {}


def _sanitize_cline_mcp_name(name: str) -> str:
    """Mirror Cline's MCP tool-name sanitizer: bad chars collapse to ``_``."""
    return regex_safe.sub(r"[^a-zA-Z0-9_-]+", "_", name)


def resolve_cline_cli_mcp_tool(tool_name: str) -> tuple[str, MCPServer] | None:
    """Resolve a Cline ``<server>__<tool>`` name to its configured MCP server.

    Cline flattens MCP tools into the normal tool namespace as
    ``f"{server}__{tool}"`` with **no** ``mcp__`` prefix, then — if the result
    exceeds 64 chars or contains characters outside ``[a-zA-Z0-9_-]`` — sanitizes
    it and truncates to 55 chars plus ``_<8-hex sha1>`` of the *raw* name.

    That transform is lossy and irreversible, and ``__`` is itself legal inside a
    server or tool name, so splitting on ``__`` is wrong even in the happy path.
    Instead we match the name against the *known* server inventory by longest
    prefix. Truncation only ever removes the tail, so the server prefix survives
    for any server whose (sanitized) name fits within the 55-char base — which
    covers the realistic cases. Anything unresolvable returns ``None`` and the
    caller treats it as an unknown MCP tool rather than guessing a server.
    """
    if "__" not in tool_name:
        return None

    servers = _read_cline_cli_mcp_servers()
    candidates: list[str] = [str(name) for name in servers if str(name)]
    # Longest server name first so a server whose name prefixes another cannot
    # shadow the more specific match.
    candidates.sort(key=lambda name: len(name), reverse=True)

    for candidate in candidates:
        prefixes = {f"{candidate}__", f"{_sanitize_cline_mcp_name(candidate)}__"}
        if not any(tool_name.startswith(prefix) for prefix in prefixes):
            continue
        server = _extract_server_by_key(servers, candidate)
        if server is not None:
            return candidate, server
    return None


def cline_cli_tool_resolves_mcp_source(tool_name: str) -> bool:
    """True when a Cline tool name resolves to a configured MCP server."""
    return resolve_cline_cli_mcp_tool(tool_name) is not None


def lookup_cline_cli_mcp_server(server_name: str) -> MCPServer | None:
    """Resolve one Cline MCP server entry by exact configured name."""
    servers = _read_cline_cli_mcp_servers()
    return _extract_server_by_key(servers, server_name)


def resolve_hermes_mcp_tool(tool_name: str) -> tuple[str, MCPServer] | None:
    """Resolve ``mcp_<server>_<tool>`` Hermes tool names by longest normalized server prefix."""
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


def _gemini_cli_system_settings_dir() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/GeminiCli")
    if system == "Windows":
        return Path("C:/ProgramData/gemini-cli")
    return Path("/etc/gemini-cli")


def _gemini_cli_mcp_config_paths(cwd: str) -> list[Path]:
    """Gemini CLI settings files in highest-to-lowest precedence order."""
    paths = [_gemini_cli_system_settings_dir() / "settings.json"]
    if cwd:
        paths.append(Path(cwd) / ".gemini" / "settings.json")
    paths.append(Path.home() / ".gemini" / "settings.json")
    return paths


def _read_gemini_cli_mcp_servers(cwd: str) -> dict[object, Any]:
    """Union of ``mcpServers`` across Gemini's settings scopes.

    Gemini merges ``mcpServers`` by server name across scopes, so for a
    name-resolution lookup the union is what matters. Earlier (higher
    precedence) paths win on conflict.
    """
    merged: dict[object, Any] = {}
    for path in _gemini_cli_mcp_config_paths(cwd):
        data = _read_json_object(path)
        if data is None:
            continue
        servers = data.get("mcpServers", {})
        if not isinstance(servers, dict):
            continue
        for key, value in cast(dict[object, Any], servers).items():
            merged.setdefault(key, value)
    return merged


def resolve_gemini_cli_mcp_tool(
    tool_name: str, cwd: str
) -> tuple[str, MCPServer] | None:
    """Resolve a legacy Gemini ``mcp_<server>_<tool>`` fallback name.

    Current hooks carry authoritative ``mcp_context``. Older payloads only had
    sanitized names, whose server/tool boundary is ambiguous; longest-prefix
    matching preserves enforcement for those clients.
    """
    if not tool_name.startswith("mcp_"):
        return None

    servers = _read_gemini_cli_mcp_servers(cwd)
    normalized_tool_name = _normalized_name(tool_name.removeprefix("mcp_"))
    candidates = [name for name in servers if _normalized_name(str(name))]
    candidates.sort(key=lambda name: len(_normalized_name(str(name))), reverse=True)

    for candidate_name in candidates:
        if not normalized_tool_name.startswith(_normalized_name(str(candidate_name))):
            continue
        server = _extract_server_by_key(servers, candidate_name)
        if server is not None:
            return str(candidate_name), server
    return None


def lookup_gemini_cli_mcp_server(server_name: str, cwd: str) -> MCPServer | None:
    """Resolve a Gemini CLI MCP server by exact configured name."""
    return _extract_server_by_key(_read_gemini_cli_mcp_servers(cwd), server_name)


def resolve_gemini_cli_mcp_context(
    input_data: Mapping[str, Any] | None,
) -> tuple[str, MCPServer | None] | None:
    """Resolve Gemini's authoritative MCP hook context.

    A non-``None`` result identifies an MCP tool even when its connection
    details are malformed, so Enforce can fail closed instead of routing the
    call through local-tool scanning.
    """
    if input_data is None:
        return None
    context = input_data.get("mcp_context")
    if not isinstance(context, dict):
        return None
    server_name = context.get("server_name")
    if not isinstance(server_name, str) or not server_name.strip():
        return None
    server = _extract_server_entry(context)
    if server is not None:
        server["name"] = server_name
    return server_name, server


def lookup_cursor_mcp_server(
    server_name: str, payload: Mapping[str, Any]
) -> MCPServer | None:
    """Resolve a Cursor beforeMCPExecution display name across workspace + global mcp.json."""
    _name, scope_separator, scope_metadata = server_name.partition("::mcpScope:")
    scope = scope_metadata.partition(":")[0] if scope_separator else None
    if scope is not None and scope != "profile":
        return None

    for path in _cursor_mcp_config_paths(payload, profile_only=scope == "profile"):
        result = _search_cursor_file(path, server_name)
        if result is not None:
            return result
    return None


def resolve_cursor_before_mcp_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a Cursor MCP payload with its display-name source resolved if found."""
    if payload.get("url"):
        return payload

    # A command can carry ::mcpScope: metadata and is authoritative when present.
    # Falling back to an unscoped name could escape profile-only resolution.
    server_name = payload.get("command")
    if not isinstance(server_name, str) or not server_name.strip():
        server_name = payload.get("mcp_server_name")
    if not isinstance(server_name, str) or not server_name.strip():
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


def _candidate_project_roots(cwd: str) -> list[str]:
    """Project roots whose config may govern *cwd*: cwd itself first, then the
    enclosing repo/worktree root, then the main checkout root when cwd is
    inside a linked git worktree. Candidates are normalized lexically (never
    resolved) so they still match config keyed by exact path strings."""
    candidates = [cwd]
    git_entry: Path | None = None
    start = Path(os.path.normpath(cwd))
    for directory in (start, *start.parents):
        entry = directory / ".git"
        if entry.exists():
            git_entry = entry
            break
    if git_entry is not None:
        candidates.append(str(git_entry.parent))
        if git_entry.is_file():
            main_root = _worktree_main_root(git_entry)
            if main_root is not None:
                candidates.append(main_root)
    return list(dict.fromkeys(candidates))


def _worktree_main_root(git_file: Path) -> str | None:
    admin = _worktree_admin_dir(git_file)
    if admin is None:
        return None
    common = _read_first_line(admin / "commondir")
    if common:
        if not os.path.isabs(common):
            common = os.path.join(str(admin), common)
        return os.path.dirname(os.path.normpath(common))
    if admin.parent.name == "worktrees" and admin.parent.parent.name == ".git":
        return str(admin.parent.parent.parent)
    return None


def _worktree_admin_dir(git_file: Path) -> Path | None:
    line = _read_first_line(git_file)
    if line is None or not line.startswith("gitdir:"):
        return None
    pointer = line.removeprefix("gitdir:").strip()
    if not pointer:
        return None
    if not os.path.isabs(pointer):
        pointer = os.path.join(str(git_file.parent), pointer)
    return Path(os.path.normpath(pointer))


def _read_first_line(path: Path) -> str | None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    lines = content.splitlines()
    return lines[0].strip() if lines else None


def _search_file(path: Path, server_name: str) -> MCPServer | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return _extract_server(data.get("mcpServers", {}), server_name)


def _cursor_mcp_config_paths(
    payload: Mapping[str, Any], *, profile_only: bool = False
) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()

    def add_path(root: object) -> None:
        if isinstance(root, str) and root:
            path = Path(root) / ".cursor" / "mcp.json"
            if path not in seen:
                seen.add(path)
                paths.append(path)

    if not profile_only:
        workspace_roots = payload.get("workspace_roots")
        if isinstance(workspace_roots, list):
            for root in workspace_roots:
                add_path(root)
        add_path(payload.get("cwd"))

    home_path = Path.home() / ".cursor" / "mcp.json"
    if home_path not in seen:
        paths.append(home_path)
    return paths


def _vscode_mcp_config_paths(cwd: str) -> tuple[Path, ...]:
    paths = [
        Path(cwd) / ".vscode" / "mcp.json",
        Path.home() / "Library" / "Application Support" / "Code" / "User" / "mcp.json",
        Path.home() / ".config" / "Code" / "User" / "mcp.json",
    ]
    appdata = hook_io.getenv("APPDATA")
    if appdata:
        paths.append(Path(appdata) / "Code" / "User" / "mcp.json")
    return tuple(paths)


def _windsurf_mcp_config_paths(cwd: str) -> tuple[Path, ...]:
    """Workspace config first, then the Codeium profile Cascade actually reads."""
    paths = [Path.home() / ".codeium" / "windsurf" / "mcp_config.json"]
    if cwd:
        paths.insert(0, Path(cwd) / ".windsurf" / "mcp_config.json")
    return tuple(paths)


# Devin imports MCP servers from these tools when the matching
# ``read_config_from`` key is on. ``agents_standard`` and ``copilot`` import
# only rules/skills, so they can never contribute a server.
_DEVIN_MCP_IMPORT_SOURCES = ("claude", "cursor", "windsurf", "opencode", "zed")


def _devin_cli_user_config_roots() -> list[Path]:
    """``~/.config/devin`` plus ``%APPDATA%/devin``.

    Both are probed rather than branching on platform -- ``APPDATA`` is unset
    off Windows, so the extra entry simply never exists there.
    """
    roots = [Path.home() / ".config" / "devin"]
    appdata = hook_io.getenv("APPDATA")
    if appdata:
        roots.append(Path(appdata) / "devin")
    return roots


def _devin_cli_mcp_config_paths(cwd: str) -> tuple[Path, ...]:
    """Project overrides first, then the user-level Devin config root.

    ``.devin/config.json`` is included because servers lived there before
    Devin v3000.3 split them into ``mcp_config.json``; un-migrated hosts still
    resolve.
    """
    paths: list[Path] = []
    for root in _candidate_project_roots(cwd):
        project = Path(root) / ".devin"
        paths.extend(
            (
                project / "mcp_config.local.json",
                project / "mcp_config.json",
                project / "config.json",
            )
        )
    for root_dir in _devin_cli_user_config_roots():
        paths.extend((root_dir / "mcp_config.json", root_dir / "config.json"))
    return tuple(dict.fromkeys(paths))


def _devin_cli_settings_paths(cwd: str) -> tuple[Path, ...]:
    """Devin config files that can carry ``read_config_from``, lowest priority first."""
    paths: list[Path] = [
        root_dir / "config.json" for root_dir in _devin_cli_user_config_roots()
    ]
    for root in reversed(_candidate_project_roots(cwd)):
        project = Path(root) / ".devin"
        paths.extend((project / "config.json", project / "config.local.json"))
    return tuple(dict.fromkeys(paths))


def _devin_cli_enabled_import_sources(cwd: str) -> frozenset[str]:
    """Which ``read_config_from`` sources Devin is importing servers from.

    Devin documents every import as enabled unless explicitly disabled, so only
    a literal ``false`` switches one off; absent or non-bool values leave it on.
    """
    enabled = dict.fromkeys(_DEVIN_MCP_IMPORT_SOURCES, True)
    for path in _devin_cli_settings_paths(cwd):
        # JSONC-tolerant: a strict read of a commented config would silently drop
        # the toggles and treat a disabled source as enabled.
        data = _read_jsonc_object(path)
        if data is None:
            continue
        section = data.get("read_config_from")
        if not isinstance(section, dict):
            continue
        for source in _DEVIN_MCP_IMPORT_SOURCES:
            value = section.get(source)
            if isinstance(value, bool):
                enabled[source] = value
    return frozenset(source for source, is_on in enabled.items() if is_on)


def _devin_cursor_import_paths(cwd: str) -> tuple[Path, ...]:
    paths = [
        Path(root) / ".cursor" / "mcp.json" for root in _candidate_project_roots(cwd)
    ]
    paths.append(Path.home() / ".cursor" / "mcp.json")
    return tuple(dict.fromkeys(paths))


def _devin_windsurf_import_paths(cwd: str) -> tuple[Path, ...]:
    """Project config, then every Codeium channel directory.

    Devin imports ``~/.codeium/<channel>/mcp_config.json`` -- ``windsurf`` plus
    release channels like ``windsurf-next``. This deliberately does not reuse
    ``lookup_windsurf_mcp_server``, which only knows the stable channel: a server
    configured on Next would stay unresolved and be denied under Enforce.
    Channels are enumerated rather than hardcoded so a newly shipped one resolves
    instead of failing closed.
    """
    paths = [
        Path(root) / ".windsurf" / "mcp_config.json"
        for root in _candidate_project_roots(cwd)
    ]
    codeium_root = Path.home() / ".codeium"
    # Stable channel first so resolution order stays deterministic.
    paths.append(codeium_root / "windsurf" / "mcp_config.json")
    paths.extend(child / "mcp_config.json" for child in _iter_child_dirs(codeium_root))
    return tuple(dict.fromkeys(paths))


def _devin_opencode_import_paths(cwd: str) -> tuple[Path, ...]:
    paths: list[Path] = []
    for root in _candidate_project_roots(cwd):
        paths.extend((Path(root) / "opencode.json", Path(root) / "opencode.jsonc"))
    user_root = Path.home() / ".config" / "opencode"
    paths.extend((user_root / "opencode.json", user_root / "opencode.jsonc"))
    return tuple(dict.fromkeys(paths))


def _devin_zed_import_paths(cwd: str) -> tuple[Path, ...]:
    paths = [
        Path(root) / ".zed" / "settings.json" for root in _candidate_project_roots(cwd)
    ]
    paths.append(Path.home() / ".config" / "zed" / "settings.json")
    appdata = hook_io.getenv("APPDATA")
    if appdata:
        paths.append(Path(appdata) / "Zed" / "settings.json")
    return tuple(dict.fromkeys(paths))


def _iter_child_dirs(path: Path) -> Iterator[Path]:
    try:
        children = sorted(path.iterdir())
    except OSError:
        return
    for child in children:
        if child.is_dir():
            yield child


def _codex_mcp_config_paths() -> tuple[Path, ...]:
    return (
        Path.home() / ".codex" / "config.toml",
        Path.home() / ".codex" / "managed_config.toml",
        Path("/etc/codex/managed_config.toml"),
    )


def _claude_managed_mcp_config_path() -> Path:
    """Claude Code enterprise managed MCP config (MDM-deployed).

    When this file exists its server set is exclusive (users can't override),
    so it must be consulted first. See
    https://code.claude.com/docs/en/managed-mcp.
    """
    system = platform.system()
    if system == "Darwin":
        return Path("/Library/Application Support/ClaudeCode/managed-mcp.json")
    if system == "Windows":
        program_files = hook_io.getenv("PROGRAMFILES") or r"C:\Program Files"
        return Path(program_files) / "ClaudeCode" / "managed-mcp.json"
    return Path("/etc/claude-code/managed-mcp.json")


def _goose_mcp_config_paths() -> tuple[Path, ...]:
    paths = [Path.home() / ".config" / "goose" / "config.yaml"]
    appdata = hook_io.getenv("APPDATA")
    if appdata:
        paths.append(Path(appdata) / "Block" / "goose" / "config" / "config.yaml")
    return tuple(paths)


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


def _search_file_key(path: Path, server_name: str, key: str) -> MCPServer | None:
    servers = _read_json_servers(path, key)
    return _search_server_map(servers, server_name)


def _search_server_map(
    servers: Mapping[object, Any], server_name: str
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


def _search_yaml_key(path: Path, server_name: str, key: str) -> MCPServer | None:
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    if not isinstance(data, dict):
        return None

    servers = data.get(key, {})
    result = _extract_server(servers, server_name)
    if result is not None:
        return result

    normalized_server_name = _normalized_name(server_name)
    if isinstance(servers, dict):
        for candidate_name in servers:
            if (
                isinstance(candidate_name, str)
                and _normalized_name(candidate_name) == normalized_server_name
            ):
                return _extract_server_by_key(servers, candidate_name)
    return None


def _lookup_goose_extension_entry(server_name: str) -> dict[str, Any] | None:
    for path in _goose_mcp_config_paths():
        entry = _search_yaml_entry(path, server_name, "extensions")
        if entry is not None:
            return entry
    return None


def _search_yaml_entry(path: Path, server_name: str, key: str) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    if not isinstance(data, dict):
        return None

    servers = data.get(key, {})
    if not isinstance(servers, dict):
        return None

    entry = cast(dict[object, Any], servers).get(server_name)
    if isinstance(entry, dict):
        return cast(dict[str, Any], entry)

    normalized_server_name = _normalized_name(server_name)
    for candidate_name, candidate_entry in servers.items():
        if (
            isinstance(candidate_name, str)
            and _normalized_name(candidate_name) == normalized_server_name
            and isinstance(candidate_entry, dict)
        ):
            return cast(dict[str, Any], candidate_entry)
    return None


def _goose_extension_is_mcp(entry: Mapping[str, Any]) -> bool:
    enabled = entry.get("enabled")
    if enabled is False or (isinstance(enabled, str) and enabled.lower() == "false"):
        return False

    ext_type = entry.get("type")
    if isinstance(ext_type, str):
        normalized_type = ext_type.strip().lower()
        if normalized_type in _GOOSE_LOCAL_EXTENSION_TYPES:
            return False
        if normalized_type in _GOOSE_MCP_TRANSPORT_TYPES:
            return True
        if normalized_type:
            return False

    return any(entry.get(key) for key in ("url", "serverUrl", "uri", "command", "cmd"))


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

    scoped_server_name, scope_separator, _scope = server_name.partition("::mcpScope:")
    if scope_separator:
        lookup_names.append(scoped_server_name)
        if scoped_server_name.startswith("user-"):
            lookup_names.append(scoped_server_name.removeprefix("user-"))

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


def _strip_block_comments(text: str) -> str:
    """Remove ``/* */`` comments, preserving the markers inside JSON strings.

    Deliberately local to this read-only lookup path rather than added to
    ``tolerant_json``: install-path writers reserialize whatever they parse, so a
    block-commented file has to stay *unparseable* there for the writer to leave
    the user's settings untouched instead of silently dropping their comments
    (pinned by ``test_user_preserves_vscode_settings_on_parse_error``). Reading
    never rewrites, so extra tolerance here is free.
    """
    out: list[str] = []
    in_string = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if ch == "\\" and i + 1 < n:
                out.append(text[i : i + 2])
                i += 2
                continue
            if ch == '"':
                in_string = False
            out.append(ch)
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            if end == -1:
                break
            # Keep newline count stable so json's error positions stay usable.
            out.append("\n" * text.count("\n", i, end))
            i = end + 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _read_jsonc_object(path: Path) -> dict[str, Any] | None:
    """``_read_json_object`` that also accepts JSONC comments + trailing commas.

    Zed's ``settings.json`` and OpenCode's ``opencode.jsonc`` are JSONC by
    convention (the scanner parses them with ``json5``, which the hook bundle
    excludes), and Devin's own config is read tolerantly on the install side. A
    strict read here would report a live server as unregistered -- a hard deny
    under Enforce.
    """
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    for candidate in (text, _strip_block_comments(text)):
        try:
            data = tolerant_json_loads(candidate)
        except (ValueError, OSError):
            continue
        if isinstance(data, dict):
            return cast(dict[str, Any], data)
        return None
    return None


def _search_jsonc_file(path: Path, server_name: str) -> MCPServer | None:
    """``_search_file`` over a JSONC-tolerant read of a ``mcpServers`` config."""
    data = _read_jsonc_object(path)
    if data is None:
        return None
    return _extract_server(data.get("mcpServers", {}), server_name)


def _search_keyed_file(
    path: Path,
    servers_key: str,
    server_name: str,
    extractor: Callable[[object, str], MCPServer | None],
) -> MCPServer | None:
    """``_search_file`` for a foreign config whose servers live under *servers_key*."""
    data = _read_jsonc_object(path)
    if data is None:
        return None
    return extractor(data.get(servers_key), server_name)


def _extract_toggleable_server(servers: object, server_name: str) -> MCPServer | None:
    """Standard-shaped entry that an ``enabled: false`` flag can switch off.

    Zed's ``context_servers`` carry a string ``command`` plus ``args`` (or a
    ``url``), which the standard extractor already understands.
    """
    if not isinstance(servers, dict):
        return None
    entry = cast(dict[object, Any], servers).get(server_name)
    if not isinstance(entry, dict) or entry.get("enabled") is False:
        return None
    return _extract_server_entry(entry)


def _extract_opencode_server(servers: object, server_name: str) -> MCPServer | None:
    """OpenCode entry: argv arrives as one ``command`` list, not command + args.

    Falling through to the standard extractor would stringify that list into a
    command no policy could match, so the list is joined explicitly.
    """
    if not isinstance(servers, dict):
        return None
    entry = cast(dict[object, Any], servers).get(server_name)
    if not isinstance(entry, dict) or entry.get("enabled") is False:
        return None
    url = entry.get("url")
    if isinstance(url, str) and url:
        return MCPServer(url=url)
    command = entry.get("command")
    if isinstance(command, list) and command:
        joined = " ".join(str(part) for part in command).strip()
        if joined:
            return MCPServer(command=joined)
        return None
    return _extract_server_entry(entry)


def _extract_server_entry(entry: object) -> MCPServer | None:
    """Extract remote or stdio identity across supported client formats."""
    if not entry or not isinstance(entry, dict):
        return None
    server = cast(dict[str, Any], entry)
    url = (
        server.get("url")
        or server.get("serverUrl")
        or server.get("uri")
        or server.get("httpUrl")
        or server.get("tcp")
    )
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

    # Fallback: plugins active on disk but not surfaced by the registry pass
    # above -- managed/Cowork provisioning, dev symlinks, marketplace bundles,
    # or a plugin registered only for a *different* project. Skip only plugins
    # explicitly disabled for this cwd, so the scan can't re-enable a disabled
    # plugin but a same-named plugin registered elsewhere still resolves here.
    disabled = _disabled_plugin_names(cwd)
    for plugin_root, plugin_name in _claude_filesystem_plugin_roots():
        if plugin_name in disabled:
            continue
        result = _search_claude_plugin_root(plugin_root, server_name, plugin_name)
        if result is not None:
            return result
    return None


# Top-level entries under ~/.claude/plugins that are not themselves plugin roots.
_NON_PLUGIN_PLUGIN_DIRS = frozenset({"cache", "marketplaces", "repos"})


def _safe_iterdir(path: Path) -> list[Path]:
    try:
        return list(path.iterdir())
    except OSError:
        return []


def _disabled_plugin_names(cwd: str) -> set[str]:
    """Plugin names (``<name>`` from ``<name>@<marketplace>``) explicitly
    disabled (``enabledPlugins[key] == false``) for this cwd. Used to keep the
    filesystem fallback from re-enabling a disabled plugin, without suppressing
    a same-named plugin that's only registered for another project."""
    enabled = _claude_enabled_plugins(_claude_settings_cwd(cwd))
    return {
        str(key).rsplit("@", 1)[0] for key, value in enabled.items() if value is False
    }


def _plugin_root_and_name(plugin_dir: Path) -> tuple[Path, str] | None:
    """Return ``(plugin_dir, plugin_name)`` if ``plugin_dir`` holds a plugin
    manifest. ``plugin_name`` prefers the manifest ``name`` (what Claude Code
    uses in the ``plugin_<name>_<server>`` tool namespace) over the dir name."""
    manifest = _read_json_object(plugin_dir / ".claude-plugin" / "plugin.json")
    if manifest is None:
        return None
    name = manifest.get("name")
    plugin_name = name if isinstance(name, str) and name else plugin_dir.name
    return plugin_dir, plugin_name


def _claude_filesystem_plugin_roots() -> Iterator[tuple[Path, str]]:
    """Discover plugin roots on disk beyond ``installed_plugins.json``:
    top-level (symlinked/dev) dirs, the install cache, and marketplace-bundled
    plugins. De-duplicated by resolved path."""
    plugins_dir = Path.home() / ".claude" / "plugins"
    if not plugins_dir.is_dir():
        return

    candidates: list[Path] = []
    # Top-level (symlinked / dev) plugin dirs: ~/.claude/plugins/<name>
    for entry in _safe_iterdir(plugins_dir):
        if entry.name in _NON_PLUGIN_PLUGIN_DIRS or entry.name.startswith("."):
            continue
        candidates.append(entry)
    # Install cache: ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>
    for marketplace in _safe_iterdir(plugins_dir / "cache"):
        for plugin in _safe_iterdir(marketplace):
            candidates.extend(_safe_iterdir(plugin))
    # Marketplace-bundled roots from plugins/ and external_plugins/.
    for marketplace in _safe_iterdir(plugins_dir / "marketplaces"):
        candidates.extend(_safe_iterdir(marketplace / "plugins"))
        candidates.extend(_safe_iterdir(marketplace / "external_plugins"))

    seen: set[Path] = set()
    for plugin_dir in candidates:
        if not plugin_dir.is_dir():
            continue
        try:
            resolved = plugin_dir.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        root_and_name = _plugin_root_and_name(plugin_dir)
        if root_and_name is not None:
            yield root_and_name


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
        if not any(
            Path(candidate).resolve().is_relative_to(project_root)
            for candidate in _candidate_project_roots(cwd)
        ):
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
