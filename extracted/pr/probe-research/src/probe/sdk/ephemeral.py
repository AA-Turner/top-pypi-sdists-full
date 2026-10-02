"""Does a file's storage outlive the job that wrote it?

Output capture needs this answer for every file it cannot upload (over 64 MB,
past the close's time budget, or not inspectable). On storage that outlives
the job it is recorded as a POINTER (path, size): the bytes are still there
tomorrow, and copying a 16 GB checkpoint off a team drive per run is
duplication, not capture. On the job's own throwaway disk a pointer is refused
-- it would name bytes that are gone the moment the container is -- so the file
is LISTED as not kept.

THE FILE'S STORAGE DECIDES, NOT THE MACHINE. An Anthrogen job pod on OCI is a
Kubernetes pod -- a "throwaway machine" -- but its checkpoints sit on the shared
`/workspace` drive every pod mounts, which is exactly the storage that lasts.
So the mount the file's REAL path lives on is read first (links are followed:
a Modal Volume is a symlink into `/__modal/volumes`):

* throwaway filesystems -- the container's own layer (`overlay`), RAM
  (`tmpfs`, `ramfs`) -- are throwaway wherever they appear;
* network and shared filesystems (NFS, Lustre, GPFS, CephFS, SMB, virtiofs,
  FUSE mounts of buckets or remote drives) last;
* `9p` lasts, except on Modal outside `/__modal/volumes` (Modal serves its own
  code mounts over 9p);
* a plain local disk (ext4, xfs, apfs ...) lasts on an ordinary machine and is
  throwaway on one that says it is disposable (Modal, a Kubernetes pod, a
  container, CI, Colab, SageMaker, Batch, SkyPilot, RunPod, a Slurm node's
  local disk).

When in doubt the answer is "throwaway": the cost of that mistake is a big file
listed instead of pointed to, the cost of the other is a pointer to nothing.

`PROBE_EPHEMERAL=1` makes everything throwaway, `=0` everything lasting.
"""

from __future__ import annotations

import functools
import os

ENV = "PROBE_EPHEMERAL"

THROWAWAY_FSTYPES = frozenset({
    "overlay", "overlayfs", "aufs", "tmpfs", "ramfs", "devtmpfs", "squashfs", "zram",
    # Rootless containers (Podman) and unprivileged images mount their layers
    # through FUSE: a container's own disk all the same.
    "fuse.fuse-overlayfs", "fuse.squashfuse", "fuse.squashfuse_ll", "squashfuse",
})
#: Kernel views, not storage. A walk never enters them: with the working folder
#: at `/`, `/proc/<pid>/environ` is a "new file" holding every secret in the
#: environment.
PSEUDO_FSTYPES = frozenset({
    "proc", "sysfs", "devtmpfs", "devpts", "cgroup", "cgroup2", "mqueue", "debugfs", "tracefs",
    "securityfs", "pstore", "bpf", "fusectl", "configfs", "binfmt_misc", "hugetlbfs", "autofs",
    "nsfs", "rpc_pipefs", "efivarfs", "selinuxfs",
})
NETWORK_FSTYPES = frozenset({
    "nfs", "nfs4", "cifs", "smb3", "smbfs", "lustre", "gpfs", "beegfs", "ceph", "cephfs",
    "glusterfs", "panfs", "wekafs", "afs", "virtiofs", "9p", "davfs", "fuse.glusterfs",
})
#: FUSE filesystems that are local, not remote storage.
LOCAL_FUSE_FSTYPES = frozenset({
    "fuse.lxcfs", "fuse.gvfsd-fuse", "fuse.portal", "fuse.snapfuse", "fuse.xdg-document-portal",
    "fuse.appimagekit", "fuseblk",
})
#: Environment variables that mean "this machine is disposable".
MACHINE_MARKERS = (
    "MODAL_TASK_ID", "KUBERNETES_SERVICE_HOST", "COLAB_RELEASE_TAG", "TRAINING_JOB_NAME",
    "SM_TRAINING_ENV", "AWS_BATCH_JOB_ID", "SKYPILOT_TASK_ID", "RUNPOD_POD_ID",
    "GITHUB_ACTIONS", "GITLAB_CI", "BUILDKITE", "SLURM_JOB_ID",
)
_CONTAINER_FILES = ("/.dockerenv", "/run/.containerenv")
_MODAL_VOLUMES = "/__modal/volumes"
_realpath = os.path.realpath  # indirection so tests can map links without patching os


