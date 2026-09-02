"""Bounded k3s/crictl discovery and inventory parsing."""

from __future__ import annotations

import json
import os
import platform
import posixpath
import shutil
from pathlib import Path
from typing import cast

from runlayer_cli.scan.containers.docker_cli import (
    MAX_INSPECT_BYTES,
    MAX_PS_BYTES,
    _remaining_timeout,
    _run_text,
)
from runlayer_cli.scan.containers.inspect_parse import (
    MAX_CONTAINERS,
    ContainerMount,
    DiscoveredContainer,
    DockerPSInventory,
    _bounded_labels,
    _container_home,
    _mounts_host_home,
)

K3S_CONTAINERD_ENDPOINT = "unix:///run/k3s/containerd/containerd.sock"
K3S_CONFIG_DIR = Path("/etc/rancher/k3s")
K3S_FALLBACK_BINARY = Path("/usr/local/bin/k3s")
INCLUDE_KUBE_SYSTEM_ENV = "RUNLAYER_CONTAINERS_INCLUDE_KUBE_SYSTEM"

_KUBERNETES_CONTAINER_NAME = "io.kubernetes.container.name"
_KUBERNETES_POD_NAME = "io.kubernetes.pod.name"
_KUBERNETES_POD_NAMESPACE = "io.kubernetes.pod.namespace"
_NORMALIZED_KUBERNETES_LABELS = (
    _KUBERNETES_POD_NAME,
    _KUBERNETES_POD_NAMESPACE,
    _KUBERNETES_CONTAINER_NAME,
)
_TRUTHY = {"1", "true", "yes", "on"}

CrictlCommand = tuple[str, ...]


def _find_k3s_crictl() -> CrictlCommand | None:
    """Resolve a root-only k3s CRI command on Linux."""
    if platform.system() != "Linux" or getattr(os, "geteuid", lambda: -1)() != 0:
        return None

    k3s = shutil.which("k3s")
    if (
        k3s is None
        and K3S_FALLBACK_BINARY.is_file()
        and os.access(K3S_FALLBACK_BINARY, os.X_OK)
    ):
        k3s = str(K3S_FALLBACK_BINARY)
    if k3s is not None:
        return (k3s, "crictl")

    crictl = shutil.which("crictl")
    if crictl is not None and K3S_CONFIG_DIR.is_dir():
        return (crictl, "--runtime-endpoint", K3S_CONTAINERD_ENDPOINT)
    return None


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        return {}
    return cast(dict[str, object], value)


def _is_running(value: object) -> bool:
    return (isinstance(value, str) and value in {"CONTAINER_RUNNING", "RUNNING"}) or (
        isinstance(value, int) and not isinstance(value, bool) and value == 1
    )


def _include_kube_system() -> bool:
    return os.environ.get(INCLUDE_KUBE_SYSTEM_ENV, "").strip().lower() in _TRUTHY


def _kubernetes_metadata_value(row: dict[str, object], key: str) -> str | None:
    for field in ("labels", "annotations"):
        value = _mapping(row.get(field)).get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _parse_crictl_ps_inventory(
    text: str,
    *,
    include_kube_system: bool | None = None,
) -> DockerPSInventory:
    """Parse the stable CRI ``ListContainersResponse`` fields."""
    try:
        payload = json.loads(text)
    except (TypeError, ValueError):
        payload = None
    if not isinstance(payload, dict):
        return {
            "container_ids": [],
            "truncated": False,
            "malformed": True,
            "output_empty": False,
        }

    rows = payload.get("containers")
    if not isinstance(rows, list):
        return {
            "container_ids": [],
            "truncated": False,
            "malformed": True,
            "output_empty": False,
        }

    include_system = (
        _include_kube_system() if include_kube_system is None else include_kube_system
    )
    container_ids: list[str] = []
    seen: set[str] = set()
    truncated = False
    malformed = False
    for value in rows:
        if not isinstance(value, dict):
            malformed = True
            continue
        row = cast(dict[str, object], value)
        if not _is_running(row.get("state")):
            continue

        container_name = _kubernetes_metadata_value(row, _KUBERNETES_CONTAINER_NAME)
        if not container_name or container_name == "POD":
            continue
        namespace = _kubernetes_metadata_value(row, _KUBERNETES_POD_NAMESPACE)
        if (
            not include_system
            and namespace is not None
            and namespace.startswith("kube-")
        ):
            continue

        container_id = row.get("id")
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
        "output_empty": not container_ids,
    }


