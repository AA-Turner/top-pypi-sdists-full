"""Auto-generated stub for module: matrice_stream."""
from typing import Any, Dict, List, Optional, Union

from .kafka_stream import AsyncKafkaUtils, KafkaUtils
from .redis_stream import AsyncRedisUtils, RedisUtils

# Constants
logger: Any

# Classes
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

class StreamType:
    # Enumeration for supported stream types.

    KAFKA: str
    REDIS: str