def _unescape(field: str) -> str:
    # mountinfo octal-escapes space, tab, newline and backslash.
    return (
        field.replace("\\040", " ").replace("\\011", "\t").replace("\\012", "\n").replace("\\134", "\\")
    )


@functools.lru_cache(maxsize=1)
def _mounts() -> tuple[tuple[str, str], ...]:
    """((mount point, fstype), ...) from /proc/self/mountinfo, longest first;
    of two mounts on one point, the later (the one on top) first."""
    try:
        with open("/proc/self/mountinfo", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return ()
    found = []
    for line in lines:
        before, sep, after = line.partition(" - ")
        fields = before.split()
        if not sep or len(fields) < 5 or not after.split():
            continue
        found.append((_unescape(fields[4]), after.split()[0]))
    found.reverse()  # later lines are mounted over earlier ones; sort is stable
    found.sort(key=lambda m: len(m[0]), reverse=True)
    return tuple(found)


def mount_points() -> frozenset[str]:
    """Every mount point, directories and single bind-mounted files alike."""
    return frozenset(point for point, _fstype in _mounts())


def pseudo_mountpoints() -> frozenset[str]:
    """Mount points of kernel pseudo-filesystems (`/proc`, `/sys` ...)."""
    return frozenset(point for point, fstype in _mounts() if fstype in PSEUDO_FSTYPES)


def refresh() -> None:
    """Forget the cached mount table (a mount appeared or went)."""
    _mounts.cache_clear()


def fstype_of(path: str) -> str | None:
    """The filesystem type holding `path`'s real location, or None when the
    platform has no mount table (macOS, Windows)."""
    return _fstype_at(_realpath(path))


def _fstype_at(real: str) -> str | None:
    for mountpoint, fstype in _mounts():
        if mountpoint == "/" or real == mountpoint or real.startswith(mountpoint.rstrip("/") + "/"):
            return fstype
    return None


def machine_is_disposable() -> bool:
    if any(os.environ.get(name) for name in MACHINE_MARKERS):
        return True
    if (os.environ.get("CI") or "").strip().lower() in {"1", "true", "yes"}:
        return True
    return any(os.path.exists(marker) for marker in _CONTAINER_FILES)


def storage_is_durable(path: str) -> bool:
    """True when the storage holding `path` outlives this job."""
    return describe(path)["durable"]


def describe(path: str) -> dict:
    """``{"durable": bool, "fstype": str|None, "reason": str}`` for `path`."""
    override = (os.environ.get(ENV) or "").strip().lower()
    if override in {"1", "true", "yes", "on"}:
        return {"durable": False, "fstype": None, "reason": f"{ENV}=1"}
    if override in {"0", "false", "no", "off"}:
        return {"durable": True, "fstype": None, "reason": f"{ENV}=0"}
    real = _realpath(path)
    fstype = _fstype_at(real)
    if fstype in THROWAWAY_FSTYPES:
        return {"durable": False, "fstype": fstype, "reason": "throwaway filesystem"}
    if fstype == "9p" and os.environ.get("MODAL_TASK_ID"):
        inside = real == _MODAL_VOLUMES or real.startswith(_MODAL_VOLUMES + "/")
        return {
            "durable": inside,
            "fstype": fstype,
            "reason": "Modal Volume" if inside else "Modal internal mount",
        }
    if fstype in NETWORK_FSTYPES or (
        fstype is not None and fstype.startswith("fuse.") and fstype not in LOCAL_FUSE_FSTYPES
    ):
        return {"durable": True, "fstype": fstype, "reason": "network or shared filesystem"}
    disposable = machine_is_disposable()
    return {
        "durable": not disposable,
        "fstype": fstype,
        "reason": "local disk on a disposable machine" if disposable else "local disk",
    }