def _discover_container_ids(
    *,
    crictl: CrictlCommand,
    deadline: float,
    subprocess_timeout: float,
) -> DockerPSInventory | None:
    timeout = _remaining_timeout(deadline, subprocess_timeout)
    if timeout is None:
        return None
    output = _run_text(
        [*crictl, "ps", "-o", "json"],
        timeout=timeout,
        max_output=MAX_PS_BYTES,
    )
    if output is None:
        return None
    return _parse_crictl_ps_inventory(output)


def _environment_from_cri(
    value: object,
    *,
    runtime_environment: object = None,
) -> dict[str, str]:
    environment: dict[str, str] = {}
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                env = cast(dict[str, object], item)
                key = env.get("key")
                env_value = env.get("value")
                if isinstance(key, str) and key and isinstance(env_value, str):
                    environment[key] = env_value
            elif isinstance(item, str) and "=" in item:
                key, env_value = item.split("=", 1)
                if key:
                    environment[key] = env_value
    if not environment and isinstance(runtime_environment, list):
        for item in runtime_environment:
            if isinstance(item, str) and "=" in item:
                key, env_value = item.split("=", 1)
                if key:
                    environment[key] = env_value
    return environment


def _mounts_from_cri(value: object) -> list[ContainerMount]:
    mounts: list[ContainerMount] = []
    if not isinstance(value, list):
        return mounts
    for item in value:
        mount = _mapping(item)
        source = mount.get("hostPath") or mount.get("host_path")
        destination = mount.get("containerPath") or mount.get("container_path")
        if (
            not isinstance(source, str)
            or not source
            or not isinstance(destination, str)
            or not destination.startswith("/")
        ):
            continue
        mounts.append(
            ContainerMount(
                mount_type="bind",
                source=source,
                destination=posixpath.normpath(destination),
            )
        )
    return mounts


def _normalized_labels(
    *,
    status: dict[str, object],
    config: dict[str, object],
    runtime_spec: dict[str, object],
) -> dict[str, str]:
    status_labels = _mapping(status.get("labels"))
    sources = (
        status_labels,
        _mapping(status.get("annotations")),
        _mapping(config.get("labels")),
        _mapping(config.get("annotations")),
        _mapping(runtime_spec.get("annotations")),
    )
    combined: dict[str, str] = {}
    for key in _NORMALIZED_KUBERNETES_LABELS:
        for source in sources:
            value = source.get(key)
            if isinstance(value, str):
                combined[key] = value
                break
    for key, value in status_labels.items():
        if isinstance(key, str) and isinstance(value, str) and key not in combined:
            combined[key] = value
    return _bounded_labels(combined)


def _positive_pid(value: object) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool) and value > 0:
        return value
    if isinstance(value, str) and value.isdecimal() and len(value) <= 20:
        parsed = int(value)
        if parsed > 0:
            return parsed
    return None


