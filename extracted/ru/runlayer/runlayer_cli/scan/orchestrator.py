"""Concurrent phase 1-11 orchestration for the device scan."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from concurrent.futures import Future
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TypeVar

import structlog

from runlayer_cli import telemetry
from runlayer_cli.scan.agent_scan import (
    discover_agents,
    filter_static_skill_descendants,
)
from runlayer_cli.scan.agent_definition_scanner import (
    DiscoveredAgentDefinition,
    dedupe_agent_definitions,
    get_agent_definition_search_patterns,
    process_agent_definition_paths,
    scan_user_agent_definitions,
)
from runlayer_cli.scan.agents.detect import DiscoveredAgent
from runlayer_cli.scan.agents.manifests import agent_manifest_search_filenames
from runlayer_cli.scan.claude_code_plugins import scan_claude_code_plugins
from runlayer_cli.scan.clients import (
    MCPClientDefinition,
    _wsl_homes,
    get_client_by_name,
    get_clients_with_project_configs,
)
from runlayer_cli.scan.codex_plugins import scan_codex_plugins
from runlayer_cli.scan.concurrency import (
    ScanThreadPool,
    bounded_thread_pool,
    scan_worker_count,
)
from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    compute_config_hash,
    parse_config_file,
)
from runlayer_cli.scan.copilot_plugins import scan_copilot_plugins
from runlayer_cli.scan.cursor_plugins import scan_cursor_plugins
from runlayer_cli.scan.disguised_skills import scan_disguised_skills
from runlayer_cli.scan.renamed_plugin_caches import (
    filter_novel_plugin_artifacts,
    scan_renamed_plugin_caches,
)
from runlayer_cli.scan.gemini_extensions import (
    process_project_gemini_extensions,
    scan_gemini_extensions,
)
from runlayer_cli.scan.hidden_space_sweep import (
    HiddenSpaceScanResult,
    scan_hidden_spaces,
)
from runlayer_cli.scan.jetbrains_plugins import scan_jetbrains_plugins
from runlayer_cli.scan.opencode_plugins import scan_opencode_plugins
from runlayer_cli.scan.plugin_scanner import (
    DiscoveredPluginArtifact,
    finalize_plugin_scan_state,
    reset_plugin_scan_state,
    scan_claude_code_plugin_artifacts,
    scan_claude_desktop_connectors,
    scan_codex_plugin_artifacts,
    scan_cursor_native_plugins,
    scan_opencode_plugin_artifacts,
)
from runlayer_cli.scan.project_scanner import (
    NESTED_PROJECT_SCAN_DEPTH,
    NESTED_PROJECT_SCAN_TIMEOUT,
    find_files_and_node_modules_under_home,
    find_files_under_project_roots,
    scan_for_project_configs,
)
from runlayer_cli.scan.resource_governor import ResourceGovernor
from runlayer_cli.scan.skill_scanner import (
    DiscoveredSkillArtifact,
    clear_git_remote_cache,
    finalize_skill_scan_state,
    get_skill_search_filenames,
    process_skill_paths,
    reset_skill_scan_state,
    scan_global_skills,
    strip_duplicate_skill_files,
    tag_skills_with_plugins,
)
from runlayer_cli.scan.timing import PhaseTimer
from runlayer_cli.scan.vscode_extensions import scan_vscode_extensions
from runlayer_cli.scan.warp_sqlite import enrich_configurations_with_warp_sqlite

logger = structlog.get_logger(__name__)
_PhaseResult = TypeVar("_PhaseResult")


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
class ProjectPhaseResult:
    """Findings produced by the shared project crawl."""

    configurations: list[MCPClientConfig] = field(default_factory=list)
    discovered_project_paths: list[Path] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    gemini_artifacts: list[DiscoveredPluginArtifact] = field(default_factory=list)
    found_paths: list[Path] = field(default_factory=list)
    node_modules_paths: list[Path] = field(default_factory=list)
    agent_skill_roots: list[Path] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)


@dataclass
class GlobalPhaseResult:
    """Findings from the global-config scan (phase 1)."""

    configurations: list[MCPClientConfig] = field(default_factory=list)
    # Clients whose extensions folder produced servers; feeds client presence.
    extension_clients: set[str] = field(default_factory=set)


@dataclass
class ConcurrentScanResult:
    """Assembled findings from concurrent phases 1-11."""

    configurations: list[MCPClientConfig] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    plugins: list[DiscoveredPluginArtifact] = field(default_factory=list)
    agents: list[DiscoveredAgent] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)
    extension_clients: set[str] = field(default_factory=set)
    node_modules_paths: list[Path] = field(default_factory=list)
    hidden_space_result: HiddenSpaceScanResult = field(
        default_factory=HiddenSpaceScanResult
    )


def run_timed_phase(
    timer: PhaseTimer,
    name: str,
    governor: ResourceGovernor,
    work: Callable[[], _PhaseResult],
) -> _PhaseResult:
    """Run one phase with resource checks and duration recording."""
    with timer.phase(name):
        governor.checkpoint()
        return work()


def _submit_timed_phase(
    pool: ScanThreadPool,
    timer: PhaseTimer,
    name: str,
    governor: ResourceGovernor,
    work: Callable[[], _PhaseResult],
) -> Future[_PhaseResult]:
    def run() -> _PhaseResult:
        return run_timed_phase(timer, name, governor, work)

    return pool.submit(run)


def _scan_global_configurations(
    clients: list[MCPClientDefinition],
    governor: ResourceGovernor,
) -> GlobalPhaseResult:
    """Phase 1: scan global configs without mutating shared aggregates."""
    logger.info("Scanning global configurations")
    configurations: list[MCPClientConfig] = []
    extension_clients: set[str] = set()

    for client_def in clients:
        config_paths = client_def.get_config_paths()
        found_servers_in_config = False

        for config_path in config_paths:
            logger.debug("Scanning global config", client=client_def.name)
            governor.checkpoint()
            config = parse_config_file(client_def, config_path)
            if config and config.servers:
                found_servers_in_config = True
                config.config_scope = "global"
                if client_def.extensions_paths:
                    extension_names = scan_extensions_folder(client_def)
                    if extension_names:
                        extension_clients.add(client_def.name)
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

        if not found_servers_in_config and client_def.extensions_paths:
            extension_names = scan_extensions_folder(client_def)
            if extension_names:
                extension_clients.add(client_def.name)
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

    enrich_configurations_with_warp_sqlite(configurations)
    return GlobalPhaseResult(
        configurations=configurations,
        extension_clients=extension_clients,
    )


def _scan_project_phase(
    *,
    governor: ResourceGovernor,
    project_scan_timeout: int,
    project_scan_depth: int,
    run_static_agents: bool,
    extra_home_roots: Sequence[Path] = (),
) -> ProjectPhaseResult:
    """Phase 2: crawl once, then split project configs, skills, and extensions."""
    logger.info("Scanning project-level configurations and skills")
    clients_with_projects = get_clients_with_project_configs()

    mcp_filenames: list[str] = []
    for client in clients_with_projects:
        for project_config in client.iter_project_configs():
            relative_path = project_config.relative_path
            filename = (
                relative_path if "/" in relative_path else Path(relative_path).name
            )
            if filename not in mcp_filenames:
                mcp_filenames.append(filename)

    skill_filenames = get_skill_search_filenames()
    agent_filenames = agent_manifest_search_filenames() if run_static_agents else []
    agent_definition_patterns = get_agent_definition_search_patterns()
    all_filenames = sorted(
        set(
            mcp_filenames
            + skill_filenames
            + ["gemini-extension.json"]
            + agent_filenames
            + agent_definition_patterns
        )
    )

    with telemetry.command_span(
        "scan.phase.project_find",
        filename_count=len(all_filenames),
    ):
        crawl_result = find_files_and_node_modules_under_home(
            all_filenames,
            project_scan_timeout,
            project_scan_depth,
            governor=governor,
        )
        found_paths = crawl_result.found_paths

    configurations: list[MCPClientConfig] = []
    discovered_project_paths: list[Path] = []
    project_configs = scan_for_project_configs(
        clients=clients_with_projects,
        precomputed_paths=found_paths,
    )
    for project_config in project_configs:
        governor.checkpoint()
        discovered_project_paths.append(project_config.project_path)
        client_def = get_client_by_name(project_config.client_name)
        if client_def is None:
            continue

        temp_client_def = replace(
            client_def,
            paths=[],
            servers_key=project_config.servers_key,
        )
        config = parse_config_file(temp_client_def, project_config.config_path)
        if config and config.servers:
            config.config_scope = "project"
            config.project_path = str(project_config.project_path)
            for server in config.servers:
                server.project_name = config.project_path
            configurations.append(config)
            logger.info(
                "Found MCP servers (project)",
                client=client_def.name,
                server_count=len(config.servers),
            )

    if discovered_project_paths:
        governor.checkpoint()
        nested_patterns = sorted(set(skill_filenames + agent_definition_patterns))
        with telemetry.command_span(
            "scan.phase.project_nested_find",
            filename_count=len(nested_patterns),
            project_count=len(discovered_project_paths),
        ):
            nested_paths = find_files_under_project_roots(
                nested_patterns,
                discovered_project_paths,
                timeout=min(project_scan_timeout, NESTED_PROJECT_SCAN_TIMEOUT),
                max_depth=NESTED_PROJECT_SCAN_DEPTH,
                governor=governor,
            )
        found_paths = sorted(set(found_paths + nested_paths))

    governor.checkpoint()
    skills = process_skill_paths(
        found_paths,
        extra_home_roots=extra_home_roots,
        checkpoint=governor.checkpoint,
    )
    agent_definitions = process_agent_definition_paths(
        found_paths,
        extra_home_roots=extra_home_roots,
        logical_paths=crawl_result.logical_paths,
    )
    agent_skill_roots = [Path(skill.path) for skill in skills]
    gemini_configs, gemini_artifacts = process_project_gemini_extensions(found_paths)
    configurations.extend(gemini_configs)
    if gemini_configs:
        logger.info(
            "Found MCP servers in project Gemini extensions",
            config_count=len(gemini_configs),
        )

    return ProjectPhaseResult(
        configurations=configurations,
        discovered_project_paths=discovered_project_paths,
        skills=skills,
        gemini_artifacts=gemini_artifacts,
        found_paths=found_paths,
        node_modules_paths=crawl_result.node_modules_paths,
        agent_skill_roots=agent_skill_roots,
        agent_definitions=agent_definitions,
    )


def _log_found_servers(
    message: str,
    configurations: list[MCPClientConfig],
    *,
    count_key: str = "plugin_count",
) -> None:
    if not configurations:
        return
    logger.info(
        message,
        **{count_key: len(configurations)},
        server_count=sum(len(config.servers) for config in configurations),
    )


def _scan_cursor_plugin_phase(
    discovered_project_paths: list[Path],
) -> list[MCPClientConfig]:
    """Phase 4: scan Cursor plugins after project roots are known."""
    logger.info("Scanning Cursor plugins")
    cursor_def = get_client_by_name("cursor")
    if cursor_def is None or not cursor_def.plugin_paths:
        return []

    unique_project_paths = list(dict.fromkeys(discovered_project_paths))
    configurations = scan_cursor_plugins(
        cursor_def,
        project_paths=unique_project_paths,
    )
    _log_found_servers("Found MCP servers in Cursor plugins", configurations)
    return configurations


def _scan_claude_plugin_phase(
    extra_home_roots: Sequence[Path] = (),
) -> list[MCPClientConfig]:
    """Phase 3: scan Claude Code plugins."""
    configurations = scan_claude_code_plugins()
    for home in extra_home_roots:
        configurations.extend(scan_claude_code_plugins(home=home))
    _log_found_servers("Found MCP servers in Claude Code plugins", configurations)
    return configurations


def _scan_codex_plugin_phase(
    extra_home_roots: Sequence[Path] = (),
) -> list[MCPClientConfig]:
    """Phase 5: scan Codex plugins."""
    configurations = scan_codex_plugins()
    for home in extra_home_roots:
        configurations.extend(scan_codex_plugins(home=home))
    _log_found_servers("Found MCP servers in Codex plugins", configurations)
    return configurations


def _scan_opencode_plugin_phase(
    extra_home_roots: Sequence[Path] = (),
) -> list[MCPClientConfig]:
    """Phase 6: scan OpenCode plugins."""
    configurations = scan_opencode_plugins()
    for home in extra_home_roots:
        configurations.extend(scan_opencode_plugins(home=home))
    _log_found_servers("Found MCP servers in OpenCode plugins", configurations)
    return configurations


def _scan_gemini_extension_phase() -> tuple[
    list[MCPClientConfig], list[DiscoveredPluginArtifact]
]:
    """Phase 7: scan global Gemini extensions."""
    configurations, artifacts = scan_gemini_extensions()
    _log_found_servers(
        "Found MCP servers in Gemini extensions",
        configurations,
        count_key="extension_count",
    )
    return configurations, artifacts


def _scan_copilot_plugin_phase(
    extra_home_roots: Sequence[Path] = (),
) -> tuple[list[MCPClientConfig], list[DiscoveredPluginArtifact]]:
    """Phase 8: scan Copilot plugins."""
    configurations, artifacts = scan_copilot_plugins()
    for home in extra_home_roots:
        home_configurations, home_artifacts = scan_copilot_plugins(home=home)
        configurations.extend(home_configurations)
        artifacts.extend(home_artifacts)
    _log_found_servers("Found MCP servers in Copilot plugins", configurations)
    return configurations, artifacts


def _scan_plugin_artifact_phase(
    *,
    governor: ResourceGovernor,
    extra_home_roots: Sequence[Path] = (),
) -> list[DiscoveredPluginArtifact]:
    """Phase 10: scan independent first-class plugin artifacts."""
    logger.info("Scanning for plugin artifacts")
    artifacts: list[DiscoveredPluginArtifact] = []
    artifacts.extend(scan_cursor_native_plugins())
    artifacts.extend(scan_claude_code_plugin_artifacts())
    artifacts.extend(scan_claude_desktop_connectors())
    artifacts.extend(scan_codex_plugin_artifacts())
    artifacts.extend(scan_opencode_plugin_artifacts())
    for home in extra_home_roots:
        artifacts.extend(scan_cursor_native_plugins(home=home))
        artifacts.extend(scan_claude_code_plugin_artifacts(home=home))
        artifacts.extend(scan_claude_desktop_connectors(home=home))
        artifacts.extend(scan_codex_plugin_artifacts(home=home))
        artifacts.extend(scan_opencode_plugin_artifacts(home=home))
    artifacts.extend(
        scan_vscode_extensions(
            extra_home_roots=extra_home_roots,
            checkpoint=governor.checkpoint,
        )
    )
    artifacts.extend(
        scan_jetbrains_plugins(
            extra_home_roots=extra_home_roots,
            checkpoint=governor.checkpoint,
        )
    )
    return artifacts


def _assemble_configurations(
    *phase_configurations: list[MCPClientConfig],
) -> list[MCPClientConfig]:
    """Concatenate per-phase configurations preserving phase order."""
    return [
        config for configurations in phase_configurations for config in configurations
    ]


def _assemble_plugins(
    skills: list[DiscoveredSkillArtifact],
    *artifact_groups: list[DiscoveredPluginArtifact],
) -> list[DiscoveredPluginArtifact]:
    """Merge plugin artifacts and tag skills that live inside plugin installs."""
    plugins = [artifact for group in artifact_groups for artifact in group]
    plugin_path_map = {
        Path(plugin.install_path).resolve(): plugin.identifier
        for plugin in plugins
        if plugin.identifier and plugin.install_path
    }
    if plugin_path_map:
        tag_skills_with_plugins(skills, plugin_path_map)
    return plugins


def _assemble_agents(
    skills: list[DiscoveredSkillArtifact],
    *agent_groups: list[DiscoveredAgent],
) -> list[DiscoveredAgent]:
    """Merge agent channels and exclude static units nested under skills."""
    agents = [agent for group in agent_groups for agent in group]
    return filter_static_skill_descendants(
        agents,
        (Path(skill.path) for skill in skills),
    )


def _assemble_agent_definitions(
    *definition_groups: list[DiscoveredAgentDefinition],
) -> list[DiscoveredAgentDefinition]:
    """Dedupe only identical client installation paths."""
    return dedupe_agent_definitions(
        [definition for group in definition_groups for definition in group]
    )


def run_concurrent_scan_phases(
    *,
    clients: list[MCPClientDefinition],
    governor: ResourceGovernor,
    timer: PhaseTimer,
    scan_projects: bool,
    project_scan_timeout: int,
    project_scan_depth: int,
    detect_agents: bool,
    run_static_agents: bool,
    detect_disguised_skills: bool = False,
    detect_renamed_plugin_caches: bool = False,
) -> ConcurrentScanResult:
    """Run phases 1-11 as a bounded dependency graph."""
    clear_git_remote_cache()
    reset_skill_scan_state()
    reset_plugin_scan_state(checkpoint=governor.checkpoint)
    wsl_homes = _wsl_homes()
    with bounded_thread_pool(
        max_workers=scan_worker_count(governor),
        thread_name_prefix="device-scan",
    ) as pool:
        global_future = _submit_timed_phase(
            pool,
            timer,
            "phase_01_global_configurations",
            governor,
            lambda: _scan_global_configurations(clients, governor),
        )
        project_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_02_project_crawl",
                governor,
                lambda: _scan_project_phase(
                    governor=governor,
                    project_scan_timeout=project_scan_timeout,
                    project_scan_depth=project_scan_depth,
                    run_static_agents=run_static_agents,
                    extra_home_roots=wsl_homes,
                ),
            )
            if scan_projects
            else None
        )
        if project_future is None:
            timer.record("phase_02_project_crawl", 0)
        hidden_space_future = _submit_timed_phase(
            pool,
            timer,
            "phase_02b_hidden_space_sweep",
            governor,
            lambda: scan_hidden_spaces(
                extra_home_roots=wsl_homes,
                include_files=detect_disguised_skills,
                time_budget_s=project_scan_timeout,
                checkpoint=governor.checkpoint,
            ),
        )

        claude_future = _submit_timed_phase(
            pool,
            timer,
            "phase_03_claude_code_plugins",
            governor,
            lambda: _scan_claude_plugin_phase(wsl_homes),
        )
        codex_future = _submit_timed_phase(
            pool,
            timer,
            "phase_05_codex_plugins",
            governor,
            lambda: _scan_codex_plugin_phase(wsl_homes),
        )
        opencode_future = _submit_timed_phase(
            pool,
            timer,
            "phase_06_opencode_plugins",
            governor,
            lambda: _scan_opencode_plugin_phase(wsl_homes),
        )
        gemini_future = _submit_timed_phase(
            pool,
            timer,
            "phase_07_gemini_extensions",
            governor,
            _scan_gemini_extension_phase,
        )
        copilot_future = _submit_timed_phase(
            pool,
            timer,
            "phase_08_copilot_plugins",
            governor,
            lambda: _scan_copilot_plugin_phase(wsl_homes),
        )
        global_skills_future = _submit_timed_phase(
            pool,
            timer,
            "phase_09_global_skills",
            governor,
            lambda: scan_global_skills(
                extra_home_roots=wsl_homes,
                checkpoint=governor.checkpoint,
            ),
        )
        user_agent_definitions_future = _submit_timed_phase(
            pool,
            timer,
            "phase_09_user_agent_definitions",
            governor,
            lambda: scan_user_agent_definitions(extra_home_roots=wsl_homes),
        )
        plugin_artifacts_future = _submit_timed_phase(
            pool,
            timer,
            "phase_10_plugin_artifacts",
            governor,
            lambda: _scan_plugin_artifact_phase(
                governor=governor,
                extra_home_roots=wsl_homes,
            ),
        )
        renamed_plugin_caches_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_10b_renamed_plugin_caches",
                governor,
                lambda: scan_renamed_plugin_caches(
                    extra_home_roots=wsl_homes,
                    checkpoint=governor.checkpoint,
                ),
            )
            if detect_renamed_plugin_caches
            else None
        )
        if renamed_plugin_caches_future is None:
            timer.record("phase_10b_renamed_plugin_caches", 0)
        else:
            logger.info("Scanning renamed plugin caches")
        install_agents_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_11_install_agents",
                governor,
                lambda: discover_agents(
                    detect_static=False,
                    detect_install=True,
                ),
            )
            if detect_agents
            else None
        )
        if install_agents_future is None:
            timer.record("phase_11_install_agents", 0)

        project_result = (
            pool.result(project_future)
            if project_future is not None
            else ProjectPhaseResult()
        )
        hidden_space_result = pool.result(hidden_space_future)
        global_skills = pool.result(global_skills_future)
        disguised_skills_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_09b_disguised_skills",
                governor,
                lambda: scan_disguised_skills(
                    extra_home_roots=wsl_homes,
                    hidden_candidates=hidden_space_result.files,
                    hidden_candidate_targets=hidden_space_result.file_targets,
                    normal_skill_paths=tuple(
                        Path(skill.path)
                        for skill in (*project_result.skills, *global_skills)
                    ),
                    time_budget_s=project_scan_timeout,
                    checkpoint=governor.checkpoint,
                ),
            )
            if detect_disguised_skills
            else None
        )
        if disguised_skills_future is None:
            timer.record("phase_09b_disguised_skills", 0)
        else:
            logger.info("Scanning disguised skills")
        cursor_future = _submit_timed_phase(
            pool,
            timer,
            "phase_04_cursor_plugins",
            governor,
            lambda: _scan_cursor_plugin_phase(
                project_result.discovered_project_paths,
            ),
        )
        static_agents_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_11_static_agents",
                governor,
                lambda: discover_agents(
                    found_paths=project_result.found_paths,
                    mcp_project_paths=project_result.discovered_project_paths,
                    skill_paths=project_result.agent_skill_roots,
                    detect_static=True,
                    detect_install=False,
                    time_budget_s=project_scan_timeout,
                    checkpoint=governor.checkpoint,
                ),
            )
            if run_static_agents
            else None
        )
        if static_agents_future is None:
            timer.record("phase_11_static_agents", 0)

        pool.wait_for_all()
        global_result = global_future.result()
        gemini_configs, gemini_artifacts = gemini_future.result()
        copilot_configs, copilot_artifacts = copilot_future.result()

        configurations = _assemble_configurations(
            global_result.configurations,
            project_result.configurations,
            claude_future.result(),
            cursor_future.result(),
            codex_future.result(),
            opencode_future.result(),
            gemini_configs,
            copilot_configs,
        )
        skills = strip_duplicate_skill_files(
            [
                *project_result.skills,
                *global_skills,
                *(
                    disguised_skills_future.result()
                    if disguised_skills_future is not None
                    else []
                ),
            ]
        )
        plugins = _assemble_plugins(
            skills,
            plugin_artifacts_future.result(),
            gemini_artifacts,
            project_result.gemini_artifacts,
            copilot_artifacts,
        )
        if renamed_plugin_caches_future is not None:
            plugins.extend(
                filter_novel_plugin_artifacts(
                    renamed_plugin_caches_future.result(),
                    plugins,
                )
            )

        install_agents = (
            install_agents_future.result().agents
            if install_agents_future is not None
            else []
        )
        static_agents = (
            static_agents_future.result().agents
            if static_agents_future is not None
            else []
        )
        agents = _assemble_agents(skills, install_agents, static_agents)
        agent_definitions = _assemble_agent_definitions(
            project_result.agent_definitions,
            user_agent_definitions_future.result(),
        )

        scan_result = ConcurrentScanResult(
            configurations=configurations,
            skills=skills,
            plugins=plugins,
            agents=agents,
            agent_definitions=agent_definitions,
            extension_clients=global_result.extension_clients,
            node_modules_paths=project_result.node_modules_paths,
            hidden_space_result=hidden_space_result,
        )

    finalize_skill_scan_state()
    finalize_plugin_scan_state()
    return scan_result
