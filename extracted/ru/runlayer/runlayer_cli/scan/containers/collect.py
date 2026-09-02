"""Bounded artifact collection and running-container scan orchestration."""

from __future__ import annotations

import posixpath
import time
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import Callable, TypeVar

import structlog

from runlayer_cli.scan.agent_definition_scanner import (
    AGENT_DEFINITION_PATTERNS,
    MAX_AGENT_DEFINITION_USER_DEPTH,
    AgentDefinitionPattern,
    AgentDefinitionScope,
    DiscoveredAgentDefinition,
    dedupe_agent_definitions,
    matches_agent_definition_filename,
    parse_agent_definition,
)
from runlayer_cli.scan.client_presence import (
    DetectedClient,
    coalesce_detected_clients,
)
from runlayer_cli.scan.clients import MCPClientDefinition, NpmPackage, get_all_clients
from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    parse_config_content,
)
from runlayer_cli.scan.containers.collector import ContainerRuntimeCollector
from runlayer_cli.scan.containers.docker_cli import (
    MAX_DOCKER_CP_ARCHIVE_BYTES,
    SCAN_BASE_TIME_BUDGET_S,
    SUBPROCESS_TIMEOUT_S,
    _collect_image_digests,
    _discover_container_ids,
    _discover_stopped_container_ids,
    _find_container_cli,
    _find_docker_cli,
    _inspect_containers,
    _inspect_stopped_containers,
    _list_container_images,
    _remaining_timeout,
    _run_bytes,
    _scaled_scan_time_budget,
)
from runlayer_cli.scan.containers.docker_socket import (
    DockerSocketClient,
    find_docker_socket,
)
from runlayer_cli.scan.containers.inspect_parse import (
    MAX_CONTAINER_IMAGES,
    MAX_CONTAINERS,
    ContainerImageInventory,
    ContainerScanResult,
    DiscoveredContainer,
    DiscoveredContainerImage,
    DockerPSInventory,
    _container_path_within,
    _expand_container_path,
    path_is_shared_with_host_home,
)
from runlayer_cli.scan.containers.k3s_cli import (
    CrictlCommand,
    _collect_image_digests as _collect_k3s_image_digests,
    _discover_container_ids as _discover_k3s_container_ids,
    _find_k3s_crictl,
    _inspect_containers as _inspect_k3s_containers,
)
from runlayer_cli.scan.containers.proc_walk import (
    _copy_proc_file_archive,
    _walk_proc_tree,
)
from runlayer_cli.scan.containers.tar_walk import (
    MAX_DOCKER_TREE_STREAM_BYTES,
    _TarWalkResult,
    _copy_container_tree,
    _extract_copied_file,
)
from runlayer_cli.scan.disguised_skills import validate_disguised_skill_content
from runlayer_cli.scan.file_collector import MAX_TOTAL_BYTES
from runlayer_cli.scan.hidden_space_sweep import is_hidden_container_path
from runlayer_cli.scan.npm_global import ValidatedNpmManifest, validate_npm_manifest
from runlayer_cli.scan.project_tree_match import (
    _ConfigCandidate,
    _ProjectConfigSpec,
    _ProjectFileClassification,
    _iter_agent_matches,
    _iter_skill_groups,
    _project_agent_definition_match,
    _project_candidates_for_path,
    _project_config_specs,
    _project_skill_file_match,
)
from runlayer_cli.scan.skill_scanner import (
    SUPPORTED_EXTENSIONS as SKILL_SUPPORTED_EXTENSIONS,
)
from runlayer_cli.scan.skill_scanner import (
    DiscoveredSkillArtifact,
    SkillFile,
    _GLOBAL_SKILL_DIRS,
    apply_retention_policy,
    build_skill_artifact_from_files,
)

logger = structlog.get_logger(__name__)

_COLLECTOR = TypeVar("_COLLECTOR", bound=ContainerRuntimeCollector)
_STANDARD_CONTAINER_NODE_MODULES = (
    "/usr/local/lib/node_modules",
    "/usr/lib/node_modules",
)
MAX_DOCKER_SCAN_STREAM_BYTES = MAX_DOCKER_TREE_STREAM_BYTES


@dataclass(frozen=True)
class DockerCliCollector:
    """Collector for any docker-CLI-compatible runtime binary.

    ``runtime`` labels discovered containers; podman and nerdctl reuse this
    collector because their ps/inspect/image-ls JSON output is CLI-compatible
    with Docker's.
    """

    docker: str
    operation_timeout: float
    runtime: str = "docker"

    def _stamp_runtime(
        self, containers: list[DiscoveredContainer] | None
    ) -> list[DiscoveredContainer] | None:
        if containers is not None:
            for container in containers:
                container.runtime = self.runtime
        return containers

    def discover_container_ids(self, *, deadline: float) -> DockerPSInventory | None:
        return _discover_container_ids(
            docker=self.docker,
            deadline=deadline,
            subprocess_timeout=self.operation_timeout,
        )

    def inspect_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None:
        return self._stamp_runtime(
            _inspect_containers(
                docker=self.docker,
                container_ids=container_ids,
                deadline=deadline,
                subprocess_timeout=self.operation_timeout,
                host_home=host_home,
            )
        )

    def collect_image_digests(
        self,
        *,
        containers: list[DiscoveredContainer],
        deadline: float,
    ) -> list[DiscoveredContainer]:
        return _collect_image_digests(
            docker=self.docker,
            containers=containers,
            deadline=deadline,
            subprocess_timeout=self.operation_timeout,
        )

    def discover_stopped_container_ids(
        self, *, deadline: float
    ) -> DockerPSInventory | None:
        return _discover_stopped_container_ids(
            docker=self.docker,
            deadline=deadline,
            subprocess_timeout=self.operation_timeout,
        )

    def inspect_stopped_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None:
        return self._stamp_runtime(
            _inspect_stopped_containers(
                docker=self.docker,
                container_ids=container_ids,
                deadline=deadline,
                subprocess_timeout=self.operation_timeout,
                host_home=host_home,
            )
        )

    def list_container_images(
        self, *, deadline: float
    ) -> ContainerImageInventory | None:
        return _list_container_images(
            docker=self.docker,
            deadline=deadline,
            subprocess_timeout=self.operation_timeout,
        )

    def copy_file_archive(
        self,
        *,
        container: DiscoveredContainer,
        path: str,
        deadline: float,
    ) -> bytes | None:
        timeout = _remaining_timeout(deadline, self.operation_timeout)
        if timeout is None:
            return None
        return _run_bytes(
            [self.docker, "cp", f"{container.container_id}:{path}", "-"],
            timeout=timeout,
            max_output=MAX_DOCKER_CP_ARCHIVE_BYTES,
        )

    def copy_tree(
        self,
        *,
        container: DiscoveredContainer,
        root_path: str,
        wanted_file: Callable[[str], bool],
        allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
        deadline: float,
        max_stream_bytes: int = MAX_DOCKER_TREE_STREAM_BYTES,
    ) -> _TarWalkResult:
        return _copy_container_tree(
            docker=self.docker,
            container_id=container.container_id,
            root_path=root_path,
            wanted_file=wanted_file,
            allow_file_in_skipped_directory=allow_file_in_skipped_directory,
            deadline=deadline,
            max_stream_bytes=max_stream_bytes,
        )


