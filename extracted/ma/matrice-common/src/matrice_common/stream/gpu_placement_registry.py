"""Shared-memory GPU placement registry for app-affinity camera scheduling.

Complements ``GpuCameraMap`` (which holds ``camera_id -> gpu_id``) with a
richer per-GPU view that captures the *current* set of cameras AND apps
loaded on each GPU, used by the SG placer to make app-aware assignments
("place a new camera on a GPU that already runs its app's IE worker").

Format in shared memory:
- 4 bytes: uint32 little-endian size of JSON body
- N bytes: JSON object keyed by gpu_id (str) -> {cameras: [...], apps: [...], load: float}

Writers (both under ``fcntl.flock``):
- The Streaming Gateway updates ``cameras[]`` (+ load) on camera add/remove.
- Each Inference Engine container updates ``apps[]`` when its workers
  start/stop on a given GPU.

Readers (shared lock):
- The SG placer at every camera-placement decision.
- IE main for post-placement logging / diagnostics.

The registry is purely advisory — losing it (e.g. host reboot wipes ``/dev/shm``)
just degrades the next placement decision to load-only balancing. The
``GpuCameraMap`` remains the single source of truth for which GPU each
camera lives on; the registry is the side-state needed to do *smart*
placement of *new* cameras.
"""

from __future__ import annotations

import fcntl
import json
import logging
import mmap
import os
import struct
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

logger = logging.getLogger(__name__)

# Reuse the same SHM base path convention as GpuCameraMap.
SHM_BASE_PATH = os.getenv("MATRICE_SHM_PATH", "/dev/shm")  # nosec B108

MAP_SHARED = getattr(mmap, "MAP_SHARED", 1)
PROT_READ = getattr(mmap, "PROT_READ", 1)
PROT_WRITE = getattr(mmap, "PROT_WRITE", 2)


@dataclass
class GpuState:
    """Per-GPU state snapshot."""

    cameras: List[str] = field(default_factory=list)
    apps: List[str] = field(default_factory=list)
    load: float = 0.0

    @classmethod
    def empty(cls) -> "GpuState":
        return cls()

    @classmethod
    def from_dict(cls, d: dict) -> "GpuState":
        return cls(
            cameras=list(d.get("cameras", [])),
            apps=list(d.get("apps", [])),
            load=float(d.get("load", 0.0)),
        )

    def to_dict(self) -> dict:
        return {"cameras": list(self.cameras), "apps": list(self.apps), "load": float(self.load)}


