"""Machine GPU topology — auto-detect device count + peer-access matrix and
enable cross-GPU peer access on demand.

This backs the decoupled decode/inference path: a consumer running on GPU Y can
read a producer's CUDA-IPC ring buffer allocated on GPU X by enabling NVLink
peer access (Y -> X) and copying the frame to local memory. Measured on an
8xH100 NVSwitch box at ~5 us / 0.6 MB frame (see
ml-codebases/docs/new-architecture/08-decode-inference-decoupling-d2d.md).

The old same-GPU classes in cuda_shm_ring_buffer.py / databus.py are kept
unchanged for reference; this module is additive.
"""

from __future__ import annotations

import logging
import threading
from typing import Dict, Optional, Set, Tuple

logger = logging.getLogger(__name__)

try:
    import cupy as cp
    from cupy.cuda import runtime as _rt

    CUPY_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only where cupy is absent
    CUPY_AVAILABLE = False
    cp = None  # type: ignore[assignment]
    _rt = None  # type: ignore[assignment]


class MachineTopology:
    """Process-wide cache of GPU count, peer-access capability, and which
    (consumer, producer) peer links have already been enabled. Thread-safe and
    idempotent — safe to call enable_peer() on every connect."""

    def __init__(self) -> None:
        # Reentrant: enable_peer() holds the lock and calls can_access_peer().
        self._lock = threading.RLock()
        self._count: Optional[int] = None
        self._peer_ok: Dict[Tuple[int, int], bool] = {}
        self._enabled: Set[Tuple[int, int]] = set()

    @property
    def device_count(self) -> int:
        if self._count is None:
            try:
                self._count = int(_rt.getDeviceCount()) if CUPY_AVAILABLE else 0
            except Exception:  # noqa: BLE001
                self._count = 0
        return self._count

    def can_access_peer(self, local_gpu: int, producer_gpu: int) -> bool:
        """True if local_gpu can directly read producer_gpu's memory (NVLink/
        PCIe P2P). Same device is trivially True. Result is cached."""
        if local_gpu == producer_gpu:
            return True
        if not CUPY_AVAILABLE:
            return False
        key = (local_gpu, producer_gpu)
        with self._lock:
            cached = self._peer_ok.get(key)
            if cached is None:
                try:
                    cached = bool(_rt.deviceCanAccessPeer(local_gpu, producer_gpu))
                except Exception:  # noqa: BLE001
                    cached = False
                self._peer_ok[key] = cached
            return cached

    def enable_peer(self, local_gpu: int, producer_gpu: int) -> bool:
        """Idempotently enable local_gpu -> producer_gpu peer access.

        Returns True when frames on producer_gpu are reachable from local_gpu
        (same GPU, or NVLink/PCIe P2P successfully enabled).

        Returns False when local_gpu != producer_gpu and no peer path exists
        (a multi-GPU host without NVLink/P2P). This is **terminal** for
        cross-GPU consume — there is no transparent host-bounce fallback (the
        CUDA-IPC handle itself can't be opened for another device's memory
        without P2P). consumer_auto turns False into a PeerUnavailableError;
        the operator's remedy is to co-locate inference on the producer's GPU.
        Single-GPU hosts (Orin/Thor) never reach this (producer_gpu == local).
        """
        if not CUPY_AVAILABLE or local_gpu == producer_gpu:
            return True
        key = (local_gpu, producer_gpu)
        with self._lock:
            if key in self._enabled:
                return True
            if not self.can_access_peer(local_gpu, producer_gpu):
                logger.warning(
                    "GPU %s cannot peer-access GPU %s (no NVLink/P2P) — cross-GPU "
                    "consume is unsupported on this host; co-locate inference on GPU %s",
                    local_gpu,
                    producer_gpu,
                    producer_gpu,
                )
                return False
            try:
                with cp.cuda.Device(local_gpu):
                    _rt.deviceEnablePeerAccess(producer_gpu)
            except Exception as e:  # noqa: BLE001
                # PeerAccessAlreadyEnabled is success; anything else is a real failure.
                if "already" not in str(e).lower():
                    logger.warning("enablePeerAccess %s -> %s failed: %s", local_gpu, producer_gpu, e)
                    return False
            self._enabled.add(key)
            logger.info("Enabled peer access GPU %s -> GPU %s", local_gpu, producer_gpu)
            return True

    def has_full_p2p(self, device_ids=None) -> bool:
        """True if every ordered pair among device_ids can peer-access (full P2P/
        NVLink mesh). Used by the SG to decide whether cross-GPU consume is viable
        and by consumer_auto to pick a transport. Same-device pairs are trivially
        OK; a single GPU is trivially a full mesh."""
        ids = list(range(self.device_count)) if device_ids is None else list(device_ids)
        for a in ids:
            for b in ids:
                if a != b and not self.can_access_peer(a, b):
                    return False
        return True


# Process-wide singleton.
topology = MachineTopology()