class DockerSocketCollector:
    def __init__(self, socket_path: str, *, operation_timeout: float) -> None:
        self._client = DockerSocketClient(
            socket_path,
            request_timeout=operation_timeout,
        )

    def discover_container_ids(self, *, deadline: float) -> DockerPSInventory | None:
        return self._client.discover_container_ids(deadline=deadline)

    def inspect_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None:
        return self._client.inspect_containers(
            container_ids=container_ids,
            deadline=deadline,
            host_home=host_home,
        )

    def collect_image_digests(
        self,
        *,
        containers: list[DiscoveredContainer],
        deadline: float,
    ) -> list[DiscoveredContainer]:
        return self._client.collect_image_digests(
            containers=containers,
            deadline=deadline,
        )

    def discover_stopped_container_ids(
        self, *, deadline: float
    ) -> DockerPSInventory | None:
        return self._client.discover_stopped_container_ids(deadline=deadline)

    def inspect_stopped_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None:
        return self._client.inspect_stopped_containers(
            container_ids=container_ids,
            deadline=deadline,
            host_home=host_home,
        )

    def list_container_images(
        self, *, deadline: float
    ) -> ContainerImageInventory | None:
        return self._client.list_container_images(deadline=deadline)

    def copy_file_archive(
        self,
        *,
        container: DiscoveredContainer,
        path: str,
        deadline: float,
    ) -> bytes | None:
        return self._client.copy_file_archive(
            container_id=container.container_id,
            path=path,
            deadline=deadline,
        )

    def copy_tree(
        self,
        *,
        container: DiscoveredContainer,
        root_path: str,
        wanted_file: Callable[[str], bool],
        allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
        deadline: float,
        max_stream_bytes: int = MAX_DOCKER_TREE_STREAM_BYTES,
    ) -> _TarWalkResult:
        return self._client.copy_tree(
            container_id=container.container_id,
            root_path=root_path,
            wanted_file=wanted_file,
            allow_file_in_skipped_directory=allow_file_in_skipped_directory,
            deadline=deadline,
            max_stream_bytes=max_stream_bytes,
        )


@dataclass(frozen=True)
class K3sCrictlCollector:
    crictl: CrictlCommand
    operation_timeout: float
    proc_root: Path = Path("/proc")

    def discover_container_ids(self, *, deadline: float) -> DockerPSInventory | None:
        return _discover_k3s_container_ids(
            crictl=self.crictl,
            deadline=deadline,
            subprocess_timeout=self.operation_timeout,
        )

    def inspect_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None:
        return _inspect_k3s_containers(
            crictl=self.crictl,
            container_ids=container_ids,
            deadline=deadline,
            subprocess_timeout=self.operation_timeout,
            host_home=host_home,
        )

    def collect_image_digests(
        self,
        *,
        containers: list[DiscoveredContainer],
        deadline: float,
    ) -> list[DiscoveredContainer]:
        return _collect_k3s_image_digests(
            crictl=self.crictl,
            containers=containers,
            deadline=deadline,
            subprocess_timeout=self.operation_timeout,
        )

    def copy_file_archive(
        self,
        *,
        container: DiscoveredContainer,
        path: str,
        deadline: float,
    ) -> bytes | None:
        pid = container.pid
        if pid is None:
            return None
        operation_deadline = min(
            deadline,
            time.monotonic() + max(self.operation_timeout, 0.05),
        )
        return _copy_proc_file_archive(
            proc_root=self.proc_root,
            pid=pid,
            path=path,
            deadline=operation_deadline,
            container_id=container.container_id,
        )

    def copy_tree(
        self,
        *,
        container: DiscoveredContainer,
        root_path: str,
        wanted_file: Callable[[str], bool],
        allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
        deadline: float,
        max_stream_bytes: int = MAX_DOCKER_TREE_STREAM_BYTES,
    ) -> _TarWalkResult:
        pid = container.pid
        if pid is None:
            return _TarWalkResult()
        operation_deadline = min(
            deadline,
            time.monotonic() + max(self.operation_timeout, 0.05),
        )
        return _walk_proc_tree(
            proc_root=self.proc_root,
            pid=pid,
            root_path=root_path,
            wanted_file=wanted_file,
            allow_file_in_skipped_directory=allow_file_in_skipped_directory,
            deadline=operation_deadline,
            max_stream_bytes=max_stream_bytes,
            container_id=container.container_id,
        )


# Path matching, the classification type, and the drift-prone grouping/iteration
# skeletons are shared via project_tree_match. Classification and config building
# stay container-local: they thread per-container metadata + side effects
# (has_mcp_configs, runtime="container", container_* fields) and filter
# host-home-shared / excluded global-skill / user-agent roots — sharing them
# would be predicate/kwarg soup for no real gain.
@dataclass
class _CollectedContainerArtifacts:
    configurations: list[MCPClientConfig] = field(default_factory=list)
    detected_clients: list[DetectedClient] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)


@dataclass(frozen=True)
class _ContainerNpmSpec:
    client: MCPClientDefinition
    package: NpmPackage


def _config_candidates(
    container: DiscoveredContainer,
    clients: list[MCPClientDefinition],
) -> list[_ConfigCandidate]:
    candidates: list[_ConfigCandidate] = []
    seen: set[tuple[str, str]] = set()
    for client in clients:
        for config_path in client.paths:
            if config_path.platform not in {"linux", "all"}:
                continue
            resolved = _expand_container_path(
                config_path.path,
                home=container.home,
                environment=container.environment,
            )
            key = (client.name, resolved or "")
            if resolved and key not in seen:
                seen.add(key)
                candidates.append(_ConfigCandidate(client=client, path=resolved))
    return candidates


def _container_agent_user_roots(
    container: DiscoveredContainer,
) -> tuple[tuple[AgentDefinitionPattern, str], ...]:
    roots: list[tuple[AgentDefinitionPattern, str]] = []
    seen: set[tuple[str, str]] = set()
    for pattern in AGENT_DEFINITION_PATTERNS:
        for template in pattern.user_roots:
            if not template.startswith("~/"):
                continue
            root = posixpath.normpath(posixpath.join(container.home, template[2:]))
            key = (pattern.client, root)
            if key not in seen:
                seen.add(key)
                roots.append((pattern, root))
    return tuple(roots)


def _classify_project_file(
    path: str,
    *,
    root_path: str,
    specs: list[_ProjectConfigSpec],
    container: DiscoveredContainer,
    host_home: Path,
    excluded_skill_roots: tuple[str, ...],
    excluded_agent_roots: tuple[str, ...],
) -> _ProjectFileClassification | None:
    """Classify one work-tree file, or ``None`` when nothing is collectible.

    Runs the config/skill/agent path matching (and host-home / excluded-root
    filtering) exactly once, so the tar ``wanted_file`` predicate and the
    downstream builders reuse one result instead of recomputing per file.
    """
    if path_is_shared_with_host_home(path, container.mounts, host_home):
        return None
    config_candidates = tuple(
        _project_candidates_for_path(path, root_path=root_path, specs=specs)
    )
    skill_match = _project_skill_file_match(path, root_path=root_path)
    if skill_match is not None and any(
        _container_path_within(skill_match.skill_path, excluded_root)
        for excluded_root in excluded_skill_roots
    ):
        skill_match = None
    agent_match = _project_agent_definition_match(path, root_path=root_path)
    if agent_match is not None and any(
        _container_path_within(path, excluded_root)
        for excluded_root in excluded_agent_roots
    ):
        agent_match = None
    if not config_candidates and skill_match is None and agent_match is None:
        return None
    return _ProjectFileClassification(
        config_candidates=config_candidates,
        skill_match=skill_match,
        agent_match=agent_match,
    )


