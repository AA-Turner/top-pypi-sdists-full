"""Stub file for stream directory."""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from .kafka_stream import KafkaUtils, AsyncKafkaUtils
from .orin_shm_ring_buffer import OrinShmRingBuffer
from .redis_stream import RedisUtils, AsyncRedisUtils

# Constants
CUDA_IPC_HANDLE_SIZE: int = ...  # From cuda_shm_ring_buffer
MAP_SHARED: Any = ...  # From cuda_shm_ring_buffer
PROT_READ: Any = ...  # From cuda_shm_ring_buffer
PROT_WRITE: Any = ...  # From cuda_shm_ring_buffer
SHM_BASE_PATH: Any = ...  # From cuda_shm_ring_buffer
logger: Any = ...  # From cuda_shm_ring_buffer
MAP_SHARED: Any = ...  # From gpu_camera_map
PROT_READ: Any = ...  # From gpu_camera_map
PROT_WRITE: Any = ...  # From gpu_camera_map
SHM_BASE_PATH: Any = ...  # From gpu_camera_map
logger: Any = ...  # From gpu_camera_map
CUDA_IPC_HANDLE_SIZE: int = ...  # From orin_shm_ring_buffer
MAP_SHARED: Any = ...  # From orin_shm_ring_buffer
PROT_READ: Any = ...  # From orin_shm_ring_buffer
PROT_WRITE: Any = ...  # From orin_shm_ring_buffer
SHM_BASE_PATH: Any = ...  # From orin_shm_ring_buffer
logger: Any = ...  # From orin_shm_ring_buffer

# Functions
# From cuda_shm_ring_buffer
def benchmark_cuda_ipc() -> Any:
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

# From matrice_stream_usage_example
async def async_context_manager_example() -> Any:
    """
    Example using async context managers.
    """
    ...

# From matrice_stream_usage_example
def context_manager_example() -> Any:
    """
    Example using context managers for automatic cleanup.
    """
    ...

# From matrice_stream_usage_example
async def kafka_async_example() -> Any:
    """
    Example of asynchronous Kafka streaming operations.
    """
    ...

# From matrice_stream_usage_example
def kafka_sync_example() -> Any:
    """
    Example of synchronous Kafka streaming operations.
    """
    ...

# From matrice_stream_usage_example
async def main() -> Any:
    """
    Main function running all examples.
    """
    ...

# From matrice_stream_usage_example
def metrics_example() -> Any:
    """
    Example of configuring metrics reporting.
    """
    ...

# From matrice_stream_usage_example
def multi_stream_example() -> Any:
    """
    Example of working with multiple streams simultaneously.
    """
    ...

# From matrice_stream_usage_example
async def redis_async_example() -> Any:
    """
    Example of asynchronous Redis streaming operations.
    """
    ...

# From matrice_stream_usage_example
def redis_sync_example() -> Any:
    """
    Example of synchronous Redis streaming operations.
    """
    ...

# From shm_ring_buffer
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

# From shm_ring_buffer
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

