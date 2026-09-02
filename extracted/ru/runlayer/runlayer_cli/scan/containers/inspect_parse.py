"""Docker inventory parsing and container path metadata."""

from __future__ import annotations

import json
import os
import posixpath
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypedDict, cast

from runlayer_cli import regex_safe
from runlayer_cli.scan.agent_definition_scanner import DiscoveredAgentDefinition
from runlayer_cli.scan.client_presence import DetectedClient
from runlayer_cli.scan.config_parser import MCPClientConfig
from runlayer_cli.scan.project_tree_match import (
    _posix_path_within as _container_path_within,
)
from runlayer_cli.scan.skill_scanner import DiscoveredSkillArtifact

# Cross-service cap: the backend mirrors this as MAX_CONTAINERS_PER_SCAN;
# test_container_cap_contract.py enforces equality. Change both together.
MAX_CONTAINERS = 64
# Cross-service cap: the backend mirrors this as MAX_CONTAINER_IMAGES_PER_SCAN.
MAX_CONTAINER_IMAGES = 256
# Cross-service label bounds: these character/count caps are the wire storage
# contract. The backend re-applies them on ingestion; the shared golden fixture
# separately guards case-folding and priority precedence. Change both sides.
MAX_LABELS = 100
MAX_LABEL_KEY_CHARS = 256
MAX_LABEL_VALUE_CHARS = 2048
MAX_ENTRYPOINT_ITEMS = 32
MAX_ENTRYPOINT_ITEM_CHARS = 1024
MAX_IMAGE_CONFIG_METADATA_CHARS = 4 * 1024 * 1024
PRIORITY_IMAGE_LABEL_KEYS = (
    "io.modelcontextprotocol.server.name",
    "org.opencontainers.image.source",
    "org.opencontainers.image.title",
)
_ENV_VAR_RE = regex_safe.compile(
    r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))"
)


@dataclass(frozen=True)
class ContainerMount:
    """One bind/volume mount from Docker inspect."""

    mount_type: str
    source: str
    destination: str


@dataclass
class DiscoveredContainer:
    """Running container inventory item plus scan-only path metadata."""

    container_id: str
    name: str | None
    image_ref: str | None
    image_digest: str | None
    runtime: str = "docker"
    is_devcontainer: bool = False
    is_running: bool = True
    labels: dict[str, str] = field(default_factory=dict)
    mounts_host_home: bool = False
    has_mcp_configs: bool = False
    has_ai_agents: bool = False
    home: str = field(default="/root", repr=False)
    working_dir: str | None = field(default=None, repr=False)
    environment: dict[str, str] = field(default_factory=dict, repr=False)
    mounts: list[ContainerMount] = field(default_factory=list, repr=False)
    image_id: str | None = field(default=None, repr=False, compare=False)
    pid: int | None = field(default=None, repr=False, compare=False)
    wsl_distro: str | None = None

    def to_api_payload(self) -> dict[str, Any]:
        """Return the bounded inventory shape sent with the scan."""
        payload = {
            "container_id": self.container_id,
            "name": self.name,
            "image_ref": self.image_ref,
            "image_digest": self.image_digest,
            "runtime": self.runtime,
            "is_devcontainer": self.is_devcontainer,
            "is_running": self.is_running,
            "labels": self.labels,
            "mounts_host_home": self.mounts_host_home,
            "has_mcp_configs": self.has_mcp_configs,
            "has_ai_agents": self.has_ai_agents,
        }
        if self.wsl_distro is not None:
            payload["wsl_distro"] = self.wsl_distro
        return payload


@dataclass
class DiscoveredContainerImage:
    """One tagged or digest-addressed image in the local Docker inventory."""

    repository: str
    tag: str | None
    digest: str | None
    labels: dict[str, str] = field(default_factory=dict)
    entrypoint: list[str] = field(default_factory=list)
    image_id: str | None = field(default=None, repr=False, compare=False)
    labels_collected: bool = field(default=False, repr=False, compare=False)
    entrypoint_collected: bool = field(default=False, repr=False, compare=False)

    def to_api_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "repository": self.repository,
            "tag": self.tag,
            "digest": self.digest,
        }
        if self.labels_collected or self.labels:
            payload["labels"] = self.labels
        if self.entrypoint_collected or self.entrypoint:
            payload["entrypoint"] = self.entrypoint
        return payload


