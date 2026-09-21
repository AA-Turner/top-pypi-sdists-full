"""Concurrent phase 1-11 orchestration for the device scan."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from concurrent.futures import Future
from dataclasses import dataclass, field, replace
from itertools import chain
from pathlib import Path
import threading
from typing import TypedDict, TypeVar

import structlog

from runlayer_cli import telemetry
from runlayer_cli.scan.agent_scan import (
    AgentScanResult,
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
from runlayer_cli.scan.completeness import ScanCompleteness, ScanCompletionStatus
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
    scan_cursor_user_local_plugins,
    scan_opencode_plugin_artifacts,
)
from runlayer_cli.scan.project_scanner import (
    NESTED_PROJECT_SCAN_DEPTH,
    NESTED_PROJECT_SCAN_TIMEOUT,
    find_files_and_node_modules_under_home,
    find_files_under_project_roots,
    scan_for_project_configs,
)
from runlayer_cli.scan.resource_governor import (
    RESOURCE_LIMIT_EXCEEDED_REASON,
    ResourceGovernor,
    ScanResourceLimitExceeded,
)
from runlayer_cli.scan.skill_scanner import (
    DiscoveredSkillArtifact,
    SkillPhaseScan,
    clear_git_remote_cache,
    finalize_skill_scan_state,
    get_skill_search_filenames,
    process_skill_paths_with_candidates,
    reset_skill_scan_state,
    scan_global_skills_with_candidates,
    strip_duplicate_skill_files,
    tag_skills_with_plugins,
)
from runlayer_cli.scan.timing import PhaseTimer
from runlayer_cli.scan.vscode_extensions import scan_vscode_extensions
from runlayer_cli.scan.warp_sqlite import enrich_configurations_with_warp_sqlite

logger = structlog.get_logger(__name__)
_PLUGIN_ARTIFACT_SCAN_FAILED_REASON = "plugin_artifact_scan_failed"
_PhaseResult = TypeVar("_PhaseResult")


def scan_extensions_folder(
    client_def: MCPClientDefinition,
    *,
    completion: ScanCompletionStatus | None = None,
) -> list[str]:
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
                if completion is not None:
                    completion.mark_incomplete("extension_root_enumeration_failed")
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
    # Crawl-only enumeration completeness for removal reconciliation; distinct
    # from ``skill_completion``, which also revokes authority on window caps.
    skill_crawl_complete: bool = False
    project_skill_candidate_paths: list[str] = field(default_factory=list)
    completion: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    mcp_completion: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    skill_completion: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    definition_completion: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )


@dataclass
class GlobalPhaseResult:
    """Findings from the global-config scan (phase 1)."""

    configurations: list[MCPClientConfig] = field(default_factory=list)
    # Clients whose extensions folder produced servers; feeds client presence.
    extension_clients: set[str] = field(default_factory=set)
    completion: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)


@dataclass
class CompletenessPhaseStatuses:
    """Completion statuses shared with independently scheduled scan phases."""

    wsl_homes: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    hidden_spaces: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    plugin_configurations: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    global_skills: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    user_agent_definitions: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    disguised_skills: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    plugin_artifacts: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    plugin_device_artifacts: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    renamed_plugin_caches: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    # The agent phases carry their own ``completion`` inside ``AgentScanResult``;
    # these hold the phase-boundary verdict (crash, governor abort) so an abort
    # is stamped ``resource_limit_exceeded`` on ``agent_host_static`` like every
    # other phase instead of the phase-specific failure reason.
    install_agents: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    static_agents: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)


@dataclass
class ConcurrentScanResult:
    """Assembled findings from concurrent phases 1-11."""

    configurations: list[MCPClientConfig] = field(default_factory=list)
    discovered_project_paths: list[Path] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    plugins: list[DiscoveredPluginArtifact] = field(default_factory=list)
    agents: list[DiscoveredAgent] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)
    extension_clients: set[str] = field(default_factory=set)
    node_modules_paths: list[Path] = field(default_factory=list)
    hidden_space_result: HiddenSpaceScanResult = field(
        default_factory=HiddenSpaceScanResult
    )
    skill_crawl_complete: bool = False
    project_skill_candidate_paths: list[str] = field(default_factory=list)
    global_skill_candidate_paths: list[str] = field(default_factory=list)
    completeness: ScanCompleteness = field(default_factory=ScanCompleteness)
    # First governor abort message when a phase was cut short; findings above
    # are whatever finished before the trip and every surface they would have
    # fed is already marked ``resource_limit_exceeded``.
    resource_limit_exceeded: str | None = None


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


@dataclass
class ResourceAbortGuard:
    """Turns a governor abort inside a phase into that phase's incomplete default.

    The governor's abort latch is sticky, so once one phase trips it every
    later phase raises on its first checkpoint and falls through to its default
    too. The orchestrator then assembles whatever finished before the trip
    instead of discarding the whole scan; ``reason`` carries the first abort
    message so the caller can report the scan as failed after uploading.
    """

    governor: ResourceGovernor
    reason: str | None = None
    _lock: threading.Lock = field(
        default_factory=threading.Lock, init=False, repr=False, compare=False
    )

    def record(self, exc: ScanResourceLimitExceeded) -> None:
        with self._lock:
            if self.reason is None:
                self.reason = str(exc) or "scan resource limit exceeded"


def _best_effort_phase(
    work: Callable[[], _PhaseResult],
    *,
    default: _PhaseResult,
    scan_status: ScanCompletionStatus,
    reason: str,
    guard: ResourceAbortGuard,
) -> _PhaseResult:
    try:
        guard.governor.checkpoint()
        return work()
    except ScanResourceLimitExceeded as exc:
        guard.record(exc)
        scan_status.mark_incomplete(RESOURCE_LIMIT_EXCEEDED_REASON)
        logger.warning(
            "scan_phase_aborted_by_resource_limit",
            phase_failure_reason=reason,
            error=str(exc),
        )
        return default
    except Exception:
        scan_status.mark_incomplete(reason)
        logger.warning(reason, exc_info=True)
        return default


def _submit_timed_phase(
    pool: ScanThreadPool,
    timer: PhaseTimer,
    name: str,
    work: Callable[[], _PhaseResult],
) -> Future[_PhaseResult]:
    """Submit a ``_best_effort_phase`` (which owns the entry checkpoint)."""

    def run() -> _PhaseResult:
        with timer.phase(name):
            return work()

    return pool.submit(run)


class _ClientGlobalScan(TypedDict):
    configurations: list[MCPClientConfig]
    found_extensions: bool


def _scan_client_global_configuration(
    client_def: MCPClientDefinition,
    governor: ResourceGovernor,
    completion: ScanCompletionStatus,
) -> _ClientGlobalScan:
    """Scan one client's global config paths plus its extensions folder."""
    configurations: list[MCPClientConfig] = []
    found_extensions = False
    found_servers_in_config = False

    for config_path in client_def.get_config_paths():
        logger.debug("Scanning global config", client=client_def.name)
        governor.checkpoint()
        config = parse_config_file(
            client_def,
            config_path,
            scan_status=completion,
        )
        if config and config.servers:
            found_servers_in_config = True
            config.config_scope = "global"
            if client_def.extensions_paths:
                extension_names = scan_extensions_folder(
                    client_def,
                    completion=completion,
                )
                if extension_names:
                    found_extensions = True
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
        extension_names = scan_extensions_folder(
            client_def,
            completion=completion,
        )
        if extension_names:
            found_extensions = True
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

    return {"configurations": configurations, "found_extensions": found_extensions}