def _container_agent_definition(
    *,
    pattern: AgentDefinitionPattern,
    path: str,
    content: bytes,
    scope: AgentDefinitionScope,
    project_path: str | None,
    container: DiscoveredContainer,
) -> DiscoveredAgentDefinition | None:
    return parse_agent_definition(
        client=pattern.client,
        path=path,
        content=content,
        scope=scope,
        project_path=project_path,
        container_id=container.container_id,
        container_name=container.name,
        container_image_ref=container.image_ref,
        container_image_digest=container.image_digest,
        container_runtime=container.runtime,
        container_is_devcontainer=container.is_devcontainer,
        container_is_running=container.is_running,
        container_labels=container.labels,
        container_mounts_host_home=container.mounts_host_home,
    )


def _project_agent_definitions_from_files(
    files: dict[str, bytes],
    classifications: dict[str, _ProjectFileClassification],
    *,
    container: DiscoveredContainer,
) -> list[DiscoveredAgentDefinition]:
    definitions: list[DiscoveredAgentDefinition] = []
    for pattern, path, project_path, content in _iter_agent_matches(
        files, classifications
    ):
        definition = _container_agent_definition(
            pattern=pattern,
            path=path,
            content=content,
            scope="project",
            project_path=project_path,
            container=container,
        )
        if definition is not None:
            definitions.append(definition)
    return definitions


def _user_agent_definitions_from_files(
    files: dict[str, bytes],
    *,
    pattern: AgentDefinitionPattern,
    root_path: str,
    container: DiscoveredContainer,
) -> list[DiscoveredAgentDefinition]:
    definitions: list[DiscoveredAgentDefinition] = []
    for path in sorted(files):
        if not _container_path_within(
            path, root_path
        ) or not matches_agent_definition_filename(pattern, posixpath.basename(path)):
            continue
        definition = _container_agent_definition(
            pattern=pattern,
            path=path,
            content=files[path],
            scope="user",
            project_path=None,
            container=container,
        )
        if definition is not None:
            definitions.append(definition)
    return definitions


def _project_skills_from_files(
    files: dict[str, bytes],
    classifications: dict[str, _ProjectFileClassification],
    *,
    container: DiscoveredContainer,
) -> list[DiscoveredSkillArtifact]:
    skills: list[DiscoveredSkillArtifact] = []
    for skill_path, project_path, raw_files in _iter_skill_groups(
        files, classifications
    ):
        artifact = _container_skill_from_files(
            skill_path=skill_path,
            raw_files=raw_files,
            scope="project",
            tool="multi",
            project_path=project_path,
            source_type="user",
            container=container,
        )
        if artifact is not None:
            skills.append(artifact)
    return skills


def _container_skill_from_files(
    *,
    skill_path: str,
    raw_files: dict[str, bytes],
    scope: str,
    tool: str,
    project_path: str | None,
    source_type: str,
    container: DiscoveredContainer,
) -> DiscoveredSkillArtifact | None:
    return build_skill_artifact_from_files(
        skill_path=skill_path,
        files=raw_files,
        scope=scope,
        tool=tool,
        project_path=project_path,
        source_type=source_type,
        container_id=container.container_id,
        container_name=container.name,
        container_image_ref=container.image_ref,
        container_image_digest=container.image_digest,
        container_runtime=container.runtime,
        container_is_devcontainer=container.is_devcontainer,
        container_is_running=container.is_running,
        container_labels=container.labels,
        container_mounts_host_home=container.mounts_host_home,
    )


def _global_skills_from_files(
    files: dict[str, bytes],
    *,
    root_path: str,
    tool: str,
    container: DiscoveredContainer,
) -> list[DiscoveredSkillArtifact]:
    grouped: dict[str, dict[str, bytes]] = {}
    for path, content in files.items():
        if (
            not _container_path_within(path, root_path)
            or posixpath.splitext(path)[1].lower() not in SKILL_SUPPORTED_EXTENSIONS
        ):
            continue
        relative_parts = tuple(posixpath.relpath(path, root_path).split("/"))
        if len(relative_parts) < 2:
            continue
        skill_path = posixpath.join(root_path, relative_parts[0])
        relative_file = posixpath.join(*relative_parts[1:])
        grouped.setdefault(skill_path, {})[relative_file] = content

    skills: list[DiscoveredSkillArtifact] = []
    for skill_path in sorted(grouped):
        artifact = _container_skill_from_files(
            skill_path=skill_path,
            raw_files=grouped[skill_path],
            scope="global",
            tool=tool,
            project_path=None,
            source_type="installed",
            container=container,
        )
        if artifact is not None:
            skills.append(artifact)
    return skills


def _configuration_from_candidate(
    *,
    container: DiscoveredContainer,
    candidate: _ConfigCandidate,
    content: bytes,
) -> MCPClientConfig | None:
    servers = parse_config_content(candidate.client, content)
    if not servers:
        return None
    container.has_mcp_configs = True
    for server in servers:
        server.runtime = "container"
        if candidate.project_path:
            server.project_name = candidate.project_path
    return MCPClientConfig(
        client=candidate.client.name,
        config_path=candidate.path,
        servers=servers,
        config_scope="container",
        project_path=candidate.project_path,
        container_id=container.container_id,
        container_name=container.name,
        container_image_ref=container.image_ref,
        container_image_digest=container.image_digest,
        container_is_devcontainer=container.is_devcontainer,
        container_mounts_host_home=container.mounts_host_home,
    )


class _CollectionBudgetExhausted(Exception):
    """Abort all remaining collection once a time or byte budget is spent."""


@dataclass
class _ArtifactByteBudget:
    """Running total of collected artifact bytes across every container and phase.

    Covers configs, skills, and agent definitions alike: each tar walk is
    individually bounded, but the aggregate held across 4 phases x up to 64
    containers must also stay under ``MAX_TOTAL_BYTES``.
    """

    total_bytes: int = 0
    stream_bytes: int = 0

    def charge(self, size: int) -> None:
        """Account for collected bytes, aborting collection once over the cap."""
        if self.total_bytes + size > MAX_TOTAL_BYTES:
            raise _CollectionBudgetExhausted
        self.total_bytes += size

    def charge_files(self, files: dict[str, bytes]) -> None:
        """Charge one walk's matched file contents in a single debit."""
        self.charge(sum(len(content) for content in files.values()))

    def remaining_stream_bytes(self) -> int:
        return max(MAX_DOCKER_SCAN_STREAM_BYTES - self.stream_bytes, 0)

    def charge_stream(self, size: int) -> None:
        if size < 0 or size > self.remaining_stream_bytes():
            raise _CollectionBudgetExhausted
        self.stream_bytes += size


@dataclass(frozen=True)
class _PhaseContext:
    """Per-scan invariants shared by every collection phase and container.

    Built once in ``_collect_container_artifacts``; ``artifacts`` and
    ``budget`` are the shared mutable sinks each phase appends to / charges.
    """

    collector: ContainerRuntimeCollector
    artifacts: _CollectedContainerArtifacts
    budget: _ArtifactByteBudget
    deadline: float
    subprocess_timeout: float
    host_home: Path

    def tree_deadline_or_stop(self) -> float:
        """Bound one tree walk; abort collection when the deadline has passed."""
        now = time.monotonic()
        if now >= self.deadline:
            raise _CollectionBudgetExhausted
        return min(self.deadline, now + max(self.subprocess_timeout, 0.05))

    def tree_stream_allowance_or_stop(self) -> int:
        remaining = self.budget.remaining_stream_bytes()
        if remaining <= 0:
            raise _CollectionBudgetExhausted
        return remaining


