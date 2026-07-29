#!/usr/bin/env python3
"""Unified POSIX SHM Ring Buffer for frame and message storage.

Merges the best features from OrinShmRingBuffer (multi-consumer, GPU frames,
session info) and the original ShmRingBuffer (torn frame detection, health
monitoring, crash detection) into a single class.

Architecture:
- Producer creates SHM and writes frames/messages in a ring pattern
- Up to 32 consumers attach and read independently with per-consumer cursors
- Overwrite is allowed (producer never waits for consumers)
- Consumers detect overwritten frames via frame_idx validation
- Torn frame detection via seq_start/seq_end odd/even semantics

SHM Layout (2 files per buffer):
    /dev/shm/{name}         - Metadata (768B header + 48B per-slot metadata)
    /dev/shm/{name}_frames  - Frame data (page-aligned slots)

Uses os.open + mmap (not multiprocessing.shared_memory) to avoid
resource_tracker auto-unlinking issues in multi-process deployments.

Version History:
- v1.0: Original ShmRingBuffer (single-file, no multi-consumer)
- v1.1: Health check APIs, cleanup utilities
- v2.0: Unified with OrinShmRingBuffer (multi-consumer, GPU, session info,
         torn frame detection, 2-file layout, page alignment)
"""

from __future__ import annotations

__version__ = "2.0.0"

import logging
import mmap
import os
import struct
import time
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

# /dev/shm is the canonical POSIX shared memory path; override via env var if needed.
SHM_BASE_PATH = os.getenv("MATRICE_SHM_PATH", "/dev/shm")  # nosec B108
MAP_SHARED = getattr(mmap, "MAP_SHARED", 1)
PROT_READ = getattr(mmap, "PROT_READ", 1)
PROT_WRITE = getattr(mmap, "PROT_WRITE", 2)

try:
    import cupy as cp

    CUPY_AVAILABLE = True
except ImportError:
    cp = None  # type: ignore[assignment]
    CUPY_AVAILABLE = False

# CUDA IPC handle size (64 bytes, zeroed — reserved for CudaIpcRingBuffer compat)
CUDA_IPC_HANDLE_SIZE = 64


