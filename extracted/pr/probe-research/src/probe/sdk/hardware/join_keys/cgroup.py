"""The container, pod and SLURM job a /proc/<pid>/cgroup file names: the same rules as the node daemon's
`internal/occupancy/cgroup.go`, so a writer and its GPU occupant read the same ids."""

from __future__ import annotations

import re
from dataclasses import dataclass

# systemd-driver scopes: cri-containerd-<id>.scope, docker-<id>.scope, crio-<id>.scope, libpod-<id>.scope.
# crio-conmon-<id>.scope is the monitor, not the container, and is deliberately not matched.
_SCOPE_CONTAINER = re.compile(r"^(?:cri-containerd|containerd|docker|crio|libpod)-([0-9a-f]{64})\.scope$")
# cgroupfs-driver segments: /docker/<id>, /kubepods/burstable/pod<uid>/<id>.
_BARE_CONTAINER = re.compile(r"^[0-9a-f]{64}$")
# The pod UID, dashed (cgroupfs) or underscored (systemd slice names cannot hold dashes).
_POD_UID = re.compile(r"pod([0-9a-f]{8}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{12})")
_SLURM_JOB = re.compile(r"^job_([0-9]+)$")


@dataclass(frozen=True)
class CgroupIds:
    container_id: str | None = None
    pod_uid: str | None = None
    slurm_job_id: str | None = None


def parse_cgroup(content: str) -> CgroupIds:
    """Every line of a cgroup v1 or v2 file (`<id>:<controllers>:<path>`): the first container, pod and
    SLURM job ids any path names. Unknown layouts yield None."""
    container_id = pod_uid = slurm_job_id = None
    for line in str(content or "").splitlines():
        parts = line.strip().split(":", 2)
        if len(parts) != 3:
            continue
        path = parts[2]
        container_id = container_id or _find_container_id(path)
        pod_uid = pod_uid or _find_pod_uid(path)
        slurm_job_id = slurm_job_id or _find_slurm_job_id(path)
    return CgroupIds(container_id, pod_uid, slurm_job_id)


def _find_container_id(path: str) -> str | None:
    """The innermost container id on one cgroup path."""
    segments = path.split("/")
    for index in range(len(segments) - 1, -1, -1):
        segment = segments[index]
        if match := _SCOPE_CONTAINER.match(segment):
            return match.group(1)
        if _BARE_CONTAINER.match(segment) and index > 0 and _is_container_parent(segments[:index]):
            return segment
    return None


def _is_container_parent(parents: list[str]) -> bool:
    """A bare 64-hex segment sits under a runtime or pod directory, not some random hash."""
    return any(
        parent in ("docker", "crio", "containerd") or parent.startswith(("kubepods", "pod"))
        for parent in parents
    )


def _find_pod_uid(path: str) -> str | None:
    """The kubelet pod UID on one path, with systemd underscores turned back into dashes."""
    match = _POD_UID.search(path)
    if match is None or "kubepods" not in path:
        return None
    return match.group(1).replace("_", "-")


def _find_slurm_job_id(path: str) -> str | None:
    """`<id>` from a `job_<id>` segment on a path that belongs to SLURM."""
    if "slurm" not in path:
        return None
    for segment in path.split("/"):
        if match := _SLURM_JOB.match(segment):
            return match.group(1)
    return None
