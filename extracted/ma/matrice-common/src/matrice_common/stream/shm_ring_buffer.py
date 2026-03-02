"""Shared Memory Ring Buffer for raw frame storage.

This module implements a lock-free ring buffer using Python's multiprocessing.shared_memory
for storing raw video frames. It enables zero-copy frame sharing between producer (streaming
gateway) and multiple consumers (inference servers).

Architecture:
- Producer creates SHM and writes frames in a ring pattern
- Consumers attach to SHM and read frames by index
- Overwrite is allowed (producer never waits for consumers)
- Consumers detect overwritten frames via frame_idx validation

Layout:
┌────────────────────────┐
│ Header (64 bytes)      │  write_idx, width, height, format, slot_count, ts_ns
├────────────────────────┤
│ Per-slot metadata      │  Per slot (16 bytes each):
│                        │    - frame_idx (8 bytes): monotonic frame index
│                        │    - seq_start (4 bytes): incremented BEFORE write
│                        │    - seq_end (4 bytes): incremented AFTER write
├────────────────────────┤
│ Frame slot 0           │  Fixed size: calculated from width, height, format
├────────────────────────┤
│ Frame slot 1           │
├────────────────────────┤
│ ...                    │
└────────────────────────┘

Torn Frame Detection:
- Producer increments seq_start BEFORE writing frame data
- Producer increments seq_end AFTER writing frame data
- Consumer reads seq_start, then frame data, then seq_end
- If seq_start != seq_end, the frame was being overwritten during read (torn)

Version History:
- v1.0: Initial implementation with lock-free ring buffer
- v1.1: Added health check APIs, cleanup utilities, compiled struct formats
"""

__version__ = "1.1.0"

import logging
import os
import struct
import time
from dataclasses import dataclass
from multiprocessing import shared_memory
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np


