"""MCP client application definitions and configuration paths."""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class PlatformPath:
    """Base for path templates that resolve per-platform.

    Attributes:
        path: Path template string (supports ~ and env vars like %APPDATA%, $HOME)
        platform: Target platform ("macos", "windows", "linux", or "all")
    """

    path: str
    platform: str = "all"

    def resolve(self) -> Path | None:
        """Resolve the path for the current platform.

        Returns:
            Resolved Path if platform matches, None otherwise.
        """
        current_platform = {
            "Darwin": "macos",
            "Windows": "windows",
            "Linux": "linux",
        }.get(platform.system())

        if self.platform != "all" and self.platform != current_platform:
            return None

        expanded = os.path.expandvars(self.path)
        return Path(expanded).expanduser()


@dataclass
class ConfigPath(PlatformPath):
    """A configuration file path with platform specification."""


@dataclass
class ProjectConfigPattern:
    """Pattern for finding project-level config files.

    Attributes:
        relative_path: Path relative to project root (e.g., ".mcp.json", ".vscode/mcp.json")
        servers_key: JSON key containing server definitions (may differ from global config)
    """

    relative_path: str
    servers_key: str = "mcpServers"


@dataclass
class ExtensionsPath(PlatformPath):
    """Path to extensions directory with prefix pattern for folder scanning."""

    prefix: str = "mcp-server-"


@dataclass
class PluginPath(PlatformPath):
    """Path to a plugin cache directory containing installed plugins.

    Each subdirectory is <plugin-name>/<hash>/ and may contain mcp.json or .mcp.json.
    """

    mcp_filenames: tuple[str, ...] = ("mcp.json", ".mcp.json")


@dataclass
class MCPClientDefinition:
    """Definition of an MCP client application.

    This data model is designed to be:
    1. Easy to update when clients change their config locations
    2. Declarative - parsing behavior is defined by data, not code
    3. Self-documenting - each field has a clear purpose

    Attributes:
        name: Internal identifier (lowercase, snake_case)
        display_name: Human-readable name for logging/display
        paths: List of possible GLOBAL config file locations
        servers_key: JSON key path to the servers dictionary for GLOBAL configs
            - "mcpServers" - standard MCP format
            - "servers" - alternative format (VS Code)
            - "" (empty) - servers are at root level
        additional_servers_keys: Additional key paths to extract servers from
            (e.g., for Claude Code's "projects.*.mcpServers" structure)
        project_config: Optional pattern for project-level configs
        extensions_paths: Optional list of extension directories to scan for MCP servers
        config_format: Config file format ("json" or "yaml")
        enabled: Whether to scan this client (allows disabling without removing)
        notes: Optional notes about this client's config format
    """

    name: str
    display_name: str
    paths: list[ConfigPath]
    servers_key: str = "mcpServers"  # JSON key for GLOBAL configs
    additional_servers_keys: list[str] | None = (
        None  # Extra paths like "projects.*.mcpServers"
    )
    project_config: ProjectConfigPattern | None = None  # Optional project-level config
    additional_project_configs: list[ProjectConfigPattern] | None = None
    extensions_paths: list[ExtensionsPath] | None = None  # Optional extensions folders
    plugin_paths: list[PluginPath] | None = None  # Optional plugin cache directories
    config_format: str = "json"  # "json" or "yaml"
    enabled: bool = True
    notes: str | None = None

    def iter_project_configs(self) -> list[ProjectConfigPattern]:
        """Return primary + additional project config patterns."""
        result: list[ProjectConfigPattern] = []
        if self.project_config:
            result.append(self.project_config)
        if self.additional_project_configs:
            result.extend(self.additional_project_configs)
        return result

    def get_config_paths(self) -> list[Path]:
        """Get all valid config paths for the current platform.

        Returns:
            List of resolved paths that exist on the current platform.
        """
        resolved: list[Path] = []
        for config_path in self.paths:
            path = config_path.resolve()
            if path is not None:
                resolved.append(path)
        return resolved

    def _extract_from_key_path(
        self, config_data: dict[str, Any], key_path: str
    ) -> dict[str, Any]:
        """Extract servers from a specific key path.

        Supports wildcard '*' for iterating over dictionary keys.
        E.g., "projects.*.mcpServers" extracts mcpServers from each project.

        Args:
            config_data: Parsed JSON config file contents
            key_path: Dot-separated key path, with optional '*' wildcards

        Returns:
            Dictionary of server_name -> server_config
        """
        if not key_path:
            # Servers are at root level - return any dict entries that look like servers
            return {
                k: v
                for k, v in config_data.items()
                if isinstance(v, dict) and ("command" in v or "url" in v)
            }

        keys = key_path.split(".")
        result: dict[str, Any] = {}

        def traverse(
            current: Any,
            remaining_keys: list[str],
            project: str | None = None,
        ) -> None:
            if not remaining_keys:
                if isinstance(current, dict):
                    for name, config in current.items():
                        if isinstance(config, dict):
                            # Check if this server name already exists
                            if name in result:
                                # Merge: append this project to existing project_name list
                                existing = result[name]
                                existing_projects = existing.get("project_name")
                                if existing_projects is None:
                                    # Existing had no project, now we have one
                                    if project is not None:
                                        existing["project_name"] = [project]
                                elif isinstance(existing_projects, list):
                                    # Already a list, append
                                    if project is not None:
                                        existing_projects.append(project)
                                else:
                                    # Was a single string, convert to list
                                    if project is not None:
                                        existing["project_name"] = [
                                            existing_projects,
                                            project,
                                        ]
                            else:
                                # New server, add project_name field if we traversed through a wildcard
                                if project is not None:
                                    config = {**config, "project_name": [project]}
                                result[name] = config
                return

            key = remaining_keys[0]
            rest = remaining_keys[1:]

            if key == "*":
                # Wildcard - iterate over all dict keys
                # Store the full key as the project (e.g., "/Users/aidan/workspace/Runlayer")
                if isinstance(current, dict):
                    for sub_key, sub_value in current.items():
                        traverse(sub_value, rest, project=sub_key)
            else:
                # Regular key - navigate into it
                if isinstance(current, dict) and key in current:
                    traverse(current[key], rest, project)

        traverse(config_data, keys)
        return result

    def extract_servers(self, config_data: dict[str, Any]) -> dict[str, Any]:
        """Extract the servers dictionary from parsed config data.

        Args:
            config_data: Parsed JSON config file contents

        Returns:
            Dictionary of server_name -> server_config, or empty dict if not found
        """
        # Extract from primary key path
        servers = self._extract_from_key_path(config_data, self.servers_key)

        # Extract from additional key paths (e.g., projects.*.mcpServers for Claude Code)
        if self.additional_servers_keys:
            for key_path in self.additional_servers_keys:
                additional = self._extract_from_key_path(config_data, key_path)
                servers.update(additional)

        return servers


