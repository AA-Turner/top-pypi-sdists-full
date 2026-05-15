"""DataBus — Unified data transport abstraction for the Matrice pipeline.

Wraps existing ring buffers (CudaIpcRingBuffer, ShmRingBuffer) with:
- Deterministic SHM addressing: /dev/shm/databus__{camera_id}__{node_id}__{port_name}
- Auto-selected transport based on data format (CUDA IPC for GPU, POSIX SHM for CPU)
- Multi-consumer with independent cursors (up to 32 readers per channel)
- Producer never blocks (overwrite-on-wrap semantics)

Usage:
    # Producer (inference container publishes detections)
    producer = DataBus.producer("cam_001", "yolo", "detection0", "json")
    producer.publish({"detections": [...]}, {"frame_idx": 1})
    producer.close()

    # Consumer (analytics container reads detections)
    consumer = DataBus.consumer("cam_001", "yolo", "detection0", "json", consumer_key="analytics")
    data, meta = consumer.consume()
    consumer.ack(meta["frame_idx"])
    consumer.close()

    # GPU frame transport (streaming gateway -> inference)
    producer = DataBus.producer("cam_001", "sg", "frames", "cupy", gpu_id=0, width=640, height=960)
    producer.publish(nv12_gpu_frame, {"timestamp_ns": 123456, "rtp_timestamp": 0})
    producer.close()
"""

import enum
import logging
import os
import struct
import time
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)

# /dev/shm is the canonical POSIX shared memory path; override via env var if needed.
SHM_BASE_PATH = os.getenv("MATRICE_SHM_PATH", "/dev/shm")  # nosec B108

# ─── Lazy imports (avoid hard dependency on cupy/torch at import time) ───────
_cupy = None
_torch = None


def _get_cupy():
    global _cupy
    if _cupy is None:
        try:
            import cupy

            _cupy = cupy
        except ImportError:
            pass
    return _cupy


def _get_torch():
    global _torch
    if _torch is None:
        try:
            import torch

            _torch = torch
        except ImportError:
            pass
    return _torch


# ─── JSON serialization with orjson fallback ─────────────────────────────────
try:
    import orjson

    def _json_dumps(obj: Any) -> bytes:
        return orjson.dumps(obj)

    def _json_loads(data: bytes) -> Any:
        return orjson.loads(data)
except ImportError:
    import json

    def _json_dumps(obj: Any) -> bytes:
        return json.dumps(obj).encode("utf-8")

    def _json_loads(data: bytes) -> Any:
        return json.loads(data if isinstance(data, str) else data.decode("utf-8"))


def _shm_bytes_to_gpu(
    msg_bytes: bytes,
    metadata: Dict,
    target_format: "DataFormat",
    gpu_id: int,
) -> Any:
    """Convert POSIX SHM bytes to GPU tensor (cross-format conversion).

    Handles JPEG-encoded bytes and raw BGR numpy arrays. Decodes to numpy,
    then uploads to GPU via cupy.asarray(). Returns cupy array (or torch tensor).

    The producer's metadata["format"] field tells us how to decode:
      "jpeg" → cv2.imdecode
      "bgr"  → np.frombuffer + reshape using metadata width/height
      (missing) → treat as raw numpy uint8
    """
    import cv2

    producer_format = metadata.get("format", "")
    width = metadata.get("width", 0)
    height = metadata.get("height", 0)

    if producer_format == "jpeg":
        # JPEG bytes → BGR numpy
        np_buf = np.frombuffer(msg_bytes, dtype=np.uint8)
        frame = cv2.imdecode(np_buf, cv2.IMREAD_COLOR)
        if frame is None:
            logger.warning("DataBus: JPEG decode failed in cross-format conversion")
            return np.frombuffer(msg_bytes, dtype=np.uint8)
    elif producer_format == "bgr" and width > 0 and height > 0:
        # Raw BGR bytes → numpy reshape
        frame = np.frombuffer(msg_bytes, dtype=np.uint8).reshape(height, width, 3)
    else:
        # Unknown format — return as 1D uint8 array on GPU
        frame = np.frombuffer(msg_bytes, dtype=np.uint8)

    # Upload to GPU
    cp = _get_cupy()
    if cp is not None:
        with cp.cuda.Device(gpu_id):
            gpu_data = cp.asarray(frame)
        # Wrap as torch if requested
        if target_format == DataFormat.TORCH:
            torch = _get_torch()
            if torch is not None:
                return torch.as_tensor(gpu_data, device=f"cuda:{gpu_id}")
        return gpu_data

    # No cupy available — return numpy
    return frame