def _make_wanted_project_file(
    *,
    root_path: str,
    project_specs: list[_ProjectConfigSpec],
    container: DiscoveredContainer,
    host_home: Path,
    excluded_skill_roots: tuple[str, ...],
    excluded_agent_roots: tuple[str, ...],
    classifications: dict[str, _ProjectFileClassification],
) -> Callable[[str], bool]:
    """Build the project-tree predicate, memoizing matches into ``classifications``.

    Every input (including the shared ``classifications`` sink the downstream
    builders read) is bound as an explicit factory argument rather than captured
    from an enclosing loop, which sidesteps the B023 late-binding footgun.
    """

    def _wanted(path: str) -> bool:
        classification = _classify_project_file(
            path,
            root_path=root_path,
            specs=project_specs,
            container=container,
            host_home=host_home,
            excluded_skill_roots=excluded_skill_roots,
            excluded_agent_roots=excluded_agent_roots,
        )
        if classification is None:
            return False
        classifications[path] = classification
        return True

    return _wanted


def _make_wanted_global_file(
    *,
    global_root: str,
    container: DiscoveredContainer,
    host_home: Path,
) -> Callable[[str], bool]:
    """Build the predicate matching supported skill files under a global root."""

    def _wanted(path: str) -> bool:
        if path_is_shared_with_host_home(path, container.mounts, host_home):
            return False
        relative = posixpath.relpath(path, global_root)
        return (
            not relative.startswith("../")
            and len(relative.split("/")) >= 2
            and posixpath.splitext(path)[1].lower() in SKILL_SUPPORTED_EXTENSIONS
        )

    return _wanted


def _make_wanted_user_definition(
    *,
    user_root: str,
    pattern: AgentDefinitionPattern,
    container: DiscoveredContainer,
    host_home: Path,
) -> Callable[[str], bool]:
    """Build the predicate matching one client's user agent-definition files."""

    def _wanted(path: str) -> bool:
        if path_is_shared_with_host_home(path, container.mounts, host_home):
            return False
        relative = posixpath.relpath(path, user_root)
        return (
            not relative.startswith("../")
            and len(relative.split("/")) <= MAX_AGENT_DEFINITION_USER_DEPTH + 1
            and matches_agent_definition_filename(pattern, posixpath.basename(path))
        )

    return _wanted


def _container_npm_spec(
    path: str,
    specs: tuple[_ContainerNpmSpec, ...],
) -> _ContainerNpmSpec | None:
    parts = tuple(part for part in posixpath.normpath(path).split("/") if part)
    for spec in specs:
        package_parts = tuple(spec.package.name.split("/"))
        expected_suffix = ("node_modules", *package_parts, "package.json")
        if (
            len(parts) >= len(expected_suffix)
            and parts[-len(expected_suffix) :] == expected_suffix
        ):
            return spec
    return None


def _make_wanted_hidden_artifact(
    *,
    root_path: str,
    container: DiscoveredContainer,
    host_home: Path,
    npm_specs: tuple[_ContainerNpmSpec, ...],
    detect_disguised_skills: bool,
) -> Callable[[str], bool]:
    """Match identity-bearing files below bounded omitted-space roots."""

    def _wanted(path: str) -> bool:
        omitted_space = root_path in {"/tmp", "/var/tmp"} or is_hidden_container_path(
            path,
            root_path=root_path,
        )
        shared = path_is_shared_with_host_home(path, container.mounts, host_home)
        npm_spec = _container_npm_spec(path, npm_specs)
        return not shared and (
            (omitted_space and detect_disguised_skills) or npm_spec is not None
        )

    return _wanted


def _make_allow_hidden_npm_manifest(
    npm_specs: tuple[_ContainerNpmSpec, ...],
) -> Callable[[str], bool]:
    def _allowed(path: str) -> bool:
        return _container_npm_spec(path, npm_specs) is not None

    return _allowed


def _disguised_container_skill(
    *,
    path: str,
    content_bytes: bytes,
    container: DiscoveredContainer,
) -> DiscoveredSkillArtifact | None:
    content = validate_disguised_skill_content(content_bytes)
    if content is None:
        return None
    artifact = build_skill_artifact_from_files(
        skill_path=path,
        files=[SkillFile(title="SKILL.md", content=content)],
        marker_content=content,
        scope="user",
        tool="browser_cache",
        fallback_name=posixpath.splitext(posixpath.basename(path))[0],
        source_type="user",
        container_id=container.container_id,
        container_name=container.name,
        container_image_ref=container.image_ref,
        container_image_digest=container.image_digest,
        container_runtime=container.runtime,
        container_is_devcontainer=container.is_devcontainer,
        container_is_running=container.is_running,
        container_labels=container.labels,
        container_mounts_host_home=container.mounts_host_home,
    )
    if artifact is not None:
        apply_retention_policy(artifact)
    return artifact


def _record_container_npm_agent(
    artifacts: _CollectedContainerArtifacts,
    *,
    container: DiscoveredContainer,
    path: str,
    spec: _ContainerNpmSpec,
    manifest: ValidatedNpmManifest,
) -> None:
    detected = next(
        (
            item
            for item in artifacts.detected_clients
            if item.client == spec.client.name
        ),
        None,
    )
    if detected is None:
        detected = DetectedClient(
            client=spec.client.name,
            display_name=spec.client.display_name,
        )
        artifacts.detected_clients.append(detected)
    evidence_container = container.name or container.container_id
    detected.add_detection(
        "container",
        version=manifest.version,
        config_path=f"container:{evidence_container}:{path}",
        container_id=container.container_id,
    )
    container.has_ai_agents = True


def _validated_container_npm_manifest(
    ctx: _PhaseContext,
    *,
    container: DiscoveredContainer,
    manifest_path: str,
    content: bytes,
    spec: _ContainerNpmSpec,
) -> ValidatedNpmManifest | None:
    manifest = validate_npm_manifest(content, spec.package)
    if manifest is None:
        return None
    package_dir = posixpath.dirname(manifest_path)
    target_path = posixpath.normpath(
        posixpath.join(package_dir, *manifest.bin_target.parts)
    )
    if path_is_shared_with_host_home(
        target_path,
        container.mounts,
        ctx.host_home,
    ):
        return None
    archive = ctx.collector.copy_file_archive(
        container=container,
        path=target_path,
        deadline=ctx.tree_deadline_or_stop(),
    )
    target_content = _extract_copied_file(archive) if archive is not None else None
    if target_content is None:
        return None
    ctx.budget.charge(len(target_content))
    return manifest


def _collect_standard_container_npm_agents(
    ctx: _PhaseContext,
    container: DiscoveredContainer,
    npm_specs: tuple[_ContainerNpmSpec, ...],
) -> None:
    for node_modules in _STANDARD_CONTAINER_NODE_MODULES:
        if path_is_shared_with_host_home(
            node_modules,
            container.mounts,
            ctx.host_home,
        ):
            continue
        for spec in npm_specs:
            package_parts = spec.package.name.split("/")
            manifest_path = posixpath.join(
                node_modules,
                *package_parts,
                "package.json",
            )
            if path_is_shared_with_host_home(
                manifest_path,
                container.mounts,
                ctx.host_home,
            ):
                continue
            archive = ctx.collector.copy_file_archive(
                container=container,
                path=manifest_path,
                deadline=ctx.tree_deadline_or_stop(),
            )
            content = _extract_copied_file(archive) if archive is not None else None
            if content is None:
                continue
            ctx.budget.charge(len(content))
            manifest = _validated_container_npm_manifest(
                ctx,
                container=container,
                manifest_path=manifest_path,
                content=content,
                spec=spec,
            )
            if manifest is not None:
                _record_container_npm_agent(
                    ctx.artifacts,
                    container=container,
                    path=manifest_path,
                    spec=spec,
                    manifest=manifest,
                )


