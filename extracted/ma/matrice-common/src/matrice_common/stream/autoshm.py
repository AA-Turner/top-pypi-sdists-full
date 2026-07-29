"""Auto-device CUDA-SHM consumer — read a camera's frames on ANY local GPU,
regardless of which GPU the producer (Streaming Gateway) decoded on.

This is the additive "decoupled decode/inference" path. It reuses the existing
``CudaIpcRingBuffer`` for everything (header parse, IPC import, slot/skip logic,
the shipped SG-restart self-heal) and only adds:

  * reading the producer GPU from the ring-buffer header (no caller gpu_id),
  * enabling NVLink peer access (consumer GPU -> producer GPU),
  * a single peer copy of each committed frame into local memory (Model A).

Same-GPU producers stay fully zero-copy. The old same-GPU classes
(``CudaIpcRingBuffer``, ``DataBus`` consumer path, ``GpuCameraMap``,
``GpuPlacementRegistry``) are kept unchanged for reference.
"""

from __future__ import annotations

import logging
import mmap
import os
import struct
import threading
import time
from typing import Optional

from .cuda_shm_ring_buffer import (
    CUPY_AVAILABLE,
    MAP_SHARED,
    PROT_READ,
    CudaIpcRingBuffer,
    _cvd_remap,
    cp,
    np,
)
from .databus import DataBus, DataFormat, _parse_format
from .device_topology import topology

logger = logging.getLogger(__name__)

# Cross-GPU consume fallback config (no-NVLink/no-P2P hosts).
#   off        -> cross-GPU on a no-P2P host is terminal (default; current behavior)
#   host_stage -> degrade via pinned DtoH->host->HtoD instead of failing
_XGPU_FALLBACK = os.environ.get("MATRICE_XGPU_FALLBACK", "off").lower()
_XGPU_WARN_EVERY_SEC = float(os.environ.get("MATRICE_XGPU_WARN_EVERY_SEC", "30"))

_warn_lock = threading.Lock()
_warn_last: dict = {}


def _warn_throttled(key: str, msg: str, *args) -> None:
    """Emit ``logger.warning(msg, *args)`` at most once per _XGPU_WARN_EVERY_SEC
    per key. Keeps the degradation visible without flooding at frame rate."""
    now = time.monotonic()
    with _warn_lock:
        if now - _warn_last.get(key, 0.0) >= _XGPU_WARN_EVERY_SEC:
            _warn_last[key] = now
            logger.warning(msg, *args)


def _read_producer_header(address: str):
    """Read (producer_gpu, num_slots, width, height, channels) from a ring
    buffer's SHM header. The layout (offset + field order) is owned by
    ``CudaIpcRingBuffer`` — read it from there so a header change can't silently
    desync this reader."""
    offset = CudaIpcRingBuffer.PRODUCER_META_OFFSET
    fmt = CudaIpcRingBuffer.PRODUCER_META_FORMAT
    fd = os.open(address, os.O_RDONLY)
    try:
        mm = mmap.mmap(fd, 128, MAP_SHARED, PROT_READ)  # type: ignore[arg-type]
        try:
            mm.seek(offset)
            gpu_id, num_slots, width, height, channels = struct.unpack(fmt, mm.read(struct.calcsize(fmt)))
        finally:
            mm.close()
    finally:
        os.close(fd)
    return int(gpu_id), int(num_slots), int(width), int(height), int(channels)


class PeerUnavailableError(Exception):
    """Cross-GPU consume requested but no P2P/NVLink path exists (terminal — the
    caller must run inference on the producer's GPU on this host)."""


def _validate_header(producer_gpu, num_slots, width, height, channels):
    """Reject a zero/garbage header read during the producer's create/init race
    so the caller retries until the producer finishes writing it."""
    if num_slots <= 0 or width <= 0 or height <= 0 or channels <= 0:
        raise ValueError(
            f"producer header not ready (gpu={producer_gpu} slots={num_slots} w={width} h={height} ch={channels})"
        )
    dev_count = topology.device_count or (producer_gpu + 1)
    if producer_gpu < 0 or producer_gpu >= dev_count:
        raise ValueError(f"producer header gpu_id={producer_gpu} out of range (devices={dev_count})")


def resolve_decode_gpu(
    camera_id: str,
    node_id: str = "sg",
    port_name: str = "frames",
    max_retries: int = 10,
    retry_delay: float = 0.5,
) -> int:
    """Return the GPU the producer decoded this camera on, read from the ring-
    buffer header. CO-LOCATION (the supported cross-GPU strategy): the caller
    runs this camera's inference on the returned GPU so consume is zero-copy and
    no NVLink/P2P is needed. Retries while the producer is still initializing."""
    address = DataBus.compute_address(camera_id, node_id, port_name)
    last: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            pg, ns, w, h, ch = _read_producer_header(address)
            _validate_header(pg, ns, w, h, ch)
            return pg
        except (FileNotFoundError, ValueError) as e:
            last = e
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            raise
    raise last or RuntimeError(f"resolve_decode_gpu failed for {camera_id}")