class GpuPlacementRegistry:
    """SHM-backed registry of per-GPU cameras + apps + load.

    Distinct from ``GpuCameraMap`` — that one persists the per-camera
    mapping. This one persists what's currently *resident* on each GPU.

    Same atomicity discipline as ``GpuCameraMap``: every read-modify-write
    is wrapped in an exclusive ``fcntl.flock`` on the fd.
    """

    SHM_PATH = f"{SHM_BASE_PATH}/matrice_gpu_placement"
    MAX_SIZE = 256 * 1024  # 256 KB — plenty for hundreds of GPUs × hundreds of cameras/apps

    def __init__(self) -> None:
        self._fd: Optional[int] = None
        self._mmap: Optional[mmap.mmap] = None
        self._initialized = False

    # ------------------------------------------------------------------
    # Open / connect
    # ------------------------------------------------------------------
    def initialize(self, num_gpus: int) -> bool:
        """Open or create the SHM file, ensuring an entry exists for each GPU.

        Idempotent: existing file is preserved (cameras/apps survive
        producer restarts); only missing GPU ids get populated with empty
        state. Safe to call on every SG startup.
        """
        try:
            self._fd = os.open(self.SHM_PATH, os.O_CREAT | os.O_RDWR, 0o666)
            os.ftruncate(self._fd, self.MAX_SIZE)
            self._mmap = mmap.mmap(self._fd, self.MAX_SIZE, MAP_SHARED, PROT_READ | PROT_WRITE)  # type: ignore[arg-type]
            self._initialized = True

            # Make sure every gpu_id 0..num_gpus-1 has at least an empty entry.
            current = self._read_locked()
            changed = False
            for g in range(num_gpus):
                if str(g) not in current:
                    current[str(g)] = GpuState.empty().to_dict()
                    changed = True
            if changed:
                self._write_locked(current)
            logger.info(
                f"GpuPlacementRegistry initialized at {self.SHM_PATH} "
                f"(num_gpus={num_gpus}, existing_entries={len(current)})"
            )
            return True
        except Exception as e:
            logger.error(f"GpuPlacementRegistry: failed to initialize: {e}")
            return False

    def connect(self) -> bool:
        """Open an existing SHM file read/write. Returns False if missing."""
        try:
            if not os.path.exists(self.SHM_PATH):
                logger.warning(f"GpuPlacementRegistry: file not found at {self.SHM_PATH}")
                return False
            self._fd = os.open(self.SHM_PATH, os.O_RDWR)
            self._mmap = mmap.mmap(self._fd, self.MAX_SIZE, MAP_SHARED, PROT_READ | PROT_WRITE)  # type: ignore[arg-type]
            self._initialized = True
            return True
        except Exception as e:
            logger.error(f"GpuPlacementRegistry: failed to connect: {e}")
            return False

    def close(self) -> None:
        try:
            if self._mmap is not None:
                self._mmap.close()
                self._mmap = None
            if self._fd is not None:
                os.close(self._fd)
                self._fd = None
        except Exception:
            pass
        self._initialized = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def update_cameras(
        self,
        gpu_id: int,
        add: Optional[Iterable[str]] = None,
        remove: Optional[Iterable[str]] = None,
        load_delta: float = 0.0,
    ) -> None:
        """Atomically add/remove cameras and apply a load delta on one GPU."""
        if not self._guard():
            return

        def mutate(current: Dict[str, dict]) -> Dict[str, dict]:
            entry = current.setdefault(str(gpu_id), GpuState.empty().to_dict())
            cams = list(entry.get("cameras", []))
            if remove:
                for c in remove:
                    if c in cams:
                        cams.remove(c)
            if add:
                for c in add:
                    if c not in cams:
                        cams.append(c)
            entry["cameras"] = cams
            entry["load"] = max(0.0, float(entry.get("load", 0.0)) + float(load_delta))
            return current

        self._read_modify_write(mutate)

    def update_apps(
        self,
        gpu_id: int,
        add: Optional[Iterable[str]] = None,
        remove: Optional[Iterable[str]] = None,
    ) -> None:
        """Atomically add/remove app (deployment) entries on one GPU."""
        if not self._guard():
            return

        def mutate(current: Dict[str, dict]) -> Dict[str, dict]:
            entry = current.setdefault(str(gpu_id), GpuState.empty().to_dict())
            apps = list(entry.get("apps", []))
            if remove:
                for a in remove:
                    if a in apps:
                        apps.remove(a)
            if add:
                for a in add:
                    if a not in apps:
                        apps.append(a)
            entry["apps"] = apps
            return current

        self._read_modify_write(mutate)

    def remove_app_from_all(self, deployment_id: str) -> None:
        """Remove a deployment_id from every GPU's ``apps[]``.

        Used by IE startup to clean stale entries from a prior crash before
        re-registering, and by the SG stale-sweep loop to evict dead IEs.
        """
        if not self._guard():
            return

        def mutate(current: Dict[str, dict]) -> Dict[str, dict]:
            for entry in current.values():
                apps = list(entry.get("apps", []))
                if deployment_id in apps:
                    apps.remove(deployment_id)
                    entry["apps"] = apps
            return current

        self._read_modify_write(mutate)

    def replace_cameras_for_gpus(
        self, by_gpu: Dict[int, List[str]], load_by_gpu: Optional[Dict[int, float]] = None
    ) -> None:
        """Replace the ``cameras[]`` list (and optionally ``load``) for the
        given GPUs, leaving other GPUs and the ``apps[]`` lists untouched.

        Used by the SG on startup to seed the registry from the authoritative
        ``GpuCameraMap`` (single source of truth for camera->GPU placement).
        """
        if not self._guard():
            return

        def mutate(current: Dict[str, dict]) -> Dict[str, dict]:
            for gpu_id, cams in by_gpu.items():
                entry = current.setdefault(str(gpu_id), GpuState.empty().to_dict())
                entry["cameras"] = list(cams)
                if load_by_gpu and gpu_id in load_by_gpu:
                    entry["load"] = float(load_by_gpu[gpu_id])
            return current

        self._read_modify_write(mutate)

    def snapshot(self) -> Dict[int, GpuState]:
        """Read the whole registry under a shared lock."""
        raw = self._read_locked()
        return {int(k): GpuState.from_dict(v) for k, v in raw.items()}

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _guard(self) -> bool:
        if not self._initialized or self._mmap is None or self._fd is None:
            logger.warning("GpuPlacementRegistry: not initialized; skipping write")
            return False
        return True

    def _read_locked(self) -> Dict[str, dict]:
        """Read JSON under a shared lock. Returns {} on missing/corrupt."""
        if not self._initialized or self._mmap is None or self._fd is None:
            return {}
        try:
            fcntl.flock(self._fd, fcntl.LOCK_SH)
            try:
                self._mmap.seek(0)
                size_bytes = self._mmap.read(4)
                if len(size_bytes) < 4:
                    return {}
                size = struct.unpack("<I", size_bytes)[0]
                if size == 0 or size > self.MAX_SIZE - 4:
                    return {}
                data = self._mmap.read(size).decode("utf-8")
                return json.loads(data)
            finally:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
        except Exception as e:
            logger.error(f"GpuPlacementRegistry: read failed: {e}")
            return {}

    def _write_locked(self, current: Dict[str, dict]) -> None:
        if not self._initialized or self._mmap is None or self._fd is None:
            return
        data = json.dumps(current, separators=(",", ":")).encode("utf-8")
        if len(data) + 4 > self.MAX_SIZE:
            logger.error(f"GpuPlacementRegistry: payload too large ({len(data)} bytes)")
            return
        try:
            fcntl.flock(self._fd, fcntl.LOCK_EX)
            try:
                self._mmap.seek(0)
                self._mmap.write(struct.pack("<I", len(data)))
                self._mmap.write(data)
                self._mmap.flush()
            finally:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
        except Exception as e:
            logger.error(f"GpuPlacementRegistry: write failed: {e}")

    def _read_modify_write(self, mutate) -> None:
        """Read, run ``mutate(current)``, write back — all under one
        exclusive lock so concurrent writers don't lose updates."""
        if not self._initialized or self._mmap is None or self._fd is None:
            return
        try:
            fcntl.flock(self._fd, fcntl.LOCK_EX)
            try:
                # Read inside lock
                self._mmap.seek(0)
                size_bytes = self._mmap.read(4)
                current: Dict[str, dict] = {}
                if len(size_bytes) >= 4:
                    size = struct.unpack("<I", size_bytes)[0]
                    if 0 < size <= self.MAX_SIZE - 4:
                        try:
                            data = self._mmap.read(size).decode("utf-8")
                            current = json.loads(data)
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            current = {}
                # Mutate
                current = mutate(current)
                # Write inside same lock
                data_b = json.dumps(current, separators=(",", ":")).encode("utf-8")
                if len(data_b) + 4 > self.MAX_SIZE:
                    logger.error(f"GpuPlacementRegistry: payload too large after mutate ({len(data_b)} bytes)")
                    return
                self._mmap.seek(0)
                self._mmap.write(struct.pack("<I", len(data_b)))
                self._mmap.write(data_b)
                self._mmap.flush()
            finally:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
        except Exception as e:
            logger.error(f"GpuPlacementRegistry: read-modify-write failed: {e}")


__all__ = ["GpuPlacementRegistry", "GpuState"]
