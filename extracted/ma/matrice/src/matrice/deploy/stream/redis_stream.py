"""Module providing synchronous and asynchronous Redis utilities."""

import json
import logging
import time
import threading
import uuid
from collections import deque
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
import redis
import asyncio
import aioredis
from redis.exceptions import ConnectionError as RedisConnectionError, TimeoutError as RedisTimeoutError


class RedisUtils:
    """Utility class for synchronous Redis operations."""

    def __init__(
        self, 
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        username: Optional[str] = None,
        db: int = 0,
        ssl: bool = False,
        ssl_verify: bool = True,
        connection_timeout: int = 30
    ) -> None:
        """Initialize Redis utils with connection parameters.

        Args:
            host: Redis server hostname or IP address
            port: Redis server port
            password: Password for Redis authentication
            username: Username for Redis authentication (Redis 6.0+)
            db: Database number to connect to
            ssl: Whether to use SSL/TLS connection
            ssl_verify: Whether to verify SSL certificates
            connection_timeout: Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.db = db
        self.ssl = ssl
        self.ssl_verify = ssl_verify
        self.connection_timeout = connection_timeout
        self.client = None
        self.pubsub = None
        self._subscribed_channels = set()
        self._subscription_callbacks = {}
        
        # Metrics collection for performance monitoring
        self._metrics_lock = threading.Lock()
        self._metrics_log = deque(maxlen=10000)  # Keep last 10000 metrics entries
        self._pending_operations = {}  # Track pending operations for timing
        
        # Background metrics reporting
        self._metrics_reporting_config = None
        self._metrics_thread = None
        self._metrics_stop_event = threading.Event()
        self._last_metrics_reset = time.time()
        
        logging.info(
            "Initialized RedisUtils with host: %s:%d, db: %d",
            host, port, db
        )

    def _record_metric(self, operation: str, channel: str, start_time: float, end_time: float, 
                      success: bool, error_msg: str = None, message_key: str = None, 
                      message_size: int = None) -> None:
        """Record a performance metric for aggregation.
        
        Args:
            operation: Type of operation ('publish' or 'subscribe')
            channel: Redis channel name
            start_time: Operation start timestamp
            end_time: Operation end timestamp
            success: Whether operation was successful
            error_msg: Error message if operation failed
            message_key: Message key if available
            message_size: Message size in bytes if available
        """
        duration_ms = (end_time - start_time) * 1000  # Convert to milliseconds
        
        metric = {
            'timestamp': end_time,
            'operation': operation,
            'channel': channel,
            'duration_ms': duration_ms,
            'success': success,
            'error_msg': error_msg,
            'message_key': message_key,
            'message_size': message_size,
            'redis_host': f"{self.host}:{self.port}",
            'type': 'sync'
        }
        
        with self._metrics_lock:
            self._metrics_log.append(metric)
        
        # Log summary for monitoring
        status = "SUCCESS" if success else "FAILED"
        logging.info(
            "Redis %s %s: channel=%s, duration=%.2fms, key=%s, size=%s%s",
            operation.upper(), status, channel, duration_ms, message_key or 'None', 
            message_size or 'Unknown', f", error={error_msg}" if error_msg else ""
        )

    def get_metrics(self, clear_after_read: bool = False) -> List[Dict]:
        """Get collected metrics for aggregation and reporting.
        
        Args:
            clear_after_read: Whether to clear metrics after reading
            
        Returns:
            List of metric dictionaries
        """
        with self._metrics_lock:
            metrics = list(self._metrics_log)
            if clear_after_read:
                self._metrics_log.clear()
        
        return metrics

    def configure_metrics_reporting(self, 
                                   rpc_client,
                                   deployment_id: str = None,
                                   interval: int = 60,
                                   batch_size: int = 1000) -> None:
        """Configure background metrics reporting to backend API.
        
        Args:
            rpc_client: RPC client instance for API communication
            deployment_id: Deployment identifier for metrics context
            interval: Reporting interval in seconds (default: 60)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        self._metrics_reporting_config = {
            'rpc_client': rpc_client,
            'deployment_id': deployment_id,
            'interval': interval,
            'batch_size': batch_size,
            'enabled': True
        }
        
        # Start background reporting thread
        if not self._metrics_thread or not self._metrics_thread.is_alive():
            self._metrics_stop_event.clear()
            self._metrics_thread = threading.Thread(
                target=self._metrics_reporter_worker,
                daemon=True,
                name=f"redis-metrics-reporter-{id(self)}"
            )
            self._metrics_thread.start()
            logging.info("Started background Redis metrics reporting thread")

    def _metrics_reporter_worker(self) -> None:
        """Background thread worker for sending metrics to backend API."""
        logging.info("Redis metrics reporter thread started")
        
        while not self._metrics_stop_event.is_set():
            try:
                if not self._metrics_reporting_config or not self._metrics_reporting_config.get('enabled'):
                    self._metrics_stop_event.wait(10)  # Check every 10 seconds if disabled
                    continue
                
                interval = self._metrics_reporting_config.get('interval', 60)
                
                # Wait for the specified interval or stop event
                if self._metrics_stop_event.wait(interval):
                    break  # Stop event was set
                
                # Collect and send metrics
                self._collect_and_send_metrics()
                
            except Exception as exc:
                logging.error(f"Error in Redis metrics reporter thread: {exc}")
                # Wait before retrying to avoid rapid failure loops
                self._metrics_stop_event.wait(30)
        
        logging.info("Redis metrics reporter thread stopped")

    def _collect_and_send_metrics(self) -> None:
        """Collect metrics and send them to the backend API."""
        try:
            # Get metrics since last collection
            raw_metrics = self.get_metrics(clear_after_read=True)
            
            if not raw_metrics:
                logging.debug("No new Redis metrics to report")
                return
            
            # Aggregate metrics by channel for API format
            aggregated_data = self._aggregate_metrics_for_api(raw_metrics)
            
            if aggregated_data.get('channel'):
                # Send to backend API
                success = self._send_metrics_to_api(aggregated_data)
                if success:
                    logging.info(f"Successfully sent {len(raw_metrics)} Redis metrics to backend API")
                else:
                    logging.warning("Failed to send Redis metrics to backend API")
            else:
                logging.debug("No channel-level metrics to report")
                
        except Exception as exc:
            logging.error(f"Error collecting and sending Redis metrics: {exc}")

    def _aggregate_metrics_for_api(self, raw_metrics: List[Dict]) -> Dict:
        """Aggregate raw metrics into the API format expected by backend.
        
        Args:
            raw_metrics: List of raw metric dictionaries
            
        Returns:
            Aggregated metrics in API format
        """
        # Group metrics by channel
        channel_stats = {}
        current_time = datetime.now(timezone.utc).isoformat()
        
        for metric in raw_metrics:
            channel = metric.get('channel', 'unknown')
            operation = metric.get('operation', 'unknown')
            success = metric.get('success', False)
            duration_ms = metric.get('duration_ms', 0)
            
            # Skip timeout and error entries for aggregation
            if channel in ['(timeout)', '(error)', 'unknown']:
                continue
            
            if channel not in channel_stats:
                channel_stats[channel] = {
                    'channel': channel,
                    'publishCount': 0,
                    'subscribeCount': 0,
                    'totalLatency': 0,
                    'latencies': [],  # Temporary for calculations
                    'avgLatency': 0,
                    'minlatency': float('inf'),
                    'maxlatency': 0
                }
            
            stats = channel_stats[channel]
            
            # Count operations by type
            if operation == 'publish' and success:
                stats['publishCount'] += 1
            elif operation == 'subscribe' and success:
                stats['subscribeCount'] += 1
            
            # Track latencies (convert ms to nanoseconds for API compatibility)
            if success and duration_ms > 0:
                latency_ns = int(duration_ms * 1_000_000)  # Convert ms to ns
                stats['latencies'].append(latency_ns)
                stats['totalLatency'] += latency_ns
                stats['minlatency'] = min(stats['minlatency'], latency_ns)
                stats['maxlatency'] = max(stats['maxlatency'], latency_ns)
        
        # Calculate averages and clean up
        for channel, stats in channel_stats.items():
            if stats['latencies']:
                stats['avgLatency'] = stats['totalLatency'] // len(stats['latencies'])
            else:
                stats['avgLatency'] = 0
                stats['minlatency'] = 0
            
            # Remove temporary latencies list
            del stats['latencies']
        
        # Format for API
        api_payload = {
            'channel': list(channel_stats.values()),
            'status': 'success',
            'host': self.host,
            'port': str(self.port),
            'createdAt': current_time,
            'updatedAt': current_time
        }
        
        return api_payload

    def _send_metrics_to_api(self, aggregated_metrics: Dict) -> bool:
        """Send aggregated metrics to backend API using RPC client.
        
        Args:
            aggregated_metrics: Metrics data in API format
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            rpc_client = self._metrics_reporting_config.get('rpc_client')
            if not rpc_client:
                logging.error("No RPC client configured for Redis metrics reporting")
                return False
            
            # Send POST request to the Redis metrics endpoint
            response = rpc_client.post(
                path="/v1/monitoring/add_redis_metrics",
                payload=aggregated_metrics,
                timeout=30
            )
            
            # Check response following existing RPC patterns
            if response and response.get("success"):
                logging.debug("Successfully sent Redis metrics to backend API")
                return True
            else:
                error_msg = response.get('message', 'Unknown error') if response else 'No response'
                logging.error(f"Backend API rejected Redis metrics: {error_msg}")
                return False
                
        except Exception as exc:
            logging.error(f"Error sending Redis metrics to API: {exc}")
            return False

    def stop_metrics_reporting(self) -> None:
        """Stop the background metrics reporting thread."""
        if self._metrics_reporting_config:
            self._metrics_reporting_config['enabled'] = False
        
        if self._metrics_thread and self._metrics_thread.is_alive():
            logging.info("Stopping Redis metrics reporting thread...")
            self._metrics_stop_event.set()
            self._metrics_thread.join(timeout=5)
            if self._metrics_thread.is_alive():
                logging.warning("Redis metrics reporting thread did not stop gracefully")
            else:
                logging.info("Redis metrics reporting thread stopped")

    def setup_client(self, **kwargs) -> None:
        """Set up Redis client connection.

        Args:
            **kwargs: Additional Redis client configuration options

        Raises:
            RedisConnectionError: If client initialization fails
        """
        client_config = {
            "host": self.host,
            "port": self.port,
            "db": self.db,
            "socket_timeout": self.connection_timeout,
            "socket_connect_timeout": self.connection_timeout,
            "retry_on_timeout": True,
            "health_check_interval": 30,
            "decode_responses": False,  # Keep bytes for compatibility
        }
        
        # Add authentication if configured
        if self.password:
            client_config["password"] = self.password
        if self.username:
            client_config["username"] = self.username
            
        # Add SSL configuration if enabled
        if self.ssl:
            client_config["ssl"] = True
            client_config["ssl_cert_reqs"] = "required" if self.ssl_verify else "none"
        
        # Override with any additional config
        client_config.update(kwargs)
        
        try:
            self.client = redis.Redis(**client_config)
            # Test connection
            self.client.ping()
            logging.info("Successfully set up Redis client")
        except Exception as exc:
            error_msg = f"Failed to initialize Redis client: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    def setup_subscriber(self, **kwargs) -> None:
        """Set up Redis pub/sub subscriber.

        Args:
            **kwargs: Additional pub/sub configuration options

        Raises:
            RedisConnectionError: If subscriber setup fails
        """
        if not self.client:
            self.setup_client()
        
        try:
            self.pubsub = self.client.pubsub(**kwargs)
            logging.info("Successfully set up Redis subscriber")
        except Exception as exc:
            error_msg = f"Failed to set up Redis subscriber: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    def _serialize_value(self, value: Any) -> bytes:
        """Serialize message value to bytes.
        
        Args:
            value: Message value to serialize
            
        Returns:
            Serialized value as bytes
        """
        if isinstance(value, dict):
            return json.dumps(value).encode('utf-8')
        elif isinstance(value, str):
            return value.encode('utf-8')
        elif isinstance(value, bytes):
            return value
        else:
            return str(value).encode('utf-8')

    def publish_message(
        self,
        channel: str,
        message: Union[dict, str, bytes, Any],
        timeout: float = 30.0,
    ) -> int:
        """Publish message to Redis channel.

        Args:
            channel: Channel to publish to
            message: Message to publish (dict will be converted to JSON)
            timeout: Maximum time to wait for publish completion in seconds

        Returns:
            Number of subscribers that received the message

        Raises:
            RuntimeError: If client is not set up
            RedisConnectionError: If message publication fails
            ValueError: If channel is empty or message is None
        """
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first")
        if not channel or message is None:
            raise ValueError("Channel and message must be provided")

        # Serialize message
        message_bytes = self._serialize_value(message)
        message_size = len(message_bytes) if message_bytes else 0

        start_time = time.time()
        try:
            # Redis publish returns the number of subscribers
            result = self.client.publish(channel, message_bytes)
            end_time = time.time()
            
            # Record successful publish metrics
            self._record_metric(
                operation="publish",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=None,
                message_size=message_size
            )
            
            logging.debug(
                "Successfully published message to channel: %s, subscribers: %d",
                channel, result
            )
            return result
            
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to publish message: {str(exc)}"
            logging.error(error_msg)
            
            # Record failed publish metrics
            self._record_metric(
                operation="publish",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=message_size
            )
            raise RedisConnectionError(error_msg)

    def subscribe_to_channel(
        self, 
        channel: str,
        callback: Optional[Callable] = None
    ) -> None:
        """Subscribe to a Redis channel.

        Args:
            channel: Channel to subscribe to
            callback: Optional callback function for message handling

        Raises:
            RuntimeError: If subscriber is not set up
            RedisConnectionError: If subscription fails
            ValueError: If channel is empty
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first")
        if not channel:
            raise ValueError("Channel must be provided")

        start_time = time.time()
        try:
            self.pubsub.subscribe(channel)
            self._subscribed_channels.add(channel)
            if callback:
                self._subscription_callbacks[channel] = callback
            
            end_time = time.time()
            
            # Record successful subscription metrics
            self._record_metric(
                operation="subscribe",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=None,
                message_size=None
            )
            
            logging.info("Successfully subscribed to channel: %s", channel)
            
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to subscribe to channel: {str(exc)}"
            logging.error(error_msg)
            
            # Record failed subscription metrics
            self._record_metric(
                operation="subscribe",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None
            )
            raise RedisConnectionError(error_msg)

    def unsubscribe_from_channel(self, channel: str) -> None:
        """Unsubscribe from a Redis channel.

        Args:
            channel: Channel to unsubscribe from

        Raises:
            RuntimeError: If subscriber is not set up
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first")

        try:
            self.pubsub.unsubscribe(channel)
            self._subscribed_channels.discard(channel)
            self._subscription_callbacks.pop(channel, None)
            logging.info("Successfully unsubscribed from channel: %s", channel)
        except Exception as exc:
            logging.error("Failed to unsubscribe from channel %s: %s", channel, str(exc))

    def _parse_message_value(self, value: bytes) -> Any:
        """Parse message value from bytes.
        
        Args:
            value: Message value in bytes
            
        Returns:
            Parsed value or original bytes if parsing fails
        """
        if not value:
            return None

        try:
            return json.loads(value.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return value

    def get_message(self, timeout: float = 1.0) -> Optional[Dict]:
        """Get a single message from subscribed channels.

        Args:
            timeout: Maximum time to block waiting for message in seconds

        Returns:
            Message dict if available, None if timeout. Dict contains:
                - type: Message type ('message', 'subscribe', 'unsubscribe', etc.)
                - channel: Channel name
                - data: Message data
                - pattern: Pattern if pattern subscription (None otherwise)

        Raises:
            RuntimeError: If subscriber is not set up
            RedisConnectionError: If message retrieval fails
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first")
        
        start_time = time.time()
        try:
            message = self.pubsub.get_message(timeout=timeout)
            end_time = time.time()
            
            if message is None:
                # Record timeout as successful operation with no message
                self._record_metric(
                    operation="get_message",
                    channel="(timeout)",
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=None
                )
                return None
            
            # Skip subscription confirmation messages
            if message['type'] in ['subscribe', 'unsubscribe', 'psubscribe', 'punsubscribe']:
                return message
            
            channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else str(message['channel'])
            message_data = message.get('data', b'')
            message_size = len(message_data) if message_data else 0
            
            # Parse the message data
            parsed_data = self._parse_message_value(message_data)
            
            # Record successful message retrieval metrics
            self._record_metric(
                operation="get_message",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=None,
                message_size=message_size
            )
            
            # Execute callback if registered
            if channel in self._subscription_callbacks:
                try:
                    self._subscription_callbacks[channel](message)
                except Exception as callback_exc:
                    logging.error("Error in message callback for channel %s: %s", channel, str(callback_exc))
            
            result = {
                "type": message['type'],
                "channel": channel,
                "data": parsed_data,
                "pattern": message.get('pattern'),
                "raw_data": message_data
            }
            return result
            
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to get message: {str(exc)}"
            logging.error(error_msg)
            
            # Record error metrics
            self._record_metric(
                operation="get_message",
                channel="(error)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None
            )
            raise RedisConnectionError(error_msg)

    def listen_for_messages(self, callback: Optional[Callable] = None) -> None:
        """Listen for messages on subscribed channels (blocking).

        Args:
            callback: Optional global callback function for all messages

        Raises:
            RuntimeError: If subscriber is not set up
            RedisConnectionError: If listening fails
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first")

        try:
            logging.info("Starting to listen for Redis messages...")
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else str(message['channel'])
                    
                    # Execute channel-specific callback
                    if channel in self._subscription_callbacks:
                        try:
                            self._subscription_callbacks[channel](message)
                        except Exception as callback_exc:
                            logging.error("Error in channel callback for %s: %s", channel, str(callback_exc))
                    
                    # Execute global callback
                    if callback:
                        try:
                            callback(message)
                        except Exception as callback_exc:
                            logging.error("Error in global callback: %s", str(callback_exc))
                            
        except Exception as exc:
            error_msg = f"Error listening for messages: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    def close(self) -> None:
        """Close Redis client and subscriber connections."""
        try:
            # Stop metrics reporting thread first
            self.stop_metrics_reporting()
            
            if self.pubsub:
                # Unsubscribe from all channels
                if self._subscribed_channels:
                    try:
                        self.pubsub.unsubscribe(*self._subscribed_channels)
                    except Exception as exc:
                        logging.warning("Error unsubscribing from channels: %s", str(exc))
                
                # Close pubsub connection
                try:
                    self.pubsub.close()
                except Exception as exc:
                    logging.warning("Error closing Redis pubsub: %s", str(exc))
                
                self.pubsub = None
                self._subscribed_channels.clear()
                self._subscription_callbacks.clear()
                
            if self.client:
                try:
                    self.client.close()
                except Exception as exc:
                    logging.warning("Error closing Redis client: %s", str(exc))
                self.client = None
                
            logging.info("Closed Redis connections")
        except Exception as exc:
            logging.error("Error closing Redis connections: %s", str(exc))
            raise


class AsyncRedisUtils:
    """Utility class for asynchronous Redis operations."""

    def __init__(
        self, 
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        username: Optional[str] = None,
        db: int = 0,
        ssl: bool = False,
        ssl_verify: bool = True,
        connection_timeout: int = 30
    ) -> None:
        """Initialize async Redis utils with connection parameters.
        
        Args:
            host: Redis server hostname or IP address
            port: Redis server port
            password: Password for Redis authentication
            username: Username for Redis authentication (Redis 6.0+)
            db: Database number to connect to
            ssl: Whether to use SSL/TLS connection
            ssl_verify: Whether to verify SSL certificates
            connection_timeout: Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.db = db
        self.ssl = ssl
        self.ssl_verify = ssl_verify
        self.connection_timeout = connection_timeout
        self.client: Optional[aioredis.Redis] = None
        self.pubsub = None
        self._subscribed_channels = set()
        self._subscription_callbacks = {}
        
        # Metrics collection for performance monitoring (async-safe)
        self._metrics_log = deque(maxlen=10000)  # Keep last 10000 metrics entries
        self._metrics_lock = threading.Lock()
        self._pending_operations = {}  # Track pending async operations for timing
        
        # Background metrics reporting (shared with sync version)
        self._metrics_reporting_config = None
        self._metrics_thread = None
        self._metrics_stop_event = threading.Event()
        
        logging.info("Initialized AsyncRedisUtils with host: %s:%d, db: %d", host, port, db)

    def _record_metric(self, operation: str, channel: str, start_time: float, end_time: float, 
                      success: bool, error_msg: str = None, message_key: str = None, 
                      message_size: int = None) -> None:
        """Record a performance metric for aggregation.
        
        Args:
            operation: Type of operation ('publish' or 'subscribe')
            channel: Redis channel name
            start_time: Operation start timestamp
            end_time: Operation end timestamp
            success: Whether operation was successful
            error_msg: Error message if operation failed
            message_key: Message key if available
            message_size: Message size in bytes if available
        """
        duration_ms = (end_time - start_time) * 1000  # Convert to milliseconds
        
        metric = {
            'timestamp': end_time,
            'operation': operation,
            'channel': channel,
            'duration_ms': duration_ms,
            'success': success,
            'error_msg': error_msg,
            'message_key': message_key,
            'message_size': message_size,
            'redis_host': f"{self.host}:{self.port}",
            'type': 'async'
        }
        
        # Protect with lock to coordinate with background reporter thread
        try:
            self._metrics_lock.acquire()
            self._metrics_log.append(metric)
        finally:
            self._metrics_lock.release()
        
        # Log summary for monitoring
        status = "SUCCESS" if success else "FAILED"
        logging.info(
            "Async Redis %s %s: channel=%s, duration=%.2fms, key=%s, size=%s%s",
            operation.upper(), status, channel, duration_ms, message_key or 'None', 
            message_size or 'Unknown', f", error={error_msg}" if error_msg else ""
        )

    def get_metrics(self, clear_after_read: bool = False) -> List[Dict]:
        """Get collected metrics for aggregation and reporting.
        
        Args:
            clear_after_read: Whether to clear metrics after reading
            
        Returns:
            List of metric dictionaries
        """
        try:
            self._metrics_lock.acquire()
            metrics = list(self._metrics_log)
            if clear_after_read:
                self._metrics_log.clear()
        finally:
            self._metrics_lock.release()
        
        return metrics

    def configure_metrics_reporting(self, 
                                   rpc_client,
                                   deployment_id: str = None,
                                   interval: int = 60,
                                   batch_size: int = 1000) -> None:
        """Configure background metrics reporting to backend API.
        
        Args:
            rpc_client: RPC client instance for API communication
            deployment_id: Deployment identifier for metrics context
            interval: Reporting interval in seconds (default: 60)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        self._metrics_reporting_config = {
            'rpc_client': rpc_client,
            'deployment_id': deployment_id,
            'interval': interval,
            'batch_size': batch_size,
            'enabled': True
        }
        
        # Start background reporting thread (reuse sync implementation)
        if not self._metrics_thread or not self._metrics_thread.is_alive():
            self._metrics_stop_event.clear()
            self._metrics_thread = threading.Thread(
                target=self._metrics_reporter_worker,
                daemon=True,
                name=f"async-redis-metrics-reporter-{id(self)}"
            )
            self._metrics_thread.start()
            logging.info("Started background async Redis metrics reporting thread")

    def _metrics_reporter_worker(self) -> None:
        """Background thread worker for sending metrics to backend API (async version)."""
        logging.info("Async Redis metrics reporter thread started")
        
        while not self._metrics_stop_event.is_set():
            try:
                if not self._metrics_reporting_config or not self._metrics_reporting_config.get('enabled'):
                    self._metrics_stop_event.wait(10)
                    continue
                
                interval = self._metrics_reporting_config.get('interval', 60)
                
                if self._metrics_stop_event.wait(interval):
                    break
                
                self._collect_and_send_metrics()
                
            except Exception as exc:
                logging.error(f"Error in async Redis metrics reporter thread: {exc}")
                self._metrics_stop_event.wait(30)
        
        logging.info("Async Redis metrics reporter thread stopped")

    def _collect_and_send_metrics(self) -> None:
        """Collect metrics and send them to the backend API (async version)."""
        try:
            raw_metrics = self.get_metrics(clear_after_read=True)
            
            if not raw_metrics:
                logging.debug("No new async Redis metrics to report")
                return
            
            aggregated_data = self._aggregate_metrics_for_api(raw_metrics)
            
            if aggregated_data.get('channel'):
                success = self._send_metrics_to_api(aggregated_data)
                if success:
                    logging.info(f"Successfully sent {len(raw_metrics)} async Redis metrics to backend API")
                else:
                    logging.warning("Failed to send async Redis metrics to backend API")
            else:
                logging.debug("No async channel-level metrics to report")
                
        except Exception as exc:
            logging.error(f"Error collecting and sending async Redis metrics: {exc}")

    def _aggregate_metrics_for_api(self, raw_metrics: List[Dict]) -> Dict:
        """Aggregate raw metrics into the API format expected by backend (async version)."""
        channel_stats = {}
        current_time = datetime.now(timezone.utc).isoformat()
        
        for metric in raw_metrics:
            channel = metric.get('channel', 'unknown')
            operation = metric.get('operation', 'unknown')
            success = metric.get('success', False)
            duration_ms = metric.get('duration_ms', 0)
            
            if channel in ['(timeout)', '(error)', 'unknown']:
                continue
            
            if channel not in channel_stats:
                channel_stats[channel] = {
                    'channel': channel,
                    'publishCount': 0,
                    'subscribeCount': 0,
                    'totalLatency': 0,
                    'latencies': [],
                    'avgLatency': 0,
                    'minlatency': float('inf'),
                    'maxlatency': 0
                }
            
            stats = channel_stats[channel]
            
            if operation == 'publish' and success:
                stats['publishCount'] += 1
            elif operation in ['subscribe', 'get_message'] and success:
                stats['subscribeCount'] += 1
            
            if success and duration_ms > 0:
                latency_ns = int(duration_ms * 1_000_000)
                stats['latencies'].append(latency_ns)
                stats['totalLatency'] += latency_ns
                stats['minlatency'] = min(stats['minlatency'], latency_ns)
                stats['maxlatency'] = max(stats['maxlatency'], latency_ns)
        
        for channel, stats in channel_stats.items():
            if stats['latencies']:
                stats['avgLatency'] = stats['totalLatency'] // len(stats['latencies'])
            else:
                stats['avgLatency'] = 0
                stats['minlatency'] = 0
            del stats['latencies']
        
        payload = {
            'channel': list(channel_stats.values()),
            'status': 'success',
            'host': self.host,
            'port': str(self.port),
            'createdAt': current_time,
            'updatedAt': current_time
        }

        return payload

    def _send_metrics_to_api(self, aggregated_metrics: Dict) -> bool:
        """Send aggregated metrics to backend API using RPC client (async version)."""
        try:
            rpc_client = self._metrics_reporting_config.get('rpc_client')
            if not rpc_client:
                logging.error("No RPC client configured for async Redis metrics reporting")
                return False
            
            response = rpc_client.post(
                path="/v1/monitoring/add_redis_metrics",
                payload=aggregated_metrics,
                timeout=30
            )
            
            if response and response.get("success"):
                logging.debug("Successfully sent async Redis metrics to backend API")
                return True
            else:
                error_msg = response.get('message', 'Unknown error') if response else 'No response'
                logging.error(f"Backend API rejected async Redis metrics: {error_msg}")
                return False
                
        except Exception as exc:
            logging.error(f"Error sending async Redis metrics to API: {exc}")
            return False

    def stop_metrics_reporting(self) -> None:
        """Stop the background metrics reporting thread (async version)."""
        if self._metrics_reporting_config:
            self._metrics_reporting_config['enabled'] = False
        
        if self._metrics_thread and self._metrics_thread.is_alive():
            logging.info("Stopping async Redis metrics reporting thread...")
            self._metrics_stop_event.set()
            self._metrics_thread.join(timeout=5)
            if self._metrics_thread.is_alive():
                logging.warning("Async Redis metrics reporting thread did not stop gracefully")
            else:
                logging.info("Async Redis metrics reporting thread stopped")

    async def setup_client(self, **kwargs) -> None:
        """Set up async Redis client connection.
        
        Args:
            **kwargs: Additional Redis client configuration options
            
        Raises:
            RedisConnectionError: If client initialization fails
        """
        client_config = {
            "host": self.host,
            "port": self.port,
            "db": self.db,
            "socket_timeout": self.connection_timeout,
            "socket_connect_timeout": self.connection_timeout,
            "retry_on_timeout": True,
            "health_check_interval": 30,
            "decode_responses": False,  # Keep bytes for compatibility
        }
        
        # Add authentication if configured
        if self.password:
            client_config["password"] = self.password
        if self.username:
            client_config["username"] = self.username
            
        # Add SSL configuration if enabled
        if self.ssl:
            client_config["ssl"] = True
            if not self.ssl_verify:
                client_config["ssl_cert_reqs"] = None
        
        # Override with any additional config
        client_config.update(kwargs)
        
        # Close existing client if any
        if self.client:
            try:
                await self.client.close()
            except Exception:
                pass  # Ignore errors during cleanup
                
        try:
            self.client = aioredis.Redis(**client_config)
            # Test connection
            await self.client.ping()
            logging.info("Successfully set up async Redis client")
        except Exception as exc:
            error_msg = f"Failed to initialize async Redis client: {str(exc)}"
            logging.error(error_msg)
            # Clean up on failure
            self.client = None
            raise RedisConnectionError(error_msg)

    async def setup_subscriber(self, **kwargs) -> None:
        """Set up async Redis pub/sub subscriber.

        Args:
            **kwargs: Additional pub/sub configuration options

        Raises:
            RedisConnectionError: If subscriber setup fails
        """
        if not self.client:
            await self.setup_client()
        
        try:
            self.pubsub = self.client.pubsub(**kwargs)
            logging.info("Successfully set up async Redis subscriber")
        except Exception as exc:
            error_msg = f"Failed to set up async Redis subscriber: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    def _serialize_value(self, value: Any) -> bytes:
        """Serialize message value to bytes.
        
        Args:
            value: Message value to serialize
            
        Returns:
            Serialized value as bytes
        """
        if isinstance(value, dict):
            return json.dumps(value).encode('utf-8')
        elif isinstance(value, str):
            return value.encode('utf-8')
        elif isinstance(value, bytes):
            return value
        else:
            return str(value).encode('utf-8')

    async def publish_message(
        self,
        channel: str,
        message: Union[dict, str, bytes, Any],
        timeout: float = 30.0,
    ) -> int:
        """Publish a message to a Redis channel asynchronously.
        
        Args:
            channel: Channel to publish to
            message: Message to publish (dict will be converted to JSON)
            timeout: Maximum time to wait for publish completion in seconds
            
        Returns:
            Number of subscribers that received the message
            
        Raises:
            RuntimeError: If client is not initialized
            ValueError: If channel or message is invalid
            RedisConnectionError: If message publication fails
        """
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first.")
        if not channel or message is None:
            raise ValueError("Channel and message must be provided")
            
        # Serialize message
        message_bytes = self._serialize_value(message)
        message_size = len(message_bytes) if message_bytes else 0
        
        start_time = time.time()
        try:
            # Redis publish returns the number of subscribers
            result = await self.client.publish(channel, message_bytes)
            end_time = time.time()
            
            # Record successful publish metrics
            self._record_metric(
                operation="publish",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=None,
                message_size=message_size
            )
            
            logging.debug("Successfully published async message to channel: %s, subscribers: %d", channel, result)
            return result
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to publish async message: {str(exc)}"
            logging.error(error_msg)
            
            # Record failed publish metrics
            self._record_metric(
                operation="publish",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=message_size
            )
            raise RedisConnectionError(error_msg)

    async def subscribe_to_channel(
        self, 
        channel: str,
        callback: Optional[Callable] = None
    ) -> None:
        """Subscribe to a Redis channel asynchronously.

        Args:
            channel: Channel to subscribe to
            callback: Optional callback function for message handling

        Raises:
            RuntimeError: If subscriber is not set up
            RedisConnectionError: If subscription fails
            ValueError: If channel is empty
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first")
        if not channel:
            raise ValueError("Channel must be provided")

        start_time = time.time()
        try:
            await self.pubsub.subscribe(channel)
            self._subscribed_channels.add(channel)
            if callback:
                self._subscription_callbacks[channel] = callback
            
            end_time = time.time()
            
            # Record successful subscription metrics
            self._record_metric(
                operation="subscribe",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=None,
                message_size=None
            )
            
            logging.info("Successfully subscribed to async channel: %s", channel)
            
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to subscribe to async channel: {str(exc)}"
            logging.error(error_msg)
            
            # Record failed subscription metrics
            self._record_metric(
                operation="subscribe",
                channel=channel,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None
            )
            raise RedisConnectionError(error_msg)

    async def unsubscribe_from_channel(self, channel: str) -> None:
        """Unsubscribe from a Redis channel asynchronously.

        Args:
            channel: Channel to unsubscribe from

        Raises:
            RuntimeError: If subscriber is not set up
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first")

        try:
            await self.pubsub.unsubscribe(channel)
            self._subscribed_channels.discard(channel)
            self._subscription_callbacks.pop(channel, None)
            logging.info("Successfully unsubscribed from async channel: %s", channel)
        except Exception as exc:
            logging.error("Failed to unsubscribe from async channel %s: %s", channel, str(exc))

    def _parse_message_value(self, value: bytes) -> Any:
        """Parse message value from bytes.
        
        Args:
            value: Message value in bytes
            
        Returns:
            Parsed value or original bytes if parsing fails
        """
        if not value:
            return None
            
        try:
            return json.loads(value.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return value

    async def get_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Get a single message from subscribed channels asynchronously.
        
        Args:
            timeout: Maximum time to wait for message in seconds
            
        Returns:
            Message dictionary if available, None if no message received
            
        Raises:
            RuntimeError: If subscriber is not initialized
            RedisConnectionError: If message retrieval fails
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first.")
        
        start_time = time.time()
        try:
            # Use get_message with timeout to avoid blocking indefinitely
            try:
                message = await asyncio.wait_for(self.pubsub.get_message(ignore_subscribe_messages=False), timeout=timeout)
                end_time = time.time()
                
                if message is None:
                    # Record timeout as successful operation with no message
                    self._record_metric(
                        operation="get_message",
                        channel="(timeout)",
                        start_time=start_time,
                        end_time=end_time,
                        success=True,
                        error_msg=None,
                        message_key=None,
                        message_size=None
                    )
                    return None
                
                # Skip subscription confirmation messages
                if message['type'] in ['subscribe', 'unsubscribe', 'psubscribe', 'punsubscribe']:
                    return message
                
                channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else str(message['channel'])
                message_data = message.get('data', b'')
                message_size = len(message_data) if message_data else 0
                
                # Parse the message data
                parsed_data = self._parse_message_value(message_data)
                
                # Record successful message retrieval metrics
                self._record_metric(
                    operation="get_message",
                    channel=channel,
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=message_size
                )
                
                # Execute callback if registered
                if channel in self._subscription_callbacks:
                    try:
                        if asyncio.iscoroutinefunction(self._subscription_callbacks[channel]):
                            await self._subscription_callbacks[channel](message)
                        else:
                            self._subscription_callbacks[channel](message)
                    except Exception as callback_exc:
                        logging.error("Error in async message callback for channel %s: %s", channel, str(callback_exc))
                
                return {
                    "type": message['type'],
                    "channel": channel,
                    "data": parsed_data,
                    "pattern": message.get('pattern'),
                    "raw_data": message_data
                }
            except asyncio.TimeoutError:
                end_time = time.time()
                # Record timeout as successful operation with no message
                self._record_metric(
                    operation="get_message",
                    channel="(timeout)",
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=None
                )
                return None
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to get async message: {str(exc)}"
            logging.error(error_msg)
            
            # Record error metrics
            self._record_metric(
                operation="get_message",
                channel="(error)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None
            )
            raise RedisConnectionError(error_msg)

    async def listen_for_messages(self, callback: Optional[Callable] = None) -> None:
        """Listen for messages on subscribed channels asynchronously (blocking).

        Args:
            callback: Optional global callback function for all messages

        Raises:
            RuntimeError: If subscriber is not set up
            RedisConnectionError: If listening fails
        """
        if not self.pubsub:
            raise RuntimeError("Redis subscriber not initialized. Call setup_subscriber() first")

        try:
            logging.info("Starting to listen for async Redis messages...")
            async for message in self.pubsub.listen():
                if message['type'] == 'message':
                    channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else str(message['channel'])
                    
                    # Execute channel-specific callback
                    if channel in self._subscription_callbacks:
                        try:
                            if asyncio.iscoroutinefunction(self._subscription_callbacks[channel]):
                                await self._subscription_callbacks[channel](message)
                            else:
                                self._subscription_callbacks[channel](message)
                        except Exception as callback_exc:
                            logging.error("Error in async channel callback for %s: %s", channel, str(callback_exc))
                    
                    # Execute global callback
                    if callback:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(message)
                            else:
                                callback(message)
                        except Exception as callback_exc:
                            logging.error("Error in async global callback: %s", str(callback_exc))
                            
        except Exception as exc:
            error_msg = f"Error listening for async messages: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    async def close(self) -> None:
        """Close async Redis client and subscriber connections."""
        errors = []
        
        # Stop background metrics reporting first
        try:
            self.stop_metrics_reporting()
        except Exception as exc:
            error_msg = f"Error stopping async Redis metrics reporting: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)
        
        # Check if event loop is still running
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                logging.warning("Event loop is closed, skipping async Redis cleanup")
                self.client = None
                self.pubsub = None
                return
        except RuntimeError:
            logging.warning("No running event loop, skipping async Redis cleanup")
            self.client = None
            self.pubsub = None
            return
        
        # Close pubsub connection
        if self.pubsub:
            try:
                logging.debug("Closing async Redis pubsub...")
                # Unsubscribe from all channels
                if self._subscribed_channels:
                    try:
                        await self.pubsub.unsubscribe(*self._subscribed_channels)
                    except Exception as exc:
                        logging.warning("Error unsubscribing from async channels: %s", str(exc))
                
                await self.pubsub.close()
                self.pubsub = None
                self._subscribed_channels.clear()
                self._subscription_callbacks.clear()
                logging.debug("Async Redis pubsub closed successfully")
            except Exception as exc:
                error_msg = f"Error closing async Redis pubsub: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.pubsub = None
                
        # Close client connection
        if self.client:
            try:
                logging.debug("Closing async Redis client...")
                await self.client.close()
                self.client = None
                logging.debug("Async Redis client closed successfully")
            except Exception as exc:
                error_msg = f"Error closing async Redis client: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.client = None
                
        if not errors:
            logging.info("Closed async Redis connections successfully")
        else:
            # Don't raise exception during cleanup, just log errors
            logging.error("Errors occurred during async Redis close: %s", "; ".join(errors))


class MatriceRedisDeployment:
    """Class for managing Redis deployments for Matrice streaming API."""

    def __init__(
        self, 
        session, 
        service_id: str, 
        type: str, 
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        username: Optional[str] = None,
        db: int = 0,
        ssl: bool = False,
        ssl_verify: bool = True,
        enable_metrics: bool = True,
        metrics_interval: int = 60
    ) -> None:
        """Initialize Redis deployment with deployment ID.

        Args:
            session: Session object for authentication and RPC
            service_id: ID of the deployment
            type: Type of deployment ("client" or "server")
            host: Redis server hostname or IP address
            port: Redis server port
            password: Password for Redis authentication
            username: Username for Redis authentication (Redis 6.0+)
            db: Database number to connect to
            ssl: Whether to use SSL/TLS connection
            ssl_verify: Whether to verify SSL certificates
            enable_metrics: Whether to auto-enable metrics reporting (default: True)
            metrics_interval: Metrics reporting interval in seconds (default: 60)
        Raises:
            ValueError: If type is not "client" or "server"
        """
        self.session = session
        self.rpc = session.rpc
        self.service_id = service_id
        self.type = type
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.db = db
        self.ssl = ssl
        self.ssl_verify = ssl_verify

        self.setup_success = True
        self.request_channel = f"{service_id}_requests"
        self.result_channel = f"{service_id}_results"
        self.publishing_channel = None
        self.subscribing_channel = None

        # Initialize Redis utilities as None - create as needed
        self.sync_redis = None
        self.async_redis = None
        
        # Initialize metrics configuration
        self._metrics_config = None

        # Configure channels based on deployment type
        if self.type == "client":
            self.publishing_channel = self.request_channel
            self.subscribing_channel = self.result_channel
        elif self.type == "server":
            self.publishing_channel = self.result_channel
            self.subscribing_channel = self.request_channel
        else:
            raise ValueError("Invalid type: must be 'client' or 'server'")

        logging.info(
            "Initialized MatriceRedisDeployment: deployment_id=%s, type=%s, host=%s:%d",
            service_id, type, host, port
        )

        # Auto-enable metrics reporting by default
        if enable_metrics:
            self.configure_metrics_reporting(interval=metrics_interval)

    def check_setup_success(self) -> bool:
        """Check if the Redis setup is successful.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        return self.setup_success

    def get_all_metrics(self) -> Dict:
        """Get aggregated metrics from all Redis utilities.
        
        Returns:
            Dict: Combined metrics from sync and async Redis utilities
        """
        all_metrics = {
            'sync_metrics': [],
            'async_metrics': [],
            'deployment_info': {
                'type': self.type,
                'setup_success': self.setup_success,
                'publishing_channel': getattr(self, 'publishing_channel', None),
                'subscribing_channel': getattr(self, 'subscribing_channel', None)
            }
        }
        
        # Get sync metrics
        if self.sync_redis:
            try:
                all_metrics['sync_metrics'] = self.sync_redis.get_metrics()
            except Exception as exc:
                logging.warning("Error getting sync Redis metrics: %s", str(exc))
        
        # Get async metrics
        if self.async_redis:
            try:
                all_metrics['async_metrics'] = self.async_redis.get_metrics()
            except Exception as exc:
                logging.warning("Error getting async Redis metrics: %s", str(exc))
        
        return all_metrics

    def get_metrics_summary(self) -> Dict:
        """Get a summary of metrics from all Redis utilities.
        
        Returns:
            Dict: Summarized metrics with counts and statistics
        """
        all_metrics = self.get_all_metrics()
        summary = {
            'sync_summary': {
                'total_operations': len(all_metrics['sync_metrics']),
                'success_count': 0,
                'error_count': 0,
                'avg_latency': 0.0
            },
            'async_summary': {
                'total_operations': len(all_metrics['async_metrics']),
                'success_count': 0,
                'error_count': 0,
                'avg_latency': 0.0
            },
            'deployment_info': all_metrics['deployment_info']
        }
        
        # Calculate sync summary
        if all_metrics['sync_metrics']:
            sync_latencies = []
            for metric in all_metrics['sync_metrics']:
                if metric.get('success'):
                    summary['sync_summary']['success_count'] += 1
                    if 'duration_ms' in metric:
                        sync_latencies.append(metric['duration_ms'])
                else:
                    summary['sync_summary']['error_count'] += 1
            
            if sync_latencies:
                summary['sync_summary']['avg_latency'] = sum(sync_latencies) / len(sync_latencies)
        
        # Calculate async summary
        if all_metrics['async_metrics']:
            async_latencies = []
            for metric in all_metrics['async_metrics']:
                if metric.get('success'):
                    summary['async_summary']['success_count'] += 1
                    if 'duration_ms' in metric:
                        async_latencies.append(metric['duration_ms'])
                else:
                    summary['async_summary']['error_count'] += 1
            
            if async_latencies:
                summary['async_summary']['avg_latency'] = sum(async_latencies) / len(async_latencies)
        
        return summary

    def refresh(self):
        """Refresh the Redis client and subscriber connections."""
        logging.info("Refreshing Redis connections")
        # Clear existing connections to force recreation
        if self.sync_redis:
            try:
                self.sync_redis.close()
            except Exception as exc:
                logging.warning("Error closing sync Redis during refresh: %s", str(exc))
            self.sync_redis = None
            
        if self.async_redis:
            try:
                # Note: close() is async but we can't await here
                logging.warning("Async Redis connections will be recreated on next use")
            except Exception as exc:
                logging.warning("Error during async Redis refresh: %s", str(exc))
            self.async_redis = None
            
        logging.info("Redis connections will be refreshed on next use")

    def _ensure_sync_client(self):
        """Ensure sync Redis client is set up."""
        if not self.sync_redis:
            self.sync_redis = RedisUtils(
                host=self.host,
                port=self.port,
                password=self.password,
                username=self.username,
                db=self.db,
                ssl=self.ssl,
                ssl_verify=self.ssl_verify
            )
            # Configure metrics reporting if enabled
            if self._metrics_config and self._metrics_config.get('enabled'):
                try:
                    self.sync_redis.configure_metrics_reporting(
                        rpc_client=self.session.rpc,
                        deployment_id=self.service_id,
                        interval=self._metrics_config.get('interval', 60),
                        batch_size=self._metrics_config.get('batch_size', 1000)
                    )
                except Exception as exc:
                    logging.warning(f"Failed to configure sync Redis metrics reporting: {exc}")
        
        try:
            if not self.sync_redis.client:
                self.sync_redis.setup_client()
            return True
        except Exception as exc:
            logging.error("Failed to set up sync Redis client: %s", str(exc))
            return False

    def _ensure_sync_subscriber(self):
        """Ensure sync Redis subscriber is set up."""
        if not self._ensure_sync_client():
            return False
        
        try:
            if not self.sync_redis.pubsub:
                self.sync_redis.setup_subscriber()
                self.sync_redis.subscribe_to_channel(self.subscribing_channel)
            return True
        except Exception as exc:
            logging.error("Failed to set up sync Redis subscriber: %s", str(exc))
            return False

    async def _ensure_async_client(self):
        """Ensure async Redis client is set up.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        if not self.async_redis:
            self.async_redis = AsyncRedisUtils(
                host=self.host,
                port=self.port,
                password=self.password,
                username=self.username,
                db=self.db,
                ssl=self.ssl,
                ssl_verify=self.ssl_verify
            )
            # Configure metrics reporting if enabled
            if self._metrics_config and self._metrics_config.get('enabled'):
                try:
                    self.async_redis.configure_metrics_reporting(
                        rpc_client=self.session.rpc,
                        deployment_id=self.service_id,
                        interval=self._metrics_config.get('interval', 60),
                        batch_size=self._metrics_config.get('batch_size', 1000)
                    )
                except Exception as exc:
                    logging.warning(f"Failed to configure async Redis metrics reporting: {exc}")
        
        try:
            if not self.async_redis.client:
                await self.async_redis.setup_client()
            return True
        except Exception as exc:
            logging.error("Failed to set up async Redis client: %s", str(exc))
            return False

    async def _ensure_async_subscriber(self):
        """Ensure async Redis subscriber is set up.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        if not await self._ensure_async_client():
            return False
        
        try:
            if not self.async_redis.pubsub:
                await self.async_redis.setup_subscriber()
                await self.async_redis.subscribe_to_channel(self.subscribing_channel)
            return True
        except Exception as exc:
            logging.error("Failed to set up async Redis subscriber: %s", str(exc))
            return False

    def _parse_message(self, result: dict) -> dict:
        """Handle message parsing for consistency."""
        if not result:
            return result
        # Redis messages are already parsed by the utility classes
        return result

    def publish_message(self, message: dict, timeout: float = 60.0) -> int:
        """Publish a message to Redis.

        Args:
            message: Message to publish
            timeout: Maximum time to wait for message publication in seconds
            
        Returns:
            Number of subscribers that received the message
            
        Raises:
            RuntimeError: If client is not initialized
            ValueError: If message is invalid
            RedisConnectionError: If message publication fails
        """
        if not self._ensure_sync_client():
            raise RuntimeError("Failed to set up Redis client")
        return self.sync_redis.publish_message(self.publishing_channel, message, timeout=timeout)

    def get_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Get a message from Redis.

        Args:
            timeout: Maximum time to wait for message in seconds
            
        Returns:
            Message dictionary if available, None if no message received
            
        Raises:
            RuntimeError: If subscriber is not initialized
            RedisConnectionError: If message retrieval fails
        """
        if not self._ensure_sync_subscriber():
            logging.warning("Redis subscriber setup unsuccessful, returning None for get request")
            return None

        result = self.sync_redis.get_message(timeout)
        result = self._parse_message(result)
        return result

    async def async_publish_message(self, message: dict, timeout: float = 60.0) -> int:
        """Publish a message to Redis asynchronously.

        Args:
            message: Message to publish
            timeout: Maximum time to wait for message publication in seconds
            
        Returns:
            Number of subscribers that received the message
            
        Raises:
            RuntimeError: If client is not initialized
            ValueError: If message is invalid
            RedisConnectionError: If message publication fails
        """
        if not await self._ensure_async_client():
            raise RuntimeError("Failed to set up async Redis client")
        return await self.async_redis.publish_message(self.publishing_channel, message, timeout=timeout)

    async def async_get_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Get a message from Redis asynchronously.

        Args:
            timeout: Maximum time to wait for message in seconds
            
        Returns:
            Message dictionary if available, None if no message received
            
        Raises:
            RuntimeError: If subscriber is not initialized
            RedisConnectionError: If message retrieval fails
        """
        try:
            if not await self._ensure_async_subscriber():
                logging.warning("Async Redis subscriber setup unsuccessful, returning None for get request")
                return None

            result = await self.async_redis.get_message(timeout)
            result = self._parse_message(result)
            return result
        except RuntimeError as exc:
            logging.error("Runtime error in async_get_message: %s", str(exc))
            return None
        except Exception as exc:
            logging.error("Unexpected error in async_get_message: %s", str(exc))
            return None

    def configure_metrics_reporting(self, 
                                   interval: int = 60,
                                   batch_size: int = 1000) -> None:
        """Configure background metrics reporting for both sync and async Redis utilities.
        
        This method enables automatic metrics collection and reporting to the backend API
        for all Redis operations performed through this deployment.
        
        Args:
            interval: Reporting interval in seconds (default: 60)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        try:
            # Configure metrics reporting for sync Redis utils if they exist
            if self.sync_redis:
                self.sync_redis.configure_metrics_reporting(
                    rpc_client=self.session.rpc,
                    deployment_id=self.service_id,
                    interval=interval,
                    batch_size=batch_size
                )
                logging.info(f"Configured sync Redis metrics reporting for deployment {self.service_id}")
            
            # Configure metrics reporting for async Redis utils if they exist
            if self.async_redis:
                self.async_redis.configure_metrics_reporting(
                    rpc_client=self.session.rpc,
                    deployment_id=self.service_id,
                    interval=interval,
                    batch_size=batch_size
                )
                logging.info(f"Configured async Redis metrics reporting for deployment {self.service_id}")
            
            # If no Redis utils exist yet, they will be configured when first created
            if not self.sync_redis and not self.async_redis:
                logging.info(f"Metrics reporting will be configured when Redis connections are established for deployment {self.service_id}")
                
            # Store configuration for future Redis utils creation
            self._metrics_config = {
                'interval': interval,
                'batch_size': batch_size,
                'enabled': True
            }
            
        except Exception as exc:
            logging.error(f"Error configuring Redis metrics reporting for deployment {self.service_id}: {exc}")

    async def close(self) -> None:
        """Close Redis client and subscriber connections.
        
        This method gracefully closes all Redis connections without raising exceptions
        to ensure proper cleanup during shutdown.
        """
        errors = []

        # Close sync Redis connections
        if self.sync_redis:
            try:
                logging.debug("Closing sync Redis connections...")
                self.sync_redis.close()
                self.sync_redis = None
                logging.debug("Sync Redis connections closed successfully")
            except Exception as exc:
                error_msg = f"Error closing sync Redis connections: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.sync_redis = None

        # Close async Redis connections
        if self.async_redis:
            try:
                logging.debug("Closing async Redis connections...")
                await self.async_redis.close()
                self.async_redis = None
                logging.debug("Async Redis connections closed successfully")
            except Exception as exc:
                error_msg = f"Error closing async Redis connections: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.async_redis = None

        if not errors:
            logging.info("Closed Redis connections successfully")
        else:
            # Log errors but don't raise exception during cleanup
            logging.error("Errors occurred during Redis close: %s", "; ".join(errors))