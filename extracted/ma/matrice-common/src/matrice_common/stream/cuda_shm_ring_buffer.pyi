"""Auto-generated stub for module: cuda_shm_ring_buffer."""
from typing import Any, Dict, Optional, Set, Tuple

from .shm_ring_buffer import ShmRingBuffer

# Constants
CUDA_IPC_HANDLE_SIZE: int
MAP_SHARED: Any
PROT_READ: Any
PROT_WRITE: Any
SHM_BASE_PATH: Any
logger: Any

# Functions
def benchmark_cuda_ipc() -> None:
    """
    Benchmark CUDA IPC ring buffer performance.
    """
    ...

# Classes
class CudaIpcRingBuffer:
    # CUDA IPC Ring Buffer for zero-copy cross-process GPU memory sharing.
    #
    #     This class manages a ring buffer stored entirely in GPU memory, with
    #     metadata stored in POSIX shared memory for cross-process coordination.

    def __init__(self: Any, camera_id: str, gpu_id: int, num_slots: int, width: int, height: int, channels: int, is_producer: bool) -> None: ...

    CONSUMER_SLOT_SIZE: int
    HEADER_SIZE: Any
    MAX_CONSUMERS: int
    SESSION_INFO_OFFSET: Any
    SESSION_INFO_SIZE: int
    SLOT_META_SIZE: int

    def ack_frame_done(self: Any, frame_idx: int) -> Any:
        """
        Acknowledge that consumer has finished processing up to frame_idx.
        
                Multi-consumer design: Each consumer has its own cursor in SHM.
                This allows monitoring consumer progress and coordinating multiple consumers.
        
                Args:
                    frame_idx: The highest frame index that has been fully processed
        """
        ...

    def check_file_recreated(self: Any) -> bool:
        """
        Check if the SHM file has been recreated (different inode).
        
                When the producer (SG) restarts, it unlinks and recreates the SHM file,
                giving it a new inode. Our fd still points to the old (deleted) file.
                Comparing os.fstat(fd) vs os.stat(path) detects this.
        
                Returns:
                    True if file was recreated (stale) or missing, False if same file.
        """
        ...

    def close(self: Any) -> Any:
        """
        Close and cleanup resources.
        
                Order matters on Jetson Thor unified memory: drop the GPU buffer view,
                then call ipcCloseMemHandle (consumer side) so the GPU driver releases
                its mapping to the producer's pages, then flush CuPy's mempool blocks
                back to the driver. Skipping any of these leaves pages tied to inode
                references that only ``drop_caches=2`` reclaims.
        """
        ...

    def connect(self: Any, stale_threshold_sec: float = 30.0) -> bool:
        """
        Connect as consumer - import CUDA IPC handle.
        
                Args:
                    stale_threshold_sec: Warn if last write was more than this many seconds ago
        """
        ...

    def connect_consumer(cls: Any, camera_id: str, gpu_id: int = 0, consumer_key: str = 'default', max_retries: int = 10, retry_delay: float = 0.5) -> 'Any':
        """
        Connect as consumer with retry logic for cross-container startup race.
        
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
        ...

    def create_producer(cls: Any, camera_id: str, gpu_id: int = 0, num_slots: int = 8, width: int = 640, height: int = 640, channels: int = 1) -> 'Any':
        """
        Create a producer ring buffer.
        
                For NV12: height should be H*1.5 (e.g., 960 for 640x640 frames), channels=1
        """
        ...

    def get_all_consumer_cursors(self: Any) -> Dict[int, int]:
        """
        Get all registered consumer cursors (for monitoring).
        
                Returns:
                    Dict mapping consumer_id -> frame_idx for all registered consumers
        """
        ...

    def get_committed_idx(self: Any) -> int:
        """
        Read committed index — highest frame_idx with completed GPU writes.
        
                Returns 0 if producer hasn't called sync_writes() yet (or is an
                old version that doesn't support committed_idx). Consumers should
                fall back to get_write_idx() when this returns 0.
        """
        ...

    def get_consumer_cursor(self: Any, consumer_id: Optional[int] = None) -> int:
        """
        Get a consumer's cursor position (for debugging/monitoring).
        
                Args:
                    consumer_id: Consumer ID to query. Defaults to this consumer's ID.
        """
        ...

    def get_file_inode(self: Any) -> int:
        """
        Get the inode of the currently open SHM file descriptor.
        
                Returns 0 if fd is not open or fstat fails.
        """
        ...

    def get_frames_behind(self: Any) -> int:
        """
        Get number of frames this consumer is behind the producer.
        
                Useful for monitoring consumer performance and detecting backpressure.
        """
        ...

    def get_registered_consumers(self: Any) -> Dict[int, Dict]:
        """
        Get all registered consumer slots with their key hashes (for monitoring).
        
                Returns:
                    Dict mapping consumer_id -> {"key_hash": int, "cursor": int}
        """
        ...

    def get_session_info(self: Any) -> Tuple[str, int]:
        """
        Get RTSP session info for Mode B frame-accurate sync.
        
                Consumer can call this to get current session info.
        
                Returns:
                    (session_id, session_start_ns) tuple
                    session_id: 8-char unique session ID (empty string if not set)
                    session_start_ns: T0 wall clock (ns) when RTSP connected (0 if not set)
        """
        ...

    def get_source_dims(self: Any, slot: int) -> Tuple[int, int]:
        """
        Read the pre-resize source dimensions stored with a slot.
        
                Returns (0, 0) when the producer did not set them — callers should
                treat that as "unknown" and fall back to ring-buffer dimensions.
        
                Args:
                    slot: Slot index to read.
        
                Returns:
                    (src_w, src_h) tuple in pixels.
        """
        ...

    def get_status(self: Any) -> Dict:
        """
        Get ring buffer status.
        """
        ...

    def get_write_idx(self: Any) -> int:
        """
        Get current write index.
        """
        ...

    def initialize(self: Any) -> bool:
        """
        Initialize as producer - allocate GPU memory and create SHM.
        """
        ...

    def read_frame(self: Any, slot: int) -> Optional[Any.Any]:
        """
        Read a frame from a specific slot (NO COPY - view).
        
                Self-heals on CUDA IPC invalidation: if constructing the view faults
                because the producer reallocated its GPU buffer, the handle is
                re-imported once and the read retried. Returns None if recovery fails.
        """
        ...

    def read_latest(self: Any) -> Tuple[Optional[Any.Any], int]:
        """
        Read the most recently written frame (NO COPY - view).
        
                Note: For sequential processing with skip detection, use read_next() instead.
        """
        ...

    def read_next(self: Any) -> Tuple[Optional[Any.Any], int, bool]:
        """
        Read next frame after last read, with skip detection.
        
                Multi-consumer design: Each consumer tracks its own position.
                If consumer falls behind (producer overwrote frames), skips forward.
        
                Returns:
                    (frame, frame_idx, was_skipped)
                    - frame: GPU array view, or None if no new frames
                    - frame_idx: The frame index, or -1 if no new frames
                    - was_skipped: True if frames were skipped (consumer too slow)
        """
        ...

    def revalidate(self: Any) -> bool:
        """
        Public hook: recover from a CUDA IPC invalidation on demand.
        
                Consumers that hold a frame *view* and only dereference it later (e.g.
                inside a preprocessing kernel) won't fault until that dereference. When
                they catch a ``CUDA_ERROR_ILLEGAL_ADDRESS`` they should call this to
                rebuild the mapping, then re-read the frame. Returns True on success.
        """
        ...

    def set_session_info(self: Any, session_id: str, session_start_ns: int) -> Any:
        """
        Set RTSP session info for Mode B frame-accurate sync.
        
                Producer should call this when RTSP connects/reconnects.
        
                Args:
                    session_id: 8-char unique session ID (changes on reconnect)
                    session_start_ns: T0 wall clock (ns) when RTSP connected
        """
        ...

    def sync_writes(self: Any) -> Any:
        """
        Sync all pending GPU writes and publish committed_idx.
        
                After this call, all frames written via write_frame_fast(sync=False)
                are guaranteed to have their GPU data fully written. Consumers reading
                get_committed_idx() will see the updated value and can safely read
                those frames without encountering stale/zero GPU memory.
        """
        ...

    def update_committed_idx(self: Any) -> Any:
        """
        Publish committed_idx without GPU sync.
        
                Use after another ring buffer's sync_writes() has already synchronized
                a shared CUDA stream. This avoids redundant GPU stalls when multiple
                ring buffers share the same stream.
        """
        ...

    def write_frame(self: Any, gpu_frame: Any.Any, src_w: int = 0, src_h: int = 0) -> int:
        """
        Write a frame to the ring buffer - NEVER BLOCKS.
        
                Multi-consumer design: Producer always wins and overwrites ring buffer.
                Slow consumers will detect skipped frames via read_next().
        
                Args:
                    gpu_frame: NV12 frame to write (must match frame_shape)
                    src_w: Pre-resize source frame width (uint16, 0 = unknown). When the
                        producer resizes/letterboxes before writing, pass the ORIGINAL
                        source width so consumers can invert the geometry.
                    src_h: Pre-resize source frame height (uint16, 0 = unknown).
        
                Returns:
                    Frame index (always succeeds, never returns -1)
        """
        ...

    def write_frame_fast(self: Any, gpu_frame: Any.Any, sync: bool = True, timestamp_ns: Optional[int] = None, rtp_timestamp: int = 0, src_w: int = 0, src_h: int = 0) -> int:
        """
        Fast write without device context switch - NEVER BLOCKS.
        
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
                    src_w: Pre-resize source frame width (uint16, 0 = unknown). When the
                        producer resizes/letterboxes before writing, pass the ORIGINAL
                        source width so consumers can invert the geometry.
                    src_h: Pre-resize source frame height (uint16, 0 = unknown).
        
                Returns:
                    Frame index written
        """
        ...

class GlobalFrameCounter:
    # Global atomic frame counter for event-driven notification.
    #
    #     Instead of polling N ring buffers, consumers watch ONE counter.
    #     When counter changes → new frames available somewhere.

    def __init__(self: Any, is_producer: bool = True) -> None: ...

    SHM_PATH: Any
    SIZE: int

    def close(self: Any) -> Any:
        """
        Close counter.
        """
        ...

    def connect(self: Any) -> bool:
        """
        Connect to counter (consumer).
        """
        ...

    def get(self: Any) -> int:
        """
        Get current value.
        """
        ...

    def increment(self: Any) -> int:
        """
        Increment and return new value.
        """
        ...

    def initialize(self: Any) -> bool:
        """
        Initialize counter (producer).
        """
        ...

    def wait_for_change(self: Any, last_value: int, timeout_ms: float = 100.0) -> Tuple[int, bool]:
        """
        Wait for counter to change.
        """
        ...