class DataFormat(enum.Enum):
    """Data format declaration — determines transport auto-selection."""

    CUPY = "cupy"  # GPU tensor → CUDA IPC transport
    NUMPY = "numpy"  # CPU array → POSIX SHM transport
    TORCH = "torch"  # GPU tensor → CUDA IPC transport
    JSON = "json"  # Dict/list → POSIX SHM with orjson
    BYTES = "bytes"  # Raw bytes → POSIX SHM


def _parse_format(fmt: Union[str, DataFormat]) -> DataFormat:
    """Accept string or enum, return DataFormat."""
    if isinstance(fmt, DataFormat):
        return fmt
    return DataFormat(fmt)


def _select_transport(fmt: DataFormat) -> str:
    """Select transport backend based on format and platform (used by producers)."""
    if fmt in (DataFormat.CUPY, DataFormat.TORCH):
        platform = os.environ.get("MATRICE_PLATFORM", "").lower()
        if platform == "orin":
            return "orin_shm"
        return "cuda_ipc"
    return "posix_shm"


def _probe_shm_header(file_path: str) -> Optional[str]:
    """Probe SHM file header to identify the transport type.

    Unified ShmRingBuffer v2 (768B header):
        magic at offset 676 = 0x4D415452 ("MATR") → "posix_shm"

    Legacy ShmRingBuffer v1 (<QIIIIQ, 32 bytes):
        height==1, format in {0,1,2}, slot_count > 0 → "posix_shm"

    CudaIpcRingBuffer (<QQQQIIIIIIQ, 80 bytes):
        Anything else → "cuda_ipc" (or "orin_shm" if MATRICE_PLATFORM=orin)

    Returns "posix_shm", "cuda_ipc", "orin_shm", or None if inconclusive.
    """
    try:
        fd = os.open(file_path, os.O_RDONLY)
        try:
            raw = os.read(fd, 684)  # enough to read magic at offset 676
        finally:
            os.close(fd)
    except OSError:
        return None

    if len(raw) < 32:
        return None

    # Check for unified v2 magic at offset 676
    if len(raw) >= 680:
        magic = struct.unpack_from("<I", raw, 676)[0]
        if magic == 0x4D415452:  # "MATR"
            return "posix_shm"

    # Legacy v1 ShmRingBuffer: bytes 8-24 as four uint32 values
    val = struct.unpack_from("<IIII", raw, 8)
    height = val[1]
    frame_format = val[2]
    slot_count = val[3]
    if height == 1 and frame_format in (0, 1, 2) and 0 < slot_count <= 10000:
        return "posix_shm"

    # Non-POSIX SHM — check for Orin platform
    platform = os.environ.get("MATRICE_PLATFORM", "").lower()
    if platform == "orin":
        return "orin_shm"

    return "cuda_ipc"


def _detect_producer_transport(address: str, requested_fmt: DataFormat) -> str:
    """Detect which transport the producer actually used at this address.

    Probes the SHM file header to distinguish CUDA IPC from POSIX SHM,
    since both transports write to the same /dev/shm/ path. Falls back to
    format-based selection if the file doesn't exist yet (producer not started).

    This enables transparent cross-format consumption: a consumer can request
    'cupy' format and DataBus will auto-detect if the producer wrote POSIX SHM
    (bytes/numpy) and handle the conversion.
    """
    shm_basename = os.path.basename(address)
    # /dev/shm is the canonical POSIX shared memory location on Linux.
    posix_shm_path = f"/dev/shm/{shm_basename}"  # nosec B108

    # Find the SHM file — check both the computed address and /dev/shm/ fallback
    file_path = None
    if os.path.exists(address):
        file_path = address
    elif address != posix_shm_path and os.path.exists(posix_shm_path):
        file_path = posix_shm_path

    if file_path is None:
        # File doesn't exist yet — fall back to format-based selection
        return _select_transport(requested_fmt)

    # Probe header to distinguish transport type
    transport = _probe_shm_header(file_path)
    if transport is not None:
        return transport

    # Probe inconclusive — fall back to format-based selection
    return _select_transport(requested_fmt)


