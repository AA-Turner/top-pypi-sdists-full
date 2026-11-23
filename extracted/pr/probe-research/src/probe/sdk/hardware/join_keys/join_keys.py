"""Join keys: where this process runs (its GPUs, node, pod, container, SLURM job, pid namespace), sent on the
writer lease beat so the server ties a node daemon's GPU occupants to this run (probe-node P0)."""

from __future__ import annotations

import os
import threading
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from probe.sdk.hardware.join_keys.cgroup import parse_cgroup

#: `PROBE_JOIN_KEYS=0` (or false/off) sends none and asks no metadata server; `PROBE_HW=0` drops gpu_uuids.
OFF_ENV = "PROBE_JOIN_KEYS"
#: Every field a beat may carry (the server's WriterBeat), each omitted when unknown.
FIELDS = ("gpu_uuids", "node_key", "instance_id", "pod_uid", "container_id", "k8s_node", "slurm_job_id", "pidns")
#: The beat's lease sessions whose last sent keys are remembered; past this the oldest are forgotten.
_MAX_SESSIONS = 256
PROCFS_ROOT = Path("/proc")


def is_enabled(env: Mapping[str, str] | None = None) -> bool:
    env = os.environ if env is None else env
    return str(env.get(OFF_ENV, "1")).strip().lower() not in ("0", "false", "off")


def read_local_keys(env: Mapping[str, str] | None = None, procfs_root: Path = PROCFS_ROOT) -> dict[str, Any]:
    """The keys the environment and /proc hold (microseconds; Linux only, nothing elsewhere). Never raises."""
    env = os.environ if env is None else env
    keys: dict[str, Any] = {}
    try:
        cgroup = parse_cgroup(_read_text(procfs_root / "self" / "cgroup"))
    except Exception:  # noqa: BLE001
        cgroup = parse_cgroup("")
    pod_uid = (env.get("POD_UID") or "").strip() or cgroup.pod_uid
    slurm_job_id = (env.get("SLURM_JOB_ID") or "").strip() or cgroup.slurm_job_id
    k8s_node = (env.get("NODE_NAME") or "").strip()
    for name, value in (("pod_uid", pod_uid), ("container_id", cgroup.container_id),
                        ("k8s_node", k8s_node), ("slurm_job_id", slurm_job_id)):
        if value:
            keys[name] = value
    try:
        keys["pidns"] = int((procfs_root / "self" / "ns" / "pid").stat().st_ino)
    except (OSError, ValueError):
        pass
    return keys


def read_gpu_uuids(env: Mapping[str, str] | None = None, nvml: Any = None) -> list[str]:
    """The GPU UUIDs this process can see, by the NVML source's CUDA_VISIBLE_DEVICES rules. Empty when NVML
    is not there or `PROBE_HW=0`. A modern MIG entry (`MIG-<uuid>`) is its own UUID, sent as written."""
    env = os.environ if env is None else env
    from probe.sdk.hardware.wiring import hw_enabled

    if not hw_enabled(None, env):
        return []
    from probe.sdk.hardware.resources.nvidia import NvidiaResource

    spec = env.get("CUDA_VISIBLE_DEVICES")
    try:
        resource = NvidiaResource.create(nvml=nvml if nvml is not None else _load_nvml(), visible_devices=spec)
    except Exception:  # noqa: BLE001
        return []
    if resource is None:
        return []
    try:
        if resource._visible is None:
            migs = [entry.strip() for entry in str(spec or "").split(",") if entry.strip().startswith("MIG-")]
            if migs:
                return migs
            indices: list[int] = list(range(resource._nvml.nvmlDeviceGetCount()))
        else:
            indices = sorted(resource._visible)
        return [resource.get_device_uuid(index) for index in indices]
    except Exception:  # noqa: BLE001 -- a glitched device costs the key, never the beat
        return []
    finally:
        resource.close()


def resolve_node_key(cloud_key: str | None, env: Mapping[str, str] | None = None) -> str | None:
    """The node daemon's order: the cloud's node key, then NODE_NAME, else none."""
    env = os.environ if env is None else env
    return cloud_key or (env.get("NODE_NAME") or "").strip() or None