# =============================================================================
# MCP CLIENT REGISTRY
# =============================================================================
#
# To add a new client:
#   1. Add a new MCPClientDefinition to MCP_CLIENTS list
#   2. Specify all known config paths for each platform
#   3. Set servers_key based on the client's JSON structure
#   4. Add a note if there's anything unusual about the format
#
# To update a client:
#   1. Find the client in MCP_CLIENTS by name
#   2. Update the paths or servers_key as needed
#   3. Update notes if the format changed
#
# To disable a client temporarily:
#   1. Set enabled=False on the client definition
#
# IMPORTANT: Documentation sync
#   When adding or updating clients, also update the "Supported Clients" table in:
#   docs/shadow-ai/detect/index.mdx (under "## Supported Clients")
#
# =============================================================================

MCP_CLIENTS: list[MCPClientDefinition] = [
    MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[
            ConfigPath("~/.cursor/mcp.json", platform="macos"),
            ConfigPath("%USERPROFILE%/.cursor/mcp.json", platform="windows"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".cursor/mcp.json",
            servers_key="mcpServers",
        ),
        plugin_paths=[
            PluginPath("~/.cursor/plugins/cache/cursor-public", platform="macos"),
            PluginPath(
                "%USERPROFILE%/.cursor/plugins/cache/cursor-public",
                platform="windows",
            ),
        ],
        notes="Plugins in ~/.cursor/plugins/cache/cursor-public/<name>/<hash>/. "
        "Project scope via .cursor/settings.json plugins key.",
    ),
    MCPClientDefinition(
        name="claude_desktop",
        display_name="Claude Desktop",
        paths=[
            ConfigPath(
                "~/Library/Application Support/Claude/extensions-installations.json",
                platform="macos",
            ),
            ConfigPath(
                "%APPDATA%/Claude/extensions-installations.json", platform="windows"
            ),
            ConfigPath(
                "~/Library/Application Support/Claude/claude_desktop_config.json",
                platform="macos",
            ),
            ConfigPath(
                "%APPDATA%/Claude/claude_desktop_config.json",
                platform="windows",
            ),
        ],
        servers_key="extensions",
        additional_servers_keys=["mcpServers"],
        project_config=None,
        notes="Extensions via extensions-installations.json and manual mcpServers via claude_desktop_config.json. "
        "Also covers Claude Cowork which shares the same config.",
    ),
    MCPClientDefinition(
        name="claude_code",
        display_name="Claude Code",
        paths=[
            ConfigPath("~/.claude.json", platform="macos"),
            ConfigPath("%USERPROFILE%/.claude.json", platform="windows"),
        ],
        servers_key="mcpServers",
        additional_servers_keys=[
            "projects.*.mcpServers"
        ],  # Project-specific servers in global file
        project_config=ProjectConfigPattern(
            relative_path=".mcp.json",
            servers_key="mcpServers",
        ),
        notes="Has mcpServers at root AND projects.*.mcpServers for project-specific configs in same file",
    ),
    MCPClientDefinition(
        name="vscode",
        display_name="VS Code",
        paths=[
            ConfigPath(
                "~/Library/Application Support/Code/User/mcp.json", platform="macos"
            ),
            ConfigPath("%APPDATA%/Code/User/mcp.json", platform="windows"),
        ],
        servers_key="servers",  # VS Code uses "servers" NOT "mcpServers"!
        project_config=ProjectConfigPattern(
            relative_path=".vscode/mcp.json",
            servers_key="servers",  # Project config also uses "servers"
        ),
        notes="VS Code uses 'servers' key (not 'mcpServers') for both global and project configs",
    ),
    MCPClientDefinition(
        name="windsurf",
        display_name="Windsurf",
        paths=[
            ConfigPath("~/.codeium/windsurf/mcp_config.json", platform="macos"),
            ConfigPath(
                "%USERPROFILE%/.codeium/windsurf/mcp_config.json", platform="windows"
            ),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".windsurf/mcp_config.json",
            servers_key="mcpServers",
        ),
        notes="Has both global and project-level (.windsurf/mcp_config.json) configs",
    ),
    MCPClientDefinition(
        name="goose",
        display_name="Goose",
        paths=[
            ConfigPath("~/.config/goose/config.yaml", platform="macos"),
            ConfigPath("%APPDATA%/Block/goose/config/config.yaml", platform="windows"),
        ],
        servers_key="extensions",
        config_format="yaml",
        project_config=None,  # Goose only has global config
        notes="YAML format. Uses 'extensions' key with enabled filtering. cmd/envs instead of command/env.",
    ),
    MCPClientDefinition(
        name="zed",
        display_name="Zed",
        paths=[
            ConfigPath("~/.config/zed/settings.json", platform="macos"),
            ConfigPath("%APPDATA%/Zed/settings.json", platform="windows"),
        ],
        servers_key="context_servers",
        project_config=ProjectConfigPattern(
            relative_path=".zed/settings.json",
            servers_key="context_servers",
        ),
        extensions_paths=[
            ExtensionsPath(
                "~/Library/Application Support/Zed/extensions/installed",
                platform="macos",
                prefix="mcp-server-",
            ),
            ExtensionsPath(
                "%LOCALAPPDATA%/Zed/extensions/installed",
                platform="windows",
                prefix="mcp-server-",
            ),
        ],
        notes="Uses 'context_servers' key. Extensions in installed/ folder with mcp-server-* prefix.",
    ),
    MCPClientDefinition(
        name="opencode",
        display_name="OpenCode",
        paths=[
            # OpenCode merges config from multiple sources; we only scan the common
            # user-level config location.
            ConfigPath("~/.config/opencode/opencode.json", platform="all"),
            ConfigPath("~/.config/opencode/opencode.jsonc", platform="all"),
        ],
        servers_key="mcp",
        project_config=ProjectConfigPattern(
            relative_path="opencode.json",
            servers_key="mcp",
        ),
        notes="Servers live under top-level 'mcp' and use OpenCode format (type=local|remote, command[]=..., environment={...}).",
    ),
    MCPClientDefinition(
        name="codex",
        display_name="Codex",
        paths=[
            ConfigPath("~/.codex/config.toml", platform="macos"),
            ConfigPath("~/.codex/config.toml", platform="linux"),
            ConfigPath("%USERPROFILE%/.codex/config.toml", platform="windows"),
        ],
        servers_key="mcp_servers",
        config_format="toml",
        project_config=ProjectConfigPattern(
            relative_path=".codex/config.toml",
            servers_key="mcp_servers",
        ),
        plugin_paths=[
            PluginPath(
                "~/.codex/plugins/cache",
                platform="macos",
                mcp_filenames=("mcp.json", ".mcp.json"),
            ),
            PluginPath(
                "%USERPROFILE%/.codex/plugins/cache",
                platform="windows",
                mcp_filenames=("mcp.json", ".mcp.json"),
            ),
            PluginPath(
                "~/.codex/plugins/cache",
                platform="linux",
                mcp_filenames=("mcp.json", ".mcp.json"),
            ),
        ],
        notes="TOML format. MCP servers under [mcp_servers.<name>] tables. "
        "Plugins in ~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/.",
    ),
    MCPClientDefinition(
        name="cline",
        display_name="Cline (VS Code Extension)",
        paths=[
            ConfigPath(
                "~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
                platform="macos",
            ),
            ConfigPath(
                "%APPDATA%/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
                platform="windows",
            ),
            ConfigPath(
                "~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
                platform="linux",
            ),
        ],
        servers_key="mcpServers",
        project_config=None,
        notes="VS Code extension (saoudrizwan.claude-dev). Global config only.",
    ),
    MCPClientDefinition(
        name="cline_cli",
        display_name="Cline CLI",
        paths=[
            ConfigPath(
                "$CLINE_DIR/data/settings/cline_mcp_settings.json", platform="all"
            ),
            ConfigPath(
                "~/.cline/data/settings/cline_mcp_settings.json", platform="all"
            ),
        ],
        servers_key="mcpServers",
        project_config=None,
        notes="Honors $CLINE_DIR; default ~/.cline. Global config only.",
    ),
    MCPClientDefinition(
        name="gemini_cli",
        display_name="Gemini CLI",
        paths=[
            ConfigPath("~/.gemini/settings.json", platform="all"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".gemini/settings.json",
            servers_key="mcpServers",
        ),
        notes="Settings file also holds non-MCP keys; extract only mcpServers.",
    ),
    MCPClientDefinition(
        name="antigravity",
        display_name="Antigravity",
        paths=[
            ConfigPath("~/.gemini/antigravity/mcp_config.json", platform="all"),
        ],
        servers_key="mcpServers",
        project_config=None,
        notes="Global only. Shares ~/.gemini base dir with Gemini CLI.",
    ),
    MCPClientDefinition(
        name="github_copilot_cli",
        display_name="GitHub Copilot CLI",
        paths=[
            ConfigPath("$COPILOT_HOME/mcp-config.json", platform="all"),
            ConfigPath("~/.copilot/mcp-config.json", platform="all"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".mcp.json",
            servers_key="mcpServers",
        ),
        additional_project_configs=[
            ProjectConfigPattern(
                relative_path=".github/mcp.json",
                servers_key="mcpServers",
            ),
            ProjectConfigPattern(
                relative_path=".vscode/mcp.json",
                servers_key="servers",
            ),
        ],
        notes="$COPILOT_HOME overrides ~/.copilot. Project configs: .mcp.json "
        "and .github/mcp.json use mcpServers; .vscode/mcp.json (legacy) uses servers.",
    ),
    # ==========================================================================
    # DESCOPED FROM v0 - Add these in a future release
    # ==========================================================================
    # MCPClientDefinition(
    #     name="warp",
    #     display_name="Warp",
    #     paths=[
    #         ConfigPath(
    #             "~/Library/Group Containers/2BBY89MBSN.dev.warp/Library/Application Support/dev.warp.Warp-Stable/mcp/config.json",
    #             platform="macos",
    #         ),
    #         ConfigPath("%APPDATA%/Warp/mcp/config.json", platform="windows"),
    #     ],
    #     servers_key="mcpServers",
    #     notes="Descoped from v0 - complex path, Windows path unverified",
    # ),
    # MCPClientDefinition(
    #     name="raycast",
    #     display_name="Raycast",
    #     paths=[
    #         ConfigPath("???", platform="macos"),  # TODO: Research exact path
    #     ],
    #     servers_key="mcpServers",
    #     notes="Descoped from v0 - config path needs research",
    # ),
]


def get_all_clients() -> list[MCPClientDefinition]:
    """Get all enabled MCP client definitions.

    Returns:
        List of MCPClientDefinition for enabled clients only.
    """
    return [c for c in MCP_CLIENTS if c.enabled]


def get_client_by_name(name: str) -> MCPClientDefinition | None:
    """Get a specific client definition by name.

    Args:
        name: Client name (e.g., "cursor", "claude_desktop")

    Returns:
        MCPClientDefinition if found, None otherwise.
    """
    for client in MCP_CLIENTS:
        if client.name == name:
            return client
    return None


def get_clients_with_project_configs() -> list[MCPClientDefinition]:
    """Get all enabled clients that have project-level config patterns.

    Returns:
        List of MCPClientDefinition for clients with any project configs.
    """
    return [c for c in MCP_CLIENTS if c.enabled and c.iter_project_configs()]