class DataBus:
    """Unified data transport — all methods are static, no state held."""

    @staticmethod
    def compute_address(camera_id: str, node_id: str, port_name: str) -> str:
        """Compute deterministic SHM path. Pure function, no I/O."""
        return f"{SHM_BASE_PATH}/databus__{camera_id}__{node_id}__{port_name}"

    @staticmethod
    def producer(
        camera_id: str,
        node_id: str,
        port_name: str,
        format: Union[str, DataFormat],
        *,
        gpu_id: int = 0,
        num_slots: int = 64,
        max_msg_size: int = 65536,
        width: int = 0,
        height: int = 0,
    ) -> "DataBusProducer":
        """Create a producer at the deterministic address.

        Args:
            camera_id: Camera identifier
            node_id: Node identifier (e.g., "sg", "yolo", "output")
            port_name: Output port name (e.g., "frames", "detection0")
            format: Data format — determines transport auto-selection
            gpu_id: GPU device ID (for cupy/torch formats)
            num_slots: Ring buffer slot count
            max_msg_size: Max message size in bytes (for json/bytes/numpy formats)
            width: Frame width (for cupy format, NV12: actual pixel width)
            height: Frame height (for cupy format, NV12: H*1.5)
        """
        fmt = _parse_format(format)
        transport = _select_transport(fmt)
        address = DataBus.compute_address(camera_id, node_id, port_name)
        return DataBusProducer(
            address=address,
            fmt=fmt,
            transport=transport,
            camera_id=camera_id,
            gpu_id=gpu_id,
            num_slots=num_slots,
            max_msg_size=max_msg_size,
            width=width,
            height=height,
        )

    @staticmethod
    def consumer(
        camera_id: str,
        node_id: str,
        port_name: str,
        format: Union[str, DataFormat],
        consumer_key: str = "default",
        *,
        gpu_id: int = 0,
    ) -> "DataBusConsumer":
        """Create a consumer at the deterministic address.

        Auto-detects the transport the producer used (CUDA IPC vs POSIX SHM)
        and handles format conversion transparently. The consumer always gets
        data in the requested format regardless of how the producer wrote it.

        Args:
            camera_id: Camera identifier
            node_id: Node identifier
            port_name: Port name
            format: Desired data format — auto-converts if producer format differs
            consumer_key: Consumer group ID (independent cursor per key)
            gpu_id: GPU device ID (for cupy/torch formats)
        """
        fmt = _parse_format(format)
        address = DataBus.compute_address(camera_id, node_id, port_name)
        transport = _detect_producer_transport(address, fmt)
        return DataBusConsumer(
            address=address,
            fmt=fmt,
            transport=transport,
            consumer_key=consumer_key,
            gpu_id=gpu_id,
        )


# ─── Length-prefixed wire format for POSIX SHM slots ─────────────────────────
# Each slot: [4B msg_len (uint32)][4B meta_len (uint32)][msg_bytes][meta_bytes][padding]
_LENGTH_PREFIX_SIZE = 8  # 4 + 4 bytes
_LENGTH_PREFIX_FMT = "<II"


