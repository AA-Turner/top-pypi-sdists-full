"""MCP Watch scan entry point, result models, payloads, and submission."""

from __future__ import annotations

import datetime
import getpass
import os
import stat
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any, Generic, Literal, Protocol, TypeVar, cast

try:
    import pwd
except ImportError:  # pragma: no cover - Windows only
    pwd = None  # ty: ignore[invalid-assignment]

import httpx
import structlog

from runlayer_cli.paths import strip_reported_path_prefix
from runlayer_cli.scan.artifact_cache import ArtifactCache
from runlayer_cli.scan.agent_definition_scanner import (
    DiscoveredAgentDefinition,
    dedupe_agent_definitions,
)
from runlayer_cli.scan.agents.detect import DiscoveredAgent
from runlayer_cli.scan.client_presence import (
    DetectedClient,
    detect_client_presence,
    merge_client_presence,
)
from runlayer_cli.scan.clients import MCPClientDefinition, get_all_clients
from runlayer_cli.scan.completeness import ScanCompleteness, ScanCompletionStatus
from runlayer_cli.scan.config_redact import BENIGN_ENV_KEYS, redact_config_mapping
from runlayer_cli.scan.config_parser import MCPClientConfig, parse_config_file
from runlayer_cli.scan.containers import (
    CONTAINER_SCAN_INCOMPLETE_REASON,
    ContainerScanResult,
    DiscoveredContainer,
    DiscoveredContainerImage,
    sanitize_container_scan_error,
    scan_running_containers,
)
from runlayer_cli.scan.containers.inspect_parse import MAX_CONTAINERS
from runlayer_cli.scan.device import (
    DeviceContext,
    DiscoveredWSLDistro,
    InstalledTool,
    get_device_metadata,
    get_installed_tools,
    get_or_create_device_id,
    get_wsl_distro_inventory,
    get_wsl_distro_root,
)
from runlayer_cli.scan.orchestrator import (
    ConcurrentScanResult,
    run_concurrent_scan_phases,
    run_timed_phase,
)
from runlayer_cli.scan.plugin_scanner import (
    DiscoveredPluginArtifact,
    reset_plugin_scan_state,
)
from runlayer_cli.scan.processes import (
    DiscoveredProcess,
    ProcessDiscoveryResult,
    discover_processes,
)
from runlayer_cli.scan.processes.models import ExtensionRootRef, OverrideConfigRef
from runlayer_cli.scan.project_scanner import (
    MAX_PROJECT_DEPTH,
    _clamp_scan_bound,
)
from runlayer_cli.scan.resource_governor import (
    RESOURCE_LIMIT_EXCEEDED_REASON,
    ResourceGovernor,
    ScanResourceLimitExceeded,
    build_governor,
)
from runlayer_cli.scan.skill_presence import (
    SkillPresenceParams,
    SkillPresenceState,
    build_state as build_presence_state,
    compute_removals,
    load_state as load_presence_state,
    save_state as save_presence_state,
)
from runlayer_cli.scan.skill_scanner import (
    DiscoveredSkillArtifact,
    reset_skill_scan_state,
    strip_duplicate_skill_files,
)
from runlayer_cli.scan.timing import PhaseTimer
from runlayer_cli.scan.vscode_extensions import (
    VSCodeExtensionRoot,
    scan_vscode_extension_roots,
)
from runlayer_cli.scan.wsl_paths import parse_wsl_unc_path
from runlayer_cli.scan.wsl_projects import WSLProjectScanResult, scan_wsl_projects
from runlayer_cli.scan.wsl_exec import WSLContainerScanResult, scan_wsl_containers
from runlayer_cli.scan.wsl_runtime_signals import scan_wsl_runtime_file_signals
from runlayer_cli.safe_parse import parse_json

if TYPE_CHECKING:
    from runlayer_cli.api import RunlayerClient

logger = structlog.get_logger(__name__)
_IN_PROCESS_SCAN_LOCK = threading.Lock()

SubmissionStatus = Literal["success", "unsupported", "failed"]
ScanManifestCategory = Literal[
    "mcp",
    "client",
    "skill",
    "plugin",
    "agent",
    "agent_definition",
]
ScanManifestSurface = Literal[
    "host_static",
    "host_runtime",
    "container",
    "wsl",
    "wsl_runtime",
    "device",
]

CATEGORY_SURFACES: Mapping[
    ScanManifestCategory,
    tuple[ScanManifestSurface, ...],
] = {
    "mcp": ("host_static", "host_runtime", "container", "wsl", "wsl_runtime"),
    "client": ("host_static", "host_runtime", "container", "wsl", "wsl_runtime"),
    "skill": ("host_static", "container", "wsl"),
    "plugin": ("host_static", "host_runtime", "container", "device"),
    "agent": ("host_static", "host_runtime", "wsl", "wsl_runtime"),
    "agent_definition": ("host_static", "container", "wsl"),
}

# Exit codes distinguish "scan ran but nothing persisted" from a clean run, so a
# scheduled-task scan (whose only on-device signal is the process exit code,
# surfaced via Task Scheduler LastTaskResult) does not read a silent no-op as
# healthy. The CLI layer owns 1 (generic auth/5xx/unexpected error) and 0 (clean
# run / no findings / dry run).
EXIT_UNSUPPORTED = 2  # endpoint 404 — backend too old / wrong host / intercepted
EXIT_SUBMIT_FAILED = 3  # submission attempted but failed (network error / 5xx)

# Per-report agent cap. Mirrors the backend MAX_AGENTS_PER_REPORT so an outlier
# host (huge monorepo, many detected projects) can't send an unbounded batch;
# the backend rejects anything larger, so truncate on the wire.
MAX_AGENTS = 1000
MAX_AGENT_DEFINITIONS = 1000
MAX_OVERRIDE_CONFIG_BYTES = 5 * 1024 * 1024
MAX_OVERRIDE_OWNER_LOOKUPS = 32
ARTIFACT_LOOKUP_BATCH_SIZE = 200


@dataclass
class ScanSubmissionResult:
    """Outcome of submitting a scan's findings to the backend.

    Aggregates per-category submission status (servers/skills/plugins/agents) so
    the process exit-code policy lives in one testable place (``exit_code``)
    instead of inline in the CLI callback. ``response`` is the server submission
    body when it persisted, used only for the success summary.
    """

    response: dict[str, Any] | None = None
    unsupported: list[str] = field(default_factory=list)
    failed_submissions: list[str] = field(default_factory=list)
    category_outcomes: dict[ScanManifestCategory, SubmissionStatus] = field(
        default_factory=lambda: {category: "success" for category in CATEGORY_SURFACES}
    )
    surface_outcomes: dict[
        tuple[ScanManifestCategory, ScanManifestSurface],
        SubmissionStatus,
    ] = field(
        default_factory=lambda: {
            (category, surface): "success"
            for category, surfaces in CATEGORY_SURFACES.items()
            for surface in surfaces
        }
    )
    incomplete_surfaces: dict[
        tuple[ScanManifestCategory, ScanManifestSurface],
        str,
    ] = field(default_factory=dict)

    @property
    def exit_code(self) -> int:
        """Process exit code implied by this submission outcome.

        A submission was attempted but did not persist ⇒ exit nonzero so a
        scheduled-task scan does not surface it as a healthy run (the only
        on-device signal is the exit code via Task Scheduler LastTaskResult).
        ``failed`` (network error / 5xx) outranks ``unsupported`` (404): it is the
        more urgent signal and more likely to be transient.
        """
        if self.failed_submissions:
            return EXIT_SUBMIT_FAILED
        if self.unsupported:
            return EXIT_UNSUPPORTED
        return 0


_MCP_TRANSPORT_TYPES = frozenset({"stdio", "sse", "http", "streaming-http"})


def _coerce_transport_type_for_api(transport_type: str, *, has_url: bool) -> str:
    """Map client transport aliases to the backend enum, clamping unknowns.

    Mirrors the backend before-validator: normalize url-bearing HTTP transports
    to ``streaming-http``; clamp unknowns to that same remote type when a url is
    present and to ``stdio`` otherwise. Keeps one off-enum server from 422ing the
    whole scan batch.
    """
    t = str(transport_type).strip().lower().replace("_", "-")
    if t in ("streamablehttp", "streamable-http") or (t == "http" and has_url):
        t = "streaming-http"
    if t not in _MCP_TRANSPORT_TYPES:
        t = "streaming-http" if has_url else "stdio"
    return t


def _stringify_str_mapping(value: Any) -> Any:
    """Stringify a mapping's keys/values, dropping ``None`` values.

    Real-world configs carry numeric/bool env & header values (e.g.
    ``{"PORT": 8080}``) but the backend requires ``dict[str, str]``.
    """
    if not isinstance(value, dict):
        return value
    return {str(k): str(v) for k, v in value.items() if v is not None}


def _stringify_args(value: Any) -> Any:
    """Stringify list elements, dropping ``None``; backend requires ``list[str]``."""
    if not isinstance(value, list):
        return value
    return [str(a) for a in value if a is not None]


@dataclass(frozen=True)
class _WSLArtifactPaths:
    """Normalized paths sharing one WSL identity."""

    path: str | None
    project_path: str | None
    distro: str
    user: str | None


def _wsl_artifact_paths(
    path: str | None,
    project_path: str | None,
) -> _WSLArtifactPaths | None:
    """Normalize two independently parsed paths when their WSL identities agree."""
    parsed_path = parse_wsl_unc_path(path)
    parsed_project_path = parse_wsl_unc_path(project_path)
    parsed = [item for item in (parsed_path, parsed_project_path) if item is not None]
    if not parsed:
        return None

    distro = parsed[0].distro
    users = {item.user for item in parsed if item.user is not None}
    if (
        any(item.distro.casefold() != distro.casefold() for item in parsed)
        or len(users) > 1
    ):
        logger.warning(
            "WSL artifact paths have inconsistent identity",
            path=str(path) if path is not None else None,
            project_path=str(project_path) if project_path is not None else None,
        )
        return None

    return _WSLArtifactPaths(
        path=parsed_path.linux_path if parsed_path is not None else path,
        project_path=(
            parsed_project_path.linux_path
            if parsed_project_path is not None
            else project_path
        ),
        distro=distro,
        user=next(iter(users), None),
    )


def _normalize_matching_wsl_path(
    value: str,
    *,
    distro: str,
    user: str | None,
) -> str:
    parsed = parse_wsl_unc_path(value)
    if parsed is None or parsed.distro.casefold() != distro.casefold():
        return value
    if user is not None and parsed.user not in {None, user}:
        return value
    return parsed.linux_path


def _corroborated_wsl_artifact_paths(
    path: str | None,
    project_path: str | None,
    *,
    known_distros: dict[str, str],
    uncorroborated: set[str],
) -> _WSLArtifactPaths | None:
    """Normalize paths only for a distro the uploaded inventory names."""
    attribution = _wsl_artifact_paths(path, project_path)
    if attribution is None:
        return None
    inventory_name = known_distros.get(attribution.distro.casefold())
    if inventory_name is None:
        uncorroborated.add(attribution.distro)
        return None
    return replace(attribution, distro=inventory_name)