def _collect_container_configs(
    ctx: _PhaseContext,
    container: DiscoveredContainer,
    clients: list[MCPClientDefinition],
) -> None:
    """Phase 1: copy and parse each known per-client config path."""
    for candidate in _config_candidates(container, clients):
        if path_is_shared_with_host_home(
            candidate.path, container.mounts, ctx.host_home
        ):
            continue
        timeout = _remaining_timeout(ctx.deadline, ctx.subprocess_timeout)
        if timeout is None:
            raise _CollectionBudgetExhausted
        archive = ctx.collector.copy_file_archive(
            container=container,
            path=candidate.path,
            deadline=ctx.deadline,
        )
        if archive is None:
            continue
        content = _extract_copied_file(archive)
        if content is None:
            continue
        ctx.budget.charge(len(content))
        configuration = _configuration_from_candidate(
            container=container,
            candidate=candidate,
            content=content,
        )
        if configuration is not None:
            ctx.artifacts.configurations.append(configuration)


def _collect_container_project_tree(
    ctx: _PhaseContext,
    container: DiscoveredContainer,
    project_specs: list[_ProjectConfigSpec],
    excluded_skill_roots: tuple[str, ...],
    excluded_agent_roots: tuple[str, ...],
) -> None:
    """Phase 2: walk the working-dir tree for project configs, skills, agents."""
    root_path = container.working_dir
    if root_path is None or path_is_shared_with_host_home(
        root_path, container.mounts, ctx.host_home
    ):
        return
    tree_deadline = ctx.tree_deadline_or_stop()
    classifications: dict[str, _ProjectFileClassification] = {}
    walked = ctx.collector.copy_tree(
        container=container,
        root_path=root_path,
        wanted_file=_make_wanted_project_file(
            root_path=root_path,
            project_specs=project_specs,
            container=container,
            host_home=ctx.host_home,
            excluded_skill_roots=excluded_skill_roots,
            excluded_agent_roots=excluded_agent_roots,
            classifications=classifications,
        ),
        deadline=tree_deadline,
        max_stream_bytes=ctx.tree_stream_allowance_or_stop(),
    )
    ctx.budget.charge_stream(walked.stream_bytes)
    ctx.budget.charge_files(walked.files)
    for path, content in walked.files.items():
        candidates = classifications[path].config_candidates
        if not candidates:
            continue
        for candidate in candidates:
            configuration = _configuration_from_candidate(
                container=container,
                candidate=candidate,
                content=content,
            )
            if configuration is not None:
                ctx.artifacts.configurations.append(configuration)
    ctx.artifacts.skills.extend(
        _project_skills_from_files(walked.files, classifications, container=container)
    )
    ctx.artifacts.agent_definitions.extend(
        _project_agent_definitions_from_files(
            walked.files, classifications, container=container
        )
    )


def _collect_container_global_skills(
    ctx: _PhaseContext,
    container: DiscoveredContainer,
    global_skill_roots: dict[str, str],
) -> None:
    """Phase 3: walk each installed global skill root."""
    for relative_root, tool in _GLOBAL_SKILL_DIRS:
        global_root = global_skill_roots[relative_root]
        if path_is_shared_with_host_home(
            global_root,
            container.mounts,
            ctx.host_home,
        ):
            continue
        tree_deadline = ctx.tree_deadline_or_stop()
        wanted_global_file = _make_wanted_global_file(
            global_root=global_root,
            container=container,
            host_home=ctx.host_home,
        )
        walked = ctx.collector.copy_tree(
            container=container,
            root_path=global_root,
            wanted_file=wanted_global_file,
            deadline=tree_deadline,
            max_stream_bytes=ctx.tree_stream_allowance_or_stop(),
        )
        ctx.budget.charge_stream(walked.stream_bytes)
        ctx.budget.charge_files(walked.files)
        ctx.artifacts.skills.extend(
            _global_skills_from_files(
                walked.files,
                root_path=global_root,
                tool=tool,
                container=container,
            )
        )


def _collect_container_user_definitions(
    ctx: _PhaseContext,
    container: DiscoveredContainer,
    agent_user_roots: tuple[tuple[AgentDefinitionPattern, str], ...],
) -> None:
    """Phase 4: walk each client's user agent-definition root."""
    for pattern, user_root in agent_user_roots:
        if path_is_shared_with_host_home(
            user_root,
            container.mounts,
            ctx.host_home,
        ):
            continue
        tree_deadline = ctx.tree_deadline_or_stop()
        wanted_user_definition = _make_wanted_user_definition(
            user_root=user_root,
            pattern=pattern,
            container=container,
            host_home=ctx.host_home,
        )
        walked = ctx.collector.copy_tree(
            container=container,
            root_path=user_root,
            wanted_file=wanted_user_definition,
            deadline=tree_deadline,
            max_stream_bytes=ctx.tree_stream_allowance_or_stop(),
        )
        ctx.budget.charge_stream(walked.stream_bytes)
        ctx.budget.charge_files(walked.files)
        ctx.artifacts.agent_definitions.extend(
            _user_agent_definitions_from_files(
                walked.files,
                pattern=pattern,
                root_path=user_root,
                container=container,
            )
        )


def _collect_container_hidden_artifacts(
    ctx: _PhaseContext,
    container: DiscoveredContainer,
    *,
    npm_specs: tuple[_ContainerNpmSpec, ...],
    detect_disguised_skills: bool,
) -> None:
    """Probe hidden home/tmp trees once for skill and npm identities."""
    roots = tuple(
        dict.fromkeys(
            root
            for root in (
                container.home,
                "/tmp",
                "/var/tmp",
                container.working_dir,
            )
            if root is not None
        )
    )
    for root_path in roots:
        if path_is_shared_with_host_home(
            root_path,
            container.mounts,
            ctx.host_home,
        ):
            continue
        walked = ctx.collector.copy_tree(
            container=container,
            root_path=root_path,
            wanted_file=_make_wanted_hidden_artifact(
                root_path=root_path,
                container=container,
                host_home=ctx.host_home,
                npm_specs=npm_specs,
                detect_disguised_skills=detect_disguised_skills,
            ),
            allow_file_in_skipped_directory=_make_allow_hidden_npm_manifest(npm_specs),
            deadline=ctx.tree_deadline_or_stop(),
            max_stream_bytes=ctx.tree_stream_allowance_or_stop(),
        )
        ctx.budget.charge_stream(walked.stream_bytes)
        ctx.budget.charge_files(walked.files)
        for path, content in walked.files.items():
            if detect_disguised_skills:
                artifact = _disguised_container_skill(
                    path=path,
                    content_bytes=content,
                    container=container,
                )
                if artifact is not None:
                    ctx.artifacts.skills.append(artifact)
            npm_spec = _container_npm_spec(path, npm_specs)
            if npm_spec is not None:
                manifest = _validated_container_npm_manifest(
                    ctx,
                    container=container,
                    manifest_path=path,
                    content=content,
                    spec=npm_spec,
                )
                if manifest is not None:
                    _record_container_npm_agent(
                        ctx.artifacts,
                        container=container,
                        path=path,
                        spec=npm_spec,
                        manifest=manifest,
                    )