class DataBusProducer:
    """Produces data to a DataBus channel.

    Wraps CudaIpcRingBuffer (for cupy/torch) or ShmRingBuffer (for json/bytes/numpy).
    """

    def __init__(self, address: str, fmt: DataFormat, transport: str, camera_id: str = "", **config):
        self._address = address
        self._format = fmt
        self._transport = transport
        self._camera_id = camera_id
        self._rb = None  # underlying ring buffer
        self._max_msg_size = config.get("max_msg_size", 65536)
        self._slot_frame_size = 0  # actual frame_size in ShmRingBuffer
        self._initialize(**config)

    def _initialize(self, **config):
        shm_basename = os.path.basename(self._address)

        if self._transport == "cuda_ipc":
            self._init_cuda_ipc(shm_basename, config)
        elif self._transport == "posix_shm":
            self._init_posix_shm(shm_basename, config)
        elif self._transport == "orin_shm":
            self._init_orin_shm(shm_basename, config)
        else:
            raise ValueError(f"Unknown transport: {self._transport}")

    def _init_cuda_ipc(self, shm_basename: str, config: dict):
        from .cuda_shm_ring_buffer import CudaIpcRingBuffer

        gpu_id = config.get("gpu_id", 0)
        num_slots = config.get("num_slots", 32)
        width = config.get("width", 640)
        height = config.get("height", 960)

        rb = CudaIpcRingBuffer(
            camera_id=shm_basename,
            gpu_id=gpu_id,
            num_slots=num_slots,
            width=width,
            height=height,
            channels=1,
            is_producer=True,
        )
        # Override SHM path to DataBus deterministic address
        rb.meta_shm_name = shm_basename
        rb.meta_shm_path = self._address
        rb.initialize()
        self._rb = rb

    def _init_posix_shm(self, shm_basename: str, config: dict):
        from .shm_ring_buffer import ShmRingBuffer

        num_slots = config.get("num_slots", 64)
        max_msg_size = self._max_msg_size

        rb = ShmRingBuffer(
            camera_id=self._camera_id or shm_basename,
            max_msg_size=max_msg_size,
            num_slots=num_slots,
            is_producer=True,
            shm_name=shm_basename,
        )
        rb.initialize()
        self._rb = rb
        self._slot_frame_size = rb.frame_size

    def _init_orin_shm(self, shm_basename: str, config: dict):
        from .shm_ring_buffer import ShmRingBuffer

        gpu_id = config.get("gpu_id", 0)
        num_slots = config.get("num_slots", 32)
        width = config.get("width", 640)
        height = config.get("height", 960)

        rb = ShmRingBuffer(
            camera_id=shm_basename,
            gpu_id=gpu_id,
            num_slots=num_slots,
            width=width,
            height=height,
            channels=1,
            is_producer=True,
            shm_name=shm_basename,
        )
        rb.meta_shm_name = shm_basename
        rb.meta_shm_path = self._address
        rb.initialize()
        self._rb = rb

    def publish(self, data: Any, metadata: Optional[Dict] = None) -> int:
        """Publish data with optional metadata. Returns frame_idx.

        For cupy/torch: data is a GPU array, metadata keys used:
            timestamp_ns, rtp_timestamp
        For json: data is a dict/list, serialized with orjson
        For bytes: data is bytes
        For numpy: data is a numpy array, serialized with tobytes()
        """
        if self._transport in ("cuda_ipc", "orin_shm"):
            return self._publish_gpu(data, metadata)
        else:
            return self._publish_shm(data, metadata)

    def _publish_gpu(self, data: Any, metadata: Optional[Dict]) -> int:
        meta = metadata or {}
        timestamp_ns = meta.get("timestamp_ns", None)
        rtp_timestamp = meta.get("rtp_timestamp", 0)

        # Convert torch tensor to cupy if needed
        if self._format == DataFormat.TORCH:
            cp = _get_cupy()
            if cp is None:
                raise RuntimeError("CuPy required for torch→cupy conversion")
            import cupy

            data = cupy.asarray(data)

        return self._rb.write_frame_fast(
            data,
            sync=False,
            timestamp_ns=timestamp_ns,
            rtp_timestamp=rtp_timestamp,
        )

    def _publish_shm(self, data: Any, metadata: Optional[Dict]) -> int:
        meta = metadata or {}

        # Serialize data based on format
        if self._format == DataFormat.JSON:
            msg_bytes = _json_dumps(data)
        elif self._format == DataFormat.BYTES:
            msg_bytes = data if isinstance(data, (bytes, bytearray)) else bytes(data)
        elif self._format == DataFormat.NUMPY:
            if isinstance(data, np.ndarray):
                msg_bytes = data.tobytes()
            else:
                msg_bytes = bytes(data)
        else:
            msg_bytes = _json_dumps(data)

        # Serialize metadata
        meta_bytes = _json_dumps(meta) if meta else b"{}"

        # Build length-prefixed payload
        msg_len = len(msg_bytes)
        meta_len = len(meta_bytes)
        total_needed = _LENGTH_PREFIX_SIZE + msg_len + meta_len

        if total_needed > self._slot_frame_size:
            logger.warning(
                f"DataBus: message too large ({total_needed} > {self._slot_frame_size}), truncating metadata"
            )
            # Truncate metadata to fit
            max_meta = self._slot_frame_size - _LENGTH_PREFIX_SIZE - msg_len
            if max_meta < 2:
                # Even message alone is too large — this is a config error
                raise ValueError(
                    f"Message payload ({msg_len} bytes) exceeds slot size "
                    f"({self._slot_frame_size - _LENGTH_PREFIX_SIZE} bytes). "
                    f"Increase max_msg_size."
                )
            meta_bytes = meta_bytes[:max_meta]
            meta_len = len(meta_bytes)

        # Pack: [4B msg_len][4B meta_len][msg][meta][zero-pad]
        header = struct.pack(_LENGTH_PREFIX_FMT, msg_len, meta_len)
        payload = bytearray(self._slot_frame_size)
        payload[:4] = header[:4]
        payload[4:8] = header[4:8]
        payload[8 : 8 + msg_len] = msg_bytes
        payload[8 + msg_len : 8 + msg_len + meta_len] = meta_bytes

        frame_idx, _slot = self._rb.write_frame(bytes(payload))
        return frame_idx

    def close(self):
        """Close and cleanup underlying ring buffer."""
        if self._rb is not None:
            self._rb.close()
            self._rb = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @property
    def rb(self):
        """Access the underlying ring buffer for advanced operations."""
        return self._rb

    def __repr__(self):
        return f"DataBusProducer(address={self._address!r}, format={self._format.value})"