class ShmRingBuffer:
    """Shared memory ring buffer for raw frame storage.

    Supports NV12, RGB, and BGR frame formats for efficient video streaming.
    Uses a lock-free design where the producer overwrites old frames without
    waiting for consumers.

    Example (Producer):
        buffer = ShmRingBuffer(
            camera_id="cam_001",
            width=1920,
            height=1080,
            frame_format=ShmRingBuffer.FORMAT_BGR,  # Default - no conversion needed
            slot_count=300,
            create=True
        )
        frame_idx, slot = buffer.write_frame(bgr_frame.tobytes())

    Example (Consumer):
        buffer = ShmRingBuffer(
            camera_id="cam_001",
            width=1920,
            height=1080,
            frame_format=ShmRingBuffer.FORMAT_BGR,  # Default
            slot_count=300,
            create=False  # Attach to existing
        )
        if buffer.is_frame_valid(frame_idx):
            frame_data = buffer.read_frame(frame_idx)
    """

    # Header layout (64 bytes total, C-compatible for future GPU/CUDA interop)
    # Using struct format: '<QIIIIQ' = Little-endian
    #   Q = uint64 (8 bytes) - write_idx
    #   I = uint32 (4 bytes) - width
    #   I = uint32 (4 bytes) - height
    #   I = uint32 (4 bytes) - format
    #   I = uint32 (4 bytes) - slot_count
    #   Q = uint64 (8 bytes) - last_ts_ns (heartbeat timestamp)
    #   Padding to 64 bytes for alignment
    HEADER_FORMAT = '<QIIIIQ'
    HEADER_SIZE = 64  # Fixed header size (includes padding)

    # Per-slot metadata layout (16 bytes per slot):
    #   Q = uint64 (8 bytes) - frame_idx
    #   I = uint32 (4 bytes) - seq_start (incremented BEFORE write)
    #   I = uint32 (4 bytes) - seq_end (incremented AFTER write)
    SLOT_METADATA_SIZE = 16  # bytes per slot

    # Page alignment for hardware efficiency
    # Aligning frame slots to page boundaries improves:
    # - Memory mapping performance
    # - Cache efficiency
    # - Potential future DMA/GPU transfer efficiency
    PAGE_SIZE = 4096  # 4KB pages (standard on x86/x64)

    # Frame format constants
    FORMAT_NV12 = 0   # width * height * 1.5 bytes (GPU-friendly)
    FORMAT_RGB = 1    # width * height * 3 bytes
    FORMAT_BGR = 2    # width * height * 3 bytes (OpenCV native)

    # Format names for logging
    FORMAT_NAMES = {
        FORMAT_NV12: "NV12",
        FORMAT_RGB: "RGB",
        FORMAT_BGR: "BGR",
    }

    def __init__(
        self,
        camera_id: str,
        width: int,
        height: int,
        frame_format: int = FORMAT_BGR,
        slot_count: int = 300,
        create: bool = True,
        shm_name: Optional[str] = None,
    ):
        """Initialize SHM ring buffer.

        Args:
            camera_id: Unique camera identifier (used in SHM name if shm_name not provided)
            width: Frame width in pixels
            height: Frame height in pixels
            frame_format: One of FORMAT_NV12, FORMAT_RGB, FORMAT_BGR
            slot_count: Number of frame slots in ring buffer (default: 300)
            create: True for producer (creates SHM), False for consumer (attaches)
            shm_name: Direct SHM segment name (bypasses name generation from camera_id)

        Raises:
            ValueError: If frame_format is invalid
            FileExistsError: If create=True but SHM already exists (producer conflict)
            FileNotFoundError: If create=False but SHM doesn't exist (producer not started)
        """
        self.logger = logging.getLogger(f"{__name__}.ShmRingBuffer")

        # Validate inputs
        if frame_format not in self.FORMAT_NAMES:
            raise ValueError(f"Invalid frame_format: {frame_format}. Must be one of {list(self.FORMAT_NAMES.keys())}")
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid dimensions: {width}x{height}")
        if slot_count < 2:
            raise ValueError(f"slot_count must be >= 2, got {slot_count}")

        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.frame_format = frame_format
        self.slot_count = slot_count
        self._is_producer = create

        # Calculate frame size based on format
        self.frame_size = self._calculate_frame_size(width, height, frame_format)

        # Calculate page-aligned slot size for hardware efficiency
        self._aligned_slot_size = self._calculate_aligned_slot_size(self.frame_size)

        # Per-slot metadata: frame_idx + seq_start + seq_end (16 bytes per slot)
        self._slot_metadata_size = self.SLOT_METADATA_SIZE * slot_count

        # Calculate total SHM size (using aligned slots)
        self._total_size = self._calculate_total_size()

        # Use provided shm_name if given, otherwise generate from camera_id
        self.shm_name = shm_name if shm_name else self._generate_shm_name(camera_id)

        # =================================================================
        # OPTIMIZATION: Producer-side cached counters (avoid SHM reads)
        # =================================================================
        # Cache write_idx locally - producer doesn't need to read from SHM
        self._cached_write_idx: int = 0
        # Cache per-slot sequence counters - eliminates 2 SHM reads per frame
        # Uses odd/even semantics: odd = writing, even = committed
        self._cached_slot_seq: list = [0] * slot_count

        # Initialize shared memory
        self._shm: Any = None
        self._init_shared_memory(create)

        # Calculate alignment overhead for logging
        alignment_overhead = self._aligned_slot_size - self.frame_size
        self.logger.info(
            f"ShmRingBuffer {'created' if create else 'attached'}: "
            f"name={self.shm_name}, size={self._total_size:,} bytes, "
            f"{width}x{height} {self.FORMAT_NAMES[frame_format]}, "
            f"{slot_count} slots, frame_size={self.frame_size:,} bytes, "
            f"aligned_slot_size={self._aligned_slot_size:,} bytes (+{alignment_overhead:,} padding)"
        )

    def _generate_shm_name(self, camera_id: str) -> str:
        """Generate Windows-compatible SHM name.

        Args:
            camera_id: Camera identifier

        Returns:
            Sanitized SHM name (max 200 chars, no special chars)
        """
        # Replace problematic characters and limit length
        safe_id = camera_id.replace("/", "_").replace("\\", "_").replace(":", "_")
        safe_id = "".join(c for c in safe_id if c.isalnum() or c == "_")
        return f"shm_cam_{safe_id[:180]}"

    def _calculate_frame_size(self, width: int, height: int, frame_format: int) -> int:
        """Calculate frame size in bytes based on format.

        Args:
            width: Frame width
            height: Frame height
            frame_format: Frame format constant

        Returns:
            Size in bytes for one frame
        """
        if frame_format == self.FORMAT_NV12:
            # NV12: Y plane (full) + UV plane (half height, interleaved)
            # Total = width * height * 1.5
            return int(width * height * 1.5)
        elif frame_format in (self.FORMAT_RGB, self.FORMAT_BGR):
            # RGB/BGR: 3 bytes per pixel
            return width * height * 3
        else:
            raise ValueError(f"Unknown frame format: {frame_format}")

    def _calculate_aligned_slot_size(self, frame_size: int) -> int:
        """Calculate page-aligned slot size for hardware efficiency.

        Pads frame slot size to PAGE_SIZE (4KB) boundaries for:
        - Better memory mapping performance
        - Improved cache efficiency
        - Future DMA/GPU transfer compatibility

        Args:
            frame_size: Unaligned frame size in bytes

        Returns:
            Page-aligned slot size in bytes
        """
        # Round up to next page boundary
        return ((frame_size + self.PAGE_SIZE - 1) // self.PAGE_SIZE) * self.PAGE_SIZE

    def _calculate_total_size(self) -> int:
        """Calculate total SHM size using page-aligned slots.

        Returns:
            Total size in bytes for entire SHM segment
        """
        # Use aligned slot size for frame data area
        return self.HEADER_SIZE + self._slot_metadata_size + (self._aligned_slot_size * self.slot_count)

    def _init_shared_memory(self, create: bool) -> None:
        """Initialize or attach to shared memory.

        Args:
            create: True to create new SHM, False to attach to existing

        Raises:
            FileExistsError: If create=True but SHM exists
            FileNotFoundError: If create=False but SHM doesn't exist
        """
        if create:
            try:
                # Try to create new SHM
                self._shm = shared_memory.SharedMemory(
                    name=self.shm_name,
                    create=True,
                    size=self._total_size
                )
                # Initialize header
                self._write_header(
                    write_idx=0,
                    width=self.width,
                    height=self.height,
                    frame_format=self.frame_format,
                    slot_count=self.slot_count,
                    last_ts_ns=int(time.time() * 1e9)
                )
                # Initialize slot metadata (all zeros = no valid frames yet)
                for slot in range(self.slot_count):
                    self._write_slot_frame_idx(slot, 0)
                    self._write_slot_seq_start(slot, 0)
                    self._write_slot_seq_end(slot, 0)

            except FileExistsError:
                # On Windows, SHM may exist from previous crashed run
                # Try to unlink and recreate
                self.logger.warning(f"SHM {self.shm_name} exists, attempting to reuse/recreate")
                try:
                    # Attach and unlink old one
                    old_shm = shared_memory.SharedMemory(name=self.shm_name, create=False)
                    old_shm.close()
                    old_shm.unlink()
                except Exception as e:
                    self.logger.warning(f"Could not unlink old SHM: {e}")

                # Try creating again
                self._shm = shared_memory.SharedMemory(
                    name=self.shm_name,
                    create=True,
                    size=self._total_size
                )
                self._write_header(
                    write_idx=0,
                    width=self.width,
                    height=self.height,
                    frame_format=self.frame_format,
                    slot_count=self.slot_count,
                    last_ts_ns=int(time.time() * 1e9)
                )
                for slot in range(self.slot_count):
                    self._write_slot_frame_idx(slot, 0)
                    self._write_slot_seq_start(slot, 0)
                    self._write_slot_seq_end(slot, 0)
        else:
            # Consumer: attach to existing SHM
            try:
                self._shm = shared_memory.SharedMemory(name=self.shm_name, create=False)

                # Validate header matches expected configuration
                header = self._read_header()
                if header['width'] != self.width or header['height'] != self.height:
                    self.logger.warning(
                        f"SHM dimension mismatch: expected {self.width}x{self.height}, "
                        f"got {header['width']}x{header['height']}"
                    )
                if header['format'] != self.frame_format:
                    self.logger.warning(
                        f"SHM format mismatch: expected {self.FORMAT_NAMES.get(self.frame_format)}, "
                        f"got {self.FORMAT_NAMES.get(header['format'], 'unknown')}"
                    )

            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SHM segment '{self.shm_name}' not found. "
                    f"Ensure producer (streaming gateway) is running first."
                )

    def _write_header(
        self,
        write_idx: int,
        width: int,
        height: int,
        frame_format: int,
        slot_count: int,
        last_ts_ns: int
    ) -> None:
        """Write header to SHM.

        Args:
            write_idx: Current write index
            width: Frame width
            height: Frame height
            frame_format: Frame format constant
            slot_count: Number of slots
            last_ts_ns: Timestamp in nanoseconds
        """
        header_bytes = struct.pack(
            self.HEADER_FORMAT,
            write_idx,
            width,
            height,
            frame_format,
            slot_count,
            last_ts_ns
        )
        # Pad to HEADER_SIZE
        header_bytes = header_bytes.ljust(self.HEADER_SIZE, b'\x00')
        self._shm.buf[:self.HEADER_SIZE] = header_bytes

    def _read_header(self) -> dict:
        """Read header from SHM.

        Returns:
            Dict with header fields: write_idx, width, height, format, slot_count, last_ts_ns
        """
        header_bytes = bytes(self._shm.buf[:struct.calcsize(self.HEADER_FORMAT)])
        write_idx, width, height, fmt, slot_count, last_ts_ns = struct.unpack(
            self.HEADER_FORMAT, header_bytes
        )
        return {
            'write_idx': write_idx,
            'width': width,
            'height': height,
            'format': fmt,
            'slot_count': slot_count,
            'last_ts_ns': last_ts_ns,
        }

    def _update_write_idx(self, new_idx: int) -> None:
        """Update write_idx in header (atomic uint64 write)."""
        # Write only the first 8 bytes (write_idx)
        self._shm.buf[:8] = struct.pack('<Q', new_idx)

    def _update_last_ts_ns(self, ts_ns: int) -> None:
        """Update heartbeat timestamp in header."""
        # last_ts_ns is at offset 24 (after write_idx=8 + width=4 + height=4 + format=4 + slot_count=4)
        offset = 8 + 4 + 4 + 4 + 4
        self._shm.buf[offset:offset+8] = struct.pack('<Q', ts_ns)

    def _get_slot_metadata_offset(self, slot: int) -> int:
        """Get offset for slot's metadata (frame_idx + seq_start + seq_end).

        Layout per slot (16 bytes):
            - frame_idx (8 bytes) at offset 0
            - seq_start (4 bytes) at offset 8
            - seq_end (4 bytes) at offset 12
        """
        return self.HEADER_SIZE + (slot * self.SLOT_METADATA_SIZE)

    def _write_slot_frame_idx(self, slot: int, frame_idx: int) -> None:
        """Write frame_idx to slot metadata."""
        offset = self._get_slot_metadata_offset(slot)
        self._shm.buf[offset:offset+8] = struct.pack('<Q', frame_idx)

    def _read_slot_frame_idx(self, slot: int) -> int:
        """Read frame_idx from slot metadata."""
        offset = self._get_slot_metadata_offset(slot)
        return struct.unpack('<Q', bytes(self._shm.buf[offset:offset+8]))[0]

    def _write_slot_seq_start(self, slot: int, seq: int) -> None:
        """Write seq_start counter for slot (incremented BEFORE frame write)."""
        offset = self._get_slot_metadata_offset(slot) + 8  # After frame_idx
        self._shm.buf[offset:offset+4] = struct.pack('<I', seq & 0xFFFFFFFF)

    def _read_slot_seq_start(self, slot: int) -> int:
        """Read seq_start counter for slot."""
        offset = self._get_slot_metadata_offset(slot) + 8
        return struct.unpack('<I', bytes(self._shm.buf[offset:offset+4]))[0]

    def _write_slot_seq_end(self, slot: int, seq: int) -> None:
        """Write seq_end counter for slot (incremented AFTER frame write)."""
        offset = self._get_slot_metadata_offset(slot) + 12  # After frame_idx + seq_start
        self._shm.buf[offset:offset+4] = struct.pack('<I', seq & 0xFFFFFFFF)

    def _read_slot_seq_end(self, slot: int) -> int:
        """Read seq_end counter for slot."""
        offset = self._get_slot_metadata_offset(slot) + 12
        return struct.unpack('<I', bytes(self._shm.buf[offset:offset+4]))[0]

    def _increment_slot_seq_start(self, slot: int) -> int:
        """Increment and return new seq_start for slot."""
        current = self._read_slot_seq_start(slot)
        new_seq = (current + 1) & 0xFFFFFFFF  # Wrap at 32-bit
        self._write_slot_seq_start(slot, new_seq)
        return new_seq

    def _increment_slot_seq_end(self, slot: int) -> int:
        """Increment and return new seq_end for slot."""
        current = self._read_slot_seq_end(slot)
        new_seq = (current + 1) & 0xFFFFFFFF  # Wrap at 32-bit
        self._write_slot_seq_end(slot, new_seq)
        return new_seq

    def _get_frame_offset(self, slot: int) -> int:
        """Get byte offset for frame data in given slot.

        Uses page-aligned slot size for hardware efficiency.
        """
        return self.HEADER_SIZE + self._slot_metadata_size + (slot * self._aligned_slot_size)

    def write_frame(self, raw_bytes: Union[bytes, memoryview, np.ndarray]) -> Tuple[int, int]:
        """Write frame to next slot (producer only).

        This method is NOT thread-safe - only one producer should write.
        Overwrites old frames in ring buffer pattern.

        OPTIMIZED: Uses cached counters to minimize SHM reads.
        Uses odd/even sequence semantics for torn frame and crash detection:
        - seq becomes ODD before writing (in progress)
        - seq becomes EVEN after writing (committed)
        - Consumer checks: seq_start != seq_end OR (seq_start & 1) → torn/crashed

        Args:
            raw_bytes: Raw frame data (NV12, RGB, or BGR bytes)

        Returns:
            Tuple of (frame_idx, slot_idx):
                - frame_idx: Monotonically increasing frame index
                - slot_idx: Physical slot where frame was written

        Raises:
            RuntimeError: If called on consumer instance
            ValueError: If raw_bytes size doesn't match expected frame_size
        """
        if not self._is_producer:
            raise RuntimeError("write_frame() can only be called on producer instance")

        # OPTIMIZATION: Use memoryview to avoid copies where possible
        if isinstance(raw_bytes, np.ndarray):
            # Get memoryview from contiguous numpy array (avoids tobytes() copy)
            if raw_bytes.flags['C_CONTIGUOUS']:
                raw_mv = memoryview(raw_bytes.data).cast('B')
            else:
                raw_bytes = raw_bytes.tobytes()
                raw_mv = memoryview(raw_bytes)
        elif isinstance(raw_bytes, memoryview):
            raw_mv = raw_bytes.cast('B') if raw_bytes.itemsize != 1 else raw_bytes
        else:
            raw_mv = memoryview(raw_bytes)

        if len(raw_mv) != self.frame_size:
            raise ValueError(
                f"Frame size mismatch: expected {self.frame_size} bytes, "
                f"got {len(raw_mv)} bytes"
            )

        # OPTIMIZATION: Use cached write_idx instead of reading from SHM
        self._cached_write_idx += 1
        frame_idx = self._cached_write_idx
        slot = frame_idx % self.slot_count

        # OPTIMIZATION: Use cached slot sequence with odd/even semantics
        # Odd = write in progress, Even = committed
        # This also enables crash detection (stuck on odd = crashed mid-write)
        self._cached_slot_seq[slot] += 1  # Now ODD → writing in progress
        seq_writing = self._cached_slot_seq[slot]
        self._write_slot_seq_start(slot, seq_writing)

        # Write frame data to slot using memoryview (zero-copy when possible)
        frame_offset = self._get_frame_offset(slot)
        self._shm.buf[frame_offset:frame_offset + self.frame_size] = raw_mv

        # Update slot metadata (frame_idx for this slot)
        self._write_slot_frame_idx(slot, frame_idx)

        # TORN FRAME DETECTION: Set seq_start = seq_end (now EVEN = committed)
        # Increment to make even, then write same value to BOTH seq_start and seq_end
        self._cached_slot_seq[slot] += 1  # Now EVEN → committed
        seq_committed = self._cached_slot_seq[slot]
        self._write_slot_seq_end(slot, seq_committed)
        self._write_slot_seq_start(slot, seq_committed)  # Update seq_start to EVEN too!

        # MEMORY BARRIER: Force all prior writes (seq_end, frame data) to be visible
        # to other processes BEFORE updating write_idx. This prevents the race where
        # consumer sees write_idx=N but seq_end for frame N is not yet visible.
        # Reading from the buffer forces a memory sync across process boundaries.
        _ = bytes(self._shm.buf[0:1])

        # Update header: write_idx and timestamp
        ts_ns = int(time.time() * 1e9)
        self._update_write_idx(frame_idx)
        self._update_last_ts_ns(ts_ns)

        return frame_idx, slot

    def read_frame(self, frame_idx: int) -> Optional[memoryview]:
        """Read frame by index (consumer).

        Returns a memoryview into the shared memory for zero-copy access.
        Caller should copy the data if needed beyond the current frame.

        IMPORTANT: This returns a memoryview which may be overwritten by the producer.
        For safe reads, use read_frame_copy() instead.

        Args:
            frame_idx: Frame index to read

        Returns:
            memoryview of frame data, or None if frame was overwritten or torn
        """
        if not self.is_frame_valid(frame_idx):
            return None

        slot = frame_idx % self.slot_count
        frame_offset = self._get_frame_offset(slot)

        # Return memoryview for zero-copy access
        # Note: For memoryview, caller should verify frame wasn't torn after reading
        return self._shm.buf[frame_offset:frame_offset + self.frame_size]

    def read_frame_copy(self, frame_idx: int, max_wait_ms: float = 5.0) -> Optional[bytes]:
        """Read frame and return a copy (consumer) with torn frame detection.

        Use this when you need the frame data to persist after
        the producer may overwrite the slot.

        This method detects torn frames using odd/even sequence semantics:
        - Reads seq_start BEFORE reading frame data
        - Reads seq_end AFTER reading frame data
        - Torn if: seq_start != seq_end (write in progress)
        - Write in progress if: seq_start is ODD

        RETRY LOGIC: If write is in progress (ODD seq_start), waits briefly
        for the write to complete instead of failing immediately. Producer
        typically finishes writing in ~1-2ms.

        Args:
            frame_idx: Frame index to read
            max_wait_ms: Max time to wait for write completion (default 5ms)

        Returns:
            Bytes copy of frame data, or None if frame was overwritten, torn, or corrupted
        """
        if not self.is_frame_valid(frame_idx):
            return None

        slot = frame_idx % self.slot_count
        start_time = time.time()
        max_wait_sec = max_wait_ms / 1000.0
        retry_count = 0

        while True:
            # TORN FRAME DETECTION: Read seq_start BEFORE reading frame data
            seq_start = self._read_slot_seq_start(slot)

            # WRITE IN PROGRESS: If seq_start is ODD, producer is currently writing
            # Wait briefly for write to complete instead of failing immediately
            if seq_start & 1:
                elapsed = time.time() - start_time
                if elapsed >= max_wait_sec:
                    # Timeout - write didn't complete in time
                    header = self._read_header()
                    current_write_idx = header['write_idx']
                    self.logger.warning(
                        f"[WRITE_TIMEOUT] frame_idx={frame_idx}, slot={slot}, "
                        f"seq_start={seq_start} (odd = write in progress), "
                        f"waited={elapsed*1000:.1f}ms, retries={retry_count}, "
                        f"write_idx={current_write_idx}, frames_behind={current_write_idx - frame_idx}"
                    )
                    return None
                # Wait a tiny bit and retry
                time.sleep(0.0002)  # 0.2ms
                retry_count += 1
                continue

            # Read frame data
            frame_offset = self._get_frame_offset(slot)
            frame_data = bytes(self._shm.buf[frame_offset:frame_offset + self.frame_size])

            # TORN FRAME DETECTION: Read seq_end AFTER reading frame data
            seq_end = self._read_slot_seq_end(slot)

            # If seq_start != seq_end, producer was writing during our read (torn frame)
            if seq_start != seq_end:
                elapsed = time.time() - start_time
                if elapsed >= max_wait_sec:
                    header = self._read_header()
                    current_write_idx = header['write_idx']
                    self.logger.warning(
                        f"[TORN_TIMEOUT] frame_idx={frame_idx}, slot={slot}, "
                        f"seq_start={seq_start}, seq_end={seq_end}, "
                        f"waited={elapsed*1000:.1f}ms, retries={retry_count}, "
                        f"write_idx={current_write_idx}, frames_behind={current_write_idx - frame_idx}"
                    )
                    return None
                # Write happened during our read - retry
                time.sleep(0.0002)  # 0.2ms
                retry_count += 1
                continue

            # Also verify the frame_idx didn't change during read (double-check)
            stored_frame_idx = self._read_slot_frame_idx(slot)
            if stored_frame_idx != frame_idx:
                # Frame was overwritten during our read - no point retrying
                header = self._read_header()
                current_write_idx = header['write_idx']
                self.logger.warning(
                    f"[OVERWRITE_DEBUG] expected frame_idx={frame_idx}, got stored={stored_frame_idx}, "
                    f"slot={slot}, write_idx={current_write_idx}, slot_count={self.slot_count}, "
                    f"frames_behind={current_write_idx - frame_idx}"
                )
                return None

            # SUCCESS - log if we had to retry
            if retry_count > 0:
                self.logger.debug(
                    f"[READ_SUCCESS_AFTER_RETRY] frame_idx={frame_idx}, retries={retry_count}, "
                    f"waited={(time.time() - start_time)*1000:.2f}ms"
                )

            return frame_data

    def is_frame_torn(self, frame_idx: int) -> bool:
        """Check if a frame read would be torn (producer writing during read).

        Uses odd/even semantics:
        - ODD seq_start = write in progress (or crashed)
        - seq_start != seq_end = write in progress

        Args:
            frame_idx: Frame index to check

        Returns:
            True if the frame is currently being written or corrupted (torn risk)
        """
        slot = frame_idx % self.slot_count
        seq_start = self._read_slot_seq_start(slot)
        seq_end = self._read_slot_seq_end(slot)
        # Torn if: seq mismatch OR seq_start is odd (crashed mid-write)
        return seq_start != seq_end or (seq_start & 1) == 1

    def is_frame_valid(self, frame_idx: int, max_wait_ms: float = 5.0) -> bool:
        """Check if frame_idx is still available (not overwritten).

        Handles cross-process memory visibility delays by retrying when:
        1. Frame appears to be in the future (frame_idx > write_idx)
        2. Frame is at the edge (frame_idx == write_idx) but slot metadata not visible yet

        The v2 fix addresses the race condition where:
        - Producer writes frame data, updates slot metadata, then updates write_idx
        - Consumer reads write_idx (e.g., 2343), sees frames_behind=0
        - Consumer reads slot metadata but it's NOT YET VISIBLE
        - Without retry, this incorrectly returns False ("Frame not yet written")

        Args:
            frame_idx: Frame index to validate
            max_wait_ms: Max time to wait for visibility (default 5ms)

        Returns:
            True if frame is still valid and readable
        """
        if frame_idx <= 0:
            return False

        start_time = time.time()
        max_wait_sec = max_wait_ms / 1000.0

        while True:
            # Check if within ring buffer window
            header = self._read_header()
            current_write_idx = header['write_idx']

            # Frame is too old - overwritten, no retry will help
            if current_write_idx - frame_idx >= self.slot_count:
                return False

            # Frame is in the future - retry until visible or timeout
            if frame_idx > current_write_idx:
                if time.time() - start_time >= max_wait_sec:
                    return False  # Timeout - genuinely not written yet
                time.sleep(0.0001)  # 0.1ms
                continue

            # Frame is within valid range - check slot metadata
            slot = frame_idx % self.slot_count
            stored_frame_idx = self._read_slot_frame_idx(slot)

            if stored_frame_idx == frame_idx:
                return True  # SUCCESS - frame is valid

            # === KEY FIX v2: Retry on slot mismatch when at the edge ===
            # When frame_idx == write_idx, the slot metadata may not be visible yet
            # due to cross-process memory visibility delay (mmap propagation)
            if frame_idx == current_write_idx:
                if time.time() - start_time >= max_wait_sec:
                    return False  # Timeout - visibility never propagated
                time.sleep(0.0001)  # 0.1ms
                continue  # RETRY the slot metadata check

            # Slot mismatch and NOT at the edge - frame was overwritten
            return False

    def get_current_frame_idx(self) -> int:
        """Get latest written frame index.

        Returns:
            Current write_idx (0 if no frames written yet)
        """
        header = self._read_header()
        return header['write_idx']

    def get_last_heartbeat_ns(self) -> int:
        """Get last heartbeat timestamp in nanoseconds.

        Useful for detecting if producer is still alive.

        Returns:
            Last write timestamp in nanoseconds
        """
        header = self._read_header()
        return header['last_ts_ns']

    def is_producer_alive(self, timeout_ns: int = 2_000_000_000) -> bool:
        """Check if producer is still alive (heartbeat watchdog).

        This is critical for production deployments:
        - Detects producer crashes
        - Allows consumers to detach/reconnect
        - Prevents spinning on stale data

        Args:
            timeout_ns: Max time since last write before considering producer dead.
                       Default: 2 seconds (2_000_000_000 ns)

        Returns:
            True if producer has written within timeout_ns
        """
        now_ns = time.time_ns()
        last_heartbeat = self.get_last_heartbeat_ns()
        return (now_ns - last_heartbeat) < timeout_ns

    def get_producer_age_ms(self) -> float:
        """Get time since last producer write in milliseconds.

        Useful for monitoring and diagnostics.

        Returns:
            Milliseconds since last frame was written
        """
        now_ns = time.time_ns()
        last_heartbeat = self.get_last_heartbeat_ns()
        return (now_ns - last_heartbeat) / 1_000_000

    def get_header(self) -> dict:
        """Get full header information.

        Returns:
            Dict with all header fields
        """
        return self._read_header()

    def close(self) -> None:
        """Close and optionally unlink SHM.

        Producer unlinks (deletes) the SHM segment.
        Consumer just detaches without deleting.
        """
        if self._shm is None:
            return

        try:
            self._shm.close()

            if self._is_producer:
                # Producer is responsible for cleanup
                try:
                    self._shm.unlink()
                    self.logger.info(f"SHM segment {self.shm_name} unlinked")
                except FileNotFoundError:
                    pass  # Already unlinked (maybe by another process)
                except Exception as e:
                    self.logger.warning(f"Error unlinking SHM {self.shm_name}: {e}")
            else:
                self.logger.debug(f"Detached from SHM segment {self.shm_name}")

        except Exception as e:
            self.logger.warning(f"Error closing SHM {self.shm_name}: {e}")
        finally:
            self._shm = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ShmRingBuffer(name={self.shm_name}, "
            f"{self.width}x{self.height} {self.FORMAT_NAMES.get(self.frame_format, 'unknown')}, "
            f"slots={self.slot_count}, producer={self._is_producer})"
        )

    # =========================================================================
    # Health Check and Utility APIs (v1.1)
    # =========================================================================

    def get_health_status(self) -> Dict:
        """Get comprehensive health status for orchestration tools.

        Useful for:
        - Kubernetes liveness/readiness probes
        - Docker HEALTHCHECK
        - Prometheus metrics
        - Container orchestration

        Returns:
            Dict with health status fields:
            - is_healthy: Overall health status
            - producer_alive: Whether producer is writing
            - producer_age_ms: Time since last frame
            - frames_written: Total frames written
            - buffer_utilization: 0.0-1.0 utilization ratio
            - error_message: Error details if unhealthy
        """
        try:
            header = self._read_header()
            producer_alive = self.is_producer_alive()
            producer_age_ms = self.get_producer_age_ms()
            frames_written = header['write_idx']

            # Calculate utilization (capped at 1.0)
            utilization = min(1.0, frames_written / self.slot_count) if self.slot_count > 0 else 0.0

            return {
                'is_healthy': True,
                'producer_alive': producer_alive,
                'producer_age_ms': producer_age_ms,
                'frames_written': frames_written,
                'buffer_utilization': utilization,
                'shm_name': self.shm_name,
                'width': self.width,
                'height': self.height,
                'frame_format': self.FORMAT_NAMES.get(self.frame_format, 'unknown'),
                'slot_count': self.slot_count,
                'frame_size': self.frame_size,
                'is_producer': self._is_producer,
                'error_message': None,
            }
        except Exception as e:
            return {
                'is_healthy': False,
                'producer_alive': False,
                'producer_age_ms': float('inf'),
                'frames_written': 0,
                'buffer_utilization': 0.0,
                'shm_name': self.shm_name,
                'error_message': str(e),
            }

    def wait_for_producer(
        self,
        timeout_sec: float = 30.0,
        poll_interval_ms: float = 100.0
    ) -> bool:
        """Wait for producer to start writing frames.

        Useful for container startup ordering when consumer needs
        to wait for producer to be ready.

        Args:
            timeout_sec: Maximum time to wait (default 30s)
            poll_interval_ms: Polling interval (default 100ms)

        Returns:
            True if producer started within timeout, False otherwise
        """
        start_time = time.time()
        poll_interval_sec = poll_interval_ms / 1000.0

        while time.time() - start_time < timeout_sec:
            if self.get_current_frame_idx() > 0 and self.is_producer_alive():
                return True
            time.sleep(poll_interval_sec)

        return False

    @staticmethod
    def cleanup_stale_buffers(prefix: str = "shm_cam_") -> List[str]:
        """Clean up stale SHM segments from crashed processes.

        Scans /dev/shm for segments matching the prefix and removes
        those that appear to be orphaned (no active producer).

        Useful for:
        - Container restart cleanup hooks
        - Development/testing cleanup
        - Recovery from crashes

        Args:
            prefix: SHM name prefix to match (default: "shm_cam_")

        Returns:
            List of cleaned up SHM segment names

        Note:
            On Linux, SHM segments are files in /dev/shm/
            On macOS/Windows, this uses the shared_memory API
        """
        cleaned: List[str] = []
        shm_path = "/dev/shm"

        if not os.path.exists(shm_path):
            # Not Linux, try to list via other means
            return cleaned

        try:
            for entry in os.listdir(shm_path):
                if not entry.startswith(prefix):
                    continue

                try:
                    # Try to attach and check if producer is alive
                    shm = shared_memory.SharedMemory(name=entry, create=False)

                    # Read header to check heartbeat
                    buf: Any = shm.buf
                    header_bytes = bytes(buf[:struct.calcsize('<QIIIIQ')])
                    _, _, _, _, _, last_ts_ns = struct.unpack('<QIIIIQ', header_bytes)

                    # If no heartbeat in 10 seconds, consider stale
                    now_ns = time.time_ns()
                    if (now_ns - last_ts_ns) > 10_000_000_000:  # 10 seconds
                        shm.close()
                        shm.unlink()
                        cleaned.append(entry)
                    else:
                        shm.close()

                except FileNotFoundError:
                    # Already cleaned up
                    pass
                except Exception:
                    # Can't access - leave it alone
                    pass

        except Exception:
            pass

        return cleaned

    @staticmethod
    def list_buffers(prefix: str = "shm_cam_") -> List[Dict]:
        """List all active SHM ring buffers matching prefix.

        Scans for SHM segments and returns info about each.

        Args:
            prefix: SHM name prefix to match

        Returns:
            List of dicts with buffer info:
            - name: SHM segment name
            - size: Total size in bytes
            - frames_written: Number of frames written
            - producer_alive: Whether producer is active
            - age_ms: Time since last write
        """
        buffers: List[Dict[str, Any]] = []
        shm_path = "/dev/shm"

        if not os.path.exists(shm_path):
            return buffers

        try:
            for entry in os.listdir(shm_path):
                if not entry.startswith(prefix):
                    continue

                try:
                    shm = shared_memory.SharedMemory(name=entry, create=False)

                    # Read header
                    buf: Any = shm.buf
                    header_bytes = bytes(buf[:struct.calcsize('<QIIIIQ')])
                    write_idx, width, height, fmt, slot_count, last_ts_ns = struct.unpack(
                        '<QIIIIQ', header_bytes
                    )

                    now_ns = time.time_ns()
                    age_ms = (now_ns - last_ts_ns) / 1_000_000
                    producer_alive = age_ms < 2000  # 2 second timeout

                    buffers.append({
                        'name': entry,
                        'size': shm.size,
                        'width': width,
                        'height': height,
                        'format': fmt,
                        'slot_count': slot_count,
                        'frames_written': write_idx,
                        'producer_alive': producer_alive,
                        'age_ms': age_ms,
                    })

                    shm.close()

                except Exception:
                    pass

        except Exception:
            pass

        return buffers

    def benchmark_write_throughput(
        self,
        num_frames: int = 1000,
        frame_data: Optional[bytes] = None
    ) -> Dict:
        """Benchmark write throughput (producer only).

        Writes num_frames as fast as possible and measures performance.

        Args:
            num_frames: Number of frames to write
            frame_data: Optional pre-generated frame data

        Returns:
            Dict with benchmark results:
            - fps: Frames per second achieved
            - latency_us_avg: Average write latency in microseconds
            - latency_us_p50: Median write latency
            - latency_us_p99: 99th percentile latency
            - throughput_mbps: Megabytes per second
            - throughput_gbps: Gigabits per second
        """
        if not self._is_producer:
            raise RuntimeError("benchmark_write_throughput() can only be called on producer")

        if frame_data is None:
            frame_data = bytes(self.frame_size)

        latencies = []
        start = time.perf_counter()

        for _ in range(num_frames):
            t0 = time.perf_counter()
            self.write_frame(frame_data)
            latencies.append((time.perf_counter() - t0) * 1e6)

        elapsed = time.perf_counter() - start
        latencies_sorted = sorted(latencies)

        total_bytes = num_frames * self.frame_size

        return {
            'num_frames': num_frames,
            'elapsed_sec': elapsed,
            'fps': num_frames / elapsed,
            'latency_us_avg': sum(latencies) / len(latencies),
            'latency_us_p50': latencies_sorted[len(latencies_sorted) // 2],
            'latency_us_p99': latencies_sorted[int(len(latencies_sorted) * 0.99)],
            'throughput_mbps': (total_bytes / elapsed) / (1024 * 1024),
            'throughput_gbps': (total_bytes * 8 / elapsed) / 1e9,
        }


# =============================================================================
# NV12 Conversion Helper Functions
# =============================================================================

def bgr_to_nv12(bgr_frame: np.ndarray) -> bytes:
    """Convert BGR frame to NV12 format (GPU-friendly).

    NV12 layout:
    - Y plane: width * height bytes (luma - brightness)
    - UV plane: width * height / 2 bytes (interleaved chroma - color)
    - Total: width * height * 1.5 bytes

    This format is optimal for GPU-based inference (CUDA, TensorRT) as it:
    1. Matches camera sensor output (YUV native)
    2. Enables hardware-accelerated color space conversion
    3. Reduces memory bandwidth (1.5 vs 3 bytes per pixel)

    Args:
        bgr_frame: OpenCV BGR frame (numpy array, shape HxWx3, dtype uint8)

    Returns:
        NV12 bytes (Y plane followed by interleaved UV plane)

    Example:
        frame = cv2.imread("image.jpg")  # BGR format
        nv12_bytes = bgr_to_nv12(frame)
        assert len(nv12_bytes) == frame.shape[0] * frame.shape[1] * 1.5
    """
    import cv2

    height, width = bgr_frame.shape[:2]

    # BGR -> YUV_I420 (Y plane, U plane, V plane - all separate)
    yuv_i420 = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2YUV_I420)

    # I420 layout in OpenCV:
    # - Y plane: rows 0 to height-1 (full resolution)
    # - U plane: rows height to height + height/4 (quarter resolution)
    # - V plane: rows height + height/4 to height + height/2 (quarter resolution)

    # Extract planes
    y_end = height
    u_end = height + height // 4
    v_end = height + height // 2

    y_plane = yuv_i420[:y_end, :].flatten()
    u_plane = yuv_i420[y_end:u_end, :].flatten()
    v_plane = yuv_i420[u_end:v_end, :].flatten()

    # NV12 has interleaved UV (UVUVUV...) instead of separate U and V planes
    uv_interleaved: np.ndarray = np.empty(len(u_plane) * 2, dtype=np.uint8)
    uv_interleaved[0::2] = u_plane
    uv_interleaved[1::2] = v_plane

    # Concatenate Y and interleaved UV
    return np.concatenate([y_plane, uv_interleaved]).tobytes()


