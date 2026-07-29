"""Stub file for stream directory."""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from .cuda_shm_ring_buffer import CUPY_AVAILABLE, MAP_SHARED, PROT_READ, CudaIpcRingBuffer, _cvd_remap, cp, np
from .cuda_shm_ring_buffer import CudaIpcRingBuffer
from .databus import DataBus, DataBusConsumer, DataFormat, _parse_format
from .databus import DataBus, DataFormat, _parse_format
from .databus_status import STALE_THRESHOLD_NS, NodeStatus
from .device_topology import topology
from .kafka_stream import AsyncKafkaUtils, KafkaUtils
from .redis_stream import AsyncRedisUtils, RedisUtils
from .shm_ring_buffer import ShmRingBuffer

# Constants
DEFAULT_CHECK_INTERVAL: Any = ...  # From app_warning
DEFAULT_STALE_THRESHOLD_SEC: Any = ...  # From app_warning
logger: Any = ...  # From app_warning
logger: Any = ...  # From autoshm
CONSUMER_NOT_CONNECTED_MSG: str = ...  # From cuda_shm_ring_buffer
CUDA_IPC_HANDLE_SIZE: int = ...  # From cuda_shm_ring_buffer
MAP_SHARED: Any = ...  # From cuda_shm_ring_buffer
PROT_READ: Any = ...  # From cuda_shm_ring_buffer
PROT_WRITE: Any = ...  # From cuda_shm_ring_buffer
SHM_BASE_PATH: Any = ...  # From cuda_shm_ring_buffer
logger: Any = ...  # From cuda_shm_ring_buffer
SHM_BASE_PATH: Any = ...  # From databus
logger: Any = ...  # From databus
BatchItem: Any = ...  # From databus_batch_consumer
logger: Any = ...  # From databus_batch_consumer
SHM_BASE_PATH: Any = ...  # From databus_status
STALE_THRESHOLD_NS: int = ...  # From databus_status
STATUS_PREFIX: str = ...  # From databus_status
logger: Any = ...  # From databus_status
logger: Any = ...  # From device_topology
topology: Any = ...  # From device_topology
logger: Any = ...  # From event_listener
MAP_SHARED: Any = ...  # From gpu_camera_map
NOT_INITIALIZED_MSG: str = ...  # From gpu_camera_map
PROT_READ: Any = ...  # From gpu_camera_map
PROT_WRITE: Any = ...  # From gpu_camera_map
SHM_BASE_PATH: Any = ...  # From gpu_camera_map
logger: Any = ...  # From gpu_camera_map
MAP_SHARED: Any = ...  # From gpu_placement_registry
PROT_READ: Any = ...  # From gpu_placement_registry
PROT_WRITE: Any = ...  # From gpu_placement_registry
SHM_BASE_PATH: Any = ...  # From gpu_placement_registry
logger: Any = ...  # From gpu_placement_registry
CONFIG_BOOTSTRAP_SERVERS: str = ...  # From kafka_stream
CONFIG_SASL_MECHANISM: str = ...  # From kafka_stream
CONFIG_SASL_PASSWORD: str = ...  # From kafka_stream
CONFIG_SASL_USERNAME: str = ...  # From kafka_stream
CONFIG_SECURITY_PROTOCOL: str = ...  # From kafka_stream
SCHEDULE_AFTER_SHUTDOWN_MSG: str = ...  # From kafka_stream
logger: Any = ...  # From kafka_stream
logger: Any = ...  # From matrice_stream
DEFAULT_CHECK_INTERVAL: Any = ...  # From offline_cache
DEFAULT_FLUSH_BATCH_SIZE: Any = ...  # From offline_cache
DEFAULT_MAX_SIZE: Any = ...  # From offline_cache
DEFAULT_TTL_SECONDS: Any = ...  # From offline_cache
logger: Any = ...  # From offline_cache
logger: Any = ...  # From redis_stream
CUDA_IPC_HANDLE_SIZE: int = ...  # From shm_ring_buffer
MAP_SHARED: Any = ...  # From shm_ring_buffer
PROT_READ: Any = ...  # From shm_ring_buffer
PROT_WRITE: Any = ...  # From shm_ring_buffer
SHM_BASE_PATH: Any = ...  # From shm_ring_buffer
logger: Any = ...  # From shm_ring_buffer

# Functions
# From _stream_helpers
def accumulate_metric(stats: Dict, metric: Dict) -> None:
    """
    Accumulate a single metric into stream/topic stats.
    
        Args:
            stats: The running statistics dict (modified in place)
            metric: A single metric entry
    """
    ...

# From _stream_helpers
def aggregate_kafka_metrics(raw_metrics: List[Dict], ip: str, port: str) -> Dict:
    """
    Aggregate raw Kafka metrics into the API format expected by backend.
    
        Works for both sync and async Kafka classes.
    
        Args:
            raw_metrics: List of raw metric dictionaries
            ip: Kafka broker IP
            port: Kafka broker port
    
        Returns:
            Aggregated metrics payload dict
    """
    ...

# From _stream_helpers
def aggregate_redis_metrics(raw_metrics: List[Dict], host: str, port: int) -> Dict:
    """
    Aggregate raw Redis metrics into the API format expected by backend.
    
        Works for both sync and async Redis classes.
    
        Args:
            raw_metrics: List of raw metric dictionaries
            host: Redis host
            port: Redis port
    
        Returns:
            Aggregated metrics payload dict
    """
    ...

# From _stream_helpers
def compute_dynamic_batch_size(avg_throughput: float) -> int:
    """
    Return the optimal batch size for the given throughput level.
    
        Adaptive batching strategy:
        - Low throughput (< 1K msg/sec): batch_size = 50 (responsive, low latency)
        - Medium throughput (1K-10K msg/sec): batch_size = 200 (balanced)
        - High throughput (10K-50K msg/sec): batch_size = 500 (efficient batching)
        - Very high throughput (> 50K msg/sec): batch_size = 1000 (maximum efficiency)
    
        Args:
            avg_throughput: Average messages per second
    
        Returns:
            Optimal batch size integer
    """
    ...

# From _stream_helpers
def finalize_stats(all_stats: Dict[str, Dict]) -> None:
    """
    Compute averages and remove temporary fields from all stats dicts.
    
        Args:
            all_stats: Mapping of name -> stats dict (modified in place)
    """
    ...

# From _stream_helpers
def new_stream_stats(name: str, name_key: str, add_op: str, read_op: Union[str, tuple]) -> Dict:
    """
    Create a fresh statistics dict for a stream/topic.
    
        Args:
            name: Stream or topic name
            name_key: Key to store the name under ("stream" or "topic")
            add_op: Operation name for add/publish counting
            read_op: Operation name (or tuple of names) for read/consume counting
    
        Returns:
            Dict with initial zero counters
    """
    ...

# From _stream_helpers
def parse_message_value(value: Any) -> Any:
    """
    Parse message value from bytes.
    
        Args:
            value: Message value in bytes
    
        Returns:
            Parsed value or original bytes if parsing fails
    """
    ...

# From _stream_helpers
def parse_stream_fields(fields: Dict) -> Tuple[Dict, Optional[str], int]:
    """
    Parse raw Redis stream fields into structured data.
    
        Returns:
            Tuple of (parsed_data, message_key, total_size)
    """
    ...

# From _stream_helpers
def safe_decode(value: Union[str, Any], keep_binary: bool = True) -> Any:
    """
    Safely decode bytes to string, handling both str and bytes input.
    
        Args:
            value: Value to decode (str or bytes)
            keep_binary: If True, return bytes as-is if UTF-8 decoding fails
    
        Returns:
            Decoded string or original bytes if decoding fails and keep_binary=True
    """
    ...

# From _stream_helpers
def serialize_key(key: Any) -> Optional[Any]:
    """
    Serialize message key to bytes.
    
        Args:
            key: Message key to serialize
    
        Returns:
            Serialized key as bytes or None
    """
    ...

# From _stream_helpers
def serialize_value(value: Any) -> Any:
    """
    Serialize message value to bytes.
    
        Args:
            value: Message value to serialize
    
        Returns:
            Serialized value as bytes
    """
    ...

# From autoshm
def consumer_auto(camera_id: str, node_id: str = 'sg', port_name: str = 'frames', fmt: Any = 'cupy', consumer_key: str = 'inference', local_gpu_id: Optional[int] = None, max_retries: int = 10, retry_delay: float = 0.5) -> Any:
    """
    Connect a consumer that reads ``camera_id`` on ``local_gpu_id`` no matter
        which GPU the producer decoded on. Resolves the producer GPU from the header,
        enables peer access, and peer-copies frames into local memory.
    
        local_gpu_id=None means "the current cupy device" (the worker's inference GPU).
    """
    ...

# From autoshm
def resolve_decode_gpu(camera_id: str, node_id: str = 'sg', port_name: str = 'frames', max_retries: int = 10, retry_delay: float = 0.5) -> int:
    """
    Return the GPU the producer decoded this camera on, read from the ring-
        buffer header. CO-LOCATION (the supported cross-GPU strategy): the caller
        runs this camera's inference on the returned GPU so consume is zero-copy and
        no NVLink/P2P is needed. Retries while the producer is still initializing.
    """
    ...

# From cuda_shm_ring_buffer
def benchmark_cuda_ipc() -> None:
    """
    Benchmark CUDA IPC ring buffer performance.
    """
    ...

# From gpu_camera_map
def get_gpu_camera_map(is_producer: bool = False) -> Any:
    """
    Get or create the global GpuCameraMap instance.
    
        Args:
            is_producer: True if this is the producer process
    
        Returns:
            GpuCameraMap instance (may not be initialized)
    """
    ...

# From shm_ring_buffer
def bgr_to_nv12(bgr_frame: 'Any.Any') -> Any:
    """
    Convert BGR frame to NV12 format.
    """
    ...

# From shm_ring_buffer
def nv12_to_bgr(nv12_bytes: Any, width: int, height: int) -> 'Any.Any':
    """
    Convert NV12 bytes to BGR frame.
    """
    ...