def _attribute_wsl_artifacts(
    configurations: list[MCPClientConfig],
    skills: list[DiscoveredSkillArtifact],
    agent_definitions: list[DiscoveredAgentDefinition],
    *,
    inventory_distros: list[str],
) -> list[DiscoveredAgentDefinition]:
    """Attach WSL identity and Linux paths in one post-discovery pass.

    Only a distro in *inventory_distros* — the ``wsl --list --verbose``
    inventory this same scan uploads — may claim an artifact. An incomplete
    parse withholds that inventory from the payload, so attributing against it
    would ship ``config_scope="wsl"`` artifacts whose only corroboration is a
    backend-synthesized distro row with a guessed running state. Uncorroborated
    artifacts keep their UNC path and original scope. Attribution reports the
    inventory's spelling so the backend resolves the ``wsl`` block against the
    row this scan reported.

    Container paths belong to the container namespace and are deliberately
    excluded even when their text happens to resemble a WSL UNC path. So are
    ``process_override`` configs: rewriting them to ``wsl`` would erase the
    launch-flag attribution the Shadow UI surfaces.

    *configurations* and *skills* are mutated in place; *agent_definitions* is
    frozen, so its attributed replacements come back as the return value and
    callers must rebind the list they passed in.
    """
    known_distros = {name.casefold(): name for name in inventory_distros}
    uncorroborated: set[str] = set()

    def attribute(
        path: str | None, project_path: str | None
    ) -> _WSLArtifactPaths | None:
        return _corroborated_wsl_artifact_paths(
            path,
            project_path,
            known_distros=known_distros,
            uncorroborated=uncorroborated,
        )

    for config in configurations:
        if config.container_id is not None or config.config_scope in (
            "container",
            "process_override",
        ):
            continue
        attribution = attribute(config.config_path, config.project_path)
        if attribution is None:
            continue
        config.config_path = attribution.path
        config.project_path = attribution.project_path
        config.config_scope = "wsl"
        config.wsl_distro = attribution.distro
        config.wsl_user = attribution.user
        for server in config.servers:
            if isinstance(server.project_name, list):
                server.project_name = [
                    _normalize_matching_wsl_path(
                        path,
                        distro=attribution.distro,
                        user=attribution.user,
                    )
                    for path in server.project_name
                ]
            elif isinstance(server.project_name, str):
                server.project_name = _normalize_matching_wsl_path(
                    server.project_name,
                    distro=attribution.distro,
                    user=attribution.user,
                )

    for skill in skills:
        if skill.container_id is not None:
            continue
        attribution = attribute(skill.path, skill.project_path)
        if attribution is None or attribution.path is None:
            continue
        skill.path = attribution.path
        skill.project_path = attribution.project_path
        skill.wsl_distro = attribution.distro
        skill.wsl_user = attribution.user
        skill.symlinks_found = [
            _normalize_matching_wsl_path(
                path,
                distro=attribution.distro,
                user=attribution.user,
            )
            for path in skill.symlinks_found
        ]

    attributed_definitions: list[DiscoveredAgentDefinition] = []
    for definition in agent_definitions:
        if definition.container_id is not None:
            attributed_definitions.append(definition)
            continue
        attribution = attribute(definition.path, definition.project_path)
        if attribution is None or attribution.path is None:
            attributed_definitions.append(definition)
            continue
        attributed_definitions.append(
            replace(
                definition,
                path=attribution.path,
                project_path=attribution.project_path,
                wsl_distro=attribution.distro,
                wsl_user=attribution.user,
            )
        )

    if uncorroborated:
        logger.warning(
            "Skipped WSL attribution for distros absent from the scan inventory",
            distros=sorted(uncorroborated),
            inventory_distros=sorted(inventory_distros),
        )
    return attributed_definitions


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
    scan_session_id: uuid.UUID = field(default_factory=uuid.uuid4)
    scan_started_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    completeness: ScanCompleteness = field(default_factory=ScanCompleteness)
    windows_user_sid: str | None = None
    machine_scope: bool = True
    project_scan_requested: bool = True
    agent_discovery_complete: bool = True
    client_discovery_complete: bool = True
    process_scan_requested: bool = False
    processes_scanned: bool = False
    is_wsl: bool = False
    serial_number: str | None = None
    tools: list[InstalledTool] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    plugins: list[DiscoveredPluginArtifact] = field(default_factory=list)
    agents: list[DiscoveredAgent] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)
    processes: list[DiscoveredProcess] = field(default_factory=list)
    container_scan_requested: bool = False
    container_scan_error: str | None = None
    containers: list[DiscoveredContainer] = field(default_factory=list)
    containers_scanned: bool = False
    stopped_containers: list[DiscoveredContainer] = field(default_factory=list)
    stopped_containers_scanned: bool = False
    container_images: list[DiscoveredContainerImage] = field(default_factory=list)
    container_images_scanned: bool = False
    container_images_truncated: bool = False
    wsl_distros: list[DiscoveredWSLDistro] = field(default_factory=list)
    wsl_scanned: bool = False
    wsl_container_scanned_distros: list[str] = field(default_factory=list)
    detected_clients: list[DetectedClient] = field(default_factory=list)
    phase_durations_ms: dict[str, int] = field(default_factory=dict)
    # Governor abort message when the scan was cut short by a resource cap.
    # Findings are partial (every affected surface is already incomplete);
    # the command uploads them, then reports the scan as failed.
    resource_limit_exceeded: str | None = None
    skill_crawl_complete: bool = False
    project_scan_depth: int = 7
    project_scan_home: str | None = None
    project_skill_candidate_paths: list[str] = field(default_factory=list)
    global_skill_candidate_paths: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if (
            self.scan_started_at.tzinfo is None
            or self.scan_started_at.utcoffset() is None
        ):
            raise ValueError("scan_started_at must be timezone-aware")
        self.scan_started_at = self.scan_started_at.astimezone(datetime.timezone.utc)

    @property
    def total_servers(self) -> int:
        return sum(len(c.servers) for c in self.configurations)

    @property
    def total_detected_clients(self) -> int:
        return len(self.detected_clients)

    @property
    def total_skills(self) -> int:
        return len(self.skills)

    @property
    def total_agents(self) -> int:
        return len(self.agents)

    @property
    def total_agent_definitions(self) -> int:
        return len(self.agent_definitions)

    @property
    def total_processes(self) -> int:
        return len(self.processes)

    @property
    def total_containers(self) -> int:
        return len(self.containers)

    @property
    def total_wsl_distros(self) -> int:
        return len(self.wsl_distros)

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
    def container_configs(self) -> list[MCPClientConfig]:
        return [c for c in self.configurations if c.config_scope == "container"]

    @property
    def wsl_configs(self) -> list[MCPClientConfig]:
        return [c for c in self.configurations if c.config_scope == "wsl"]

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

    def container_scan_failure_reason(self) -> str:
        return (
            sanitize_container_scan_error(
                self.container_scan_error or CONTAINER_SCAN_INCOMPLETE_REASON
            )
            or CONTAINER_SCAN_INCOMPLETE_REASON
        )

    def to_api_payload(self) -> dict[str, Any]:
        """The MCP-scan submission contract.

        This is what actually goes over the wire (see ``submit_mcp_watch_scan``).
        It includes device context, tools, detected AI clients, MCP
        configurations, and redacted runtime process sightings. Skills,
        plugins, framework agents, and client-native agent definitions each
        submit through their own endpoints.
        For the complete *display* view (dry-run), use :meth:`to_full_payload`.
        """
        payload: dict[str, Any] = {
            **device_context_dict(self),
            "scan_session_id": str(self.scan_session_id),
            "scan_started_at": self.scan_started_at.astimezone(
                datetime.timezone.utc
            ).isoformat(),
            "scan_duration_ms": self.scan_duration_ms,
            "collector_version": self.collector_version,
            "tools": self.tools,
            "detected_clients": [
                {
                    "client": client.client,
                    "display_name": client.display_name,
                    "client_version": client.client_version,
                    "detected_via": client.detected_via,
                    "evidence_origin": client.evidence_origin,
                    "config_paths": [
                        strip_reported_path_prefix(path) for path in client.config_paths
                    ],
                    **(
                        {
                            "wsl_contexts": [
                                context.to_api_payload()
                                for context in client.wsl_contexts
                            ]
                        }
                        if client.wsl_contexts
                        else {}
                    ),
                }
                for client in self.detected_clients
            ],
            "configurations": [
                {
                    "client": c.client,
                    "client_version": c.client_version,
                    "config_path": strip_reported_path_prefix(c.config_path),
                    "config_modified_at": c.config_modified_at,
                    "config_scope": c.config_scope,
                    "project_path": strip_reported_path_prefix(c.project_path),
                    "plugin_identifier": c.plugin_identifier,
                    **(
                        {
                            "wsl": {
                                "distro": c.wsl_distro,
                                "user": c.wsl_user,
                            }
                        }
                        if c.wsl_distro is not None and c.container_id is None
                        else {}
                    ),
                    **(
                        {
                            "container": {
                                "container_id": c.container_id,
                                "name": c.container_name,
                                "image_ref": c.container_image_ref,
                                "image_digest": c.container_image_digest,
                                "is_devcontainer": bool(c.container_is_devcontainer),
                                "mounts_host_home": bool(c.container_mounts_host_home),
                            }
                        }
                        if c.container_id
                        else {}
                    ),
                    "servers": [
                        {
                            "name": s.name,
                            "type": _coerce_transport_type_for_api(
                                s.type, has_url=bool(s.url)
                            ),
                            # command/args/url upload verbatim: they are the
                            # config-identity inputs — the backend re-derives
                            # config_hash and container identity from them, so
                            # client-side redaction would re-key the org
                            # catalog. TODO(ENG-4542): redact literal secrets
                            # in args/url once the backend hashes the same
                            # redacted form.
                            "command": s.command,
                            "args": _stringify_args(s.args),
                            "url": s.url,
                            "env": redact_config_mapping(
                                _stringify_str_mapping(s.env),
                                allowed_literal_keys=BENIGN_ENV_KEYS,
                            ),
                            "headers": redact_config_mapping(
                                _stringify_str_mapping(s.headers)
                            ),
                            "config_hash": s.config_hash,
                            "runtime": s.runtime,
                            "image_ref": s.image_ref,
                            "image_digest": s.image_digest,
                            **(
                                {
                                    "command_invalid": True,
                                    "command_invalid_reason": (
                                        s.command_invalid_reason
                                    ),
                                }
                                if s.command_invalid
                                else {}
                            ),
                            "project_names": (
                                [strip_reported_path_prefix(p) for p in s.project_name]
                                if isinstance(s.project_name, list)
                                else strip_reported_path_prefix(s.project_name)
                            ),
                        }
                        for s in c.servers
                    ],
                }
                for c in self.configurations
            ],
        }
        if self.is_wsl:
            payload["is_wsl"] = True
        if self.wsl_scanned:
            payload["wsl_distros"] = [
                distro.to_api_payload() for distro in self.wsl_distros
            ]
        if self.processes:
            payload["processes"] = [
                process.to_api_payload() for process in self.processes
            ]
        if self.container_scan_requested:
            payload["containers"] = [
                container.to_api_payload() for container in self.containers
            ]
            payload["host_containers_scanned"] = self.containers_scanned
            payload["wsl_container_scanned_distros"] = (
                self.wsl_container_scanned_distros
            )
            if not self.containers_scanned:
                payload["container_scan_error"] = self.container_scan_failure_reason()
        if self.stopped_containers_scanned:
            payload["stopped_containers"] = [
                container.to_api_payload() for container in self.stopped_containers
            ]
        if self.container_images_scanned:
            payload["container_images"] = [
                image.to_api_payload() for image in self.container_images
            ]
            payload["container_images_truncated"] = self.container_images_truncated
        return payload

    def to_full_payload(self, *, include_agents: bool = False) -> dict[str, Any]:
        """The complete scan view for *display* (``scan --dry-run``).

        Builds on :meth:`to_api_payload` (the MCP wire submission) and folds back
        the strands submitted through their own endpoints so a dry-run prints
        exactly what was found in one object: ``skills``, ``plugins``, and
        client-native ``agent_definitions`` plus, when ``include_agents`` is set,
        the framework ``agents`` view (the richer local ``to_dict`` shape, not
        the redacted wire payload -- dry-run is local-only and shows the operator
        everything detected). Centralizing this here keeps the formerly-inline
        patch sites from drifting into different shapes.

        Runtime ``processes`` use their richer local view here so dry-run keeps
        the internal ``runtime_probe`` source omitted from version-tolerant wire
        submissions.
        """
        payload = self.to_api_payload()
        if self.processes:
            payload["processes"] = [process.to_dict() for process in self.processes]
        if self.containers and "containers" not in payload:
            payload["containers"] = [
                container.to_api_payload() for container in self.containers
            ]
        if self.wsl_distros and "wsl_distros" not in payload:
            payload["wsl_distros"] = [
                distro.to_api_payload() for distro in self.wsl_distros
            ]
        if self.skills:
            payload["skills"] = [s.to_api_payload() for s in self.skills]
        if self.plugins:
            payload["plugins"] = [p.to_api_payload() for p in self.plugins]
        if include_agents and self.agents:
            payload["agents"] = [a.to_dict() for a in self.agents]
        if self.agent_definitions:
            payload["agent_definitions"] = [
                definition.to_api_payload() for definition in self.agent_definitions
            ]
        payload["phase_durations_ms"] = dict(sorted(self.phase_durations_ms.items()))
        return payload

    def to_agent_report_payload(self) -> dict[str, Any]:
        """The per-agent *submission* contract for ``POST /ai-watch/agents``.

        Device context + redacted discovered agents. Only real agents
        (``is_agent`` -- a non-null ``framework_id``) are sent, capped at
        :data:`MAX_AGENTS`. Each agent is scrubbed by
        :meth:`DiscoveredAgent.to_api_payload` (never file contents or env), with
        the scan's own username threaded in so it is redacted from paths /
        evidence even outside the standard home layout. Under ``--all-users`` each
        profile is a separate ``scan --username <user>`` child, so ``self.username``
        is the single authoritative owner of every discovered path.

        An outlier host over :data:`MAX_AGENTS` submits a silently-incomplete
        report, so log when the cap truncates -- parity with the time-budget
        walk's ``truncated`` signal (:func:`agent_scan.discover_static_agents`).
        """
        agents = [a for a in self.agents if a.is_agent]
        usernames = [self.username] if self.username else []
        if len(agents) > MAX_AGENTS:
            logger.warning(
                "agent_report_truncated",
                detected=len(agents),
                sent=MAX_AGENTS,
            )
        return {
            **device_context_dict(self),
            "scan_session_id": str(self.scan_session_id),
            "scan_started_at": self.scan_started_at.astimezone(
                datetime.timezone.utc
            ).isoformat(),
            "agents": [
                a.to_api_payload(usernames=usernames) for a in agents[:MAX_AGENTS]
            ],
        }

    def to_agent_definition_report_payload(self) -> dict[str, Any]:
        """Bounded client-native agent-definition submission contract."""
        if len(self.agent_definitions) > MAX_AGENT_DEFINITIONS:
            logger.warning(
                "agent_definition_report_truncated",
                detected=len(self.agent_definitions),
                sent=MAX_AGENT_DEFINITIONS,
            )
        return {
            **device_context_dict(self),
            "scan_session_id": str(self.scan_session_id),
            "scan_started_at": self.scan_started_at.astimezone(
                datetime.timezone.utc
            ).isoformat(),
            "agent_definitions": [
                definition.to_api_payload()
                for definition in self.agent_definitions[:MAX_AGENT_DEFINITIONS]
            ],
        }