@dataclass
class ContainerScanResult:
    """Container inventory and artifacts found inside it."""

    containers: list[DiscoveredContainer] = field(default_factory=list)
    stopped_containers: list[DiscoveredContainer] = field(default_factory=list)
    container_images: list[DiscoveredContainerImage] = field(default_factory=list)
    configurations: list[MCPClientConfig] = field(default_factory=list)
    detected_clients: list[DetectedClient] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)
    scan_succeeded: bool = False
    stopped_containers_succeeded: bool = False
    container_images_succeeded: bool = False
    # A truncated image list is not an authoritative snapshot: the backend must
    # not reap absent rows from it, so the flag travels with the payload.
    container_images_truncated: bool = False


class ContainerImageInventory(TypedDict):
    images: list[DiscoveredContainerImage]
    truncated: bool


class DockerPSInventory(TypedDict):
    container_ids: list[str]
    truncated: bool
    malformed: bool
    output_empty: bool


class ImageConfigMetadata(TypedDict, total=False):
    labels: dict[str, str]
    entrypoint: list[str]


def _parse_docker_ps_inventory(text: str) -> DockerPSInventory:
    container_ids: list[str] = []
    seen: set[str] = set()
    truncated = False
    malformed = False
    for line in text.splitlines():
        try:
            row = json.loads(line)
        except (TypeError, ValueError):
            malformed = True
            continue
        if not isinstance(row, dict):
            malformed = True
            continue
        container_id = row.get("ID") or row.get("Id")
        if (
            not isinstance(container_id, str)
            or not container_id
            or container_id in seen
        ):
            malformed = True
            continue
        if len(container_ids) >= MAX_CONTAINERS:
            truncated = True
            break
        seen.add(container_id)
        container_ids.append(container_id)
    return {
        "container_ids": container_ids,
        "truncated": truncated,
        "malformed": malformed,
        "output_empty": not bool(text.strip()),
    }


def _parse_docker_engine_inventory(text: str) -> DockerPSInventory:
    """Parse the Engine API ``/containers/json`` response."""
    try:
        rows = json.loads(text)
    except (TypeError, ValueError):
        rows = None
    if not isinstance(rows, list):
        return {
            "container_ids": [],
            "truncated": False,
            "malformed": True,
            "output_empty": False,
        }

    container_ids: list[str] = []
    seen: set[str] = set()
    truncated = False
    malformed = False
    for row in rows:
        if not isinstance(row, dict):
            malformed = True
            continue
        container_id = row.get("Id")
        if (
            not isinstance(container_id, str)
            or not container_id
            or container_id in seen
        ):
            malformed = True
            continue
        if len(container_ids) >= MAX_CONTAINERS:
            truncated = True
            break
        seen.add(container_id)
        container_ids.append(container_id)
    return {
        "container_ids": container_ids,
        "truncated": truncated,
        "malformed": malformed,
        "output_empty": not rows,
    }


def parse_image_digests(text: str) -> dict[str, str]:
    """Map Docker image IDs to repository/content digests."""
    try:
        rows = json.loads(text)
    except (TypeError, ValueError):
        return {}
    if isinstance(rows, dict):
        rows = [rows]
    if not isinstance(rows, list):
        return {}

    digests: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        image_id = row.get("Id")
        if not isinstance(image_id, str) or not image_id:
            continue
        repo_digests = row.get("RepoDigests")
        if isinstance(repo_digests, list):
            for repo_digest in repo_digests:
                if isinstance(repo_digest, str) and "@sha256:" in repo_digest:
                    digests[image_id] = repo_digest.rsplit("@", 1)[1]
                    break
        if image_id not in digests and image_id.startswith("sha256:"):
            digests[image_id] = image_id
    return digests


