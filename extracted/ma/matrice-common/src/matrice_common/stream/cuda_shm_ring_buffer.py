#!/usr/bin/env python3
"""CUDA IPC Ring Buffer - True Zero-Copy GPU Memory Sharing (Multi-Consumer).

This module implements a ring buffer using CUDA IPC for cross-process
GPU memory sharing with ZERO CPU copies after initial decode.

Multi-Consumer Design:
=====================
    - Producer NEVER blocks - always overwrites ring buffer freely
    - Up to 32 independent consumers can attach to same ring buffer
    - Each consumer has its own cursor position in shared memory
    - Slow consumers skip frames instead of blocking or corrupting data

Architecture:
============

    Producer (Streaming Gateway)              Consumer 1 (Triton)      Consumer 2 (Recorder)
    ┌─────────────────────────────┐          ┌─────────────────────┐  ┌─────────────────────┐
    │ 1. NVDEC decode (GPU)       │          │ read_next()         │  │ read_next()         │
    │ 2. NV12 resize (GPU)        │  ──────> │ (60 FPS)            │  │ (15 FPS - skips)    │
    │ 3. write_frame() - no wait  │   SHM    │ ack_frame_done()    │  │ ack_frame_done()    │
    │ 4. Export IPC handle to SHM │ (392 B)  └─────────────────────┘  └─────────────────────┘
    └─────────────────────────────┘

Requirements:
=============
    - CuPy with CUDA support
    - CUDA driver >= 450 (for IPC support)
    - Docker: --ipc=host OR same IPC namespace
    - Same GPU visibility across containers

Usage:
======
    # Producer (streaming gateway)
    ring = CudaIpcRingBuffer.create_producer("cam_001", gpu_id=0, height=960, width=640)
    ring.write_frame(nv12_frame)  # (H*1.5, W, 1) uint8 - NEVER BLOCKS

    # Consumer 1 (inference server) - fast consumer
    ring = CudaIpcRingBuffer.connect_consumer("cam_001", gpu_id=0, consumer_key="inference")
    frame, idx, skipped = ring.read_next()  # Zero-copy GPU access with skip detection
    ring.ack_frame_done(idx)

    # Consumer 2 (recorder) - slow consumer, same ring buffer, different key
    ring2 = CudaIpcRingBuffer.connect_consumer("cam_001", gpu_id=0, consumer_key="recorder")
    frame, idx, skipped = ring2.read_next()  # Will skip if too slow
"""

import os
import mmap
import struct
import time
import logging
from typing import Optional, Tuple, Dict

import numpy as np

logger = logging.getLogger(__name__)

# Environment variable for SHM base path (for Docker/custom environments)
SHM_BASE_PATH = os.getenv('MATRICE_SHM_PATH', '/dev/shm')

# Cross-platform mmap flags (fallbacks for Windows)
MAP_SHARED = getattr(mmap, 'MAP_SHARED', 1)
PROT_READ = getattr(mmap, 'PROT_READ', 1)
PROT_WRITE = getattr(mmap, 'PROT_WRITE', 2)

try:
    import cupy as cp
    from cupy.cuda import runtime as cuda_runtime
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    cp = None
    cuda_runtime = None

CUDA_IPC_HANDLE_SIZE = 64