def _collect_container_artifacts(
    *,
    collector: ContainerRuntimeCollector,
    containers: list[DiscoveredContainer],
    clients: list[MCPClientDefinition],
    deadline: float,
    subprocess_timeout: float,
    host_home: Path,
    detect_disguised_skills: bool = False,
) -> _CollectedContainerArtifacts:
    """Copy and parse known artifacts from inspected containers.

    Standard npm identities run across every container before general artifact
    collection so earlier noisy trees cannot consume their reserved ordering.
    General phases then collect configs, project trees, global skills, user
    definitions, and hidden artifacts under shared content and stream budgets.
    """
    ctx = _PhaseContext(
        collector=collector,
        artifacts=_CollectedContainerArtifacts(),
        budget=_ArtifactByteBudget(),
        deadline=deadline,
        subprocess_timeout=subprocess_timeout,
        host_home=host_home,
    )
    project_specs = _project_config_specs(clients)
    npm_specs = tuple(
        _ContainerNpmSpec(client=client, package=package)
        for client in clients
        if client.install_probe is not None
        for package in client.install_probe.npm_packages
    )
    try:
        for container in containers:
            _collect_standard_container_npm_agents(ctx, container, npm_specs)
        for container in containers:
            agent_user_roots = _container_agent_user_roots(container)
            global_skill_roots = {
                relative_root: posixpath.normpath(
                    posixpath.join(container.home, relative_root)
                )
                for relative_root, _ in _GLOBAL_SKILL_DIRS
            }
            _collect_container_configs(ctx, container, clients)
            _collect_container_project_tree(
                ctx,
                container,
                project_specs,
                excluded_skill_roots=tuple(global_skill_roots.values()),
                excluded_agent_roots=tuple(
                    user_root for _, user_root in agent_user_roots
                ),
            )
            _collect_container_global_skills(ctx, container, global_skill_roots)
            _collect_container_user_definitions(ctx, container, agent_user_roots)
            if detect_disguised_skills or npm_specs:
                _collect_container_hidden_artifacts(
                    ctx,
                    container,
                    npm_specs=npm_specs,
                    detect_disguised_skills=detect_disguised_skills,
                )
    except _CollectionBudgetExhausted:
        pass
    return ctx.artifacts


def _scan_with_collector(
    *,
    collector: ContainerRuntimeCollector,
    clients: list[MCPClientDefinition],
    subprocess_timeout: float,
    time_budget: float | None,
    host_home: Path,
    started_at: float | None = None,
    detect_disguised_skills: bool = False,
) -> ContainerScanResult | None:
    """Run the bounded discovery and collection pipeline for one runtime.

    The time budget is per-runtime. Docker threads one ``started_at`` through its
    transport fallback and supplemental inventory; distinct runtimes omit it and
    receive independent budgets. See ``_scan_running_containers``.
    """
    scan_started_at = started_at if started_at is not None else time.monotonic()
    deadline = scan_started_at + (
        time_budget if time_budget is not None else SCAN_BASE_TIME_BUDGET_S
    )
    inventory = collector.discover_container_ids(
        deadline=deadline,
    )
    if inventory is None:
        return None
    container_ids = inventory["container_ids"]
    if not container_ids:
        return ContainerScanResult(
            scan_succeeded=not inventory["malformed"] and inventory["output_empty"]
        )

    if time_budget is None:
        deadline = scan_started_at + _scaled_scan_time_budget(len(container_ids))

    containers = collector.inspect_containers(
        container_ids=container_ids,
        deadline=deadline,
        host_home=host_home,
    )
    if containers is None:
        return ContainerScanResult()
    containers = collector.collect_image_digests(
        containers=containers,
        deadline=deadline,
    )
    artifacts = _collect_container_artifacts(
        collector=collector,
        containers=containers,
        clients=clients,
        deadline=deadline,
        subprocess_timeout=subprocess_timeout,
        host_home=host_home,
        detect_disguised_skills=detect_disguised_skills,
    )

    logger.info(
        "Container scan complete",
        container_count=len(containers),
        config_count=len(artifacts.configurations),
        skill_count=len(artifacts.skills),
        agent_definition_count=len(artifacts.agent_definitions),
    )
    # scan_succeeded marks the inventory authoritative: the backend treats any
    # previously-seen container missing from a successful scan as stopped. The
    # Docker CLI and Engine-API socket collectors return None from
    # inspect_containers unless every discovered ID parsed, so their inspected
    # set always matches. The k3s/crictl collector inspects per container and
    # drops rows that fail to parse or raced to stopped between ps and inspect,
    # returning a short (or empty) list. Require the inspected set to equal the
    # discovered set here so a partial k3s inventory reports scan_succeeded=False
    # instead of reaping still-running containers, while its parsed containers
    # and their artifacts are still collected above.
    inventory_complete = len(containers) == len(container_ids) and {
        container.container_id for container in containers
    } == set(container_ids)
    return ContainerScanResult(
        containers=containers,
        configurations=artifacts.configurations,
        detected_clients=artifacts.detected_clients,
        skills=artifacts.skills,
        agent_definitions=dedupe_agent_definitions(artifacts.agent_definitions),
        scan_succeeded=not inventory["truncated"]
        and not inventory["malformed"]
        and inventory_complete,
    )


def _iter_available_docker_collectors(
    *,
    operation_timeout: float,
) -> Iterator[DockerCliCollector | DockerSocketCollector]:
    """Yield CLI then socket fallback, resolving each only when requested."""
    docker = _find_docker_cli()
    if docker is not None:
        yield DockerCliCollector(
            docker,
            operation_timeout=operation_timeout,
        )

    socket_path = find_docker_socket()
    if socket_path is not None:
        yield DockerSocketCollector(
            socket_path,
            operation_timeout=operation_timeout,
        )


# Docker-CLI-compatible runtimes that are distinct daemons (not alternate
# transports to the Docker daemon), scanned alongside Docker so hosts running
# both surface both container sets. CLI-only in this pass: no socket transport
# for podman/nerdctl.
_DISTINCT_CLI_RUNTIMES: tuple[str, ...] = ("podman", "nerdctl")


def _iter_available_cli_runtime_collectors(
    runtime: str,
    *,
    operation_timeout: float,
) -> Iterator[DockerCliCollector]:
    binary = _find_container_cli(runtime)
    if binary is not None:
        yield DockerCliCollector(
            binary,
            operation_timeout=operation_timeout,
            runtime=runtime,
        )


@dataclass
class DockerInventoryResult:
    """Supplemental Docker inventory merged into the runtime scan once."""

    stopped_containers: list[DiscoveredContainer] = field(default_factory=list)
    container_images: list[DiscoveredContainerImage] = field(default_factory=list)
    stopped_containers_succeeded: bool = False
    container_images_succeeded: bool = False
    container_images_truncated: bool = False