def _bounded_entrypoint(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    entrypoint: list[str] = []
    for item in value:
        if len(entrypoint) >= MAX_ENTRYPOINT_ITEMS:
            break
        if isinstance(item, str) and item:
            entrypoint.append(item[:MAX_ENTRYPOINT_ITEM_CHARS])
    return entrypoint


def parse_image_config_metadata(
    text: str,
    *,
    max_metadata_chars: int | None = None,
) -> dict[str, ImageConfigMetadata]:
    """Parse bounded OCI config signals keyed by immutable image id."""
    if max_metadata_chars is None:
        max_metadata_chars = MAX_IMAGE_CONFIG_METADATA_CHARS
    try:
        rows = json.loads(text)
    except (TypeError, ValueError):
        return {}
    if isinstance(rows, dict):
        rows = [rows]
    if not isinstance(rows, list):
        return {}
    metadata: dict[str, ImageConfigMetadata] = {}
    metadata_chars = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        image_id = row.get("Id")
        config = row.get("Config")
        if (
            not isinstance(image_id, str)
            or not image_id
            or not isinstance(config, dict)
        ):
            continue
        config_row = cast(dict[str, object], config)
        item: ImageConfigMetadata = {}
        labels_value = config_row.get("Labels")
        if "Labels" in config_row and (
            labels_value is None or isinstance(labels_value, dict)
        ):
            labels = _bounded_labels(labels_value)
            label_chars = sum(len(key) + len(value) for key, value in labels.items())
            if metadata_chars + label_chars <= max_metadata_chars:
                metadata_chars += label_chars
                item["labels"] = labels
        entrypoint_value = config_row.get("Entrypoint")
        if "Entrypoint" in config_row and (
            entrypoint_value is None or isinstance(entrypoint_value, list)
        ):
            entrypoint = _bounded_entrypoint(entrypoint_value)
            entrypoint_chars = sum(len(value) for value in entrypoint)
            if metadata_chars + entrypoint_chars <= max_metadata_chars:
                metadata_chars += entrypoint_chars
                item["entrypoint"] = entrypoint
        if item:
            metadata[image_id] = item
    return metadata


def bound_image_inventory_metadata(
    images: list[DiscoveredContainerImage],
) -> None:
    """Keep repeated tag aliases inside the scan-wide wire metadata cap."""
    metadata_chars = 0
    for image in images:
        if image.labels_collected:
            label_chars = sum(
                len(key) + len(value) for key, value in image.labels.items()
            )
            if metadata_chars + label_chars <= MAX_IMAGE_CONFIG_METADATA_CHARS:
                metadata_chars += label_chars
            else:
                image.labels = {}
                image.labels_collected = False
        if image.entrypoint_collected:
            entrypoint_chars = sum(len(item) for item in image.entrypoint)
            if metadata_chars + entrypoint_chars <= MAX_IMAGE_CONFIG_METADATA_CHARS:
                metadata_chars += entrypoint_chars
            else:
                image.entrypoint = []
                image.entrypoint_collected = False


def _optional_image_value(value: object, *, max_chars: int) -> str | None:
    if not isinstance(value, str) or not value or value == "<none>":
        return None
    return value[:max_chars]


def _split_repo_tag(image_ref: str) -> tuple[str, str | None]:
    repository, separator, tag = image_ref.rpartition(":")
    if separator and "/" not in tag:
        return repository, tag or None
    return image_ref, None


def parse_docker_image_ls(text: str) -> ContainerImageInventory | None:
    """Parse bounded ``docker image ls --format '{{json .}}'`` output."""
    images: list[DiscoveredContainerImage] = []
    seen: set[tuple[str, str | None, str | None]] = set()
    truncated = False
    for line in text.splitlines():
        try:
            row = json.loads(line)
        except (TypeError, ValueError):
            return None
        if not isinstance(row, dict):
            return None
        raw_repository = row.get("Repository")
        repository = _optional_image_value(raw_repository, max_chars=512)
        if repository is None:
            if raw_repository == "<none>":
                continue
            return None
        tag = _optional_image_value(row.get("Tag"), max_chars=255)
        digest = _optional_image_value(row.get("Digest"), max_chars=140)
        image_id = _optional_image_value(row.get("ID"), max_chars=140)
        if digest is None and image_id is not None and image_id.startswith("sha256:"):
            digest = image_id
        key = (repository, tag, digest)
        if key in seen:
            continue
        if len(images) >= MAX_CONTAINER_IMAGES:
            truncated = True
            break
        seen.add(key)
        images.append(
            DiscoveredContainerImage(
                repository=repository,
                tag=tag,
                digest=digest,
                image_id=image_id,
            )
        )
    return {"images": images, "truncated": truncated}


def parse_docker_engine_images(text: str) -> ContainerImageInventory | None:
    """Parse Engine API image summaries into repository identities."""
    try:
        rows = json.loads(text)
    except (TypeError, ValueError):
        return None
    if not isinstance(rows, list):
        return None

    images: list[DiscoveredContainerImage] = []
    seen: set[tuple[str, str | None, str | None]] = set()
    for row in rows:
        if not isinstance(row, dict):
            return None
        raw_image_id = row.get("Id")
        image_id = (
            raw_image_id
            if isinstance(raw_image_id, str) and raw_image_id.startswith("sha256:")
            else None
        )
        repo_digests = row.get("RepoDigests")
        digests_by_repository: dict[str, str] = {}
        if repo_digests is not None and not isinstance(repo_digests, list):
            return None
        if isinstance(repo_digests, list):
            for repo_digest in repo_digests:
                if not isinstance(repo_digest, str) or "@" not in repo_digest:
                    return None
                repository, digest = repo_digest.rsplit("@", 1)
                if not repository or not digest:
                    return None
                if repository != "<none>" and digest != "<none>":
                    digests_by_repository[repository] = digest

        repo_tags = row.get("RepoTags")
        if repo_tags is not None and not isinstance(repo_tags, list):
            return None
        references = repo_tags if isinstance(repo_tags, list) else []
        parsed_references: list[tuple[str, str | None]] = []
        for reference in references:
            if not isinstance(reference, str):
                return None
            if reference == "<none>:<none>":
                continue
            repository, tag = _split_repo_tag(reference)
            if not repository:
                return None
            parsed_references.append((repository, tag))
        if not parsed_references:
            parsed_references = [
                (repository, None) for repository in digests_by_repository
            ]

        for repository, tag in parsed_references:
            normalized_repository = repository[:512]
            normalized_tag = tag[:255] if tag else None
            digest = digests_by_repository.get(repository) or image_id
            normalized_digest = digest[:140] if digest else None
            key = (normalized_repository, normalized_tag, normalized_digest)
            if not normalized_repository or key in seen:
                continue
            if len(images) >= MAX_CONTAINER_IMAGES:
                bound_image_inventory_metadata(images)
                return {"images": images, "truncated": True}
            seen.add(key)
            labels_value = row.get("Labels")
            labels_collected = "Labels" in row and (
                labels_value is None or isinstance(labels_value, dict)
            )
            images.append(
                DiscoveredContainerImage(
                    repository=normalized_repository,
                    tag=normalized_tag,
                    digest=normalized_digest,
                    labels=(_bounded_labels(labels_value) if labels_collected else {}),
                    image_id=image_id,
                    labels_collected=labels_collected,
                )
            )
    bound_image_inventory_metadata(images)
    return {"images": images, "truncated": False}


def _environment(values: object) -> dict[str, str]:
    result: dict[str, str] = {}
    if not isinstance(values, list):
        return result
    for item in values:
        if not isinstance(item, str) or "=" not in item:
            continue
        key, value = item.split("=", 1)
        if key:
            result[key] = value
    return result


def _container_home(environment: dict[str, str], user: object) -> str:
    home = environment.get("HOME")
    if home and home.startswith("/"):
        return posixpath.normpath(home)
    username = str(user or "").split(":", 1)[0]
    if not username or username in {"0", "root"}:
        return "/root"
    return posixpath.normpath(f"/home/{username}")


def _bounded_labels(value: object) -> dict[str, str]:
    labels: dict[str, str] = {}
    if not isinstance(value, dict):
        return labels
    label_rows = cast(dict[object, object], value)
    priority_keys = frozenset(PRIORITY_IMAGE_LABEL_KEYS)
    folded_rows = {
        key.casefold(): label_value
        for key, label_value in label_rows.items()
        if isinstance(key, str) and isinstance(label_value, str)
    }
    for key in PRIORITY_IMAGE_LABEL_KEYS:
        label_value = label_rows.get(key)
        if not isinstance(label_value, str):
            label_value = folded_rows.get(key)
        if isinstance(label_value, str):
            labels[key] = label_value[:MAX_LABEL_VALUE_CHARS]
    for key, label_value in label_rows.items():
        if len(labels) >= MAX_LABELS:
            break
        if (
            isinstance(key, str)
            and key.casefold() not in priority_keys
            and isinstance(label_value, str)
        ):
            labels[key[:MAX_LABEL_KEY_CHARS]] = label_value[:MAX_LABEL_VALUE_CHARS]
    return labels


def _mounts(value: object) -> list[ContainerMount]:
    mounts: list[ContainerMount] = []
    if not isinstance(value, list):
        return mounts
    for item in value:
        if not isinstance(item, dict):
            continue
        mount_item = cast(dict[str, object], item)
        mount_type = mount_item.get("Type")
        source = mount_item.get("Source")
        destination = mount_item.get("Destination")
        if not (
            isinstance(mount_type, str)
            and isinstance(source, str)
            and isinstance(destination, str)
        ):
            continue
        mounts.append(
            ContainerMount(
                mount_type=mount_type,
                source=source,
                destination=posixpath.normpath(destination),
            )
        )
    return mounts


def _host_path_within(path: str, root: str) -> bool:
    normalized_path = os.path.normpath(path)
    normalized_root = os.path.normpath(root)
    return normalized_path == normalized_root or normalized_path.startswith(
        normalized_root.rstrip(os.sep) + os.sep
    )


def _mounts_host_home(mounts: list[ContainerMount], host_home: Path) -> bool:
    home = os.path.normpath(str(host_home))
    return any(
        mount.mount_type == "bind"
        and (
            _host_path_within(mount.source, home)
            or _host_path_within(home, mount.source)
        )
        for mount in mounts
    )


def path_is_shared_with_host_home(
    container_path: str,
    mounts: list[ContainerMount],
    host_home: Path,
) -> bool:
    """Whether a container path maps to a source inside the scanning home."""
    home = os.path.normpath(str(host_home))
    for mount in mounts:
        if mount.mount_type != "bind" or not _container_path_within(
            container_path, mount.destination
        ):
            continue
        relative = posixpath.relpath(container_path, mount.destination)
        source_path = os.path.normpath(os.path.join(mount.source, *relative.split("/")))
        if _host_path_within(source_path, home):
            return True
    return False


def parse_container_inspect(
    rows: list[object],
    *,
    host_home: Path | None = None,
    running_only: bool = True,
) -> list[DiscoveredContainer]:
    """Parse ``docker inspect`` rows into bounded inventory records.

    Repository digests are enriched afterwards by ``_collect_image_digests``;
    here only the ``sha256:`` image-id fallback applies.
    """
    resolved_host_home = host_home or Path.home()
    containers: list[DiscoveredContainer] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        inspect_row = cast(dict[str, object], row)
        container_id = inspect_row.get("Id")
        config = inspect_row.get("Config")
        state = inspect_row.get("State")
        if not isinstance(container_id, str) or not isinstance(config, dict):
            continue
        config_row = cast(dict[str, object], config)
        state_row = cast(dict[str, object], state) if isinstance(state, dict) else {}
        is_running = (
            state_row.get("Running") is not False or state_row.get("Restarting") is True
        )
        if running_only and not is_running:
            continue

        environment = _environment(config_row.get("Env"))
        mounts = _mounts(inspect_row.get("Mounts"))
        labels = _bounded_labels(config_row.get("Labels"))
        image_id = inspect_row.get("Image")
        image_ref = config_row.get("Image")
        name = inspect_row.get("Name")
        working_dir = config_row.get("WorkingDir")
        image_digest = (
            image_id
            if isinstance(image_id, str) and image_id.startswith("sha256:")
            else None
        )

        containers.append(
            DiscoveredContainer(
                container_id=container_id[:255],
                name=name.lstrip("/")[:255] if isinstance(name, str) else None,
                image_ref=image_ref[:512] if isinstance(image_ref, str) else None,
                image_digest=(
                    image_digest[:140] if isinstance(image_digest, str) else None
                ),
                is_devcontainer=any(key.startswith("devcontainer.") for key in labels),
                is_running=is_running,
                labels=labels,
                mounts_host_home=_mounts_host_home(mounts, resolved_host_home),
                home=_container_home(environment, config_row.get("User")),
                working_dir=(
                    posixpath.normpath(working_dir)
                    if isinstance(working_dir, str) and working_dir.startswith("/")
                    else None
                ),
                environment=environment,
                mounts=mounts,
                image_id=image_id if isinstance(image_id, str) else None,
            )
        )
        if len(containers) >= MAX_CONTAINERS:
            break
    return containers


def parse_complete_inspect_inventory(
    rows: list[object],
    *,
    container_ids: list[str],
    host_home: Path | None,
    running: bool,
) -> list[DiscoveredContainer] | None:
    """Parse inspect rows that must cover exactly the discovered inventory.

    Fails closed (None) unless the parsed containers in the requested state
    match ``container_ids`` one-to-one, so a partially answered inspect never
    masquerades as a complete snapshot. Shared by the Docker CLI and Engine
    API collectors.
    """
    parsed = parse_container_inspect(
        rows,
        host_home=host_home,
        running_only=running,
    )
    containers = (
        parsed
        if running
        else [container for container in parsed if not container.is_running]
    )
    if len(containers) != len(container_ids) or {
        container.container_id for container in containers
    } != set(container_ids):
        return None
    return containers


def _expand_container_path(
    template: str,
    *,
    home: str,
    environment: dict[str, str],
) -> str | None:
    path = template
    if path == "~":
        path = home
    elif path.startswith("~/"):
        path = posixpath.join(home, path[2:])

    unresolved = False

    def _replace_env(match: regex_safe.Match) -> str:
        nonlocal unresolved
        key = match.group(1) or match.group(2)
        value = environment.get(key)
        if value is None:
            unresolved = True
            return match.group(0)
        return value

    path = _ENV_VAR_RE.sub(_replace_env, path)
    if unresolved or not path.startswith("/"):
        return None
    return posixpath.normpath(path)
