"""Auto-generated stub for module: shm_ring_buffer."""
from typing import Any, Dict, List, Optional, Tuple, Union

# Constants
CUDA_IPC_HANDLE_SIZE: int
MAP_SHARED: Any
PROT_READ: Any
PROT_WRITE: Any
SHM_BASE_PATH: Any
logger: Any

# Functions
def bgr_to_nv12(bgr_frame: 'Any.Any') -> Any:
    """
    Convert BGR frame to NV12 format.
    """
    ...
def nv12_to_bgr(nv12_bytes: Any, width: int, height: int) -> 'Any.Any':
    """
    Convert NV12 bytes to BGR frame.
    """
    ...
def rgb_to_nv12(rgb_frame: 'Any.Any') -> Any:
    """
    Convert RGB frame to NV12 format.
    """
    ...

# Classes
class ShmRingBuffer:
    # Unified POSIX SHM ring buffer with multi-consumer support,
    #     torn frame detection, GPU frame support, and health monitoring.
    #
    #     Supports two usage modes:
    #     - GPU frame streaming: width/height/channels for raw video frames
    #     - Message passing: max_msg_size for serialized JSON/bytes (DataBus)
    #
    #     Header layout (768 bytes):
    #       0-7:     write_idx (Q)
    #       8-15:    read_idx (Q, legacy compat)
    #       16-23:   frame_count (Q, = write_idx)
    #       24-31:   timestamp_ns (Q, heartbeat)
    #       32-35:   gpu_id (I)
    #       36-39:   num_slots (I)
    #       40-43:   width (I)
    #       44-47:   height (I)
    #       48-51:   channels (I)
    #       52-55:   dtype_code (I, 0=uint8)
    #       56-63:   flags (Q)
    #       64-127:  ipc_handle (64B, zeroed — CudaIpc compat)
    #       128-135: max_consumers (Q, =32)
    #       136-647: consumer_registry[32] (16B × 32: key_hash + cursor)
    #       648-655: session_id (8B ASCII)
    #       656-663: session_start_ns (Q)
    #       664-667: frame_format (I)
    #       668-671: frame_size (I)
    #       672-675: aligned_slot_size (I)
    #       676-679: magic (I, 0x4D415452 = "MATR")
    #       680-683: version (I, =2)
    #       684-767: reserved (84B, zeroed)
    #
    #     Per-slot metadata (48 bytes):
    #       0-7:   frame_idx (Q)
    #       8-15:  timestamp_ns (Q)
    #       16-23: flags (Q)
    #       24-27: rtp_timestamp (I)
    #       28-31: seq_start (I) — torn frame: incremented BEFORE write
    #       32-35: seq_end (I) — torn frame: incremented AFTER write
    #       36-47: padding (12B)

    def __init__(self: Any, camera_id: str) -> None:
        """
        Initialize SHM ring buffer.
        
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
        ...

    def ack_frame_done(self: Any, frame_idx: int) -> Any:
        """
        Advance this consumer's cursor to mark a frame as processed (consumer only).
        """
        ...

    def benchmark_write_throughput(self: Any, num_frames: int = 1000, frame_data: Optional[Any] = None) -> Dict:
        """
        Measure write FPS, latency percentiles, and throughput (producer only).
        """
        ...

    def cleanup_stale_buffers(prefix: str = 'shm_rb_') -> List[str]:
        """
        Unlink SHM buffers idle longer than 10s; return the names cleaned.
        """
        ...

    def close(self: Any) -> Any:
        """
        Close mmaps/fds and (for producers) unlink the SHM files; never raises.
        """
        ...

    def connect(self: Any, stale_threshold_sec: float = 30.0) -> bool:
        """
        Connect as consumer — open existing SHM segments.
        """
        ...

    def connect_consumer(cls: Any, camera_id: str, gpu_id: int = 0, consumer_key: str = 'default', max_retries: int = 10, retry_delay: float = 0.5, shm_name: Optional[str] = None) -> 'Any':
        """
        Attach to a producer's ring buffer as a consumer, retrying until it exists.
        """
        ...

    def create_producer(cls: Any, camera_id: str, gpu_id: int = 0, num_slots: int = 8, width: int = 640, height: int = 640, channels: int = 1) -> 'Any':
        """
        Create and initialize a producer ring buffer.
        """
        ...

    def get_all_consumer_cursors(self: Any) -> Dict[int, int]:
        """
        Return {consumer_id: cursor} for all registered consumers.
        """
        ...

    def get_consumer_cursor(self: Any, consumer_id: Optional[int] = None) -> int:
        """
        Return a consumer's cursor (defaults to this instance's consumer).
        """
        ...

    def get_current_frame_idx(self: Any) -> int:
        """
        Return the most recently written frame index.
        """
        ...

    def get_frames_behind(self: Any) -> int:
        """
        Return how many frames this consumer lags behind the producer.
        """
        ...

    def get_header(self: Any) -> dict:
        """
        Return a decoded dict of the buffer's header fields.
        """
        ...

    def get_health_status(self: Any) -> Dict:
        """
        Return a health snapshot (producer liveness, utilization, geometry).
        """
        ...

    def get_last_heartbeat_ns(self: Any) -> int:
        """
        Return the producer's last write/heartbeat timestamp in nanoseconds.
        """
        ...

    def get_producer_age_ms(self: Any) -> float:
        """
        Return milliseconds since the producer's last heartbeat.
        """
        ...

    def get_registered_consumers(self: Any) -> Dict[int, Dict]:
        """
        Return {consumer_id: {key_hash, cursor}} for all registered consumers.
        """
        ...

    def get_session_info(self: Any) -> Tuple[str, int]:
        """
        Return the stored (session_id, session_start_ns) from the header.
        """
        ...

    def get_status(self: Any) -> Dict:
        """
        CudaIpcRingBuffer-compatible status.
        """
        ...

    def get_write_idx(self: Any) -> int:
        """
        Return the producer's current write index.
        """
        ...

    def initialize(self: Any) -> bool:
        """
        Initialize as producer — create SHM segments and write header.
        """
        ...

    def is_frame_torn(self: Any, frame_idx: int) -> bool:
        """
        Check if frame is currently being written (torn risk).
        """
        ...

    def is_frame_valid(self: Any, frame_idx: int, max_wait_ms: float = 5.0) -> bool:
        """
        Check if frame_idx is still readable (not overwritten).
                Retries for cross-process memory visibility.
        """
        ...

    def is_producer_alive(self: Any, timeout_ns: int = 2000000000) -> bool:
        """
        Return True if the producer wrote within the given timeout window.
        """
        ...

    def list_buffers(prefix: str = 'shm_rb_') -> List[Dict]:
        """
        Enumerate existing SHM buffers with size, frame count, and age info.
        """
        ...

    def read_frame(self: Any, frame_idx_or_slot: int) -> Any:
        """
        Read a frame. If numpy view available, returns ndarray from slot.
                Otherwise returns memoryview of frame data by frame_idx.
        """
        ...

    def read_frame_copy(self: Any, frame_idx: int, max_wait_ms: float = 5.0) -> Optional[Any]:
        """
        Read frame with torn frame detection and retry.
        
                Returns a copy of frame data, or None if overwritten/torn/timeout.
        """
        ...

    def read_latest(self: Any) -> Tuple:
        """
        Read most recently written frame. Returns (frame, write_idx).
        """
        ...

    def read_next(self: Any) -> Tuple:
        """
        Read next frame after last read. Returns (frame, frame_idx, was_skipped).
        """
        ...

    def set_session_info(self: Any, session_id: str, session_start_ns: int) -> Any:
        """
        Store the RTSP session id and start timestamp in the header (producer only).
        """
        ...

    def sync_writes(self: Any) -> Any:
        """
        Flush SHM writes.
        """
        ...

    def wait_for_producer(self: Any, timeout_sec: float = 30.0, poll_interval_ms: float = 100.0) -> bool:
        """
        Block until the producer is alive and has written a frame, or timeout.
        """
        ...

    def write_frame(self: Any, raw_data: Union[Any, Any, Any.Any, Any]) -> Tuple[int, int]:
        """
        Write frame/message to next slot with torn frame protection.
        
                Args:
                    raw_data: Frame bytes, numpy array, or CuPy array
        
                Returns:
                    (frame_idx, slot_idx)
        """
        ...

    def write_frame_fast(self: Any, gpu_frame: Any, sync: bool = True, timestamp_ns: Optional[int] = None, rtp_timestamp: int = 0) -> int:
        """
        Write a GPU/numpy frame with torn frame protection.
        
                CudaIpcRingBuffer-compatible API. Returns frame_idx only.
        
                Args:
                    gpu_frame: CuPy ndarray, numpy ndarray, or bytes
                    sync: Ignored (SHM writes are always coherent)
                    timestamp_ns: Frame capture timestamp (default: now)
                    rtp_timestamp: RTP timestamp from RTSP stream
        """
        ...