def _merge_inventory_results(
    inventories: list[DockerInventoryResult],
) -> DockerInventoryResult:
    """Merge per-runtime supplemental inventories into one payload.

    Success flags AND across the present runtimes so a runtime whose collection
    *failed* never masquerades as covered. The combined lists are re-capped to
    the shared per-scan bounds. Cap overflow is not a failure for either list:
    neither stopped containers nor images are reaped on absence by the backend
    (image ingestion suppresses reaping via container_images_truncated), so a
    capped list is strictly better than none — and the wire payload omits
    stopped_containers entirely when the success flag is down, which would
    discard every stopped detection instead of just the overflow. This matches
    single-runtime truncation, which submits the capped list with a warning.
    """
    if not inventories:
        return DockerInventoryResult()

    stopped = [c for inv in inventories for c in inv.stopped_containers]
    images = [i for inv in inventories for i in inv.container_images]
    stopped_succeeded = all(inv.stopped_containers_succeeded for inv in inventories)
    images_succeeded = all(inv.container_images_succeeded for inv in inventories)
    images_truncated = any(inv.container_images_truncated for inv in inventories)

    if len(stopped) > MAX_CONTAINERS:
        logger.warning(
            "Merged stopped container inventory truncated",
            max_containers=MAX_CONTAINERS,
            discovered=len(stopped),
        )
        stopped = stopped[:MAX_CONTAINERS]
    if len(images) > MAX_CONTAINER_IMAGES:
        images = images[:MAX_CONTAINER_IMAGES]
        images_truncated = True

    return DockerInventoryResult(
        stopped_containers=stopped,
        container_images=images,
        stopped_containers_succeeded=stopped_succeeded,
        container_images_succeeded=images_succeeded,
        container_images_truncated=images_truncated,
    )


def _collect_docker_inventory(
    collectors: Iterable[DockerCliCollector | DockerSocketCollector],
    *,
    started_at: float,
    running_container_count: int,
    time_budget: float | None,
    host_home: Path,
) -> DockerInventoryResult:
    """Collect non-running containers and images without affecting running reaps."""
    result = DockerInventoryResult()
    deadline = started_at + (
        time_budget
        if time_budget is not None
        else _scaled_scan_time_budget(running_container_count)
    )
    for collector in collectors:
        if not result.stopped_containers_succeeded:
            try:
                inventory = collector.discover_stopped_container_ids(deadline=deadline)
                if inventory is not None and not inventory["malformed"]:
                    if inventory["truncated"]:
                        logger.warning(
                            "Stopped container inventory truncated",
                            max_containers=MAX_CONTAINERS,
                        )
                    container_ids = inventory["container_ids"]
                    if time_budget is None:
                        deadline = started_at + _scaled_scan_time_budget(
                            running_container_count + len(container_ids)
                        )
                    if container_ids:
                        stopped_containers = collector.inspect_stopped_containers(
                            container_ids=container_ids,
                            deadline=deadline,
                            host_home=host_home,
                        )
                        if stopped_containers is not None:
                            stopped_containers = collector.collect_image_digests(
                                containers=stopped_containers,
                                deadline=deadline,
                            )
                            result.stopped_containers = stopped_containers
                            result.stopped_containers_succeeded = True
                    elif inventory["output_empty"]:
                        result.stopped_containers_succeeded = True
            except Exception as exc:
                logger.warning(
                    "Stopped container inventory failed",
                    error_type=type(exc).__name__,
                    exc_info=True,
                )

        if not result.container_images_succeeded:
            try:
                image_inventory = collector.list_container_images(deadline=deadline)
                if image_inventory is not None:
                    result.container_images = image_inventory["images"]
                    result.container_images_truncated = image_inventory["truncated"]
                    result.container_images_succeeded = True
            except Exception as exc:
                logger.warning(
                    "Container image inventory failed",
                    error_type=type(exc).__name__,
                    exc_info=True,
                )

        if result.stopped_containers_succeeded and result.container_images_succeeded:
            break
    return result


def _iter_available_k3s_collectors(
    *,
    operation_timeout: float,
) -> Iterator[ContainerRuntimeCollector]:
    crictl = _find_k3s_crictl()
    if crictl is not None:
        yield K3sCrictlCollector(
            crictl,
            operation_timeout=operation_timeout,
        )


def _merge_scan_results(
    results: list[ContainerScanResult],
    *,
    docker_inventory: DockerInventoryResult | None = None,
) -> ContainerScanResult:
    """Merge ordered collector results, keeping the first copy of each container.

    The shared ``MAX_CONTAINERS`` budget (the backend rejects any scan whose
    container list exceeds it) is filled round-robin across results, so a runtime
    that discovers many containers (e.g. Docker) can't consume the whole cap and
    starve a distinct runtime merged after it (e.g. k3s). Within a result the
    original container order is preserved.

    ``scan_succeeded`` requires every input to have succeeded *and* the cap to
    not have discarded a running container. Each runtime is already capped to
    ``MAX_CONTAINERS`` at discovery (over-cap ⇒ truncated ⇒ scan_succeeded=False
    there), so a single result never both overflows and reports success. Two
    distinct runtimes can each be complete yet exceed the cap combined; the
    round-robin then drops the overflow. Those drops are silent, but the merged
    inventory is authoritative — the backend reaps any previously-seen container
    absent from a successful scan — so a cap-truncated merge must report
    scan_succeeded=False rather than reap the dropped-but-running containers.
    Cross-runtime duplicate container_ids are different: they dedupe to a
    distinct count that still fits, lose no running container, and stay
    authoritative. Failing any one runtime freezes reaping for all merged
    containers, which is the safe direction (never a false reap).

    That freeze relies on the caller: a runtime that is present but could not be
    enumerated must appear here as a failed ``ContainerScanResult`` rather than
    be omitted (``_scan_runtime`` guarantees this). An omitted runtime is
    indistinguishable from an absent one, so the merge would report success over
    a partial inventory and reap the missing runtime's still-running containers.
    """
    containers: list[DiscoveredContainer] = []
    configurations: list[MCPClientConfig] = []
    detected_clients: list[DetectedClient] = []
    skills: list[DiscoveredSkillArtifact] = []
    agent_definitions: list[DiscoveredAgentDefinition] = []
    seen_container_ids: set[str] = set()
    accepted_ids_per_result: list[set[str]] = [set() for _ in results]

    longest_result = max((len(result.containers) for result in results), default=0)
    for index in range(longest_result):
        if len(containers) >= MAX_CONTAINERS:
            break
        for result, accepted_ids in zip(results, accepted_ids_per_result):
            if len(containers) >= MAX_CONTAINERS:
                break
            if index >= len(result.containers):
                continue
            container = result.containers[index]
            if container.container_id in seen_container_ids:
                continue
            seen_container_ids.add(container.container_id)
            accepted_ids.add(container.container_id)
            containers.append(container)

    for result, accepted_ids in zip(results, accepted_ids_per_result):
        configurations.extend(
            configuration
            for configuration in result.configurations
            if configuration.container_id in accepted_ids
        )
        skills.extend(
            skill for skill in result.skills if skill.container_id in accepted_ids
        )
        agent_definitions.extend(
            definition
            for definition in result.agent_definitions
            if definition.container_id in accepted_ids
        )
        detected_clients.extend(
            detected
            for detected in result.detected_clients
            if set(detected.container_ids) & accepted_ids
        )

    # Distinct ids across all inputs; the round-robin keeps
    # min(len(distinct), MAX_CONTAINERS) of them. More distinct ids than the cap
    # means at least one running container was dropped to fit — a cap-truncation,
    # not a harmless dedup — so the merge is not authoritative.
    distinct_container_ids = {
        container.container_id for result in results for container in result.containers
    }
    cap_truncated = len(distinct_container_ids) > MAX_CONTAINERS
    supplemental = docker_inventory or DockerInventoryResult()

    return ContainerScanResult(
        containers=containers,
        stopped_containers=supplemental.stopped_containers,
        container_images=supplemental.container_images,
        configurations=configurations,
        detected_clients=coalesce_detected_clients(detected_clients),
        skills=skills,
        agent_definitions=dedupe_agent_definitions(agent_definitions),
        scan_succeeded=bool(results)
        and all(result.scan_succeeded for result in results)
        and not cap_truncated,
        stopped_containers_succeeded=supplemental.stopped_containers_succeeded,
        container_images_succeeded=supplemental.container_images_succeeded,
        container_images_truncated=supplemental.container_images_truncated,
    )


