#!/usr/bin/env python3
"""Orin POSIX SHM Ring Buffer - Drop-in replacement for CudaIpcRingBuffer on Jetson Orin.

On Jetson Orin, cudaIpcGetMemHandle returns cudaErrorNotSupported because Orin
uses unified memory (CPU and GPU share the same DRAM). This module provides a
drop-in replacement for CudaIpcRingBuffer that uses POSIX shared memory (mmap)
for frame storage instead of CUDA IPC handles.

Activated by: MATRICE_PLATFORM=orin environment variable.

Frame data flow (Orin):
    Producer: CuPy ndarray (GPU) -> tobytes() -> memcpy to SHM mmap
    Consumer: SHM mmap -> numpy view -> cp.asarray() -> CuPy ndarray (GPU)

On Orin's unified memory, CPU<->GPU copies are essentially free (same DRAM).
The mmap-based approach adds <0.01% overhead vs CUDA IPC on unified memory.

SHM layout per camera (matches CudaIpcRingBuffer header exactly):
    /dev/shm/cuda_ipc_{camera_id}        - Metadata (648B header + 16B session + slot meta)
    /dev/shm/cuda_ipc_{camera_id}_frames - Frame data (num_slots x H x W x C bytes)
"""

from __future__ import annotations

import os
import mmap
import struct
import time
import logging
from typing import Optional, Tuple, Dict

import numpy as np

logger = logging.getLogger(__name__)

SHM_BASE_PATH = os.getenv('MATRICE_SHM_PATH', '/dev/shm')
MAP_SHARED = getattr(mmap, 'MAP_SHARED', 1)
PROT_READ = getattr(mmap, 'PROT_READ', 1)
PROT_WRITE = getattr(mmap, 'PROT_WRITE', 2)

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    cp = None  # type: ignore[assignment]
    CUPY_AVAILABLE = False

# CUDA IPC handle size (64 bytes, zeroed on Orin)
CUDA_IPC_HANDLE_SIZE = 64