def scan_all_clients(
    device_id: str | None = None,
    org_device_id: str | None = None,
    collector_version: str = "unknown",
    scan_projects: bool = True,
    project_scan_timeout: int = 60,
    project_scan_depth: int = 7,
    username_override: str | None = None,
    windows_user_sid: str | None = None,
    windows_system_profile: bool = False,
    machine_scope: bool = True,
    detect_agents: bool = True,
    detect_agent_frameworks: bool = True,
    detect_processes: bool = False,
    detect_containers: bool = False,
    detect_disguised_skills: bool = False,
    detect_renamed_plugin_caches: bool = False,
    cpu_cores: int | None = None,
    max_cpu_percent: int | None = None,
    memory_limit_mb: int | None = None,
    governor: ResourceGovernor | None = None,
) -> ScanResult:
    """
    Scan all known MCP client configurations (global and project-level).

    A cooperative :class:`ResourceGovernor` wraps the whole scan: it throttles
    CPU at phase/loop checkpoints and aborts (raising
    :class:`ScanResourceLimitExceeded`) if the ``tracemalloc`` high-water mark
    trips the memory cap. Caps are best-effort and default to the values in
    :func:`build_governor`.

    Args:
        device_id: Override device ID (uses auto-generated if None)
        org_device_id: Organization-provided device ID (e.g., from MDM)
        collector_version: Version of the CLI performing the scan
        scan_projects: Whether to scan for project-level configs (default True)
        project_scan_timeout: Timeout in seconds for project scanning (default 60)
        project_scan_depth: Max directory depth for project scanning (default 7)
        username_override: Explicit username, bypasses auto-detection
        windows_user_sid: Internal target Windows profile SID
        windows_system_profile: Internal safety context for a target profile
            scanned from a SYSTEM child instead of its logged-on user token
        machine_scope: Include machine-wide builtin extension roots. Multi-user
            orchestrators enable this for exactly one child.
        detect_agents: Master switch for ALL agent detection (on by default). It
            runs the install-channel probes (e.g. OpenClaw) and gates the static
            scan below. False disables every channel.
        detect_agent_frameworks: Switch for the STATIC framework scan (manifest +
            source scoring). ON by default: discovered agents now submit to the
            backend (POST /ai-watch/agents), so the extra crawl/walk I/O buys real
            fleet visibility. Requires detect_agents; the install channel is
            unaffected and stays on with detect_agents alone.
        detect_processes: Opt-in runtime process-discovery channel (PHASE 12).
            OFF by default. Enumerates running processes + listening sockets,
            scores AI-relatedness, and correlates back to the config scan.
            Discovered processes are submitted with the MCP scan payload.
        detect_containers: Temporary opt-in for running-container artifact
            discovery (PHASE 13) and, on Windows, bounded project config, skill,
            and agent-definition discovery across WSL home UNC paths
            (PHASE 13b). Both are best-effort/non-fatal.
        detect_disguised_skills: Opt-in browser/cache probe for disguised skill
            artifacts (PHASE 9b). OFF by default.
        detect_renamed_plugin_caches: Opt-in marker-based probe for renamed
            plugin cache directories under known client roots (PHASE 10b).
            OFF by default.
        cpu_cores: Scan concurrency ceiling (None => half logical cores).
        max_cpu_percent: Single-core-equivalent CPU duty budget; 50 means
            0.5 core regardless host size (None => default).
        memory_limit_mb: Peak scan-memory growth ceiling in MB (RSS since
            governor enter; Python-heap fallback where the resource module is
            unavailable); exceeding it aborts the scan (None => default).
        governor: Pre-built governor (test seam). When given, the three cap
            args are ignored and this governor is entered directly.

    Returns:
        ScanResult with all discovered configurations
    """
    active_governor = governor or build_governor(
        cpu_cores=cpu_cores,
        max_cpu_percent=max_cpu_percent,
        memory_limit_mb=memory_limit_mb,
    )
    with _IN_PROCESS_SCAN_LOCK, active_governor:
        try:
            return _scan_all_clients_impl(
                active_governor,
                device_id=device_id,
                org_device_id=org_device_id,
                collector_version=collector_version,
                scan_projects=scan_projects,
                project_scan_timeout=project_scan_timeout,
                project_scan_depth=project_scan_depth,
                username_override=username_override,
                windows_user_sid=windows_user_sid,
                windows_system_profile=windows_system_profile,
                machine_scope=machine_scope,
                detect_agents=detect_agents,
                detect_agent_frameworks=detect_agent_frameworks,
                detect_processes=detect_processes,
                detect_containers=detect_containers,
                detect_disguised_skills=detect_disguised_skills,
                detect_renamed_plugin_caches=detect_renamed_plugin_caches,
            )
        finally:
            reset_plugin_scan_state()
            reset_skill_scan_state()
            cache_clear = getattr(get_wsl_distro_inventory, "cache_clear", None)
            if cache_clear is not None:
                cache_clear()


def _config_dedupe_key(
    config: MCPClientConfig,
) -> tuple[str, str, tuple[str, ...], int, int] | None:
    """Identify aliases only when both paths resolve to one backing file."""
    if (
        config.config_scope == "container"
        and config.container_mounts_host_home is not True
    ):
        return None
    if not config.config_path or not config.project_path or not config.servers:
        return None

    config_parts = tuple(
        part
        for part in config.config_path.replace("\\", "/").split("/")
        if part not in {"", "."}
    )
    project_parts = tuple(
        part
        for part in config.project_path.replace("\\", "/").split("/")
        if part not in {"", "."}
    )
    project_prefix = tuple(part.casefold() for part in project_parts)
    config_prefix = tuple(
        part.casefold() for part in config_parts[: len(project_parts)]
    )
    hashes = tuple(sorted(server.config_hash for server in config.servers))
    if (
        not project_parts
        or len(config_parts) <= len(project_parts)
        or config_prefix != project_prefix
        or any(not config_hash for config_hash in hashes)
    ):
        return None
    try:
        backing = os.stat(config.config_path)
    except (OSError, ValueError):
        return None
    if not stat.S_ISREG(backing.st_mode) or not backing.st_ino:
        return None

    relative_path = "/".join(config_parts[len(project_parts) :])
    return config.client, relative_path, hashes, backing.st_dev, backing.st_ino


def dedupe_host_container_configurations(
    configurations: list[MCPClientConfig],
) -> list[MCPClientConfig]:
    """Prefer container attribution only for verified host-file aliases."""
    container_keys = {
        key
        for config in configurations
        if config.config_scope == "container"
        if (key := _config_dedupe_key(config)) is not None
    }
    return [
        config
        for config in configurations
        if config.config_scope == "container"
        or config.wsl_distro is not None
        or _config_dedupe_key(config) not in container_keys
    ]


def _process_owner_matches_effective_user(process_owner: str) -> bool:
    """Return whether a process owner identifies the scanner's effective user."""

    get_euid = getattr(os, "geteuid", None)
    if callable(get_euid):
        try:
            effective_uid = get_euid()
        except OSError:
            return False
        if process_owner == str(effective_uid):
            return True
        if pwd is None:
            return False
        try:
            effective_username = pwd.getpwuid(effective_uid).pw_name
        except (KeyError, OSError):
            return False
        return process_owner == effective_username

    try:
        effective_username = getpass.getuser()
    except (KeyError, OSError):
        return False
    return process_owner.casefold() == effective_username.casefold()


@dataclass(frozen=True)
class _ResolvedOverrideConfigPath:
    host_path: Path
    reported_path: str


def _resolve_wsl_override_config_path(
    ref: OverrideConfigRef | ExtensionRootRef,
) -> _ResolvedOverrideConfigPath | None:
    owner = (ref.user or "").strip()
    if (
        not owner
        or owner in {".", ".."}
        or any(character in owner for character in ("/", "\\", "\x00"))
        or "\\" in ref.value
    ):
        return None
    try:
        linux_path = PurePosixPath(ref.value)
        if not linux_path.is_absolute():
            if ref.cwd is None:
                return None
            cwd = PurePosixPath(ref.cwd)
            if not cwd.is_absolute():
                return None
            linux_path = cwd / linux_path
        if ".." in linux_path.parts:
            return None
        if getattr(ref, "mcp_config", None) == "user_data_dir":
            linux_path = linux_path / "User" / "mcp.json"
        expected_home = (
            PurePosixPath("/root")
            if owner == "root"
            else PurePosixPath("/home") / owner
        )
        linux_path.relative_to(expected_home)
    except (OSError, RuntimeError, ValueError):
        return None

    distro_root = get_wsl_distro_root(ref.wsl_distro or "")
    if distro_root is None:
        return None
    return _ResolvedOverrideConfigPath(
        host_path=distro_root.joinpath(*linux_path.parts[1:]),
        reported_path=linux_path.as_posix(),
    )


def _resolve_override_config_path(
    ref: OverrideConfigRef | ExtensionRootRef,
) -> _ResolvedOverrideConfigPath | None:
    """Resolve one raw process flag value without guessing a missing cwd."""

    if getattr(ref, "wsl_distro", None) is not None:
        return _resolve_wsl_override_config_path(ref)
    try:
        path = Path(ref.value).expanduser()
        if not path.is_absolute():
            if ref.cwd is None:
                return None
            path = Path(ref.cwd) / path
        if getattr(ref, "mcp_config", None) == "user_data_dir":
            path = path / "User" / "mcp.json"
    except (OSError, RuntimeError, ValueError):
        return None
    return _ResolvedOverrideConfigPath(
        host_path=path,
        reported_path=str(path),
    )


def _normalized_host_path(path: str | Path) -> str:
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def _override_config_path_key(
    path: str | Path,
    *,
    wsl_distro: str | None,
    wsl_user: str | None,
) -> tuple[str, str, str | None, str | None]:
    """Identify one config path within its host or WSL namespace."""
    if wsl_distro is None:
        return ("host", _normalized_host_path(path), None, None)

    parsed = parse_wsl_unc_path(path)
    linux_path = (
        parsed.linux_path
        if parsed is not None and parsed.distro.casefold() == wsl_distro.casefold()
        else PurePosixPath(os.fspath(path)).as_posix()
    )
    return ("wsl", linux_path, wsl_distro.casefold(), wsl_user)


