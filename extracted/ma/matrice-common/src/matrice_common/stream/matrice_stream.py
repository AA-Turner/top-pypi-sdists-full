"""Comprehensive wrapper class combining Kafka and Redis streaming functionality."""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

logger = logging.getLogger(__name__)


class StreamType(Enum):
    """Enumeration for supported stream types."""

    KAFKA = "kafka"
    REDIS = "redis"


class MatriceStream:
    """
    Comprehensive wrapper class that provides unified interface for Kafka and Redis operations.
    Supports both synchronous and asynchronous operations with full configuration support.
    """

    def __init__(self, stream_type: StreamType, **config: Any) -> None:
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
        self.stream_type = stream_type
        self.config = config
        self.sync_client: Any = None
        self.async_client: Any = None
        self._setup_complete: bool = False
        self._async_setup_complete: bool = False
        self._topics_or_channels: Set[str] = set()
        self._consumer_group_id: Optional[str] = None

        # Initialize the appropriate clients
        if stream_type == StreamType.KAFKA:
            self._init_kafka_clients()
        elif stream_type == StreamType.REDIS:
            self._init_redis_clients()
        else:
            raise ValueError(f"Unsupported stream type: {stream_type}")

    def _init_kafka_clients(self):
        """Initialize Kafka sync and async clients."""
        from .kafka_stream import AsyncKafkaUtils, KafkaUtils

        # Extract Kafka configuration
        bootstrap_servers = self.config.get("bootstrap_servers", "localhost:9092")
        sasl_mechanism = self.config.get("sasl_mechanism", "SCRAM-SHA-256")
        sasl_username = self.config.get("sasl_username")
        sasl_password = self.config.get("sasl_password")
        security_protocol = self.config.get("security_protocol", "SASL_PLAINTEXT")

        # Initialize sync Kafka client
        self.sync_client = KafkaUtils(
            bootstrap_servers=bootstrap_servers,
            sasl_mechanism=sasl_mechanism,
            sasl_username=sasl_username,
            sasl_password=sasl_password,
            security_protocol=security_protocol,
        )

        # Initialize async Kafka client
        self.async_client = AsyncKafkaUtils(
            bootstrap_servers=bootstrap_servers,
            sasl_mechanism=sasl_mechanism,
            sasl_username=sasl_username,
            sasl_password=sasl_password,
            security_protocol=security_protocol,
        )

    @staticmethod
    def _resolve_sentinel_master(sentinel_hosts, master_name, host, port, password):
        """Resolve Redis master address via Sentinel.

        Returns:
            Tuple of (resolved_host, resolved_port).
        """
        try:
            from redis.sentinel import Sentinel

            sentinel_entries = []
            for sh in sentinel_hosts:
                if isinstance(sh, (list, tuple)):
                    sentinel_entries.append(tuple(sh))
                elif isinstance(sh, str):
                    parts = sh.split(":")
                    sentinel_entries.append((parts[0], int(parts[1]) if len(parts) > 1 else 26379))
                elif isinstance(sh, dict):
                    sentinel_entries.append((sh.get("host", host), int(sh.get("port", 26379))))
            if not sentinel_entries:
                sentinel_entries = [(host, 26379)]
            sentinel_kwargs = {"socket_timeout": 5}
            if password:
                sentinel_kwargs["password"] = password
            sentinel = Sentinel(sentinel_entries, **sentinel_kwargs)
            master_addr = sentinel.discover_master(master_name)
            logging.info(
                "Sentinel resolved master '%s' to %s:%d (was %s:%d)",
                master_name,
                master_addr[0],
                master_addr[1],
                host,
                port,
            )
            return master_addr[0], master_addr[1]
        except Exception as e:
            logging.warning(
                "Sentinel master resolution failed for '%s', using configured host %s:%d: %s",
                master_name,
                host,
                port,
                e,
            )
            return host, port

    def _init_redis_clients(self):
        """Initialize Redis sync and async clients."""
        from .redis_stream import AsyncRedisUtils, RedisUtils

        # Extract Redis configuration
        host = self.config.get("host", "localhost")
        port = self.config.get("port", 6379)
        password = self.config.get("password")
        username = self.config.get("username")
        db = self.config.get("db", 0)
        connection_timeout = self.config.get("connection_timeout", 30)

        # New configuration for connection pooling and batching
        pool_max_connections = self.config.get("pool_max_connections", 50)
        enable_batching = self.config.get("enable_batching", True)
        batch_size = self.config.get("batch_size", 50)
        batch_timeout = self.config.get("batch_timeout", 0.1)
        enable_shm_batching = self.config.get("enable_shm_batching", False)

        # Sentinel configuration for HA Redis
        sentinel_hosts = self.config.get("sentinel_hosts")
        master_name = self.config.get("master_name")

        # Resolve master via Sentinel before creating clients.
        if sentinel_hosts and master_name:
            host, port = self._resolve_sentinel_master(sentinel_hosts, master_name, host, port, password)

        # Initialize sync Redis client with pooling and batching
        self.sync_client = RedisUtils(
            host=host,
            port=port,
            password=password,
            username=username,
            db=db,
            connection_timeout=connection_timeout,
            pool_max_connections=pool_max_connections,
            enable_batching=enable_batching,
            batch_size=batch_size,
            batch_timeout=batch_timeout,
            enable_shm_batching=enable_shm_batching,
            sentinel_hosts=sentinel_hosts,
            master_name=master_name,
        )

        # Initialize async Redis client with pooling and batching
        self.async_client = AsyncRedisUtils(
            host=host,
            port=port,
            password=password,
            username=username,
            db=db,
            connection_timeout=connection_timeout,
            pool_max_connections=pool_max_connections,
            enable_batching=enable_batching,
            batch_size=batch_size,
            batch_timeout=batch_timeout,
            enable_shm_batching=enable_shm_batching,
            sentinel_hosts=sentinel_hosts,
            master_name=master_name,
        )

    def setup(self, topic_or_channel: str, consumer_group_id: Optional[str] = None):
        """
        Setup the synchronous stream for operations.

        Args:
            topic_or_channel: Topic name (Kafka) or channel name (Redis)
            consumer_group_id: Consumer group ID (Kafka only, optional)

        Raises:
            RuntimeError: If setup fails
        """
        try:
            if self.stream_type == StreamType.KAFKA:
                # Setup producer and consumer for Kafka
                self.sync_client.setup_producer()
                if consumer_group_id:
                    self._consumer_group_id = consumer_group_id
                    self.sync_client.setup_consumer(topics=[topic_or_channel], group_id=consumer_group_id)
                self._topics_or_channels.add(topic_or_channel)
            elif self.stream_type == StreamType.REDIS:
                # Setup Redis client and stream
                self.sync_client.setup_client()
                consumer_group = consumer_group_id or f"{topic_or_channel}_group"
                consumer_name = f"consumer_{id(self)}"
                self.sync_client.setup_stream(topic_or_channel, consumer_group, consumer_name)
                self._topics_or_channels.add(topic_or_channel)

            self._setup_complete = True
            logging.info(f"Successfully setup {self.stream_type.value} stream for {topic_or_channel}")
        except Exception as e:
            error_msg = f"Failed to setup {self.stream_type.value} stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    async def async_setup(self, topic_or_channel: str, consumer_group_id: Optional[str] = None):
        """
        Setup the asynchronous stream for operations.

        Args:
            topic_or_channel: Topic name (Kafka) or channel name (Redis)
            consumer_group_id: Consumer group ID (Kafka only, optional)

        Raises:
            RuntimeError: If setup fails
        """
        try:
            if self.stream_type == StreamType.KAFKA:
                # Setup producer and consumer for Kafka
                await self.async_client.setup_producer()
                if consumer_group_id:
                    self._consumer_group_id = consumer_group_id
                    await self.async_client.setup_consumer(topics=[topic_or_channel], group_id=consumer_group_id)
                self._topics_or_channels.add(topic_or_channel)
            elif self.stream_type == StreamType.REDIS:
                # Setup Redis client and stream
                await self.async_client.setup_client()
                consumer_group = consumer_group_id or f"{topic_or_channel}_group"
                consumer_name = f"async_consumer_{id(self)}"
                await self.async_client.setup_stream(topic_or_channel, consumer_group, consumer_name)
                self._topics_or_channels.add(topic_or_channel)

            self._async_setup_complete = True
            logging.info(f"Successfully setup async {self.stream_type.value} stream for {topic_or_channel}")
        except Exception as e:
            error_msg = f"Failed to setup async {self.stream_type.value} stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    def add_message(
        self, topic_or_channel: str, message: Union[dict, str, bytes, Any], key: Optional[str] = None, **kwargs
    ) -> Union[None, int]:
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
        if not self._setup_complete:
            raise RuntimeError("Stream not setup. Call setup() first")

        try:
            if self.stream_type == StreamType.KAFKA:
                self.sync_client.produce_message(topic=topic_or_channel, value=message, key=key, **kwargs)
                return None
            elif self.stream_type == StreamType.REDIS:
                return self.sync_client.add_message(
                    stream_name=topic_or_channel, message=message, message_key=key, **kwargs
                )
        except Exception as e:
            error_msg = f"Failed to add message to {self.stream_type.value} stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    async def async_add_message(
        self, topic_or_channel: str, message: Union[dict, str, bytes, Any], key: Optional[str] = None, **kwargs
    ) -> Union[None, int]:
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
        if not self._async_setup_complete:
            raise RuntimeError("Async stream not setup. Call async_setup() first")

        try:
            if self.stream_type == StreamType.KAFKA:
                await self.async_client.produce_message(topic=topic_or_channel, value=message, key=key, **kwargs)
                return None
            elif self.stream_type == StreamType.REDIS:
                return await self.async_client.add_message(
                    stream_name=topic_or_channel, message=message, message_key=key, **kwargs
                )
        except Exception as e:
            error_msg = f"Failed to add message to async {self.stream_type.value} stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    def get_message(self, timeout: float = 1.0) -> Optional[Dict]:
        """
        Get a message from the stream synchronously.

        Args:
            timeout: Maximum time to wait for message in seconds

        Returns:
            Message dictionary or None if timeout

        Raises:
            RuntimeError: If stream is not setup or operation fails
        """
        if not self._setup_complete:
            raise RuntimeError("Stream not setup. Call setup() first")

        try:
            if self.stream_type == StreamType.KAFKA:
                return self.sync_client.consume_message(timeout=timeout)
            elif self.stream_type == StreamType.REDIS:
                return self.sync_client.get_message(timeout=timeout)
        except Exception as e:
            error_msg = f"Failed to get message from {self.stream_type.value} stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    async def async_get_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """
        Get a message from the stream asynchronously.

        Args:
            timeout: Maximum time to wait for message in seconds

        Returns:
            Message dictionary or None if timeout

        Raises:
            RuntimeError: If stream is not setup or operation fails
        """
        if not self._async_setup_complete:
            raise RuntimeError("Async stream not setup. Call async_setup() first")

        try:
            if self.stream_type == StreamType.KAFKA:
                return await self.async_client.consume_message(timeout=timeout)
            elif self.stream_type == StreamType.REDIS:
                return await self.async_client.get_message(timeout=timeout)
        except Exception as e:
            error_msg = f"Failed to get message from async {self.stream_type.value} stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    async def async_get_messages_batch(self, timeout: float = 0.001, count: int = 32) -> List[Dict]:
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
        if not self._async_setup_complete:
            raise RuntimeError("Async stream not setup. Call async_setup() first")

        try:
            if self.stream_type == StreamType.KAFKA:
                # Kafka: Use batch consume if available, otherwise fall back to single
                if hasattr(self.async_client, "consume_messages_batch"):
                    return await self.async_client.consume_messages_batch(timeout=timeout, count=count)
                else:
                    # Fallback: single message wrapped in list
                    msg = await self.async_client.consume_message(timeout=timeout)
                    return [msg] if msg else []
            elif self.stream_type == StreamType.REDIS:
                return await self.async_client.get_messages_batch(timeout=timeout, count=count)
            return []
        except Exception as e:
            error_msg = f"Failed to get message batch from async {self.stream_type.value} stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    def configure_metrics_reporting(
        self, rpc_client, deployment_id: Optional[str] = None, interval: Optional[int] = None, batch_size: int = 1000
    ) -> None:
        """
        Configure background metrics reporting for stream operations.

        Args:
            rpc_client: RPC client instance for API communication
            deployment_id: Deployment identifier for metrics context
            interval: Reporting interval in seconds (default varies by stream type)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        try:
            # Set default interval based on stream type
            if interval is None:
                interval = 120 if self.stream_type == StreamType.KAFKA else 60

            # Configure sync client metrics
            if self.sync_client:
                self.sync_client.configure_metrics_reporting(
                    rpc_client=rpc_client, deployment_id=deployment_id, interval=interval, batch_size=batch_size
                )

            # Configure async client metrics
            if self.async_client:
                self.async_client.configure_metrics_reporting(
                    rpc_client=rpc_client, deployment_id=deployment_id, interval=interval, batch_size=batch_size
                )

            logging.info(f"Configured metrics reporting for {self.stream_type.value} stream")
        except Exception as exc:
            logging.error(f"Error configuring metrics reporting: {exc}")

    def get_metrics(self, clear_after_read: bool = False) -> Dict:
        """
        Get collected metrics from both sync and async clients.

        Args:
            clear_after_read: Whether to clear metrics after reading

        Returns:
            Dict containing sync and async metrics
        """
        metrics = {
            "sync_metrics": [],
            "async_metrics": [],
            "stream_type": self.stream_type.value,
            "topics_or_channels": list(self._topics_or_channels),
        }

        try:
            if self.sync_client:
                metrics["sync_metrics"] = self.sync_client.get_metrics(clear_after_read)
        except Exception as exc:
            logging.warning(f"Error getting sync metrics: {exc}")

        try:
            if self.async_client:
                metrics["async_metrics"] = self.async_client.get_metrics(clear_after_read)
        except Exception as exc:
            logging.warning(f"Error getting async metrics: {exc}")

        return metrics

    def close(self):
        """
        Close the synchronous stream and cleanup resources.

        Raises:
            RuntimeError: If close operation fails
        """
        try:
            if self.sync_client:
                self.sync_client.close()
            self._setup_complete = False
            logging.info(f"Closed {self.stream_type.value} sync stream")
        except Exception as e:
            error_msg = f"Failed to close {self.stream_type.value} sync stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    async def async_close(self):
        """
        Close the asynchronous stream and cleanup resources.

        Raises:
            RuntimeError: If close operation fails
        """
        try:
            if self.async_client:
                await self.async_client.close()
            self._async_setup_complete = False
            logging.info(f"Closed {self.stream_type.value} async stream")
        except Exception as e:
            error_msg = f"Failed to close {self.stream_type.value} async stream: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

    def is_setup(self) -> bool:
        """
        Check if the synchronous stream is properly setup.

        Returns:
            True if sync setup is complete, False otherwise
        """
        return self._setup_complete

    def is_async_setup(self) -> bool:
        """
        Check if the asynchronous stream is properly setup.

        Returns:
            True if async setup is complete, False otherwise
        """
        return self._async_setup_complete

    def get_stream_type(self) -> StreamType:
        """
        Get the stream type.

        Returns:
            The StreamType enum value
        """
        return self.stream_type

    def get_topics_or_channels(self) -> List[str]:
        """
        Get the list of configured topics or channels.

        Returns:
            List of topic/channel names
        """
        return list(self._topics_or_channels)

    def get_consumer_group_id(self) -> Optional[str]:
        """
        Get the consumer group ID (Kafka only).

        Returns:
            Consumer group ID or None
        """
        return self._consumer_group_id

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.async_close()

    def __repr__(self):
        """String representation of the MatriceStream instance."""
        return (
            f"MatriceStream(type={self.stream_type.value}, "
            f"sync_setup={self._setup_complete}, "
            f"async_setup={self._async_setup_complete}, "
            f"topics_channels={len(self._topics_or_channels)})"
        )
