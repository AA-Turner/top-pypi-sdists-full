"""MCP client application definitions and configuration paths."""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from runlayer_cli.scan.device import get_wsl_user_homes, list_wsl_distros


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
            Resolved Path if platform matches and the template fully expands
            to an absolute path, None otherwise.
        """
        current_platform = {
            "Darwin": "macos",
            "Windows": "windows",
            "Linux": "linux",
        }.get(platform.system())

        if self.platform != "all" and self.platform != current_platform:
            return None

        expanded = os.path.expandvars(self.path)
        resolved = Path(expanded).expanduser()
        # expandvars leaves unset vars literal (e.g. "$CLINE_DIR/..."), which
        # makes the candidate a relative path that stats against the process
        # cwd. Under the Linux all-users scan the cwd (/root, via cron) is not
        # searchable by the scanned user, so that stat raises EACCES and, on
        # Python 3.13, Path.exists() propagates it and kills the whole scan.
        # A non-absolute candidate can never be a real global config — drop it.
        if not resolved.is_absolute():
            return None
        return resolved


@dataclass
class ConfigPath(PlatformPath):
    """A configuration file path with platform specification."""


@dataclass
class ProjectConfigPattern:
    """Pattern for finding project-level config files.

    Attributes:
        relative_path: Path relative to project root (e.g., ".mcp.json", ".vscode/mcp.json")
        servers_key: JSON key containing server definitions (may differ from global config)
        requires_client_presence: Ignore this shared path unless the client is installed.
    """

    relative_path: str
    servers_key: str = "mcpServers"
    requires_client_presence: bool = False


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


@dataclass(frozen=True)
class NpmPackage:
    """Exact npm package identity and expected executable name."""

    name: str
    bin_name: str


@dataclass(frozen=True)
class PipPackage:
    """Exact Python distribution identity."""

    name: str


@dataclass(frozen=True)
class SettingsOverrideFlag:
    """Client launch flag that overrides a default settings location."""

    flag: str
    takes_value: bool = True
    mcp_config: Literal["none", "file", "user_data_dir"] = "none"
    variadic: bool = False


@dataclass
class InstallProbe:
    """Declarative filesystem and registry signals for client presence.

    Config-file and directory probes supplement the parents derived from
    ``MCPClientDefinition.paths``. They are mainly for presence-only clients
    that intentionally have no MCP config paths.

    Executes binaries: any ``cli_binaries`` entry with ``probe_cli_version=True``
    (the default) is resolved on PATH and run as ``<binary> --version`` to read
    a version. Generically-named binaries risk a PATH name-collision that
    executes an unrelated tool, so weigh that risk when adding a client — prefer
    specific names, and set ``probe_cli_version=False`` for GUI launchers or
    ambiguous commands.
    """

    macos_app_bundles: list[str] = field(default_factory=list)
    # Match VS Code-family extension dirs in host and WSL homes.
    vscode_extension_ids: list[str] = field(default_factory=list)
    npm_packages: list[NpmPackage] = field(default_factory=list)
    pip_packages: list[PipPackage] = field(default_factory=list)
    cli_binaries: list[str] = field(default_factory=list)
    # GUI launchers are valid presence signals but must not be executed.
    probe_cli_version: bool = True
    windows_display_name_prefixes: list[str] = field(default_factory=list)
    windows_install_dirs: list[str] = field(default_factory=list)
    linux_desktop_ids: list[str] = field(default_factory=list)
    config_files: list[PlatformPath] = field(default_factory=list)
    config_dirs: list[PlatformPath] = field(default_factory=list)
    # Some config files live under state roots shared by sibling products.
    probe_config_parents: bool = True


@lru_cache(maxsize=1)
def _is_windows_with_wsl() -> bool:
    """Cached: running on a Windows host that has WSL distros installed."""
    if platform.system() != "Windows":
        return False
    return bool(list_wsl_distros())


@lru_cache(maxsize=1)
def _wsl_homes() -> list[Path]:
    """Cached Linux user home dirs across all installed WSL distros."""
    if platform.system() != "Windows":
        return []
    homes: list[Path] = []
    for distro in list_wsl_distros():
        homes.extend(get_wsl_user_homes(distro))
    return homes


def _resolve_wsl_linux_paths(template: str) -> list[Path]:
    """Translate a ``~/...`` Linux path template into WSL UNC paths.

    Returns one path per discovered WSL user home. Empty when not on a Windows
    host with WSL or when the template is not ``~``-rooted.
    """
    if not _is_windows_with_wsl():
        return []
    if not template.startswith("~/"):
        return []

    relative = template[2:]
    return [home / relative for home in _wsl_homes()]


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
        sqlite_paths: Optional list of sqlite db paths for clients that store some
            servers in a database alongside their JSON config (e.g. Warp's in-app
            gallery installs). Resolution/WSL handling lives here so paths stay in
            one declarative place; the sqlite reading itself is client-specific.
        process_signatures: Optional case-insensitive substrings that identify this
            client's *running* executable (used by the runtime process-discovery
            channel to recognize a live client and its child MCP servers). Match
            against the process executable path; keep them specific (bundle /
            binary paths) so they do not collide with unrelated processes.
            npm-installed clients need no entry here: the runtime channel also
            matches ``node_modules/<name>/`` argv paths derived from
            ``install_probe.npm_packages``.
        settings_override_flags: Optional launch flags that bypass the client's
            default settings locations. Process discovery reports every match and
            may parse referenced MCP configs according to each flag's ``mcp_config``.
        install_probe: Optional declarative app/CLI/registry/config-directory
            signals used to inventory the client even when it has no MCP servers.
        config_format: Config file format ("json" or "yaml")
        enabled: Whether to scan this client (allows disabling without removing)
        notes: Optional notes about this client's config format
        entry_format: Parser registry key for individual server entries
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
    sqlite_paths: list[ConfigPath] | None = None  # Optional sqlite db locations
    process_signatures: list[str] | None = None  # Optional running-process markers
    settings_override_flags: list[SettingsOverrideFlag] | None = None
    config_format: str = "json"  # "json" or "yaml"
    enabled: bool = True
    notes: str | None = None
    install_probe: InstallProbe | None = None
    entry_format: str = "standard"

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

        On a Windows host with WSL installed, the Linux-side paths are also
        resolved (one per WSL user home) so that configs inside WSL distros
        are discovered alongside native Windows ones.

        Returns:
            List of resolved paths that exist on the current platform.
        """
        resolved: list[Path] = []
        for config_path in self.paths:
            path = config_path.resolve()
            if path is not None:
                resolved.append(path)

        if _is_windows_with_wsl():
            for config_path in self.paths:
                if config_path.platform == "linux":
                    resolved.extend(_resolve_wsl_linux_paths(config_path.path))

        return resolved

    def get_resolved_sqlite_paths(self) -> list[Path]:
        """Get candidate sqlite db paths for the current platform.

        Mirrors ``get_config_paths`` (including WSL Linux-side resolution on a
        Windows host with WSL) but for ``sqlite_paths``. Paths are candidates,
        not guaranteed to exist; the caller checks existence.
        """
        if not self.sqlite_paths:
            return []

        resolved: list[Path] = []
        for sqlite_path in self.sqlite_paths:
            path = sqlite_path.resolve()
            if path is not None:
                resolved.append(path)

        if _is_windows_with_wsl():
            for sqlite_path in self.sqlite_paths:
                if sqlite_path.platform == "linux":
                    resolved.extend(_resolve_wsl_linux_paths(sqlite_path.path))

        return resolved

    def get_resolved_plugin_paths(
        self,
    ) -> list[tuple[Path, tuple[str, ...]]]:
        """Get resolved plugin cache paths with MCP filenames.

        Returns list of (resolved_path, mcp_filenames) tuples, including
        WSL Linux-side paths when run on a Windows host with WSL.
        """
        if not self.plugin_paths:
            return []
        resolved: list[tuple[Path, tuple[str, ...]]] = []
        for pp in self.plugin_paths:
            path = pp.resolve()
            if path is not None:
                resolved.append((path, pp.mcp_filenames))
        if _is_windows_with_wsl():
            for pp in self.plugin_paths:
                if pp.platform == "linux":
                    for wsl_path in _resolve_wsl_linux_paths(pp.path):
                        resolved.append((wsl_path, pp.mcp_filenames))
        return resolved

    def get_resolved_extensions_paths(
        self,
    ) -> list[tuple[Path, str]]:
        """Get resolved extension paths with prefix.

        Includes WSL Linux-side paths when run on a Windows host with WSL.

        Returns list of (resolved_path, prefix) tuples.
        """
        if not self.extensions_paths:
            return []
        resolved: list[tuple[Path, str]] = []
        for ep in self.extensions_paths:
            path = ep.resolve()
            if path is not None:
                resolved.append((path, ep.prefix))
        if _is_windows_with_wsl():
            for ep in self.extensions_paths:
                if ep.platform == "linux":
                    for wsl_path in _resolve_wsl_linux_paths(ep.path):
                        resolved.append((wsl_path, ep.prefix))
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
#   When adding or updating clients, also update the "Supported Clients" tables
#   and "Presence-only clients" list in docs/shadow-ai/detect/index.mdx. A
#   presence-only client is one with no config paths (paths=[]).
#   tests/test_docs_client_sync.py enforces this so drift fails CI instead of
#   silently shipping stale docs.
#
# =============================================================================