def nv12_to_bgr(nv12_bytes: bytes, width: int, height: int) -> np.ndarray:
    """Convert NV12 bytes back to BGR frame.

    Args:
        nv12_bytes: NV12 format bytes
        width: Frame width
        height: Frame height

    Returns:
        BGR numpy array (shape HxWx3, dtype uint8)
    """
    import cv2

    # Calculate expected sizes
    y_size = width * height
    uv_size = y_size // 2
    expected_size = y_size + uv_size

    if len(nv12_bytes) != expected_size:
        raise ValueError(f"NV12 size mismatch: expected {expected_size}, got {len(nv12_bytes)}")

    # Create NV12 array for OpenCV
    # OpenCV expects NV12 in a specific layout
    nv12_array = np.frombuffer(nv12_bytes, dtype=np.uint8).reshape((height + height // 2, width))

    # Convert NV12 -> BGR
    bgr_frame = cv2.cvtColor(nv12_array, cv2.COLOR_YUV2BGR_NV12)

    return bgr_frame


def rgb_to_nv12(rgb_frame: np.ndarray) -> bytes:
    """Convert RGB frame to NV12 format.

    Args:
        rgb_frame: RGB frame (numpy array, shape HxWx3, dtype uint8)

    Returns:
        NV12 bytes
    """
    import cv2

    # RGB -> BGR -> NV12
    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
    return bgr_to_nv12(bgr_frame)