# From shm_ring_buffer
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

    def close(self: Any) -> Any:
        """
        Close and cleanup resources.
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

    def get_consumer_cursor(self: Any, consumer_id: Optional[int] = None) -> int:
        """
        Get a consumer's cursor position (for debugging/monitoring).
        
                Args:
                    consumer_id: Consumer ID to query. Defaults to this consumer's ID.
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
        Sync all pending writes.
        """
        ...

    def write_frame(self: Any, gpu_frame: Any.Any) -> int:
        """
        Write a frame to the ring buffer - NEVER BLOCKS.
        
                Multi-consumer design: Producer always wins and overwrites ring buffer.
                Slow consumers will detect skipped frames via read_next().
        
                Args:
                    gpu_frame: NV12 frame to write (must match frame_shape)
        
                Returns:
                    Frame index (always succeeds, never returns -1)
        """
        ...

    def write_frame_fast(self: Any, gpu_frame: Any.Any, sync: bool = True, timestamp_ns: Optional[int] = None, rtp_timestamp: int = 0) -> int:
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


# From event_listener
class EventListener:
    # Generic listener for Kafka events with filtering and custom handlers.
    #
    #     This class provides a flexible event listening infrastructure that can be used
    #     for various event types (camera events, app events, etc.) from Kafka topics.
    #
    #     Example:
    #         ```python
    #         def my_handler(event):
    #             print(f"Received event: {event['eventType']}")
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

    def __init__(self: Any, session: Any, topics: Union[str, List[str]], event_handler: Callable[[Dict[str, Any]], None], filter_field: Optional[str] = None, filter_value: Optional[str] = None, consumer_group_id: Optional[str] = None, offset_reset: str = 'latest') -> None:
        """
        Initialize event listener.
        
                Args:
                    session: Session object for authentication and API access
                    topics: List of Kafka topics to subscribe to
                    event_handler: Callback function to handle events
                    filter_field: Optional field name to filter events (e.g., 'streamingGatewayId')
                    filter_value: Optional value to match for filtering
                    consumer_group_id: Optional Kafka consumer group ID (auto-generated if not provided)
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

    def close(self: Any) -> Any:
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

    def get_cameras_for_gpu(self: Any, gpu_id: int) -> list:
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
                    deployment_id: Deployment identifier for metrics context
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

    def get_metrics(self: Any, clear_after_read: bool = False) -> List[Dict]:
        """
        Get collected metrics for aggregation and reporting.
        
                Args:
                    clear_after_read: Whether to clear metrics after reading
        
                Returns:
                    List of metric dictionaries
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

    def stop_metrics_reporting(self: Any) -> None:
        """
        Stop the background metrics reporting thread (async version).
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
                    deployment_id: Deployment identifier for metrics context
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

    def get_metrics(self: Any, clear_after_read: bool = False) -> List[Dict]:
        """
        Get collected metrics for aggregation and reporting.
        
                Args:
                    clear_after_read: Whether to clear metrics after reading
        
                Returns:
                    List of metric dictionaries
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

    def stop_metrics_reporting(self: Any) -> None:
        """
        Stop the background metrics reporting thread.
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
                sasl_password="pass"
            )
        
            # Redis configuration
            redis_stream = MatriceStream(
                StreamType.REDIS,
                host="localhost",
                port=6379,
                password="redis_pass"
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


# From orin_shm_ring_buffer
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


# From redis_stream
class AsyncRedisUtils:
    # Utility class for asynchronous Redis Streams operations.

    def __init__(self: Any, host: str = 'localhost', port: int = 6379, password: Optional[str] = None, username: Optional[str] = None, db: int = 0, connection_timeout: int = 30, pool_max_connections: int = 50, enable_batching: bool = True, batch_size: int = 10, batch_timeout: float = 0.01, enable_shm_batching: bool = False, enable_cross_stream_batching: bool = True, flusher_interval: float = 0.025, stream_maxlen: Optional[int] = None) -> None:
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

    def get_metrics(self: Any, clear_after_read: bool = False) -> List[Dict]:
        """
        Get collected metrics for aggregation and reporting.
        
                Args:
                    clear_after_read: Whether to clear metrics after reading
        
                Returns:
                    List of metric dictionaries
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

    def stop_metrics_reporting(self: Any) -> None:
        """
        Stop the background metrics reporting thread (async version).
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

    def __init__(self: Any, host: str = 'localhost', port: int = 6379, password: Optional[str] = None, username: Optional[str] = None, db: int = 0, connection_timeout: int = 30, pool_max_connections: int = 50, enable_batching: bool = True, batch_size: int = 10, batch_timeout: float = 0.01, enable_shm_batching: bool = False, stream_maxlen: Optional[int] = None) -> None:
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

    def get_metrics(self: Any, clear_after_read: bool = False) -> List[Dict]:
        """
        Get collected metrics for aggregation and reporting.
        
                Args:
                    clear_after_read: Whether to clear metrics after reading
        
                Returns:
                    List of metric dictionaries
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

    def stop_metrics_reporting(self: Any) -> None:
        """
        Stop the background metrics reporting thread.
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


from . import cuda_shm_ring_buffer, event_listener, gpu_camera_map, kafka_stream, matrice_stream, matrice_stream_usage_example, orin_shm_ring_buffer, redis_stream, shm_ring_buffer