MCP_CLIENTS: list[MCPClientDefinition] = [
    MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[
            ConfigPath("~/.cursor/mcp.json", platform="macos"),
            ConfigPath("~/.cursor/mcp.json", platform="linux"),
            ConfigPath("%USERPROFILE%/.cursor/mcp.json", platform="windows"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".cursor/mcp.json",
            servers_key="mcpServers",
        ),
        plugin_paths=[
            PluginPath("~/.cursor/plugins/cache/cursor-public", platform="macos"),
            PluginPath("~/.cursor/plugins/cache/cursor-public", platform="linux"),
            PluginPath(
                "%USERPROFILE%/.cursor/plugins/cache/cursor-public",
                platform="windows",
            ),
        ],
        process_signatures=[
            "cursor.app/contents/macos/cursor",
            "\\cursor\\cursor.exe",
            "/share/cursor/cursor",
        ],
        settings_override_flags=[
            SettingsOverrideFlag("--user-data-dir"),
            SettingsOverrideFlag("--extensions-dir"),
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["Cursor.app"],
            cli_binaries=["cursor"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Cursor"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/cursor/Cursor.exe",
                "%PROGRAMFILES%/cursor/Cursor.exe",
            ],
            linux_desktop_ids=["cursor.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Cursor",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Cursor", platform="windows"),
                PlatformPath("~/.config/Cursor", platform="linux"),
            ],
        ),
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
                "%LOCALAPPDATA%/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/"
                "Claude/extensions-installations.json",
                platform="windows",
            ),
            ConfigPath(
                "~/.config/Claude/extensions-installations.json",
                platform="linux",
            ),
            ConfigPath(
                "~/Library/Application Support/Claude/claude_desktop_config.json",
                platform="macos",
            ),
            ConfigPath(
                "%APPDATA%/Claude/claude_desktop_config.json",
                platform="windows",
            ),
            ConfigPath(
                "%LOCALAPPDATA%/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/"
                "Claude/claude_desktop_config.json",
                platform="windows",
            ),
            ConfigPath(
                "~/.config/Claude/claude_desktop_config.json",
                platform="linux",
            ),
        ],
        servers_key="extensions",
        additional_servers_keys=["mcpServers"],
        project_config=None,
        process_signatures=[
            "claude.app/contents/macos/claude",
            "\\claude\\claude.exe",
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["Claude.app"],
            cli_binaries=["claude-desktop"],
            probe_cli_version=False,
            windows_install_dirs=[
                "%LOCALAPPDATA%/AnthropicClaude/claude.exe",
            ],
            linux_desktop_ids=["com.anthropic.Claude.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Claude",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Claude", platform="windows"),
                PlatformPath(
                    "%LOCALAPPDATA%/Packages/Claude_pzs8sxrjxfjjc",
                    platform="windows",
                ),
                PlatformPath("~/.config/Claude", platform="linux"),
            ],
        ),
        notes="Extensions via extensions-installations.json and manual mcpServers via claude_desktop_config.json. "
        "Also covers Claude Cowork which shares the same config.",
    ),
    MCPClientDefinition(
        name="claude_code",
        display_name="Claude Code",
        paths=[
            ConfigPath("~/.claude.json", platform="macos"),
            ConfigPath("~/.claude.json", platform="linux"),
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
        process_signatures=[
            "/claude-code/",
            "\\claude-code\\",
        ],
        settings_override_flags=[
            SettingsOverrideFlag("--settings"),
            SettingsOverrideFlag(
                "--mcp-config",
                variadic=True,
                mcp_config="file",
            ),
            SettingsOverrideFlag("--strict-mcp-config", takes_value=False),
        ],
        install_probe=InstallProbe(
            vscode_extension_ids=["anthropic.claude-code"],
            npm_packages=[
                NpmPackage(name="@anthropic-ai/claude-code", bin_name="claude")
            ],
            cli_binaries=["claude"],
            windows_display_name_prefixes=["Claude Code"],
            windows_install_dirs=["%USERPROFILE%/.local/bin/claude.exe"],
            probe_config_parents=False,
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
            ConfigPath("~/.config/Code/User/mcp.json", platform="linux"),
        ],
        servers_key="servers",  # VS Code uses "servers" NOT "mcpServers"!
        project_config=ProjectConfigPattern(
            relative_path=".vscode/mcp.json",
            servers_key="servers",  # Project config also uses "servers"
        ),
        process_signatures=[
            "visual studio code.app/contents/macos/",
            "\\microsoft vs code\\code.exe",
            "/share/code/code",
        ],
        settings_override_flags=[
            SettingsOverrideFlag("--user-data-dir", mcp_config="user_data_dir"),
            SettingsOverrideFlag("--extensions-dir"),
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["Visual Studio Code.app"],
            cli_binaries=["code"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Microsoft Visual Studio Code"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Microsoft VS Code/Code.exe",
                "%PROGRAMFILES%/Microsoft VS Code/Code.exe",
            ],
            linux_desktop_ids=["code.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Code",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Code", platform="windows"),
                PlatformPath("~/.config/Code", platform="linux"),
            ],
        ),
        notes="VS Code uses 'servers' key (not 'mcpServers') for both global and project configs",
    ),
    MCPClientDefinition(
        name="windsurf",
        display_name="Windsurf",
        paths=[
            ConfigPath("~/.codeium/windsurf/mcp_config.json", platform="macos"),
            ConfigPath("~/.codeium/windsurf/mcp_config.json", platform="linux"),
            ConfigPath(
                "%USERPROFILE%/.codeium/windsurf/mcp_config.json", platform="windows"
            ),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".windsurf/mcp_config.json",
            servers_key="mcpServers",
        ),
        process_signatures=[
            "windsurf.app/contents/macos/",
            "\\windsurf\\windsurf.exe",
        ],
        settings_override_flags=[
            SettingsOverrideFlag("--user-data-dir"),
            SettingsOverrideFlag("--extensions-dir"),
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["Windsurf.app", "Devin.app"],
            cli_binaries=["windsurf", "devin-desktop"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Windsurf", "Devin"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Windsurf/Windsurf.exe",
                "%LOCALAPPDATA%/Programs/Devin/Devin.exe",
                "%PROGRAMFILES%/Windsurf/Windsurf.exe",
                "%PROGRAMFILES%/Devin/Devin.exe",
            ],
            linux_desktop_ids=["windsurf.desktop", "devin-desktop.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Windsurf",
                    platform="macos",
                ),
                PlatformPath(
                    "~/Library/Application Support/Devin",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Windsurf", platform="windows"),
                PlatformPath("%APPDATA%/Devin", platform="windows"),
                PlatformPath("~/.config/Windsurf", platform="linux"),
                PlatformPath("~/.config/Devin", platform="linux"),
            ],
        ),
        notes="Has both global and project-level (.windsurf/mcp_config.json) configs",
    ),
    MCPClientDefinition(
        name="goose",
        display_name="Goose",
        paths=[
            ConfigPath("~/.config/goose/config.yaml", platform="macos"),
            ConfigPath("~/.config/goose/config.yaml", platform="linux"),
            ConfigPath("%APPDATA%/Block/goose/config/config.yaml", platform="windows"),
        ],
        servers_key="extensions",
        config_format="yaml",
        entry_format="goose",
        project_config=None,  # Goose only has global config
        install_probe=InstallProbe(
            macos_app_bundles=["Goose.app"],
            cli_binaries=["goose"],
            windows_install_dirs=["%USERPROFILE%/.local/bin/goose.exe"],
            linux_desktop_ids=[
                "goose.desktop",
                "Goose.desktop",
            ],
            config_dirs=[
                PlatformPath("$GOOSE_PATH_ROOT", platform="all"),
                PlatformPath("~/.config/goose", platform="macos"),
                PlatformPath("~/.config/goose", platform="linux"),
                PlatformPath("~/.local/share/goose", platform="macos"),
                PlatformPath("~/.local/share/goose", platform="linux"),
                PlatformPath("~/.local/state/goose", platform="macos"),
                PlatformPath("~/.local/state/goose", platform="linux"),
                PlatformPath("%APPDATA%/Block/goose", platform="windows"),
            ],
        ),
        notes="YAML format. Uses 'extensions' key with enabled filtering. cmd/envs instead of command/env.",
    ),
    MCPClientDefinition(
        name="zed",
        display_name="Zed",
        paths=[
            ConfigPath("~/.config/zed/settings.json", platform="macos"),
            ConfigPath("~/.config/zed/settings.json", platform="linux"),
            ConfigPath("%APPDATA%/Zed/settings.json", platform="windows"),
        ],
        servers_key="context_servers",
        entry_format="zed",
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
                "~/.local/share/zed/extensions/installed",
                platform="linux",
                prefix="mcp-server-",
            ),
            ExtensionsPath(
                "%LOCALAPPDATA%/Zed/extensions/installed",
                platform="windows",
                prefix="mcp-server-",
            ),
        ],
        process_signatures=[
            "zed.app/contents/macos/zed",
            "zed.app/contents/macos/cli",
            "zed preview.app/contents/macos/zed",
            "zed preview.app/contents/macos/cli",
            "/.local/zed.app/bin/zed",
            "/.local/zed-preview.app/bin/zed",
            "\\programs\\zed\\zed.exe",
            "\\programs\\zed preview\\zed.exe",
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["Zed.app", "Zed Preview.app"],
            cli_binaries=["zed", "zed-preview"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Zed"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Zed/Zed.exe",
                "%LOCALAPPDATA%/Programs/Zed Preview/Zed.exe",
                "%PROGRAMFILES%/Zed/Zed.exe",
                "%PROGRAMFILES%/Zed Preview/Zed.exe",
            ],
            linux_desktop_ids=[
                "dev.zed.Zed.desktop",
                "dev.zed.Zed-Preview.desktop",
            ],
            config_dirs=[
                PlatformPath("~/.config/zed", platform="macos"),
                PlatformPath("~/.config/zed", platform="linux"),
                PlatformPath("%APPDATA%/Zed", platform="windows"),
                PlatformPath(
                    "~/Library/Application Support/Zed",
                    platform="macos",
                ),
                PlatformPath("~/.local/share/zed", platform="linux"),
                PlatformPath("%LOCALAPPDATA%/Zed", platform="windows"),
            ],
        ),
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
        entry_format="opencode",
        project_config=ProjectConfigPattern(
            relative_path="opencode.json",
            servers_key="mcp",
        ),
        process_signatures=[
            "/.opencode/bin/opencode",
            "/cellar/opencode/",
            "opencode.app/contents/macos/opencode",
            "\\programs\\@opencode-aidesktop\\opencode.exe",
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["OpenCode.app"],
            npm_packages=[NpmPackage(name="opencode-ai", bin_name="opencode")],
            cli_binaries=["opencode"],
            windows_display_name_prefixes=["OpenCode"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/@opencode-aidesktop/OpenCode.exe"
            ],
            linux_desktop_ids=[
                "ai.opencode.desktop.desktop",
                "opencode-desktop.desktop",
            ],
            config_dirs=[
                PlatformPath("$OPENCODE_CONFIG_DIR", platform="all"),
                PlatformPath("~/.config/opencode", platform="all"),
                PlatformPath("~/.local/share/opencode", platform="all"),
                PlatformPath("~/.local/state/opencode", platform="all"),
            ],
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
        entry_format="codex",
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
        process_signatures=[
            "/.codex/packages/standalone/",
            "/caskroom/codex/",
            "\\programs\\openai\\codex\\bin\\codex.exe",
        ],
        install_probe=InstallProbe(
            npm_packages=[NpmPackage(name="@openai/codex", bin_name="codex")],
            cli_binaries=["codex"],
            windows_display_name_prefixes=["Codex CLI"],
            windows_install_dirs=["%LOCALAPPDATA%/Programs/OpenAI/Codex/bin/codex.exe"],
            config_dirs=[
                PlatformPath("$CODEX_HOME", platform="all"),
                PlatformPath("~/.codex", platform="all"),
            ],
        ),
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
        install_probe=InstallProbe(
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Code/User/globalStorage/"
                    "saoudrizwan.claude-dev",
                    platform="macos",
                ),
                PlatformPath(
                    "%APPDATA%/Code/User/globalStorage/saoudrizwan.claude-dev",
                    platform="windows",
                ),
                PlatformPath(
                    "~/.config/Code/User/globalStorage/saoudrizwan.claude-dev",
                    platform="linux",
                ),
            ],
        ),
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
        install_probe=InstallProbe(
            cli_binaries=["cline"],
            probe_config_parents=False,
        ),
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
        process_signatures=[
            "/cellar/gemini-cli/",
        ],
        install_probe=InstallProbe(
            npm_packages=[NpmPackage(name="@google/gemini-cli", bin_name="gemini")],
            cli_binaries=["gemini"],
            probe_config_parents=False,
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
        install_probe=InstallProbe(
            macos_app_bundles=["Antigravity.app", "Antigravity IDE.app"],
            cli_binaries=["agy", "antigravity", "antigravity-ide"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Antigravity"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/antigravity/Antigravity.exe",
                "%LOCALAPPDATA%/Programs/Antigravity IDE/Antigravity IDE.exe",
                "%LOCALAPPDATA%/agy/bin/agy.exe",
            ],
            linux_desktop_ids=["antigravity.desktop"],
            config_dirs=[
                PlatformPath("~/.antigravity", platform="all"),
                PlatformPath("~/.antigravity-ide", platform="all"),
                PlatformPath("~/.gemini/antigravity", platform="all"),
                PlatformPath("~/.gemini/antigravity-ide", platform="all"),
                PlatformPath("~/.gemini/antigravity-cli", platform="all"),
            ],
        ),
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
            requires_client_presence=True,
        ),
        additional_project_configs=[
            ProjectConfigPattern(
                relative_path=".github/mcp.json",
                servers_key="mcpServers",
            ),
        ],
        process_signatures=[
            "/.local/bin/copilot",
            "/caskroom/copilot-cli/",
            "\\microsoft\\winget\\packages\\github.copilot_",
        ],
        install_probe=InstallProbe(
            npm_packages=[NpmPackage(name="@github/copilot", bin_name="copilot")],
            cli_binaries=["copilot"],
            windows_display_name_prefixes=["Copilot CLI", "GitHub Copilot CLI"],
            config_dirs=[
                PlatformPath("$COPILOT_HOME", platform="all"),
                PlatformPath("~/.copilot", platform="all"),
            ],
        ),
        notes="$COPILOT_HOME overrides ~/.copilot. Project configs: .mcp.json "
        "and .github/mcp.json use mcpServers. Shared .mcp.json attribution "
        "requires independent Copilot presence.",
    ),
    MCPClientDefinition(
        name="smithery_cli",
        display_name="Smithery CLI",
        paths=[],
        install_probe=InstallProbe(
            npm_packages=[NpmPackage(name="@smithery/cli", bin_name="smithery")],
            cli_binaries=["smithery"],
        ),
        notes="Presence-only npm CLI; no client MCP configuration.",
    ),
    MCPClientDefinition(
        name="mcp_inspector",
        display_name="MCP Inspector",
        paths=[],
        install_probe=InstallProbe(
            npm_packages=[
                NpmPackage(
                    name="@modelcontextprotocol/inspector",
                    bin_name="mcp-inspector",
                )
            ],
            cli_binaries=["mcp-inspector"],
        ),
        notes="Presence-only official MCP npm tool.",
    ),
    MCPClientDefinition(
        name="mcp_server_everything",
        display_name="Everything MCP Server",
        paths=[],
        install_probe=InstallProbe(
            npm_packages=[
                NpmPackage(
                    name="@modelcontextprotocol/server-everything",
                    bin_name="mcp-server-everything",
                )
            ],
            cli_binaries=["mcp-server-everything"],
        ),
        notes="Presence-only official MCP npm server.",
    ),
    MCPClientDefinition(
        name="mcp_server_filesystem",
        display_name="Filesystem MCP Server",
        paths=[],
        install_probe=InstallProbe(
            npm_packages=[
                NpmPackage(
                    name="@modelcontextprotocol/server-filesystem",
                    bin_name="mcp-server-filesystem",
                )
            ],
            cli_binaries=["mcp-server-filesystem"],
        ),
        notes="Presence-only official MCP npm server.",
    ),
    MCPClientDefinition(
        name="mcp_server_memory",
        display_name="Memory MCP Server",
        paths=[],
        install_probe=InstallProbe(
            npm_packages=[
                NpmPackage(
                    name="@modelcontextprotocol/server-memory",
                    bin_name="mcp-server-memory",
                )
            ],
            cli_binaries=["mcp-server-memory"],
        ),
        notes="Presence-only official MCP npm server.",
    ),
    MCPClientDefinition(
        name="mcp_server_sequential_thinking",
        display_name="Sequential Thinking MCP Server",
        paths=[],
        install_probe=InstallProbe(
            npm_packages=[
                NpmPackage(
                    name="@modelcontextprotocol/server-sequential-thinking",
                    bin_name="mcp-server-sequential-thinking",
                )
            ],
            cli_binaries=["mcp-server-sequential-thinking"],
        ),
        notes="Presence-only official MCP npm server.",
    ),
    MCPClientDefinition(
        name="mcp_server_fetch",
        display_name="Fetch MCP Server",
        paths=[],
        install_probe=InstallProbe(
            pip_packages=[PipPackage("mcp-server-fetch")],
        ),
        notes="Presence-only official MCP Python server.",
    ),
    MCPClientDefinition(
        name="mcp_server_git",
        display_name="Git MCP Server",
        paths=[],
        install_probe=InstallProbe(
            pip_packages=[PipPackage("mcp-server-git")],
        ),
        notes="Presence-only official MCP Python server.",
    ),
    MCPClientDefinition(
        name="mcp_server_time",
        display_name="Time MCP Server",
        paths=[],
        install_probe=InstallProbe(
            pip_packages=[PipPackage("mcp-server-time")],
        ),
        notes="Presence-only official MCP Python server.",
    ),
    MCPClientDefinition(
        name="warp",
        display_name="Warp",
        paths=[
            ConfigPath("~/.warp/.mcp.json", platform="macos"),
            ConfigPath("~/.warp/.mcp.json", platform="linux"),
            ConfigPath("%USERPROFILE%/.warp/.mcp.json", platform="windows"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".warp/.mcp.json",
            servers_key="mcpServers",
        ),
        sqlite_paths=[
            # macOS sandboxed Group Container, Stable + Preview channels.
            ConfigPath(
                "~/Library/Group Containers/2BBY89MBSN.dev.warp/Library/"
                "Application Support/dev.warp.Warp-Stable/warp.sqlite",
                platform="macos",
            ),
            ConfigPath(
                "~/Library/Group Containers/2BBY89MBSN.dev.warp/Library/"
                "Application Support/dev.warp.Warp-Preview/warp.sqlite",
                platform="macos",
            ),
            ConfigPath("%LOCALAPPDATA%/warp/Warp/data/warp.sqlite", platform="windows"),
            ConfigPath(
                "%LOCALAPPDATA%/warp/WarpPreview/data/warp.sqlite",
                platform="windows",
            ),
            # Linux honors XDG_STATE_HOME, defaulting to ~/.local/state (both
            # candidates listed, mirroring the $CLINE_DIR / ~/.cline pattern).
            ConfigPath("$XDG_STATE_HOME/warp-terminal/warp.sqlite", platform="linux"),
            ConfigPath(
                "$XDG_STATE_HOME/warp-terminal-preview/warp.sqlite", platform="linux"
            ),
            ConfigPath("~/.local/state/warp-terminal/warp.sqlite", platform="linux"),
            ConfigPath(
                "~/.local/state/warp-terminal-preview/warp.sqlite", platform="linux"
            ),
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["Warp.app", "WarpPreview.app"],
            cli_binaries=["warp-terminal", "warp-terminal-preview"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Warp"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Warp/warp.exe",
                "%LOCALAPPDATA%/Programs/WarpPreview/preview.exe",
                "%PROGRAMFILES%/Warp/warp.exe",
                "%PROGRAMFILES%/WarpPreview/preview.exe",
            ],
            linux_desktop_ids=[
                "dev.warp.Warp.desktop",
                "dev.warp.WarpPreview.desktop",
            ],
            config_dirs=[
                PlatformPath("~/.warp", platform="macos"),
                PlatformPath("~/.warp-preview", platform="macos"),
                PlatformPath("%LOCALAPPDATA%/warp/Warp", platform="windows"),
                PlatformPath(
                    "%LOCALAPPDATA%/warp/WarpPreview",
                    platform="windows",
                ),
                PlatformPath("~/.config/warp-terminal", platform="linux"),
                PlatformPath(
                    "~/.config/warp-terminal-preview",
                    platform="linux",
                ),
            ],
        ),
        notes="JSON. Global ~/.warp/.mcp.json; project .warp/.mcp.json. "
        "Stable+Preview share ~/.warp/. No plugin marketplace. "
        "In-app gallery servers live in warp.sqlite (mcp_server_installations) "
        "at sqlite_paths; scan/warp_sqlite.py reads + merges them into the "
        "global warp config.",
    ),
    MCPClientDefinition(
        name="kimi_code",
        display_name="Kimi Code",
        paths=[
            ConfigPath("$KIMI_CODE_HOME/mcp.json", platform="all"),
            ConfigPath("~/.kimi-code/mcp.json", platform="all"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".kimi-code/mcp.json",
            servers_key="mcpServers",
        ),
        install_probe=InstallProbe(
            config_dirs=[
                PlatformPath("$KIMI_CODE_HOME", platform="all"),
                PlatformPath("~/.kimi-code", platform="all"),
            ],
        ),
        notes="Honors $KIMI_CODE_HOME; default ~/.kimi-code. Servers live in "
        "mcp.json — config.toml only carries MCP timeouts. Transport is "
        "inferred (command=stdio, url=streamable HTTP) with explicit "
        "transport=sse for legacy SSE; gating key is 'enabled'. Bare kimi is "
        "omitted because the legacy Python kimi-cli (~/.kimi) ships the same "
        "command as a different product.",
    ),
    MCPClientDefinition(
        name="pi",
        display_name="Pi Coding Agent",
        paths=[
            ConfigPath("$PI_CODING_AGENT_DIR/mcp.json", platform="all"),
            ConfigPath("~/.pi/agent/mcp.json", platform="all"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".pi/mcp.json",
            servers_key="mcpServers",
        ),
        install_probe=InstallProbe(
            config_files=[
                PlatformPath("$PI_CODING_AGENT_DIR/settings.json", platform="all"),
                PlatformPath("~/.pi/agent/settings.json", platform="all"),
            ],
            # ~/.pi/agent is not a presence signal: third-party hosts pre-seed
            # extensions/ there on machines where Pi was never installed, so
            # parent-directory tracing would report a phantom install.
            probe_config_parents=False,
        ),
        notes="Earendil's terminal agent (not Inflection's Pi chatbot). Pi core "
        "ships no MCP; mcp.json is read by the pi-mcp-adapter extension, so the "
        "file is absent until a user installs it. Servers carry no type/transport "
        "field (command=stdio, url=HTTP, socket=uds) and gate on 'disabled'. Bare "
        "pi is omitted from CLI probes as a collision-prone command.",
    ),
    MCPClientDefinition(
        name="intellij_idea_community",
        display_name="IntelliJ IDEA Community",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["IntelliJ IDEA CE.app"],
            windows_display_name_prefixes=["IntelliJ IDEA Community"],
            linux_desktop_ids=["jetbrains-idea-ce.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/JetBrains/IdeaIC*",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/JetBrains/IdeaIC*", platform="windows"),
                PlatformPath("~/.config/JetBrains/IdeaIC*", platform="linux"),
                PlatformPath("~/.local/share/JetBrains/IdeaIC*", platform="linux"),
            ],
        ),
        notes="Presence-only; detected independently of Junie MCP configuration.",
    ),
    MCPClientDefinition(
        name="junie",
        display_name="JetBrains Junie",
        paths=[
            ConfigPath("~/.junie/mcp/mcp.json", platform="all"),
            # Pre-2026 flat layout, documented once on the JetBrains blog and
            # kept as a secondary candidate; current docs all use mcp/mcp.json.
            ConfigPath("~/.junie/mcp.json", platform="all"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".junie/mcp/mcp.json",
            servers_key="mcpServers",
        ),
        install_probe=InstallProbe(
            cli_binaries=["junie"],
            config_dirs=[
                PlatformPath("~/.junie", platform="all"),
                PlatformPath("~/.local/share/junie", platform="macos"),
                PlatformPath("~/.local/share/junie", platform="linux"),
            ],
        ),
        notes="~/.junie is shared by the IDE plugin and the CLI; the plugin's MCP "
        "Settings page writes JSON here, not into the IDE's XML options. Servers "
        "carry no type/transport field (command=local, url=remote). config.json "
        "'mcp-locations' can add further MCP dirs, so default paths can "
        "under-report. No Windows uninstall entry exists (npm/brew/script only).",
    ),
    MCPClientDefinition(
        name="kilo_code",
        display_name="Kilo Code",
        paths=[
            ConfigPath("$KILO_CONFIG", platform="all"),
            # Windows really is ~/.config too: Kilo resolves the root through
            # xdg-basedir, which falls back to homedir/.config on every OS.
            ConfigPath("~/.config/kilo/kilo.jsonc", platform="all"),
            # Marketplace MCP installs write strict JSON, not JSONC.
            ConfigPath("~/.config/kilo/kilo.json", platform="all"),
            ConfigPath("~/.config/kilo/config.json", platform="all"),
            ConfigPath("~/.kilo/kilo.jsonc", platform="all"),
            # Legacy Cline-lineage store, still merged on every config load.
            ConfigPath(
                "~/Library/Application Support/Code/User/globalStorage/"
                "kilocode.kilo-code/settings/mcp_settings.json",
                platform="macos",
            ),
            ConfigPath(
                "%APPDATA%/Code/User/globalStorage/kilocode.kilo-code/settings/"
                "mcp_settings.json",
                platform="windows",
            ),
            ConfigPath(
                "~/.config/Code/User/globalStorage/kilocode.kilo-code/settings/"
                "mcp_settings.json",
                platform="linux",
            ),
        ],
        servers_key="mcp",
        additional_servers_keys=["mcpServers"],
        entry_format="kilo_code",
        project_config=ProjectConfigPattern(
            relative_path=".kilo/kilo.jsonc",
            servers_key="mcp",
        ),
        additional_project_configs=[
            ProjectConfigPattern(
                relative_path="kilo.json",
                servers_key="mcp",
            ),
            ProjectConfigPattern(
                relative_path="kilo.jsonc",
                servers_key="mcp",
            ),
            ProjectConfigPattern(
                relative_path=".kilo/kilo.json",
                servers_key="mcp",
            ),
            ProjectConfigPattern(
                relative_path=".kilo/mcp.json",
                servers_key="mcpServers",
            ),
            ProjectConfigPattern(
                relative_path=".kilocode/mcp.json",
                servers_key="mcpServers",
            ),
        ],
        install_probe=InstallProbe(
            cli_binaries=["kilocode"],
            config_dirs=[
                PlatformPath("~/.config/kilo", platform="all"),
                PlatformPath("~/.kilo", platform="all"),
                PlatformPath("~/.kilocode", platform="all"),
            ],
        ),
        notes="Two live config generations. Modern kilo.jsonc keys servers under "
        "'mcp' in the embedded OpenCode format (type=local|remote, command[], "
        "environment, enabled); the legacy VS Code globalStorage "
        "mcp_settings.json keys them under 'mcpServers' in the standard Cline "
        "format and is still merged at runtime, not just migrated. Bare kilo is "
        "omitted as collision-prone. Legacy alwaysAllow entries are dropped by "
        "Kilo's own migration, so auto-approved tools can vanish silently.",
    ),
    MCPClientDefinition(
        name="devin_cli",
        display_name="Devin CLI",
        paths=[
            ConfigPath("~/.config/devin/mcp_config.json", platform="macos"),
            ConfigPath("~/.config/devin/mcp_config.json", platform="linux"),
            ConfigPath("%APPDATA%/devin/mcp_config.json", platform="windows"),
            # Pre-v3000.3 servers lived in config.json and are migrated out on
            # startup; scanned so un-upgraded hosts still report.
            ConfigPath("~/.config/devin/config.json", platform="macos"),
            ConfigPath("~/.config/devin/config.json", platform="linux"),
            ConfigPath("%APPDATA%/devin/config.json", platform="windows"),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".devin/mcp_config.json",
            servers_key="mcpServers",
        ),
        additional_project_configs=[
            ProjectConfigPattern(
                relative_path=".devin/mcp_config.local.json",
                servers_key="mcpServers",
            ),
            ProjectConfigPattern(
                relative_path=".devin/config.json",
                servers_key="mcpServers",
            ),
        ],
        install_probe=InstallProbe(
            cli_binaries=["devin"],
            config_dirs=[
                PlatformPath("~/.config/devin", platform="macos"),
                PlatformPath("~/.config/devin", platform="linux"),
                PlatformPath("%APPDATA%/devin", platform="windows"),
            ],
        ),
        notes="Cognition's terminal agent, a separate surface from Devin Desktop "
        "(the renamed Windsurf, covered by the windsurf entry at "
        "~/.codeium/windsurf/mcp_config.json). Remote servers use transport "
        "http|sse and may carry inline oauthClientSecret. ~/.devin is omitted as "
        "a signal because the desktop app creates it too.",
    ),
    MCPClientDefinition(
        name="roo_code",
        display_name="Roo Code",
        paths=[
            ConfigPath(
                "~/Library/Application Support/Code/User/globalStorage/"
                "rooveterinaryinc.roo-cline/settings/mcp_settings.json",
                platform="macos",
            ),
            ConfigPath(
                "%APPDATA%/Code/User/globalStorage/rooveterinaryinc.roo-cline/"
                "settings/mcp_settings.json",
                platform="windows",
            ),
            ConfigPath(
                "~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/"
                "settings/mcp_settings.json",
                platform="linux",
            ),
        ],
        servers_key="mcpServers",
        project_config=ProjectConfigPattern(
            relative_path=".roo/mcp.json",
            servers_key="mcpServers",
        ),
        install_probe=InstallProbe(
            cli_binaries=["roo"],
            probe_cli_version=False,
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Code/User/globalStorage/"
                    "rooveterinaryinc.roo-cline",
                    platform="macos",
                ),
                PlatformPath(
                    "%APPDATA%/Code/User/globalStorage/rooveterinaryinc.roo-cline",
                    platform="windows",
                ),
                PlatformPath(
                    "~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline",
                    platform="linux",
                ),
                PlatformPath("~/.roo", platform="all"),
            ],
        ),
        notes="Roo Code is sunset but installed extensions remain detectable. "
        "Both global mcp_settings.json and project .roo/mcp.json use mcpServers.",
    ),
    # Presence-only clients: these participate in installed-client inventory
    # but intentionally have no MCP config paths yet.
    MCPClientDefinition(
        name="ollama",
        display_name="Ollama",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Ollama.app"],
            cli_binaries=["ollama"],
            windows_display_name_prefixes=["Ollama"],
            windows_install_dirs=["%LOCALAPPDATA%/Programs/Ollama"],
            config_dirs=[
                PlatformPath("~/.ollama", platform="all"),
                PlatformPath(
                    "~/Library/Application Support/Ollama",
                    platform="macos",
                ),
                PlatformPath("%LOCALAPPDATA%/Ollama", platform="windows"),
            ],
        ),
        notes="Presence-only model server; Ollama has no MCP client configuration.",
    ),
    MCPClientDefinition(
        name="lm_studio",
        display_name="LM Studio",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["LM Studio.app"],
            cli_binaries=["lms"],
            probe_cli_version=False,
            windows_display_name_prefixes=["LM Studio"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/LM Studio/LM Studio.exe",
                "%LOCALAPPDATA%/LM-Studio",
            ],
            linux_desktop_ids=[
                "lm-studio.desktop",
                "ai.lmstudio.lm-studio.desktop",
            ],
            config_dirs=[
                PlatformPath("~/.lmstudio", platform="all"),
                PlatformPath("~/.cache/lm-studio", platform="all"),
                PlatformPath(
                    "~/Library/Application Support/LM Studio",
                    platform="macos",
                ),
            ],
        ),
        notes="Presence-only; MCP config is ~/.lmstudio/mcp.json "
        "(legacy ~/.cache/lm-studio/mcp.json). The lms launcher is not "
        "version-probed because commands can launch the app.",
    ),
    MCPClientDefinition(
        name="jan",
        display_name="Jan",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Jan.app"],
            cli_binaries=["jan"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Jan"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Jan/Jan.exe",
                "%LOCALAPPDATA%/Programs/Jan/jan-desktop.exe",
                "%LOCALAPPDATA%/Programs/Jan",
            ],
            linux_desktop_ids=[
                "Jan.desktop",
                "ai.jan.Jan.desktop",
                "jan.desktop",
            ],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Jan",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Jan", platform="windows"),
                PlatformPath("~/.local/share/Jan", platform="linux"),
                PlatformPath("~/jan", platform="all"),
            ],
        ),
        notes="Presence-only; MCP config is <Jan data folder>/data/mcp_config.json. "
        "The jan launcher is not version-probed because it can launch the app.",
    ),
    MCPClientDefinition(
        name="cherry_studio",
        display_name="Cherry Studio",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Cherry Studio.app"],
            windows_display_name_prefixes=["Cherry Studio"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Cherry Studio/Cherry Studio.exe",
                "%PROGRAMFILES%/Cherry Studio/Cherry Studio.exe",
            ],
            linux_desktop_ids=[
                "CherryStudio.desktop",
                "Cherry Studio.desktop",
                "com.cherry_ai.CherryStudio.desktop",
            ],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/CherryStudio",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/CherryStudio", platform="windows"),
                PlatformPath("~/.config/CherryStudio", platform="linux"),
            ],
        ),
        notes="Presence-only; MCP settings are stored in app-managed IndexedDB, "
        "not a standalone configuration file.",
    ),
    MCPClientDefinition(
        name="msty",
        display_name="Msty",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=[
                "Msty.app",
                "MstyStudio.app",
                "Msty Studio.app",
            ],
            windows_display_name_prefixes=["Msty"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Msty/Msty.exe",
                "%LOCALAPPDATA%/Programs/MstyStudio/MstyStudio.exe",
            ],
            linux_desktop_ids=["Msty.desktop", "MstyStudio.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Msty",
                    platform="macos",
                ),
                PlatformPath(
                    "~/Library/Application Support/MstyStudio",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Msty", platform="windows"),
                PlatformPath("%APPDATA%/MstyStudio", platform="windows"),
                PlatformPath("~/.config/Msty", platform="linux"),
                PlatformPath("~/.config/MstyStudio", platform="linux"),
                PlatformPath("~/.msty", platform="all"),
            ],
        ),
        notes="Presence-only; covers legacy Msty and Msty Studio. Studio stores "
        "Toolbox MCP settings inside app-managed user data.",
    ),
    MCPClientDefinition(
        name="gpt4all",
        display_name="GPT4All",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["GPT4All.app"],
            windows_display_name_prefixes=["GPT4All"],
            windows_install_dirs=["%USERPROFILE%/gpt4all/bin/chat.exe"],
            linux_desktop_ids=["io.gpt4all.gpt4all.desktop"],
            config_dirs=[
                PlatformPath("~/.config/gpt4all.io", platform="macos"),
                PlatformPath(
                    "~/Library/Application Support/nomic.ai/GPT4All",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/nomic.ai", platform="windows"),
                PlatformPath(
                    "%LOCALAPPDATA%/nomic.ai/GPT4All",
                    platform="windows",
                ),
                PlatformPath("~/.config/nomic.ai", platform="linux"),
                PlatformPath(
                    "~/.local/share/nomic.ai/GPT4All",
                    platform="linux",
                ),
                PlatformPath("~/gpt4all", platform="linux"),
            ],
        ),
        notes="Presence-only; GPT4All has no MCP client configuration.",
    ),
    MCPClientDefinition(
        name="anythingllm",
        display_name="AnythingLLM",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["AnythingLLM.app"],
            windows_display_name_prefixes=["AnythingLLM"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/AnythingLLM/AnythingLLM.exe",
                "%LOCALAPPDATA%/Programs/anythingllm-desktop/AnythingLLMDesktop.exe",
                "%PROGRAMFILES%/AnythingLLM",
            ],
            linux_desktop_ids=["anythingllmdesktop.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/anythingllm-desktop",
                    platform="macos",
                ),
                PlatformPath(
                    "%APPDATA%/anythingllm-desktop",
                    platform="windows",
                ),
                PlatformPath(
                    "~/.config/anythingllm-desktop",
                    platform="linux",
                ),
            ],
        ),
        notes="Presence-only; MCP config is "
        "<app storage>/plugins/anythingllm_mcp_servers.json.",
    ),
    MCPClientDefinition(
        name="chatwise",
        display_name="ChatWise",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["ChatWise.app"],
            windows_display_name_prefixes=["ChatWise"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/ChatWise/ChatWise.exe",
                "%LOCALAPPDATA%/ChatWise/ChatWise.exe",
            ],
            linux_desktop_ids=["ChatWise.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/app.chatwise",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/app.chatwise", platform="windows"),
                PlatformPath("~/.config/app.chatwise", platform="linux"),
                PlatformPath("~/.config/ChatWise", platform="linux"),
            ],
        ),
        notes="Presence-only; MCP settings live in app.db and are managed "
        "through the ChatWise Tools UI.",
    ),
    MCPClientDefinition(
        name="chatgpt_desktop",
        display_name="ChatGPT Desktop",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["ChatGPT.app", "ChatGPT Classic.app"],
            linux_desktop_ids=["chatgpt.desktop"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/com.openai.chat",
                    platform="macos",
                ),
                PlatformPath(
                    "~/Library/Application Support/OpenAI/Codex",
                    platform="macos",
                ),
                PlatformPath(
                    "%LOCALAPPDATA%/Packages/OpenAI.Codex_2p2nqsd0c76g0",
                    platform="windows",
                ),
                PlatformPath(
                    "%LOCALAPPDATA%/Packages/OpenAI.ChatGPT-Desktop_2p2nqsd0c76g0",
                    platform="windows",
                ),
                PlatformPath("~/.config/chatgpt", platform="linux"),
            ],
        ),
        notes="Presence-only; the unified desktop app shares ~/.codex/config.toml "
        "with Codex CLI, so that path is intentionally not a ChatGPT signal.",
    ),
    MCPClientDefinition(
        name="microsoft_copilot",
        display_name="Microsoft Copilot",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Microsoft Copilot.app", "Copilot.app"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Containers/com.microsoft.copilot-mac",
                    platform="macos",
                ),
                PlatformPath(
                    "%LOCALAPPDATA%/Packages/Microsoft.Copilot_8wekyb3d8bbwe",
                    platform="windows",
                ),
            ],
        ),
        notes="Presence-only; no Linux client or local MCP config. The Windows "
        "Store package is provisioned by default on many Windows 11 devices, "
        "so its presence is not evidence of deliberate adoption.",
    ),
    MCPClientDefinition(
        name="perplexity",
        display_name="Perplexity",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Perplexity.app"],
            windows_display_name_prefixes=["Perplexity"],
            windows_install_dirs=["%LOCALAPPDATA%/Programs/Perplexity/Perplexity.exe"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Containers/ai.perplexity.mac",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Perplexity", platform="windows"),
            ],
        ),
        notes="Presence-only; MCP connectors are managed inside the app. "
        "%LOCALAPPDATA%/Perplexity is intentionally omitted because it is "
        "shared with the separate Comet browser.",
    ),
    MCPClientDefinition(
        name="raycast",
        display_name="Raycast",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Raycast.app"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/com.raycast.macos",
                    platform="macos",
                ),
                PlatformPath("~/.config/raycast", platform="macos"),
            ],
        ),
        notes="Presence-only; native MCP settings are stored in Raycast's "
        "encrypted app data. The community MCP extension uses "
        "extensions/EvanZhouDev.mcp/mcp-config.json.",
    ),
    MCPClientDefinition(
        name="replit_desktop",
        display_name="Replit Desktop",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Replit.app"],
            windows_display_name_prefixes=["Replit"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Replit/Replit.exe",
                "%LOCALAPPDATA%/Replit",
            ],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/Replit",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/Replit", platform="windows"),
            ],
        ),
        notes="Presence-only; the redesigned app supports macOS and Windows. "
        "Linux support was dropped and no local MCP config exists.",
    ),
    MCPClientDefinition(
        name="continue",
        display_name="Continue",
        paths=[],
        install_probe=InstallProbe(
            config_dirs=[
                PlatformPath("~/.continue", platform="all"),
                PlatformPath(
                    "~/Library/Application Support/Code/User/globalStorage/"
                    "continue.continue",
                    platform="macos",
                ),
                PlatformPath(
                    "%APPDATA%/Code/User/globalStorage/continue.continue",
                    platform="windows",
                ),
                PlatformPath(
                    "~/.config/Code/User/globalStorage/continue.continue",
                    platform="linux",
                ),
            ],
        ),
        notes="Presence-only; Continue stores MCP settings in config.yaml and "
        "global/project mcpServers directories. Collision-prone cn and the "
        "shell builtin continue are intentionally omitted.",
    ),
    MCPClientDefinition(
        name="amazon_q",
        display_name="Amazon Q",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Amazon Q.app"],
            cli_binaries=["qchat", "qterm"],
            probe_cli_version=False,
            linux_desktop_ids=["amazon-q.desktop"],
            config_dirs=[
                PlatformPath("~/.aws/amazonq", platform="all"),
                PlatformPath(
                    "~/Library/Application Support/amazon-q",
                    platform="macos",
                ),
                PlatformPath("~/.local/share/amazon-q", platform="linux"),
                PlatformPath(
                    "~/Library/Application Support/Code/User/globalStorage/"
                    "amazonwebservices.amazon-q-vscode",
                    platform="macos",
                ),
                PlatformPath(
                    "%APPDATA%/Code/User/globalStorage/"
                    "amazonwebservices.amazon-q-vscode",
                    platform="windows",
                ),
                PlatformPath(
                    "~/.config/Code/User/globalStorage/"
                    "amazonwebservices.amazon-q-vscode",
                    platform="linux",
                ),
            ],
        ),
        notes="Presence-only legacy family after the Kiro CLI rebrand. MCP "
        "config remains at ~/.aws/amazonq/mcp.json and .amazonq/mcp.json.",
    ),
    MCPClientDefinition(
        name="tabnine",
        display_name="Tabnine",
        paths=[],
        install_probe=InstallProbe(
            cli_binaries=["tabnine"],
            config_dirs=[
                PlatformPath("~/.tabnine", platform="all"),
                PlatformPath(
                    "~/Library/Preferences/TabNine",
                    platform="macos",
                ),
                PlatformPath(
                    "~/Library/Application Support/TabNine",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/TabNine", platform="windows"),
                PlatformPath("~/.config/TabNine", platform="linux"),
                PlatformPath(
                    "~/Library/Application Support/Code/User/globalStorage/"
                    "tabnine.tabnine-vscode",
                    platform="macos",
                ),
                PlatformPath(
                    "%APPDATA%/Code/User/globalStorage/tabnine.tabnine-vscode",
                    platform="windows",
                ),
                PlatformPath(
                    "~/.config/Code/User/globalStorage/tabnine.tabnine-vscode",
                    platform="linux",
                ),
            ],
        ),
        notes="Presence-only; MCP config may live at ~/.tabnine/mcp_servers.json, "
        "project .tabnine/mcp_servers.json, or ~/.tabnine/agent/settings.json.",
    ),
    MCPClientDefinition(
        name="kiro",
        display_name="Kiro",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Kiro.app"],
            cli_binaries=["kiro"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Kiro (User)"],
            windows_install_dirs=["%LOCALAPPDATA%/Programs/Kiro/Kiro.exe"],
            linux_desktop_ids=["kiro.desktop"],
            config_dirs=[PlatformPath("~/.kiro", platform="all")],
        ),
        notes="Presence-only; MCP configuration scanning is not yet supported.",
    ),
    MCPClientDefinition(
        name="trae",
        display_name="Trae",
        paths=[],
        process_signatures=[
            "trae.app/contents/macos/electron",
            "trae.app/contents/macos/trae",
            "\\programs\\trae\\trae.exe",
            "/usr/share/trae/trae",
        ],
        install_probe=InstallProbe(
            macos_app_bundles=["Trae.app"],
            cli_binaries=["trae"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Trae (User)"],
            windows_install_dirs=["%LOCALAPPDATA%/Programs/Trae/Trae.exe"],
            linux_desktop_ids=["trae.desktop"],
            config_dirs=[PlatformPath("~/.trae", platform="all")],
        ),
        notes="Presence-only; MCP configuration scanning is not yet supported.",
    ),
    MCPClientDefinition(
        name="traework",
        display_name="TraeWork",
        paths=[],
        process_signatures=[
            "trae solo.app/contents/macos/electron",
            "\\programs\\trae solo\\trae solo.exe",
        ],
        install_probe=InstallProbe(
            macos_app_bundles=[
                "TRAE SOLO.app",
                "TRAE SOLO CN.app",
                "TraeWork.app",
            ],
            windows_display_name_prefixes=["TraeWork (User)"],
            windows_install_dirs=["%LOCALAPPDATA%/Programs/TRAE SOLO/TRAE SOLO.exe"],
            config_dirs=[
                PlatformPath(
                    "~/Library/Application Support/TRAE SOLO",
                    platform="macos",
                ),
                PlatformPath(
                    "~/Library/Application Support/TRAE SOLO CN",
                    platform="macos",
                ),
                PlatformPath("%APPDATA%/TRAE SOLO", platform="windows"),
            ],
        ),
        notes="Presence-only standalone ByteDance workspace; tasks and MCP "
        "configuration run inside its cloud VM sandbox.",
    ),
    MCPClientDefinition(
        name="qoder",
        display_name="Qoder",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Qoder.app"],
            cli_binaries=["qoder"],
            probe_cli_version=False,
            windows_display_name_prefixes=["Qoder (User)"],
            windows_install_dirs=["%LOCALAPPDATA%/Programs/Qoder/Qoder.exe"],
            linux_desktop_ids=["qoder.desktop"],
            config_dirs=[PlatformPath("~/.qoder", platform="all")],
        ),
        notes="Presence-only; MCP configuration scanning is not yet supported.",
    ),
    MCPClientDefinition(
        name="void",
        display_name="Void",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Void.app"],
            windows_display_name_prefixes=["Void"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Void/Void.exe",
                "%PROGRAMFILES%/Void/Void.exe",
            ],
            linux_desktop_ids=["void.desktop"],
            config_dirs=[PlatformPath("~/.void-editor", platform="all")],
        ),
        notes="Presence-only; Windows user- and machine-scope installers are "
        "covered. Development is paused, but published binaries remain available.",
    ),
    MCPClientDefinition(
        name="aider",
        display_name="Aider",
        paths=[],
        process_signatures=[
            "/uv/tools/aider-chat/",
            "/pipx/venvs/aider-chat/",
            "\\uv\\tools\\aider-chat\\",
            "\\pipx\\venvs\\aider-chat\\",
            "/.local/bin/aider",
            "\\.local\\bin\\aider.exe",
        ],
        install_probe=InstallProbe(
            cli_binaries=["aider"],
            pip_packages=[PipPackage("aider-chat")],
            config_files=[PlatformPath("~/.aider.conf.yml", platform="all")],
            config_dirs=[PlatformPath("~/.aider", platform="all")],
        ),
        notes="Presence-only; MCP configuration scanning is not yet supported.",
    ),
    MCPClientDefinition(
        name="amp",
        display_name="Amp",
        paths=[],
        install_probe=InstallProbe(
            windows_install_dirs=["%USERPROFILE%/.amp/bin/amp.exe"],
            config_files=[
                PlatformPath("~/.config/amp/settings.json", platform="all"),
                PlatformPath("~/.config/amp/settings.jsonc", platform="all"),
            ],
            config_dirs=[
                PlatformPath("~/.amp", platform="all"),
            ],
        ),
        notes="Presence-only; bare amp is omitted because unrelated tools ship the same command.",
    ),
    MCPClientDefinition(
        name="crush",
        display_name="Crush",
        paths=[],
        install_probe=InstallProbe(
            cli_binaries=["crush"],
            config_dirs=[
                PlatformPath("~/.config/crush", platform="all"),
                PlatformPath("~/.local/share/crush", platform="macos"),
                PlatformPath("~/.local/share/crush", platform="linux"),
                PlatformPath("%LOCALAPPDATA%/crush", platform="windows"),
            ],
        ),
        notes="Presence-only; MCP configuration scanning is not yet supported.",
    ),
    MCPClientDefinition(
        name="droid",
        display_name="Droid",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Factory.app"],
            cli_binaries=["droid"],
            windows_install_dirs=[
                "%USERPROFILE%/bin/droid.exe",
                "%LOCALAPPDATA%/Factory",
            ],
            config_dirs=[PlatformPath("~/.factory", platform="all")],
        ),
        notes="Presence-only; broad Factory registry matching is intentionally omitted.",
    ),
    MCPClientDefinition(
        name="qwen_code",
        display_name="Qwen Code",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Qwen Code Desktop.app"],
            cli_binaries=["qwen"],
            windows_display_name_prefixes=["Qwen Code Desktop"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Qwen Code Desktop/Qwen Code Desktop.exe",
                "%LOCALAPPDATA%/qwen-code/bin/qwen.cmd",
            ],
            linux_desktop_ids=["qwen-code-desktop.desktop"],
            config_dirs=[PlatformPath("~/.qwen", platform="all")],
        ),
        notes="Presence-only; MCP configuration scanning is not yet supported.",
    ),
    MCPClientDefinition(
        name="openhands",
        display_name="OpenHands",
        paths=[],
        install_probe=InstallProbe(
            cli_binaries=["openhands", "openhands-acp", "agent-canvas"],
            probe_cli_version=False,
            config_dirs=[
                PlatformPath("~/.openhands", platform="macos"),
                PlatformPath("~/.openhands", platform="linux"),
            ],
        ),
        notes="Presence-only; Windows support is detected through WSL.",
    ),
    MCPClientDefinition(
        name="auggie",
        display_name="Auggie",
        paths=[],
        install_probe=InstallProbe(
            cli_binaries=["auggie"],
        ),
        notes="Presence-only; shared Augment IDE state is not an Auggie-specific signal.",
    ),
    MCPClientDefinition(
        name="grok_cli",
        display_name="Grok CLI",
        paths=[],
        install_probe=InstallProbe(
            windows_install_dirs=["%USERPROFILE%/.grok/bin/grok.exe"],
            config_files=[
                PlatformPath("~/.grok/bin/grok", platform="macos"),
                PlatformPath("~/.grok/bin/grok", platform="linux"),
            ],
            config_dirs=[PlatformPath("~/.grok", platform="all")],
        ),
        notes="Presence-only; exact Grok Build binary paths are probed. Bare "
        "grok and agent commands are omitted due to collisions; xAI ships no "
        "macOS desktop app.",
    ),
    MCPClientDefinition(
        name="hermes",
        display_name="Hermes",
        paths=[],
        install_probe=InstallProbe(
            macos_app_bundles=["Hermes.app"],
            cli_binaries=["hermes-agent", "hermes-acp"],
            windows_install_dirs=[
                "%LOCALAPPDATA%/Programs/Hermes/Hermes.exe",
            ],
            config_files=[
                PlatformPath("$HERMES_HOME/config.yaml", platform="all"),
                PlatformPath("~/.hermes/config.yaml", platform="macos"),
                PlatformPath("~/.hermes/config.yaml", platform="linux"),
                PlatformPath(
                    "%LOCALAPPDATA%/hermes/config.yaml",
                    platform="windows",
                ),
            ],
        ),
        notes="Presence-only; exact config.yaml avoids the unrelated Hermes relayer's config.toml.",
    ),
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