class DataBusConsumer:
    """Consumes data from a DataBus channel.

    Wraps CudaIpcRingBuffer (for cupy/torch) or ShmRingBuffer (for json/bytes/numpy).
    """

    def __init__(self, address: str, fmt: DataFormat, transport: str, consumer_key: str = "default", gpu_id: int = 0):
        self._address = address
        self._format = fmt
        self._transport = transport
        self._consumer_key = consumer_key
        self._gpu_id = gpu_id
        self._rb = None
        self._last_consumed_idx = 0
        self._connected = False
        self._connect()

    def _connect(self):
        shm_basename = os.path.basename(self._address)

        if self._transport == "cuda_ipc":
            self._connect_cuda_ipc(shm_basename)
        elif self._transport == "posix_shm":
            self._connect_posix_shm(shm_basename)
        elif self._transport == "orin_shm":
            self._connect_orin_shm(shm_basename)
        else:
            raise ValueError(f"Unknown transport: {self._transport}")

        self._connected = True

    def _connect_cuda_ipc(self, shm_basename: str):
        from .cuda_shm_ring_buffer import CudaIpcRingBuffer

        # Read header from the DataBus address to get dimensions
        cp = _get_cupy()
        if cp is None:
            raise RuntimeError("CuPy required for CUDA IPC consumer")

        # Warm GPU context
        with cp.cuda.Device(self._gpu_id):
            _ = cp.zeros(1, dtype=cp.uint8)

        import mmap as mmap_mod

        fd = os.open(self._address, os.O_RDONLY, 0o666)
        mm = mmap_mod.mmap(fd, 128, mmap_mod.MAP_SHARED, mmap_mod.PROT_READ)
        mm.seek(32)
        gpu_id_stored = struct.unpack("<I", mm.read(4))[0]
        num_slots = struct.unpack("<I", mm.read(4))[0]
        width = struct.unpack("<I", mm.read(4))[0]
        height = struct.unpack("<I", mm.read(4))[0]
        channels = struct.unpack("<I", mm.read(4))[0]
        mm.close()
        os.close(fd)

        if gpu_id_stored != self._gpu_id:
            raise RuntimeError(f"GPU mismatch: producer used GPU {gpu_id_stored}, consumer trying GPU {self._gpu_id}")

        rb = CudaIpcRingBuffer(
            camera_id=shm_basename,
            gpu_id=self._gpu_id,
            num_slots=num_slots,
            width=width,
            height=height,
            channels=channels,
            is_producer=False,
        )
        # Override SHM path to DataBus address
        rb.meta_shm_name = shm_basename
        rb.meta_shm_path = self._address
        rb._consumer_key = self._consumer_key

        if not rb.connect():
            raise RuntimeError(f"Failed to connect consumer to {self._address}")

        rb._consumer_id = rb._register_consumer_key(self._consumer_key)
        self._rb = rb

    def _connect_posix_shm(self, shm_basename: str):
        import mmap as mmap_mod

        from .shm_ring_buffer import ShmRingBuffer

        meta_path = self._address
        try:
            fd = os.open(meta_path, os.O_RDONLY)
        except FileNotFoundError:
            raise FileNotFoundError(f"DataBus channel not found: {self._address}. Ensure producer is running first.")

        try:
            mm = mmap_mod.mmap(fd, ShmRingBuffer.HEADER_SIZE, mmap_mod.MAP_SHARED, mmap_mod.PROT_READ)
            # Read dimensions from unified header
            mm.seek(ShmRingBuffer._OFF_NUM_SLOTS)
            num_slots = struct.unpack("<I", mm.read(4))[0]
            width = struct.unpack("<I", mm.read(4))[0]
            height = struct.unpack("<I", mm.read(4))[0]
            channels = struct.unpack("<I", mm.read(4))[0]
            # Read extended fields
            mm.seek(ShmRingBuffer._OFF_FRAME_FORMAT)
            frame_format = struct.unpack("<I", mm.read(4))[0]
            mm.seek(ShmRingBuffer._OFF_MAGIC)
            magic = struct.unpack("<I", mm.read(4))[0]
            if magic != ShmRingBuffer.MAGIC:
                frame_format = ShmRingBuffer.FORMAT_RAW
            mm.close()
        finally:
            os.close(fd)

        rb = ShmRingBuffer(
            camera_id=shm_basename,
            num_slots=num_slots,
            width=width,
            height=height,
            channels=channels,
            frame_format=frame_format,
            is_producer=False,
            shm_name=shm_basename,
        )
        if not rb.connect():
            raise RuntimeError(f"Failed to connect consumer to {self._address}")
        self._rb = rb

    def _connect_orin_shm(self, shm_basename: str):
        import mmap as mmap_mod

        from .shm_ring_buffer import ShmRingBuffer

        fd = os.open(self._address, os.O_RDONLY, 0o666)
        mm = mmap_mod.mmap(fd, ShmRingBuffer.HEADER_SIZE, mmap_mod.MAP_SHARED, mmap_mod.PROT_READ)
        mm.seek(ShmRingBuffer._OFF_GPU_ID)
        gpu_id_stored = struct.unpack("<I", mm.read(4))[0]
        num_slots = struct.unpack("<I", mm.read(4))[0]
        width = struct.unpack("<I", mm.read(4))[0]
        height = struct.unpack("<I", mm.read(4))[0]
        channels = struct.unpack("<I", mm.read(4))[0]
        mm.close()
        os.close(fd)

        rb = ShmRingBuffer(
            camera_id=shm_basename,
            gpu_id=self._gpu_id,
            num_slots=num_slots,
            width=width,
            height=height,
            channels=channels,
            is_producer=False,
            shm_name=shm_basename,
        )
        rb.meta_shm_name = shm_basename
        rb.meta_shm_path = self._address
        rb._consumer_key = self._consumer_key
        if not rb.connect():
            raise RuntimeError(f"Failed to connect Orin consumer to {self._address}")
        rb._consumer_id = rb._register_consumer_key(self._consumer_key)
        self._rb = rb

    def consume(self) -> Tuple[Optional[Any], Optional[Dict]]:
        """Read next unread message.

        Returns:
            (data, metadata) or (None, None) if no new data.
            For cupy: data is a GPU array view (must stay alive during use)
            For json: data is a dict/list
            For bytes: data is bytes
            For numpy: data is np.ndarray (1D uint8, caller reshapes)
        """
        if not self._connected:
            return None, None

        if self._transport in ("cuda_ipc", "orin_shm"):
            return self._consume_gpu()
        else:
            return self._consume_shm()

    def _consume_gpu(self) -> Tuple[Optional[Any], Optional[Dict]]:
        frame, frame_idx, was_skipped = self._rb.read_next()
        if frame is None:
            return None, None

        # Read slot metadata for timestamps
        slot = (frame_idx - 1) % self._rb.num_slots
        _fidx, timestamp_ns, flags, rtp_timestamp = self._rb._read_slot_meta(slot)

        metadata = {
            "frame_idx": frame_idx,
            "timestamp_ns": timestamp_ns,
            "rtp_timestamp": rtp_timestamp,
            "was_skipped": was_skipped,
            "width": self._rb.width,
            "height": self._rb.height,
        }

        # Format conversion if needed
        if self._format == DataFormat.NUMPY:
            cp = _get_cupy()
            if cp is not None:
                data = cp.asnumpy(frame)
            else:
                data = frame
        elif self._format == DataFormat.TORCH:
            torch = _get_torch()
            if torch is not None:
                data = torch.as_tensor(frame, device=f"cuda:{self._gpu_id}")
            else:
                data = frame
        else:
            data = frame

        return data, metadata

    def _consume_gpu_latest(self) -> Tuple[Optional[Any], Optional[Dict]]:
        """Read the latest frame from GPU ring buffer, skipping intermediates."""
        write_idx = self._rb.get_write_idx()
        if write_idx <= 0 or write_idx <= self._last_consumed_idx:
            return None, None

        frame_idx = write_idx
        slot = (frame_idx - 1) % self._rb.num_slots
        frame = self._rb.read_frame(slot)
        if frame is None:
            return None, None

        _fidx, timestamp_ns, flags, rtp_timestamp = self._rb._read_slot_meta(slot)

        metadata = {
            "frame_idx": frame_idx,
            "timestamp_ns": timestamp_ns,
            "rtp_timestamp": rtp_timestamp,
            "was_skipped": frame_idx - self._last_consumed_idx > 1,
            "width": self._rb.width,
            "height": self._rb.height,
        }

        # Format conversion if needed
        if self._format == DataFormat.NUMPY:
            cp = _get_cupy()
            if cp is not None:
                data = cp.asnumpy(frame)
            else:
                data = frame
        elif self._format == DataFormat.TORCH:
            torch = _get_torch()
            if torch is not None:
                data = torch.as_tensor(frame, device=f"cuda:{self._gpu_id}")
            else:
                data = frame
        else:
            data = frame

        self._last_consumed_idx = frame_idx
        return data, metadata

    def _consume_shm(self) -> Tuple[Optional[Any], Optional[Dict]]:
        current_write = self._rb.get_current_frame_idx()
        next_idx = self._last_consumed_idx + 1

        if next_idx > current_write:
            return None, None  # No new messages

        # Skip if too far behind
        if current_write - next_idx >= self._rb.slot_count:
            next_idx = current_write - self._rb.slot_count + 1

        # Read frame data (copy to avoid torn reads)
        raw = self._rb.read_frame_copy(next_idx)
        if raw is None:
            self._last_consumed_idx = next_idx
            return None, None

        # Decode length-prefixed message
        if len(raw) < _LENGTH_PREFIX_SIZE:
            self._last_consumed_idx = next_idx
            return None, None

        msg_len, meta_len = struct.unpack(_LENGTH_PREFIX_FMT, raw[:_LENGTH_PREFIX_SIZE])

        # Bounds check
        if msg_len + meta_len + _LENGTH_PREFIX_SIZE > len(raw):
            logger.warning(f"DataBus: corrupt message at idx {next_idx}, skipping")
            self._last_consumed_idx = next_idx
            return None, None

        msg_bytes = raw[_LENGTH_PREFIX_SIZE : _LENGTH_PREFIX_SIZE + msg_len]
        meta_bytes = raw[_LENGTH_PREFIX_SIZE + msg_len : _LENGTH_PREFIX_SIZE + msg_len + meta_len]

        # Deserialize metadata first (needed for format-aware conversion)
        try:
            metadata = _json_loads(meta_bytes) if meta_bytes else {}
        except Exception:
            metadata = {}
        metadata["frame_idx"] = next_idx

        # Deserialize data based on requested format
        if self._format in (DataFormat.CUPY, DataFormat.TORCH):
            # Cross-format: consumer wants GPU tensor but producer wrote CPU data.
            # Decode bytes → numpy → upload to GPU.
            data = _shm_bytes_to_gpu(msg_bytes, metadata, self._format, self._gpu_id)
        elif self._format == DataFormat.JSON:
            data = _json_loads(msg_bytes)
        elif self._format == DataFormat.BYTES:
            data = bytes(msg_bytes)
        elif self._format == DataFormat.NUMPY:
            data = np.frombuffer(msg_bytes, dtype=np.uint8)
        else:
            data = _json_loads(msg_bytes)

        self._last_consumed_idx = next_idx
        return data, metadata

    def _consume_shm_latest(self) -> Tuple[Optional[Any], Optional[Dict]]:
        """Read the latest message from SHM ring buffer, skipping intermediates."""
        current_write = self._rb.get_current_frame_idx()

        if current_write <= 0 or current_write <= self._last_consumed_idx:
            return None, None

        # Jump straight to the latest frame
        next_idx = current_write

        raw = self._rb.read_frame_copy(next_idx)
        if raw is None:
            self._last_consumed_idx = next_idx
            return None, None

        if len(raw) < _LENGTH_PREFIX_SIZE:
            self._last_consumed_idx = next_idx
            return None, None

        msg_len, meta_len = struct.unpack(_LENGTH_PREFIX_FMT, raw[:_LENGTH_PREFIX_SIZE])

        if msg_len + meta_len + _LENGTH_PREFIX_SIZE > len(raw):
            logger.warning(f"DataBus: corrupt message at idx {next_idx}, skipping")
            self._last_consumed_idx = next_idx
            return None, None

        msg_bytes = raw[_LENGTH_PREFIX_SIZE : _LENGTH_PREFIX_SIZE + msg_len]
        meta_bytes = raw[_LENGTH_PREFIX_SIZE + msg_len : _LENGTH_PREFIX_SIZE + msg_len + meta_len]

        try:
            metadata = _json_loads(meta_bytes) if meta_bytes else {}
        except Exception:
            metadata = {}
        metadata["frame_idx"] = next_idx
        metadata["was_skipped"] = next_idx - self._last_consumed_idx > 1

        if self._format in (DataFormat.CUPY, DataFormat.TORCH):
            data = _shm_bytes_to_gpu(msg_bytes, metadata, self._format, self._gpu_id)
        elif self._format == DataFormat.JSON:
            data = _json_loads(msg_bytes)
        elif self._format == DataFormat.BYTES:
            data = bytes(msg_bytes)
        elif self._format == DataFormat.NUMPY:
            data = np.frombuffer(msg_bytes, dtype=np.uint8)
        else:
            data = _json_loads(msg_bytes)

        self._last_consumed_idx = next_idx
        return data, metadata

    def consume_latest(self) -> Tuple[Optional[Any], Optional[Dict]]:
        """Read the latest available message, skipping all intermediate frames.

        Use this instead of consume() when the consumer is slower than the
        producer and you want overlays to stay in sync with the live video
        (e.g., ML inference at 10 FPS reading from a 30 FPS stream).

        Returns:
            (data, metadata) or (None, None) if no new data.
            metadata includes 'was_skipped' (bool) indicating if frames were dropped.
        """
        if not self._connected:
            return None, None

        if self._transport in ("cuda_ipc", "orin_shm"):
            return self._consume_gpu_latest()
        else:
            return self._consume_shm_latest()

    def ack(self, frame_idx: int):
        """Acknowledge consumption up to frame_idx.

        For CUDA IPC: updates per-consumer cursor in SHM.
        For POSIX SHM: updates local tracking only.
        """
        if self._transport in ("cuda_ipc", "orin_shm"):
            self._rb.ack_frame_done(frame_idx)
        self._last_consumed_idx = frame_idx

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def address(self) -> str:
        return self._address

    @property
    def rb(self):
        """Access the underlying ring buffer for advanced operations."""
        return self._rb

    def is_stale(self) -> bool:
        """Check if the underlying ring buffer's SHM file has been recreated.

        This indicates the producer restarted and our connection points to
        stale data. Caller should close this consumer and create a new one.

        Returns:
            True if stale (producer restarted), False if still valid.
        """
        if self._rb is None or not self._connected:
            return True
        if hasattr(self._rb, "check_file_recreated"):
            return self._rb.check_file_recreated()
        return False

    def close(self):
        """Close and cleanup."""
        if self._rb is not None:
            self._rb.close()
            self._rb = None
        self._connected = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        return f"DataBusConsumer(address={self._address!r}, format={self._format.value}, key={self._consumer_key!r})"