def collect_join_keys(
    env: Mapping[str, str] | None = None,
    procfs_root: Path = PROCFS_ROOT,
    *,
    nvml: Any = None,
    fetch_node_key=None,
) -> dict[str, Any]:
    """Every key at once, blocking (the metadata ask included): the background collector's whole job."""
    env = os.environ if env is None else env
    if not is_enabled(env):
        return {}
    keys = read_local_keys(env, procfs_root)
    if uuids := read_gpu_uuids(env, nvml):
        keys["gpu_uuids"] = uuids
    from probe.sdk.hardware.join_keys import cloud  # lazy: urllib is no cost to a process that never beats

    fetch = fetch_node_key or _fetch_node_key
    try:
        cloud_key = cloud.clean_node_key(fetch())
    except Exception:  # noqa: BLE001
        cloud_key = None
    if instance_id := cloud.get_instance_id(cloud_key):
        keys["instance_id"] = instance_id
    if node_key := resolve_node_key(cloud_key, env):
        keys["node_key"] = node_key
    return keys


class _Collector:
    """This process's keys: the cheap ones read at once, the rest (NVML, the metadata servers) on a daemon
    thread so no beat waits. Keyed by pid, so a forked child reads its own."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pid: int | None = None
        self._keys: dict[str, Any] = {}
        self._sent: dict[tuple[str, str], dict[str, Any]] = {}

    def get_current(self) -> dict[str, Any]:
        with self._lock:
            if self._pid != os.getpid():
                self._start()
            return dict(self._keys)

    def _start(self) -> None:
        self._pid = os.getpid()
        self._sent = {}
        self._keys = read_local_keys() if is_enabled() else {}
        if not is_enabled():
            return
        node_key = resolve_node_key(None)
        if node_key:
            self._keys["node_key"] = node_key
        threading.Thread(target=self._collect_slow, args=(self._pid,), name="probe-join-keys", daemon=True).start()

    def _collect_slow(self, pid: int) -> None:
        try:
            keys = collect_join_keys()
        except Exception:  # noqa: BLE001
            return
        with self._lock:
            if self._pid == pid:
                self._keys = keys

    def get_unsent(self, run_id: str, session_id: str) -> dict[str, Any]:
        """The keys to put on this beat: all of them on a session's first, again only once they change."""
        keys = self.get_current()
        with self._lock:
            return {} if not keys or self._sent.get((run_id, session_id)) == keys else keys

    def record_sent(self, run_id: str, session_id: str, keys: Mapping[str, Any]) -> None:
        with self._lock:
            self._sent.pop((run_id, session_id), None)
            self._sent[(run_id, session_id)] = dict(keys)
            while len(self._sent) > _MAX_SESSIONS:
                self._sent.pop(next(iter(self._sent)))

    def forget(self) -> None:
        """Back to a fresh process (tests)."""
        with self._lock:
            self._pid, self._keys, self._sent = None, {}, {}


_COLLECTOR = _Collector()


def warm_join_keys() -> None:
    """Start reading this process's keys now, so the first beat finds them ready. Never raises."""
    try:
        _COLLECTOR.get_current()
    except Exception:  # noqa: BLE001
        pass


def get_beat_join_keys(run_id: str, session_id: str) -> dict[str, Any]:
    """The join keys this lease beat carries ({} when there is nothing new to say). Never raises."""
    try:
        return _COLLECTOR.get_unsent(str(run_id), str(session_id))
    except Exception:  # noqa: BLE001
        return {}


def mark_join_keys_sent(run_id: str, session_id: str, keys: Mapping[str, Any]) -> None:
    """A beat carrying ``keys`` was answered: later beats leave them out until they change."""
    try:
        _COLLECTOR.record_sent(str(run_id), str(session_id), keys)
    except Exception:  # noqa: BLE001
        pass


def forget_join_keys() -> None:
    _COLLECTOR.forget()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _fetch_node_key() -> str | None:
    """The metadata ask (tests replace this: no test reaches a metadata server or reads cloud-init)."""
    from probe.sdk.hardware.join_keys import cloud

    return cloud.fetch_node_key()


def _load_nvml() -> Any:
    try:
        import pynvml  # lazy: absence means no gpu_uuids
    except ImportError:
        return None
    return pynvml