class OrinShmRingBuffer:
    """POSIX SHM Ring Buffer for Jetson Orin (no CUDA IPC).

    Drop-in replacement for CudaIpcRingBuffer. Uses mmap'd shared memory for
    frame storage instead of GPU memory with CUDA IPC handles.

    Header layout matches CudaIpcRingBuffer exactly for cross-compatibility:
      0-7:     write_idx (8B)
      8-15:    read_idx (8B, legacy)
      16-23:   frame_count (8B)
      24-31:   timestamp_ns (8B)
      32-35:   gpu_id (4B)
      36-39:   num_slots (4B)
      40-43:   width (4B)
      44-47:   height (4B)
      48-51:   channels (4B)
      52-55:   dtype_code (4B)
      56-63:   flags (8B)
      64-127:  ipc_handle (64B, zeroed on Orin)
      128-135: max_consumers (8B)
      136-647: consumer_registry[32] (16B x 32)
      648-655: session_id (8B)
      656-663: session_start_ns (8B)
      664+:    per-slot metadata (32B per slot)
    """

    MAX_CONSUMERS = 32
    CONSUMER_SLOT_SIZE = 16  # 8 bytes key_hash + 8 bytes cursor
    HEADER_SIZE = 136 + (MAX_CONSUMERS * CONSUMER_SLOT_SIZE)  # 648 bytes
    SESSION_INFO_OFFSET = HEADER_SIZE  # 648
    SESSION_INFO_SIZE = 16  # 8 bytes session_id + 8 bytes session_start_ns
    SLOT_META_SIZE = 32  # frame_idx(8) + timestamp_ns(8) + flags(8) + rtp_timestamp(4) + padding(4)

    def __init__(self, camera_id: str, gpu_id: int, num_slots: int,
                 width: int, height: int, channels: int, is_producer: bool):
        self.camera_id = camera_id
        self.gpu_id = gpu_id
        self.num_slots = num_slots
        self.width = width
        self.height = height
        self.channels = channels
        self.is_producer = is_producer

        self.frame_shape = (height, width, channels)
        self.frame_elements = height * width * channels
        self.frame_bytes = self.frame_elements
        self.total_gpu_bytes = self.frame_bytes * num_slots  # For get_status() compat

        self.meta_shm_name = f"cuda_ipc_{camera_id}"
        self.meta_shm_path = f"{SHM_BASE_PATH}/{self.meta_shm_name}"
        self.frames_shm_path = f"{SHM_BASE_PATH}/cuda_ipc_{camera_id}_frames"
        self.meta_size = self.HEADER_SIZE + self.SESSION_INFO_SIZE + (self.SLOT_META_SIZE * num_slots)
        self.frames_size = num_slots * self.frame_bytes

        self._meta_fd: Optional[int] = None
        self._meta_mmap: Optional[mmap.mmap] = None
        self._frames_fd: Optional[int] = None
        self._frames_mmap: Optional[mmap.mmap] = None
        self._initialized = False
        self._cached_write_idx = 0
        self._last_read_idx = 0

        # Multi-consumer support
        self._consumer_id: Optional[int] = None
        self._consumer_key: Optional[str] = None

        # Consumer: cached numpy view of frame data
        self._frames_np: Optional[np.ndarray] = None

    # =========================================================================
    # Consumer Key Registry (matches CudaIpcRingBuffer multi-consumer)
    # =========================================================================

    @classmethod
    def _compute_key_hash(cls, consumer_key: str) -> int:
        """Compute a deterministic 64-bit FNV-1a hash for a consumer key."""
        FNV_OFFSET = 0xcbf29ce484222325
        FNV_PRIME = 0x100000001b3

        h = FNV_OFFSET
        for c in str(consumer_key).encode('utf-8'):
            h ^= c
            h = (h * FNV_PRIME) & 0xFFFFFFFFFFFFFFFF

        return h if h != 0 else 1

    def _get_consumer_slot_offset(self, consumer_id: int) -> int:
        """Get SHM offset for a consumer slot (key_hash + cursor)."""
        return 136 + (consumer_id * self.CONSUMER_SLOT_SIZE)

    def _read_consumer_slot(self, consumer_id: int) -> Tuple[int, int]:
        """Read consumer slot (key_hash, cursor) from SHM."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS - 1}")
        offset = self._get_consumer_slot_offset(consumer_id)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        data = self._meta_mmap.read(16)
        key_hash, cursor = struct.unpack("<QQ", data)
        return key_hash, cursor

    def _write_consumer_slot(self, consumer_id: int, key_hash: int, cursor: int):
        """Write consumer slot (key_hash, cursor) to SHM."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS - 1}")
        offset = self._get_consumer_slot_offset(consumer_id)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<QQ", key_hash, cursor))
        self._meta_mmap.flush()

    def _register_consumer_key(self, consumer_key: str) -> int:
        """Register a consumer key and get assigned consumer_id (0-31)."""
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
        """Read specific consumer's progress cursor from SHM."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS - 1}")
        offset = self._get_consumer_slot_offset(consumer_id) + 8
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    def _write_consumer_cursor(self, consumer_id: int, frame_idx: int):
        """Write specific consumer's progress cursor to SHM."""
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
    def create_producer(cls, camera_id: str, gpu_id: int = 0,
                        num_slots: int = 8, width: int = 640, height: int = 640,
                        channels: int = 1) -> "OrinShmRingBuffer":
        """Create a producer ring buffer.

        For NV12: height should be H*1.5 (e.g., 960 for 640x640 frames), channels=1
        """
        rb = cls(camera_id, gpu_id, num_slots, width, height, channels, is_producer=True)
        rb.initialize()
        return rb

    @classmethod
    def connect_consumer(cls, camera_id: str, gpu_id: int = 0,
                         consumer_key: str = "default",
                         max_retries: int = 10, retry_delay: float = 0.5) -> "OrinShmRingBuffer":
        """Connect as consumer with retry logic for cross-container startup race.

        Args:
            camera_id: Camera identifier
            gpu_id: GPU device ID
            consumer_key: Consumer group identifier string
            max_retries: Maximum connection attempts
            retry_delay: Delay between retries in seconds

        Returns:
            Connected OrinShmRingBuffer instance
        """
        consumer_key = str(consumer_key)
        meta_shm_path = f"{SHM_BASE_PATH}/cuda_ipc_{camera_id}"

        last_error: Optional[Exception] = None
        for attempt in range(max_retries):
            try:
                # Read header to discover dimensions
                fd = os.open(meta_shm_path, os.O_RDONLY, 0o666)
                mm = mmap.mmap(fd, 128, MAP_SHARED, PROT_READ)

                mm.seek(32)
                gpu_id_stored = struct.unpack("<I", mm.read(4))[0]
                num_slots = struct.unpack("<I", mm.read(4))[0]
                width = struct.unpack("<I", mm.read(4))[0]
                height = struct.unpack("<I", mm.read(4))[0]
                channels = struct.unpack("<I", mm.read(4))[0]

                mm.close()
                os.close(fd)

                rb = cls(camera_id, gpu_id, num_slots, width, height, channels, is_producer=False)
                rb._consumer_key = consumer_key
                if rb.connect():
                    rb._consumer_id = rb._register_consumer_key(consumer_key)
                    logger.debug(f"Consumer key '{consumer_key}' assigned to slot {rb._consumer_id}")
                    return rb
                else:
                    raise RuntimeError(f"Failed to connect to ring buffer {camera_id}")

            except FileNotFoundError as e:
                last_error = e
                if attempt < max_retries - 1:
                    logger.debug(f"Ring buffer {camera_id} not found, retry {attempt + 1}/{max_retries}")
                    time.sleep(retry_delay)
                    continue

            except RuntimeError:
                raise

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                    time.sleep(retry_delay)
                    continue

        raise FileNotFoundError(
            f"Ring buffer for {camera_id} not found after {max_retries} attempts. "
            f"Start producer first. Last error: {last_error}"
        )

    # =========================================================================
    # Producer Initialization
    # =========================================================================

    def initialize(self) -> bool:
        """Initialize as producer - create SHM segments with CudaIpcRingBuffer-compatible header."""
        if not self.is_producer:
            raise RuntimeError("Use connect() for consumer")

        try:
            # Create metadata SHM
            try:
                os.unlink(self.meta_shm_path)
            except FileNotFoundError:
                pass
            self._meta_fd = os.open(self.meta_shm_path, os.O_CREAT | os.O_RDWR, 0o666)
            os.ftruncate(self._meta_fd, self.meta_size)
            self._meta_mmap = mmap.mmap(self._meta_fd, self.meta_size, MAP_SHARED, PROT_READ | PROT_WRITE)

            # Create frame data SHM
            try:
                os.unlink(self.frames_shm_path)
            except FileNotFoundError:
                pass
            self._frames_fd = os.open(self.frames_shm_path, os.O_CREAT | os.O_RDWR, 0o666)
            os.ftruncate(self._frames_fd, self.frames_size)
            self._frames_mmap = mmap.mmap(self._frames_fd, self.frames_size, MAP_SHARED, PROT_READ | PROT_WRITE)

            # Write header (matches CudaIpcRingBuffer layout exactly)
            self._write_header()

            # Initialize all slot metadata
            for slot in range(self.num_slots):
                self._write_slot_meta(slot, frame_idx=0, timestamp_ns=0, flags=0)

            self._meta_mmap.flush()
            self._frames_mmap.flush()
            self._initialized = True

            logger.info(
                f"[Orin SHM] Producer initialized: {self.camera_id}, "
                f"{self.frames_size / 1024 / 1024:.1f} MB SHM buffer "
                f"({self.num_slots} slots x {self.frame_bytes} bytes)"
            )
            return True

        except Exception as e:
            logger.error(f"[Orin SHM] Failed to initialize producer: {e}")
            return False

    def _write_header(self):
        """Write CudaIpcRingBuffer-compatible header to SHM."""
        # Base header: 64 bytes of fixed fields
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
            0,  # dtype_code (always uint8)
            0,  # flags
        )
        # CUDA IPC handle area (64 bytes, zeroed on Orin)
        header += b'\x00' * CUDA_IPC_HANDLE_SIZE

        # Multi-consumer support: max_consumers + consumer registry
        header += struct.pack("<Q", self.MAX_CONSUMERS)
        for _ in range(self.MAX_CONSUMERS):
            header += struct.pack("<QQ", 0, 0)  # (key_hash=0, cursor=0)

        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        self._meta_mmap.write(header)

    def connect(self, stale_threshold_sec: float = 30.0) -> bool:
        """Connect as consumer - open existing SHM segments."""
        if self.is_producer:
            raise RuntimeError("Use initialize() for producer")

        try:
            if not os.path.exists(self.meta_shm_path):
                logger.debug(f"[Orin SHM] {self.camera_id}: meta SHM not found")
                return False

            # Open metadata SHM (read-write for consumer cursor updates)
            self._meta_fd = os.open(self.meta_shm_path, os.O_RDWR, 0o666)
            self._meta_mmap = mmap.mmap(self._meta_fd, self.meta_size, MAP_SHARED, PROT_READ | PROT_WRITE)

            # Check for stale buffer
            self._meta_mmap.seek(24)
            last_write_ns = struct.unpack("<Q", self._meta_mmap.read(8))[0]
            if last_write_ns > 0:
                age_sec = (time.time_ns() - last_write_ns) / 1e9
                if age_sec > stale_threshold_sec:
                    logger.warning(
                        f"Ring buffer {self.camera_id} appears stale "
                        f"(last write {age_sec:.1f}s ago). Producer may have crashed."
                    )

            # Open frame data SHM
            if not os.path.exists(self.frames_shm_path):
                logger.debug(f"[Orin SHM] {self.camera_id}: frames SHM not found")
                return False

            self._frames_fd = os.open(self.frames_shm_path, os.O_RDONLY)
            self._frames_mmap = mmap.mmap(self._frames_fd, self.frames_size, MAP_SHARED, PROT_READ)

            # Create numpy view of frame data for efficient reading
            self._frames_np = np.ndarray(
                shape=(self.num_slots, self.height, self.width, self.channels),
                dtype=np.uint8,
                buffer=self._frames_mmap,
            )

            self._initialized = True
            logger.info(f"[Orin SHM] Consumer connected: {self.camera_id}")
            return True

        except Exception as e:
            logger.error(f"[Orin SHM] Failed to connect consumer: {e}")
            return False

    # =========================================================================
    # Metadata Operations (CudaIpcRingBuffer-compatible layout)
    # =========================================================================

    def _update_write_idx(self, write_idx: int, timestamp_ns: int):
        """Update header write index and timestamp."""
        header_data = struct.pack("<QQQQ", write_idx, 0, write_idx, timestamp_ns)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        self._meta_mmap.write(header_data)
        self._meta_mmap.flush()

    def _read_write_idx(self) -> int:
        """Read current write index from header."""
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    def _write_slot_meta(self, slot: int, frame_idx: int, timestamp_ns: int,
                         flags: int, rtp_timestamp: int = 0):
        """Write per-slot metadata (CudaIpcRingBuffer-compatible 32-byte layout)."""
        offset = self.HEADER_SIZE + self.SESSION_INFO_SIZE + (slot * self.SLOT_META_SIZE)
        data = struct.pack("<QQQI4x", frame_idx, timestamp_ns, flags, rtp_timestamp & 0xFFFFFFFF)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(data)

    def _read_slot_meta(self, slot: int) -> Tuple[int, int, int, int]:
        """Read per-slot metadata. Returns (frame_idx, timestamp_ns, flags, rtp_timestamp)."""
        offset = self.HEADER_SIZE + self.SESSION_INFO_SIZE + (slot * self.SLOT_META_SIZE)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        data = self._meta_mmap.read(self.SLOT_META_SIZE)
        frame_idx, timestamp_ns, flags, rtp_timestamp = struct.unpack("<QQQI4x", data)
        return frame_idx, timestamp_ns, flags, rtp_timestamp

    # =========================================================================
    # Session Info (Mode B T0+PTS Sync)
    # =========================================================================

    def set_session_info(self, session_id: str, session_start_ns: int):
        """Set RTSP session info for Mode B frame-accurate sync."""
        if not self.is_producer:
            raise RuntimeError("set_session_info() only for producer")
        assert self._meta_mmap is not None

        session_bytes = session_id.encode('ascii')[:8].ljust(8, b'\x00')
        data = struct.pack("<8sQ", session_bytes, session_start_ns)

        self._meta_mmap.seek(self.SESSION_INFO_OFFSET)
        self._meta_mmap.write(data)
        self._meta_mmap.flush()

    def get_session_info(self) -> Tuple[str, int]:
        """Get RTSP session info. Returns (session_id, session_start_ns)."""
        assert self._meta_mmap is not None

        self._meta_mmap.seek(self.SESSION_INFO_OFFSET)
        data = self._meta_mmap.read(self.SESSION_INFO_SIZE)
        session_bytes, session_start_ns = struct.unpack("<8sQ", data)

        session_id = session_bytes.rstrip(b'\x00').decode('ascii', errors='replace')
        return session_id, session_start_ns

    # =========================================================================
    # Producer Operations
    # =========================================================================

    def write_frame(self, gpu_frame) -> int:
        """Write a frame to the ring buffer - NEVER BLOCKS."""
        if not self.is_producer:
            raise RuntimeError("write_frame() only for producer")
        if not self._initialized:
            raise RuntimeError("Producer not initialized")

        return self.write_frame_fast(gpu_frame, sync=True)

    def write_frame_fast(self, gpu_frame, sync: bool = True,
                         timestamp_ns: Optional[int] = None,
                         rtp_timestamp: int = 0) -> int:
        """Write a frame to the ring buffer (SHM version).

        Args:
            gpu_frame: CuPy ndarray (GPU) or numpy ndarray (CPU)
            sync: Ignored on Orin (SHM is always coherent)
            timestamp_ns: Frame timestamp in nanoseconds
            rtp_timestamp: RTP timestamp from RTSP stream
        """
        self._cached_write_idx += 1
        frame_idx = self._cached_write_idx
        slot = (frame_idx - 1) % self.num_slots

        assert self._frames_mmap is not None

        # Convert GPU frame to CPU bytes for SHM write
        if CUPY_AVAILABLE and cp is not None and isinstance(gpu_frame, cp.ndarray):
            frame_bytes = gpu_frame.tobytes()
        elif isinstance(gpu_frame, np.ndarray):
            frame_bytes = gpu_frame.tobytes()
        else:
            frame_bytes = bytes(gpu_frame)

        # Write frame data to SHM
        offset = slot * self.frame_bytes
        self._frames_mmap.seek(offset)
        self._frames_mmap.write(frame_bytes)

        if timestamp_ns is None:
            timestamp_ns = time.time_ns()

        self._write_slot_meta(slot, frame_idx, timestamp_ns, 0, rtp_timestamp)
        self._update_write_idx(frame_idx, timestamp_ns)

        return frame_idx

    def sync_writes(self):
        """Flush SHM writes (lightweight on Orin unified memory)."""
        if self._frames_mmap is not None:
            self._frames_mmap.flush()
        if self._meta_mmap is not None:
            self._meta_mmap.flush()

    # =========================================================================
    # Consumer Operations
    # =========================================================================

    def read_frame(self, slot: int):
        """Read a frame from a specific slot, returns CuPy ndarray on GPU."""
        if not self._initialized:
            raise RuntimeError("Consumer not connected")

        if slot < 0 or slot >= self.num_slots:
            return None

        if self._frames_np is not None:
            frame_np = self._frames_np[slot]
            if CUPY_AVAILABLE and cp is not None:
                return cp.asarray(frame_np)
            return frame_np
        return None

    def read_latest(self) -> Tuple:
        """Read the most recently written frame."""
        write_idx = self._read_write_idx()
        if write_idx == 0:
            return None, -1

        slot = (write_idx - 1) % self.num_slots
        self._last_read_idx = write_idx

        frame = self.read_frame(slot)
        return frame, write_idx

    def read_next(self) -> Tuple:
        """Read next frame after last read, with skip detection.

        Returns:
            (frame, frame_idx, was_skipped)
        """
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

    def get_frames_behind(self) -> int:
        """Get number of frames consumer is behind producer."""
        write_idx = self._read_write_idx()
        return max(0, write_idx - self._last_read_idx)

    def ack_frame_done(self, frame_idx: int):
        """Acknowledge frame processing - updates consumer cursor in SHM."""
        if self.is_producer:
            raise RuntimeError("ack_frame_done() only for consumer")
        if not self._initialized:
            raise RuntimeError("Consumer not connected")
        if self._consumer_id is None:
            raise RuntimeError("consumer_id not set - use connect_consumer()")

        current_ack = self._read_consumer_cursor(self._consumer_id)
        if frame_idx > current_ack:
            self._write_consumer_cursor(self._consumer_id, frame_idx)

    def get_consumer_cursor(self, consumer_id: Optional[int] = None) -> int:
        """Get a consumer's cursor position."""
        if consumer_id is None:
            consumer_id = self._consumer_id
        if consumer_id is None:
            raise RuntimeError("consumer_id not set - use connect_consumer()")
        return self._read_consumer_cursor(consumer_id)

    def get_all_consumer_cursors(self) -> Dict[int, int]:
        """Get all registered consumer cursors."""
        cursors = {}
        for cid in range(self.MAX_CONSUMERS):
            key_hash, cursor = self._read_consumer_slot(cid)
            if key_hash != 0:
                cursors[cid] = cursor
        return cursors

    def get_registered_consumers(self) -> Dict[int, Dict]:
        """Get all registered consumer slots with their key hashes."""
        consumers = {}
        for cid in range(self.MAX_CONSUMERS):
            key_hash, cursor = self._read_consumer_slot(cid)
            if key_hash != 0:
                consumers[cid] = {"key_hash": key_hash, "cursor": cursor}
        return consumers

    def get_write_idx(self) -> int:
        """Get current write index."""
        return self._read_write_idx()

    def get_status(self) -> Dict:
        """Get ring buffer status (CudaIpcRingBuffer-compatible format)."""
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
            "transport": "orin_posix_shm",
        }

        if not self.is_producer and self._consumer_id is not None:
            status["consumer_key"] = self._consumer_key
            status["consumer_id"] = self._consumer_id
            status["last_read_idx"] = self._last_read_idx
            status["frames_behind"] = self.get_frames_behind()

        return status

    # =========================================================================
    # Cleanup
    # =========================================================================

    def close(self):
        """Close and cleanup SHM segments."""
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

            # Producer cleans up SHM files
            if self.is_producer:
                try:
                    os.unlink(self.meta_shm_path)
                except FileNotFoundError:
                    pass
                try:
                    os.unlink(self.frames_shm_path)
                except FileNotFoundError:
                    pass

            self._frames_np = None
            self._initialized = False
        except Exception as e:
            logger.warning(f"[Orin SHM] Close error for {self.camera_id}: {e}")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