class CudaIpcRingBuffer:
    """CUDA IPC Ring Buffer for zero-copy cross-process GPU memory sharing.

    This class manages a ring buffer stored entirely in GPU memory, with
    metadata stored in POSIX shared memory for cross-process coordination.
    """

    # Header layout (multi-consumer support with key registry):
    # 0-7:   write_idx (8 bytes)
    # 8-15:  read_idx (8 bytes) - legacy, unused
    # 16-23: frame_count (8 bytes)
    # 24-31: timestamp_ns (8 bytes)
    # 32-35: gpu_id (4 bytes)
    # 36-39: num_slots (4 bytes)
    # 40-43: width (4 bytes)
    # 44-47: height (4 bytes)
    # 48-51: channels (4 bytes)
    # 52-55: dtype_code (4 bytes)
    # 56-63: flags (8 bytes)
    # 64-127: ipc_handle (64 bytes)
    # 128-135: max_consumers (8 bytes) - number of consumer cursor slots
    # 136-647: consumer_registry[32] (16 bytes × 32) - per-consumer key+cursor
    #          Per slot (16 bytes):
    #            0-7:  key_hash (8 bytes, 0 = empty/unregistered)
    #            8-15: cursor_position (8 bytes)
    # 648-655: session_id (8 bytes) - 8-char session ID for RTSP sync (Mode B)
    # 656-663: session_start_ns (8 bytes) - T0 wall clock when RTSP connected
    # Slot metadata layout (32 bytes per slot):
    #   0-7:   frame_idx (8 bytes)
    #   8-15:  timestamp_ns (8 bytes)
    #   16-23: flags (8 bytes)
    #   24-27: rtp_timestamp (4 bytes) - raw 32-bit RTP timestamp from RTSP stream
    #   28-31: padding (4 bytes) - alignment
    MAX_CONSUMERS = 32
    CONSUMER_SLOT_SIZE = 16  # 8 bytes key_hash + 8 bytes cursor
    HEADER_SIZE = 136 + (MAX_CONSUMERS * CONSUMER_SLOT_SIZE)  # 648 bytes
    SESSION_INFO_OFFSET = HEADER_SIZE  # 648 - session info starts here
    SESSION_INFO_SIZE = 16  # 8 bytes session_id + 8 bytes session_start_ns
    SLOT_META_SIZE = 32  # Extended from 24 to include RTP timestamp

    def __init__(self, camera_id: str, gpu_id: int, num_slots: int,
                 width: int, height: int, channels: int, is_producer: bool):
        if not CUPY_AVAILABLE:
            raise RuntimeError("CuPy is required for CUDA IPC ring buffer")

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
        self.total_gpu_bytes = self.frame_bytes * num_slots

        self.meta_shm_name = f"cuda_ipc_{camera_id}"
        self.meta_shm_path = f"{SHM_BASE_PATH}/{self.meta_shm_name}"
        # Include session info size in meta_size for Mode B sync support
        self.meta_size = self.HEADER_SIZE + self.SESSION_INFO_SIZE + (self.SLOT_META_SIZE * num_slots)

        self.gpu_buffer: Optional[cp.ndarray] = None
        self._meta_fd: Optional[int] = None
        self._meta_mmap: Optional[mmap.mmap] = None
        self._initialized = False
        self._cached_write_idx = 0
        self._write_event: Optional[cp.cuda.Event] = None

        # Multi-consumer support: per-consumer state tracking
        self._consumer_id: Optional[int] = None  # Assigned on connect
        self._consumer_key: Optional[str] = None  # Original key used for ID assignment
        self._last_read_idx: int = 0  # Track local read progress

    @classmethod
    def _compute_key_hash(cls, consumer_key: str) -> int:
        """Compute a deterministic 64-bit hash for a consumer key.

        Uses a simple but deterministic hash that is consistent across:
        - Different Python processes
        - Different machines
        - Different Python versions

        Args:
            consumer_key: Any string identifier

        Returns:
            64-bit hash value (never 0, as 0 means empty slot)
        """
        # FNV-1a hash (64-bit) - deterministic across all environments
        FNV_OFFSET = 0xcbf29ce484222325
        FNV_PRIME = 0x100000001b3

        h = FNV_OFFSET
        for c in str(consumer_key).encode('utf-8'):
            h ^= c
            h = (h * FNV_PRIME) & 0xFFFFFFFFFFFFFFFF

        # Ensure hash is never 0 (0 means empty slot)
        return h if h != 0 else 1

    def _get_consumer_slot_offset(self, consumer_id: int) -> int:
        """Get SHM offset for a consumer slot (key_hash + cursor)."""
        return 136 + (consumer_id * self.CONSUMER_SLOT_SIZE)

    def _read_consumer_slot(self, consumer_id: int) -> tuple:
        """Read consumer slot (key_hash, cursor) from SHM.

        Returns:
            (key_hash, cursor_position) tuple
        """
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS-1}")
        offset = self._get_consumer_slot_offset(consumer_id)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        data = self._meta_mmap.read(16)
        key_hash, cursor = struct.unpack("<QQ", data)
        return key_hash, cursor

    def _write_consumer_slot(self, consumer_id: int, key_hash: int, cursor: int):
        """Write consumer slot (key_hash, cursor) to SHM."""
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS-1}")
        offset = self._get_consumer_slot_offset(consumer_id)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<QQ", key_hash, cursor))
        self._meta_mmap.flush()

    def _register_consumer_key(self, consumer_key: str) -> int:
        """Register a consumer key and get assigned consumer_id.

        If the key already exists, returns the existing ID.
        If the key is new, assigns the next available ID.

        Args:
            consumer_key: Consumer group identifier string

        Returns:
            Assigned consumer_id (0-31)

        Raises:
            RuntimeError: If all consumer slots are full
        """
        key_hash = self._compute_key_hash(consumer_key)

        # First pass: look for existing registration or first empty slot
        first_empty = -1
        for cid in range(self.MAX_CONSUMERS):
            stored_hash, _ = self._read_consumer_slot(cid)
            if stored_hash == key_hash:
                # Found existing registration
                return cid
            if stored_hash == 0 and first_empty == -1:
                first_empty = cid

        # Not found - register in first empty slot
        if first_empty == -1:
            raise RuntimeError(f"All {self.MAX_CONSUMERS} consumer slots are full")

        # Register the new key
        self._write_consumer_slot(first_empty, key_hash, 0)
        logger.info(f"Registered consumer key '{consumer_key}' -> slot {first_empty}")
        return first_empty

    @classmethod
    def create_producer(cls, camera_id: str, gpu_id: int = 0,
                        num_slots: int = 8, width: int = 640, height: int = 640,
                        channels: int = 1) -> "CudaIpcRingBuffer":
        """Create a producer ring buffer.

        For NV12: height should be H*1.5 (e.g., 960 for 640x640 frames), channels=1
        """
        rb = cls(camera_id, gpu_id, num_slots, width, height, channels, is_producer=True)
        rb.initialize()
        return rb

    @classmethod
    def connect_consumer(cls, camera_id: str, gpu_id: int = 0,
                         consumer_key: str = "default",
                         max_retries: int = 10, retry_delay: float = 0.5) -> "CudaIpcRingBuffer":
        """Connect as consumer with retry logic for cross-container startup race.

        Args:
            camera_id: Camera identifier
            gpu_id: GPU device ID to use
            consumer_key: Consumer group identifier (any string). Consumers with the same
                key share position tracking. Different keys get independent cursors.
                Examples: "inference", "recorder", "gpu0_worker", "triton_server"
            max_retries: Maximum connection attempts (for container startup race)
            retry_delay: Delay between retries in seconds

        Returns:
            Connected CudaIpcRingBuffer instance

        Raises:
            FileNotFoundError: If ring buffer not found after all retries
            RuntimeError: If connection fails after retries
        """
        consumer_key = str(consumer_key)
        with cp.cuda.Device(gpu_id):
            _ = cp.zeros(1, dtype=cp.uint8)

        meta_shm_path = f"{SHM_BASE_PATH}/cuda_ipc_{camera_id}"

        last_error: Optional[Exception] = None
        for attempt in range(max_retries):
            try:
                fd = os.open(meta_shm_path, os.O_RDONLY, 0o666)
                mm = mmap.mmap(fd, 128, MAP_SHARED, PROT_READ)  # type: ignore[arg-type]

                mm.seek(32)
                gpu_id_stored = struct.unpack("<I", mm.read(4))[0]
                num_slots = struct.unpack("<I", mm.read(4))[0]
                width = struct.unpack("<I", mm.read(4))[0]
                height = struct.unpack("<I", mm.read(4))[0]
                channels = struct.unpack("<I", mm.read(4))[0]

                mm.close()
                os.close(fd)

                # Validate GPU affinity
                if gpu_id_stored != gpu_id:
                    raise RuntimeError(
                        f"GPU mismatch for {camera_id}: producer used GPU {gpu_id_stored}, "
                        f"consumer trying GPU {gpu_id}. Use matching GPU IDs."
                    )

                rb = cls(camera_id, gpu_id, num_slots, width, height, channels, is_producer=False)
                rb._consumer_key = consumer_key
                if rb.connect():
                    # Register consumer key and get assigned ID (auto-assigns next free slot)
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
                # GPU mismatch - don't retry, raise immediately
                raise

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                    time.sleep(retry_delay)
                    continue

        raise FileNotFoundError(f"Ring buffer for {camera_id} not found after {max_retries} attempts. Start producer first.")

    def initialize(self) -> bool:
        """Initialize as producer - allocate GPU memory and create SHM."""
        if not self.is_producer:
            raise RuntimeError("Use connect() for consumer")

        try:
            with cp.cuda.Device(self.gpu_id):
                total_shape = (self.num_slots,) + self.frame_shape
                self.gpu_buffer = cp.zeros(total_shape, dtype=cp.uint8)
                base_ptr = self.gpu_buffer.data.ptr
                ipc_handle = cuda_runtime.ipcGetMemHandle(base_ptr)
                self._write_event = cp.cuda.Event()

            self._create_meta_shm()
            self._write_header(ipc_handle)

            for slot in range(self.num_slots):
                self._write_slot_meta(slot, frame_idx=0, timestamp_ns=0, flags=0)

            self._initialized = True
            logger.info(f"Producer initialized: {self.camera_id}, "
                       f"{self.total_gpu_bytes / 1024 / 1024:.1f} MB GPU buffer")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize producer: {e}")
            return False

    def connect(self, stale_threshold_sec: float = 30.0) -> bool:
        """Connect as consumer - import CUDA IPC handle.

        Args:
            stale_threshold_sec: Warn if last write was more than this many seconds ago
        """
        if self.is_producer:
            raise RuntimeError("Use initialize() for producer")

        try:
            self._open_meta_shm()

            # Check for stale buffer (producer may have crashed)
            assert self._meta_mmap is not None
            self._meta_mmap.seek(24)  # timestamp_ns offset
            last_write_ns = struct.unpack("<Q", self._meta_mmap.read(8))[0]
            if last_write_ns > 0:  # Only check if producer has written at least once
                age_sec = (time.time_ns() - last_write_ns) / 1e9
                if age_sec > stale_threshold_sec:
                    logger.warning(
                        f"Ring buffer {self.camera_id} appears stale "
                        f"(last write {age_sec:.1f}s ago). Producer may have crashed."
                    )

            self._meta_mmap.seek(64)
            ipc_handle = self._meta_mmap.read(CUDA_IPC_HANDLE_SIZE)

            with cp.cuda.Device(self.gpu_id):
                _ = cp.zeros(1, dtype=cp.uint8)
                imported_ptr = cuda_runtime.ipcOpenMemHandle(ipc_handle)

                total_shape = (self.num_slots,) + self.frame_shape
                total_elements = int(np.prod(total_shape))

                mem = cp.cuda.UnownedMemory(imported_ptr, total_elements, owner=None)
                memptr = cp.cuda.MemoryPointer(mem, 0)
                self.gpu_buffer = cp.ndarray(total_shape, dtype=cp.uint8, memptr=memptr)

            self._initialized = True
            logger.info(f"Consumer connected: {self.camera_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect consumer: {e}")
            return False

    def _create_meta_shm(self):
        """Create POSIX SHM for metadata."""
        try:
            os.unlink(self.meta_shm_path)
        except FileNotFoundError:
            pass

        self._meta_fd = os.open(self.meta_shm_path, os.O_CREAT | os.O_RDWR, 0o666)
        os.ftruncate(self._meta_fd, self.meta_size)
        self._meta_mmap = mmap.mmap(
            self._meta_fd, self.meta_size,
            MAP_SHARED, PROT_READ | PROT_WRITE
        )

    def _open_meta_shm(self):
        """Open existing POSIX SHM for metadata."""
        self._meta_fd = os.open(self.meta_shm_path, os.O_RDWR, 0o666)
        self._meta_mmap = mmap.mmap(
            self._meta_fd, self.meta_size,
            MAP_SHARED, PROT_READ | PROT_WRITE
        )

    def _write_header(self, ipc_handle: bytes):
        """Write header to SHM with multi-consumer key registry."""
        header = struct.pack(
            "<QQQQIIIIIIQ",
            0,  # write_idx
            0,  # read_idx
            0,  # frame_count
            time.time_ns(),
            self.gpu_id,
            self.num_slots,
            self.width,
            self.height,
            self.channels,
            0,  # dtype_code (always uint8)
            0,  # flags
        )
        header += bytes(ipc_handle)[:CUDA_IPC_HANDLE_SIZE].ljust(CUDA_IPC_HANDLE_SIZE, b'\x00')

        # Multi-consumer support: max_consumers field + consumer registry slots
        header += struct.pack("<Q", self.MAX_CONSUMERS)  # max_consumers at offset 128

        # Initialize all consumer slots (16 bytes each: 8 key_hash + 8 cursor)
        # key_hash=0 means slot is empty/unregistered
        for _ in range(self.MAX_CONSUMERS):
            header += struct.pack("<QQ", 0, 0)  # (key_hash=0, cursor=0)

        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        self._meta_mmap.write(header)

    def _read_consumer_cursor(self, consumer_id: int) -> int:
        """Read specific consumer's progress cursor from SHM.

        Uses the new slot layout: each slot is 16 bytes (8 key_hash + 8 cursor).
        """
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS-1}")
        # Cursor is at offset +8 within each 16-byte slot
        offset = self._get_consumer_slot_offset(consumer_id) + 8
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    def _write_consumer_cursor(self, consumer_id: int, frame_idx: int):
        """Write specific consumer's progress cursor to SHM.

        Preserves the key_hash, only updates the cursor position.
        """
        if consumer_id < 0 or consumer_id >= self.MAX_CONSUMERS:
            raise ValueError(f"consumer_id must be 0-{self.MAX_CONSUMERS-1}")
        # Cursor is at offset +8 within each 16-byte slot
        offset = self._get_consumer_slot_offset(consumer_id) + 8
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(struct.pack("<Q", frame_idx))
        self._meta_mmap.flush()

    def _update_write_idx(self, write_idx: int, timestamp_ns: int):
        """Update write index atomically."""
        header_data = struct.pack("<QQQQ", write_idx, 0, write_idx, timestamp_ns)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        self._meta_mmap.write(header_data)
        self._meta_mmap.flush()

    def _read_write_idx(self) -> int:
        """Read current write index."""
        assert self._meta_mmap is not None
        self._meta_mmap.seek(0)
        return struct.unpack("<Q", self._meta_mmap.read(8))[0]

    def _write_slot_meta(self, slot: int, frame_idx: int, timestamp_ns: int, flags: int, rtp_timestamp: int = 0):
        """Write slot metadata including RTP timestamp.

        Args:
            slot: Slot index
            frame_idx: Frame index
            timestamp_ns: Capture timestamp in nanoseconds
            flags: Slot flags
            rtp_timestamp: Raw 32-bit RTP timestamp from RTSP stream (0 for non-RTSP)
        """
        # Slot metadata starts after header + session info
        offset = self.HEADER_SIZE + self.SESSION_INFO_SIZE + (slot * self.SLOT_META_SIZE)
        # Pack: frame_idx(8) + timestamp_ns(8) + flags(8) + rtp_timestamp(4) + padding(4)
        data = struct.pack("<QQQI4x", frame_idx, timestamp_ns, flags, rtp_timestamp & 0xFFFFFFFF)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        self._meta_mmap.write(data)

    def _read_slot_meta(self, slot: int) -> Tuple[int, int, int, int]:
        """Read slot metadata including RTP timestamp.

        Returns:
            (frame_idx, timestamp_ns, flags, rtp_timestamp) tuple
            rtp_timestamp: Raw 32-bit RTP timestamp (0 for non-RTSP sources)
        """
        # Slot metadata starts after header + session info
        offset = self.HEADER_SIZE + self.SESSION_INFO_SIZE + (slot * self.SLOT_META_SIZE)
        assert self._meta_mmap is not None
        self._meta_mmap.seek(offset)
        data = self._meta_mmap.read(self.SLOT_META_SIZE)
        # Unpack: frame_idx(8) + timestamp_ns(8) + flags(8) + rtp_timestamp(4) + padding(4)
        frame_idx, timestamp_ns, flags, rtp_timestamp = struct.unpack("<QQQI4x", data)
        return frame_idx, timestamp_ns, flags, rtp_timestamp

    # =========================================================================
    # Session Info Operations (Mode B T0+PTS Sync Support)
    # =========================================================================

    def set_session_info(self, session_id: str, session_start_ns: int):
        """Set RTSP session info for Mode B frame-accurate sync.

        Producer should call this when RTSP connects/reconnects.

        Args:
            session_id: 8-char unique session ID (changes on reconnect)
            session_start_ns: T0 wall clock (ns) when RTSP connected
        """
        if not self.is_producer:
            raise RuntimeError("set_session_info() only for producer")
        assert self._meta_mmap is not None

        # Encode session_id as 8 bytes (truncate or pad as needed)
        session_bytes = session_id.encode('ascii')[:8].ljust(8, b'\x00')
        data = struct.pack("<8sQ", session_bytes, session_start_ns)

        self._meta_mmap.seek(self.SESSION_INFO_OFFSET)
        self._meta_mmap.write(data)
        self._meta_mmap.flush()

    def get_session_info(self) -> Tuple[str, int]:
        """Get RTSP session info for Mode B frame-accurate sync.

        Consumer can call this to get current session info.

        Returns:
            (session_id, session_start_ns) tuple
            session_id: 8-char unique session ID (empty string if not set)
            session_start_ns: T0 wall clock (ns) when RTSP connected (0 if not set)
        """
        assert self._meta_mmap is not None

        self._meta_mmap.seek(self.SESSION_INFO_OFFSET)
        data = self._meta_mmap.read(self.SESSION_INFO_SIZE)
        session_bytes, session_start_ns = struct.unpack("<8sQ", data)

        # Decode session_id, stripping null bytes
        session_id = session_bytes.rstrip(b'\x00').decode('ascii', errors='replace')
        return session_id, session_start_ns

    # =========================================================================
    # Producer Operations (Non-blocking, multi-consumer safe)
    # =========================================================================

    def write_frame(self, gpu_frame: cp.ndarray) -> int:
        """Write a frame to the ring buffer - NEVER BLOCKS.

        Multi-consumer design: Producer always wins and overwrites ring buffer.
        Slow consumers will detect skipped frames via read_next().

        Args:
            gpu_frame: NV12 frame to write (must match frame_shape)

        Returns:
            Frame index (always succeeds, never returns -1)
        """
        if not self.is_producer:
            raise RuntimeError("write_frame() only for producer")
        if not self._initialized:
            raise RuntimeError("Producer not initialized")

        if gpu_frame.shape != self.frame_shape:
            raise ValueError(f"Shape mismatch: expected {self.frame_shape}, got {gpu_frame.shape}")

        self._cached_write_idx += 1
        frame_idx = self._cached_write_idx
        slot = (frame_idx - 1) % self.num_slots

        with cp.cuda.Device(self.gpu_id):
            assert self.gpu_buffer is not None
            cp.copyto(self.gpu_buffer[slot], gpu_frame)
            assert self._write_event is not None
            self._write_event.record()
            self._write_event.synchronize()

        timestamp_ns = time.time_ns()
        self._write_slot_meta(slot, frame_idx, timestamp_ns, 0)
        self._update_write_idx(frame_idx, timestamp_ns)

        return frame_idx

    def write_frame_fast(
        self,
        gpu_frame: cp.ndarray,
        sync: bool = True,
        timestamp_ns: Optional[int] = None,
        rtp_timestamp: int = 0
    ) -> int:
        """Fast write without device context switch - NEVER BLOCKS.

        Use this when already in the correct CUDA device context.
        Stores UTC nanosecond timestamp for frame provenance tracking.

        Args:
            gpu_frame: CuPy array to write
            sync: Whether to synchronize after copy (default True)
            timestamp_ns: Optional UTC nanosecond timestamp from frame capture.
                          If None, captures current time. Pass decode-time timestamp
                          for more accurate frame timing in the pipeline.
            rtp_timestamp: Raw 32-bit RTP timestamp from RTSP stream.
                           Pass 0 for non-RTSP sources (video files).

        Returns:
            Frame index written
        """
        self._cached_write_idx += 1
        frame_idx = self._cached_write_idx
        slot = (frame_idx - 1) % self.num_slots

        assert self.gpu_buffer is not None
        cp.copyto(self.gpu_buffer[slot], gpu_frame)

        if sync:
            assert self._write_event is not None
            self._write_event.record()
            self._write_event.synchronize()

        # Use provided timestamp or capture current time
        if timestamp_ns is None:
            timestamp_ns = time.time_ns()
        self._write_slot_meta(slot, frame_idx, timestamp_ns, 0, rtp_timestamp)
        self._update_write_idx(frame_idx, timestamp_ns)
        return frame_idx

    def sync_writes(self):
        """Sync all pending writes."""
        if self._write_event is not None:
            self._write_event.record()
            self._write_event.synchronize()

    # =========================================================================
    # Consumer Operations (Multi-consumer safe)
    # =========================================================================

    def read_frame(self, slot: int) -> Optional[cp.ndarray]:
        """Read a frame from a specific slot (NO COPY - view)."""
        if self.is_producer:
            raise RuntimeError("read_frame() only for consumer")
        if not self._initialized:
            raise RuntimeError("Consumer not connected")

        if slot < 0 or slot >= self.num_slots:
            return None

        assert self.gpu_buffer is not None
        return self.gpu_buffer[slot]

    def read_latest(self) -> Tuple[Optional[cp.ndarray], int]:
        """Read the most recently written frame (NO COPY - view).

        Note: For sequential processing with skip detection, use read_next() instead.
        """
        if self.is_producer:
            raise RuntimeError("read_latest() only for consumer")
        if not self._initialized:
            raise RuntimeError("Consumer not connected")

        write_idx = self._read_write_idx()
        if write_idx == 0:
            return None, -1

        slot = (write_idx - 1) % self.num_slots
        self._last_read_idx = write_idx  # Update local tracking
        assert self.gpu_buffer is not None
        return self.gpu_buffer[slot], write_idx

    def read_next(self) -> Tuple[Optional[cp.ndarray], int, bool]:
        """Read next frame after last read, with skip detection.

        Multi-consumer design: Each consumer tracks its own position.
        If consumer falls behind (producer overwrote frames), skips forward.

        Returns:
            (frame, frame_idx, was_skipped)
            - frame: GPU array view, or None if no new frames
            - frame_idx: The frame index, or -1 if no new frames
            - was_skipped: True if frames were skipped (consumer too slow)
        """
        if self.is_producer:
            raise RuntimeError("read_next() only for consumer")
        if not self._initialized:
            raise RuntimeError("Consumer not connected")

        write_idx = self._read_write_idx()
        if write_idx == 0:
            return None, -1, False

        next_idx = self._last_read_idx + 1

        # Check if we're too far behind (frames were overwritten)
        if write_idx - next_idx >= self.num_slots:
            # Skip forward to oldest valid frame
            skip_to = write_idx - self.num_slots + 1
            self._last_read_idx = skip_to - 1
            next_idx = skip_to
            was_skipped = True
        else:
            was_skipped = False

        # Check if frame exists yet
        if next_idx > write_idx:
            return None, -1, False  # No new frames

        slot = (next_idx - 1) % self.num_slots
        self._last_read_idx = next_idx

        assert self.gpu_buffer is not None
        return self.gpu_buffer[slot], next_idx, was_skipped

    def get_frames_behind(self) -> int:
        """Get number of frames this consumer is behind the producer.

        Useful for monitoring consumer performance and detecting backpressure.
        """
        write_idx = self._read_write_idx()
        return max(0, write_idx - self._last_read_idx)

    def ack_frame_done(self, frame_idx: int):
        """Acknowledge that consumer has finished processing up to frame_idx.

        Multi-consumer design: Each consumer has its own cursor in SHM.
        This allows monitoring consumer progress and coordinating multiple consumers.

        Args:
            frame_idx: The highest frame index that has been fully processed
        """
        if self.is_producer:
            raise RuntimeError("ack_frame_done() only for consumer")
        if not self._initialized:
            raise RuntimeError("Consumer not connected")
        if self._consumer_id is None:
            raise RuntimeError("consumer_id not set - use connect_consumer()")

        # Only update if this is higher than current ack
        current_ack = self._read_consumer_cursor(self._consumer_id)
        if frame_idx > current_ack:
            self._write_consumer_cursor(self._consumer_id, frame_idx)

    def get_consumer_cursor(self, consumer_id: Optional[int] = None) -> int:
        """Get a consumer's cursor position (for debugging/monitoring).

        Args:
            consumer_id: Consumer ID to query. Defaults to this consumer's ID.
        """
        if consumer_id is None:
            consumer_id = self._consumer_id
        if consumer_id is None:
            raise RuntimeError("consumer_id not set - use connect_consumer()")
        return self._read_consumer_cursor(consumer_id)

    def get_all_consumer_cursors(self) -> Dict[int, int]:
        """Get all registered consumer cursors (for monitoring).

        Returns:
            Dict mapping consumer_id -> frame_idx for all registered consumers
        """
        cursors = {}
        for cid in range(self.MAX_CONSUMERS):
            key_hash, cursor = self._read_consumer_slot(cid)
            if key_hash != 0:  # Slot is registered
                cursors[cid] = cursor
        return cursors

    def get_registered_consumers(self) -> Dict[int, Dict]:
        """Get all registered consumer slots with their key hashes (for monitoring).

        Returns:
            Dict mapping consumer_id -> {"key_hash": int, "cursor": int}
        """
        consumers = {}
        for cid in range(self.MAX_CONSUMERS):
            key_hash, cursor = self._read_consumer_slot(cid)
            if key_hash != 0:  # Slot is registered
                consumers[cid] = {"key_hash": key_hash, "cursor": cursor}
        return consumers

    def get_write_idx(self) -> int:
        """Get current write index."""
        return self._read_write_idx()

    def get_status(self) -> Dict:
        """Get ring buffer status."""
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
        }

        # Add consumer-specific info if this is a consumer
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
        """Close and cleanup resources."""
        if self._meta_mmap:
            self._meta_mmap.close()
            self._meta_mmap = None

        if self._meta_fd:
            os.close(self._meta_fd)
            self._meta_fd = None

        if self.is_producer:
            try:
                os.unlink(self.meta_shm_path)
            except FileNotFoundError:
                pass

        self.gpu_buffer = None
        self._initialized = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class GlobalFrameCounter:
    """Global atomic frame counter for event-driven notification.

    Instead of polling N ring buffers, consumers watch ONE counter.
    When counter changes → new frames available somewhere.
    """

    SHM_PATH = f"{SHM_BASE_PATH}/global_frame_counter"
    SIZE = 8

    def __init__(self, is_producer: bool = True):
        self.is_producer = is_producer
        self._fd: Optional[int] = None
        self._mmap: Optional[mmap.mmap] = None
        self._local_counter = 0

    def initialize(self) -> bool:
        """Initialize counter (producer)."""
        try:
            try:
                os.unlink(self.SHM_PATH)
            except FileNotFoundError:
                pass

            self._fd = os.open(self.SHM_PATH, os.O_CREAT | os.O_RDWR, 0o666)
            os.ftruncate(self._fd, self.SIZE)
            self._mmap = mmap.mmap(self._fd, self.SIZE, MAP_SHARED, PROT_READ | PROT_WRITE)  # type: ignore[arg-type]
            self._mmap.write(struct.pack("<Q", 0))
            return True
        except Exception as e:
            logger.error(f"Failed to initialize counter: {e}")
            return False

    def connect(self) -> bool:
        """Connect to counter (consumer)."""
        try:
            self._fd = os.open(self.SHM_PATH, os.O_RDWR, 0o666)
            self._mmap = mmap.mmap(self._fd, self.SIZE, MAP_SHARED, PROT_READ | PROT_WRITE)  # type: ignore[arg-type]
            return True
        except Exception as e:
            logger.error(f"Failed to connect to counter: {e}")
            return False

    def increment(self) -> int:
        """Increment and return new value."""
        self._local_counter += 1
        assert self._mmap is not None
        self._mmap.seek(0)
        self._mmap.write(struct.pack("<Q", self._local_counter))
        return self._local_counter

    def get(self) -> int:
        """Get current value."""
        assert self._mmap is not None
        self._mmap.seek(0)
        return struct.unpack("<Q", self._mmap.read(8))[0]

    def wait_for_change(self, last_value: int, timeout_ms: float = 100.0) -> Tuple[int, bool]:
        """Wait for counter to change."""
        deadline = time.perf_counter() + (timeout_ms / 1000.0)

        while True:
            current = self.get()
            if current != last_value:
                return current, True

            if time.perf_counter() >= deadline:
                return current, False

            time.sleep(0.00005)

    def close(self):
        """Close counter."""
        if self._mmap:
            self._mmap.close()
        if self._fd:
            os.close(self._fd)
        self._mmap = None
        self._fd = None