class PeerReadRingBuffer(CudaIpcRingBuffer):
    """A consumer ring buffer that may attach to a producer on a DIFFERENT GPU.

    Reads return frames copied to the local device (one peer copy over NVLink)
    when the producer is on another GPU, and identical zero-copy views when the
    producer is on the same GPU.
    """

    def __init__(
        self,
        camera_id: str,
        gpu_id: int,
        num_slots: int,
        width: int,
        height: int,
        channels: int,
        is_producer: bool = False,
        *,
        producer_gpu_id: int,
    ) -> None:
        super().__init__(camera_id, gpu_id, num_slots, width, height, channels, is_producer)
        self._producer_gpu_id = producer_gpu_id
        self._same_gpu = producer_gpu_id == gpu_id

    def _to_local(self, frame):
        """Peer-copy a frame view (on the producer GPU) to a fresh local array.
        No-op for same-GPU (returns the zero-copy view)."""
        if frame is None or self._same_gpu:
            return frame
        with cp.cuda.Device(self.gpu_id):
            return frame.copy()  # DtoD over the enabled peer link (Model A)

    def read_frame(self, slot: int):
        return self._to_local(super().read_frame(slot))

    def read_latest(self):
        frame, idx = super().read_latest()
        return self._to_local(frame), idx

    def read_next(self):
        frame, idx, skipped = super().read_next()
        return self._to_local(frame), idx, skipped


class HostBounceRingBuffer(CudaIpcRingBuffer):
    """LAST-RESORT cross-GPU consumer for hosts WITHOUT NVLink/P2P.

    Why this exists / when it runs
    ------------------------------
    A CUDA-IPC handle can only be opened on the producer's OWN device, so a
    consumer on GPU Y cannot map a producer's GPU-X memory without P2P. This
    class connects on the PRODUCER GPU (same-device IPC -> always legal) and
    bounces every frame DtoH -> pinned host -> HtoD to the local inference GPU.

    This is a PCIe round trip per frame (~250 us @1080p NV12 with pinned host
    memory) and consumes PCIe bandwidth + a pinned host buffer per camera. It is
    a SAFETY NET ONLY: the supported path is CO-LOCATION (consume each camera on
    its decode GPU via resolve_decode_gpu()). It is OFF by default and only used
    when MATRICE_XGPU_FALLBACK=host_stage. It emits a throttled WARNING every
    MATRICE_XGPU_WARN_EVERY_SEC so the degradation is never silent.

    Precondition: the consumer process must see BOTH GPUs (do NOT pin
    CUDA_VISIBLE_DEVICES to a single device, or the producer GPU can't be mapped).
    """

    def __init__(
        self,
        camera_id: str,
        local_gpu_id: int,
        num_slots: int,
        width: int,
        height: int,
        channels: int,
        *,
        producer_gpu_id: int,
    ) -> None:
        # connect() maps the IPC handle on self.gpu_id -> set it to the PRODUCER
        # GPU so same-device ipcOpenMemHandle succeeds without P2P.
        super().__init__(camera_id, producer_gpu_id, num_slots, width, height, channels, is_producer=False)
        self._local_gpu_id = local_gpu_id
        self._producer_gpu_id = producer_gpu_id
        self._pinned = None  # cached pinned host staging allocation (lazy)
        self._host = None  # numpy view over self._pinned

    def _bounce(self, frame):
        if frame is None:
            return None
        _warn_throttled(
            self.camera_id,
            "%s: cross-GPU consume via HOST-BOUNCE (decode GPU %s -> inference "
            "GPU %s; no NVLink/P2P). PCIe round trip per frame = DEGRADED. "
            "Co-locate this camera's inference on GPU %s to remove this.",
            self.camera_id,
            self._producer_gpu_id,
            self._local_gpu_id,
            self._producer_gpu_id,
        )
        # DtoH on the producer device into a reusable PINNED host buffer (pinned
        # keeps the copy a fast DMA instead of a slow pageable memcpy).
        with cp.cuda.Device(_cvd_remap(self._producer_gpu_id)):
            if self._host is None or self._host.shape != frame.shape:
                self._pinned = cp.cuda.alloc_pinned_memory(frame.nbytes)
                self._host = np.frombuffer(self._pinned, dtype=np.uint8, count=frame.size).reshape(frame.shape)
            frame.get(out=self._host)  # DtoH into pinned host memory
        # HtoD on the local inference device.
        with cp.cuda.Device(_cvd_remap(self._local_gpu_id)):
            return cp.asarray(self._host)

    def read_frame(self, slot):
        return self._bounce(super().read_frame(slot))

    def read_latest(self):
        frame, idx = super().read_latest()
        return self._bounce(frame), idx

    def read_next(self):
        frame, idx, skipped = super().read_next()
        return self._bounce(frame), idx, skipped


