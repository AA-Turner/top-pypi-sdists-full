"""Auto-generated stub for module: redis_stream."""
from typing import Any, Callable, Dict, List, Optional, Set, Union

# Classes
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