def benchmark_cuda_ipc():
    """Benchmark CUDA IPC ring buffer performance."""
    if not CUPY_AVAILABLE:
        print("CuPy not available")
        return

    print("\n" + "=" * 70)
    print("CUDA IPC RING BUFFER BENCHMARK")
    print("=" * 70)

    cam_id = "bench_cam"
    num_frames = 10000

    # NV12 dimensions: H*1.5 for 640x640 = 960x640
    producer = CudaIpcRingBuffer.create_producer(
        cam_id, gpu_id=0, num_slots=8,
        width=640, height=960, channels=1  # NV12: (H*1.5, W, 1)
    )

    with cp.cuda.Device(0):
        test_frame = cp.random.randint(0, 256, (960, 640, 1), dtype=cp.uint8)

        for _ in range(100):
            producer.write_frame(test_frame)
        cp.cuda.Stream.null.synchronize()

        print("\n--- GPU → GPU Write (Zero-Copy Ring Buffer) ---")
        start = time.perf_counter()
        for _ in range(num_frames):
            producer.write_frame(test_frame)
        cp.cuda.Stream.null.synchronize()
        elapsed = time.perf_counter() - start

        fps = num_frames / elapsed
        latency_us = (elapsed / num_frames) * 1e6
        bandwidth_gbps = (fps * 960 * 640) / 1e9

        print(f"  FPS: {fps:,.0f}")
        print(f"  Latency: {latency_us:.2f} µs/frame")
        print(f"  Bandwidth: {bandwidth_gbps:.2f} GB/s")

    producer.close()

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)


# =============================================================================
# Orin Platform Fallback (opt-in via MATRICE_PLATFORM=orin)
# =============================================================================
# On Jetson Orin, CUDA IPC is permanently unsupported (unified memory).
# When MATRICE_PLATFORM=orin is set, replace CudaIpcRingBuffer with
# OrinShmRingBuffer (POSIX SHM) which has an identical API.
if os.environ.get("MATRICE_PLATFORM", "").lower() == "orin":
    try:
        from .orin_shm_ring_buffer import OrinShmRingBuffer
        CudaIpcRingBuffer = OrinShmRingBuffer  # type: ignore[misc]
        logger.info("MATRICE_PLATFORM=orin: CudaIpcRingBuffer -> OrinShmRingBuffer (POSIX SHM)")
    except ImportError as e:
        logger.warning(f"MATRICE_PLATFORM=orin but OrinShmRingBuffer import failed: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    benchmark_cuda_ipc()