def _digest_from_reference(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    digest = value.rsplit("@", 1)[-1] if "@sha256:" in value else value
    if digest.startswith("sha256:"):
        return digest[:140]
    return None


def _parse_crictl_inspect(
    text: str,
    *,
    host_home: Path,
) -> DiscoveredContainer | None:
    """Normalize one verbose CRI container status response."""
    try:
        payload = json.loads(text)
    except (TypeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None

    status = _mapping(payload.get("status"))
    info = _mapping(payload.get("info"))
    config = _mapping(info.get("config"))
    runtime_spec = _mapping(info.get("runtimeSpec"))
    process = _mapping(runtime_spec.get("process"))
    container_id = status.get("id")
    pid = _positive_pid(info.get("pid"))
    if (
        not isinstance(container_id, str)
        or not container_id
        or pid is None
        or not _is_running(status.get("state"))
    ):
        return None

    environment = _environment_from_cri(
        config.get("envs"),
        runtime_environment=process.get("env"),
    )
    mounts = _mounts_from_cri(status.get("mounts"))
    if not mounts:
        mounts = _mounts_from_cri(config.get("mounts"))
    labels = _normalized_labels(
        status=status,
        config=config,
        runtime_spec=runtime_spec,
    )
    metadata = _mapping(status.get("metadata"))
    image = _mapping(status.get("image"))
    name = metadata.get("name")
    if not isinstance(name, str):
        name = labels.get(_KUBERNETES_CONTAINER_NAME)
    image_ref = image.get("image")
    runtime_image_ref = status.get("imageRef")
    working_dir = config.get("working_dir") or config.get("workingDir")
    if not isinstance(working_dir, str):
        working_dir = process.get("cwd")

    return DiscoveredContainer(
        container_id=container_id[:255],
        name=name[:255] if isinstance(name, str) else None,
        image_ref=image_ref[:512] if isinstance(image_ref, str) else None,
        image_digest=_digest_from_reference(runtime_image_ref),
        runtime="k3s",
        is_devcontainer=any(key.startswith("devcontainer.") for key in labels),
        labels=labels,
        mounts_host_home=_mounts_host_home(mounts, host_home),
        home=_container_home(environment, None),
        working_dir=(
            posixpath.normpath(working_dir)
            if isinstance(working_dir, str) and working_dir.startswith("/")
            else None
        ),
        environment=environment,
        mounts=mounts,
        image_id=(
            runtime_image_ref
            if isinstance(runtime_image_ref, str) and runtime_image_ref
            else image_ref
            if isinstance(image_ref, str)
            else None
        ),
        pid=pid,
    )


def _inspect_containers(
    *,
    crictl: CrictlCommand,
    container_ids: list[str],
    deadline: float,
    subprocess_timeout: float,
    host_home: Path,
) -> list[DiscoveredContainer] | None:
    containers: list[DiscoveredContainer] = []
    for container_id in container_ids:
        timeout = _remaining_timeout(deadline, subprocess_timeout)
        if timeout is None:
            return None
        output = _run_text(
            [*crictl, "inspect", "-o", "json", container_id],
            timeout=timeout,
            max_output=MAX_INSPECT_BYTES,
        )
        if output is None:
            return None
        container = _parse_crictl_inspect(output, host_home=host_home)
        if container is None:
            continue
        if container.container_id != container_id:
            # crictl echoed a different container's status.id (prefix reuse, a
            # ps/inspect race, or a crictl bug). Drop the anomalous row like a
            # failed parse instead of returning None: that keeps the earlier
            # inspected containers and lets _scan_with_collector report the short
            # inventory as scan_succeeded=False rather than collapsing the whole
            # k3s runtime to empty.
            continue
        containers.append(container)
    return containers


def _parse_crictl_image_digest(text: str) -> str | None:
    try:
        payload = json.loads(text)
    except (TypeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    status = _mapping(payload.get("status"))
    repo_digests = status.get("repoDigests")
    if isinstance(repo_digests, list):
        for value in repo_digests:
            digest = _digest_from_reference(value)
            if digest is not None:
                return digest
    return _digest_from_reference(status.get("id"))


def _collect_image_digests(
    *,
    crictl: CrictlCommand,
    containers: list[DiscoveredContainer],
    deadline: float,
    subprocess_timeout: float,
) -> list[DiscoveredContainer]:
    digests: dict[str, str | None] = {}
    for container in containers:
        image_id = container.image_id
        if not image_id:
            continue
        if image_id not in digests:
            timeout = _remaining_timeout(deadline, subprocess_timeout)
            if timeout is None:
                break
            output = _run_text(
                [*crictl, "inspecti", "-o", "json", image_id],
                timeout=timeout,
                max_output=MAX_INSPECT_BYTES,
            )
            digests[image_id] = (
                _parse_crictl_image_digest(output) if output is not None else None
            )
        digest = digests[image_id]
        if digest is not None:
            container.image_digest = digest
    return containers
