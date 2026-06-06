"""MCP Watch scan service - orchestrates the scanning process."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import httpx
import structlog

from runlayer_cli.scan.clients import (
    MCPClientDefinition,
    get_all_clients,
    get_client_by_name,
    get_clients_with_project_configs,
)
from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    compute_config_hash,
    parse_config_file,
)
from runlayer_cli.scan.claude_code_plugins import scan_claude_code_plugins
from runlayer_cli.scan.codex_plugins import scan_codex_plugins
from runlayer_cli.scan.copilot_plugins import scan_copilot_plugins
from runlayer_cli.scan.cursor_plugins import scan_cursor_plugins
from runlayer_cli.scan.gemini_extensions import (
    process_project_gemini_extensions,
    scan_gemini_extensions,
)
from runlayer_cli.scan.opencode_plugins import scan_opencode_plugins
from runlayer_cli.scan.plugin_scanner import (
    DiscoveredPluginArtifact,
    scan_claude_code_plugin_artifacts,
    scan_claude_desktop_connectors,
    scan_codex_plugin_artifacts,
    scan_cursor_native_plugins,
    scan_opencode_plugin_artifacts,
)
from runlayer_cli.scan.device import get_device_metadata, get_or_create_device_id
from runlayer_cli.scan.openclaw_detector import build_openclaw_config, detect_openclaw
from runlayer_cli.scan.project_scanner import (
    find_files_under_home,
    scan_for_project_configs,
)
from runlayer_cli.scan.skill_scanner import (
    DiscoveredSkillArtifact,
    get_skill_search_filenames,
    process_skill_paths,
    scan_global_skills,
    tag_skills_with_plugins,
)
from runlayer_cli.scan.warp_sqlite import enrich_configurations_with_warp_sqlite

if TYPE_CHECKING:
    from runlayer_cli.api import RunlayerClient

logger = structlog.get_logger(__name__)

SubmissionStatus = Literal["success", "unsupported", "failed"]


def _normalize_transport_type_for_api(transport_type: str) -> str:
    """Map client transport aliases to backend API enum values."""
    if transport_type in {"streamable-http", "streamable_http"}:
        return "streaming-http"
    return transport_type


def scan_extensions_folder(client_def: MCPClientDefinition) -> list[str]:
    """Scan extensions folder for MCP server directories.

    Scans the client's extensions directories for folders matching the
    configured prefix (e.g., "mcp-server-*").

    Args:
        client_def: Client definition with extensions_paths configured

    Returns:
        List of extension folder names (e.g., ["mcp-server-brave-search"])
    """
    if not client_def.extensions_paths:
        return []

    found_extensions: list[str] = []
    for resolved, prefix in client_def.get_resolved_extensions_paths():
        if resolved.is_dir():
            try:
                for item in resolved.iterdir():
                    if item.is_dir() and item.name.startswith(prefix):
                        found_extensions.append(item.name)
                        logger.debug(
                            "Found extension folder",
                            client=client_def.name,
                            extension=item.name,
                        )
            except OSError as e:
                logger.warning(
                    "Failed to scan extensions folder",
                    client=client_def.name,
                    path=str(resolved),
                    error=str(e),
                )

    return found_extensions


def merge_extensions_with_config(
    config: MCPClientConfig,
    extension_names: list[str],
) -> None:
    """Merge discovered extensions into config, adding any not already present.

    Extensions that exist in the extensions folder but aren't already in the
    config are added as stdio servers with None command/args (the extension
    handles invocation internally).

    Args:
        config: Existing MCPClientConfig to update in-place
        extension_names: List of extension folder names from extensions folder
    """
    # Get set of existing server names for deduplication
    existing_names = {server.name for server in config.servers}

    for ext_name in extension_names:
        if ext_name not in existing_names:
            # Create server entry for extension not in settings.json
            server = MCPServerConfig(
                name=ext_name,
                type="stdio",
                command=None,
                args=None,
                url=None,
                env=None,
                headers=None,
            )
            server.config_hash = compute_config_hash(server)
            config.servers.append(server)
            existing_names.add(ext_name)  # Prevent duplicates within extension_names
            logger.debug(
                "Added extension server not in settings",
                extension=ext_name,
            )


@dataclass
class ScanResult:
    """Result of a scan operation."""

    device_id: str
    hostname: str | None
    os: str | None
    os_version: str | None
    username: str | None
    org_device_id: str | None
    scan_duration_ms: int
    collector_version: str
    configurations: list[MCPClientConfig]
    is_wsl: bool = False
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    plugins: list[DiscoveredPluginArtifact] = field(default_factory=list)

    @property
    def total_servers(self) -> int:
        return sum(len(c.servers) for c in self.configurations)

    @property
    def total_skills(self) -> int:
        return len(self.skills)

    @property
    def clients_with_servers(self) -> list[str]:
        return [c.client for c in self.configurations]

    @property
    def global_configs(self) -> list[MCPClientConfig]:
        return [c for c in self.configurations if c.config_scope == "global"]

    @property
    def project_configs(self) -> list[MCPClientConfig]:
        return [c for c in self.configurations if c.config_scope == "project"]

    @property
    def plugin_configs(self) -> list[MCPClientConfig]:
        return [c for c in self.configurations if c.config_scope == "plugin"]

    @property
    def global_skills(self) -> list[DiscoveredSkillArtifact]:
        return [s for s in self.skills if s.scope == "global"]

    @property
    def user_skills(self) -> list[DiscoveredSkillArtifact]:
        return [s for s in self.skills if s.scope == "user"]

    @property
    def project_skills(self) -> list[DiscoveredSkillArtifact]:
        return [s for s in self.skills if s.scope == "project"]

    @property
    def total_plugins(self) -> int:
        return len(self.plugins)

    def to_api_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "device_id": self.device_id,
            "hostname": self.hostname,
            "os": self.os,
            "os_version": self.os_version,
            "username": self.username,
            "org_device_id": self.org_device_id,
            "scan_duration_ms": self.scan_duration_ms,
            "collector_version": self.collector_version,
            "configurations": [
                {
                    "client": c.client,
                    "client_version": c.client_version,
                    "config_path": c.config_path,
                    "config_modified_at": c.config_modified_at,
                    "config_scope": c.config_scope,
                    "project_path": c.project_path,
                    "plugin_identifier": c.plugin_identifier,
                    "servers": [
                        {
                            "name": s.name,
                            "type": _normalize_transport_type_for_api(s.type),
                            "command": s.command,
                            "args": s.args,
                            "url": s.url,
                            "env": s.env,
                            "headers": s.headers,
                            "config_hash": s.config_hash,
                            "project_names": s.project_name,
                        }
                        for s in c.servers
                    ],
                }
                for c in self.configurations
            ],
        }
        if self.is_wsl:
            payload["is_wsl"] = True
        return payload


def scan_all_clients(
    device_id: str | None = None,
    org_device_id: str | None = None,
    collector_version: str = "unknown",
    scan_projects: bool = True,
    project_scan_timeout: int = 60,
    project_scan_depth: int = 7,
    username_override: str | None = None,
) -> ScanResult:
    """
    Scan all known MCP client configurations (global and project-level).

    Args:
        device_id: Override device ID (uses auto-generated if None)
        org_device_id: Organization-provided device ID (e.g., from MDM)
        collector_version: Version of the CLI performing the scan
        scan_projects: Whether to scan for project-level configs (default True)
        project_scan_timeout: Timeout in seconds for project scanning (default 60)
        project_scan_depth: Max directory depth for project scanning (default 5)
        username_override: Explicit username, bypasses auto-detection

    Returns:
        ScanResult with all discovered configurations
    """
    start_time = time.time()

    # Get device info
    actual_device_id = device_id or get_or_create_device_id()
    device_metadata = get_device_metadata()

    if username_override:
        device_metadata["username"] = username_override

    configurations: list[MCPClientConfig] = []

    # ==========================================================================
    # PHASE 1: Scan global/user-level configurations
    # ==========================================================================
    logger.info("Scanning global configurations")
    clients = get_all_clients()

    for client_def in clients:
        config_paths = client_def.get_config_paths()
        found_servers_in_config = False

        for config_path in config_paths:
            logger.debug(
                "Scanning global config",
                client=client_def.name,
            )

            config = parse_config_file(client_def, config_path)
            if config and config.servers:
                found_servers_in_config = True
                config.config_scope = "global"

                # For clients with extensions folders (e.g., Zed), scan and merge
                if client_def.extensions_paths:
                    extension_names = scan_extensions_folder(client_def)
                    if extension_names:
                        merge_extensions_with_config(config, extension_names)
                        logger.info(
                            "Merged extensions with config",
                            client=client_def.name,
                            extensions_found=len(extension_names),
                        )

                configurations.append(config)
                logger.info(
                    "Found MCP servers (global)",
                    client=client_def.name,
                    server_count=len(config.servers),
                )

        # If no config file had servers, check for extensions-only installations
        if not found_servers_in_config and client_def.extensions_paths:
            extension_names = scan_extensions_folder(client_def)
            if extension_names:
                # Create a config with just the extensions
                config = MCPClientConfig(
                    client=client_def.name,
                    config_path=None,
                    config_modified_at=None,
                    servers=[],
                    config_scope="global",
                )
                merge_extensions_with_config(config, extension_names)
                configurations.append(config)
                logger.info(
                    "Found MCP servers from extensions only",
                    client=client_def.name,
                    server_count=len(config.servers),
                )

    # Supplement Warp's file config with its in-app gallery sqlite installs
    # (owned + merged inside warp_sqlite to keep ordering/dedup local).
    enrich_configurations_with_warp_sqlite(configurations)

    # ==========================================================================
    # PHASE 2: Unified project-level find crawl (MCP configs + skill files)
    # ==========================================================================
    discovered_project_paths: list[Path] = []
    all_skills: list[DiscoveredSkillArtifact] = []
    gemini_proj_artifacts: list[DiscoveredPluginArtifact] = []

    if scan_projects:
        logger.info("Scanning project-level configurations and skills")
        clients_with_projects = get_clients_with_project_configs()

        # Build unified filename list for a single find crawl.
        # Use full relative path for entries with "/" to avoid matching
        # generic basenames (e.g. "config.toml") everywhere.
        mcp_filenames: list[str] = []
        for c in clients_with_projects:
            for pc in c.iter_project_configs():
                rel = pc.relative_path
                fname = rel if "/" in rel else Path(rel).name
                if fname not in mcp_filenames:
                    mcp_filenames.append(fname)

        skill_filenames = get_skill_search_filenames()
        extra_filenames = ["gemini-extension.json"]
        all_filenames = sorted(set(mcp_filenames + skill_filenames + extra_filenames))

        found_paths = find_files_under_home(
            all_filenames, project_scan_timeout, project_scan_depth
        )

        # Split results: MCP configs use the existing matcher
        project_configs = scan_for_project_configs(
            clients=clients_with_projects,
            precomputed_paths=found_paths,
        )

        for proj_config in project_configs:
            discovered_project_paths.append(proj_config.project_path)

            client_def = get_client_by_name(proj_config.client_name)
            if client_def is None:
                continue

            temp_client_def = MCPClientDefinition(
                name=client_def.name,
                display_name=client_def.display_name,
                paths=[],
                servers_key=proj_config.servers_key,
                config_format=client_def.config_format,
            )

            config = parse_config_file(temp_client_def, proj_config.config_path)
            if config and config.servers:
                config.config_scope = "project"
                config.project_path = str(proj_config.project_path)
                for server in config.servers:
                    server.project_name = config.project_path
                configurations.append(config)
                logger.info(
                    "Found MCP servers (project)",
                    client=client_def.name,
                    server_count=len(config.servers),
                )

        # Split results: skill files
        project_skill_artifacts = process_skill_paths(found_paths)
        all_skills.extend(project_skill_artifacts)

        # Split results: project-level Gemini extensions
        gemini_proj_configs, gemini_proj_artifacts = process_project_gemini_extensions(
            found_paths
        )
        if gemini_proj_configs:
            configurations.extend(gemini_proj_configs)
            logger.info(
                "Found MCP servers in project Gemini extensions",
                config_count=len(gemini_proj_configs),
            )

    # ==========================================================================
    # PHASE 3: Detect locally installed OpenClaw (shadow client)
    # ==========================================================================
    logger.info("Scanning for OpenClaw installation")
    openclaw_detection = detect_openclaw()
    if openclaw_detection.detected:
        openclaw_config = build_openclaw_config(openclaw_detection)
        if openclaw_config:
            configurations.append(openclaw_config)
            logger.info(
                "OpenClaw detected",
                summary=openclaw_detection.summary,
                server_count=len(openclaw_config.servers),
            )
    else:
        logger.debug("OpenClaw not detected")

    # ==========================================================================
    # PHASE 4: Scan Claude Code plugins for bundled MCP servers
    # ==========================================================================
    logger.info("Scanning Claude Code plugins")
    plugin_configs = scan_claude_code_plugins()
    if plugin_configs:
        configurations.extend(plugin_configs)
        plugin_server_count = sum(len(c.servers) for c in plugin_configs)
        logger.info(
            "Found MCP servers in Claude Code plugins",
            plugin_count=len(plugin_configs),
            server_count=plugin_server_count,
        )

    # ==========================================================================
    # PHASE 5: Scan Cursor plugins for bundled MCP servers
    # ==========================================================================
    logger.info("Scanning Cursor plugins")
    cursor_def = get_client_by_name("cursor")
    if cursor_def and cursor_def.plugin_paths:
        unique_project_paths = list(dict.fromkeys(discovered_project_paths))
        cursor_plugin_configs = scan_cursor_plugins(
            cursor_def,
            project_paths=unique_project_paths if scan_projects else None,
        )
        if cursor_plugin_configs:
            configurations.extend(cursor_plugin_configs)
            cursor_plugin_server_count = sum(
                len(c.servers) for c in cursor_plugin_configs
            )
            logger.info(
                "Found MCP servers in Cursor plugins",
                plugin_count=len(cursor_plugin_configs),
                server_count=cursor_plugin_server_count,
            )

    # ==========================================================================
    # PHASE 6: Scan Codex plugins for bundled MCP servers
    # ==========================================================================
    logger.info("Scanning Codex plugins")
    codex_plugin_configs = scan_codex_plugins()
    if codex_plugin_configs:
        configurations.extend(codex_plugin_configs)
        codex_plugin_server_count = sum(len(c.servers) for c in codex_plugin_configs)
        logger.info(
            "Found MCP servers in Codex plugins",
            plugin_count=len(codex_plugin_configs),
            server_count=codex_plugin_server_count,
        )

    # ==========================================================================
    # PHASE 7: Scan OpenCode plugins for bundled MCP servers
    # ==========================================================================
    logger.info("Scanning OpenCode plugins")
    opencode_plugin_configs = scan_opencode_plugins()
    if opencode_plugin_configs:
        configurations.extend(opencode_plugin_configs)
        opencode_plugin_server_count = sum(
            len(c.servers) for c in opencode_plugin_configs
        )
        logger.info(
            "Found MCP servers in OpenCode plugins",
            plugin_count=len(opencode_plugin_configs),
            server_count=opencode_plugin_server_count,
        )

    # ==========================================================================
    # PHASE 8: Scan Gemini CLI extensions for bundled MCP servers
    # ==========================================================================
    logger.info("Scanning Gemini CLI extensions")
    gemini_ext_configs, gemini_ext_artifacts = scan_gemini_extensions()
    if gemini_ext_configs:
        configurations.extend(gemini_ext_configs)
        gemini_ext_server_count = sum(len(c.servers) for c in gemini_ext_configs)
        logger.info(
            "Found MCP servers in Gemini extensions",
            extension_count=len(gemini_ext_configs),
            server_count=gemini_ext_server_count,
        )

    # ==========================================================================
    # PHASE 9: Scan Copilot CLI plugins for bundled MCP servers
    # ==========================================================================
    logger.info("Scanning Copilot CLI plugins")
    copilot_plugin_configs, copilot_plugin_artifacts = scan_copilot_plugins()
    if copilot_plugin_configs:
        configurations.extend(copilot_plugin_configs)
        copilot_plugin_server_count = sum(
            len(c.servers) for c in copilot_plugin_configs
        )
        logger.info(
            "Found MCP servers in Copilot plugins",
            plugin_count=len(copilot_plugin_configs),
            server_count=copilot_plugin_server_count,
        )

    # ==========================================================================
    # PHASE 10: Scan global (home-directory) skill paths
    # ==========================================================================
    logger.info("Scanning global skill paths")
    global_skill_artifacts = scan_global_skills()
    all_skills.extend(global_skill_artifacts)

    # ==========================================================================
    # PHASE 11: Detect installed plugins as first-class artifacts
    # ==========================================================================
    logger.info("Scanning for plugin artifacts")
    all_plugins: list[DiscoveredPluginArtifact] = []

    cursor_native = scan_cursor_native_plugins()
    all_plugins.extend(cursor_native)

    claude_code_artifacts = scan_claude_code_plugin_artifacts()
    all_plugins.extend(claude_code_artifacts)

    desktop_connectors = scan_claude_desktop_connectors()
    all_plugins.extend(desktop_connectors)

    codex_artifacts = scan_codex_plugin_artifacts()
    all_plugins.extend(codex_artifacts)

    opencode_artifacts = scan_opencode_plugin_artifacts()
    all_plugins.extend(opencode_artifacts)

    all_plugins.extend(gemini_ext_artifacts)
    if scan_projects:
        all_plugins.extend(gemini_proj_artifacts)

    all_plugins.extend(copilot_plugin_artifacts)

    # Tag skills with their owning plugin via install-path prefix matching
    plugin_path_map: dict[Path, str] = {}
    for p in all_plugins:
        if p.identifier and p.install_path:
            plugin_path_map[Path(p.install_path).resolve()] = p.identifier
    if plugin_path_map:
        tag_skills_with_plugins(all_skills, plugin_path_map)

    scan_duration_ms = int((time.time() - start_time) * 1000)

    logger.info(
        "Scan complete",
        total_configs=len(configurations),
        global_configs=len([c for c in configurations if c.config_scope == "global"]),
        project_configs=len([c for c in configurations if c.config_scope == "project"]),
        plugin_configs=len([c for c in configurations if c.config_scope == "plugin"]),
        total_servers=sum(len(c.servers) for c in configurations),
        total_skills=len(all_skills),
        total_plugins=len(all_plugins),
        duration_ms=scan_duration_ms,
    )

    return ScanResult(
        device_id=actual_device_id,
        hostname=device_metadata.get("hostname"),
        os=device_metadata.get("os"),
        os_version=device_metadata.get("os_version"),
        username=device_metadata.get("username"),
        org_device_id=org_device_id,
        scan_duration_ms=scan_duration_ms,
        collector_version=collector_version,
        configurations=configurations,
        is_wsl=device_metadata.get("is_wsl", False),
        skills=all_skills,
        plugins=all_plugins,
    )


def _device_context_dict(scan_result: ScanResult) -> dict[str, str | None]:
    return {
        "device_id": scan_result.device_id,
        "hostname": scan_result.hostname,
        "os": scan_result.os,
        "os_version": scan_result.os_version,
        "username": scan_result.username,
        "org_device_id": scan_result.org_device_id,
    }


def submit_discovered_skills(
    client: RunlayerClient,
    skills: list[DiscoveredSkillArtifact],
    scan_result: ScanResult | None = None,
) -> SubmissionStatus:
    """For each skill: lookup fingerprint, then always submit.

    When the catalog row already exists or the artifact is oversized we
    still submit (to create the per-device installation row) but strip
    file contents to save bandwidth.

    Returns whether submission succeeded, failed, or is unsupported.
    """
    device_ctx = _device_context_dict(scan_result) if scan_result else {}
    for skill in skills:
        if not skill.identifier:
            continue
        try:
            result = client.submit_skill_fingerprint(
                skill.identifier,
                skill.artifact_type,
                oversized=skill.oversized,
            )
            if result.get("unsupported"):
                return "unsupported"
            payload = skill.to_api_payload()
            if result.get("known") or skill.oversized:
                payload["files"] = []
            payload.update(device_ctx)
            client.submit_skill(payload)
        except NotImplementedError:
            logger.debug("skill_submission_not_implemented", skill=skill.name)
        except httpx.RequestError as exc:
            logger.warning(
                "skill_submission_failed",
                skill=skill.name,
                error=str(exc),
                error_type=type(exc).__name__,
            )
            return "failed"
        except Exception as exc:
            logger.warning(
                "skill_submission_failed",
                skill=skill.name,
                error=str(exc),
                error_type=type(exc).__name__,
            )
    return "success"


def submit_discovered_plugins(
    client: RunlayerClient,
    plugins: list[DiscoveredPluginArtifact],
    scan_result: ScanResult | None = None,
) -> SubmissionStatus:
    """For each plugin: lookup fingerprint, then always submit.

    When the catalog row already exists or the artifact is oversized we
    still submit (to create the per-device installation row) but strip
    file contents to save bandwidth.

    Returns whether submission succeeded, failed, or is unsupported.
    """
    device_ctx = _device_context_dict(scan_result) if scan_result else {}
    for plugin in plugins:
        if not plugin.identifier:
            continue
        try:
            result = client.submit_plugin_fingerprint(
                plugin.identifier,
            )
            if result.get("unsupported"):
                return "unsupported"
            payload = plugin.to_api_payload()
            if result.get("known") or plugin.oversized:
                payload["files"] = []
            payload.update(device_ctx)
            client.submit_plugin(payload)
        except NotImplementedError:
            logger.debug("plugin_submission_not_implemented", plugin=plugin.name)
        except httpx.RequestError as exc:
            logger.warning(
                "plugin_submission_failed",
                plugin=plugin.name,
                error=str(exc),
                error_type=type(exc).__name__,
            )
            return "failed"
        except Exception as exc:
            logger.warning(
                "plugin_submission_failed",
                plugin=plugin.name,
                error=str(exc),
                error_type=type(exc).__name__,
            )
    return "success"
