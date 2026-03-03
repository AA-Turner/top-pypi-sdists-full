"""Auto-generated stub for module: orin_shm_ring_buffer."""
from typing import Any, Dict, Optional, Set, Tuple

# Constants
CUDA_IPC_HANDLE_SIZE: int
MAP_SHARED: Any
PROT_READ: Any
PROT_WRITE: Any
SHM_BASE_PATH: Any
logger: Any

# Classes
class OrinShmRingBuffer:
    # POSIX SHM Ring Buffer for Jetson Orin (no CUDA IPC).
    #
    #     Drop-in replacement for CudaIpcRingBuffer. Uses mmap'd shared memory for
    #     frame storage instead of GPU memory with CUDA IPC handles.
    #
    #     Header layout matches CudaIpcRingBuffer exactly for cross-compatibility:
    #       0-7:     write_idx (8B)
    #       8-15:    read_idx (8B, legacy)
    #       16-23:   frame_count (8B)
    #       24-31:   timestamp_ns (8B)
    #       32-35:   gpu_id (4B)
    #       36-39:   num_slots (4B)
    #       40-43:   width (4B)
    #       44-47:   height (4B)
    #       48-51:   channels (4B)
    #       52-55:   dtype_code (4B)
    #       56-63:   flags (8B)
    #       64-127:  ipc_handle (64B, zeroed on Orin)
    #       128-135: max_consumers (8B)
    #       136-647: consumer_registry[32] (16B x 32)
    #       648-655: session_id (8B)
    #       656-663: session_start_ns (8B)
    #       664+:    per-slot metadata (32B per slot)

    def __init__(self: Any, camera_id: str, gpu_id: int, num_slots: int, width: int, height: int, channels: int, is_producer: bool) -> None: ...

    CONSUMER_SLOT_SIZE: int
    HEADER_SIZE: Any
    MAX_CONSUMERS: int
    SESSION_INFO_OFFSET: Any
    SESSION_INFO_SIZE: int
    SLOT_META_SIZE: int

    def ack_frame_done(self: Any, frame_idx: int) -> Any:
        """
        Acknowledge frame processing - updates consumer cursor in SHM.
        """
        ...

    def close(self: Any) -> Any:
        """
        Close and cleanup SHM segments.
        """
        ...

    def connect(self: Any, stale_threshold_sec: float = 30.0) -> bool:
        """
        Connect as consumer - open existing SHM segments.
        """
        ...

    def connect_consumer(cls: Any, camera_id: str, gpu_id: int = 0, consumer_key: str = 'default', max_retries: int = 10, retry_delay: float = 0.5) -> 'Any':
        """
        Connect as consumer with retry logic for cross-container startup race.
        
                Args:
                    camera_id: Camera identifier
                    gpu_id: GPU device ID
                    consumer_key: Consumer group identifier string
                    max_retries: Maximum connection attempts
                    retry_delay: Delay between retries in seconds
        
                Returns:
                    Connected OrinShmRingBuffer instance
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
        Get all registered consumer cursors.
        """
        ...

    def get_consumer_cursor(self: Any, consumer_id: Optional[int] = None) -> int:
        """
        Get a consumer's cursor position.
        """
        ...

    def get_frames_behind(self: Any) -> int:
        """
        Get number of frames consumer is behind producer.
        """
        ...

    def get_registered_consumers(self: Any) -> Dict[int, Dict]:
        """
        Get all registered consumer slots with their key hashes.
        """
        ...

    def get_session_info(self: Any) -> Tuple[str, int]:
        """
        Get RTSP session info. Returns (session_id, session_start_ns).
        """
        ...

    def get_status(self: Any) -> Dict:
        """
        Get ring buffer status (CudaIpcRingBuffer-compatible format).
        """
        ...

    def get_write_idx(self: Any) -> int:
        """
        Get current write index.
        """
        ...

    def initialize(self: Any) -> bool:
        """
        Initialize as producer - create SHM segments with CudaIpcRingBuffer-compatible header.
        """
        ...

    def read_frame(self: Any, slot: int) -> Any:
        """
        Read a frame from a specific slot, returns CuPy ndarray on GPU.
        """
        ...

    def read_latest(self: Any) -> Tuple:
        """
        Read the most recently written frame.
        """
        ...

    def read_next(self: Any) -> Tuple:
        """
        Read next frame after last read, with skip detection.
        
                Returns:
                    (frame, frame_idx, was_skipped)
        """
        ...

    def set_session_info(self: Any, session_id: str, session_start_ns: int) -> Any:
        """
        Set RTSP session info for Mode B frame-accurate sync.
        """
        ...

    def sync_writes(self: Any) -> Any:
        """
        Flush SHM writes (lightweight on Orin unified memory).
        """
        ...

    def write_frame(self: Any, gpu_frame: Any) -> int:
        """
        Write a frame to the ring buffer - NEVER BLOCKS.
        """
        ...

    def write_frame_fast(self: Any, gpu_frame: Any, sync: bool = True, timestamp_ns: Optional[int] = None, rtp_timestamp: int = 0) -> int:
        """
        Write a frame to the ring buffer (SHM version).
        
                Args:
                    gpu_frame: CuPy ndarray (GPU) or numpy ndarray (CPU)
                    sync: Ignored on Orin (SHM is always coherent)
                    timestamp_ns: Frame timestamp in nanoseconds
                    rtp_timestamp: RTP timestamp from RTSP stream
        """
        ...