class AutoConsumer:
    """Drop-in for the connector's use of a DataBus consumer: exposes ``.rb``
    (a PeerReadRingBuffer or HostBounceRingBuffer) and ``.close()``."""

    def __init__(self, rb: CudaIpcRingBuffer) -> None:
        self._rb = rb

    @property
    def rb(self) -> CudaIpcRingBuffer:
        return self._rb

    def is_stale(self) -> bool:
        try:
            return bool(self._rb.check_file_recreated())
        except Exception as e:  # noqa: BLE001
            # Fail safe: a failed staleness probe means we can't prove the
            # buffer is healthy → treat as stale so the caller reconnects,
            # rather than silently leaving a dead camera attached.
            logger.warning("is_stale check failed (%s); treating as stale", e)
            return True

    def close(self) -> None:
        try:
            self._rb.close()
        except Exception:  # noqa: BLE001
            pass


def consumer_auto(
    camera_id: str,
    node_id: str = "sg",
    port_name: str = "frames",
    fmt="cupy",
    consumer_key: str = "inference",
    local_gpu_id: Optional[int] = None,
    max_retries: int = 10,
    retry_delay: float = 0.5,
) -> AutoConsumer:
    """Connect a consumer that reads ``camera_id`` on ``local_gpu_id`` no matter
    which GPU the producer decoded on. Resolves the producer GPU from the header,
    enables peer access, and peer-copies frames into local memory.

    local_gpu_id=None means "the current cupy device" (the worker's inference GPU).
    """
    if not CUPY_AVAILABLE:
        raise RuntimeError("CuPy required for the auto CUDA consumer")
    parsed = _parse_format(fmt)
    if parsed not in (DataFormat.CUPY, DataFormat.TORCH):
        raise ValueError(f"consumer_auto is GPU-only; got format {parsed}")

    address = DataBus.compute_address(camera_id, node_id, port_name)
    if local_gpu_id is None:
        local_gpu_id = int(cp.cuda.runtime.getDevice())

    last_error: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            producer_gpu, num_slots, width, height, channels = _read_producer_header(address)
            _validate_header(producer_gpu, num_slots, width, height, channels)
            # Pick a transport from producer-vs-consumer GPU + P2P availability.
            #   same GPU            -> zero-copy view (PeerReadRingBuffer)
            #   different + P2P      -> one D2D peer copy (PeerReadRingBuffer)
            #   different + no P2P   -> host-bounce (opt-in) or terminal (default)
            # enable_peer() returns True for same-GPU, so the first branch covers
            # both fast paths (and short-circuits before touching peer access).
            same_gpu = producer_gpu == local_gpu_id
            rb: CudaIpcRingBuffer
            if same_gpu or topology.enable_peer(local_gpu_id, producer_gpu):
                rb = PeerReadRingBuffer(
                    camera_id,
                    local_gpu_id,
                    num_slots,
                    width,
                    height,
                    channels,
                    is_producer=False,
                    producer_gpu_id=producer_gpu,
                )
            elif _XGPU_FALLBACK == "host_stage":
                # No NVLink/P2P. Degrade instead of dying. NOT the supported path.
                logger.warning(
                    "%s: GPU %s cannot peer-access decode GPU %s (no NVLink/P2P); "
                    "using HOST-BOUNCE fallback (DEGRADED). Supported fix: co-locate "
                    "inference on GPU %s (see resolve_decode_gpu).",
                    camera_id,
                    local_gpu_id,
                    producer_gpu,
                    producer_gpu,
                )
                rb = HostBounceRingBuffer(
                    camera_id,
                    local_gpu_id,
                    num_slots,
                    width,
                    height,
                    channels,
                    producer_gpu_id=producer_gpu,
                )
            else:
                # Fail fast + clearly (rather than faulting mid-stream and
                # masquerading as an IPC error) so the operator co-locates.
                raise PeerUnavailableError(
                    f"{camera_id}: GPU {local_gpu_id} cannot peer-access producer "
                    f"GPU {producer_gpu} (no NVLink/P2P). Co-locate inference on GPU "
                    f"{producer_gpu} (resolve_decode_gpu), or set "
                    f"MATRICE_XGPU_FALLBACK=host_stage to degrade via host-bounce."
                )
            rb.meta_shm_name = f"databus__{camera_id}__{node_id}__{port_name}"
            rb.meta_shm_path = address
            rb._consumer_key = consumer_key
            if not rb.connect():
                raise RuntimeError(f"auto consumer connect() returned False for {camera_id}")
            rb._consumer_id = rb._register_consumer_key(consumer_key)
            if producer_gpu != local_gpu_id and not isinstance(rb, HostBounceRingBuffer):
                logger.info(
                    "%s: auto consumer on GPU %s <- producer GPU %s (NVLink peer copy)",
                    camera_id,
                    local_gpu_id,
                    producer_gpu,
                )
            return AutoConsumer(rb)
        except PeerUnavailableError:
            raise  # terminal — never spin on a host that can't peer
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            # Producer not created/initialized yet, or mid-restart — wait & retry.
            last_error = e
            if attempt < max_retries - 1:
                if attempt == 0 or attempt == max_retries // 2:
                    logger.info("%s: producer not ready (%s); waiting for SG...", camera_id, e)
                time.sleep(retry_delay)
                continue
            raise
    raise last_error or RuntimeError(f"consumer_auto failed for {camera_id}")