# From shm_ring_buffer
def rgb_to_nv12(rgb_frame: 'Any.Any') -> Any:
    """
    Convert RGB frame to NV12 format.
    """
    ...

# Classes
# From _stream_helpers
class MetricsReporterMixin:
    # Mixin providing common metrics infrastructure for stream classes.
    #
    #     Subclasses must define:
    #         _metrics_lock: threading.Lock
    #         _metrics_log: Deque[Dict[str, Any]]
    #         _metrics_reporting_config: Optional[Dict[str, Any]]
    #         _metrics_thread: Optional[threading.Thread]
    #         _metrics_stop_event: threading.Event
    #
    #     And must implement:
    #         _build_metric_entry(...) -> Dict  — build the metric dict with class-specific fields
    #         _aggregate_metrics_for_api(raw_metrics) -> Dict
    #         _get_api_path() -> str  — the POST endpoint for metrics
    #         _get_reporter_label() -> str  — label for log messages (e.g. "Redis" or "Kafka")

    def get_metrics(self: Any, clear_after_read: bool = False) -> List[Dict]:
        """
        Get collected metrics for aggregation and reporting.
        
                Args:
                    clear_after_read: Whether to clear metrics after reading
        
                Returns:
                    List of metric dictionaries
        """
        ...

    def stop_metrics_reporting(self: Any) -> None:
        """
        Stop the background metrics reporting thread.
        """
        ...