def _scan_global_configurations(
    clients: list[MCPClientDefinition],
    governor: ResourceGovernor,
) -> GlobalPhaseResult:
    """Phase 1: scan global configs without mutating shared aggregates.

    Each client is isolated: a reader bug in one client's config must degrade
    that client to ``client_config_scan_failed``, not empty the phase for
    every sibling. Only the governor's abort propagates.
    """
    logger.info("Scanning global configurations")
    configurations: list[MCPClientConfig] = []
    extension_clients: set[str] = set()
    completion = ScanCompletionStatus()

    for client_def in clients:
        try:
            client_result = _scan_client_global_configuration(
                client_def, governor, completion
            )
        except ScanResourceLimitExceeded:
            raise
        except Exception:
            completion.mark_incomplete("client_config_scan_failed")
            logger.warning(
                "client_config_scan_failed", client=client_def.name, exc_info=True
            )
            continue
        configurations.extend(client_result["configurations"])
        if client_result["found_extensions"]:
            extension_clients.add(client_def.name)

    try:
        enrich_configurations_with_warp_sqlite(configurations, completion)
    except ScanResourceLimitExceeded:
        raise
    except Exception:
        completion.mark_incomplete("warp_sqlite_enrichment_failed")
        logger.warning("warp_sqlite_enrichment_failed", exc_info=True)
    return GlobalPhaseResult(
        configurations=configurations,
        extension_clients=extension_clients,
        completion=completion,
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
    completion = ScanCompletionStatus()
    mcp_completion = ScanCompletionStatus()
    skill_completion = ScanCompletionStatus()
    definition_completion = ScanCompletionStatus()

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
        if not getattr(crawl_result, "complete", True):
            for reason in getattr(
                crawl_result,
                "incomplete_reasons",
                ["project_crawl_incomplete"],
            ):
                completion.mark_incomplete(reason)
        found_paths = crawl_result.found_paths
        skill_crawl_complete = getattr(crawl_result, "complete", False)

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
        config = parse_config_file(
            temp_client_def,
            project_config.config_path,
            scan_status=mcp_completion,
        )
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
            nested_completion = ScanCompletionStatus()
            nested_paths = find_files_under_project_roots(
                nested_patterns,
                discovered_project_paths,
                timeout=min(project_scan_timeout, NESTED_PROJECT_SCAN_TIMEOUT),
                max_depth=NESTED_PROJECT_SCAN_DEPTH,
                governor=governor,
                completion=nested_completion,
            )
            skill_completion.merge(nested_completion)
            definition_completion.merge(nested_completion)
        found_paths = sorted(set(found_paths + nested_paths))
        skill_crawl_complete = skill_crawl_complete and nested_completion.complete

    governor.checkpoint()
    skill_scan = process_skill_paths_with_candidates(
        found_paths,
        extra_home_roots=extra_home_roots,
        checkpoint=governor.checkpoint,
        scan_status=skill_completion,
    )
    skills = skill_scan.artifacts
    agent_definitions = process_agent_definition_paths(
        found_paths,
        extra_home_roots=extra_home_roots,
        logical_paths=crawl_result.logical_paths,
        scan_status=definition_completion,
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
        project_skill_candidate_paths=skill_scan.candidate_paths,
        skill_crawl_complete=skill_crawl_complete,
        completion=completion,
        mcp_completion=mcp_completion,
        skill_completion=skill_completion,
        definition_completion=definition_completion,
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


def _scan_native_and_wsl_homes(
    scanner: Callable[..., _PhaseResult],
    extra_home_roots: Sequence[Path],
    *,
    scan_status: ScanCompletionStatus,
) -> list[_PhaseResult]:
    """Run ``scanner`` natively, then once per WSL home, isolating each home.

    A native failure still escapes to ``_best_effort_phase`` (the whole phase
    is broken). One unreadable WSL home only drops that home's slice and marks
    ``wsl_home_plugin_scan_failed`` so native and sibling-home results survive.
    """
    results = [scanner()]
    for home in extra_home_roots:
        try:
            results.append(scanner(home=home))
        except ScanResourceLimitExceeded:
            raise
        except Exception:
            scan_status.mark_incomplete("wsl_home_plugin_scan_failed")
            logger.warning("wsl_home_plugin_scan_failed", home=str(home), exc_info=True)
    return results


def _scan_plugin_configurations(
    scanner: Callable[..., list[MCPClientConfig]],
    message: str,
    extra_home_roots: Sequence[Path],
    *,
    scan_status: ScanCompletionStatus,
) -> list[MCPClientConfig]:
    configurations = list(
        chain.from_iterable(
            _scan_native_and_wsl_homes(
                scanner, extra_home_roots, scan_status=scan_status
            )
        )
    )
    _log_found_servers(message, configurations)
    return configurations


def _scan_claude_plugin_phase(
    extra_home_roots: Sequence[Path] = (),
    *,
    scan_status: ScanCompletionStatus,
) -> list[MCPClientConfig]:
    """Phase 3: scan Claude Code plugins."""
    return _scan_plugin_configurations(
        scan_claude_code_plugins,
        "Found MCP servers in Claude Code plugins",
        extra_home_roots,
        scan_status=scan_status,
    )


def _scan_codex_plugin_phase(
    extra_home_roots: Sequence[Path] = (),
    *,
    scan_status: ScanCompletionStatus,
) -> list[MCPClientConfig]:
    """Phase 5: scan Codex plugins."""
    return _scan_plugin_configurations(
        scan_codex_plugins,
        "Found MCP servers in Codex plugins",
        extra_home_roots,
        scan_status=scan_status,
    )


def _scan_opencode_plugin_phase(
    extra_home_roots: Sequence[Path] = (),
    *,
    scan_status: ScanCompletionStatus,
) -> list[MCPClientConfig]:
    """Phase 6: scan OpenCode plugins."""
    return _scan_plugin_configurations(
        scan_opencode_plugins,
        "Found MCP servers in OpenCode plugins",
        extra_home_roots,
        scan_status=scan_status,
    )


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
    *,
    scan_status: ScanCompletionStatus,
) -> tuple[list[MCPClientConfig], list[DiscoveredPluginArtifact]]:
    """Phase 8: scan Copilot plugins."""
    results = _scan_native_and_wsl_homes(
        scan_copilot_plugins, extra_home_roots, scan_status=scan_status
    )
    configurations = list(chain.from_iterable(configs for configs, _ in results))
    artifacts = list(chain.from_iterable(found for _, found in results))
    _log_found_servers("Found MCP servers in Copilot plugins", configurations)
    return configurations, artifacts


def _scan_plugin_artifact_phase(
    *,
    governor: ResourceGovernor,
    extra_home_roots: Sequence[Path] = (),
    machine_scope: bool = True,
    scan_status: ScanCompletionStatus | None = None,
    device_scan_status: ScanCompletionStatus | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Phase 10: scan independent first-class plugin artifacts.

    Each scanner (and each extra home root) is isolated so one client's
    plugin-store bug degrades that scanner to ``plugin_scanner_failed``
    instead of dropping every other client's artifacts.
    """
    logger.info("Scanning for plugin artifacts")
    status = scan_status if scan_status is not None else ScanCompletionStatus()
    artifacts: list[DiscoveredPluginArtifact] = []

    def collect(
        name: str,
        work: Callable[[], list[DiscoveredPluginArtifact]],
        *,
        also_mark: ScanCompletionStatus | None = None,
    ) -> None:
        try:
            artifacts.extend(work())
        except ScanResourceLimitExceeded:
            raise
        except Exception:
            status.mark_incomplete("plugin_scanner_failed")
            if also_mark is not None:
                also_mark.mark_incomplete("plugin_scanner_failed")
            logger.warning("plugin_scanner_failed", scanner=name, exc_info=True)

    home_scanners: list[tuple[str, Callable[..., list[DiscoveredPluginArtifact]]]] = [
        ("cursor_native", scan_cursor_native_plugins),
        ("cursor_user_local", scan_cursor_user_local_plugins),
        ("claude_code", scan_claude_code_plugin_artifacts),
        ("claude_desktop", scan_claude_desktop_connectors),
        ("codex", scan_codex_plugin_artifacts),
        ("opencode", scan_opencode_plugin_artifacts),
    ]
    for name, scanner in home_scanners:
        collect(name, scanner)
    for home in extra_home_roots:
        for name, scanner in home_scanners:
            collect(name, lambda scanner=scanner, home=home: scanner(home=home))
    collect(
        "vscode",
        lambda: scan_vscode_extensions(
            extra_home_roots=extra_home_roots,
            machine_scope=machine_scope,
            checkpoint=governor.checkpoint,
            scan_status=scan_status,
            device_scan_status=device_scan_status,
        ),
        also_mark=device_scan_status,
    )
    collect(
        "jetbrains",
        lambda: scan_jetbrains_plugins(
            extra_home_roots=extra_home_roots,
            checkpoint=governor.checkpoint,
            scan_status=scan_status,
        ),
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


def _assemble_completeness(
    *,
    scan_projects: bool,
    detect_agents: bool,
    run_static_agents: bool,
    detect_disguised_skills: bool,
    machine_scope: bool,
    global_result: GlobalPhaseResult,
    project_result: ProjectPhaseResult,
    hidden_space_result: HiddenSpaceScanResult,
    phase_statuses: CompletenessPhaseStatuses,
    install_agent_result: AgentScanResult | None,
    static_agent_result: AgentScanResult | None,
) -> ScanCompleteness:
    """Map phase completion to every absence-authority surface it can affect."""
    completeness = ScanCompleteness()
    if not detect_agents:
        completeness.agent_host_static.mark_incomplete("agent_detection_disabled")
    elif not run_static_agents:
        completeness.agent_host_static.mark_incomplete("agent_static_scan_disabled")

    if not scan_projects:
        completeness.mark_incomplete(
            "project_scan_disabled",
            "mcp_host_static",
            "skill_host_static",
            "plugin_host_static",
            "agent_host_static",
            "agent_definition_host_static",
            "wsl_static",
            "client_presence",
        )

    if not machine_scope:
        completeness.mark_incomplete(
            "machine_scope_scan_disabled",
            "plugin_device",
            "client_presence",
        )

    completeness.mcp_host_static.merge(global_result.completion)
    completeness.wsl_static.merge(global_result.completion)
    completeness.mcp_host_static.merge(phase_statuses.plugin_configurations)
    completeness.mcp_host_static.merge(phase_statuses.plugin_artifacts)
    for status_name in (
        "mcp_host_static",
        "skill_host_static",
        "plugin_host_static",
        "agent_host_static",
        "agent_definition_host_static",
        "wsl_static",
    ):
        getattr(completeness, status_name).merge(project_result.completion)
    completeness.mcp_host_static.merge(project_result.mcp_completion)
    completeness.skill_host_static.merge(project_result.skill_completion)
    completeness.agent_host_static.merge(project_result.skill_completion)
    completeness.agent_definition_host_static.merge(
        project_result.definition_completion
    )
    completeness.wsl_static.merge(project_result.mcp_completion)
    completeness.wsl_static.merge(project_result.skill_completion)
    completeness.wsl_static.merge(project_result.definition_completion)
    completeness.plugin_host_static.merge(phase_statuses.plugin_artifacts)
    completeness.plugin_host_static.merge(phase_statuses.plugin_configurations)
    completeness.plugin_device.merge(phase_statuses.plugin_device_artifacts)
    # The device scan runs inside phase 10, so a phase-boundary failure there
    # (crash or governor abort) means it never ran either; only the boundary
    # reasons bridge, since per-scanner failures already mark the device status.
    for boundary_reason in (
        _PLUGIN_ARTIFACT_SCAN_FAILED_REASON,
        RESOURCE_LIMIT_EXCEEDED_REASON,
    ):
        if boundary_reason in phase_statuses.plugin_artifacts.reasons:
            completeness.plugin_device.mark_incomplete(boundary_reason)
    completeness.plugin_host_static.merge(phase_statuses.renamed_plugin_caches)
    completeness.skill_host_static.merge(phase_statuses.disguised_skills)
    completeness.skill_host_static.merge(phase_statuses.global_skills)
    completeness.agent_definition_host_static.merge(
        phase_statuses.user_agent_definitions
    )
    for wsl_contributor in (
        phase_statuses.plugin_artifacts,
        phase_statuses.plugin_configurations,
        phase_statuses.renamed_plugin_caches,
        phase_statuses.disguised_skills,
        phase_statuses.global_skills,
        phase_statuses.user_agent_definitions,
    ):
        completeness.wsl_static.merge(wsl_contributor)

    hidden_space_truncation = ScanCompletionStatus()
    hidden_space_truncated = (
        hidden_space_result.truncated
        or hidden_space_result.node_modules_paths_truncated
        or hidden_space_result.python_env_roots_truncated
        or hidden_space_result.launcher_directories_truncated
    )
    if hidden_space_truncated:
        hidden_space_truncation.mark_incomplete("hidden_space_scan_truncated")
        completeness.wsl_static.merge(hidden_space_truncation)
        if detect_disguised_skills:
            completeness.skill_host_static.merge(hidden_space_truncation)

    completeness.wsl_static.merge(phase_statuses.hidden_spaces)
    completeness.wsl_static.merge(phase_statuses.wsl_homes)
    completeness.plugin_host_static.merge(phase_statuses.wsl_homes)
    if detect_disguised_skills:
        completeness.skill_host_static.merge(phase_statuses.hidden_spaces)

    for presence_contributor in (
        global_result.completion,
        project_result.completion,
        project_result.mcp_completion,
        project_result.skill_completion,
        project_result.definition_completion,
        hidden_space_truncation,
        phase_statuses.hidden_spaces,
        phase_statuses.plugin_configurations,
        phase_statuses.global_skills,
        phase_statuses.user_agent_definitions,
        phase_statuses.disguised_skills,
        phase_statuses.plugin_artifacts,
        phase_statuses.plugin_device_artifacts,
        phase_statuses.renamed_plugin_caches,
        phase_statuses.wsl_homes,
    ):
        completeness.client_presence.merge(presence_contributor)

    completeness.agent_host_static.merge(phase_statuses.install_agents)
    completeness.agent_host_static.merge(phase_statuses.static_agents)
    for agent_result in (install_agent_result, static_agent_result):
        if agent_result is not None and not getattr(agent_result, "complete", True):
            for reason in getattr(
                agent_result,
                "incomplete_reasons",
                ["agent_scan_incomplete"],
            ):
                completeness.agent_host_static.mark_incomplete(reason)

    return completeness


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
    machine_scope: bool = True,
) -> ConcurrentScanResult:
    """Run phases 1-11 as a bounded dependency graph."""
    clear_git_remote_cache()
    reset_skill_scan_state()
    phase_statuses = CompletenessPhaseStatuses()
    reset_plugin_scan_state(
        checkpoint=governor.checkpoint,
        scan_status=phase_statuses.plugin_artifacts,
    )
    global_phase_status = ScanCompletionStatus()
    project_phase_status = ScanCompletionStatus()
    guard = ResourceAbortGuard(governor)
    wsl_homes = _wsl_homes(scan_status=phase_statuses.wsl_homes)
    with bounded_thread_pool(
        max_workers=scan_worker_count(governor),
        thread_name_prefix="device-scan",
    ) as pool:
        global_future = _submit_timed_phase(
            pool,
            timer,
            "phase_01_global_configurations",
            lambda: _best_effort_phase(
                lambda: _scan_global_configurations(clients, governor),
                default=GlobalPhaseResult(completion=global_phase_status),
                scan_status=global_phase_status,
                reason="global_configuration_scan_failed",
                guard=guard,
            ),
        )
        project_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_02_project_crawl",
                lambda: _best_effort_phase(
                    lambda: _scan_project_phase(
                        governor=governor,
                        project_scan_timeout=project_scan_timeout,
                        project_scan_depth=project_scan_depth,
                        run_static_agents=run_static_agents,
                        extra_home_roots=wsl_homes,
                    ),
                    default=ProjectPhaseResult(completion=project_phase_status),
                    scan_status=project_phase_status,
                    reason="project_scan_failed",
                    guard=guard,
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
            lambda: _best_effort_phase(
                lambda: scan_hidden_spaces(
                    extra_home_roots=wsl_homes,
                    include_files=detect_disguised_skills,
                    time_budget_s=project_scan_timeout,
                    checkpoint=governor.checkpoint,
                ),
                default=HiddenSpaceScanResult(truncated=True),
                scan_status=phase_statuses.hidden_spaces,
                reason="hidden_space_scan_failed",
                guard=guard,
            ),
        )

        claude_future = _submit_timed_phase(
            pool,
            timer,
            "phase_03_claude_code_plugins",
            lambda: _best_effort_phase(
                lambda: _scan_claude_plugin_phase(
                    wsl_homes, scan_status=phase_statuses.plugin_configurations
                ),
                default=[],
                scan_status=phase_statuses.plugin_configurations,
                reason="claude_plugin_scan_failed",
                guard=guard,
            ),
        )
        codex_future = _submit_timed_phase(
            pool,
            timer,
            "phase_05_codex_plugins",
            lambda: _best_effort_phase(
                lambda: _scan_codex_plugin_phase(
                    wsl_homes, scan_status=phase_statuses.plugin_configurations
                ),
                default=[],
                scan_status=phase_statuses.plugin_configurations,
                reason="codex_plugin_scan_failed",
                guard=guard,
            ),
        )
        opencode_future = _submit_timed_phase(
            pool,
            timer,
            "phase_06_opencode_plugins",
            lambda: _best_effort_phase(
                lambda: _scan_opencode_plugin_phase(
                    wsl_homes, scan_status=phase_statuses.plugin_configurations
                ),
                default=[],
                scan_status=phase_statuses.plugin_configurations,
                reason="opencode_plugin_scan_failed",
                guard=guard,
            ),
        )
        gemini_future = _submit_timed_phase(
            pool,
            timer,
            "phase_07_gemini_extensions",
            lambda: _best_effort_phase(
                _scan_gemini_extension_phase,
                default=([], []),
                scan_status=phase_statuses.plugin_configurations,
                reason="gemini_extension_scan_failed",
                guard=guard,
            ),
        )
        copilot_future = _submit_timed_phase(
            pool,
            timer,
            "phase_08_copilot_plugins",
            lambda: _best_effort_phase(
                lambda: _scan_copilot_plugin_phase(
                    wsl_homes, scan_status=phase_statuses.plugin_configurations
                ),
                default=([], []),
                scan_status=phase_statuses.plugin_configurations,
                reason="copilot_plugin_scan_failed",
                guard=guard,
            ),
        )
        global_skills_future = _submit_timed_phase(
            pool,
            timer,
            "phase_09_global_skills",
            lambda: _best_effort_phase(
                lambda: scan_global_skills_with_candidates(
                    extra_home_roots=wsl_homes,
                    checkpoint=governor.checkpoint,
                    scan_status=phase_statuses.global_skills,
                ),
                default=SkillPhaseScan(
                    artifacts=[], candidate_paths=[], complete=False
                ),
                scan_status=phase_statuses.global_skills,
                reason="global_skill_scan_failed",
                guard=guard,
            ),
        )
        user_agent_definitions_future = _submit_timed_phase(
            pool,
            timer,
            "phase_09_user_agent_definitions",
            lambda: _best_effort_phase(
                lambda: scan_user_agent_definitions(
                    extra_home_roots=wsl_homes,
                    scan_status=phase_statuses.user_agent_definitions,
                ),
                default=[],
                scan_status=phase_statuses.user_agent_definitions,
                reason="user_agent_definition_scan_failed",
                guard=guard,
            ),
        )
        plugin_artifacts_future = _submit_timed_phase(
            pool,
            timer,
            "phase_10_plugin_artifacts",
            lambda: _best_effort_phase(
                lambda: _scan_plugin_artifact_phase(
                    governor=governor,
                    extra_home_roots=wsl_homes,
                    machine_scope=machine_scope,
                    scan_status=phase_statuses.plugin_artifacts,
                    device_scan_status=phase_statuses.plugin_device_artifacts,
                ),
                default=[],
                scan_status=phase_statuses.plugin_artifacts,
                reason=_PLUGIN_ARTIFACT_SCAN_FAILED_REASON,
                guard=guard,
            ),
        )
        renamed_plugin_caches_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_10b_renamed_plugin_caches",
                lambda: _best_effort_phase(
                    lambda: scan_renamed_plugin_caches(
                        extra_home_roots=wsl_homes,
                        checkpoint=governor.checkpoint,
                        scan_status=phase_statuses.renamed_plugin_caches,
                    ),
                    default=[],
                    scan_status=phase_statuses.renamed_plugin_caches,
                    reason="renamed_plugin_scan_failed",
                    guard=guard,
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
                lambda: _best_effort_phase(
                    lambda: discover_agents(
                        detect_static=False,
                        detect_install=True,
                    ),
                    default=AgentScanResult(),
                    scan_status=phase_statuses.install_agents,
                    reason="agent_install_scan_failed",
                    guard=guard,
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
        global_skill_scan = pool.result(global_skills_future)
        disguised_skills_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_09b_disguised_skills",
                lambda: _best_effort_phase(
                    lambda: scan_disguised_skills(
                        extra_home_roots=wsl_homes,
                        hidden_candidates=hidden_space_result.files,
                        hidden_candidate_targets=hidden_space_result.file_targets,
                        normal_skill_paths=tuple(
                            Path(skill.path)
                            for skill in (
                                *project_result.skills,
                                *global_skill_scan.artifacts,
                            )
                        ),
                        time_budget_s=project_scan_timeout,
                        checkpoint=governor.checkpoint,
                        scan_status=phase_statuses.disguised_skills,
                    ),
                    default=[],
                    scan_status=phase_statuses.disguised_skills,
                    reason="disguised_skill_scan_failed",
                    guard=guard,
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
            lambda: _best_effort_phase(
                lambda: _scan_cursor_plugin_phase(
                    project_result.discovered_project_paths,
                ),
                default=[],
                scan_status=phase_statuses.plugin_configurations,
                reason="cursor_plugin_scan_failed",
                guard=guard,
            ),
        )
        static_agents_future = (
            _submit_timed_phase(
                pool,
                timer,
                "phase_11_static_agents",
                lambda: _best_effort_phase(
                    lambda: discover_agents(
                        found_paths=project_result.found_paths,
                        mcp_project_paths=project_result.discovered_project_paths,
                        skill_paths=project_result.agent_skill_roots,
                        detect_static=True,
                        detect_install=False,
                        time_budget_s=project_scan_timeout,
                        checkpoint=governor.checkpoint,
                    ),
                    default=AgentScanResult(),
                    scan_status=phase_statuses.static_agents,
                    reason="agent_static_scan_failed",
                    guard=guard,
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
                *global_skill_scan.artifacts,
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

        install_agent_result = (
            install_agents_future.result()
            if install_agents_future is not None
            else None
        )
        static_agent_result = (
            static_agents_future.result() if static_agents_future is not None else None
        )
        install_agents = (
            install_agent_result.agents if install_agent_result is not None else []
        )
        static_agents = (
            static_agent_result.agents if static_agent_result is not None else []
        )
        agents = _assemble_agents(skills, install_agents, static_agents)
        agent_definitions = _assemble_agent_definitions(
            project_result.agent_definitions,
            user_agent_definitions_future.result(),
        )

        completeness = _assemble_completeness(
            scan_projects=scan_projects,
            detect_agents=detect_agents,
            run_static_agents=run_static_agents,
            detect_disguised_skills=detect_disguised_skills,
            machine_scope=machine_scope,
            global_result=global_result,
            project_result=project_result,
            hidden_space_result=hidden_space_result,
            phase_statuses=phase_statuses,
            install_agent_result=install_agent_result,
            static_agent_result=static_agent_result,
        )

        scan_result = ConcurrentScanResult(
            configurations=configurations,
            discovered_project_paths=project_result.discovered_project_paths,
            skills=skills,
            plugins=plugins,
            agents=agents,
            agent_definitions=agent_definitions,
            extension_clients=global_result.extension_clients,
            node_modules_paths=project_result.node_modules_paths,
            project_skill_candidate_paths=(
                project_result.project_skill_candidate_paths
            ),
            global_skill_candidate_paths=global_skill_scan.candidate_paths,
            hidden_space_result=hidden_space_result,
            skill_crawl_complete=(
                scan_projects
                and project_result.skill_crawl_complete
                and global_skill_scan.complete
            ),
            completeness=completeness,
            resource_limit_exceeded=guard.reason,
        )

    # The finalizers persist ``offset + admitted`` for the content rotation.
    # An aborted skill/plugin phase can admit content and then return its empty
    # default, so that content never reaches the partial manifest; advancing
    # the cursor past it would skip the slice on the next run. Leave the cursor
    # where it was so the next scan re-covers the same window.
    if guard.reason is None:
        finalize_skill_scan_state()
        finalize_plugin_scan_state()
    return scan_result