class ShmRingBuffer:
    """Unified POSIX SHM ring buffer with multi-consumer support,
    torn frame detection, GPU frame support, and health monitoring.

    Supports two usage modes:
    - GPU frame streaming: width/height/channels for raw video frames
    - Message passing: max_msg_size for serialized JSON/bytes (DataBus)

    Header layout (768 bytes):
      0-7:     write_idx (Q)
      8-15:    read_idx (Q, legacy compat)
      16-23:   frame_count (Q, = write_idx)
      24-31:   timestamp_ns (Q, heartbeat)
      32-35:   gpu_id (I)
      36-39:   num_slots (I)
      40-43:   width (I)
      44-47:   height (I)
      48-51:   channels (I)
      52-55:   dtype_code (I, 0=uint8)
      56-63:   flags (Q)
      64-127:  ipc_handle (64B, zeroed — CudaIpc compat)
      128-135: max_consumers (Q, =32)
      136-647: consumer_registry[32] (16B × 32: key_hash + cursor)
      648-655: session_id (8B ASCII)
      656-663: session_start_ns (Q)
      664-667: frame_format (I)
      668-671: frame_size (I)
      672-675: aligned_slot_size (I)
      676-679: magic (I, 0x4D415452 = "MATR")
      680-683: version (I, =2)
      684-767: reserved (84B, zeroed)

    Per-slot metadata (48 bytes):
      0-7:   frame_idx (Q)
      8-15:  timestamp_ns (Q)
      16-23: flags (Q)
      24-27: rtp_timestamp (I)
      28-31: seq_start (I) — torn frame: incremented BEFORE write
      32-35: seq_end (I) — torn frame: incremented AFTER write
      36-47: padding (12B)
    """

    # Constants
    MAX_CONSUMERS: ClassVar[int] = 32
    CONSUMER_SLOT_SIZE: ClassVar[int] = 16  # 8B key_hash + 8B cursor
    HEADER_SIZE: ClassVar[int] = 768
    SLOT_META_SIZE: ClassVar[int] = 48
    PAGE_SIZE: ClassVar[int] = 4096
    MAGIC: ClassVar[int] = 0x4D415452  # "MATR"
    VERSION: ClassVar[int] = 2

    # Frame format constants
    FORMAT_NV12: ClassVar[int] = 0
    FORMAT_RGB: ClassVar[int] = 1
    FORMAT_BGR: ClassVar[int] = 2
    FORMAT_RAW: ClassVar[int] = 3  # raw bytes, size = width * height * channels

    FORMAT_NAMES: ClassVar[Dict[int, str]] = {
        FORMAT_NV12: "NV12",
        FORMAT_RGB: "RGB",
        FORMAT_BGR: "BGR",
        FORMAT_RAW: "RAW",
    }

    # Offsets within header
    _OFF_WRITE_IDX: ClassVar[int] = 0
    _OFF_READ_IDX: ClassVar[int] = 8
    _OFF_FRAME_COUNT: ClassVar[int] = 16
    _OFF_TIMESTAMP: ClassVar[int] = 24
    _OFF_GPU_ID: ClassVar[int] = 32
    _OFF_NUM_SLOTS: ClassVar[int] = 36
    _OFF_WIDTH: ClassVar[int] = 40
    _OFF_HEIGHT: ClassVar[int] = 44
    _OFF_CHANNELS: ClassVar[int] = 48
    _OFF_DTYPE: ClassVar[int] = 52
    _OFF_FLAGS: ClassVar[int] = 56
    _OFF_IPC_HANDLE: ClassVar[int] = 64
    _OFF_MAX_CONSUMERS: ClassVar[int] = 128
    _OFF_CONSUMER_REG: ClassVar[int] = 136
    _OFF_SESSION_ID: ClassVar[int] = 648
    _OFF_SESSION_START: ClassVar[int] = 656
    _OFF_FRAME_FORMAT: ClassVar[int] = 664
    _OFF_FRAME_SIZE: ClassVar[int] = 668
    _OFF_ALIGNED_SLOT: ClassVar[int] = 672
    _OFF_MAGIC: ClassVar[int] = 676
    _OFF_VERSION: ClassVar[int] = 680

    def __init__(
        self,
        camera_id: str,
        *,
        gpu_id: int = 0,
        num_slots: int = 8,
        width: int = 0,
        height: int = 0,
        channels: int = 0,
        frame_format: int = FORMAT_BGR,
        slot_count: int = 0,
        max_msg_size: int = 0,
        is_producer: bool = True,
        create: Optional[bool] = None,
        shm_name: Optional[str] = None,
    ) -> None:
        """Initialize SHM ring buffer.

        Args:
            camera_id: Unique identifier (used in SHM name if shm_name not given)
            gpu_id: GPU device ID (for status reporting)
            num_slots: Number of ring buffer slots (default 8)
            width: Frame width in pixels (or auto-computed from max_msg_size)
            height: Frame height in pixels (1 for message mode)
            channels: Channels per pixel (0 = auto from frame_format)
            frame_format: FORMAT_NV12/RGB/BGR/RAW
            slot_count: Alias for num_slots (overrides if nonzero, backward compat)
            max_msg_size: If >0, auto-compute dims for raw byte messages (DataBus)
            is_producer: True = create SHM, False = attach as consumer
            create: Alias for is_producer (backward compat)
            shm_name: Explicit SHM name (bypasses name generation)
        """
        # Normalize aliases, message-mode dims, and channel defaults.
        is_producer, num_slots, width, height, channels, frame_format = self._resolve_params(
            is_producer, create, slot_count, num_slots, max_msg_size, width, height, channels, frame_format
        )

        # Set geometry/identity attributes and derive SHM sizes/paths.
        self._init_geometry(camera_id, gpu_id, num_slots, width, height, channels, frame_format, is_producer, shm_name)

        # Initialize internal handles, caches, and consumer registry state.
        self._init_state(num_slots)

        # Backward-compat shim: if callers opt into the legacy `create=` kwarg,
        # eagerly perform initialize()/connect() so the buffer is ready to use
        # after construction (mirrors the pre-refactor behaviour used by tests).
        if create is not None:
            if is_producer:
                self.initialize()
            else:
                self.connect()

    @classmethod
    def _resolve_params(
        cls,
        is_producer: bool,
        create: Optional[bool],
        slot_count: int,
        num_slots: int,
        max_msg_size: int,
        width: int,
        height: int,
        channels: int,
        frame_format: int,
    ) -> Tuple[bool, int, int, int, int, int]:
        """Normalize constructor aliases, message-mode dims, and channel defaults."""
        # Resolve backward-compat aliases
        if create is not None:
            is_producer = create
        if slot_count > 0:
            num_slots = slot_count

        # DataBus message mode: auto-compute dimensions
        if max_msg_size > 0:
            frame_format = cls.FORMAT_RAW
            width = max_msg_size
            height = 1
            channels = 1

        # Auto-detect channels from format if not specified
        if channels == 0:
            if frame_format == cls.FORMAT_NV12:
                channels = 1
            elif frame_format in (cls.FORMAT_RGB, cls.FORMAT_BGR):
                channels = 3
            else:
                channels = 1

        return is_producer, num_slots, width, height, channels, frame_format

    def _init_geometry(
        self,
        camera_id: str,
        gpu_id: int,
        num_slots: int,
        width: int,
        height: int,
        channels: int,
        frame_format: int,
        is_producer: bool,
        shm_name: Optional[str],
    ) -> None:
        """Set identity/geometry attributes and derive SHM sizes and paths."""
        self.camera_id = camera_id
        self.gpu_id = gpu_id
        self.num_slots = num_slots
        self.width = width
        self.height = height
        self.channels = channels
        self.frame_format = frame_format
        self.is_producer = is_producer

        # Backward compat aliases
        self.slot_count = num_slots
        self._is_producer = is_producer

        # Calculate frame size
        self.frame_size = self._calculate_frame_size(width, height, channels, frame_format)
        self.frame_bytes = self.frame_size  # alias for Orin compat

        # Page-aligned slot size
        self._aligned_slot_size = ((self.frame_size + self.PAGE_SIZE - 1) // self.PAGE_SIZE) * self.PAGE_SIZE

        # For Orin/CudaIpc compat
        self.frame_shape = (height, width, channels)
        self.frame_elements = height * width * channels
        self.total_gpu_bytes = self.frame_bytes * num_slots

        # SHM paths
        if shm_name:
            self.shm_name = shm_name
        else:
            self.shm_name = self._generate_shm_name(camera_id)
        self.meta_shm_name = self.shm_name
        self.meta_shm_path = f"{SHM_BASE_PATH}/{self.shm_name}"
        self.frames_shm_path = f"{SHM_BASE_PATH}/{self.shm_name}_frames"

        # SHM sizes
        self.meta_size = self.HEADER_SIZE + (self.SLOT_META_SIZE * num_slots)
        self.frames_size = num_slots * self._aligned_slot_size

    def _init_state(self, num_slots: int) -> None:
        """Initialize SHM handles, write/read caches, and consumer-registry state."""
        # Internal state
        self._meta_fd: Optional[int] = None
        self._meta_mmap: Optional[mmap.mmap] = None
        self._frames_fd: Optional[int] = None
        self._frames_mmap: Optional[mmap.mmap] = None
        self._initialized = False
        self._cached_write_idx: int = 0
        self._last_read_idx: int = 0
        self._cached_slot_seq: list = [0] * num_slots

        # Multi-consumer
        self._consumer_id: Optional[int] = None
        self._consumer_key: Optional[str] = None

        # Consumer numpy view of frame data
        self._frames_np: Optional[np.ndarray] = None

        # Legacy compat: _shm attribute (some callers check this)
        self._shm: Any = None

    # =========================================================================
    # Static helpers
    # =========================================================================

    @staticmethod
    def _generate_shm_name(camera_id: str) -> str:
        """Derive a filesystem-safe SHM name from a camera id."""
        safe_id = camera_id.replace("/", "_").replace("\\", "_").replace(":", "_")
        safe_id = "".join(c for c in safe_id if c.isalnum() or c == "_")
        return f"shm_rb_{safe_id[:180]}"

    @staticmethod
    def _calculate_frame_size(width: int, height: int, channels: int, frame_format: int) -> int:
        """Return the byte size of one frame for the given dimensions/format."""
        if frame_format == ShmRingBuffer.FORMAT_NV12:
            return int(width * height * 1.5)
        return width * height * channels

    # =========================================================================
    # Consumer Key Registry (FNV-1a hashing, 32 slots)
    # =========================================================================

    @classmethod
    def _compute_key_hash(cls, consumer_key: str) -> int:
        """Compute a nonzero 64-bit FNV-1a hash of a consumer key."""
        FNV_OFFSET = 0xCBF29CE484222325
        FNV_PRIME = 0x100000001B3
        h = FNV_OFFSET
        for c in str(consumer_key).encode("utf-8"):
            h ^= c
            h = (h * FNV_PRIME) & 0xFFFFFFFFFFFFFFFF
        return h if h != 0 else 1

    def _get_consumer_slot_offset(self, consumer_id: int) -> int:
        """Return the header byte offset of a consumer's registry slot."""
        return self._OFF_CONSUMER_REG + (consumer_id * self.CONSUMER_SLOT_SIZE)

    def _read_consumer_slot(self, consumer_id: int) -> Tuple[int, int]:
        """Read a consumer registry slot, returning (key_hash, cursor)."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS - 1}")
        offset = self._get_consumer_slot_offset(consumer_id)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        data = self._meta_mmap.read(16)
        return struct.unpack("<QQ", data)

    def _write_consumer_slot(self, consumer_id: int, key_hash: int, cursor: int):
        """Write key_hash and cursor into a consumer registry slot."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS - 1}")
        offset = self._get_consumer_slot_offset(consumer_id)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<QQ", key_hash, cursor))
        self._meta_mmap.flush()

    def _register_consumer_key(self, consumer_key: str) -> int:
        """Register a consumer key, returning its (existing or newly-assigned) slot id."""
        key_hash = self._compute_key_hash(consumer_key)
        first_empty = -1
        for cid in range(self.MAX_CONSUMERS):
            stored_hash, _ = self._read_consumer_slot(cid)
            if stored_hash == key_hash:
                return cid
            if stored_hash == 0 and first_empty == -1:
                first_empty = cid
        if first_empty == -1:
            raise RuntimeError(f"All {self.MAX_CONSUMERS} consumer slots are full")
        self._write_consumer_slot(first_empty, key_hash, 0)
        logger.info(f"Registered consumer key '{consumer_key}' -> slot {first_empty}")
        return first_empty

    def _read_consumer_cursor(self, consumer_id: int) -> int:
        """Read the last-acked frame_idx cursor for a consumer slot."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS - 1}")
        offset = self._get_consumer_slot_offset(consumer_id) + 8
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    def _write_consumer_cursor(self, consumer_id: int, frame_idx: int):
        """Write the last-acked frame_idx cursor for a consumer slot."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS - 1}")
        offset = self._get_consumer_slot_offset(consumer_id) + 8
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<Q", frame_idx))
        self._meta_mmap.flush()

    # =========================================================================
    # Factory Methods
    # =========================================================================

    @classmethod
    def create_producer(
        cls, camera_id: str, gpu_id: int = 0, num_slots: int = 8, width: int = 640, height: int = 640, channels: int = 1
    ) -> "ShmRingBuffer":
        """Create and initialize a producer ring buffer."""
        rb = cls(
            camera_id,
            gpu_id=gpu_id,
            num_slots=num_slots,
            width=width,
            height=height,
            channels=channels,
            is_producer=True,
        )
        rb.initialize()
        return rb

    @classmethod
    def connect_consumer(
        cls,
        camera_id: str,
        gpu_id: int = 0,
        consumer_key: str = "default",
        max_retries: int = 10,
        retry_delay: float = 0.5,
        shm_name: Optional[str] = None,
    ) -> "ShmRingBuffer":
        """Attach to a producer's ring buffer as a consumer, retrying until it exists."""
        consumer_key = str(consumer_key)

        # Determine meta path
        if shm_name:
            meta_path = f"{SHM_BASE_PATH}/{shm_name}"
        else:
            meta_path = f"{SHM_BASE_PATH}/{cls._generate_shm_name(camera_id)}"

        last_error: Optional[Exception] = None
        for attempt in range(max_retries):
            try:
                fd = os.open(meta_path, os.O_RDONLY)
                mm = mmap.mmap(fd, cls.HEADER_SIZE, MAP_SHARED, PROT_READ)

                # Read dimensions from header
                mm.seek(cls._OFF_GPU_ID)
                struct.unpack("<I", mm.read(4))[0]
                num_slots = struct.unpack("<I", mm.read(4))[0]
                width = struct.unpack("<I", mm.read(4))[0]
                height = struct.unpack("<I", mm.read(4))[0]
                channels = struct.unpack("<I", mm.read(4))[0]

                # Read extended fields if magic present
                mm.seek(cls._OFF_FRAME_FORMAT)
                frame_format = struct.unpack("<I", mm.read(4))[0]
                mm.seek(cls._OFF_MAGIC)
                magic = struct.unpack("<I", mm.read(4))[0]
                if magic != cls.MAGIC:
                    frame_format = cls.FORMAT_BGR  # legacy header

                mm.close()
                os.close(fd)

                rb = cls(
                    camera_id,
                    gpu_id=gpu_id,
                    num_slots=num_slots,
                    width=width,
                    height=height,
                    channels=channels,
                    frame_format=frame_format,
                    is_producer=False,
                    shm_name=shm_name,
                )
                rb._consumer_key = consumer_key
                if rb.connect():
                    rb._consumer_id = rb._register_consumer_key(consumer_key)
                    return rb
                else:
                    raise RuntimeError(f"Failed to connect to ring buffer {camera_id}")

            except FileNotFoundError as e:
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
            except RuntimeError:
                raise
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue

        raise FileNotFoundError(
            f"Ring buffer for {camera_id} not found after {max_retries} attempts. Last error: {last_error}"
        )

    # =========================================================================
    # Producer Initialization
    # =========================================================================

    def initialize(self) -> bool:
        """Initialize as producer — create SHM segments and write header."""
        if not self.is_producer:
            raise RuntimeError("Use connect() for consumer")

        try:
            # Create metadata SHM
            try:
                os.unlink(self.meta_shm_path)
            except FileNotFoundError:
                logger.debug(f"[SHM] No stale meta to unlink: {self.meta_shm_path}")
            # SECURITY: owner-only (0o600). Cross-container consumers attach as
            # the same uid (SG/IE share uid 65532), so world/group access is not
            # required and would let any local user read/tamper frame metadata.
            self._meta_fd = os.open(self.meta_shm_path, os.O_CREAT | os.O_RDWR, 0o600)
            os.ftruncate(self._meta_fd, self.meta_size)
            self._meta_mmap = mmap.mmap(self._meta_fd, self.meta_size, MAP_SHARED, PROT_READ | PROT_WRITE)

            # Create frame data SHM
            try:
                os.unlink(self.frames_shm_path)
            except FileNotFoundError:
                logger.debug(f"[SHM] No stale frames to unlink: {self.frames_shm_path}")
            # SECURITY: owner-only (0o600); same-uid attach model (see meta SHM).
            self._frames_fd = os.open(self.frames_shm_path, os.O_CREAT | os.O_RDWR, 0o600)
            os.ftruncate(self._frames_fd, self.frames_size)
            self._frames_mmap = mmap.mmap(self._frames_fd, self.frames_size, MAP_SHARED, PROT_READ | PROT_WRITE)

            # Write header
            self._write_header()

            # Initialize all slot metadata
            for slot in range(self.num_slots):
                self._write_slot_meta(slot, frame_idx=0, timestamp_ns=0, flags=0)

            self._meta_mmap.flush()
            self._frames_mmap.flush()
            self._initialized = True

            logger.info(
                f"[SHM] Producer initialized: {self.camera_id}, "
                f"{self.frames_size / 1024 / 1024:.1f} MB "
                f"({self.num_slots} slots × {self.frame_size} bytes, "
                f"aligned to {self._aligned_slot_size})"
            )
            return True

        except Exception as e:
            logger.exception(f"[SHM] Failed to initialize producer: {e}")
            return False

    def _write_header(self):
        """Write unified header to metadata SHM."""
        assert self._meta_mmap is not None

        # Build header in parts
        # Base fields (64 bytes)
        header = struct.pack(
            "<QQQQIIIIIIQ",
            0,  # write_idx
            0,  # read_idx (legacy)
            0,  # frame_count
            time.time_ns(),  # timestamp_ns
            self.gpu_id,
            self.num_slots,
            self.width,
            self.height,
            self.channels,
            0,  # dtype_code (uint8)
            0,  # flags
        )
        # CUDA IPC handle area (64 bytes, zeroed)
        header += b"\x00" * CUDA_IPC_HANDLE_SIZE

        # Multi-consumer registry
        header += struct.pack("<Q", self.MAX_CONSUMERS)
        for _ in range(self.MAX_CONSUMERS):
            header += struct.pack("<QQ", 0, 0)

        # Session info (16 bytes)
        header += b"\x00" * 16

        # Extended fields
        header += struct.pack(
            "<IIIII",
            self.frame_format,
            self.frame_size,
            self._aligned_slot_size,
            self.MAGIC,
            self.VERSION,
        )

        # Pad to HEADER_SIZE
        header = header.ljust(self.HEADER_SIZE, b"\x00")

        self._meta_mmap.seek(0)
        self._meta_mmap.write(header)

    # =========================================================================
    # Consumer Connection
    # =========================================================================

    def connect(self, stale_threshold_sec: float = 30.0) -> bool:
        """Connect as consumer — open existing SHM segments."""
        if self.is_producer:
            raise RuntimeError("Use initialize() for producer")

        try:
            if not os.path.exists(self.meta_shm_path):
                return False

            # Open metadata SHM (read-write for consumer cursor updates)
            self._meta_fd = os.open(self.meta_shm_path, os.O_RDWR)
            self._meta_mmap = mmap.mmap(self._meta_fd, self.meta_size, MAP_SHARED, PROT_READ | PROT_WRITE)

            # Check for stale buffer
            self._meta_mmap.seek(self._OFF_TIMESTAMP)
            last_write_ns = struct.unpack("<Q", self._meta_mmap.read(8))[0]
            if last_write_ns > 0:
                age_sec = (time.time_ns() - last_write_ns) / 1e9
                if age_sec > stale_threshold_sec:
                    logger.warning(f"Ring buffer {self.camera_id} appears stale (last write {age_sec:.1f}s ago).")

            # Open frame data SHM
            if not os.path.exists(self.frames_shm_path):
                return False
            self._frames_fd = os.open(self.frames_shm_path, os.O_RDONLY)
            self._frames_mmap = mmap.mmap(self._frames_fd, self.frames_size, MAP_SHARED, PROT_READ)

            # Create numpy view of frame data (only when numpy is available)
            if NUMPY_AVAILABLE and self.height > 0 and self.width > 0 and self.channels > 0:
                try:
                    self._frames_np = np.ndarray(
                        shape=(self.num_slots, self.height, self.width, self.channels),
                        dtype=np.uint8,
                        buffer=self._frames_mmap,
                    )
                except ValueError:
                    # Shape doesn't match mmap size (page-aligned), skip numpy view
                    self._frames_np = None
            else:
                self._frames_np = None

            self._initialized = True
            logger.info(f"[SHM] Consumer connected: {self.camera_id}")
            return True

        except Exception as e:
            logger.exception(f"[SHM] Failed to connect consumer: {e}")
            return False

    # =========================================================================
    # Metadata Operations
    # =========================================================================

    def _update_write_idx(self, write_idx: int, timestamp_ns: Optional[int] = None):
        """Update header write_idx, frame_count, and timestamp."""
        if timestamp_ns is None:
            timestamp_ns = time.time_ns()
        data = struct.pack("<QQQQ", write_idx, 0, write_idx, timestamp_ns)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        self._meta_mmap.write(data)
        self._meta_mmap.flush()

    def _read_write_idx(self) -> int:
        """Read the producer's current write index from the header."""
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    def _get_slot_meta_offset(self, slot: int) -> int:
        """Return the byte offset of a slot's metadata block."""
        return self.HEADER_SIZE + (slot * self.SLOT_META_SIZE)

    def _write_slot_meta(
        self,
        slot: int,
        frame_idx: int,
        timestamp_ns: int,
        flags: int,
        rtp_timestamp: int = 0,
        seq_start: int = 0,
        seq_end: int = 0,
    ):
        """Write per-slot metadata (48 bytes)."""
        offset = self._get_slot_meta_offset(slot)
        data = struct.pack(
            "<QQQIII12x",
            frame_idx,
            timestamp_ns,
            flags,
            rtp_timestamp & 0xFFFFFFFF,
            seq_start & 0xFFFFFFFF,
            seq_end & 0xFFFFFFFF,
        )
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(data)

    def _read_slot_meta(self, slot: int) -> Tuple[int, int, int, int]:
        """Read per-slot metadata. Returns (frame_idx, timestamp_ns, flags, rtp_timestamp)."""
        offset = self._get_slot_meta_offset(slot)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        data = self._meta_mmap.read(self.SLOT_META_SIZE)
        frame_idx, timestamp_ns, flags, rtp_timestamp, _, _ = struct.unpack("<QQQIII12x", data)
        return frame_idx, timestamp_ns, flags, rtp_timestamp

    def _read_slot_seq(self, slot: int) -> Tuple[int, int]:
        """Read seq_start and seq_end from slot metadata."""
        offset = self._get_slot_meta_offset(slot) + 28  # after frame_idx(8)+ts(8)+flags(8)+rtp(4)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        data = self._meta_mmap.read(8)
        return struct.unpack("<II", data)

    def _write_slot_seq_start(self, slot: int, seq: int):
        """Write a slot's seq_start (incremented before a write begins)."""
        offset = self._get_slot_meta_offset(slot) + 28
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<I", seq & 0xFFFFFFFF))

    def _write_slot_seq_end(self, slot: int, seq: int):
        """Write a slot's seq_end (incremented after a write commits)."""
        offset = self._get_slot_meta_offset(slot) + 32
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<I", seq & 0xFFFFFFFF))

    def _write_slot_frame_idx(self, slot: int, frame_idx: int):
        """Write only the frame_idx field of a slot's metadata."""
        offset = self._get_slot_meta_offset(slot)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<Q", frame_idx))

    def _read_slot_frame_idx(self, slot: int) -> int:
        """Read only the frame_idx field of a slot's metadata."""
        offset = self._get_slot_meta_offset(slot)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    # =========================================================================
    # Session Info (RTSP Mode B T0+PTS Sync)
    # =========================================================================

    def set_session_info(self, session_id: str, session_start_ns: int):
        """Store the RTSP session id and start timestamp in the header (producer only)."""
        if not self.is_producer:
            raise RuntimeError("set_session_info() only for producer")
        assert self._meta_mmap is not None
        session_bytes = session_id.encode("ascii")[:8].ljust(8, b"\x00")
        data = struct.pack("<8sQ", session_bytes, session_start_ns)
        self._meta_mmap.seek(self._OFF_SESSION_ID)
        self._meta_mmap.write(data)
        self._meta_mmap.flush()

    def get_session_info(self) -> Tuple[str, int]:
        """Return the stored (session_id, session_start_ns) from the header."""
        assert self._meta_mmap is not None
        self._meta_mmap.seek(self._OFF_SESSION_ID)
        data = self._meta_mmap.read(16)
        session_bytes, session_start_ns = struct.unpack("<8sQ", data)
        session_id = session_bytes.rstrip(b"\x00").decode("ascii", errors="replace")
        return session_id, session_start_ns

    # =========================================================================
    # Producer Operations
    # =========================================================================

    def write_frame(self, raw_data: Union[bytes, memoryview, np.ndarray, Any]) -> Tuple[int, int]:
        """Write frame/message to next slot with torn frame protection.

        Args:
            raw_data: Frame bytes, numpy array, or CuPy array

        Returns:
            (frame_idx, slot_idx)
        """
        if not self.is_producer:
            raise RuntimeError("write_frame() only for producer")
        if not self._initialized:
            raise RuntimeError("Producer not initialized")

        # Convert to bytes
        if CUPY_AVAILABLE and cp is not None and isinstance(raw_data, cp.ndarray):
            raw_bytes = raw_data.tobytes()
        elif NUMPY_AVAILABLE and np is not None and isinstance(raw_data, np.ndarray):
            if raw_data.flags["C_CONTIGUOUS"]:
                raw_mv = memoryview(raw_data.data).cast("B")
            else:
                raw_mv = memoryview(raw_data.tobytes())
            raw_bytes = raw_mv
        elif isinstance(raw_data, memoryview):
            raw_bytes = raw_data.cast("B") if raw_data.itemsize != 1 else raw_data
        else:
            raw_bytes = raw_data

        self._cached_write_idx += 1
        frame_idx = self._cached_write_idx
        slot = (frame_idx - 1) % self.num_slots

        # Torn frame protection: seq_start → ODD (writing)
        self._cached_slot_seq[slot] += 1
        seq_writing = self._cached_slot_seq[slot]
        self._write_slot_seq_start(slot, seq_writing)

        # Write frame data
        assert self._frames_mmap is not None
        offset = slot * self._aligned_slot_size
        self._frames_mmap.seek(offset)
        self._frames_mmap.write(bytes(raw_bytes))

        ts = time.time_ns()

        # Write slot metadata
        self._write_slot_meta(slot, frame_idx, ts, 0, 0, seq_writing, seq_writing)

        # Torn frame protection: seq_end = seq_start → EVEN (committed)
        self._cached_slot_seq[slot] += 1
        seq_committed = self._cached_slot_seq[slot]
        self._write_slot_seq_end(slot, seq_committed)
        self._write_slot_seq_start(slot, seq_committed)

        # Memory barrier
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        self._meta_mmap.read(1)

        # Update header
        self._update_write_idx(frame_idx, ts)

        return frame_idx, slot

    def write_frame_fast(
        self, gpu_frame, sync: bool = True, timestamp_ns: Optional[int] = None, rtp_timestamp: int = 0
    ) -> int:
        """Write a GPU/numpy frame with torn frame protection.

        CudaIpcRingBuffer-compatible API. Returns frame_idx only.

        Args:
            gpu_frame: CuPy ndarray, numpy ndarray, or bytes
            sync: Ignored (SHM writes are always coherent)
            timestamp_ns: Frame capture timestamp (default: now)
            rtp_timestamp: RTP timestamp from RTSP stream
        """
        if not self.is_producer:
            raise RuntimeError("write_frame_fast() only for producer")
        if not self._initialized:
            raise RuntimeError("Producer not initialized")

        # Convert to bytes
        if CUPY_AVAILABLE and cp is not None and isinstance(gpu_frame, cp.ndarray):
            frame_bytes = gpu_frame.tobytes()
        elif NUMPY_AVAILABLE and np is not None and isinstance(gpu_frame, np.ndarray):
            frame_bytes = gpu_frame.tobytes()
        else:
            frame_bytes = bytes(gpu_frame)

        self._cached_write_idx += 1
        frame_idx = self._cached_write_idx
        slot = (frame_idx - 1) % self.num_slots

        # Torn frame protection: ODD
        self._cached_slot_seq[slot] += 1
        seq_writing = self._cached_slot_seq[slot]
        self._write_slot_seq_start(slot, seq_writing)

        # Write frame data
        assert self._frames_mmap is not None
        offset = slot * self._aligned_slot_size
        self._frames_mmap.seek(offset)
        self._frames_mmap.write(frame_bytes)

        if timestamp_ns is None:
            timestamp_ns = time.time_ns()

        # Write slot metadata
        self._write_slot_meta(slot, frame_idx, timestamp_ns, 0, rtp_timestamp, seq_writing, seq_writing)

        # Torn frame protection: EVEN
        self._cached_slot_seq[slot] += 1
        seq_committed = self._cached_slot_seq[slot]
        self._write_slot_seq_end(slot, seq_committed)
        self._write_slot_seq_start(slot, seq_committed)

        # Memory barrier
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        self._meta_mmap.read(1)

        self._update_write_idx(frame_idx, timestamp_ns)

        return frame_idx

    def sync_writes(self):
        """Flush SHM writes."""
        if self._frames_mmap is not None:
            self._frames_mmap.flush()
        if self._meta_mmap is not None:
            self._meta_mmap.flush()

    # =========================================================================
    # Consumer Operations
    # =========================================================================

    def read_frame(self, frame_idx_or_slot: int):
        """Read a frame. If numpy view available, returns ndarray from slot.
        Otherwise returns memoryview of frame data by frame_idx."""
        if not self._initialized:
            raise RuntimeError("Consumer not connected")

        # GPU-style read (by slot index, returns ndarray)
        if self._frames_np is not None and 0 <= frame_idx_or_slot < self.num_slots:
            frame_np = self._frames_np[frame_idx_or_slot]
            if CUPY_AVAILABLE and cp is not None:
                return cp.asarray(frame_np)
            return frame_np

        # Message-style read (by frame_idx, returns memoryview)
        frame_idx = frame_idx_or_slot
        if not self.is_frame_valid(frame_idx):
            return None
        slot = (frame_idx - 1) % self.num_slots
        offset = slot * self._aligned_slot_size
        assert self._frames_mmap is not None
        self._frames_mmap.seek(offset)
        return self._frames_mmap.read(self.frame_size)

    def read_frame_copy(self, frame_idx: int, max_wait_ms: float = 5.0) -> Optional[bytes]:
        """Read frame with torn frame detection and retry.

        Returns a copy of frame data, or None if overwritten/torn/timeout.
        """
        if not self.is_frame_valid(frame_idx):
            return None

        slot = (frame_idx - 1) % self.num_slots
        start_time = time.time()
        max_wait_sec = max_wait_ms / 1000.0

        while True:
            seq_start, _ = self._read_slot_seq(slot)

            # Write in progress (ODD seq_start)
            if seq_start & 1:
                if time.time() - start_time >= max_wait_sec:
                    return None
                time.sleep(0.0002)
                continue

            # Read frame data
            assert self._frames_mmap is not None
            offset = slot * self._aligned_slot_size
            self._frames_mmap.seek(offset)
            frame_data = self._frames_mmap.read(self.frame_size)

            # Check torn (seq mismatch)
            seq_start2, seq_end2 = self._read_slot_seq(slot)
            if seq_start2 != seq_start or seq_end2 != seq_start:
                if time.time() - start_time >= max_wait_sec:
                    return None
                time.sleep(0.0002)
                continue

            # Verify frame_idx unchanged
            stored = self._read_slot_frame_idx(slot)
            if stored != frame_idx:
                return None

            return frame_data

    def read_latest(self) -> Tuple:
        """Read most recently written frame. Returns (frame, write_idx)."""
        write_idx = self._read_write_idx()
        if write_idx == 0:
            return None, -1
        slot = (write_idx - 1) % self.num_slots
        self._last_read_idx = write_idx
        frame = self.read_frame(slot)
        return frame, write_idx

    def read_next(self) -> Tuple:
        """Read next frame after last read. Returns (frame, frame_idx, was_skipped)."""
        write_idx = self._read_write_idx()
        if write_idx == 0:
            return None, -1, False

        next_idx = self._last_read_idx + 1
        if write_idx - next_idx >= self.num_slots:
            skip_to = write_idx - self.num_slots + 1
            self._last_read_idx = skip_to - 1
            next_idx = skip_to
            was_skipped = True
        else:
            was_skipped = False

        if next_idx > write_idx:
            return None, -1, False

        slot = (next_idx - 1) % self.num_slots
        self._last_read_idx = next_idx
        frame = self.read_frame(slot)
        return frame, next_idx, was_skipped

    # =========================================================================
    # Validation
    # =========================================================================

    def is_frame_valid(self, frame_idx: int, max_wait_ms: float = 5.0) -> bool:
        """Check if frame_idx is still readable (not overwritten).
        Retries for cross-process memory visibility."""
        if frame_idx <= 0:
            return False

        start_time = time.time()
        max_wait_sec = max_wait_ms / 1000.0

        while True:
            write_idx = self._read_write_idx()
            if write_idx - frame_idx >= self.num_slots:
                return False
            if frame_idx > write_idx:
                if time.time() - start_time >= max_wait_sec:
                    return False
                time.sleep(0.0001)
                continue

            slot = (frame_idx - 1) % self.num_slots
            stored = self._read_slot_frame_idx(slot)
            if stored == frame_idx:
                return True

            if frame_idx == write_idx:
                if time.time() - start_time >= max_wait_sec:
                    return False
                time.sleep(0.0001)
                continue
            return False

    def is_frame_torn(self, frame_idx: int) -> bool:
        """Check if frame is currently being written (torn risk)."""
        slot = (frame_idx - 1) % self.num_slots
        seq_start, seq_end = self._read_slot_seq(slot)
        return seq_start != seq_end or (seq_start & 1) == 1

    # =========================================================================
    # Consumer Tracking
    # =========================================================================

    def ack_frame_done(self, frame_idx: int):
        """Advance this consumer's cursor to mark a frame as processed (consumer only)."""
        if self.is_producer:
            raise RuntimeError("ack_frame_done() only for consumer")
        if self._consumer_id is None:
            raise RuntimeError("consumer_id not set — use connect_consumer()")
        current = self._read_consumer_cursor(self._consumer_id)
        if frame_idx > current:
            self._write_consumer_cursor(self._consumer_id, frame_idx)

    def get_consumer_cursor(self, consumer_id: Optional[int] = None) -> int:
        """Return a consumer's cursor (defaults to this instance's consumer)."""
        if consumer_id is None:
            consumer_id = self._consumer_id
        if consumer_id is None:
            raise RuntimeError("consumer_id not set")
        return self._read_consumer_cursor(consumer_id)

    def get_all_consumer_cursors(self) -> Dict[int, int]:
        """Return {consumer_id: cursor} for all registered consumers."""
        cursors = {}
        for cid in range(self.MAX_CONSUMERS):
            key_hash, cursor = self._read_consumer_slot(cid)
            if key_hash != 0:
                cursors[cid] = cursor
        return cursors

    def get_registered_consumers(self) -> Dict[int, Dict]:
        """Return {consumer_id: {key_hash, cursor}} for all registered consumers."""
        consumers = {}
        for cid in range(self.MAX_CONSUMERS):
            key_hash, cursor = self._read_consumer_slot(cid)
            if key_hash != 0:
                consumers[cid] = {"key_hash": key_hash, "cursor": cursor}
        return consumers

    def get_frames_behind(self) -> int:
        """Return how many frames this consumer lags behind the producer."""
        return max(0, self._read_write_idx() - self._last_read_idx)

    # =========================================================================
    # Health Monitoring
    # =========================================================================

    def get_write_idx(self) -> int:
        """Return the producer's current write index."""
        return self._read_write_idx()

    def get_current_frame_idx(self) -> int:
        """Return the most recently written frame index."""
        return self._read_write_idx()

    def get_last_heartbeat_ns(self) -> int:
        """Return the producer's last write/heartbeat timestamp in nanoseconds."""
        assert self._meta_mmap is not None
        self._meta_mmap.seek(self._OFF_TIMESTAMP)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    def is_producer_alive(self, timeout_ns: int = 2_000_000_000) -> bool:
        """Return True if the producer wrote within the given timeout window."""
        return (time.time_ns() - self.get_last_heartbeat_ns()) < timeout_ns

    def get_producer_age_ms(self) -> float:
        """Return milliseconds since the producer's last heartbeat."""
        return (time.time_ns() - self.get_last_heartbeat_ns()) / 1_000_000

    def get_header(self) -> dict:
        """Return a decoded dict of the buffer's header fields."""
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        data = self._meta_mmap.read(self.HEADER_SIZE)
        write_idx, _, _, ts = struct.unpack_from("<QQQQ", data, 0)
        gpu_id, num_slots, w, h, ch, _, _ = struct.unpack_from("<IIIIIIQ", data, 32)
        return {
            "write_idx": write_idx,
            "timestamp_ns": ts,
            "gpu_id": gpu_id,
            "num_slots": num_slots,
            "width": w,
            "height": h,
            "channels": ch,
            "format": self.frame_format,
            "slot_count": num_slots,
            "last_ts_ns": ts,
        }

    def get_health_status(self) -> Dict:
        """Return a health snapshot (producer liveness, utilization, geometry)."""
        try:
            write_idx = self._read_write_idx()
            producer_alive = self.is_producer_alive()
            producer_age_ms = self.get_producer_age_ms()
            utilization = min(1.0, write_idx / self.num_slots) if self.num_slots > 0 else 0.0
            return {
                "is_healthy": True,
                "producer_alive": producer_alive,
                "producer_age_ms": producer_age_ms,
                "frames_written": write_idx,
                "buffer_utilization": utilization,
                "shm_name": self.shm_name,
                "width": self.width,
                "height": self.height,
                "frame_format": self.FORMAT_NAMES.get(self.frame_format, "unknown"),
                "slot_count": self.num_slots,
                "frame_size": self.frame_size,
                "is_producer": self.is_producer,
                "error_message": None,
            }
        except Exception as e:
            return {
                "is_healthy": False,
                "producer_alive": False,
                "producer_age_ms": float("inf"),
                "frames_written": 0,
                "buffer_utilization": 0.0,
                "shm_name": self.shm_name,
                "error_message": str(e),
            }

    def get_status(self) -> Dict:
        """CudaIpcRingBuffer-compatible status."""
        if not self._initialized:
            return {"initialized": False}
        status = {
            "initialized": True,
            "camera_id": self.camera_id,
            "gpu_id": self.gpu_id,
            "write_idx": self._read_write_idx(),
            "num_slots": self.num_slots,
            "frame_shape": self.frame_shape,
            "gpu_buffer_mb": self.total_gpu_bytes / 1024 / 1024,
            "transport": "posix_shm",
        }
        if not self.is_producer and self._consumer_id is not None:
            status["consumer_key"] = self._consumer_key
            status["consumer_id"] = self._consumer_id
            status["last_read_idx"] = self._last_read_idx
            status["frames_behind"] = self.get_frames_behind()
        return status

    def wait_for_producer(self, timeout_sec: float = 30.0, poll_interval_ms: float = 100.0) -> bool:
        """Block until the producer is alive and has written a frame, or timeout."""
        start = time.time()
        interval = poll_interval_ms / 1000.0
        while time.time() - start < timeout_sec:
            if self.get_current_frame_idx() > 0 and self.is_producer_alive():
                return True
            time.sleep(interval)
        return False

    # =========================================================================
    # Stale Buffer Cleanup
    # =========================================================================

    @staticmethod
    def cleanup_stale_buffers(prefix: str = "shm_rb_") -> List[str]:
        """Unlink SHM buffers idle longer than 10s; return the names cleaned."""
        cleaned: List[str] = []
        shm_path = SHM_BASE_PATH
        if not os.path.exists(shm_path):
            return cleaned
        try:
            for entry in os.listdir(shm_path):
                if not entry.startswith(prefix) or entry.endswith("_frames"):
                    continue
                meta_path = f"{shm_path}/{entry}"
                try:
                    fd = os.open(meta_path, os.O_RDONLY)
                    mm = mmap.mmap(fd, 32, MAP_SHARED, PROT_READ)
                    mm.seek(24)
                    last_ts = struct.unpack("<Q", mm.read(8))[0]
                    mm.close()
                    os.close(fd)
                    if (time.time_ns() - last_ts) > 10_000_000_000:
                        os.unlink(meta_path)
                        frames_path = f"{meta_path}_frames"
                        try:
                            os.unlink(frames_path)
                        except FileNotFoundError:
                            logger.debug(f"[SHM] Frames file already gone: {frames_path}")
                        cleaned.append(entry)
                except Exception as e:
                    logger.debug(f"[SHM] Skipping stale-buffer candidate {entry}: {e}")
        except Exception as e:
            logger.debug(f"[SHM] cleanup_stale_buffers listdir failed: {e}")
        return cleaned

    @staticmethod
    def list_buffers(prefix: str = "shm_rb_") -> List[Dict]:
        """Enumerate existing SHM buffers with size, frame count, and age info."""
        buffers: List[Dict] = []
        shm_path = SHM_BASE_PATH
        if not os.path.exists(shm_path):
            return buffers
        try:
            for entry in os.listdir(shm_path):
                if not entry.startswith(prefix) or entry.endswith("_frames"):
                    continue
                meta_path = f"{shm_path}/{entry}"
                try:
                    fd = os.open(meta_path, os.O_RDONLY)
                    size = os.fstat(fd).st_size
                    mm = mmap.mmap(fd, min(size, 48), MAP_SHARED, PROT_READ)
                    mm.seek(0)
                    data = mm.read(48)
                    write_idx = struct.unpack_from("<Q", data, 0)[0]
                    ts = struct.unpack_from("<Q", data, 24)[0]
                    num_slots = struct.unpack_from("<I", data, 36)[0]
                    mm.close()
                    os.close(fd)
                    age_ms = (time.time_ns() - ts) / 1_000_000
                    buffers.append(
                        {
                            "name": entry,
                            "size": size,
                            "frames_written": write_idx,
                            "num_slots": num_slots,
                            "producer_alive": age_ms < 2000,
                            "age_ms": age_ms,
                        }
                    )
                except Exception as e:
                    logger.debug(f"[SHM] Skipping unreadable buffer {entry}: {e}")
        except Exception as e:
            logger.debug(f"[SHM] list_buffers listdir failed: {e}")
        return buffers

    # =========================================================================
    # Benchmark
    # =========================================================================

    def benchmark_write_throughput(self, num_frames: int = 1000, frame_data: Optional[bytes] = None) -> Dict:
        """Measure write FPS, latency percentiles, and throughput (producer only)."""
        if not self.is_producer:
            raise RuntimeError("benchmark only for producer")
        if frame_data is None:
            frame_data = bytes(self.frame_size)
        latencies = []
        start = time.perf_counter()
        for _ in range(num_frames):
            t0 = time.perf_counter()
            self.write_frame(frame_data)
            latencies.append((time.perf_counter() - t0) * 1e6)
        elapsed = time.perf_counter() - start
        latencies.sort()
        total_bytes = num_frames * self.frame_size
        return {
            "num_frames": num_frames,
            "elapsed_sec": elapsed,
            "fps": num_frames / elapsed,
            "latency_us_avg": sum(latencies) / len(latencies),
            "latency_us_p50": latencies[len(latencies) // 2],
            "latency_us_p99": latencies[int(len(latencies) * 0.99)],
            "throughput_mbps": (total_bytes / elapsed) / (1024 * 1024),
            "throughput_gbps": (total_bytes * 8 / elapsed) / 1e9,
        }

    # =========================================================================
    # Lifecycle
    # =========================================================================

    def close(self):
        """Close mmaps/fds and (for producers) unlink the SHM files; never raises."""
        try:
            if self._meta_mmap:
                self._meta_mmap.close()
                self._meta_mmap = None
            if self._frames_mmap:
                self._frames_mmap.close()
                self._frames_mmap = None
            if self._meta_fd is not None:
                os.close(self._meta_fd)
                self._meta_fd = None
            if self._frames_fd is not None:
                os.close(self._frames_fd)
                self._frames_fd = None
            if self.is_producer:
                for path in (self.meta_shm_path, self.frames_shm_path):
                    try:
                        os.unlink(path)
                    except FileNotFoundError:
                        logger.debug(f"[SHM] Unlink skipped, already gone: {path}")
            self._frames_np = None
            self._initialized = False
            self._shm = None
        except Exception as e:
            logger.warning(f"[SHM] Close error for {self.camera_id}: {e}")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        """Best-effort cleanup on garbage collection."""
        try:
            self.close()
        except Exception as e:
            logger.debug(f"[SHM] __del__ close failed: {e}")

    def __repr__(self) -> str:
        return (
            f"ShmRingBuffer(name={self.shm_name}, "
            f"{self.width}x{self.height} {self.FORMAT_NAMES.get(self.frame_format, 'RAW')}, "
            f"slots={self.num_slots}, producer={self.is_producer})"
        )


# =============================================================================
# NV12 Conversion Helpers (kept at module level for backward compat)
# =============================================================================


def _require_numpy() -> None:
    """Raise ImportError if numpy isn't installed (for runtime-only helpers)."""
    if not NUMPY_AVAILABLE:
        raise ImportError("numpy is required for this operation but is not installed. Install with: pip install numpy")


def bgr_to_nv12(bgr_frame: "np.ndarray") -> bytes:
    """Convert BGR frame to NV12 format."""
    _require_numpy()
    import cv2

    height, _ = bgr_frame.shape[:2]
    yuv_i420 = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2YUV_I420)
    y_end = height
    u_end = height + height // 4
    y_plane = yuv_i420[:y_end, :].flatten()
    u_plane = yuv_i420[y_end:u_end, :].flatten()
    v_plane = yuv_i420[u_end:, :].flatten()
    uv_interleaved = np.empty(len(u_plane) * 2, dtype=np.uint8)
    uv_interleaved[0::2] = u_plane
    uv_interleaved[1::2] = v_plane
    return np.concatenate([y_plane, uv_interleaved]).tobytes()


def nv12_to_bgr(nv12_bytes: bytes, width: int, height: int) -> "np.ndarray":
    """Convert NV12 bytes to BGR frame."""
    _require_numpy()
    import cv2

    expected = int(width * height * 1.5)
    if len(nv12_bytes) != expected:
        raise ValueError(f"NV12 size mismatch: expected {expected}, got {len(nv12_bytes)}")
    nv12_array = np.frombuffer(nv12_bytes, dtype=np.uint8).reshape((height + height // 2, width))
    return cv2.cvtColor(nv12_array, cv2.COLOR_YUV2BGR_NV12)


def rgb_to_nv12(rgb_frame: "np.ndarray") -> bytes:
    """Convert RGB frame to NV12 format."""
    _require_numpy()
    import cv2

    return bgr_to_nv12(cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