def _scan_runtime(
    collectors: Iterator[_COLLECTOR],
    *,
    clients: list[MCPClientDefinition],
    subprocess_timeout: float,
    time_budget: float | None,
    host_home: Path,
    discovered_collectors: list[_COLLECTOR] | None = None,
    started_at: float | None = None,
    detect_disguised_skills: bool = False,
) -> ContainerScanResult | None:
    """Scan one runtime's collectors, honoring transport fallback.

    Collectors are tried in order and the first usable (non-None) result wins,
    so redundant transports to the same runtime (Docker CLI then Engine-API
    socket) short-circuit at the first that works.

    The return distinguishes *absent* from *present-but-unscannable*, which the
    merge depends on to avoid false reaps:

    - No collector available (empty iterator) ⇒ the runtime is absent ⇒ ``None``.
      It contributes nothing to the merge, which stays authoritative over the
      runtimes that are present.
    - A collector was available but none produced a usable result (every
      transport's ``discover_container_ids`` returned None — a transient
      timeout / subprocess error / spent deadline) ⇒ the runtime is present but
      could not be enumerated ⇒ a failed ``ContainerScanResult()``. Returning a
      result (rather than None) is what keeps ``_merge_scan_results`` from
      treating the runtime as absent and reaping its still-running containers;
      the failed flag freezes reaping for the whole merge.

    Mirrors ``_scan_with_collector``'s own inspect-failure path, which already
    returns ``ContainerScanResult()`` for the same reason.
    """
    available = False
    for collector in collectors:
        available = True
        if discovered_collectors is not None:
            discovered_collectors.append(collector)
        result = _scan_with_collector(
            collector=collector,
            clients=clients,
            subprocess_timeout=subprocess_timeout,
            time_budget=time_budget,
            host_home=host_home,
            started_at=started_at,
            detect_disguised_skills=detect_disguised_skills,
        )
        if result is not None:
            return result
    return ContainerScanResult() if available else None


def _scan_running_containers(
    *,
    clients: list[MCPClientDefinition],
    subprocess_timeout: float,
    time_budget: float | None,
    host_home: Path,
    detect_disguised_skills: bool = False,
) -> ContainerScanResult:
    # The CLI and the Engine-API socket are two transports to the *same* Docker
    # daemon, so the first working one wins — scanning both would re-enumerate an
    # identical container set. podman, nerdctl, and k3s are distinct runtimes, so
    # each runs alongside the first working Docker transport and the results are
    # merged below.
    #
    # Each runtime is scanned via _scan_runtime, which returns None only when the
    # runtime is absent (no collector available). A runtime that is present but
    # unscannable (discovery failed on every transport) returns a failed
    # ContainerScanResult() instead of None, so the merge freezes reaping rather
    # than treating it as absent and reaping its still-running containers. This
    # holds symmetrically: Docker failing while k3s succeeds is as safe as k3s
    # failing while Docker succeeds.
    #
    # Budget is per distinct runtime by design. Every Docker operation (transport
    # fallback, running containers, stopped containers, and local images) shares
    # one scalable deadline and runs contiguously below; each other runtime
    # receives its own deadline afterward. Thus total wall-clock can scale with
    # genuinely separate container sets without giving redundant Docker
    # transports or supplemental inventory a fresh budget. One deadline across
    # runtimes is deliberately avoided so none can starve another's inventory.
    docker_started_at = time.monotonic()
    docker_collectors = _iter_available_docker_collectors(
        operation_timeout=subprocess_timeout
    )
    discovered_docker_collectors: list[DockerCliCollector | DockerSocketCollector] = []
    results: list[ContainerScanResult] = []
    inventories: list[DockerInventoryResult] = []
    docker_result = _scan_runtime(
        docker_collectors,
        clients=clients,
        subprocess_timeout=subprocess_timeout,
        time_budget=time_budget,
        host_home=host_home,
        discovered_collectors=discovered_docker_collectors,
        started_at=docker_started_at,
        detect_disguised_skills=detect_disguised_skills,
    )
    if docker_result is not None:
        results.append(docker_result)
        inventories.append(
            _collect_docker_inventory(
                chain(discovered_docker_collectors, docker_collectors),
                started_at=docker_started_at,
                running_container_count=len(docker_result.containers),
                time_budget=time_budget,
                host_home=host_home,
            )
        )

    for runtime_name in _DISTINCT_CLI_RUNTIMES:
        runtime_started_at = time.monotonic()
        runtime_collectors = _iter_available_cli_runtime_collectors(
            runtime_name,
            operation_timeout=subprocess_timeout,
        )
        discovered_runtime_collectors: list[DockerCliCollector] = []
        runtime_result = _scan_runtime(
            runtime_collectors,
            clients=clients,
            subprocess_timeout=subprocess_timeout,
            time_budget=time_budget,
            host_home=host_home,
            discovered_collectors=discovered_runtime_collectors,
            started_at=runtime_started_at,
            detect_disguised_skills=detect_disguised_skills,
        )
        if runtime_result is None:
            continue
        results.append(runtime_result)
        inventories.append(
            _collect_docker_inventory(
                chain(discovered_runtime_collectors, runtime_collectors),
                started_at=runtime_started_at,
                running_container_count=len(runtime_result.containers),
                time_budget=time_budget,
                host_home=host_home,
            )
        )

    k3s_result = _scan_runtime(
        _iter_available_k3s_collectors(operation_timeout=subprocess_timeout),
        clients=clients,
        subprocess_timeout=subprocess_timeout,
        time_budget=time_budget,
        host_home=host_home,
        detect_disguised_skills=detect_disguised_skills,
    )
    if k3s_result is not None:
        results.append(k3s_result)

    return _merge_scan_results(
        results,
        docker_inventory=_merge_inventory_results(inventories),
    )


def scan_running_containers(
    *,
    clients: list[MCPClientDefinition] | None = None,
    subprocess_timeout: float = SUBPROCESS_TIMEOUT_S,
    time_budget: float | None = None,
    host_home: Path | None = None,
    detect_disguised_skills: bool = False,
) -> ContainerScanResult:
    """Discover running containers and their known configs, skills, and agents.

    Missing binaries, denied daemons, malformed output, and any unexpected
    scanner failure are non-fatal by contract.
    """
    try:
        return _scan_running_containers(
            clients=clients if clients is not None else get_all_clients(),
            subprocess_timeout=subprocess_timeout,
            time_budget=time_budget,
            host_home=host_home or Path.home(),
            detect_disguised_skills=detect_disguised_skills,
        )
    except Exception as exc:
        logger.warning(
            "Container scan failed",
            error_type=type(exc).__name__,
            exc_info=True,
        )
        return ContainerScanResult()