def _resolve_windows_process_owners(
    refs: Sequence[OverrideConfigRef | ExtensionRootRef],
    scan_status: ScanCompletionStatus | None = None,
) -> dict[int, str]:
    """Resolve owners for ownerless process refs in one bounded query."""

    pids: list[int] = []
    seen_pids: set[int] = set()
    for ref in refs:
        pid = ref.pid
        if (
            getattr(ref, "wsl_distro", None) is not None
            or ref.user is not None
            or type(pid) is not int
            or pid <= 0
            or pid in seen_pids
        ):
            continue
        seen_pids.add(pid)
        pids.append(pid)
        if len(pids) > MAX_OVERRIDE_OWNER_LOOKUPS:
            if scan_status is not None:
                scan_status.mark_incomplete("runtime_owner_resolution_capped")
            pids.pop()
            break
    if not pids:
        return {}

    process_filter = " OR ".join(f"ProcessId = {pid}" for pid in pids)
    script = (
        "$ErrorActionPreference = 'Stop'; "
        f"$processes = @(Get-CimInstance Win32_Process -Filter '{process_filter}'); "
        "$owners = @($processes | ForEach-Object { "
        "$process = $_; $owner = $null; "
        "try { $owner = Invoke-CimMethod -InputObject $process "
        "-MethodName GetOwner -ErrorAction Stop } catch {} "
        "if ($null -ne $owner -and $owner.ReturnValue -eq 0 "
        "-and -not [string]::IsNullOrWhiteSpace($owner.User)) { "
        "[PSCustomObject]@{ ProcessId = [int]$process.ProcessId; "
        "User = [string]$owner.User } } "
        "}); ConvertTo-Json -InputObject $owners -Compress"
    )
    try:
        completed = subprocess.run(
            [
                "powershell.exe",
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                script,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        if scan_status is not None:
            scan_status.mark_incomplete("runtime_owner_resolution_failed")
        return {}
    if completed.returncode != 0:
        if scan_status is not None:
            scan_status.mark_incomplete("runtime_owner_resolution_failed")
        return {}

    outcome = parse_json(completed.stdout)
    if outcome["error"] is not None:
        if scan_status is not None:
            scan_status.mark_incomplete("runtime_owner_resolution_failed")
        return {}
    payload = outcome["value"]
    if isinstance(payload, dict):
        entries = [payload]
    elif isinstance(payload, list):
        entries = payload
    else:
        return {}

    owners: dict[int, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            return {}
        pid = entry.get("ProcessId")
        username = entry.get("User")
        if (
            type(pid) is int
            and pid in pids
            and isinstance(username, str)
            and username.strip()
        ):
            owners[pid] = username.strip()
    return owners


_OwnerSkipLogEvent = Literal[
    "process_override_config_skipped_untrusted_owner",
    "process_extension_root_skipped_untrusted_owner",
]


@dataclass(frozen=True)
class _TrustedOwnerResolver:
    """Resolve and enforce one process-owner trust policy for raw path refs."""

    windows_user_sid: str | None
    scan_status: ScanCompletionStatus | None
    windows_owners: Mapping[int, str]
    untrusted_log_event: _OwnerSkipLogEvent

    @classmethod
    def for_refs(
        cls,
        refs: Sequence[OverrideConfigRef | ExtensionRootRef],
        *,
        windows_user_sid: str | None,
        scan_status: ScanCompletionStatus | None,
        untrusted_log_event: _OwnerSkipLogEvent,
    ) -> _TrustedOwnerResolver:
        windows_owners = (
            _resolve_windows_process_owners(refs, scan_status)
            if sys.platform == "win32" and windows_user_sid is None
            else {}
        )
        return cls(
            windows_user_sid=windows_user_sid,
            scan_status=scan_status,
            windows_owners=windows_owners,
            untrusted_log_event=untrusted_log_event,
        )

    def resolve(self, ref: OverrideConfigRef | ExtensionRootRef) -> str | None:
        wsl_distro = getattr(ref, "wsl_distro", None)
        owner = ref.user
        if wsl_distro is None and owner is None and ref.pid is not None:
            owner = self.windows_owners.get(ref.pid)
        process_owner = owner.strip() if owner is not None else ""
        owner_sid = getattr(ref, "owner_sid", None)
        owner_is_trusted = bool(process_owner) and wsl_distro is not None
        if wsl_distro is None and self.windows_user_sid is not None:
            owner_is_trusted = (
                owner_sid is not None
                and owner_sid.casefold() == self.windows_user_sid.casefold()
            )
            if owner_sid is None and self.scan_status is not None:
                self.scan_status.mark_incomplete("runtime_owner_resolution_failed")
        elif wsl_distro is None:
            owner_is_trusted = bool(process_owner) and (
                _process_owner_matches_effective_user(process_owner)
            )
        if owner_is_trusted:
            return process_owner

        logger.debug(
            self.untrusted_log_event,
            client=ref.client,
            flag=ref.flag,
            owner_status="unknown" if not process_owner else "mismatch",
        )
        return None


def _parse_process_override_configurations(
    refs: list[OverrideConfigRef],
    *,
    configurations: list[MCPClientConfig],
    clients: list[MCPClientDefinition],
    scan_status: ScanCompletionStatus | None = None,
    windows_user_sid: str | None = None,
) -> list[MCPClientConfig]:
    """Best-effort parse configs referenced by detected client launch flags."""

    clients_by_name = {client.name: client for client in clients}
    seen_paths = {
        _override_config_path_key(
            config.config_path,
            wsl_distro=config.wsl_distro,
            wsl_user=config.wsl_user,
        )
        for config in configurations
        if config.config_path is not None
    }
    owner_resolver = _TrustedOwnerResolver.for_refs(
        refs,
        windows_user_sid=windows_user_sid,
        scan_status=scan_status,
        untrusted_log_event="process_override_config_skipped_untrusted_owner",
    )
    parsed: list[MCPClientConfig] = []
    for ref in refs:
        wsl_distro = getattr(ref, "wsl_distro", None)
        process_owner = owner_resolver.resolve(ref)
        if process_owner is None:
            continue
        client = clients_by_name.get(ref.client)
        if client is None:
            continue
        path_resolution = _resolve_override_config_path(ref)
        if path_resolution is None:
            if scan_status is not None:
                scan_status.mark_incomplete(
                    "runtime_override_config_path_resolution_failed"
                )
            continue
        config_path = path_resolution.host_path
        path_key = _override_config_path_key(
            path_resolution.reported_path,
            wsl_distro=wsl_distro,
            wsl_user=process_owner if wsl_distro is not None else None,
        )
        if path_key in seen_paths:
            continue
        seen_paths.add(path_key)
        try:
            config_stat = os.stat(config_path)
        except (OSError, ValueError):
            if scan_status is not None:
                scan_status.mark_incomplete("runtime_override_config_stat_failed")
            logger.debug(
                "process_override_config_skipped_unsafe_file",
                client=ref.client,
                flag=ref.flag,
                file_status="stat_failed",
            )
            continue
        if not stat.S_ISREG(config_stat.st_mode):
            file_status = "not_regular"
        elif config_stat.st_size > MAX_OVERRIDE_CONFIG_BYTES:
            file_status = "too_large"
        else:
            file_status = None
        if file_status is not None:
            if scan_status is not None:
                scan_status.mark_incomplete(f"runtime_override_config_{file_status}")
            logger.debug(
                "process_override_config_skipped_unsafe_file",
                client=ref.client,
                flag=ref.flag,
                file_status=file_status,
            )
            continue
        try:
            config = parse_config_file(
                client,
                config_path,
                redact_path_in_logs=True,
                scan_status=scan_status,
            )
        except Exception as exc:
            if scan_status is not None:
                scan_status.mark_incomplete("runtime_override_config_parse_failed")
            # error_type only: exception messages can embed the raw argv path.
            logger.warning(
                "process_override_config_parse_failed",
                client=ref.client,
                flag=ref.flag,
                error_type=type(exc).__name__,
            )
            continue
        if config is not None:
            config.config_scope = "process_override"
            config.config_path = path_resolution.reported_path
            if wsl_distro is not None:
                config.wsl_distro = wsl_distro
                config.wsl_user = process_owner
            parsed.append(config)
    return parsed


def _resolve_process_extension_roots(
    refs: list[ExtensionRootRef],
    scan_status: ScanCompletionStatus | None = None,
    windows_user_sid: str | None = None,
) -> list[VSCodeExtensionRoot]:
    """Resolve trusted process-owned extension roots without reporting raw argv."""

    owner_resolver = _TrustedOwnerResolver.for_refs(
        refs,
        windows_user_sid=windows_user_sid,
        scan_status=scan_status,
        untrusted_log_event="process_extension_root_skipped_untrusted_owner",
    )
    if len(refs) > MAX_OVERRIDE_OWNER_LOOKUPS and scan_status is not None:
        scan_status.mark_incomplete("runtime_extension_root_capped")
    roots: list[VSCodeExtensionRoot] = []
    seen_paths: set[tuple[str, str, str | None, str | None]] = set()
    for ref in refs[:MAX_OVERRIDE_OWNER_LOOKUPS]:
        wsl_distro = ref.wsl_distro
        process_owner = owner_resolver.resolve(ref)
        if process_owner is None:
            continue

        path_resolution = _resolve_override_config_path(ref)
        if path_resolution is None:
            if scan_status is not None:
                scan_status.mark_incomplete(
                    "runtime_extension_root_path_resolution_failed"
                )
            continue
        path_key = _override_config_path_key(
            path_resolution.reported_path,
            wsl_distro=wsl_distro,
            wsl_user=process_owner if wsl_distro is not None else None,
        )
        if path_key in seen_paths:
            continue
        seen_paths.add(path_key)
        try:
            root_stat = os.stat(path_resolution.host_path)
        except (OSError, ValueError):
            if scan_status is not None:
                scan_status.mark_incomplete("runtime_extension_root_stat_failed")
            continue
        if not stat.S_ISDIR(root_stat.st_mode):
            if scan_status is not None:
                scan_status.mark_incomplete("runtime_extension_root_not_directory")
            continue
        roots.append(
            VSCodeExtensionRoot(
                path=path_resolution.host_path,
                client=ref.client,
                wsl_distro=wsl_distro,
            )
        )
    return roots


def _dedupe_path_configurations(
    configurations: list[MCPClientConfig],
) -> list[MCPClientConfig]:
    """Keep one exact config path per client and attribution identity.

    This runs over every config, not just the WSL additions, so the key carries
    the whole attribution a backend installation is keyed by. One config path
    legitimately repeats across identities: a plugin config referenced by
    several projects, one in-container path present in two containers, and one
    Linux path under two distros are distinct installs, not re-discoveries.
    """
    deduped: list[MCPClientConfig] = []
    seen: set[tuple[str | None, ...]] = set()
    for config in configurations:
        if config.config_path is not None:
            key = (
                config.client,
                config.config_path,
                config.config_scope,
                config.project_path,
                config.container_id,
                config.wsl_distro.casefold() if config.wsl_distro else None,
                config.wsl_user,
            )
            if key in seen:
                continue
            seen.add(key)
        deduped.append(config)
    return deduped


_AssembledT = TypeVar("_AssembledT")


def _best_effort_assembly(
    step: str,
    work: Callable[[], _AssembledT],
    *,
    fallback: _AssembledT,
    completeness: ScanCompleteness,
    surfaces: tuple[str, ...],
) -> _AssembledT:
    """Run one post-phase assembly step without letting it sink the scan.

    The phases themselves are best-effort, but the dedupe / attribution /
    presence-merge steps that stitch their results together used to run bare
    in ``scan_all_clients``: one bug there raised out of the scan and the
    device reported nothing. On failure the untransformed input is kept and
    the affected completeness surfaces record ``assembly_step_failed``.
    """
    try:
        return work()
    except ScanResourceLimitExceeded:
        raise
    except Exception:
        completeness.mark_incomplete("assembly_step_failed", *surfaces)
        logger.warning("assembly_step_failed", step=step, exc_info=True)
        return fallback


@dataclass
class _SequentialPhaseGuard:
    """Governor-abort boundary for the sequential phases (0, 12-14).

    Mirrors :class:`ResourceAbortGuard` for the phases that run after the
    concurrent graph: once the governor's latch trips, each remaining phase
    returns its ``fallback`` with every surface it feeds marked
    ``resource_limit_exceeded``, so the partial manifest is still assembled.
    """

    governor: ResourceGovernor
    timer: PhaseTimer
    completeness: ScanCompleteness
    reason: str | None = None

    def run(
        self,
        name: str,
        work: Callable[[], _AssembledT],
        *,
        fallback: _AssembledT,
        surfaces: tuple[str, ...],
    ) -> _AssembledT:
        try:
            return run_timed_phase(self.timer, name, self.governor, work)
        except ScanResourceLimitExceeded as exc:
            if self.reason is None:
                self.reason = str(exc) or "scan resource limit exceeded"
            self.completeness.mark_incomplete(RESOURCE_LIMIT_EXCEEDED_REASON, *surfaces)
            logger.warning(
                "scan_phase_aborted_by_resource_limit", phase=name, error=str(exc)
            )
            return fallback


def _filter_presence_gated_project_configurations(
    configurations: list[MCPClientConfig],
    *,
    clients: list[MCPClientDefinition],
    probed_clients: list[DetectedClient],
    presence_status: ScanCompletionStatus,
) -> list[MCPClientConfig]:
    """Drop shared project configs when their client lacks an install signal.

    Only a *complete* presence scan may gate: if any probe failed or was cut
    short, a missing install signal is not evidence of absence, and dropping
    the shared-path config would silently lose a real finding.
    """
    if not presence_status.complete:
        logger.info(
            "presence_gate_skipped_incomplete_presence_scan",
            reasons=presence_status.reasons,
        )
        return configurations
    present_clients = {client.client for client in probed_clients}
    gated_patterns = {
        client.name: [
            tuple(
                part.casefold()
                for part in pattern.relative_path.replace("\\", "/").split("/")
                if part not in {"", "."}
            )
            for pattern in client.iter_project_configs()
            if pattern.requires_client_presence
        ]
        for client in clients
    }

    filtered: list[MCPClientConfig] = []
    for config in configurations:
        patterns = gated_patterns.get(config.client, [])
        if (
            config.client not in present_clients
            and config.config_scope in {"project", "wsl", "container"}
            and patterns
            and config.config_path
            and config.project_path
        ):
            config_parts = tuple(
                part.casefold()
                for part in config.config_path.replace("\\", "/").split("/")
                if part not in {"", "."}
            )
            project_parts = tuple(
                part.casefold()
                for part in config.project_path.replace("\\", "/").split("/")
                if part not in {"", "."}
            )
            if any(config_parts == (*project_parts, *pattern) for pattern in patterns):
                continue
        filtered.append(config)
    return filtered


def _scan_all_clients_impl(
    governor: ResourceGovernor,
    *,
    device_id: str | None = None,
    org_device_id: str | None = None,
    collector_version: str = "unknown",
    scan_projects: bool = True,
    project_scan_timeout: int = 60,
    project_scan_depth: int = 7,
    username_override: str | None = None,
    windows_user_sid: str | None = None,
    windows_system_profile: bool = False,
    machine_scope: bool = True,
    detect_agents: bool = True,
    detect_agent_frameworks: bool = True,
    detect_processes: bool = False,
    detect_containers: bool = False,
    detect_disguised_skills: bool = False,
    detect_renamed_plugin_caches: bool = False,
) -> ScanResult:
    """Run the scan phases under an already-entered *governor*.

    Split out from :func:`scan_all_clients` so the public entry point owns the
    governor lifecycle (build + ``with``). Phases 1-11 run as a bounded dependency
    graph; phases 12-14 stay sequential because they consume assembled configs.
    The crawl shards are governed via ``find_files_under_home(governor=...)``.
    """
    scan_started_at = datetime.datetime.now(datetime.timezone.utc)
    start_time = time.monotonic()
    scan_session_id = uuid.uuid4()
    effective_project_scan_depth = _clamp_scan_bound(
        project_scan_depth,
        default=7,
        maximum=MAX_PROJECT_DEPTH,
    )
    reported_home = strip_reported_path_prefix(str(Path.home()))

    # The static agent-framework scan runs by default (its results now submit to
    # the backend), widening the agent-manifest crawl and walking source trees. It
    # still rides the detect_agents master switch and can be turned off explicitly
    # via detect_agent_frameworks=False; the install channel (OpenClaw) is
    # unaffected and rides detect_agents alone.
    run_static_agents = detect_agents and detect_agent_frameworks

    # Get device info
    actual_device_id = device_id or get_or_create_device_id()
    device_metadata = get_device_metadata()

    if username_override:
        device_metadata["username"] = username_override
    wsl_distros: list[DiscoveredWSLDistro] = []
    wsl_scanned = False
    if device_metadata.get("os") == "windows":
        wsl_inventory = get_wsl_distro_inventory()
        wsl_distros = list(wsl_inventory.distros)
        wsl_scanned = wsl_inventory.success
    tools = get_installed_tools()
    if collector_version:
        tools.append({"name": "scan-collector", "version": collector_version})

    timer = PhaseTimer()
    completeness = ScanCompleteness()
    phase_guard = _SequentialPhaseGuard(governor, timer, completeness)
    if wsl_scanned:
        wsl_distros = phase_guard.run(
            "phase_0_wsl_runtime_file_signals",
            lambda: scan_wsl_runtime_file_signals(
                wsl_distros,
                checkpoint=governor.checkpoint,
            ),
            fallback=wsl_distros,
            surfaces=("wsl_static", "runtime"),
        )
    else:
        timer.record("phase_0_wsl_runtime_file_signals", 0)
    clients = get_all_clients()
    concurrent_result: ConcurrentScanResult = run_concurrent_scan_phases(
        clients=clients,
        governor=governor,
        timer=timer,
        scan_projects=scan_projects,
        project_scan_timeout=project_scan_timeout,
        project_scan_depth=effective_project_scan_depth,
        detect_agents=detect_agents,
        run_static_agents=run_static_agents,
        detect_disguised_skills=detect_disguised_skills,
        detect_renamed_plugin_caches=detect_renamed_plugin_caches,
        machine_scope=machine_scope,
    )
    completeness.merge(concurrent_result.completeness)
    if device_metadata.get("os") == "windows" and not wsl_scanned:
        completeness.wsl_static.mark_incomplete("wsl_inventory_incomplete")
        completeness.plugin_host_static.mark_incomplete("wsl_inventory_incomplete")
        completeness.client_presence.mark_incomplete("wsl_inventory_incomplete")
    configurations = concurrent_result.configurations
    extension_clients = concurrent_result.extension_clients
    all_skills = concurrent_result.skills
    all_plugins = concurrent_result.plugins
    all_agents = concurrent_result.agents
    all_agent_definitions = list(concurrent_result.agent_definitions)

    wsl_attribution_distros = (
        [distro.name for distro in wsl_distros] if wsl_scanned else []
    )
    # Runtime correlation consumes namespace identity from configurations.
    # Attribute the current batch now; the full pass below still handles
    # artifacts appended by the process, container, and WSL project phases.
    _best_effort_assembly(
        "attribute_wsl_configurations",
        lambda: _attribute_wsl_artifacts(
            configurations,
            [],
            [],
            inventory_distros=wsl_attribution_distros,
        ),
        fallback=[],
        completeness=completeness,
        surfaces=("mcp_host_static", "wsl_static"),
    )

    # ==========================================================================
    # PHASE 12: Runtime process discovery (opt-in)
    # ==========================================================================
    # Enumerates running processes + listening sockets, scores AI-relatedness,
    # and correlates back to the configs found above (config_hash / URL port /
    # client parent). OFF by default (detect_processes) since it polls the OS
    # process table; when on, it is best-effort and never raises into the scan.
    all_processes: list[DiscoveredProcess] = []
    processes_scanned = False
    if detect_processes:
        logger.info("Discovering runtime processes")
        scan_username = device_metadata.get("username")
        process_result: ProcessDiscoveryResult = phase_guard.run(
            "phase_12_runtime_processes",
            lambda: discover_processes(
                configurations=configurations,
                clients=clients,
                agents=all_agents,
                detect_agents=detect_agents,
                usernames=[scan_username] if scan_username else [],
                wsl_distros=wsl_distros if wsl_scanned else (),
                windows_user_sid=windows_user_sid,
                checkpoint=governor.checkpoint,
            ),
            fallback=ProcessDiscoveryResult(
                complete=False, incomplete_reasons=[RESOURCE_LIMIT_EXCEEDED_REASON]
            ),
            surfaces=("runtime",),
        )
        all_processes = process_result.processes
        processes_scanned = process_result.complete
        if not process_result.complete:
            for reason in getattr(process_result, "incomplete_reasons", []) or [
                "runtime_discovery_incomplete"
            ]:
                completeness.runtime.mark_incomplete(reason)
        # A failed in-VM process command yields no sightings for that distro
        # and nothing else: distro ``scanned`` stays whatever the Phase 0 file
        # probes established, because it gates persisting last_scanned_at /
        # container_runtimes — evidence the process phase never produces.
        configurations.extend(
            _parse_process_override_configurations(
                process_result.override_config_refs,
                configurations=configurations,
                clients=clients,
                scan_status=completeness.runtime,
                windows_user_sid=windows_user_sid,
            )
        )
        extension_roots = _resolve_process_extension_roots(
            process_result.extension_root_refs,
            scan_status=completeness.runtime,
            windows_user_sid=windows_user_sid,
        )
        all_plugins.extend(
            phase_guard.run(
                "phase_12a_process_extension_overrides",
                lambda: scan_vscode_extension_roots(
                    extension_roots,
                    checkpoint=governor.checkpoint,
                    scan_status=completeness.runtime,
                ),
                fallback=[],
                surfaces=("runtime", "plugin_host_static"),
            )
        )
    else:
        timer.record("phase_12_runtime_processes", 0)
        timer.record("phase_12a_process_extension_overrides", 0)

    # ==========================================================================
    # PHASE 13: Running-container artifact discovery (temporary opt-in)
    # ==========================================================================
    all_containers: list[DiscoveredContainer] = []
    stopped_containers: list[DiscoveredContainer] = []
    container_images: list[DiscoveredContainerImage] = []
    container_detected_clients: list[DetectedClient] = []
    containers_scanned = False
    stopped_containers_scanned = False
    container_images_scanned = False
    container_images_truncated = False
    container_artifacts_complete = False
    container_scan_error: str | None = None
    wsl_container_scanned_distros: list[str] = []
    if detect_containers:
        logger.info("Scanning running containers")
        container_result = phase_guard.run(
            "phase_13_running_containers",
            lambda: scan_running_containers(
                clients=clients,
                detect_disguised_skills=detect_disguised_skills,
            ),
            fallback=ContainerScanResult(
                failure_reason=RESOURCE_LIMIT_EXCEEDED_REASON,
                artifact_failure_reason=RESOURCE_LIMIT_EXCEEDED_REASON,
            ),
            surfaces=("container_artifacts",),
        )
        all_containers = container_result.containers
        stopped_containers = container_result.stopped_containers
        container_images = container_result.container_images
        container_detected_clients = container_result.detected_clients
        containers_scanned = container_result.scan_succeeded
        container_artifacts_complete = container_result.artifact_scan_succeeded
        if not container_artifacts_complete:
            completeness.container_artifacts.mark_incomplete(
                container_result.artifact_failure_reason
                or "container_artifact_discovery_incomplete"
            )
        if not containers_scanned:
            container_scan_error = sanitize_container_scan_error(
                container_result.failure_reason or CONTAINER_SCAN_INCOMPLETE_REASON
            )
        stopped_containers_scanned = container_result.stopped_containers_succeeded
        container_images_scanned = container_result.container_images_succeeded
        container_images_truncated = container_result.container_images_truncated
        configurations.extend(container_result.configurations)
        all_skills.extend(container_result.skills)
        all_plugins.extend(container_result.plugins)
        all_agent_definitions.extend(container_result.agent_definitions)
        if wsl_scanned:
            logger.info("Scanning running containers inside WSL")
            wsl_container_result = phase_guard.run(
                "phase_13a_wsl_containers",
                lambda: scan_wsl_containers(
                    wsl_distros,
                    max_containers=MAX_CONTAINERS - len(all_containers),
                    checkpoint=governor.checkpoint,
                ),
                fallback=WSLContainerScanResult(
                    completion=ScanCompletionStatus(
                        complete=False, reasons=[RESOURCE_LIMIT_EXCEEDED_REASON]
                    )
                ),
                surfaces=("container_artifacts",),
            )
            host_container_ids = {
                container.container_id
                for containers in (all_containers, stopped_containers)
                for container in containers
            }
            all_containers.extend(
                container
                for container in wsl_container_result.containers
                if container.container_id not in host_container_ids
            )
            wsl_container_scanned_distros = wsl_container_result.scanned_distros
            if not getattr(wsl_container_result, "complete", True):
                for reason in getattr(
                    wsl_container_result,
                    "incomplete_reasons",
                    ["wsl_container_inventory_incomplete"],
                ) or ["wsl_container_inventory_incomplete"]:
                    completeness.container_artifacts.mark_incomplete(reason)
        else:
            if device_metadata.get("os") == "windows":
                completeness.container_artifacts.mark_incomplete(
                    "wsl_inventory_incomplete"
                )
            timer.record("phase_13a_wsl_containers", 0)
    else:
        completeness.container_artifacts.mark_incomplete("container_scan_disabled")
        timer.record("phase_13_running_containers", 0)
        timer.record("phase_13a_wsl_containers", 0)

    # ==========================================================================
    # PHASE 13b: WSL project-tree artifact discovery (same opt-in)
    # ==========================================================================
    if detect_containers:
        logger.info("Scanning project artifacts across WSL homes")
        wsl_project_result = phase_guard.run(
            "phase_13b_wsl_projects",
            lambda: scan_wsl_projects(clients=clients),
            fallback=WSLProjectScanResult(
                complete=False, incomplete_reasons=[RESOURCE_LIMIT_EXCEEDED_REASON]
            ),
            surfaces=("wsl_static",),
        )
        configurations.extend(wsl_project_result.configurations)
        all_skills.extend(wsl_project_result.skills)
        all_agent_definitions.extend(wsl_project_result.agent_definitions)
        if not wsl_project_result.complete:
            for reason in wsl_project_result.incomplete_reasons or [
                "wsl_project_scan_failed"
            ]:
                completeness.wsl_static.mark_incomplete(reason)
    else:
        if device_metadata.get("os") == "windows":
            completeness.wsl_static.mark_incomplete("wsl_project_scan_disabled")
        timer.record("phase_13b_wsl_projects", 0)

    # Attribute every discovery route together: global config expansion, shared
    # home crawl/fan-out, and the optional bounded WSL project walk. Normalize
    # before dedupe so identity remains part of otherwise identical Linux paths.
    # Only the inventory this scan uploads may claim an artifact, so a withheld
    # inventory withholds WSL attribution with it.
    all_agent_definitions = _best_effort_assembly(
        "attribute_wsl_artifacts",
        lambda: _attribute_wsl_artifacts(
            configurations,
            all_skills,
            all_agent_definitions,
            inventory_distros=wsl_attribution_distros,
        ),
        fallback=all_agent_definitions,
        completeness=completeness,
        surfaces=(
            "mcp_host_static",
            "skill_host_static",
            "agent_definition_host_static",
            "wsl_static",
        ),
    )
    configurations = _best_effort_assembly(
        "dedupe_path_configurations",
        lambda: _dedupe_path_configurations(configurations),
        fallback=configurations,
        completeness=completeness,
        surfaces=("mcp_host_static",),
    )
    configurations = _best_effort_assembly(
        "dedupe_host_container_configurations",
        lambda: dedupe_host_container_configurations(configurations),
        fallback=configurations,
        completeness=completeness,
        surfaces=("mcp_host_static", "container_artifacts"),
    )
    all_skills = _best_effort_assembly(
        "strip_duplicate_skill_files",
        lambda: strip_duplicate_skill_files(all_skills),
        fallback=all_skills,
        completeness=completeness,
        surfaces=("skill_host_static",),
    )
    all_agent_definitions = _best_effort_assembly(
        "dedupe_agent_definitions",
        lambda: dedupe_agent_definitions(all_agent_definitions),
        fallback=all_agent_definitions,
        completeness=completeness,
        surfaces=("agent_definition_host_static",),
    )

    # ==========================================================================
    # PHASE 14: Installed AI-client presence
    # ==========================================================================
    # Install probes are independent of MCP configuration. Artifact signals are
    # folded in afterward so config/server/skill/plugin/extension-only clients
    # are still reported when no app bundle, binary, or registry entry is found.
    logger.info("Detecting installed AI clients")

    client_discovery_complete = True
    client_presence_status = ScanCompletionStatus()

    def _probe_clients() -> list[DetectedClient]:
        nonlocal client_discovery_complete
        try:
            profile_context: dict[str, Any] = {}
            if windows_user_sid is not None:
                profile_context = {
                    "home": Path.home(),
                    "environment": os.environ,
                    "windows_user_sid": windows_user_sid,
                    "windows_system_profile": windows_system_profile,
                    "include_current_user_registry": not windows_system_profile,
                }
            detected = detect_client_presence(
                clients,
                node_modules_paths=concurrent_result.node_modules_paths,
                hidden_space_result=concurrent_result.hidden_space_result,
                checkpoint=governor.checkpoint,
                wsl_distros=wsl_distros if wsl_scanned else (),
                scan_status=client_presence_status,
                **profile_context,
            )
            client_discovery_complete = client_presence_status.complete
            return detected
        except ScanResourceLimitExceeded:
            raise
        except Exception:
            logger.warning("Client install probes failed", exc_info=True)
            client_discovery_complete = False
            client_presence_status.mark_incomplete("client_presence_scan_failed")
            return []

    probed_clients = phase_guard.run(
        "phase_14_client_presence",
        _probe_clients,
        fallback=[],
        surfaces=("client_presence",),
    )
    if phase_guard.reason is not None:
        # The gate below reads this status, not ``completeness.client_presence``:
        # an aborted probe returned the empty fallback and, left complete, read
        # as "no client installed" and dropped presence-gated project configs.
        client_discovery_complete = False
        client_presence_status.mark_incomplete(RESOURCE_LIMIT_EXCEEDED_REASON)
    all_probed_clients = [*probed_clients, *container_detected_clients]
    configurations = _best_effort_assembly(
        "filter_presence_gated_project_configurations",
        lambda: _filter_presence_gated_project_configurations(
            configurations,
            clients=clients,
            probed_clients=all_probed_clients,
            presence_status=client_presence_status,
        ),
        fallback=configurations,
        completeness=completeness,
        surfaces=("mcp_host_static",),
    )
    detected_clients = _best_effort_assembly(
        "merge_client_presence",
        lambda: merge_client_presence(
            all_probed_clients,
            clients=clients,
            configurations=configurations,
            skills=all_skills,
            agent_definitions=all_agent_definitions,
            plugins=all_plugins,
            extension_clients=extension_clients,
        ),
        fallback=all_probed_clients,
        completeness=completeness,
        surfaces=("client_presence",),
    )
    if not client_presence_status.complete:
        for reason in client_presence_status.reasons:
            completeness.client_presence.mark_incomplete(reason)
    if len(all_agent_definitions) > MAX_AGENT_DEFINITIONS:
        completeness.agent_definition_host_static.mark_incomplete(
            "agent_definition_scan_capped"
        )
    reportable_agent_count = sum(1 for agent in all_agents if agent.is_agent)
    if reportable_agent_count > MAX_AGENTS:
        completeness.agent_host_static.mark_incomplete("agent_scan_capped")

    scan_duration_ms = int((time.monotonic() - start_time) * 1000)

    logger.info(
        "Scan complete",
        total_configs=len(configurations),
        global_configs=len([c for c in configurations if c.config_scope == "global"]),
        project_configs=len([c for c in configurations if c.config_scope == "project"]),
        plugin_configs=len([c for c in configurations if c.config_scope == "plugin"]),
        container_configs=len(
            [c for c in configurations if c.config_scope == "container"]
        ),
        wsl_configs=len([c for c in configurations if c.config_scope == "wsl"]),
        total_servers=sum(len(c.servers) for c in configurations),
        total_skills=len(all_skills),
        total_plugins=len(all_plugins),
        total_detected_clients=len(detected_clients),
        total_agents=len(all_agents),
        total_agent_definitions=len(all_agent_definitions),
        total_processes=len(all_processes),
        total_containers=len(all_containers),
        total_wsl_distros=len(wsl_distros),
        wsl_scanned=wsl_scanned,
        duration_ms=scan_duration_ms,
        phase_durations_ms=timer.durations_ms(),
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
        skill_crawl_complete=concurrent_result.skill_crawl_complete,
        project_scan_depth=effective_project_scan_depth,
        project_scan_home=reported_home,
        scan_session_id=scan_session_id,
        scan_started_at=scan_started_at,
        completeness=completeness,
        windows_user_sid=windows_user_sid,
        machine_scope=machine_scope,
        project_scan_requested=scan_projects,
        agent_discovery_complete=(
            detect_agents
            and detect_agent_frameworks
            and scan_projects
            and reportable_agent_count <= MAX_AGENTS
        ),
        client_discovery_complete=client_discovery_complete,
        process_scan_requested=detect_processes,
        processes_scanned=processes_scanned,
        detected_clients=detected_clients,
        is_wsl=device_metadata.get("is_wsl", False),
        serial_number=device_metadata.get("serial_number"),
        tools=tools,
        skills=all_skills,
        project_skill_candidate_paths=(concurrent_result.project_skill_candidate_paths),
        global_skill_candidate_paths=concurrent_result.global_skill_candidate_paths,
        plugins=all_plugins,
        agents=all_agents,
        agent_definitions=all_agent_definitions,
        processes=all_processes,
        container_scan_requested=detect_containers,
        container_scan_error=container_scan_error,
        containers=all_containers,
        containers_scanned=containers_scanned,
        stopped_containers=stopped_containers,
        stopped_containers_scanned=stopped_containers_scanned,
        container_images=container_images,
        container_images_scanned=container_images_scanned,
        container_images_truncated=container_images_truncated,
        wsl_distros=wsl_distros,
        wsl_scanned=wsl_scanned,
        wsl_container_scanned_distros=wsl_container_scanned_distros,
        phase_durations_ms=timer.durations_ms(),
        resource_limit_exceeded=(
            concurrent_result.resource_limit_exceeded or phase_guard.reason
        ),
    )


def device_context_dict(scan_result: ScanResult) -> DeviceContext:
    """Build the device-identity block shared by scan + check-in payloads."""
    context = DeviceContext(
        device_id=scan_result.device_id,
        hostname=scan_result.hostname,
        os=scan_result.os,
        os_version=scan_result.os_version,
        username=scan_result.username,
        org_device_id=scan_result.org_device_id,
        serial_number=scan_result.serial_number,
    )
    windows_user_sid = getattr(scan_result, "windows_user_sid", None)
    if windows_user_sid is not None:
        context["windows_user_sid"] = windows_user_sid
    return context


def _host_skill_candidate_paths(paths: list[str]) -> list[str]:
    """Exclude WSL candidates until namespace-specific removal state exists."""
    return [path for path in paths if parse_wsl_unc_path(path) is None]


def _build_current_skill_presence(scan_result: ScanResult) -> SkillPresenceState:
    return build_presence_state(
        SkillPresenceParams(
            project_depth=scan_result.project_scan_depth,
            home=scan_result.project_scan_home,
        ),
        project_paths=_host_skill_candidate_paths(
            scan_result.project_skill_candidate_paths
        ),
        global_paths=_host_skill_candidate_paths(
            scan_result.global_skill_candidate_paths
        ),
    )


def reconcile_skill_presence(
    client: RunlayerClient,
    scan_result: ScanResult,
    *,
    state_path: Path | None = None,
) -> Literal["success", "failed"]:
    """Reconcile complete host presence state after skill submission succeeds."""
    if not scan_result.skill_crawl_complete:
        return "success"

    current = _build_current_skill_presence(scan_result)
    previous = load_presence_state(state_path)
    removals = compute_removals(
        previous,
        current,
        crawl_complete=scan_result.skill_crawl_complete,
    )
    # compute_removals is empty for a first run, changed scan inputs, or an
    # incomplete crawl (already excluded above) as well as for "nothing gone";
    # every one of those just advances the baseline.
    if not removals:
        save_presence_state(current, state_path)
        return "success"

    try:
        response = client.submit_skill_removals(
            removals,
            device_context_dict(scan_result),
        )
        if not isinstance(response, dict):
            raise ValueError("invalid skill removal response")
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 403):
            raise
        logger.warning(
            "skill_removal_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            status_code=exc.response.status_code,
            removal_count=len(removals),
        )
        return "failed"
    except Exception as exc:
        logger.warning(
            "skill_removal_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            removal_count=len(removals),
        )
        return "failed"

    if response.get("unsupported") is True:
        return "success"
    save_presence_state(current, state_path)
    return "success"


@dataclass
class ServerSubmission:
    """Outcome of submitting the MCP server scan payload.

    Mirrors the SubmissionStatus skills/plugins return, but also carries the
    backend ``response`` so the orchestrator can surface it in the completion
    summary on success.
    """

    status: SubmissionStatus
    response: dict[str, Any] | None = None


def submit_discovered_servers(
    client: RunlayerClient,
    scan_result: ScanResult,
) -> ServerSubmission:
    """Submit the MCP server scan payload, owning the server error taxonomy.

    Mirrors submit_discovered_skills/plugins by translating transport errors,
    backend 5xx, and the "unsupported" (404) response into a status instead of
    leaking httpx exceptions to its caller. Auth failures (401/403) are the one
    exception: retrying the scan cannot fix them, so they re-raise for the
    command to surface as the generic error (exit 1).

    Returns the backend response alongside the status on success so the
    orchestrator can render the completion summary.
    """
    try:
        response = client.submit_mcp_watch_scan(scan_result.to_api_payload())
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 403):
            raise
        # A 422 means the backend rejected the batch payload. Capture the
        # sanitized detail (backend already strips input/ctx/url) + how many
        # servers were in the batch so the failing loc/type is diagnosable.
        validation_detail = None
        if exc.response.status_code == 422:
            try:
                validation_detail = exc.response.json().get("detail")
            except ValueError:
                validation_detail = exc.response.text[:500]
        logger.warning(
            "mcp_watch_scan_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            status_code=exc.response.status_code,
            server_count=scan_result.total_servers,
            validation_detail=validation_detail,
        )
        return ServerSubmission(status="failed")
    except httpx.RequestError as exc:
        logger.warning(
            "mcp_watch_scan_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        return ServerSubmission(status="failed")
    except Exception:
        logger.warning("mcp_watch_scan_submission_failed", exc_info=True)
        return ServerSubmission(status="failed")
    if response.get("unsupported"):
        return ServerSubmission(status="unsupported")
    return ServerSubmission(status="success", response=response)


def _artifact_cache_contains(
    artifact_cache: ArtifactCache | None,
    identifier: str,
) -> bool:
    if artifact_cache is None:
        return False
    try:
        return artifact_cache.contains(identifier)
    except Exception:
        logger.warning(
            "artifact_cache_operation_failed",
            operation="contains",
            identifier=identifier,
            exc_info=True,
        )
        return False


def _artifact_cache_record(
    artifact_cache: ArtifactCache | None,
    identifier: str,
) -> None:
    if artifact_cache is None:
        return
    try:
        artifact_cache.record(identifier)
    except Exception:
        logger.warning(
            "artifact_cache_operation_failed",
            operation="record",
            identifier=identifier,
            exc_info=True,
        )


def _artifact_cache_evict(
    artifact_cache: ArtifactCache | None,
    identifier: str,
) -> None:
    if artifact_cache is None:
        return
    try:
        artifact_cache.evict(identifier)
    except Exception:
        logger.warning(
            "artifact_cache_operation_failed",
            operation="evict",
            identifier=identifier,
            exc_info=True,
        )


def _lookup_fingerprints_in_batches(
    lookup_batch: Callable[[list[str]], dict[str, Any]],
    identifiers: list[str],
) -> dict[str, dict[str, bool]] | None:
    """Return batch results, or None when the endpoint is unavailable."""
    results: dict[str, dict[str, bool]] = {}
    for start in range(0, len(identifiers), ARTIFACT_LOOKUP_BATCH_SIZE):
        chunk = identifiers[start : start + ARTIFACT_LOOKUP_BATCH_SIZE]
        response = lookup_batch(chunk)
        if not isinstance(response, dict):
            logger.warning(
                "artifact_lookup_batch_response_malformed",
                reason="response_not_object",
            )
            return None
        if response.get("unsupported"):
            return None
        raw_results = response.get("results")
        if not isinstance(raw_results, list):
            logger.warning(
                "artifact_lookup_batch_response_malformed",
                reason="results_not_list",
            )
            return None
        expected = set(chunk)
        for item in raw_results:
            if not isinstance(item, dict):
                continue
            identifier = item.get("identifier")
            if not isinstance(identifier, str) or identifier not in expected:
                continue
            known = item.get("known") is True
            results[identifier] = {
                "known": known,
                "has_content": known and item.get("has_content") is True,
            }
        for identifier in chunk:
            results.setdefault(
                identifier,
                {"known": False, "has_content": False},
            )
    return results


class _DiscoveredArtifact(Protocol):
    name: str
    identifier: str | None
    oversized: bool

    def to_api_payload(self) -> dict[str, Any]: ...


_ArtifactT = TypeVar("_ArtifactT", bound=_DiscoveredArtifact)
_ArtifactKind = Literal["skill", "plugin"]


def _artifact_manifest_surface(
    artifact: _DiscoveredArtifact,
    *,
    kind: _ArtifactKind,
) -> ScanManifestSurface:
    surface: ScanManifestSurface = "host_static"
    if getattr(artifact, "container_id", None) is not None:
        surface = "container"
    elif getattr(artifact, "scope", None) == "process_override":
        surface = "host_runtime"
    elif getattr(artifact, "wsl_distro", None) is not None:
        surface = "wsl"
    elif getattr(artifact, "device_scope", False):
        surface = "device"
    # A failure must land on a surface the manifest emits for this category,
    # or it never revokes authority. WSL plugins submit on host surfaces.
    if surface not in CATEGORY_SURFACES[kind]:
        surface = "host_static"
    return surface


@dataclass(frozen=True)
class _ArtifactSubmissionConfig(Generic[_ArtifactT]):
    kind: _ArtifactKind
    lookup_batch: Callable[[list[str]], dict[str, Any]]
    lookup_one: Callable[[_ArtifactT, str], dict[str, Any]]
    submit: Callable[[dict[str, Any]], dict[str, Any]]
    strip_duplicate_identifiers: bool = False


def _submit_discovered_artifacts(
    artifacts: list[_ArtifactT],
    *,
    device_ctx: Mapping[str, Any],
    artifact_cache: ArtifactCache | None,
    config: _ArtifactSubmissionConfig[_ArtifactT],
    failed_surfaces: set[ScanManifestSurface] | None = None,
) -> SubmissionStatus:
    """Resolve and submit one artifact kind with cache-backed content stripping."""
    cache_hits: set[str] = set()
    miss_identifiers: list[str] = []
    seen_misses: set[str] = set()
    for artifact in artifacts:
        identifier = artifact.identifier
        if identifier is None:
            continue
        if _artifact_cache_contains(artifact_cache, identifier):
            cache_hits.add(identifier)
        elif identifier not in seen_misses:
            seen_misses.add(identifier)
            miss_identifiers.append(identifier)

    batch_lookups: dict[str, dict[str, bool]] | None = None
    if miss_identifiers:
        try:
            batch_lookups = _lookup_fingerprints_in_batches(
                config.lookup_batch,
                miss_identifiers,
            )
        except NotImplementedError:
            pass
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                raise
            logger.warning(
                f"{config.kind}_lookup_batch_failed",
                error=str(exc),
                error_type=type(exc).__name__,
                status_code=exc.response.status_code,
                artifact_count=len(miss_identifiers),
            )
        except httpx.RequestError as exc:
            logger.warning(
                f"{config.kind}_lookup_batch_failed",
                error=str(exc),
                error_type=type(exc).__name__,
                artifact_count=len(miss_identifiers),
            )
        except Exception as exc:
            logger.warning(
                f"{config.kind}_lookup_batch_failed",
                error=str(exc),
                error_type=type(exc).__name__,
                artifact_count=len(miss_identifiers),
            )

    any_failed = False

    def unsupported_status() -> SubmissionStatus:
        return "failed" if any_failed else "unsupported"

    seen_identifiers: set[str] = set()
    for artifact in artifacts:
        identifier = artifact.identifier
        if identifier is None:
            continue
        duplicate_identifier = (
            config.strip_duplicate_identifiers and identifier in seen_identifiers
        )
        seen_identifiers.add(identifier)
        artifact_log_context = {config.kind: artifact.name}
        try:
            if identifier in cache_hits:
                result = {"known": True, "has_content": True}
            elif batch_lookups is not None:
                result = batch_lookups[identifier]
            else:
                result = config.lookup_one(artifact, identifier)
            if result.get("unsupported"):
                return unsupported_status()

            full_payload = artifact.to_api_payload()
            full_payload.update(dict(device_ctx))
            strip_known_content = result.get("known") and result.get(
                "has_content", True
            )
            should_strip = (
                strip_known_content or artifact.oversized or duplicate_identifier
            )
            payload = dict(full_payload)
            if should_strip:
                payload["files"] = []
            submit_response = config.submit(payload)
            if submit_response.get("unsupported") is True:
                return unsupported_status()

            cache_backed_content_strip = (
                artifact_cache is not None
                and bool(full_payload.get("files"))
                and result.get("known") is True
                and result.get("has_content") is True
                and not artifact.oversized
                and not duplicate_identifier
            )
            if (
                cache_backed_content_strip
                and submit_response.get("has_content") is not True
            ):
                logger.warning(
                    "artifact_cache_content_missing",
                    artifact_type=config.kind,
                    identifier=identifier,
                )
                _artifact_cache_evict(artifact_cache, identifier)
                submit_response = config.submit(full_payload)
                if submit_response.get("unsupported") is True:
                    return unsupported_status()
            if submit_response.get("has_content") is True:
                _artifact_cache_record(artifact_cache, identifier)
        except NotImplementedError:
            logger.debug(
                f"{config.kind}_submission_not_implemented",
                **artifact_log_context,
            )
            return unsupported_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                raise
            logger.warning(
                f"{config.kind}_submission_failed",
                **artifact_log_context,
                error=str(exc),
                error_type=type(exc).__name__,
                status_code=exc.response.status_code,
            )
            any_failed = True
            if failed_surfaces is not None:
                failed_surfaces.add(
                    _artifact_manifest_surface(artifact, kind=config.kind)
                )
        except httpx.RequestError as exc:
            logger.warning(
                f"{config.kind}_submission_failed",
                **artifact_log_context,
                error=str(exc),
                error_type=type(exc).__name__,
            )
            if failed_surfaces is None:
                return "failed"
            any_failed = True
            failed_surfaces.add(_artifact_manifest_surface(artifact, kind=config.kind))
        except Exception as exc:
            logger.warning(
                f"{config.kind}_submission_failed",
                **artifact_log_context,
                error=str(exc),
                error_type=type(exc).__name__,
            )
            any_failed = True
            if failed_surfaces is not None:
                failed_surfaces.add(
                    _artifact_manifest_surface(artifact, kind=config.kind)
                )
    return "failed" if any_failed and failed_surfaces is None else "success"


def submit_discovered_skills(
    client: RunlayerClient,
    skills: list[DiscoveredSkillArtifact],
    scan_result: ScanResult | None = None,
    artifact_cache: ArtifactCache | None = None,
    failed_surfaces: set[ScanManifestSurface] | None = None,
) -> SubmissionStatus:
    """Resolve skill fingerprints in batches, then always submit each skill.

    Cache hits skip lookup and strip content. The submit response is the
    server-side backstop: if it cannot confirm stored content, evict the hint
    and immediately resubmit the full payload.

    Returns whether submission succeeded, failed, or is unsupported.
    """
    device_ctx: dict[str, Any] = (
        {**device_context_dict(scan_result)} if scan_result else {}
    )
    if scan_result is not None:
        device_ctx["scan_session_id"] = str(scan_result.scan_session_id)
        device_ctx["scan_started_at"] = scan_result.scan_started_at.astimezone(
            datetime.timezone.utc
        ).isoformat()
    ordered_skills = [
        skill
        for skill in sorted(skills, key=lambda skill: not skill.files)
        if skill.identifier
    ]

    def lookup_skill(
        skill: DiscoveredSkillArtifact,
        identifier: str,
    ) -> dict[str, Any]:
        return client.submit_skill_fingerprint(
            identifier,
            skill.artifact_type,
            oversized=skill.oversized,
        )

    config: _ArtifactSubmissionConfig[DiscoveredSkillArtifact] = (
        _ArtifactSubmissionConfig(
            kind="skill",
            lookup_batch=client.submit_skill_fingerprints,
            lookup_one=lookup_skill,
            submit=client.submit_skill,
            strip_duplicate_identifiers=True,
        )
    )
    return _submit_discovered_artifacts(
        ordered_skills,
        device_ctx=device_ctx,
        artifact_cache=artifact_cache,
        config=config,
        failed_surfaces=failed_surfaces,
    )


def submit_discovered_plugins(
    client: RunlayerClient,
    plugins: list[DiscoveredPluginArtifact],
    scan_result: ScanResult | None = None,
    artifact_cache: ArtifactCache | None = None,
    failed_surfaces: set[ScanManifestSurface] | None = None,
) -> SubmissionStatus:
    """Resolve plugin fingerprints in batches, then always submit each plugin.

    Cache hits skip lookup and strip content. The submit response is the
    server-side backstop: if it cannot confirm stored content, evict the hint
    and immediately resubmit the full payload.

    Returns whether submission succeeded, failed, or is unsupported.
    """
    device_ctx: dict[str, Any] = (
        {**device_context_dict(scan_result)} if scan_result else {}
    )
    if scan_result is not None:
        device_ctx["scan_session_id"] = str(scan_result.scan_session_id)
        device_ctx["scan_started_at"] = scan_result.scan_started_at.astimezone(
            datetime.timezone.utc
        ).isoformat()
    identified_plugins = [plugin for plugin in plugins if plugin.identifier]

    def lookup_plugin(
        _plugin: DiscoveredPluginArtifact,
        identifier: str,
    ) -> dict[str, Any]:
        return client.submit_plugin_fingerprint(identifier)

    config: _ArtifactSubmissionConfig[DiscoveredPluginArtifact] = (
        _ArtifactSubmissionConfig(
            kind="plugin",
            lookup_batch=client.submit_plugin_fingerprints,
            lookup_one=lookup_plugin,
            submit=client.submit_plugin,
        )
    )
    return _submit_discovered_artifacts(
        identified_plugins,
        device_ctx=device_ctx,
        artifact_cache=artifact_cache,
        config=config,
        failed_surfaces=failed_surfaces,
    )


def submit_discovered_agents(
    client: RunlayerClient,
    scan_result: ScanResult,
) -> SubmissionStatus:
    """Submit discovered agents as one batch, owning the agent error taxonomy.

    Mirrors submit_discovered_servers: a single batch POST whose transport
    errors, backend 5xx, and "unsupported" (404) response are translated into a
    status instead of leaking httpx exceptions. Auth failures (401/403) re-raise
    so the command surfaces them as the generic error (exit 1). No-op success
    when there are no real agents to submit (backend also no-ops on empty).
    """
    payload = scan_result.to_agent_report_payload()
    agent_count = len(payload["agents"])
    if not agent_count:
        return "success"
    try:
        response = client.submit_agents(payload)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 403):
            raise
        logger.warning(
            "agent_report_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            status_code=exc.response.status_code,
            agent_count=agent_count,
        )
        return "failed"
    except httpx.RequestError as exc:
        logger.warning(
            "agent_report_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        return "failed"
    except Exception:
        logger.warning("agent_report_submission_failed", exc_info=True)
        return "failed"
    if response.get("unsupported"):
        return "unsupported"
    return "success"


def submit_discovered_agent_definitions(
    client: RunlayerClient,
    scan_result: ScanResult,
) -> SubmissionStatus:
    """Submit client-native agent definitions as one bounded batch."""
    payload = scan_result.to_agent_definition_report_payload()
    definition_count = len(payload["agent_definitions"])
    if not definition_count:
        return "success"
    try:
        response = client.submit_agent_definitions(payload)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 403):
            raise
        logger.warning(
            "agent_definition_report_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            status_code=exc.response.status_code,
            definition_count=definition_count,
        )
        return "failed"
    except httpx.RequestError as exc:
        logger.warning(
            "agent_definition_report_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            definition_count=definition_count,
        )
        return "failed"
    except Exception:
        logger.warning(
            "agent_definition_report_submission_failed",
            definition_count=definition_count,
            exc_info=True,
        )
        return "failed"
    if response.get("unsupported"):
        return "unsupported"
    return "success"


def _manifest_entry(
    submission: ScanSubmissionResult,
    *,
    category: ScanManifestCategory,
    surface: ScanManifestSurface,
    authoritative: bool,
    incomplete_reason: str,
) -> dict[str, Any]:
    outcome = submission.surface_outcomes[(category, surface)]
    submission_reason = submission.incomplete_surfaces.get((category, surface))
    complete = authoritative and outcome == "success" and submission_reason is None
    entry: dict[str, Any] = {
        "category": category,
        "surface": surface,
        "complete": complete,
    }
    if not complete:
        entry["reason"] = (
            "submission_failed"
            if outcome == "failed"
            else "unsupported"
            if outcome == "unsupported"
            else submission_reason or incomplete_reason
        )
    return entry


def _runtime_scan_is_authoritative(scan_result: ScanResult) -> bool:
    return (
        scan_result.process_scan_requested
        and scan_result.processes_scanned
        and scan_result.completeness.runtime.complete
    )


def _scan_manifest_payload(
    scan_result: ScanResult,
    submission: ScanSubmissionResult,
) -> dict[str, Any]:
    completeness = scan_result.completeness
    mcp_static_complete = (
        scan_result.project_scan_requested and completeness.mcp_host_static.complete
    )
    skill_static_complete = (
        scan_result.project_scan_requested and completeness.skill_host_static.complete
    )
    plugin_static_complete = (
        scan_result.project_scan_requested and completeness.plugin_host_static.complete
    )
    windows_host = (scan_result.os or "").casefold() == "windows"
    # WSL plugins submit on host surfaces. Their authority follows the plugin
    # category status, not the broader WSL status that includes project walks.
    windows_plugin_host_complete = not windows_host or (
        scan_result.wsl_scanned and completeness.plugin_host_static.complete
    )
    plugin_static_complete = plugin_static_complete and windows_plugin_host_complete
    container_complete = (
        scan_result.container_scan_requested
        and scan_result.containers_scanned
        and completeness.container_artifacts.complete
    )
    runtime_complete = _runtime_scan_is_authoritative(scan_result)
    wsl_static_complete = (
        scan_result.wsl_scanned
        and scan_result.project_scan_requested
        and completeness.wsl_static.complete
    )
    windows_client_host_complete = not windows_host or (
        scan_result.wsl_scanned
        and (not scan_result.container_scan_requested or wsl_static_complete)
    )
    wsl_runtime_complete = scan_result.wsl_scanned and runtime_complete
    agent_payload_complete = (
        sum(1 for agent in scan_result.agents if agent.is_agent) <= MAX_AGENTS
    )
    definition_payload_complete = (
        len(scan_result.agent_definitions) <= MAX_AGENT_DEFINITIONS
    )
    agent_static_complete = (
        scan_result.project_scan_requested
        and scan_result.agent_discovery_complete
        and completeness.agent_host_static.complete
        and agent_payload_complete
    )
    definition_host_complete = (
        scan_result.project_scan_requested
        and completeness.agent_definition_host_static.complete
        and definition_payload_complete
    )
    client_static_complete = (
        mcp_static_complete
        and skill_static_complete
        and plugin_static_complete
        and definition_host_complete
        and completeness.client_presence.complete
        and scan_result.client_discovery_complete
        and windows_client_host_complete
    )
    client_wsl_complete = (
        wsl_static_complete
        and completeness.client_presence.complete
        and scan_result.client_discovery_complete
    )

    def incomplete_reason(
        status: ScanCompletionStatus,
        fallback: str,
    ) -> str:
        return status.reason(fallback)

    client_static_incomplete_reason = "client_static_discovery_incomplete"
    client_static_statuses = [
        completeness.mcp_host_static,
        completeness.skill_host_static,
        completeness.plugin_host_static,
        completeness.agent_definition_host_static,
        completeness.client_presence,
    ]
    if windows_host and scan_result.container_scan_requested:
        client_static_statuses.append(completeness.wsl_static)
    for client_status in client_static_statuses:
        if not client_status.complete:
            client_static_incomplete_reason = client_status.reason(
                client_static_incomplete_reason
            )
            break
    if windows_host and not scan_result.wsl_scanned:
        client_static_incomplete_reason = "wsl_inventory_incomplete"

    if not completeness.client_presence.complete:
        client_wsl_incomplete_reason = completeness.client_presence.reason(
            "client_discovery_incomplete"
        )
    elif not scan_result.client_discovery_complete:
        client_wsl_incomplete_reason = "client_discovery_incomplete"
    elif not scan_result.wsl_scanned:
        client_wsl_incomplete_reason = "wsl_inventory_incomplete"
    else:
        client_wsl_incomplete_reason = completeness.wsl_static.reason(
            "wsl_discovery_incomplete"
        )

    plugin_static_incomplete_reason = "static_discovery_incomplete"
    if not completeness.plugin_host_static.complete:
        plugin_static_incomplete_reason = incomplete_reason(
            completeness.plugin_host_static,
            plugin_static_incomplete_reason,
        )
    elif windows_host and not windows_plugin_host_complete:
        plugin_static_incomplete_reason = incomplete_reason(
            completeness.plugin_host_static,
            "wsl_discovery_incomplete",
        )

    plugin_runtime_incomplete_reason = "runtime_discovery_incomplete"
    if not completeness.runtime.complete:
        plugin_runtime_incomplete_reason = incomplete_reason(
            completeness.runtime,
            plugin_runtime_incomplete_reason,
        )
    elif windows_host and not windows_plugin_host_complete:
        plugin_runtime_incomplete_reason = incomplete_reason(
            completeness.plugin_host_static,
            "wsl_discovery_incomplete",
        )

    agent_wsl_incomplete_reason = "wsl_discovery_incomplete"
    if not agent_payload_complete:
        agent_wsl_incomplete_reason = "agent_payload_truncated"
    elif not agent_static_complete:
        agent_wsl_incomplete_reason = incomplete_reason(
            completeness.agent_host_static,
            "agent_discovery_incomplete",
        )
    else:
        agent_wsl_incomplete_reason = incomplete_reason(
            completeness.wsl_static,
            "wsl_discovery_incomplete",
        )

    agent_wsl_runtime_incomplete_reason = "wsl_runtime_discovery_incomplete"
    if not agent_payload_complete:
        agent_wsl_runtime_incomplete_reason = "agent_payload_truncated"
    elif not runtime_complete:
        agent_wsl_runtime_incomplete_reason = incomplete_reason(
            completeness.runtime,
            "runtime_discovery_incomplete",
        )

    def manifest_entry_state(
        category: ScanManifestCategory,
        surface: ScanManifestSurface,
    ) -> tuple[bool, str]:
        match category, surface:
            case "mcp", "host_static":
                return (
                    mcp_static_complete,
                    incomplete_reason(
                        completeness.mcp_host_static,
                        "static_discovery_incomplete",
                    ),
                )
            case "mcp", "host_runtime":
                return (
                    runtime_complete,
                    incomplete_reason(
                        completeness.runtime,
                        "runtime_discovery_incomplete",
                    ),
                )
            case "mcp", "container":
                return (
                    container_complete,
                    incomplete_reason(
                        completeness.container_artifacts,
                        "container_discovery_incomplete",
                    ),
                )
            case "mcp", "wsl":
                return (
                    wsl_static_complete,
                    incomplete_reason(
                        completeness.wsl_static,
                        "wsl_discovery_incomplete",
                    ),
                )
            case "mcp", "wsl_runtime":
                return wsl_runtime_complete, "wsl_runtime_discovery_incomplete"
            case "client", "host_static":
                return client_static_complete, client_static_incomplete_reason
            case "client", "host_runtime":
                return (
                    runtime_complete,
                    incomplete_reason(
                        completeness.runtime,
                        "runtime_discovery_incomplete",
                    ),
                )
            case "client", "container":
                return (
                    container_complete,
                    incomplete_reason(
                        completeness.container_artifacts,
                        "container_discovery_incomplete",
                    ),
                )
            case "client", "wsl":
                return client_wsl_complete, client_wsl_incomplete_reason
            case "client", "wsl_runtime":
                return wsl_runtime_complete, "wsl_runtime_discovery_incomplete"
            case "skill", "host_static":
                return (
                    skill_static_complete,
                    incomplete_reason(
                        completeness.skill_host_static,
                        "static_discovery_incomplete",
                    ),
                )
            case "skill", "container":
                return (
                    container_complete,
                    incomplete_reason(
                        completeness.container_artifacts,
                        "container_discovery_incomplete",
                    ),
                )
            case "skill", "wsl":
                return (
                    wsl_static_complete,
                    incomplete_reason(
                        completeness.wsl_static,
                        "wsl_discovery_incomplete",
                    ),
                )
            case "plugin", "host_static":
                return plugin_static_complete, plugin_static_incomplete_reason
            case "plugin", "host_runtime":
                return (
                    runtime_complete and windows_plugin_host_complete,
                    plugin_runtime_incomplete_reason,
                )
            case "plugin", "container":
                return (
                    container_complete,
                    incomplete_reason(
                        completeness.container_artifacts,
                        "container_discovery_incomplete",
                    ),
                )
            case "plugin", "device":
                return (
                    scan_result.machine_scope and completeness.plugin_device.complete,
                    (
                        incomplete_reason(
                            completeness.plugin_device,
                            "machine_plugin_discovery_incomplete",
                        )
                        if scan_result.machine_scope
                        else "machine_scope_disabled"
                    ),
                )
            case "agent", "host_static":
                return (
                    agent_static_complete,
                    (
                        "agent_payload_truncated"
                        if not agent_payload_complete
                        else incomplete_reason(
                            completeness.agent_host_static,
                            "agent_discovery_incomplete",
                        )
                    ),
                )
            case "agent", "host_runtime":
                return (
                    runtime_complete and agent_payload_complete,
                    (
                        "agent_payload_truncated"
                        if not agent_payload_complete
                        else incomplete_reason(
                            completeness.runtime,
                            "runtime_discovery_incomplete",
                        )
                    ),
                )
            case "agent", "wsl":
                return (
                    wsl_static_complete
                    and agent_static_complete
                    and agent_payload_complete,
                    agent_wsl_incomplete_reason,
                )
            case "agent", "wsl_runtime":
                return (
                    wsl_runtime_complete and agent_payload_complete,
                    agent_wsl_runtime_incomplete_reason,
                )
            case "agent_definition", "host_static":
                return (
                    definition_host_complete,
                    (
                        "agent_definition_payload_truncated"
                        if not definition_payload_complete
                        else incomplete_reason(
                            completeness.agent_definition_host_static,
                            "definition_discovery_incomplete",
                        )
                    ),
                )
            case "agent_definition", "container":
                return (
                    container_complete and definition_payload_complete,
                    (
                        "agent_definition_payload_truncated"
                        if not definition_payload_complete
                        else incomplete_reason(
                            completeness.container_artifacts,
                            "container_discovery_incomplete",
                        )
                    ),
                )
            case "agent_definition", "wsl":
                return (
                    wsl_static_complete and definition_payload_complete,
                    (
                        "agent_definition_payload_truncated"
                        if not definition_payload_complete
                        else incomplete_reason(
                            completeness.wsl_static,
                            "wsl_discovery_incomplete",
                        )
                    ),
                )
            case _:
                raise AssertionError(
                    f"Unhandled scan manifest surface: {category}/{surface}"
                )

    entries: list[dict[str, Any]] = []
    for category, surfaces in CATEGORY_SURFACES.items():
        for surface in surfaces:
            authoritative, reason = manifest_entry_state(category, surface)
            entries.append(
                _manifest_entry(
                    submission,
                    category=category,
                    surface=surface,
                    authoritative=authoritative,
                    incomplete_reason=reason,
                )
            )
    return {
        **device_context_dict(scan_result),
        "scan_session_id": str(scan_result.scan_session_id),
        "scan_started_at": scan_result.scan_started_at.astimezone(
            datetime.timezone.utc
        ).isoformat(),
        "entries": entries,
    }


def _record_category_outcome(
    submission: ScanSubmissionResult,
    *,
    category: ScanManifestCategory,
    outcome: SubmissionStatus,
    unsupported_label: str,
    failed_label: str,
) -> None:
    submission.category_outcomes[category] = outcome
    if outcome == "unsupported":
        if unsupported_label not in submission.unsupported:
            submission.unsupported.append(unsupported_label)
    elif outcome == "failed":
        if failed_label not in submission.failed_submissions:
            submission.failed_submissions.append(failed_label)


def _record_surface_outcomes(
    submission: ScanSubmissionResult,
    *,
    category: ScanManifestCategory,
    outcome: SubmissionStatus,
    surface_group: Literal["all", "at_rest", "runtime"] = "all",
) -> None:
    for surface in CATEGORY_SURFACES[category]:
        is_runtime = surface.endswith("_runtime")
        if surface_group == "at_rest" and is_runtime:
            continue
        if surface_group == "runtime" and not is_runtime:
            continue
        submission.surface_outcomes[(category, surface)] = outcome


def _record_artifact_submission_outcome(
    submission: ScanSubmissionResult,
    *,
    category: Literal["skill", "plugin"],
    outcome: SubmissionStatus,
    failed_surfaces: set[ScanManifestSurface],
    unsupported_label: str,
    failed_label: str,
) -> None:
    effective_outcome: SubmissionStatus = (
        "failed" if failed_surfaces and outcome == "unsupported" else outcome
    )
    _record_surface_outcomes(
        submission,
        category=category,
        outcome=effective_outcome,
    )
    if failed_surfaces:
        if failed_label not in submission.failed_submissions:
            submission.failed_submissions.append(failed_label)
        for surface in failed_surfaces:
            submission.surface_outcomes[(category, surface)] = "failed"
            submission.incomplete_surfaces[(category, surface)] = "submission_failed"
    if effective_outcome != "success":
        _record_category_outcome(
            submission,
            category=category,
            outcome=effective_outcome,
            unsupported_label=unsupported_label,
            failed_label=failed_label,
        )


def _consume_backend_surface_failures(
    submission: ScanSubmissionResult,
    response: dict[str, Any] | None,
) -> None:
    if response is None:
        return
    raw_failures = response.get("incomplete_surfaces", [])
    if not isinstance(raw_failures, list):
        logger.warning("mcp_watch_scan_invalid_incomplete_surfaces")
        return

    failed_labels = {
        "mcp": "servers",
        "client": "clients",
        "skill": "skills",
        "plugin": "plugins",
        "agent": "agents",
        "agent_definition": "agent definitions",
    }
    for raw_failure in raw_failures[:30]:
        if not isinstance(raw_failure, dict):
            continue
        category = raw_failure.get("category")
        surface = raw_failure.get("surface")
        reason = raw_failure.get("reason")
        if (
            not isinstance(category, str)
            or category not in CATEGORY_SURFACES
            or not isinstance(surface, str)
            or not isinstance(reason, str)
            or not reason
        ):
            continue
        typed_category = cast(ScanManifestCategory, category)
        if surface not in CATEGORY_SURFACES[typed_category]:
            continue
        typed_surface = cast(ScanManifestSurface, surface)
        submission.incomplete_surfaces[(typed_category, typed_surface)] = reason[:200]
        failed_label = failed_labels[typed_category]
        if failed_label not in submission.failed_submissions:
            submission.failed_submissions.append(failed_label)


def submit_scan_results(
    client: RunlayerClient,
    scan_result: ScanResult,
    artifact_cache: ArtifactCache | None = None,
) -> ScanSubmissionResult:
    """Submit every artifact category independently.

    One failing category does not prevent the others from being submitted. The
    returned ScanSubmissionResult records the server response plus which
    categories were unsupported / failed; callers read ``.exit_code`` for the
    process exit policy and the recorded fields for user-facing output.

    Auth failures (401/403) propagate as ``httpx.HTTPStatusError`` — they can't
    be fixed by retrying the scan, so the caller surfaces them as the generic
    error rather than a submit-failed exit.
    """
    submission = ScanSubmissionResult()

    for skill in scan_result.skills:
        if skill.identifier is not None:
            continue
        surface: ScanManifestSurface = (
            "container"
            if skill.container_id is not None
            else "wsl"
            if skill.wsl_distro is not None
            else "host_static"
        )
        submission.incomplete_surfaces[("skill", surface)] = "skill_identifier_missing"
    for plugin in scan_result.plugins:
        if plugin.identifier is not None:
            continue
        surface = _artifact_manifest_surface(plugin, kind="plugin")
        submission.incomplete_surfaces[("plugin", surface)] = (
            "plugin_identifier_missing"
        )

    # Submit at-rest agents before process sightings so first-scan runtime
    # correlation can find the catalog + installation rows it should mark live.
    # Categories remain independent: a failed/unsupported agent submit does not
    # block the MCP/process payload below.
    if scan_result.agents:
        agent_submission = submit_discovered_agents(client, scan_result)
        _record_category_outcome(
            submission,
            category="agent",
            outcome=agent_submission,
            unsupported_label="Shadow Agent Detection",
            failed_label="agents",
        )
        _record_surface_outcomes(
            submission,
            category="agent",
            outcome=agent_submission,
            surface_group="at_rest",
        )

    if scan_result.agent_definitions:
        definition_submission = submit_discovered_agent_definitions(client, scan_result)
        _record_category_outcome(
            submission,
            category="agent_definition",
            outcome=definition_submission,
            unsupported_label="Agent Definition Detection",
            failed_label="agent definitions",
        )
        _record_surface_outcomes(
            submission,
            category="agent_definition",
            outcome=definition_submission,
        )

    # Plugin-backed MCP configurations and skills resolve installation links
    # during their own ingest, so plugin rows must exist first on a new device.
    if scan_result.plugins:
        failed_plugin_surfaces: set[ScanManifestSurface] = set()
        plugin_submission = submit_discovered_plugins(
            client,
            scan_result.plugins,
            scan_result,
            artifact_cache=artifact_cache,
            failed_surfaces=failed_plugin_surfaces,
        )
        _record_artifact_submission_outcome(
            submission,
            category="plugin",
            outcome=plugin_submission,
            failed_surfaces=failed_plugin_surfaces,
            unsupported_label="Shadow Plugin Detection",
            failed_label="plugins",
        )

    # Client presence and runtime/inventory sightings ride the MCP-scan payload,
    # so successful empty process/WSL inventories and requested container
    # failures still require a POST.
    if (
        scan_result.total_servers > 0
        or scan_result.detected_clients
        or scan_result.processes
        or _runtime_scan_is_authoritative(scan_result)
        or scan_result.container_scan_requested
        or scan_result.containers_scanned
        or scan_result.stopped_containers_scanned
        or scan_result.container_images_scanned
        or scan_result.wsl_scanned
    ):
        server = submit_discovered_servers(client, scan_result)
        if server.status == "success":
            submission.response = server.response
        _record_surface_outcomes(
            submission,
            category="mcp",
            outcome=server.status,
        )
        _record_surface_outcomes(
            submission,
            category="client",
            outcome=server.status,
        )
        _record_surface_outcomes(
            submission,
            category="agent",
            outcome=server.status,
            surface_group="runtime",
        )
        if scan_result.total_servers > 0 or scan_result.processes:
            _record_category_outcome(
                submission,
                category="mcp",
                outcome=server.status,
                unsupported_label="Shadow MCP Detection",
                failed_label="servers",
            )
        else:
            submission.category_outcomes["mcp"] = server.status
        if scan_result.detected_clients:
            _record_category_outcome(
                submission,
                category="client",
                outcome=server.status,
                unsupported_label="Shadow Client Detection",
                failed_label="clients",
            )
        else:
            submission.category_outcomes["client"] = server.status
        if (
            server.status == "unsupported"
            and "Shadow MCP Detection" not in submission.unsupported
            and "Shadow Client Detection" not in submission.unsupported
        ):
            submission.unsupported.append("Scan Inventory")
        if (
            server.status == "failed"
            and "servers" not in submission.failed_submissions
            and "clients" not in submission.failed_submissions
        ):
            submission.failed_submissions.append("scan inventory")
        _consume_backend_surface_failures(submission, server.response)

    skill_submission: SubmissionStatus = "success"
    failed_skill_surfaces: set[ScanManifestSurface] = set()
    if scan_result.skills:
        skill_submission = submit_discovered_skills(
            client,
            scan_result.skills,
            scan_result,
            artifact_cache=artifact_cache,
            failed_surfaces=failed_skill_surfaces,
        )
        _record_artifact_submission_outcome(
            submission,
            category="skill",
            outcome=skill_submission,
            failed_surfaces=failed_skill_surfaces,
            unsupported_label="Shadow Skill Detection",
            failed_label="skills",
        )

    # Per-surface skill failures are collected rather than failing the whole
    # submit; presence must still be gated on them or a failed POST would
    # advance the baseline and emit removals for skills the server never saw.
    if skill_submission == "success" and not failed_skill_surfaces:
        presence_submission = reconcile_skill_presence(client, scan_result)
        if presence_submission == "failed":
            submission.failed_submissions.append("skill removals")

    manifest_payload = _scan_manifest_payload(scan_result, submission)
    try:
        manifest_response = client.submit_scan_manifest(manifest_payload)
        if manifest_response.get("unsupported") is not True:
            logger.debug(
                "scan_manifest_submitted",
                entries_reconciled=manifest_response.get("entries_reconciled"),
                installations_updated=manifest_response.get("installations_updated"),
            )
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 403):
            raise
        logger.warning(
            "scan_manifest_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            status_code=exc.response.status_code,
        )
        submission.failed_submissions.append("scan manifest")
    except httpx.RequestError as exc:
        logger.warning(
            "scan_manifest_submission_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        submission.failed_submissions.append("scan manifest")
    except Exception:
        logger.warning("scan_manifest_submission_failed", exc_info=True)
        submission.failed_submissions.append("scan manifest")

    return submission
