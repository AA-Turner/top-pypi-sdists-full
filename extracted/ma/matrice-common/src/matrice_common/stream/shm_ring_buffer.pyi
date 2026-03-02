"""Auto-generated stub for module: shm_ring_buffer."""
from typing import Any, Dict, List, Optional, Tuple, Union

# Functions
def bgr_to_nv12(bgr_frame: Any.Any) -> Any:
    """
    Convert BGR frame to NV12 format (GPU-friendly).
    
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
    ...
def nv12_to_bgr(nv12_bytes: Any, width: int, height: int) -> Any.Any:
    """
    Convert NV12 bytes back to BGR frame.
    
        Args:
            nv12_bytes: NV12 format bytes
            width: Frame width
            height: Frame height
    
        Returns:
            BGR numpy array (shape HxWx3, dtype uint8)
    """
    ...
def rgb_to_nv12(rgb_frame: Any.Any) -> Any:
    """
    Convert RGB frame to NV12 format.
    
        Args:
            rgb_frame: RGB frame (numpy array, shape HxWx3, dtype uint8)
    
        Returns:
            NV12 bytes
    """
    ...

# Classes
class ShmRingBuffer:
    # Shared memory ring buffer for raw frame storage.
    #
    #     Supports NV12, RGB, and BGR frame formats for efficient video streaming.
    #     Uses a lock-free design where the producer overwrites old frames without
    #     waiting for consumers.
    #
    #     Example (Producer):
    #         buffer = ShmRingBuffer(
    #             camera_id="cam_001",
    #             width=1920,
    #             height=1080,
    #             frame_format=ShmRingBuffer.FORMAT_BGR,  # Default - no conversion needed
    #             slot_count=300,
    #             create=True
    #         )
    #         frame_idx, slot = buffer.write_frame(bgr_frame.tobytes())
    #
    #     Example (Consumer):
    #         buffer = ShmRingBuffer(
    #             camera_id="cam_001",
    #             width=1920,
    #             height=1080,
    #             frame_format=ShmRingBuffer.FORMAT_BGR,  # Default
    #             slot_count=300,
    #             create=False  # Attach to existing
    #         )
    #         if buffer.is_frame_valid(frame_idx):
    #             frame_data = buffer.read_frame(frame_idx)

    def __init__(self: Any, camera_id: str, width: int, height: int, frame_format: int = FORMAT_BGR, slot_count: int = 300, create: bool = True, shm_name: Optional[str] = None) -> None:
        """
        Initialize SHM ring buffer.
        
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
        ...

    FORMAT_BGR: int
    FORMAT_NAMES: Dict[Any, Any]
    FORMAT_NV12: int
    FORMAT_RGB: int
    HEADER_FORMAT: str
    HEADER_SIZE: int
    PAGE_SIZE: int
    SLOT_METADATA_SIZE: int

    def benchmark_write_throughput(self: Any, num_frames: int = 1000, frame_data: Optional[Any] = None) -> Dict:
        """
        Benchmark write throughput (producer only).
        
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
        ...

    def cleanup_stale_buffers(prefix: str = 'shm_cam_') -> List[str]:
        """
        Clean up stale SHM segments from crashed processes.
        
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
        ...

    def close(self: Any) -> None:
        """
        Close and optionally unlink SHM.
        
                Producer unlinks (deletes) the SHM segment.
                Consumer just detaches without deleting.
        """
        ...

    def get_current_frame_idx(self: Any) -> int:
        """
        Get latest written frame index.
        
                Returns:
                    Current write_idx (0 if no frames written yet)
        """
        ...

    def get_header(self: Any) -> dict:
        """
        Get full header information.
        
                Returns:
                    Dict with all header fields
        """
        ...

    def get_health_status(self: Any) -> Dict:
        """
        Get comprehensive health status for orchestration tools.
        
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
        ...

    def get_last_heartbeat_ns(self: Any) -> int:
        """
        Get last heartbeat timestamp in nanoseconds.
        
                Useful for detecting if producer is still alive.
        
                Returns:
                    Last write timestamp in nanoseconds
        """
        ...

    def get_producer_age_ms(self: Any) -> float:
        """
        Get time since last producer write in milliseconds.
        
                Useful for monitoring and diagnostics.
        
                Returns:
                    Milliseconds since last frame was written
        """
        ...

    def is_frame_torn(self: Any, frame_idx: int) -> bool:
        """
        Check if a frame read would be torn (producer writing during read).
        
                Uses odd/even semantics:
                - ODD seq_start = write in progress (or crashed)
                - seq_start != seq_end = write in progress
        
                Args:
                    frame_idx: Frame index to check
        
                Returns:
                    True if the frame is currently being written or corrupted (torn risk)
        """
        ...

    def is_frame_valid(self: Any, frame_idx: int, max_wait_ms: float = 5.0) -> bool:
        """
        Check if frame_idx is still available (not overwritten).
        
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
        ...

    def is_producer_alive(self: Any, timeout_ns: int = 2000000000) -> bool:
        """
        Check if producer is still alive (heartbeat watchdog).
        
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
        ...

    def list_buffers(prefix: str = 'shm_cam_') -> List[Dict]:
        """
        List all active SHM ring buffers matching prefix.
        
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
        ...

    def read_frame(self: Any, frame_idx: int) -> Optional[Any]:
        """
        Read frame by index (consumer).
        
                Returns a memoryview into the shared memory for zero-copy access.
                Caller should copy the data if needed beyond the current frame.
        
                IMPORTANT: This returns a memoryview which may be overwritten by the producer.
                For safe reads, use read_frame_copy() instead.
        
                Args:
                    frame_idx: Frame index to read
        
                Returns:
                    memoryview of frame data, or None if frame was overwritten or torn
        """
        ...

    def read_frame_copy(self: Any, frame_idx: int, max_wait_ms: float = 5.0) -> Optional[Any]:
        """
        Read frame and return a copy (consumer) with torn frame detection.
        
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
        ...

    def wait_for_producer(self: Any, timeout_sec: float = 30.0, poll_interval_ms: float = 100.0) -> bool:
        """
        Wait for producer to start writing frames.
        
                Useful for container startup ordering when consumer needs
                to wait for producer to be ready.
        
                Args:
                    timeout_sec: Maximum time to wait (default 30s)
                    poll_interval_ms: Polling interval (default 100ms)
        
                Returns:
                    True if producer started within timeout, False otherwise
        """
        ...

    def write_frame(self: Any, raw_bytes: Union[Any, Any, Any.Any]) -> Tuple[int, int]:
        """
        Write frame to next slot (producer only).
        
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
        ...