# From app_warning
class AppWarningManager:
    # Monitors DataBus pipeline nodes and emits warnings on state changes.
    #
    #     Uses NodeStatus SHM heartbeat files for zero-overhead health checking.
    #     Warning callbacks are invoked on the monitor thread — keep handlers fast.
    #
    #     Args:
    #         check_interval: Seconds between health check sweeps.
    #         stale_threshold_sec: Seconds without heartbeat before a node is stale.

    def __init__(self: Any, check_interval: float = DEFAULT_CHECK_INTERVAL, stale_threshold_sec: float = DEFAULT_STALE_THRESHOLD_SEC) -> None: ...

    def get_node_states(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get current state of all monitored nodes.
        """
        ...

    def get_warnings(self: Any, clear: bool = True) -> List[Dict[str, Any]]:
        """
        Get accumulated warnings, optionally clearing the buffer.
        """
        ...

    def is_node_online(self: Any, node_id: str) -> bool:
        """
        Check if a specific node is online.
        """
        ...

    def on_warning(self: Any, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a callback for warning events.
        
                Callback receives a dict with keys: timestamp, node_id, type, message, details.
                Warning types: DEVICE_OFFLINE, DEVICE_ONLINE, DEVICE_STALE, NODE_DISCOVERED.
        """
        ...

    def start(self: Any) -> None:
        """
        Start the background monitoring thread.
        """
        ...

    def stop(self: Any) -> None:
        """
        Stop the monitoring thread.
        """
        ...


# From app_warning
class NodeState:
    # Internal tracking state for a monitored node.

    ...

# From autoshm
class AutoConsumer:
    # Drop-in for the connector's use of a DataBus consumer: exposes ``.rb``
    #     (a PeerReadRingBuffer or HostBounceRingBuffer) and ``.close()``.

    def __init__(self: Any, rb: Any) -> None: ...

    def close(self: Any) -> None: ...

    def is_stale(self: Any) -> bool: ...

    def rb(self: Any) -> Any: ...


# From autoshm
class HostBounceRingBuffer:
    # LAST-RESORT cross-GPU consumer for hosts WITHOUT NVLink/P2P.
    #
    #     Why this exists / when it runs
    #     ------------------------------
    #     A CUDA-IPC handle can only be opened on the producer's OWN device, so a
    #     consumer on GPU Y cannot map a producer's GPU-X memory without P2P. This
    #     class connects on the PRODUCER GPU (same-device IPC -> always legal) and
    #     bounces every frame DtoH -> pinned host -> HtoD to the local inference GPU.
    #
    #     This is a PCIe round trip per frame (~250 us @1080p NV12 with pinned host
    #     memory) and consumes PCIe bandwidth + a pinned host buffer per camera. It is
    #     a SAFETY NET ONLY: the supported path is CO-LOCATION (consume each camera on
    #     its decode GPU via resolve_decode_gpu()). It is OFF by default and only used
    #     when MATRICE_XGPU_FALLBACK=host_stage. It emits a throttled WARNING every
    #     MATRICE_XGPU_WARN_EVERY_SEC so the degradation is never silent.
    #
    #     Precondition: the consumer process must see BOTH GPUs (do NOT pin
    #     CUDA_VISIBLE_DEVICES to a single device, or the producer GPU can't be mapped).

    def __init__(self: Any, camera_id: str, local_gpu_id: int, num_slots: int, width: int, height: int, channels: int) -> None: ...

    def read_frame(self: Any, slot: Any) -> Any: ...

    def read_latest(self: Any) -> Any: ...

    def read_next(self: Any) -> Any: ...


# From autoshm
class PeerReadRingBuffer:
    # A consumer ring buffer that may attach to a producer on a DIFFERENT GPU.
    #
    #     Reads return frames copied to the local device (one peer copy over NVLink)
    #     when the producer is on another GPU, and identical zero-copy views when the
    #     producer is on the same GPU.

    def __init__(self: Any, camera_id: str, gpu_id: int, num_slots: int, width: int, height: int, channels: int, is_producer: bool = False) -> None: ...

    def read_frame(self: Any, slot: int) -> Any: ...

    def read_latest(self: Any) -> Any: ...

    def read_next(self: Any) -> Any: ...


# From autoshm
class PeerUnavailableError(Exception):
    # Cross-GPU consume requested but no P2P/NVLink path exists (terminal — the
    #     caller must run inference on the producer's GPU on this host).

    ...

# From cuda_shm_ring_buffer
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


# From cuda_shm_ring_buffer
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


# From databus
class DataBus:
    # Unified data transport — all methods are static, no state held.

    def compute_address(camera_id: str, node_id: str, port_name: str) -> str:
        """
        Compute deterministic SHM path. Pure function, no I/O.
        """
        ...

    def consumer(camera_id: str, node_id: str, port_name: str, format: Union[str, Any], consumer_key: str = 'default') -> 'Any':
        """
        Create a consumer at the deterministic address.
        
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
        ...

    def producer(camera_id: str, node_id: str, port_name: str, format: Union[str, Any]) -> 'Any':
        """
        Create a producer at the deterministic address.
        
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
        ...


# From databus
class DataBusConsumer:
    # Consumes data from a DataBus channel.
    #
    #     Wraps CudaIpcRingBuffer (for cupy/torch) or ShmRingBuffer (for json/bytes/numpy).

    def __init__(self: Any, address: str, fmt: Any, transport: str, consumer_key: str = 'default', gpu_id: int = 0) -> None: ...

    def ack(self: Any, frame_idx: int) -> Any:
        """
        Acknowledge consumption up to frame_idx.
        
                For CUDA IPC: updates per-consumer cursor in SHM.
                For POSIX SHM: updates local tracking only.
        """
        ...

    def address(self: Any) -> str: ...

    def close(self: Any) -> Any:
        """
        Close and cleanup.
        """
        ...

    def connected(self: Any) -> bool: ...

    def consume(self: Any) -> Tuple[Optional[Any], Optional[Dict]]:
        """
        Read next unread message.
        
                Returns:
                    (data, metadata) or (None, None) if no new data.
                    For cupy: data is a GPU array view (must stay alive during use)
                    For json: data is a dict/list
                    For bytes: data is bytes
                    For numpy: data is np.ndarray (1D uint8, caller reshapes)
        """
        ...

    def consume_latest(self: Any) -> Tuple[Optional[Any], Optional[Dict]]:
        """
        Read the latest available message, skipping all intermediate frames.
        
                Use this instead of consume() when the consumer is slower than the
                producer and you want overlays to stay in sync with the live video
                (e.g., ML inference at 10 FPS reading from a 30 FPS stream).
        
                Returns:
                    (data, metadata) or (None, None) if no new data.
                    metadata includes 'was_skipped' (bool) indicating if frames were dropped.
        """
        ...

    def is_stale(self: Any) -> bool:
        """
        Check if the underlying ring buffer's SHM file has been recreated.
        
                This indicates the producer restarted and our connection points to
                stale data. Caller should close this consumer and create a new one.
        
                Returns:
                    True if stale (producer restarted), False if still valid.
        """
        ...

    def rb(self: Any) -> Optional['Any']:
        """
        Access the underlying ring buffer for advanced operations.
        """
        ...


# From databus
class DataBusProducer:
    # Produces data to a DataBus channel.
    #
    #     Wraps CudaIpcRingBuffer (for cupy/torch) or ShmRingBuffer (for json/bytes/numpy).

    def __init__(self: Any, address: str, fmt: Any, transport: str, camera_id: str = '', **config: Any) -> None: ...

    def close(self: Any) -> Any:
        """
        Close and cleanup underlying ring buffer.
        """
        ...

    def publish(self: Any, data: Any, metadata: Optional[Dict] = None) -> int:
        """
        Publish data with optional metadata. Returns frame_idx.
        
                For cupy/torch: data is a GPU array, metadata keys used:
                    timestamp_ns, rtp_timestamp
                For json: data is a dict/list, serialized with orjson
                For bytes: data is bytes
                For numpy: data is a numpy array, serialized with tobytes()
        """
        ...

    def rb(self: Any) -> Optional['Any']:
        """
        Access the underlying ring buffer for advanced operations.
        """
        ...


# From databus
class DataFormat:
    # Data format declaration — determines transport auto-selection.

    BYTES: str
    CUPY: str
    JSON: str
    NUMPY: str
    TORCH: str


# From databus_batch_consumer
class BatchConsumer:
    # Multi-channel batched consumer with dynamic batching and timeout.
    #
    #     Collects from multiple DataBus channels using round-robin with adaptive
    #     polling. Returns partial batches on timeout (never blocks forever).

    def __init__(self: Any, addresses: List[str], consumer_key: str, format: Union[str, Any]) -> None: ...

    def ack_batch(self: Any, items: List[Any]) -> None:
        """
        Acknowledge all items in a batch.
        
                Args:
                    items: List of (data, metadata, address) tuples from collect_batch()
        """
        ...

    def add_channel(self: Any, address: str) -> bool:
        """
        Dynamically add a channel.
        
                Args:
                    address: Full DataBus address (e.g., /dev/shm/databus__cam__node__port)
        
                Returns:
                    True if connection succeeded
        """
        ...

    def addresses(self: Any) -> List[str]:
        """
        List of all registered addresses (connected or not).
        """
        ...

    def channel_count(self: Any) -> int:
        """
        Number of connected channels.
        """
        ...

    def close(self: Any) -> None:
        """
        Close all consumer connections and cleanup.
        """
        ...

    def collect_batch(self: Any, max_batch: int = 64, timeout_ms: float = 10.0) -> List[Any]:
        """
        Collect up to max_batch items across all channels.
        
                Implements dynamic batching:
                - Collects items until max_batch reached OR timeout expires
                - Returns early if full batch collected
                - Returns whatever items are available on timeout (even 1 item)
                - Round-robin across channels for fair scheduling
        
                Args:
                    max_batch: Maximum items to collect
                    timeout_ms: Maximum wait time in milliseconds (0 = no timeout)
        
                Returns:
                    List of (data, metadata, address) tuples
        """
        ...

    def connect(self: Any) -> bool:
        """
        Connect to all channels.
        
                Returns:
                    True if at least one channel connected successfully.
        """
        ...

    def connected(self: Any) -> bool:
        """
        True if at least one channel is connected.
        """
        ...

    def get_lag(self: Any) -> Dict[str, int]:
        """
        Get per-channel consumer lag (frames behind).
        
                Only works for CUDA IPC consumers that expose get_frames_behind().
                Returns 0 for POSIX SHM consumers (no native lag tracking).
        """
        ...

    def remove_channel(self: Any, address: str) -> None:
        """
        Dynamically remove a channel.
        
                Args:
                    address: Full DataBus address to remove
        """
        ...


# From databus_status
class NodeStatus:
    # Per-node SHM status file.
    #
    #     Each node owns exactly one file — no write contention.

    def __init__(self: Any, node_id: str) -> None: ...

    def heartbeat(self: Any) -> None:
        """
        Fast-path: update only last_heartbeat_ns in existing status.
        """
        ...

    def is_stale(status_dict: Dict, threshold_ns: int = STALE_THRESHOLD_NS) -> bool:
        """
        Check if a node's status is stale (no heartbeat within threshold).
        
                Args:
                    status_dict: Status dict from read() or read_all()
                    threshold_ns: Stale threshold in nanoseconds (default 30s)
        
                Returns:
                    True if last heartbeat is older than threshold.
        """
        ...

    def read(node_id: str) -> Optional[Dict]:
        """
        Read one node's status by ID.
        
                Returns:
                    Status dict or None if not found/corrupt.
        """
        ...

    def read_all() -> List[Dict]:
        """
        Read all node status files.
        
                Returns:
                    List of status dicts for all active nodes.
        """
        ...

    def remove(self: Any) -> None:
        """
        Delete status file on graceful shutdown.
        """
        ...

    def write(self: Any, status: str = 'alive', model_loaded: bool = False, buffer_addresses: Optional[List[str]] = None, **extra: Any) -> None:
        """
        Write full status. Creates file if needed.
        """
        ...


# From device_topology
class MachineTopology:
    # Process-wide cache of GPU count, peer-access capability, and which
    #     (consumer, producer) peer links have already been enabled. Thread-safe and
    #     idempotent — safe to call enable_peer() on every connect.

    def __init__(self: Any) -> None: ...

    def can_access_peer(self: Any, local_gpu: int, producer_gpu: int) -> bool:
        """
        True if local_gpu can directly read producer_gpu's memory (NVLink/
                PCIe P2P). Same device is trivially True. Result is cached.
        """
        ...

    def device_count(self: Any) -> int: ...

    def enable_peer(self: Any, local_gpu: int, producer_gpu: int) -> bool:
        """
        Idempotently enable local_gpu -> producer_gpu peer access.
        
                Returns True when frames on producer_gpu are reachable from local_gpu
                (same GPU, or NVLink/PCIe P2P successfully enabled).
        
                Returns False when local_gpu != producer_gpu and no peer path exists
                (a multi-GPU host without NVLink/P2P). This is **terminal** for
                cross-GPU consume — there is no transparent host-bounce fallback (the
                CUDA-IPC handle itself can't be opened for another device's memory
                without P2P). consumer_auto turns False into a PeerUnavailableError;
                the operator's remedy is to co-locate inference on the producer's GPU.
                Single-GPU hosts (Orin/Thor) never reach this (producer_gpu == local).
        """
        ...

    def has_full_p2p(self: Any, device_ids: Any = None) -> bool:
        """
        True if every ordered pair among device_ids can peer-access (full P2P/
                NVLink mesh). Used by the SG to decide whether cross-GPU consume is viable
                and by consumer_auto to pick a transport. Same-device pairs are trivially
                OK; a single GPU is trivially a full mesh.
        """
        ...


# From event_listener
class EventListener:
    # Generic listener for Kafka events with filtering and custom handlers.
    #
    #     This class provides a flexible event listening infrastructure that can be used
    #     for various event types (camera events, app events, etc.) from Kafka topics.
    #
    #     Example:
    #         ```python
    #         import logging
    #         logger = logging.getLogger(__name__)
    #
    #         def my_handler(event):
    #             logger.info("Received event: %s", event.get("eventType"))
    #
    #         listener = EventListener(
    #             session=session,
    #             topics=['Camera_Events_Topic', 'App_Events_Topic'],
    #             event_handler=my_handler,
    #             filter_field='streamingGatewayId',
    #             filter_value='gateway123'
    #         )
    #         listener.start()
    #         ```

    def __init__(self: Any, session: Any, topics: Union[str, List[str]], event_handler: Callable[[Dict[str, Any]], None], filter_field: Optional[str] = None, filter_value: Optional[str] = None, consumer_group_id: Optional[str] = None, offset_reset: str = 'latest', max_poll_interval_ms: int = 300000, session_timeout_ms: int = 45000, heartbeat_interval_ms: int = 15000) -> None:
        """
        Initialize event listener.
        
                Args:
                    session: Session object for authentication and API access
                    topics: List of Kafka topics to subscribe to
                    event_handler: Callback function to handle events
                    filter_field: Optional field name to filter events (e.g., 'streamingGatewayId')
                    filter_value: Optional value to match for filtering
                    consumer_group_id: Optional Kafka consumer group ID (auto-generated if not provided)
                    max_poll_interval_ms: Max delay between poll() calls before the broker
                        evicts the consumer (default: 300000). Also drives the time-based
                        staleness recreate in the listen loop.
                    session_timeout_ms: Consumer session timeout (default: 45000).
                    heartbeat_interval_ms: Consumer heartbeat interval (default: 15000).
        """
        ...

    def get_statistics(self: Any) -> dict:
        """
        Get listener statistics.
        
                Returns:
                    dict: Statistics including events received, processed, filtered, and failed
        """
        ...

    def start(self: Any) -> bool:
        """
        Start listening to events.
        
                Returns:
                    bool: True if started successfully
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop listening.
        """
        ...


# From gpu_camera_map
class GpuCameraMap:
    # Shared memory store for camera_id -> gpu_id mapping.
    #
    #     Uses a simple JSON format stored in shared memory with a size header.
    #     Thread-safe via file locking for writes.
    #
    #     Format in shared memory:
    #     - 4 bytes: uint32 size of JSON data
    #     - N bytes: JSON string {"camera_id": gpu_id, ...}

    def __init__(self: Any, is_producer: bool = True) -> None:
        """
        Initialize the GPU camera map.
        
                Args:
                    is_producer: True if this process creates/writes the mapping,
                                False if this process only reads.
        """
        ...

    MAX_SIZE: Any
    SHM_PATH: Any

    def check_file_recreated(self: Any) -> bool:
        """
        Return True if the SHM file's on-disk inode no longer matches our open fd.
        
                When the SHM file is unlinked + recreated (SG restart with external cleanup,
                operator `rm -f /dev/shm/gpu_camera_map`, or `docker rm` on the SG container),
                the open fd keeps pointing at the deleted inode while a new inode appears at
                the same path. Comparing os.fstat(fd).st_ino vs os.stat(path).st_ino detects
                this. Mirrors CudaShmRingBuffer.check_file_recreated().
        
                Returns:
                    True if file was recreated (stale) or missing, False if still the same file.
        """
        ...

    def close(self: Any) -> None:
        """
        Close the shared memory mapping.
        
                Producer should call this during cleanup.
        """
        ...

    def connect(self: Any) -> bool:
        """
        Connect to existing shared memory.
        
                For producers: opens with read-write access to allow writing mappings.
                For consumers: opens with read-only access.
        
                Returns:
                    True if successful, False otherwise.
        """
        ...

    def get_all_mappings(self: Any) -> Dict[str, int]:
        """
        Get all camera-to-GPU mappings.
        
                Returns:
                    Dict of camera_id -> gpu_id
        """
        ...

    def get_cameras_for_gpu(self: Any, gpu_id: int) -> List[str]:
        """
        Get all camera IDs assigned to a specific GPU.
        
                Args:
                    gpu_id: GPU ID to filter by
        
                Returns:
                    List of camera IDs assigned to this GPU
        """
        ...

    def get_gpu_id(self: Any, camera_id: str) -> Optional[int]:
        """
        Get GPU ID for a camera (consumer).
        
                Args:
                    camera_id: Camera identifier
        
                Returns:
                    GPU ID if found, None otherwise.
        """
        ...

    def initialize(self: Any) -> bool:
        """
        Initialize as producer - create shared memory.
        
                Creates the shared memory file and initializes with empty mapping.
                Should be called by the streaming gateway before creating ring buffers.
        
                Returns:
                    True if successful, False otherwise.
        """
        ...

    def reconnect(self: Any) -> bool:
        """
        Close the stale mmap+fd and re-open the current SHM file by path.
        
                Idempotent: safe to call even when not connected. Returns True on success,
                False when the file is missing (caller should retry later).
        """
        ...

    def remove_mapping(self: Any, camera_id: str) -> None:
        """
        Remove a single camera from the map (producer only).
        
                Thread-safe via file locking.
        
                Args:
                    camera_id: Camera identifier to remove
        """
        ...

    def replace_all_mappings(self: Any, mappings: Dict[str, int]) -> None:
        """
        Replace the entire map with the given mappings (producer only).
        
                Unlike set_bulk_mapping() which merges, this does a full atomic replace.
                Removed cameras will no longer appear in the map.
        
                Args:
                    mappings: Complete dict of camera_id -> gpu_id
        """
        ...

    def set_bulk_mapping(self: Any, mappings: Dict[str, int]) -> None:
        """
        Set multiple GPU assignments at once (producer only).
        
                More efficient than multiple set_mapping() calls.
                Uses exclusive lock around the entire read-modify-write cycle
                to prevent race conditions when multiple processes write concurrently.
        
                Args:
                    mappings: Dict of camera_id -> gpu_id
        """
        ...

    def set_mapping(self: Any, camera_id: str, gpu_id: int) -> None:
        """
        Set GPU assignment for a camera (producer only).
        
                Thread-safe via file locking.
        
                Args:
                    camera_id: Camera identifier
                    gpu_id: GPU ID to assign this camera to
        """
        ...


# From gpu_placement_registry
class GpuPlacementRegistry:
    # SHM-backed registry of per-GPU cameras + apps + load.
    #
    #     Distinct from ``GpuCameraMap`` — that one persists the per-camera
    #     mapping. This one persists what's currently *resident* on each GPU.
    #
    #     Same atomicity discipline as ``GpuCameraMap``: every read-modify-write
    #     is wrapped in an exclusive ``fcntl.flock`` on the fd.

    def __init__(self: Any) -> None: ...

    MAX_SIZE: Any
    SHM_PATH: Any

    def close(self: Any) -> None: ...

    def connect(self: Any) -> bool:
        """
        Open an existing SHM file read/write. Returns False if missing.
        """
        ...

    def initialize(self: Any, num_gpus: int) -> bool:
        """
        Open or create the SHM file, ensuring an entry exists for each GPU.
        
                Idempotent: existing file is preserved (cameras/apps survive
                producer restarts); only missing GPU ids get populated with empty
                state. Safe to call on every SG startup.
        """
        ...

    def remove_app_from_all(self: Any, deployment_id: str) -> None:
        """
        Remove a deployment_id from every GPU's ``apps[]``.
        
                Used by IE startup to clean stale entries from a prior crash before
                re-registering, and by the SG stale-sweep loop to evict dead IEs.
        """
        ...

    def replace_cameras_for_gpus(self: Any, by_gpu: Dict[int, List[str]], load_by_gpu: Optional[Dict[int, float]] = None) -> None:
        """
        Replace the ``cameras[]`` list (and optionally ``load``) for the
                given GPUs, leaving other GPUs and the ``apps[]`` lists untouched.
        
                Used by the SG on startup to seed the registry from the authoritative
                ``GpuCameraMap`` (single source of truth for camera->GPU placement).
        """
        ...

    def snapshot(self: Any) -> Dict[int, Any]:
        """
        Read the whole registry under a shared lock.
        """
        ...

    def update_apps(self: Any, gpu_id: int, add: Optional[Any[str]] = None, remove: Optional[Any[str]] = None) -> None:
        """
        Atomically add/remove app (deployment) entries on one GPU.
        """
        ...

    def update_cameras(self: Any, gpu_id: int, add: Optional[Any[str]] = None, remove: Optional[Any[str]] = None, load_delta: float = 0.0) -> None:
        """
        Atomically add/remove cameras and apply a load delta on one GPU.
        """
        ...


# From gpu_placement_registry
class GpuState:
    # Per-GPU state snapshot.

    def empty(cls: Any) -> 'Any': ...

    def from_dict(cls: Any, d: dict) -> 'Any': ...

    def to_dict(self: Any) -> dict: ...


# From kafka_stream
class AsyncKafkaUtils:
    # Utility class for asynchronous Kafka operations.

    def __init__(self: Any, bootstrap_servers: str, sasl_mechanism: Optional[str] = 'SCRAM-SHA-256', sasl_username: Optional[str] = None, sasl_password: Optional[str] = None, security_protocol: str = 'SASL_PLAINTEXT') -> None:
        """
        Initialize async Kafka utils with bootstrap servers and SASL configuration.
        
                Args:
                    bootstrap_servers: Comma-separated list of Kafka broker addresses
                    sasl_mechanism: SASL mechanism for authentication
                    sasl_username: Username for SASL authentication
                    sasl_password: Password for SASL authentication
                    security_protocol: Security protocol for Kafka connection
        """
        ...

    async def close(self: Any) -> None:
        """
        Close async Kafka producer and consumer connections.
        """
        ...

    def configure_metrics_reporting(self: Any, rpc_client: Any, service_id: Optional[str] = None, interval: int = 120, batch_size: int = 1000) -> None:
        """
        Configure background metrics reporting to backend API.
        
                Args:
                    rpc_client: RPC client instance for API communication
                    service_id: Deployment identifier for metrics context
                    interval: Reporting interval in seconds (default: 120)
                    batch_size: Maximum metrics per batch (default: 1000)
        """
        ...

    async def consume_message(self: Any, timeout: float = 60.0) -> Optional[Dict]:
        """
        Consume a single message from Kafka.
        
                Args:
                    timeout: Maximum time to wait for message in seconds
        
                Returns:
                    Message dictionary if available, None if no message received
        
                Raises:
                    RuntimeError: If consumer is not initialized
                    AsyncKafkaError: If message consumption fails
        """
        ...

    async def produce_message(self: Any, topic: str, value: Union[dict, str, Any, Any], key: Optional[Union[str, Any, Any]] = None, headers: Optional[List[Tuple[str, Any]]] = None, timeout: float = 30.0) -> None:
        """
        Produce a message to a Kafka topic.
        
                Args:
                    topic: Topic to produce to
                    value: Message value (dict will be converted to JSON)
                    key: Optional message key
                    headers: Optional message headers
                    timeout: Maximum time to wait for message delivery in seconds
        
                Raises:
                    RuntimeError: If producer is not initialized
                    ValueError: If topic or value is invalid
                    AsyncKafkaError: If message production fails
        """
        ...

    async def setup_consumer(self: Any, topics: List[str], group_id: str, group_instance_id: Optional[str] = None, config: Optional[Dict] = None) -> None:
        """
        Set up async Kafka consumer.
        
                Args:
                    topics: List of topics to subscribe to
                    group_id: Consumer group ID
                    group_instance_id: Consumer group instance ID for static membership
                    config: Additional consumer configuration
        
                Raises:
                    ValueError: If topics list is empty
                    AsyncKafkaError: If consumer initialization fails
        """
        ...

    async def setup_producer(self: Any, config: Optional[Dict] = None) -> None:
        """
        Set up async Kafka producer.
        
                Args:
                    config: Additional producer configuration
        
                Raises:
                    AsyncKafkaError: If producer initialization fails
        """
        ...


# From kafka_stream
class AsyncRebalanceListener:
    # Top-level listener for async partition rebalance events.

    def __init__(self: Any, consumer: Any, parent: Any) -> None: ...

    async def on_partitions_assigned(self: Any, partitions: Any) -> Any: ...

    async def on_partitions_revoked(self: Any, revoked: Any) -> Any: ...


# From kafka_stream
class KafkaUtils:
    # Utility class for synchronous Kafka operations.

    def __init__(self: Any, bootstrap_servers: str, sasl_mechanism: Optional[str] = 'SCRAM-SHA-256', sasl_username: Optional[str] = None, sasl_password: Optional[str] = None, security_protocol: str = 'SASL_PLAINTEXT') -> None:
        """
        Initialize Kafka utils with bootstrap servers and SASL configuration.
        
                Args:
                    bootstrap_servers: Comma-separated list of Kafka broker addresses
                    sasl_mechanism: SASL mechanism for authentication
                    sasl_username: Username for SASL authentication
                    sasl_password: Password for SASL authentication
                    security_protocol: Security protocol for Kafka connection
        """
        ...

    def close(self: Any) -> None:
        """
        Close Kafka producer and consumer connections.
        """
        ...

    def configure_metrics_reporting(self: Any, rpc_client: Any, service_id: Optional[str] = None, interval: int = 120, batch_size: int = 1000) -> None:
        """
        Configure background metrics reporting to backend API.
        
                Args:
                    rpc_client: RPC client instance for API communication
                    service_id: Deployment identifier for metrics context
                    interval: Reporting interval in seconds (default: 120)
                    batch_size: Maximum metrics per batch (default: 1000)
        """
        ...

    def consume_message(self: Any, timeout: float = 1.0) -> Optional[Dict]:
        """
        Consume single message from subscribed topics.
        
                Args:
                    timeout: Maximum time to block waiting for message in seconds
        
                Returns:
                    Message dict if available, None if timeout. Dict contains:
                        - topic: Topic name
                        - partition: Partition number
                        - offset: Message offset
                        - key: Message key (if present)
                        - value: Message value
                        - headers: Message headers (if present)
                        - timestamp: Message timestamp
        
                Raises:
                    RuntimeError: If consumer is not set up
                    KafkaError: If message consumption fails
        """
        ...

    def create_topic_dynamic(self: Any, topic: str, partitions: int, replication: int, kafka_ip: Optional[str] = None, kafka_port: Optional[str] = None) -> bool:
        """
        Create a Kafka topic dynamically - equivalent to Go CreateTopic().
        
                Args:
                    topic: Topic name to create
                    partitions: Number of partitions
                    replication: Replication factor
                    kafka_ip: Kafka server IP (optional, uses existing bootstrap_servers if None)
                    kafka_port: Kafka server port (optional, uses existing bootstrap_servers if None)
        
                Returns:
                    bool: True if topic was created successfully, False otherwise
        """
        ...

    def get_consumer(self: Any, topic: Optional[str] = None, group_id: Optional[str] = None, ip: Optional[str] = None, port: Optional[str] = None) -> Optional[Any]:
        """
        Get existing consumer instance or create new one - equivalent to Go GetConsumer().
        
                Args:
                    topic: Topic to subscribe to (optional if consumer already set up)
                    group_id: Consumer group ID (optional if consumer already set up)
                    ip: Kafka server IP (ignored if consumer already set up)
                    port: Kafka server port (ignored if consumer already set up)
        
                Returns:
                    Consumer instance (existing self.consumer) or newly created consumer
        """
        ...

    def produce_message(self: Any, topic: str, value: Union[dict, str, Any, Any], key: Optional[Union[str, Any, Any]] = None, headers: Optional[List[Tuple]] = None, timeout: float = 30.0, wait_for_delivery: bool = False) -> None:
        """
        Produce message to Kafka topic.
        
                Args:
                    topic: Topic to produce to
                    value: Message value (dict will be converted to JSON)
                    key: Optional message key
                    headers: Optional list of (key, value) tuples for message headers
                    timeout: Maximum time to wait for message delivery in seconds
                    wait_for_delivery: Whether to wait for delivery confirmation
        
                Raises:
                    RuntimeError: If producer is not set up
                    KafkaError: If message production fails
                    ValueError: If topic is empty or value is None
        """
        ...

    def publish_message_with_timestamp(self: Any, topic: str, key: Any, value: Any, ip: Optional[str] = None, port: Optional[str] = None) -> bool:
        """
        Publish message using Kafka message timestamp (no headers) - equivalent to Go Publish().
        
                Args:
                    topic: Topic to publish to
                    key: Message key as bytes
                    value: Message value as bytes
                    ip: Kafka server IP (ignored if producer already set up)
                    port: Kafka server port (ignored if producer already set up)
        
                Returns:
                    bool: True if message was published successfully, False otherwise
        """
        ...

    def read_consumer_with_latency(self: Any, consumer: Optional[Any] = None, ip: Optional[str] = None, port: Optional[str] = None) -> Tuple[Optional[Dict], Optional[float], Optional[str]]:
        """
        Read message from consumer with latency calculation - equivalent to Go ReadConsumer().
        
                Args:
                    consumer: Consumer instance to read from (uses self.consumer if None)
                    ip: Kafka server IP (ignored, for Go compatibility)
                    port: Kafka server port (ignored, for Go compatibility)
        
                Returns:
                    Tuple of (message_dict, latency_seconds, error_string)
        """
        ...

    def setup_consumer(self: Any, topics: List[str], group_id: str, group_instance_id: Optional[str] = None, config: Optional[Dict] = None) -> None:
        """
        Set up Kafka consumer for given topics.
        
                Args:
                    topics: List of topics to subscribe to
                    group_id: Consumer group ID
                    group_instance_id: Consumer group instance ID for static membership
                    config: Additional consumer configuration
        
                Raises:
                    KafkaError: If consumer initialization or subscription fails
                    ValueError: If topics list is empty
        """
        ...

    def setup_producer(self: Any, config: Optional[Dict] = None) -> None:
        """
        Set up Kafka producer with optional config.
        
                Args:
                    config: Additional producer configuration
        
                Raises:
                    KafkaError: If producer initialization fails
        """
        ...


# From kafka_stream
class MatriceKafkaDeployment:
    # Class for managing Kafka deployments for Matrice streaming API.

    def __init__(self: Any, session: Any, service_id: str, type: str, consumer_group_id: Optional[str] = None, consumer_group_instance_id: Optional[str] = None, sasl_mechanism: Optional[str] = 'SCRAM-SHA-256', sasl_username: Optional[str] = None, sasl_password: Optional[str] = None, security_protocol: str = 'SASL_PLAINTEXT', custom_request_service_id: Optional[str] = None, custom_result_service_id: Optional[str] = None, enable_metrics: bool = True, metrics_interval: int = 120) -> None:
        """
        Initialize Kafka deployment with deployment ID.
        
                Args:
                    session: Session object for authentication and RPC
                    service_id: ID of the deployment/service (used as deployment_id for metrics)
                    type: Type of deployment ("client" or "server")
                    consumer_group_id: Kafka consumer group ID
                    consumer_group_instance_id: Kafka consumer group instance ID for static membership
                    sasl_mechanism: SASL mechanism for authentication
                    sasl_username: Username for SASL authentication
                    sasl_password: Password for SASL authentication
                    security_protocol: Security protocol for Kafka connection
                    custom_request_service_id: Custom request service ID
                    custom_result_service_id: Custom result service ID
                    enable_metrics: Enable metrics reporting
                    metrics_interval: Metrics reporting interval in seconds
                Raises:
                    ValueError: If type is not "client" or "server"
        """
        ...

    async def async_consume_message(self: Any, timeout: float = 60.0) -> Optional[Dict]:
        """
        Consume a message from Kafka asynchronously.
        
                Args:
                    timeout: Maximum time to wait for message in seconds
        
                Returns:
                    Message dictionary if available, None if no message received
        
                Raises:
                    RuntimeError: If consumer is not initialized
                    AsyncKafkaError: If message consumption fails
        """
        ...

    async def async_produce_message(self: Any, message: dict, timeout: float = 60.0, key: Optional[str] = None) -> None:
        """
        Produce a message to Kafka asynchronously.
        
                Args:
                    message: Message to produce
                    timeout: Maximum time to wait for message delivery in seconds
                    key: Optional key for message partitioning (stream_id/camera_id)
        
                Raises:
                    RuntimeError: If producer is not initialized or event loop is unavailable
                    ValueError: If message is invalid
                    AsyncKafkaError: If message production fails
        """
        ...

    def check_setup_success(self: Any) -> bool:
        """
        Check if the Kafka setup is successful and attempt to recover if not.
        
                Returns:
                    bool: True if setup was successful, False otherwise
        """
        ...

    async def close(self: Any) -> None:
        """
        Close Kafka producer and consumer connections.
        
                This method gracefully closes all Kafka connections without raising exceptions
                to ensure proper cleanup during shutdown.
        """
        ...

    def configure_metrics_reporting(self: Any, interval: int = 120, batch_size: int = 1000) -> None:
        """
        Configure background metrics reporting for both sync and async Kafka utilities.
        
                This method enables automatic metrics collection and reporting to the backend API
                for all Kafka operations performed through this deployment.
        
                Args:
                    interval: Reporting interval in seconds (default: 120)
                    batch_size: Maximum metrics per batch (default: 1000)
        """
        ...

    def consume_message(self: Any, timeout: float = 60.0) -> Optional[Dict]:
        """
        Consume a message from Kafka.
        
                Args:
                    timeout: Maximum time to wait for message in seconds
        
                Returns:
                    Message dictionary if available, None if no message received
        
                Raises:
                    RuntimeError: If consumer is not initialized
                    KafkaError: If message consumption fails
        """
        ...

    def get_all_metrics(self: Any) -> Dict:
        """
        Get aggregated metrics from all Kafka utilities.
        
                Returns:
                    Dict: Combined metrics from sync and async Kafka utilities
        """
        ...

    def get_kafka_info(self: Any) -> Any:
        """
        Get Kafka setup information from the API.
        
                Returns:
                    Tuple containing (setup_success, bootstrap_server, request_topic, result_topic)
        
                Raises:
                    ValueError: If API requests fail or return invalid data
        """
        ...

    def get_metrics_summary(self: Any) -> Dict:
        """
        Get a summary of metrics from all Kafka utilities.
        
                Returns:
                    Dict: Summarized metrics with counts and statistics
        """
        ...

    def produce_message(self: Any, message: dict, timeout: float = 60.0, key: Optional[str] = None) -> None:
        """
        Produce a message to Kafka.
        
                Args:
                    message: Message to produce
                    timeout: Maximum time to wait for message delivery in seconds
                    key: Optional key for message partitioning (stream_id/camera_id)
        
                Raises:
                    RuntimeError: If producer is not initialized
                    ValueError: If message is invalid
                    KafkaError: If message production fails
        """
        ...

    def refresh(self: Any) -> Any:
        """
        Refresh the Kafka producer and consumer connections.
        """
        ...


# From matrice_stream
class MatriceStream:
    # Comprehensive wrapper class that provides unified interface for Kafka and Redis operations.
    # Supports both synchronous and asynchronous operations with full configuration support.

    def __init__(self: Any, stream_type: Any, **config: Any) -> None:
        """
        Initialize MatriceStream wrapper.
        
        Args:
            stream_type: Either StreamType.KAFKA or StreamType.REDIS
            **config: Configuration parameters for the underlying stream client
        
        Kafka Configuration:
            bootstrap_servers (str): Kafka bootstrap servers
            sasl_mechanism (str): SASL mechanism (default: "SCRAM-SHA-256")
            sasl_username (str): SASL username (default: from KAFKA_SASL_USERNAME env var)
            sasl_password (str): SASL password (default: from KAFKA_SASL_PASSWORD env var)
            security_protocol (str): Security protocol (default: "SASL_PLAINTEXT")
            enable_metrics (bool): Enable metrics reporting (default: True)
            metrics_interval (int): Metrics reporting interval (default: 120)
        
        Redis Configuration:
            host (str): Redis server hostname (default: "localhost")
            port (int): Redis server port (default: 6379)
            password (str): Redis password
            username (str): Redis username (Redis 6.0+)
            db (int): Database number (default: 0)
            connection_timeout (int): Connection timeout (default: 30)
            enable_metrics (bool): Enable metrics reporting (default: True)
            metrics_interval (int): Metrics reporting interval (default: 60)
            enable_shm_batching (bool): Enable batching for SHM metadata operations (default: False)
        
        Example:
            # Kafka configuration
            kafka_stream = MatriceStream(
                StreamType.KAFKA,
                bootstrap_servers="localhost:9092",
                sasl_username="user",
                sasl_password="pass"  # pragma: allowlist secret
            )
        
            # Redis configuration
            redis_stream = MatriceStream(
                StreamType.REDIS,
                host="localhost",
                port=6379,
                password="redis_pass"  # pragma: allowlist secret
            )
        """
        ...

    def add_message(self: Any, topic_or_channel: str, message: Union[dict, str, Any, Any], key: Optional[str] = None, **kwargs: Any) -> Union[None, int]:
        """
        Add/send a message to the stream synchronously.
        
        Args:
            topic_or_channel: Topic (Kafka) or channel (Redis) name
            message: Message to send
            key: Message key (Kafka only)
            **kwargs: Additional parameters
        
        Returns:
            None for Kafka, number of subscribers for Redis
        
        Raises:
            RuntimeError: If stream is not setup or operation fails
        """
        ...

    async def async_add_message(self: Any, topic_or_channel: str, message: Union[dict, str, Any, Any], key: Optional[str] = None, **kwargs: Any) -> Union[None, int]:
        """
        Add/send a message to the stream asynchronously.
        
        Args:
            topic_or_channel: Topic (Kafka) or channel (Redis) name
            message: Message to send
            key: Message key (Kafka only)
            **kwargs: Additional parameters
        
        Returns:
            None for Kafka, number of subscribers for Redis
        
        Raises:
            RuntimeError: If stream is not setup or operation fails
        """
        ...

    async def async_close(self: Any) -> Any:
        """
        Close the asynchronous stream and cleanup resources.
        
        Raises:
            RuntimeError: If close operation fails
        """
        ...

    async def async_get_message(self: Any, timeout: float = 60.0) -> Optional[Dict]:
        """
        Get a message from the stream asynchronously.
        
        Args:
            timeout: Maximum time to wait for message in seconds
        
        Returns:
            Message dictionary or None if timeout
        
        Raises:
            RuntimeError: If stream is not setup or operation fails
        """
        ...

    async def async_get_messages_batch(self: Any, timeout: float = 0.001, count: int = 32) -> List[Dict]:
        """
        Get multiple messages from the stream in a single batch (high-throughput).
        
        This method is optimized for high-frequency polling scenarios.
        Instead of one message per call, reads up to `count` messages at once,
        reducing syscalls and network round-trips by 10-50x.
        
        Args:
            timeout: Maximum time to wait for messages in seconds (default: 1ms)
            count: Maximum number of messages to read (default: 32)
        
        Returns:
            List of message dictionaries (may be empty if timeout)
        
        Raises:
            RuntimeError: If stream is not setup or operation fails
        """
        ...

    async def async_setup(self: Any, topic_or_channel: str, consumer_group_id: Optional[str] = None) -> Any:
        """
        Setup the asynchronous stream for operations.
        
        Args:
            topic_or_channel: Topic name (Kafka) or channel name (Redis)
            consumer_group_id: Consumer group ID (Kafka only, optional)
        
        Raises:
            RuntimeError: If setup fails
        """
        ...

    def close(self: Any) -> Any:
        """
        Close the synchronous stream and cleanup resources.
        
        Raises:
            RuntimeError: If close operation fails
        """
        ...

    def configure_metrics_reporting(self: Any, rpc_client: Any, deployment_id: Optional[str] = None, interval: Optional[int] = None, batch_size: int = 1000) -> None:
        """
        Configure background metrics reporting for stream operations.
        
        Args:
            rpc_client: RPC client instance for API communication
            deployment_id: Deployment identifier for metrics context
            interval: Reporting interval in seconds (default varies by stream type)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        ...

    def get_consumer_group_id(self: Any) -> Optional[str]:
        """
        Get the consumer group ID (Kafka only).
        
        Returns:
            Consumer group ID or None
        """
        ...

    def get_message(self: Any, timeout: float = 1.0) -> Optional[Dict]:
        """
        Get a message from the stream synchronously.
        
        Args:
            timeout: Maximum time to wait for message in seconds
        
        Returns:
            Message dictionary or None if timeout
        
        Raises:
            RuntimeError: If stream is not setup or operation fails
        """
        ...

    def get_metrics(self: Any, clear_after_read: bool = False) -> Dict:
        """
        Get collected metrics from both sync and async clients.
        
        Args:
            clear_after_read: Whether to clear metrics after reading
        
        Returns:
            Dict containing sync and async metrics
        """
        ...

    def get_stream_type(self: Any) -> Any:
        """
        Get the stream type.
        
        Returns:
            The StreamType enum value
        """
        ...

    def get_topics_or_channels(self: Any) -> List[str]:
        """
        Get the list of configured topics or channels.
        
        Returns:
            List of topic/channel names
        """
        ...

    def is_async_setup(self: Any) -> bool:
        """
        Check if the asynchronous stream is properly setup.
        
        Returns:
            True if async setup is complete, False otherwise
        """
        ...

    def is_setup(self: Any) -> bool:
        """
        Check if the synchronous stream is properly setup.
        
        Returns:
            True if sync setup is complete, False otherwise
        """
        ...

    def setup(self: Any, topic_or_channel: str, consumer_group_id: Optional[str] = None) -> Any:
        """
        Setup the synchronous stream for operations.
        
        Args:
            topic_or_channel: Topic name (Kafka) or channel name (Redis)
            consumer_group_id: Consumer group ID (Kafka only, optional)
        
        Raises:
            RuntimeError: If setup fails
        """
        ...


# From matrice_stream
class StreamType:
    # Enumeration for supported stream types.

    KAFKA: str
    REDIS: str


# From offline_cache
class DeviceInfo:
    # Tracked state for a single device.

    ...

# From offline_cache
class DeviceState:
    OFFLINE: str
    ONLINE: str
    UNKNOWN: str


# From offline_cache
class OfflineRequestCache:
    # Store-and-forward cache that queues requests for offline devices.
    #
    #     When a device goes offline (detected via health_check_fn or send failure),
    #     subsequent requests are queued in memory. When the device comes back online,
    #     queued requests are flushed in order.
    #
    #     Args:
    #         send_fn: Callable(device_id, payload) -> bool. Returns True on success.
    #         health_check_fn: Optional callable(device_id) -> bool. Returns True if online.
    #             If not provided, online/offline is inferred from send_fn success/failure.
    #         max_size: Maximum total queued requests across all devices.
    #         ttl_seconds: Per-request TTL. Expired requests are discarded.
    #         flush_batch_size: Max requests to flush per cycle per device.
    #         check_interval: Seconds between health check cycles.

    def __init__(self: Any, send_fn: Callable[[str, Any], bool], health_check_fn: Optional[Callable[[str], bool]] = None, max_size: int = DEFAULT_MAX_SIZE, ttl_seconds: float = DEFAULT_TTL_SECONDS, flush_batch_size: int = DEFAULT_FLUSH_BATCH_SIZE, check_interval: float = DEFAULT_CHECK_INTERVAL) -> None: ...

    def device_status(self: Any, device_id: str) -> str:
        """
        Get current status of a device.
        """
        ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Get cache statistics.
        """
        ...

    def get_warnings(self: Any, clear: bool = True) -> List[Dict[str, Any]]:
        """
        Get and optionally clear accumulated warnings.
        """
        ...

    def start(self: Any) -> None:
        """
        Start the background health-check and flush thread.
        """
        ...

    def stop(self: Any, flush_timeout: float = 5.0) -> None:
        """
        Stop monitoring and attempt final flush of queued requests.
        """
        ...

    def submit(self: Any, device_id: str, payload: Any) -> bool:
        """
        Submit a request for a device.
        
                If the device is online, sends immediately. If offline or send fails,
                queues the request for later delivery.
        
                Returns:
                    True if sent immediately, False if queued.
        """
        ...


# From offline_cache
class QueuedRequest:
    # A request waiting to be sent when the target comes back online.

    def is_expired(self: Any, ttl: float) -> bool: ...


# From redis_stream
class AsyncRedisUtils:
    # Utility class for asynchronous Redis Streams operations.

    def __init__(self: Any, host: str = 'localhost', port: int = 6379, password: Optional[str] = None, username: Optional[str] = None, db: int = 0, connection_timeout: int = 30, pool_max_connections: int = 50, enable_batching: bool = True, batch_size: int = 10, batch_timeout: float = 0.01, enable_shm_batching: bool = False, enable_cross_stream_batching: bool = True, flusher_interval: float = 0.025, stream_maxlen: Optional[int] = None, sentinel_hosts: Optional[List[Tuple[str, int]]] = None, master_name: Optional[str] = None) -> None:
        """
        Initialize async Redis utils with connection parameters.
        
                Args:
                    host: Redis server hostname or IP address
                    port: Redis server port
                    password: Password for Redis authentication
                    username: Username for Redis authentication (Redis 6.0+)
                    db: Database number to connect to
                    connection_timeout: Connection timeout in seconds
                    pool_max_connections: Maximum connections in the connection pool
                    enable_batching: Whether to enable message batching
                    batch_size: Number of messages to batch before flushing (default: 10 - conservative)
                    batch_timeout: Maximum time to wait before flushing batch in seconds (default: 0.01 = 10ms - low latency)
                    enable_shm_batching: Whether to enable batching for SHM metadata operations (default: False)
                    enable_cross_stream_batching: Whether to batch ALL streams in single pipeline (5-10x throughput)
                    flusher_interval: How often batch flusher checks for pending batches (default: 25ms)
                    stream_maxlen: Maximum number of entries to keep in Redis streams (approximate mode)
                    sentinel_hosts: List of (host, port) tuples for Redis Sentinel nodes (optional)
                    master_name: Name of the Redis master in Sentinel configuration (required if sentinel_hosts is set)
        """
        ...

    async def add_frame(self: Any, stream_name: str, frame_data: Any, metadata: Optional[Dict[str, Any]] = None, message_key: Optional[str] = None) -> str:
        """
        Optimized method for adding video frame data to a stream.
        
                This method is specifically optimized for high-throughput video frame
                streaming with minimal overhead. It stores frame data as raw bytes
                without base64 encoding and supports optional batching.
        
                Args:
                    stream_name: Name of the Redis stream
                    frame_data: Raw frame bytes (e.g., JPEG, PNG, H264)
                    metadata: Optional metadata dictionary
                    message_key: Optional message ID
        
                Returns:
                    Message ID assigned by Redis
        
                Raises:
                    RedisConnectionError: If operation fails
        """
        ...

    async def add_message(self: Any, stream_name: str, message: Union[dict, str, Any, Any], message_key: Optional[str] = None, timeout: float = 30.0) -> str:
        """
        Add message to Redis stream asynchronously with automatic batching.
        
                When batching is enabled, messages are buffered and sent in batches via
                Redis pipeline for optimal performance (10x fewer round-trips).
        
                Args:
                    stream_name: Stream to add message to
                    message: Message to add (dict will be converted to fields)
                    message_key: Optional message key for routing
                    timeout: Maximum time to wait for add completion in seconds
        
                Returns:
                    Message ID assigned by Redis (or placeholder if batched)
        
                Raises:
                    RuntimeError: If client is not initialized
                    ValueError: If stream_name or message is invalid
                    RedisConnectionError: If message addition fails
        """
        ...

    async def add_messages_batch(self: Any, stream_name: str, messages: List[Dict[str, Any]], message_keys: Optional[List[Optional[str]]] = None) -> List[str]:
        """
        Add multiple messages to a stream in a single batch operation.
        
                This method is optimized for high throughput when you have multiple
                messages to send at once. It uses Redis pipelining internally.
        
                Args:
                    stream_name: Name of the Redis stream
                    messages: List of message dictionaries to add
                    message_keys: Optional list of message IDs (same length as messages)
        
                Returns:
                    List of message IDs assigned by Redis
        
                Raises:
                    RedisConnectionError: If operation fails
        """
        ...

    async def add_shm_metadata(self: Any, stream_name: str, cam_id: str, shm_name: str, frame_idx: int, slot: int, ts_ns: int, width: int, height: int, format: str, is_similar: bool = False, reference_frame_idx: Optional[int] = None, similarity_score: Optional[float] = None, **extra_metadata: Any) -> str:
        """
        Async: Add metadata-only message for SHM frame (no binary content).
        
                In SHM_MODE, frames are stored in shared memory ring buffers.
                Redis only carries lightweight metadata pointing to the SHM location.
        
                Message format:
                {
                    "shm_mode": 1,           # Flag for consumers to detect SHM messages
                    "cam_id": "camera_123",
                    "shm_name": "shm_cam_camera_123",
                    "frame_idx": 183921231,  # Monotonic frame counter
                    "slot": 7,               # Physical slot in ring buffer
                    "ts_ns": 1735190401123456789,
                    "width": 1920,
                    "height": 1080,
                    "format": "NV12",
                    "is_similar": false,     # True if frame similar to previous
                    "reference_frame_idx": null,  # For similar frames
                    ... extra_metadata fields
                }
        
                Args:
                    stream_name: Redis stream to publish to
                    cam_id: Camera identifier
                    shm_name: Shared memory segment name
                    frame_idx: Monotonically increasing frame index
                    slot: Physical slot index in ring buffer
                    ts_ns: Timestamp in nanoseconds
                    width: Frame width in pixels
                    height: Frame height in pixels
                    format: Frame format ("NV12", "BGR", "RGB")
                    is_similar: True if frame is similar to previous (skip SHM read)
                    reference_frame_idx: For similar frames, the frame_idx to reference
                    similarity_score: Similarity score if is_similar is True
                    **extra_metadata: Additional metadata fields (stream_group_key, etc.)
        
                Returns:
                    Message ID from Redis XADD
        
                Raises:
                    RedisConnectionError: If message publish fails
        """
        ...

    async def close(self: Any) -> None:
        """
        Close async Redis client connections.
        """
        ...

    def configure_metrics_reporting(self: Any, rpc_client: Any, deployment_id: Optional[str] = None, interval: int = 60, batch_size: int = 1000) -> None:
        """
        Configure background metrics reporting to backend API.
        
                Args:
                    rpc_client: RPC client instance for API communication
                    deployment_id: Deployment identifier for metrics context
                    interval: Reporting interval in seconds (default: 60)
                    batch_size: Maximum metrics per batch (default: 1000)
        """
        ...

    async def flush_pending_messages(self: Any) -> None:
        """
        Manually flush all pending batched messages for all streams.
        
                This is useful when you want to ensure all messages are sent immediately,
                such as before closing the connection or at critical points.
        """
        ...

    async def get_message(self: Any, stream_name: Optional[str] = None, timeout: float = 60.0) -> Optional[Dict]:
        """
        Get a single message from Redis stream asynchronously.
        
                Args:
                    stream_name: Stream to read from (if None, reads from all configured streams)
                    timeout: Maximum time to wait for message in seconds
        
                Returns:
                    Message dictionary if available, None if no message received
        
                Raises:
                    RuntimeError: If no streams are configured
                    RedisConnectionError: If message retrieval fails
        """
        ...

    async def get_messages_batch(self: Any, stream_name: Optional[str] = None, timeout: float = 0.001, count: int = 32) -> List[Dict]:
        """
        Get multiple messages from Redis stream in a single batch.
        
                HIGH-THROUGHPUT: This method is optimized for high-frequency polling.
                Instead of one message per call, reads up to `count` messages at once.
                Reduces syscalls and network round-trips by 10-50x.
        
                Args:
                    stream_name: Stream to read from (if None, reads from all configured streams)
                    timeout: Maximum time to block waiting for messages in seconds (default: 1ms)
                    count: Maximum number of messages to read (default: 32)
        
                Returns:
                    List of message dictionaries (may be empty if timeout)
        
                Raises:
                    RuntimeError: If no streams are configured
                    RedisConnectionError: If message retrieval fails
        """
        ...

    async def listen_for_messages(self: Any, callback: Optional[Callable] = None, stream_name: Optional[str] = None) -> None:
        """
        Listen for messages on configured streams asynchronously (blocking).
        
                Args:
                    callback: Optional callback function for all messages
                    stream_name: Optional specific stream to listen to (listens to all if None)
        
                Raises:
                    RuntimeError: If no streams are configured
                    RedisConnectionError: If listening fails
        """
        ...

    async def setup_client(self: Any, **kwargs: Any) -> None:
        """
        Set up async Redis client connection.
        
                Args:
                    **kwargs: Additional Redis client configuration options
        
                Raises:
                    RedisConnectionError: If client initialization fails
        """
        ...

    async def setup_stream(self: Any, stream_name: str, consumer_group: str, consumer_name: Optional[str] = None) -> None:
        """
        Set up Redis stream with consumer group asynchronously.
        
                Args:
                    stream_name: Name of the Redis stream
                    consumer_group: Name of the consumer group
                    consumer_name: Name of the consumer (defaults to hostname-timestamp)
        
                Raises:
                    RedisConnectionError: If stream setup fails
        """
        ...

    async def subscribe_to_stream(self: Any, stream_name: str, consumer_group: str, consumer_name: Optional[str] = None) -> None:
        """
        Subscribe to a Redis stream asynchronously (alias for setup_stream for compatibility).
        
                Args:
                    stream_name: Stream to subscribe to
                    consumer_group: Consumer group name
                    consumer_name: Consumer name (optional)
        
                Raises:
                    RedisConnectionError: If stream setup fails
                    ValueError: If stream_name is empty
        """
        ...

    async def unsubscribe_from_stream(self: Any, stream_name: str) -> None:
        """
        Remove stream from local tracking asynchronously (consumer group remains on Redis).
        
                Args:
                    stream_name: Stream to unsubscribe from
        """
        ...


# From redis_stream
class MatriceRedisDeployment:
    # Class for managing Redis deployments for Matrice streaming API.

    def __init__(self: Any, session: Any, service_id: str, type: str, host: str = 'localhost', port: int = 6379, password: Optional[str] = None, username: Optional[str] = None, db: int = 0, consumer_group: Optional[str] = None, enable_metrics: bool = True, metrics_interval: int = 60) -> None:
        """
        Initialize Redis streams deployment with deployment ID.
        
                Args:
                    session: Session object for authentication and RPC
                    service_id: ID of the deployment
                    type: Type of deployment ("client" or "server")
                    host: Redis server hostname or IP address
                    port: Redis server port
                    password: Password for Redis authentication
                    username: Username for Redis authentication (Redis 6.0+)
                    db: Database number to connect to
                    consumer_group: Consumer group name (defaults to service_id-type)
                    enable_metrics: Whether to auto-enable metrics reporting (default: True)
                    metrics_interval: Metrics reporting interval in seconds (default: 60)
                Raises:
                    ValueError: If type is not "client" or "server"
        """
        ...

    async def async_get_message(self: Any, timeout: float = 60.0) -> Optional[Dict]:
        """
        Get a message from Redis stream asynchronously.
        
                Args:
                    timeout: Maximum time to wait for message in seconds
        
                Returns:
                    Message dictionary if available, None if no message received
        
                Raises:
                    RuntimeError: If subscriber is not initialized
                    RedisConnectionError: If message retrieval fails
        """
        ...

    async def async_publish_message(self: Any, message: dict, timeout: float = 60.0) -> str:
        """
        Add a message to Redis stream asynchronously.
        
                Args:
                    message: Message to add to stream
                    timeout: Maximum time to wait for message addition in seconds
        
                Returns:
                    Message ID assigned by Redis
        
                Raises:
                    RuntimeError: If client is not initialized
                    ValueError: If message is invalid
                    RedisConnectionError: If message addition fails
        """
        ...

    def check_setup_success(self: Any) -> bool:
        """
        Check if the Redis setup is successful.
        
                Returns:
                    bool: True if setup was successful, False otherwise
        """
        ...

    async def close(self: Any) -> None:
        """
        Close Redis client and subscriber connections.
        
                This method gracefully closes all Redis connections without raising exceptions
                to ensure proper cleanup during shutdown.
        """
        ...

    def configure_metrics_reporting(self: Any, interval: int = 60, batch_size: int = 1000) -> None:
        """
        Configure background metrics reporting for both sync and async Redis utilities.
        
                This method enables automatic metrics collection and reporting to the backend API
                for all Redis operations performed through this deployment.
        
                Args:
                    interval: Reporting interval in seconds (default: 60)
                    batch_size: Maximum metrics per batch (default: 1000)
        """
        ...

    def get_all_metrics(self: Any) -> Dict:
        """
        Get aggregated metrics from all Redis utilities.
        
                Returns:
                    Dict: Combined metrics from sync and async Redis utilities
        """
        ...

    def get_message(self: Any, timeout: float = 60.0) -> Optional[Dict]:
        """
        Get a message from Redis stream.
        
                Args:
                    timeout: Maximum time to wait for message in seconds
        
                Returns:
                    Message dictionary if available, None if no message received
        
                Raises:
                    RuntimeError: If subscriber is not initialized
                    RedisConnectionError: If message retrieval fails
        """
        ...

    def get_metrics_summary(self: Any) -> Dict:
        """
        Get a summary of metrics from all Redis utilities.
        
                Returns:
                    Dict: Summarized metrics with counts and statistics
        """
        ...

    def publish_message(self: Any, message: dict, timeout: float = 60.0) -> str:
        """
        Add a message to Redis stream.
        
                Args:
                    message: Message to add to stream
                    timeout: Maximum time to wait for message addition in seconds
        
                Returns:
                    Message ID assigned by Redis
        
                Raises:
                    RuntimeError: If client is not initialized
                    ValueError: If message is invalid
                    RedisConnectionError: If message addition fails
        """
        ...

    def refresh(self: Any) -> Any:
        """
        Refresh the Redis client and subscriber connections.
        """
        ...


# From redis_stream
class RedisUtils:
    # Utility class for synchronous Redis operations.

    def __init__(self: Any, host: str = 'localhost', port: int = 6379, password: Optional[str] = None, username: Optional[str] = None, db: int = 0, connection_timeout: int = 30, pool_max_connections: int = 50, enable_batching: bool = True, batch_size: int = 10, batch_timeout: float = 0.01, enable_shm_batching: bool = False, stream_maxlen: Optional[int] = None, sentinel_hosts: Optional[List[Tuple[str, int]]] = None, master_name: Optional[str] = None) -> None:
        """
        Initialize Redis utils with connection parameters.
        
                Args:
                    host: Redis server hostname or IP address
                    port: Redis server port
                    password: Password for Redis authentication
                    username: Username for Redis authentication (Redis 6.0+)
                    db: Database number to connect to
                    connection_timeout: Connection timeout in seconds
                    pool_max_connections: Maximum connections in the connection pool
                    enable_batching: Whether to enable message batching
                    batch_size: Number of messages to batch before flushing (default: 10 - conservative)
                    batch_timeout: Maximum time to wait before flushing batch in seconds (default: 0.01 = 10ms - low latency)
                    enable_shm_batching: Whether to enable batching for SHM metadata operations (default: False)
                    stream_maxlen: Maximum number of entries to keep in Redis streams (approximate mode)
                    sentinel_hosts: List of (host, port) tuples for Redis Sentinel nodes (optional)
                    master_name: Name of the Redis master in Sentinel configuration (required if sentinel_hosts is set)
        """
        ...

    def add_frame(self: Any, stream_name: str, frame_data: Any, metadata: Dict, use_batching: Optional[bool] = None) -> Optional[str]:
        """
        Optimized method for adding video frame to Redis stream.
        
                Args:
                    stream_name: Stream to add frame to
                    frame_data: Raw binary frame data (no encoding)
                    metadata: Frame metadata (camera_id, timestamp, etc.)
                    use_batching: Override default batching behavior
        
                Returns:
                    Message ID if sent immediately, None if batched
        
                Raises:
                    RuntimeError: If client is not set up
        """
        ...

    def add_message(self: Any, stream_name: str, message: Union[dict, str, Any, Any], message_key: Optional[str] = None, timeout: float = 30.0) -> str:
        """
        Add message to Redis stream.
        
                Args:
                    stream_name: Stream to add message to
                    message: Message to add (dict will be converted to fields)
                    message_key: Optional message key for routing
                    timeout: Maximum time to wait for add completion in seconds
        
                Returns:
                    Message ID assigned by Redis
        
                Raises:
                    RuntimeError: If client is not set up
                    RedisConnectionError: If message addition fails
                    ValueError: If stream_name is empty or message is None
        """
        ...

    def add_messages_batch(self: Any, stream_name: str, messages: List[Dict], timeout: float = 30.0) -> List[str]:
        """
        Add multiple messages to Redis stream using pipeline.
        
                Args:
                    stream_name: Stream to add messages to
                    messages: List of message dicts
                    timeout: Maximum time to wait (not used, for API compatibility)
        
                Returns:
                    List of message IDs
        
                Raises:
                    RuntimeError: If client is not set up
                    ValueError: If stream_name is empty or messages is empty
        """
        ...

    def add_shm_metadata(self: Any, stream_name: str, cam_id: str, shm_name: str, frame_idx: int, slot: int, ts_ns: int, width: int, height: int, format: str, is_similar: bool = False, reference_frame_idx: Optional[int] = None, similarity_score: Optional[float] = None, **extra_metadata: Any) -> str:
        """
        Add metadata-only message for SHM frame (no binary content).
        
                SHM_MODE: This method sends only frame metadata to Redis.
                Actual frame data is stored in shared memory and accessed via shm_name + slot.
        
                Args:
                    stream_name: Redis stream name (topic)
                    cam_id: Camera identifier
                    shm_name: Shared memory segment name
                    frame_idx: Monotonic frame index from SHM ring buffer
                    slot: Physical slot index in SHM ring buffer
                    ts_ns: Frame timestamp in nanoseconds
                    width: Frame width in pixels
                    height: Frame height in pixels
                    format: Frame format ("NV12", "RGB", "BGR")
                    is_similar: True if this frame is similar to previous (FrameOptimizer)
                    reference_frame_idx: If is_similar, the frame_idx of the reference frame
                    similarity_score: Similarity score from FrameOptimizer
                    **extra_metadata: Additional metadata fields to include
        
                Returns:
                    Message ID assigned by Redis
        
                Raises:
                    RuntimeError: If client is not initialized
                    ValueError: If required fields are missing
                    RedisConnectionError: If message addition fails
        """
        ...

    def close(self: Any) -> None:
        """
        Close Redis client connections.
        """
        ...

    def configure_metrics_reporting(self: Any, rpc_client: Any, deployment_id: Optional[str] = None, interval: int = 60, batch_size: int = 1000) -> None:
        """
        Configure background metrics reporting to backend API.
        
                Args:
                    rpc_client: RPC client instance for API communication
                    deployment_id: Deployment identifier for metrics context
                    interval: Reporting interval in seconds (default: 60)
                    batch_size: Maximum metrics per batch (default: 1000)
        """
        ...

    def flush_pending_messages(self: Any) -> Dict[str, List[str]]:
        """
        Manually flush all pending batched messages.
        
                Returns:
                    Dict mapping stream names to lists of message IDs
        """
        ...

    def get_message(self: Any, stream_name: Optional[str] = None, timeout: float = 1.0) -> Optional[Dict]:
        """
        Get a single message from Redis stream.
        
                Args:
                    stream_name: Stream to read from (if None, reads from all configured streams)
                    timeout: Maximum time to block waiting for message in seconds
        
                Returns:
                    Message dict if available, None if timeout. Dict contains:
                        - stream: Stream name
                        - message_id: Message ID from Redis
                        - data: Parsed message data
                        - fields: Raw fields dictionary
        
                Raises:
                    RuntimeError: If no streams are configured
                    RedisConnectionError: If message retrieval fails
        """
        ...

    def listen_for_messages(self: Any, callback: Optional[Callable] = None, stream_name: Optional[str] = None) -> None:
        """
        Listen for messages on configured streams (blocking).
        
                Args:
                    callback: Optional callback function for all messages
                    stream_name: Optional specific stream to listen to (listens to all if None)
        
                Raises:
                    RuntimeError: If no streams are configured
                    RedisConnectionError: If listening fails
        """
        ...

    def setup_client(self: Any, **kwargs: Any) -> None:
        """
        Set up Redis client connection with connection pooling.
        
                Supports Redis Sentinel for HA: if sentinel_hosts and master_name are
                configured, connects via Sentinel to discover the master. Otherwise
                uses standard standalone connection pooling.
        
                Args:
                    **kwargs: Additional Redis client configuration options
        
                Raises:
                    RedisConnectionError: If client initialization fails
        """
        ...

    def setup_stream(self: Any, stream_name: str, consumer_group: str, consumer_name: Optional[str] = None) -> None:
        """
        Set up Redis stream with consumer group.
        
                Args:
                    stream_name: Name of the Redis stream
                    consumer_group: Name of the consumer group
                    consumer_name: Name of the consumer (defaults to hostname-timestamp)
        
                Raises:
                    RedisConnectionError: If stream setup fails
        """
        ...

    def subscribe_to_stream(self: Any, stream_name: str, consumer_group: str, consumer_name: Optional[str] = None) -> None:
        """
        Subscribe to a Redis stream (alias for setup_stream for compatibility).
        
                Args:
                    stream_name: Stream to subscribe to
                    consumer_group: Consumer group name
                    consumer_name: Consumer name (optional)
        
                Raises:
                    RedisConnectionError: If stream setup fails
                    ValueError: If stream_name is empty
        """
        ...

    def unsubscribe_from_stream(self: Any, stream_name: str) -> None:
        """
        Remove stream from local tracking (consumer group remains on Redis).
        
                Args:
                    stream_name: Stream to unsubscribe from
        """
        ...


# From shm_ring_buffer
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


from . import _stream_helpers, app_warning, autoshm, cuda_shm_ring_buffer, databus, databus_batch_consumer, databus_status, device_topology, event_listener, gpu_camera_map, gpu_placement_registry, kafka_stream, matrice_stream, offline_cache, redis_stream, shm_ring_buffer