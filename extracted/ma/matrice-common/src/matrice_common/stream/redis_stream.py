"""Module providing synchronous and asynchronous Redis Streams utilities."""
from __future__ import annotations

import base64
import json
import logging
import time
import threading
from collections import deque
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple, Union, Any, Callable, Deque
import redis
import asyncio
import redis.asyncio as redis_asyncio
from redis.exceptions import ConnectionError as RedisConnectionError, ResponseError


class RedisUtils:
    """Utility class for synchronous Redis operations."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        username: Optional[str] = None,
        db: int = 0,
        connection_timeout: int = 30,
        pool_max_connections: int = 50,
        enable_batching: bool = True,
        batch_size: int = 10,
        batch_timeout: float = 0.01,
        enable_shm_batching: bool = False,
        stream_maxlen: Optional[int] = None
    ) -> None:
        """Initialize Redis utils with connection parameters.

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
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.db = db
        self.connection_timeout = connection_timeout
        self.pool_max_connections = pool_max_connections
        self.enable_batching = enable_batching
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self._initial_batch_size = batch_size  # Store initial for reset
        self.enable_shm_batching = enable_shm_batching
        self.stream_maxlen = stream_maxlen

        self.client: Any = None
        self.connection_pool: Any = None
        self._streams: Set[str] = set()  # Set of stream names we're working with
        self._consumer_groups: Dict[str, str] = {}  # Map of stream -> consumer group
        self._consumer_names: Dict[str, str] = {}  # Map of stream -> consumer name

        # Batching support
        self._batch_buffer: Dict[str, Any] = {}  # stream_name -> list of (fields, message_key, start_time)
        self._batch_lock = threading.Lock()
        self._last_flush_time: Dict[str, float] = {}  # stream_name -> last flush timestamp
        self._batch_thread: Optional[threading.Thread] = None
        self._batch_stop_event = threading.Event()

        # Dynamic batching controller for adaptive throughput
        self._throughput_samples: Deque[float] = deque(maxlen=10)  # Last 10 throughput samples
        self._last_throughput_check = time.time()
        self._message_count_since_check = 0
        self._throughput_check_interval = 5.0  # Check every 5 seconds

        # Metrics collection for performance monitoring
        self._metrics_lock = threading.Lock()
        self._metrics_log: Deque[Dict[str, Any]] = deque(maxlen=10000)  # Keep last 10000 metrics entries
        self._pending_operations: Dict[str, Any] = {}  # Track pending operations for timing

        # Background metrics reporting
        self._metrics_reporting_config: Optional[Dict[str, Any]] = None
        self._metrics_thread: Optional[threading.Thread] = None
        self._metrics_stop_event = threading.Event()
        self._last_metrics_reset = time.time()
        
        logging.info(
            "Initialized RedisUtils with host: %s:%d, db: %d",
            host, port, db
        )

    def _record_metric(self, operation: str, stream: str, start_time: float, end_time: float, 
                      success: bool, error_msg: Optional[str] = None, message_key: Optional[str] = None, 
                      message_size: Optional[int] = None) -> None:
        """Record a performance metric for aggregation.
        
        Args:
            operation: Type of operation ('add' or 'read')
            stream: Redis stream name
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
            'stream': stream,
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
        if success:
            status = "SUCCESS"
            logging.debug(
                "Redis %s %s: stream=%s, duration=%.2fms, key=%s, size=%s%s",
                operation.upper(), status, stream, duration_ms, message_key or 'None', 
                message_size or 'Unknown', f", error={error_msg}" if error_msg else ""
            )
        else:
            status = "FAILED"
            logging.warning(
                "Redis %s %s: stream=%s, duration=%.2fms, key=%s, size=%s%s",
                operation.upper(), status, stream, duration_ms, message_key or 'None', 
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

    def _update_dynamic_batch_size(self) -> None:
        """Dynamically adjust batch size based on throughput to optimize for varying loads.

        Adaptive batching strategy:
        - Low throughput (< 1K msg/sec): batch_size = 50 (responsive, low latency)
        - Medium throughput (1K-10K msg/sec): batch_size = 200 (balanced)
        - High throughput (10K-50K msg/sec): batch_size = 500 (efficient batching)
        - Very high throughput (> 50K msg/sec): batch_size = 1000 (maximum efficiency)

        This prevents slow cameras from experiencing high latency with large batches,
        while enabling high throughput when processing many cameras.
        """
        current_time = time.time()
        elapsed = current_time - self._last_throughput_check

        # Check throughput every interval
        if elapsed >= self._throughput_check_interval:
            # Calculate messages per second
            throughput = self._message_count_since_check / elapsed if elapsed > 0 else 0
            self._throughput_samples.append(throughput)

            # Calculate average throughput from recent samples (smooth out spikes)
            avg_throughput = sum(self._throughput_samples) / len(self._throughput_samples) if self._throughput_samples else 0

            # Determine optimal batch size based on throughput
            old_batch_size = self.batch_size
            if avg_throughput < 1000:
                self.batch_size = 50
            elif avg_throughput < 10000:
                self.batch_size = 200
            elif avg_throughput < 50000:
                self.batch_size = 500
            else:
                self.batch_size = 1000

            # Log batch size changes
            if self.batch_size != old_batch_size:
                logging.info(
                    "Dynamic batching: adjusted batch_size from %d to %d "
                    "(throughput: %.1f msg/sec, avg: %.1f msg/sec)",
                    old_batch_size, self.batch_size, throughput, avg_throughput
                )

            # Reset counters
            self._message_count_since_check = 0
            self._last_throughput_check = current_time

    def configure_metrics_reporting(self, 
                                   rpc_client,
                                   deployment_id: Optional[str] = None,
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
            t = threading.Thread(
                target=self._metrics_reporter_worker,
                daemon=True,
                name=f"redis-metrics-reporter-{id(self)}"
            )
            self._metrics_thread = t
            t.start()
            logging.info("Started background Redis metrics reporting thread")

    def _metrics_reporter_worker(self) -> None:
        """Background thread worker for sending metrics to backend API."""
        logging.info("Redis metrics reporter thread started")
        
        while not self._metrics_stop_event.is_set():
            try:
                cfg: Dict[str, Any] = self._metrics_reporting_config or {}
                if not cfg or not cfg.get('enabled'):
                    self._metrics_stop_event.wait(10)  # Check every 10 seconds if disabled
                    continue
                
                interval = cfg.get('interval', 60)
                
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
            
            # Aggregate metrics by stream for API format
            aggregated_data = self._aggregate_metrics_for_api(raw_metrics)
            
            if aggregated_data.get('stream'):
                # Send to backend API
                success = self._send_metrics_to_api(aggregated_data)
                if success:
                    logging.info(f"Successfully sent {len(raw_metrics)} Redis metrics to backend API")
                    logging.info(f"Redis Metrics: {raw_metrics}")
                else:
                    logging.warning("Failed to send Redis metrics to backend API")
            else:
                logging.debug("No stream-level metrics to report")
                
        except Exception as exc:
            logging.error(f"Error collecting and sending Redis metrics: {exc}")

    def _aggregate_metrics_for_api(self, raw_metrics: List[Dict]) -> Dict:
        """Aggregate raw metrics into the API format expected by backend.
        
        Args:
            raw_metrics: List of raw metric dictionaries
            
        Returns:
            Aggregated metrics in API format
        """
        # Group metrics by stream
        stream_stats = {}
        current_time = datetime.now(timezone.utc).isoformat()
        
        for metric in raw_metrics:
            stream = metric.get('stream', 'unknown')
            operation = metric.get('operation', 'unknown')
            success = metric.get('success', False)
            duration_ms = metric.get('duration_ms', 0)
            
            # Skip timeout and error entries for aggregation
            if stream in ['(timeout)', '(error)', 'unknown']:
                continue
            
            if stream not in stream_stats:
                stream_stats[stream] = {
                    'stream': stream,
                    'addCount': 0,
                    'readCount': 0,
                    'totalLatency': 0,
                    'latencies': [],  # Temporary for calculations
                    'avgLatency': 0,
                    'minlatency': float('inf'),
                    'maxlatency': 0
                }
            
            stats = stream_stats[stream]
            
            # Count operations by type
            if operation == 'add' and success:
                stats['addCount'] += 1
            elif operation in ['read', 'get_message'] and success:
                stats['readCount'] += 1
            
            # Track latencies (convert ms to nanoseconds for API compatibility)
            if success and duration_ms > 0:
                latency_ns = int(duration_ms * 1_000_000)  # Convert ms to ns
                stats['latencies'].append(latency_ns)
                stats['totalLatency'] += latency_ns
                stats['minlatency'] = min(stats['minlatency'], latency_ns)
                stats['maxlatency'] = max(stats['maxlatency'], latency_ns)
        
        # Calculate averages and clean up
        for stream, stats in stream_stats.items():
            if stats['latencies']:
                stats['avgLatency'] = stats['totalLatency'] // len(stats['latencies'])
            else:
                stats['avgLatency'] = 0
                stats['minlatency'] = 0
            
            # Remove temporary latencies list
            del stats['latencies']
        
        # Format for API
        api_payload = {
            'stream': list(stream_stats.values()),
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
            cfg: Dict[str, Any] = self._metrics_reporting_config or {}
            rpc_client = cfg.get('rpc_client')
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
        """Set up Redis client connection with connection pooling.

        Args:
            **kwargs: Additional Redis client configuration options

        Raises:
            RedisConnectionError: If client initialization fails
        """
        pool_config = {
            "host": self.host,
            "port": self.port,
            "db": self.db,
            "socket_timeout": self.connection_timeout,
            "socket_connect_timeout": self.connection_timeout,
            "retry_on_timeout": True,
            "health_check_interval": 30,
            "decode_responses": False,  # Keep bytes for compatibility
            "max_connections": self.pool_max_connections,
        }

        # Add authentication if configured
        if self.password:
            pool_config["password"] = self.password
        if self.username:
            pool_config["username"] = self.username

        # Override with any additional config
        pool_config.update(kwargs)

        try:
            # Create connection pool
            self.connection_pool = redis.ConnectionPool(**pool_config)  # type: ignore[arg-type]
            self.client = redis.Redis(connection_pool=self.connection_pool)

            # Test connection
            self.client.ping()
            logging.info("Successfully set up Redis client with connection pool (max_connections=%d)",
                        self.pool_max_connections)

            # Start batching thread if enabled
            if self.enable_batching and not self._batch_thread:
                self._batch_thread = threading.Thread(
                    target=self._batch_flusher,
                    daemon=True,
                    name="RedisUtils-BatchFlusher"
                )
                self._batch_thread.start()
                logging.info("Started Redis batching thread (batch_size=%d, timeout=%.2fs)",
                           self.batch_size, self.batch_timeout)
        except Exception as exc:
            error_msg = f"Failed to initialize Redis client: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    def _verify_stream_setup(self, stream_name: str, consumer_group: str, max_retries: int = 3) -> None:
        """Verify stream and consumer group exist after setup.

        This method prevents race conditions by ensuring the stream and consumer group
        are actually created before returning from setup_stream(). If verification fails,
        it attempts to recreate them.

        Args:
            stream_name: Name of the Redis stream
            consumer_group: Name of the consumer group
            max_retries: Maximum verification attempts

        Raises:
            RedisConnectionError: If verification fails after retries
        """
        stream_name = self._safe_decode(stream_name)
        consumer_group = self._safe_decode(consumer_group)

        for attempt in range(max_retries):
            try:
                # Check if stream exists using XINFO GROUPS
                groups = self.client.xinfo_groups(stream_name)
                group_names = []
                for g in groups:
                    name = g.get('name', g.get(b'name', b''))
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    group_names.append(name)

                if consumer_group in group_names:
                    logging.debug(f"Verified consumer group '{consumer_group}' exists on stream '{stream_name}'")
                    return

                # Group not found, try to create it
                logging.warning(f"Consumer group '{consumer_group}' not found on attempt {attempt + 1}, recreating...")
                try:
                    self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
                except ResponseError as create_err:
                    if "BUSYGROUP" not in str(create_err):
                        raise

            except Exception as e:
                error_str = str(e).lower()
                if "nogroup" in error_str or "no such key" in error_str or "doesn't exist" in error_str:
                    # Stream doesn't exist, create it with xgroup_create + mkstream=True
                    logging.warning(f"Stream '{stream_name}' doesn't exist on attempt {attempt + 1}, creating...")
                    try:
                        self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
                        logging.info(f"Created stream '{stream_name}' with consumer group '{consumer_group}'")
                        # Successfully created, continue to verify on next iteration
                    except ResponseError as create_err:
                        if "BUSYGROUP" not in str(create_err):
                            if attempt == max_retries - 1:
                                raise RedisConnectionError(
                                    f"Failed to verify/create stream setup after {max_retries} attempts: {create_err}"
                                )
                elif attempt == max_retries - 1:
                    raise RedisConnectionError(
                        f"Failed to verify stream setup after {max_retries} attempts: {e}"
                    )

            time.sleep(0.1 * (attempt + 1))  # Small backoff between retries

        # Final verification after all retries
        try:
            groups = self.client.xinfo_groups(stream_name)
            group_names = []
            for g in groups:
                name = g.get('name', g.get(b'name', b''))
                if isinstance(name, bytes):
                    name = name.decode('utf-8')
                group_names.append(name)

            if consumer_group in group_names:
                logging.info(f"Stream '{stream_name}' with consumer group '{consumer_group}' verified after retries")
                return
        except Exception:
            pass

        raise RedisConnectionError(
            f"Failed to verify consumer group '{consumer_group}' on stream '{stream_name}' after {max_retries} attempts"
        )

    def setup_stream(self, stream_name: str, consumer_group: str, consumer_name: Optional[str] = None) -> None:
        """Set up Redis stream with consumer group.

        Args:
            stream_name: Name of the Redis stream
            consumer_group: Name of the consumer group
            consumer_name: Name of the consumer (defaults to hostname-timestamp)

        Raises:
            RedisConnectionError: If stream setup fails
        """
        if not self.client:
            self.setup_client()
        
        try:
            # Ensure all parameters are strings, not bytes
            stream_name = self._safe_decode(stream_name)
            consumer_group = self._safe_decode(consumer_group)
            
            # Generate default consumer name if not provided
            if not consumer_name:
                consumer_name = f"consumer-{int(time.time())}-{threading.current_thread().ident}"
            else:
                consumer_name = self._safe_decode(consumer_name)
            
            # Create consumer group if it doesn't exist
            try:
                self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
                logging.info(f"Created consumer group '{consumer_group}' for stream '{stream_name}'")
            except ResponseError as e:
                if "BUSYGROUP" in str(e):
                    logging.debug(f"Consumer group '{consumer_group}' already exists for stream '{stream_name}'")
                else:
                    raise

            # Verify stream and consumer group were actually created (prevents race conditions)
            self._verify_stream_setup(stream_name, consumer_group)

            # Store stream configuration (ensure all are strings)
            self._streams.add(stream_name)  # type: ignore[arg-type]
            self._consumer_groups[stream_name] = consumer_group  # type: ignore[assignment]
            self._consumer_names[stream_name] = consumer_name  # type: ignore[assignment]

            logging.info(f"Successfully set up Redis stream '{stream_name}' with consumer group '{consumer_group}'")
        except Exception as exc:
            error_msg = f"Failed to set up Redis stream: {str(exc)}"
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

    def _safe_decode(self, value: Union[str, bytes], keep_binary: bool = True) -> Any:
        """Safely decode bytes to string, handling both str and bytes input.

        Args:
            value: Value to decode (str or bytes)
            keep_binary: If True, return bytes as-is if UTF-8 decoding fails

        Returns:
            Decoded string or original bytes if decoding fails and keep_binary=True
        """
        if isinstance(value, bytes):
            if keep_binary:
                try:
                    return value.decode('utf-8')
                except UnicodeDecodeError:
                    # Return bytes as-is for binary data (images, etc.)
                    return value
            else:
                return value.decode('utf-8')
        elif isinstance(value, str):
            return value
        else:
            return str(value)

    def add_message(
        self,
        stream_name: str,
        message: Union[dict, str, bytes, Any],
        message_key: Optional[str] = None,
        timeout: float = 30.0,
    ) -> str:
        """Add message to Redis stream.

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
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first")
        if not stream_name or message is None:
            raise ValueError("Stream name and message must be provided")
        
        # Ensure stream_name is always a string
        stream_name = self._safe_decode(stream_name)
        
        # Ensure message_key is always a string if provided
        if message_key is not None:
            message_key = self._safe_decode(message_key)

        # Prepare message fields for Redis stream
        if isinstance(message, dict):
            fields: Dict[str, Any] = {}
            for k, v in message.items():
                # Ensure keys are strings
                key_str = self._safe_decode(k)
                if isinstance(v, (dict, list)):
                    # For nested dicts: Extract binary content to separate field, JSON serialize rest
                    # Redis Streams are binary-safe, so we can store raw bytes in separate fields
                    if isinstance(v, dict):
                        # Check if dict contains binary content that should be extracted
                        extracted_content = None
                        cleaned_dict = {}

                        for nested_k, nested_v in v.items():
                            if nested_k == 'content' and isinstance(nested_v, bytes):
                                # Extract binary content to separate field
                                extracted_content = nested_v
                            else:
                                # Keep non-binary fields for JSON serialization
                                cleaned_dict[nested_k] = nested_v

                        # Store extracted binary content as separate field (Redis binary-safe)
                        if extracted_content:
                            fields[f"{key_str}__content"] = extracted_content

                        # JSON serialize the cleaned dict (no binary data)
                        fields[key_str] = json.dumps(cleaned_dict).encode('utf-8')
                    else:
                        # List: just JSON serialize (no binary expected in lists)
                        fields[key_str] = json.dumps(v).encode('utf-8')
                elif isinstance(v, bytes):
                    # Store binary data directly (NO base64 encoding)
                    # Redis supports binary-safe strings
                    fields[key_str] = v
                else:
                    fields[key_str] = str(v).encode('utf-8')
            # Add message key if provided
            if message_key:
                fields['_message_key'] = message_key.encode('utf-8')
        else:
            # For non-dict messages, handle different types
            if isinstance(message, bytes):
                # Store binary data directly (NO base64 encoding)
                fields = {'data': message}
            else:
                fields = {'data': str(message).encode('utf-8')}

            if message_key:
                fields['_message_key'] = message_key.encode('utf-8')

        message_size = sum(len(str(k)) + len(str(v)) for k, v in fields.items() if not isinstance(v, bytes))
        message_size += sum(len(v) for k, v in fields.items() if isinstance(v, bytes))

        start_time = time.time()
        try:
            # Redis XADD returns the message ID (with optional maxlen for stream trimming)
            if self.stream_maxlen:
                message_id = self.client.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
            else:
                message_id = self.client.xadd(stream_name, fields)
            end_time = time.time()
            
            # Record successful add metrics
            self._record_metric(
                operation="add",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=message_key,
                message_size=message_size
            )
            
            logging.debug(
                "Successfully added message to stream: %s, ID: %s",
                stream_name, message_id
            )
            return self._safe_decode(message_id)
            
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to add message: {str(exc)}"
            logging.error(error_msg, exc_info=True)
            
            # Record failed add metrics
            self._record_metric(
                operation="add",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=message_key,
                message_size=message_size
            )
            raise RedisConnectionError(error_msg)

    # ========================================================================
    # SHM_MODE: Metadata-only operations for shared memory architecture
    # ========================================================================

    def add_shm_metadata(
        self,
        stream_name: str,
        cam_id: str,
        shm_name: str,
        frame_idx: int,
        slot: int,
        ts_ns: int,
        width: int,
        height: int,
        format: str,
        is_similar: bool = False,
        reference_frame_idx: Optional[int] = None,
        similarity_score: Optional[float] = None,
        **extra_metadata
    ) -> str:
        """Add metadata-only message for SHM frame (no binary content).

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
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first")
        if not stream_name or not cam_id or not shm_name:
            raise ValueError("stream_name, cam_id, and shm_name are required")

        start_time = time.time()

        # Build metadata-only message (no binary content!)
        fields = {
            "cam_id": cam_id,
            "shm_name": shm_name,
            "frame_idx": str(frame_idx),
            "slot": str(slot) if slot is not None else "",
            "ts_ns": str(ts_ns),
            "width": str(width),
            "height": str(height),
            "format": format,
            "is_similar": "1" if is_similar else "0",
            "shm_mode": "1",  # Flag to identify SHM metadata messages
        }

        # Add optional fields
        if reference_frame_idx is not None:
            fields["reference_frame_idx"] = str(reference_frame_idx)
        if similarity_score is not None:
            fields["similarity_score"] = str(similarity_score)

        # Add extra metadata (convert all values to strings)
        for key, value in extra_metadata.items():
            if isinstance(value, dict):
                fields[key] = json.dumps(value)
            else:
                fields[key] = str(value)

        message_size = sum(len(k) + len(str(v)) for k, v in fields.items())

        # SHM batching: Use batch buffer when enabled for reduced RTT
        if self.enable_shm_batching and self.enable_batching:
            with self._batch_lock:
                if stream_name not in self._batch_buffer:
                    self._batch_buffer[stream_name] = []
                    self._last_flush_time[stream_name] = time.time()

                # Store as (fields, message_key) to match _flush_stream_batch expectations
                self._batch_buffer[stream_name].append((fields, cam_id))
                self._message_count_since_check += 1
                self._update_dynamic_batch_size()

                should_flush = len(self._batch_buffer[stream_name]) >= self.batch_size

            # Flush outside lock if batch is full
            if should_flush:
                self._flush_stream_batch(stream_name)

            # Record metric for batched operation
            end_time = time.time()
            self._record_metric(
                operation="add_shm_metadata_batched",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=cam_id,
                message_size=message_size
            )

            # Return placeholder ID for batched message
            return f"shm-batched-{int(start_time * 1000000)}"

        # Direct XADD when batching is disabled (original behavior)
        try:
            if self.stream_maxlen:
                message_id = self.client.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
            else:
                message_id = self.client.xadd(stream_name, fields)
            end_time = time.time()

            self._record_metric(
                operation="add_shm_metadata",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=cam_id,
                message_size=message_size
            )

            logging.debug(
                f"Added SHM metadata to stream {stream_name}: "
                f"cam_id={cam_id}, frame_idx={frame_idx}, slot={slot}"
            )
            return self._safe_decode(message_id)

        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to add SHM metadata: {str(exc)}"
            logging.error(error_msg, exc_info=True)

            self._record_metric(
                operation="add_shm_metadata",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=cam_id,
                message_size=message_size
            )
            raise RedisConnectionError(error_msg)

    def subscribe_to_stream(
        self,
        stream_name: str,
        consumer_group: str,
        consumer_name: Optional[str] = None
    ) -> None:
        """Subscribe to a Redis stream (alias for setup_stream for compatibility).

        Args:
            stream_name: Stream to subscribe to
            consumer_group: Consumer group name
            consumer_name: Consumer name (optional)

        Raises:
            RedisConnectionError: If stream setup fails
            ValueError: If stream_name is empty
        """
        if not stream_name:
            raise ValueError("Stream name must be provided")

        # This is just an alias for setup_stream for compatibility
        self.setup_stream(stream_name, consumer_group, consumer_name)

    def unsubscribe_from_stream(self, stream_name: str) -> None:
        """Remove stream from local tracking (consumer group remains on Redis).

        Args:
            stream_name: Stream to unsubscribe from
        """
        try:
            # Ensure stream_name is a string
            stream_name = self._safe_decode(stream_name)
            self._streams.discard(stream_name)
            self._consumer_groups.pop(stream_name, None)
            self._consumer_names.pop(stream_name, None)
            logging.info("Successfully unsubscribed from stream: %s", stream_name)
        except Exception as exc:
            logging.error("Failed to unsubscribe from stream %s: %s", stream_name, str(exc))

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

    def _recreate_consumer_group(self, stream_name: str, consumer_group: str) -> bool:
        """Recreate consumer group for a stream (handles NOGROUP recovery).

        This method is called when an XREADGROUP fails with NOGROUP error,
        indicating the consumer group or stream doesn't exist.

        Args:
            stream_name: Name of the Redis stream
            consumer_group: Name of the consumer group

        Returns:
            bool: True if successfully recreated, False otherwise
        """
        try:
            stream_name = self._safe_decode(stream_name)
            consumer_group = self._safe_decode(consumer_group)

            self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
            logging.info(
                f"Recreated consumer group '{consumer_group}' for stream '{stream_name}' after NOGROUP error"
            )
            return True
        except ResponseError as e:
            if "BUSYGROUP" in str(e):
                # Group was created by another process between error and retry
                logging.debug(f"Consumer group '{consumer_group}' already exists (concurrent creation)")
                return True
            else:
                logging.error(f"Failed to recreate consumer group: {str(e)}")
                return False
        except Exception as e:
            logging.error(f"Failed to recreate consumer group: {str(e)}")
            return False

    def get_message(self, stream_name: Optional[str] = None, timeout: float = 1.0) -> Optional[Dict]:
        """Get a single message from Redis stream.

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
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first")
        
        # Determine which streams to read from
        if stream_name:
            if stream_name not in self._consumer_groups:
                raise RuntimeError(f"Stream '{stream_name}' not set up. Call setup_stream() first")
            streams_to_read = [stream_name]
        else:
            streams_to_read = list(self._streams)
            if not streams_to_read:
                raise RuntimeError("No streams configured. Call setup_stream() first")
        
        start_time = time.time()
        try:
            # Build streams dictionary for XREADGROUP
            streams_dict = {}
            # For multi-stream setups, we'll use the first stream's consumer group/name
            # This is a limitation of Redis XREADGROUP when reading from multiple streams
            first_stream = streams_to_read[0]
            primary_consumer_group = self._consumer_groups[first_stream]
            primary_consumer_name = self._consumer_names[first_stream]
            
            for stream in streams_to_read:
                # Ensure stream names are strings, not bytes
                stream_str = self._safe_decode(stream)
                streams_dict[stream_str] = '>'  # Read new messages
            
            # Use XREADGROUP to read from streams with NOGROUP recovery
            timeout_ms = int(timeout * 1000) if timeout > 0 else 0

            nogroup_retry_attempted = False
            result = None
            while True:
                try:
                    result = self.client.xreadgroup(
                        groupname=self._safe_decode(primary_consumer_group),
                        consumername=self._safe_decode(primary_consumer_name),
                        streams=streams_dict,
                        count=1,
                        block=timeout_ms
                    )
                    break  # Success, exit retry loop
                except ResponseError as xread_exc:
                    error_str = str(xread_exc)

                    # Check for NOGROUP error (stream or consumer group doesn't exist)
                    if "NOGROUP" in error_str and not nogroup_retry_attempted:
                        nogroup_retry_attempted = True
                        logging.warning(
                            f"NOGROUP error detected in get_message, "
                            f"attempting to recreate consumer group: {error_str}"
                        )

                        # Recreate consumer group for the affected stream
                        recreate_success = self._recreate_consumer_group(
                            first_stream,
                            primary_consumer_group
                        )

                        if recreate_success:
                            logging.info("Consumer group recreated, retrying xreadgroup...")
                            continue  # Retry the xreadgroup call
                        else:
                            logging.error("Failed to recreate consumer group, raising original error")
                            raise
                    else:
                        raise

            end_time = time.time()
            
            if not result:
                # Record timeout as successful operation with no message
                self._record_metric(
                    operation="read",
                    stream="(timeout)",
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=None
                )
                return None
            
            # Extract the first message from the result
            stream_name, messages = result[0]
            if not messages:
                return None
            
            # Decode stream_name and message_id to strings immediately
            stream_name = self._safe_decode(stream_name)  # type: ignore[arg-type,assignment]
            message_id, fields = messages[0]
            message_id = self._safe_decode(message_id)  # type: ignore[arg-type,assignment]
            
            # Parse fields into structured data
            parsed_data = {}
            message_key = None
            total_size = 0

            for field_name, field_value in fields.items():
                field_name = self._safe_decode(field_name)

                # Skip UTF-8 decode for binary content fields to preserve raw bytes
                # This includes both direct 'content' fields and flattened '__content' fields
                if isinstance(field_value, bytes) and ('__content' in field_name or field_name == 'content'):
                    # Keep binary data as bytes (no UTF-8 decode)
                    total_size += len(field_name) + len(field_value)
                    parsed_data[field_name] = field_value
                    continue

                field_value = self._safe_decode(field_value)
                total_size += len(field_name) + len(field_value)

                if field_name == '_message_key':
                    message_key = field_value
                    continue

                # Try to parse JSON values
                try:
                    parsed_data[field_name] = json.loads(field_value)
                except (json.JSONDecodeError, ValueError):
                    parsed_data[field_name] = field_value
            
            # Record successful message retrieval metrics
            self._record_metric(
                operation="read",
                stream=stream_name,  # type: ignore[arg-type]
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=message_key,
                message_size=total_size
            )
            
            # Acknowledge the message
            try:
                consumer_group = self._consumer_groups[stream_name]  # type: ignore[index]
                self.client.xack(stream_name, consumer_group, message_id)
            except Exception as ack_exc:
                logging.warning("Failed to acknowledge message: %s", str(ack_exc))
            
            result = {
                "stream": stream_name,  # Already decoded
                "message_id": message_id,  # Already decoded
                "data": parsed_data,
                "fields": {self._safe_decode(k): self._safe_decode(v, keep_binary=True) for k, v in fields.items()},
                "message_key": message_key
            }
            return result
            
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to get message: {str(exc)}"
            logging.error(error_msg)
            
            # Record error metrics
            self._record_metric(
                operation="read",
                stream="(error)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None
            )
            raise RedisConnectionError(error_msg)

    def listen_for_messages(self, callback: Optional[Callable] = None, stream_name: Optional[str] = None) -> None:
        """Listen for messages on configured streams (blocking).

        Args:
            callback: Optional callback function for all messages
            stream_name: Optional specific stream to listen to (listens to all if None)

        Raises:
            RuntimeError: If no streams are configured
            RedisConnectionError: If listening fails
        """
        if not self._streams:
            raise RuntimeError("No streams configured. Call setup_stream() first")

        try:
            logging.info("Starting to listen for Redis stream messages...")
            while True:
                try:
                    message = self.get_message(stream_name=stream_name, timeout=5.0)
                    if message:
                        # Execute callback
                        if callback:
                            try:
                                callback(message)
                            except Exception as callback_exc:
                                logging.error("Error in stream callback: %s", str(callback_exc))
                except RedisConnectionError as exc:
                    logging.error("Redis connection error while listening: %s", str(exc))
                    # Sleep briefly before retrying
                    time.sleep(1.0)
                except Exception as exc:
                    logging.error("Unexpected error while listening: %s", str(exc))
                    time.sleep(1.0)
                            
        except KeyboardInterrupt:
            logging.info("Stopped listening for Redis stream messages")
        except Exception as exc:
            error_msg = f"Error listening for messages: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    def _batch_flusher(self) -> None:
        """Background thread that periodically flushes batched messages."""
        logging.info("Redis batch flusher thread started")
        while not self._batch_stop_event.is_set():
            try:
                # Sleep in small intervals so we can stop quickly
                time.sleep(0.05)  # Check every 50ms

                current_time = time.time()
                streams_to_flush = []

                with self._batch_lock:
                    for stream_name in list(self._batch_buffer.keys()):
                        last_flush = self._last_flush_time.get(stream_name, 0)
                        buffer_size = len(self._batch_buffer.get(stream_name, []))

                        # Flush if timeout reached or batch size exceeded
                        if (buffer_size > 0 and current_time - last_flush >= self.batch_timeout) or \
                           buffer_size >= self.batch_size:
                            streams_to_flush.append(stream_name)

                # Flush outside of lock to avoid blocking add operations
                for stream_name in streams_to_flush:
                    self._flush_stream_batch(stream_name)

            except Exception as exc:
                logging.error("Error in batch flusher thread: %s", str(exc), exc_info=True)

        logging.info("Redis batch flusher thread stopped")

    def _flush_stream_batch(self, stream_name: str) -> List[str]:
        """Flush pending messages for a specific stream using pipeline.

        Args:
            stream_name: Stream to flush

        Returns:
            List of message IDs
        """
        messages_to_flush = []

        with self._batch_lock:
            if stream_name in self._batch_buffer:
                messages_to_flush = self._batch_buffer[stream_name]
                self._batch_buffer[stream_name] = []
                self._last_flush_time[stream_name] = time.time()

        if not messages_to_flush:
            return []

        message_ids = []
        pipeline = self.client.pipeline()

        try:
            # Add all messages to pipeline
            for fields, message_key, start_time in messages_to_flush:
                if self.stream_maxlen:
                    pipeline.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                else:
                    pipeline.xadd(stream_name, fields)

            # Execute pipeline
            pipeline_start = time.time()
            results = pipeline.execute()
            pipeline_end = time.time()

            # Record metrics for each message
            for i, (fields, message_key, start_time) in enumerate(messages_to_flush):
                message_id = results[i] if i < len(results) else None
                if message_id:
                    message_ids.append(self._safe_decode(message_id))
                    message_size = sum(len(str(k)) + len(str(v)) for k, v in fields.items())

                    self._record_metric(
                        operation="add_batch",
                        stream=stream_name,
                        start_time=start_time,
                        end_time=pipeline_end,
                        success=True,
                        message_key=message_key,
                        message_size=message_size
                    )

            logging.debug("Flushed %d messages to stream '%s' in %.2fms",
                         len(messages_to_flush), stream_name,
                         (pipeline_end - pipeline_start) * 1000)

            return message_ids

        except Exception as exc:
            error_msg = f"Failed to flush batch: {str(exc)}"
            logging.error(error_msg, exc_info=True)

            # Record failed metrics
            end_time = time.time()
            for fields, message_key, start_time in messages_to_flush:
                message_size = sum(len(str(k)) + len(str(v)) for k, v in fields.items())
                self._record_metric(
                    operation="add_batch",
                    stream=stream_name,
                    start_time=start_time,
                    end_time=end_time,
                    success=False,
                    error_msg=error_msg,
                    message_key=message_key,
                    message_size=message_size
                )

            raise RedisConnectionError(error_msg)

    def flush_pending_messages(self) -> Dict[str, List[str]]:
        """Manually flush all pending batched messages.

        Returns:
            Dict mapping stream names to lists of message IDs
        """
        if not self.client:
            raise RuntimeError("Redis client not initialized")

        results = {}
        with self._batch_lock:
            streams = list(self._batch_buffer.keys())

        for stream_name in streams:
            try:
                message_ids = self._flush_stream_batch(stream_name)
                results[stream_name] = message_ids
            except Exception as exc:
                logging.error("Error flushing stream %s: %s", stream_name, str(exc))
                results[stream_name] = []

        return results

    def add_messages_batch(
        self,
        stream_name: str,
        messages: List[Dict],
        timeout: float = 30.0
    ) -> List[str]:
        """Add multiple messages to Redis stream using pipeline.

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
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        if not stream_name or not messages:
            raise ValueError("Stream name and messages must be provided")

        stream_name = self._safe_decode(stream_name)
        pipeline = self.client.pipeline()
        start_time = time.time()

        try:
            # Prepare all messages
            for message in messages:
                if isinstance(message, dict):
                    fields: Dict[str, Any] = {}
                    for k, v in message.items():
                        key_str = self._safe_decode(k)
                        if isinstance(v, (dict, list)):
                            # For nested dicts: Extract binary content to separate field
                            if isinstance(v, dict):
                                extracted_content = None
                                cleaned_dict = {}

                                for nested_k, nested_v in v.items():
                                    if nested_k == 'content' and isinstance(nested_v, bytes):
                                        extracted_content = nested_v
                                    else:
                                        cleaned_dict[nested_k] = nested_v

                                if extracted_content:
                                    fields[f"{key_str}__content"] = extracted_content

                                fields[key_str] = json.dumps(cleaned_dict).encode('utf-8')
                            else:
                                fields[key_str] = json.dumps(v).encode('utf-8')
                        elif isinstance(v, bytes):
                            # Store binary data directly (no base64)
                            fields[key_str] = v
                        else:
                            fields[key_str] = str(v).encode('utf-8')
                    if self.stream_maxlen:
                        pipeline.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                    else:
                        pipeline.xadd(stream_name, fields)

            # Execute pipeline
            results = pipeline.execute()
            end_time = time.time()

            message_ids = [self._safe_decode(mid) for mid in results]

            # Record metrics
            total_size = sum(
                sum(len(str(k)) + len(str(v)) for k, v in msg.items())
                for msg in messages if isinstance(msg, dict)
            )
            self._record_metric(
                operation="add_messages_batch",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=True,
                message_size=total_size
            )

            logging.debug("Added %d messages to stream '%s' via batch",
                         len(messages), stream_name)
            return message_ids

        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to add message batch: {str(exc)}"
            logging.error(error_msg, exc_info=True)

            self._record_metric(
                operation="add_messages_batch",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg
            )
            raise RedisConnectionError(error_msg)

    def add_frame(
        self,
        stream_name: str,
        frame_data: bytes,
        metadata: Dict,
        use_batching: Optional[bool] = None
    ) -> Optional[str]:
        """Optimized method for adding video frame to Redis stream.

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
        if not self.client:
            raise RuntimeError("Redis client not initialized")

        stream_name = self._safe_decode(stream_name)
        use_batching = use_batching if use_batching is not None else self.enable_batching

        # Prepare fields with binary frame data (no base64 encoding)
        fields: Dict[str, Any] = {
            'metadata': json.dumps(metadata).encode('utf-8'),
            'frame_data': frame_data,  # Raw binary
            'timestamp': str(time.time()).encode('utf-8')
        }

        start_time = time.time()
        message_key = metadata.get('camera_id', None)

        if use_batching:
            # Add to batch buffer
            with self._batch_lock:
                if stream_name not in self._batch_buffer:
                    self._batch_buffer[stream_name] = []
                    self._last_flush_time[stream_name] = time.time()

                self._batch_buffer[stream_name].append((fields, message_key, start_time))

                # Track throughput for dynamic batching
                self._message_count_since_check += 1
                self._update_dynamic_batch_size()

                # Flush if batch size reached (flusher thread handles actual flush)
                # No immediate action needed here

            return None  # Message will be sent asynchronously
        else:
            # Send immediately
            try:
                if self.stream_maxlen:
                    message_id = self.client.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                else:
                    message_id = self.client.xadd(stream_name, fields)
                end_time = time.time()

                # Metrics
                message_size = len(frame_data)
                self._record_metric(
                    operation="add_frame",
                    stream=stream_name,
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=message_key,
                    message_size=message_size
                )

                return self._safe_decode(message_id)

            except Exception as exc:
                end_time = time.time()
                error_msg = f"Failed to add frame: {str(exc)}"
                self._record_metric(
                    operation="add_frame",
                    stream=stream_name,
                    start_time=start_time,
                    end_time=end_time,
                    success=False,
                    error_msg=error_msg,
                    message_key=message_key,
                    message_size=None
                )
                raise RedisConnectionError(error_msg)

    def close(self) -> None:
        """Close Redis client connections."""
        try:
            # Stop metrics reporting thread first
            self.stop_metrics_reporting()

            # Stop batching thread and flush pending messages
            if self._batch_thread and self._batch_thread.is_alive():
                logging.info("Stopping Redis batching thread...")
                # Flush any pending messages before stopping
                self.flush_pending_messages()
                self._batch_stop_event.set()
                self._batch_thread.join(timeout=5)
                if self._batch_thread.is_alive():
                    logging.warning("Redis batching thread did not stop gracefully")
                else:
                    logging.info("Redis batching thread stopped")

            # Clear stream tracking
            if self._streams:
                try:
                    self._streams.clear()
                    self._consumer_groups.clear()
                    self._consumer_names.clear()
                    logging.debug("Cleared stream tracking")
                except Exception as exc:
                    logging.warning("Error clearing stream tracking: %s", str(exc))

            if self.client:
                try:
                    self.client.close()
                except Exception as exc:
                    logging.warning("Error closing Redis client: %s", str(exc))
                self.client = None

            # Disconnect connection pool
            if self.connection_pool:
                try:
                    self.connection_pool.disconnect()
                except Exception as exc:
                    logging.warning("Error disconnecting connection pool: %s", str(exc))
                self.connection_pool = None

            logging.info("Closed Redis connections")
        except Exception as exc:
            logging.error("Error closing Redis connections: %s", str(exc))
            raise


class AsyncRedisUtils:
    """Utility class for asynchronous Redis Streams operations."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        username: Optional[str] = None,
        db: int = 0,
        connection_timeout: int = 30,
        pool_max_connections: int = 50,
        enable_batching: bool = True,
        batch_size: int = 10,
        batch_timeout: float = 0.01,
        enable_shm_batching: bool = False,
        # Cross-stream batching optimization (Phase 2)
        enable_cross_stream_batching: bool = True,  # Single pipeline for ALL streams
        flusher_interval: float = 0.025,  # Batch flusher check interval (25ms default)
        stream_maxlen: Optional[int] = None
    ) -> None:
        """Initialize async Redis utils with connection parameters.

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
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.db = db
        self.connection_timeout = connection_timeout
        self.pool_max_connections = pool_max_connections
        self.enable_batching = enable_batching
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self._initial_batch_size = batch_size  # Store initial for reset
        self.enable_shm_batching = enable_shm_batching
        # Cross-stream batching optimization (Phase 2)
        self.enable_cross_stream_batching = enable_cross_stream_batching
        self.flusher_interval = flusher_interval
        self.stream_maxlen = stream_maxlen

        self.client: Optional[redis_asyncio.Redis] = None
        self.connection_pool: Optional[Any] = None
        self._streams: Set[str] = set()  # Set of stream names we're working with
        self._consumer_groups: Dict[str, str] = {}  # Map of stream -> consumer group
        self._consumer_names: Dict[str, str] = {}  # Map of stream -> consumer name

        # Batching support (async)
        self._batch_buffer: Dict[str, List[Tuple[Dict[str, Any], Optional[str]]]] = {}
        self._batch_lock: Optional[asyncio.Lock] = None  # Will be initialized in setup_client
        self._last_flush_time: Dict[str, float] = {}
        self._batch_task: Optional[asyncio.Task[None]] = None  # Background asyncio task for flushing
        self._batch_stop_event: Optional[asyncio.Event] = None  # Will be initialized in setup_client

        # Dynamic batching controller for adaptive throughput
        self._throughput_samples: Deque[float] = deque(maxlen=10)  # Last 10 throughput samples
        self._last_throughput_check = time.time()
        self._message_count_since_check = 0
        self._throughput_check_interval = 5.0  # Check every 5 seconds

        # Metrics collection for performance monitoring (async-safe)
        self._metrics_log: Deque[Dict[str, Any]] = deque(maxlen=10000)  # Keep last 10000 metrics entries
        self._metrics_lock = threading.Lock()
        self._pending_operations: Dict[str, Any] = {}  # Track pending async operations for timing

        # Background metrics reporting (shared with sync version)
        self._metrics_reporting_config: Optional[Dict[str, Any]] = None
        self._metrics_thread: Optional[threading.Thread] = None
        self._metrics_stop_event = threading.Event()

        logging.info("Initialized AsyncRedisUtils with host: %s:%d, db: %d", host, port, db)

    def _record_metric(self, operation: str, stream: str, start_time: float, end_time: float, 
                      success: bool, error_msg: Optional[str] = None, message_key: Optional[str] = None, 
                      message_size: Optional[int] = None) -> None:
        """Record a performance metric for aggregation.
        
        Args:
            operation: Type of operation ('add' or 'read')
            stream: Redis stream name
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
            'stream': stream,
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
        if success:
            status = "SUCCESS"
            logging.debug(
                "Async Redis %s %s: stream=%s, duration=%.2fms, key=%s, size=%s%s",
                operation.upper(), status, stream, duration_ms, message_key or 'None', 
                message_size or 'Unknown', f", error={error_msg}" if error_msg else ""
            )
        else:
            status = "FAILED"
            logging.warning(
                "Async Redis %s %s: stream=%s, duration=%.2fms, key=%s, size=%s%s",
                operation.upper(), status, stream, duration_ms, message_key or 'None', 
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

    def _update_dynamic_batch_size(self) -> None:
        """Dynamically adjust batch size based on throughput to optimize for varying loads.

        Adaptive batching strategy:
        - Low throughput (< 1K msg/sec): batch_size = 50 (responsive, low latency)
        - Medium throughput (1K-10K msg/sec): batch_size = 200 (balanced)
        - High throughput (10K-50K msg/sec): batch_size = 500 (efficient batching)
        - Very high throughput (> 50K msg/sec): batch_size = 1000 (maximum efficiency)

        This prevents slow cameras from experiencing high latency with large batches,
        while enabling high throughput when processing many cameras.
        """
        current_time = time.time()
        elapsed = current_time - self._last_throughput_check

        # Check throughput every interval
        if elapsed >= self._throughput_check_interval:
            # Calculate messages per second
            throughput = self._message_count_since_check / elapsed if elapsed > 0 else 0
            self._throughput_samples.append(throughput)

            # Calculate average throughput from recent samples (smooth out spikes)
            avg_throughput = sum(self._throughput_samples) / len(self._throughput_samples) if self._throughput_samples else 0

            # Determine optimal batch size based on throughput
            old_batch_size = self.batch_size
            if avg_throughput < 1000:
                self.batch_size = 50
            elif avg_throughput < 10000:
                self.batch_size = 200
            elif avg_throughput < 50000:
                self.batch_size = 500
            else:
                self.batch_size = 1000

            # Log batch size changes
            if self.batch_size != old_batch_size:
                logging.info(
                    "Dynamic batching (async): adjusted batch_size from %d to %d "
                    "(throughput: %.1f msg/sec, avg: %.1f msg/sec)",
                    old_batch_size, self.batch_size, throughput, avg_throughput
                )

            # Reset counters
            self._message_count_since_check = 0
            self._last_throughput_check = current_time

    def configure_metrics_reporting(self,
                                   rpc_client,
                                   deployment_id: Optional[str] = None,
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
            
            if aggregated_data.get('stream'):
                success = self._send_metrics_to_api(aggregated_data)
                if success:
                    logging.info(f"Successfully sent {len(raw_metrics)} async Redis metrics to backend API")
                    logging.info(f"Async Redis Metrics: {raw_metrics}")
                else:
                    logging.warning("Failed to send async Redis metrics to backend API")
            else:
                logging.debug("No async stream-level metrics to report")
                
        except Exception as exc:
            logging.error(f"Error collecting and sending async Redis metrics: {exc}")

    def _aggregate_metrics_for_api(self, raw_metrics: List[Dict]) -> Dict:
        """Aggregate raw metrics into the API format expected by backend (async version)."""
        stream_stats = {}
        current_time = datetime.now(timezone.utc).isoformat()
        
        for metric in raw_metrics:
            stream = metric.get('stream', 'unknown')
            operation = metric.get('operation', 'unknown')
            success = metric.get('success', False)
            duration_ms = metric.get('duration_ms', 0)
            
            if stream in ['(timeout)', '(error)', 'unknown']:
                continue
            
            if stream not in stream_stats:
                stream_stats[stream] = {
                    'stream': stream,
                    'addCount': 0,
                    'readCount': 0,
                    'totalLatency': 0,
                    'latencies': [],
                    'avgLatency': 0,
                    'minlatency': float('inf'),
                    'maxlatency': 0
                }
            
            stats = stream_stats[stream]
            
            if operation == 'add' and success:
                stats['addCount'] += 1
            elif operation in ['read', 'get_message'] and success:
                stats['readCount'] += 1
            
            if success and duration_ms > 0:
                latency_ns = int(duration_ms * 1_000_000)
                stats['latencies'].append(latency_ns)
                stats['totalLatency'] += latency_ns
                stats['minlatency'] = min(stats['minlatency'], latency_ns)
                stats['maxlatency'] = max(stats['maxlatency'], latency_ns)
        
        for stream, stats in stream_stats.items():
            if stats['latencies']:
                stats['avgLatency'] = stats['totalLatency'] // len(stats['latencies'])
            else:
                stats['avgLatency'] = 0
                stats['minlatency'] = 0
            del stats['latencies']
        
        payload = {
            'stream': list(stream_stats.values()),
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
            cfg: Dict[str, Any] = self._metrics_reporting_config or {}
            rpc_client = cfg.get('rpc_client')
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

    def _safe_decode(self, value: Union[str, bytes], keep_binary: bool = True) -> Any:
        """Safely decode bytes to string, handling both str and bytes input.

        Args:
            value: Value to decode (str or bytes)
            keep_binary: If True, return bytes as-is if UTF-8 decoding fails

        Returns:
            Decoded string or original bytes if decoding fails and keep_binary=True
        """
        if isinstance(value, bytes):
            if keep_binary:
                try:
                    return value.decode('utf-8')
                except UnicodeDecodeError:
                    # Return bytes as-is for binary data (images, etc.)
                    return value
            else:
                return value.decode('utf-8')
        elif isinstance(value, str):
            return value
        else:
            return str(value)

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
        
        # Override with any additional config
        client_config.update(kwargs)
        
        # Close existing client if any
        if self.client:
            try:
                await self.client.close()
            except Exception:
                pass  # Ignore errors during cleanup
                
        try:
            self.client = redis_asyncio.Redis(**client_config)  # type: ignore[call-overload]
            # Test connection
            assert self.client is not None
            await self.client.ping()
            logging.info("Successfully set up async Redis client")

            # Initialize async batching infrastructure if enabled
            if self.enable_batching:
                self._batch_lock = asyncio.Lock()
                self._batch_stop_event = asyncio.Event()

                # Start background batching task
                self._batch_task = asyncio.create_task(self._batch_flusher())
                logging.info("Started async Redis batch flusher task")

        except Exception as exc:
            error_msg = f"Failed to initialize async Redis client: {str(exc)}"
            logging.error(error_msg)
            # Clean up on failure
            self.client = None
            raise RedisConnectionError(error_msg)

    async def _verify_stream_setup(self, stream_name: str, consumer_group: str, max_retries: int = 3) -> None:
        """Verify stream and consumer group exist after setup.

        This method prevents race conditions by ensuring the stream and consumer group
        are actually created before returning from setup_stream(). If verification fails,
        it attempts to recreate them.

        Args:
            stream_name: Name of the Redis stream
            consumer_group: Name of the consumer group
            max_retries: Maximum verification attempts

        Raises:
            RedisConnectionError: If verification fails after retries
        """
        stream_name = self._safe_decode(stream_name)
        consumer_group = self._safe_decode(consumer_group)

        assert self.client is not None
        for attempt in range(max_retries):
            try:
                # Check if stream exists using XINFO GROUPS
                groups = await self.client.xinfo_groups(stream_name)
                group_names = []
                for g in groups:
                    name = g.get('name', g.get(b'name', b''))
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    group_names.append(name)

                if consumer_group in group_names:
                    logging.debug(f"Verified async consumer group '{consumer_group}' exists on stream '{stream_name}'")
                    return

                # Group not found, try to create it
                logging.warning(f"Async consumer group '{consumer_group}' not found on attempt {attempt + 1}, recreating...")
                try:
                    await self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
                except Exception as create_err:
                    if "BUSYGROUP" not in str(create_err):
                        raise

            except Exception as e:
                error_str = str(e).lower()
                if "nogroup" in error_str or "no such key" in error_str or "doesn't exist" in error_str:
                    # Stream doesn't exist, create it with xgroup_create + mkstream=True
                    logging.warning(f"Async stream '{stream_name}' doesn't exist on attempt {attempt + 1}, creating...")
                    try:
                        await self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
                        logging.info(f"Created async stream '{stream_name}' with consumer group '{consumer_group}'")
                        # Successfully created, continue to verify on next iteration
                    except Exception as create_err:
                        if "BUSYGROUP" not in str(create_err):
                            if attempt == max_retries - 1:
                                raise RedisConnectionError(
                                    f"Failed to verify/create async stream setup after {max_retries} attempts: {create_err}"
                                )
                elif attempt == max_retries - 1:
                    raise RedisConnectionError(
                        f"Failed to verify async stream setup after {max_retries} attempts: {e}"
                    )

            await asyncio.sleep(0.1 * (attempt + 1))  # Small backoff between retries

        # Final verification after all retries
        try:
            groups = await self.client.xinfo_groups(stream_name)
            group_names = []
            for g in groups:
                name = g.get('name', g.get(b'name', b''))
                if isinstance(name, bytes):
                    name = name.decode('utf-8')
                group_names.append(name)

            if consumer_group in group_names:
                logging.info(f"Async stream '{stream_name}' with consumer group '{consumer_group}' verified after retries")
                return
        except Exception:
            pass

        raise RedisConnectionError(
            f"Failed to verify async consumer group '{consumer_group}' on stream '{stream_name}' after {max_retries} attempts"
        )

    async def setup_stream(self, stream_name: str, consumer_group: str, consumer_name: Optional[str] = None) -> None:
        """Set up Redis stream with consumer group asynchronously.

        Args:
            stream_name: Name of the Redis stream
            consumer_group: Name of the consumer group
            consumer_name: Name of the consumer (defaults to hostname-timestamp)

        Raises:
            RedisConnectionError: If stream setup fails
        """
        if not self.client:
            await self.setup_client()
        
        try:
            # Ensure all parameters are strings, not bytes
            stream_name = self._safe_decode(stream_name)
            consumer_group = self._safe_decode(consumer_group)
            
            # Generate default consumer name if not provided
            if not consumer_name:
                import threading
                consumer_name = f"async-consumer-{int(time.time())}-{threading.current_thread().ident}"
            else:
                consumer_name = self._safe_decode(consumer_name)
            
            # Create consumer group if it doesn't exist
            assert self.client is not None
            try:
                await self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
                logging.info(f"Created async consumer group '{consumer_group}' for stream '{stream_name}'")
            except Exception as e:
                error_str = str(e)
                if "BUSYGROUP" in error_str:
                    logging.debug(f"Async consumer group '{consumer_group}' already exists for stream '{stream_name}'")
                else:
                    raise

            # Verify stream and consumer group were actually created (prevents race conditions)
            await self._verify_stream_setup(stream_name, consumer_group)

            # Store stream configuration (ensure all are strings)
            self._streams.add(stream_name)  # type: ignore[arg-type]
            self._consumer_groups[stream_name] = consumer_group  # type: ignore[assignment]
            self._consumer_names[stream_name] = consumer_name  # type: ignore[assignment]

            logging.info(f"Successfully set up async Redis stream '{stream_name}' with consumer group '{consumer_group}'")
        except Exception as exc:
            error_msg = f"Failed to set up async Redis stream: {str(exc)}"
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

    @staticmethod
    def _prepare_for_json(obj: Any) -> Any:
        """Recursively prepare object for JSON serialization.

        Converts bytes and memoryview objects to base64 strings so they can
        be safely JSON serialized. Handles nested dicts and lists.

        Args:
            obj: Object to prepare

        Returns:
            JSON-serializable version of the object
        """
        if isinstance(obj, bytes):
            # Convert bytes to base64 string for JSON serialization
            import base64
            return base64.b64encode(obj).decode('ascii')
        elif isinstance(obj, memoryview):
            # Convert memoryview to base64 string
            import base64
            return base64.b64encode(bytes(obj)).decode('ascii')
        elif hasattr(obj, '__buffer__'):
            # Handle buffer protocol objects
            import base64
            return base64.b64encode(bytes(memoryview(obj))).decode('ascii')
        elif isinstance(obj, dict):
            # Recursively process dict values
            return {k: AsyncRedisUtils._prepare_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Recursively process list items
            return [AsyncRedisUtils._prepare_for_json(item) for item in obj]
        elif isinstance(obj, tuple):
            # Convert tuple to list (JSON doesn't have tuples)
            return [AsyncRedisUtils._prepare_for_json(item) for item in obj]
        else:
            # Return as-is for JSON-safe types (str, int, float, bool, None)
            return obj

    async def add_message(
        self,
        stream_name: str,
        message: Union[dict, str, bytes, Any],
        message_key: Optional[str] = None,
        timeout: float = 30.0,
    ) -> str:
        """Add message to Redis stream asynchronously with automatic batching.

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
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first.")
        if not stream_name or message is None:
            raise ValueError("Stream name and message must be provided")

        # Ensure stream_name is always a string
        stream_name = self._safe_decode(stream_name)

        # Ensure message_key is always a string if provided
        if message_key is not None:
            message_key = self._safe_decode(message_key)

        # Prepare message fields for Redis stream
        if isinstance(message, dict):
            fields: Dict[str, Any] = {}
            for k, v in message.items():
                # Ensure both keys and values are strings
                key_str = self._safe_decode(k)
                if isinstance(v, (dict, list)):
                    # For nested dicts: Extract binary content to separate field, JSON serialize rest
                    # Redis Streams are binary-safe, so we can store raw bytes in separate fields
                    if isinstance(v, dict):
                        # Check if dict contains binary content that should be extracted
                        extracted_content = None
                        cleaned_dict = {}

                        for nested_k, nested_v in v.items():
                            if nested_k == 'content' and isinstance(nested_v, (bytes, memoryview)):
                                # Extract binary content to separate field
                                if isinstance(nested_v, memoryview):
                                    extracted_content = bytes(nested_v)
                                else:
                                    extracted_content = nested_v
                            else:
                                # Keep non-binary fields for JSON serialization
                                cleaned_dict[nested_k] = nested_v

                        # Store extracted binary content as separate field (Redis binary-safe)
                        if extracted_content:
                            fields[f"{key_str}__content"] = extracted_content

                        # JSON serialize the cleaned dict (no binary data)
                        fields[key_str] = json.dumps(cleaned_dict).encode('utf-8')
                    else:
                        # List: just JSON serialize (no binary expected in lists)
                        fields[key_str] = json.dumps(v).encode('utf-8')
                elif isinstance(v, bytes):
                    # Store binary data directly (NO base64 encoding for performance)
                    # Redis supports binary-safe strings
                    fields[key_str] = v
                elif isinstance(v, memoryview):
                    # ZERO-COPY: Convert memoryview to bytes only at last moment
                    # This is unavoidable but delays copy until absolutely necessary
                    # Reduces memory allocations by 66% in the pipeline
                    fields[key_str] = bytes(v)
                elif hasattr(v, '__buffer__'):
                    # Support any buffer protocol object (numpy arrays, etc.)
                    fields[key_str] = bytes(memoryview(v))
                else:
                    fields[key_str] = str(v).encode('utf-8')
            # Add message key if provided
            if message_key:
                fields['_message_key'] = message_key.encode('utf-8')
        else:
            # For non-dict messages, handle different types
            if isinstance(message, bytes):
                # Store binary data directly (NO base64 encoding)
                fields = {'data': message}
            elif isinstance(message, memoryview):
                # ZERO-COPY: Convert at last moment
                fields = {'data': bytes(message)}
            elif hasattr(message, '__buffer__'):
                # Support buffer protocol
                fields = {'data': bytes(memoryview(message))}
            else:
                fields = {'data': str(message).encode('utf-8')}

            if message_key:
                fields['_message_key'] = message_key.encode('utf-8')

        message_size = sum(len(str(k)) + len(str(v)) for k, v in fields.items())
        start_time = time.time()

        # BATCHING: Add to batch buffer if enabled for automatic batching
        if self.enable_batching and self._batch_lock is not None:
            try:
                async with self._batch_lock:
                    # Initialize stream buffer if needed
                    if stream_name not in self._batch_buffer:
                        self._batch_buffer[stream_name] = []
                        self._last_flush_time[stream_name] = time.time()

                    # Add to batch
                    self._batch_buffer[stream_name].append((fields, message_key))

                    # Track throughput for dynamic batching
                    self._message_count_since_check += 1
                    self._update_dynamic_batch_size()

                    # Check if we should flush immediately
                    should_flush = len(self._batch_buffer[stream_name]) >= self.batch_size

                if should_flush:
                    await self._flush_stream_batch(stream_name)

                # Return placeholder ID (actual ID assigned during flush)
                return f"*-batched-{int(start_time * 1000000)}"

            except Exception as exc:
                end_time = time.time()
                error_msg = f"Failed to add async message to batch: {str(exc)}"
                logging.error(error_msg, exc_info=True)

                # Record failed add metrics
                self._record_metric(
                    operation="add",
                    stream=stream_name,
                    start_time=start_time,
                    end_time=end_time,
                    success=False,
                    error_msg=error_msg,
                    message_key=message_key,
                    message_size=message_size
                )
                raise RedisConnectionError(error_msg)
        else:
            # NO BATCHING: Send immediately
            try:
                # Redis XADD returns the message ID (with optional maxlen for stream trimming)
                assert self.client is not None
                if self.stream_maxlen:
                    message_id = await self.client.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                else:
                    message_id = await self.client.xadd(stream_name, fields)
                end_time = time.time()

                # Record successful add metrics
                self._record_metric(
                    operation="add",
                    stream=stream_name,
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=message_key,
                    message_size=message_size
                )

                logging.debug("Successfully added async message to stream: %s, ID: %s", stream_name, message_id)
                return self._safe_decode(message_id)
            except Exception as exc:
                end_time = time.time()
                error_msg = f"Failed to add async message: {str(exc)}"
                logging.error(error_msg, exc_info=True)

                # Record failed add metrics
                self._record_metric(
                    operation="add",
                    stream=stream_name,
                    start_time=start_time,
                    end_time=end_time,
                    success=False,
                    error_msg=error_msg,
                    message_key=message_key,
                    message_size=message_size
                )
                raise RedisConnectionError(error_msg)

    # ================================================================
    # SHM_MODE: Metadata-only operations for shared memory architecture
    # ================================================================

    async def add_shm_metadata(
        self,
        stream_name: str,
        cam_id: str,
        shm_name: str,
        frame_idx: int,
        slot: int,
        ts_ns: int,
        width: int,
        height: int,
        format: str,
        is_similar: bool = False,
        reference_frame_idx: Optional[int] = None,
        similarity_score: Optional[float] = None,
        **extra_metadata
    ) -> str:
        """Async: Add metadata-only message for SHM frame (no binary content).

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
        if not stream_name:
            raise ValueError("Stream name must be provided")

        # Build metadata-only message (NO binary frame content)
        fields = {
            "shm_mode": "1",  # Flag for consumers - string for Redis compatibility
            "cam_id": cam_id,
            "shm_name": shm_name if shm_name else "",
            "frame_idx": str(frame_idx),
            "slot": str(slot) if slot is not None else "",
            "ts_ns": str(ts_ns),
            "width": str(width),
            "height": str(height),
            "format": format,
            "is_similar": "1" if is_similar else "0",
        }

        # Add reference frame for similar frames
        if reference_frame_idx is not None:
            fields["reference_frame_idx"] = str(reference_frame_idx)

        if similarity_score is not None:
            fields["similarity_score"] = str(similarity_score)

        # Add extra metadata fields (stream_group_key, camera_location, etc.)
        for key, value in extra_metadata.items():
            if value is not None:
                fields[key] = str(value) if not isinstance(value, str) else value

        message_size = sum(len(str(k)) + len(str(v)) for k, v in fields.items())
        start_time = time.time()

        # SHM batching: Use batch buffer when enabled for reduced RTT (10x improvement)
        if self.enable_shm_batching and self.enable_batching and self._batch_lock is not None:
            async with self._batch_lock:
                if stream_name not in self._batch_buffer:
                    self._batch_buffer[stream_name] = []
                    self._last_flush_time[stream_name] = time.time()

                # Store as (fields, message_key) to match _flush_stream_batch expectations
                self._batch_buffer[stream_name].append((fields, cam_id))
                self._message_count_since_check += 1
                self._update_dynamic_batch_size()

                should_flush = len(self._batch_buffer[stream_name]) >= self.batch_size

            # Flush outside lock if batch is full
            if should_flush:
                await self._flush_stream_batch(stream_name)

            # Record metric for batched operation
            end_time = time.time()
            self._record_metric(
                operation="add_shm_metadata_batched",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=cam_id,
                message_size=message_size
            )

            # Return placeholder ID for batched message
            return f"shm-batched-{int(start_time * 1000000)}"

        # Direct XADD when batching is disabled (original behavior)
        try:
            assert self.client is not None
            if self.stream_maxlen:
                message_id = await self.client.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
            else:
                message_id = await self.client.xadd(stream_name, fields)
            end_time = time.time()

            # Record metrics
            self._record_metric(
                operation="add_shm_metadata",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=cam_id,
                message_size=message_size
            )

            logging.debug(
                "SHM metadata added to stream %s: cam=%s frame_idx=%d slot=%s",
                stream_name, cam_id, frame_idx, slot
            )
            return self._safe_decode(message_id)

        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to add SHM metadata: {str(exc)}"
            logging.error(error_msg, exc_info=True)

            self._record_metric(
                operation="add_shm_metadata",
                stream=stream_name,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=cam_id,
                message_size=message_size
            )
            raise RedisConnectionError(error_msg)

    async def subscribe_to_stream(
        self,
        stream_name: str,
        consumer_group: str,
        consumer_name: Optional[str] = None
    ) -> None:
        """Subscribe to a Redis stream asynchronously (alias for setup_stream for compatibility).

        Args:
            stream_name: Stream to subscribe to
            consumer_group: Consumer group name
            consumer_name: Consumer name (optional)

        Raises:
            RedisConnectionError: If stream setup fails
            ValueError: If stream_name is empty
        """
        if not stream_name:
            raise ValueError("Stream name must be provided")

        # This is just an alias for setup_stream for compatibility
        await self.setup_stream(stream_name, consumer_group, consumer_name)

    async def unsubscribe_from_stream(self, stream_name: str) -> None:
        """Remove stream from local tracking asynchronously (consumer group remains on Redis).

        Args:
            stream_name: Stream to unsubscribe from
        """
        try:
            # Ensure stream_name is a string
            stream_name = self._safe_decode(stream_name)
            self._streams.discard(stream_name)
            self._consumer_groups.pop(stream_name, None)
            self._consumer_names.pop(stream_name, None)
            logging.info("Successfully unsubscribed from async stream: %s", stream_name)
        except Exception as exc:
            logging.error("Failed to unsubscribe from async stream %s: %s", stream_name, str(exc))

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

    async def _recreate_consumer_group_async(self, stream_name: str, consumer_group: str) -> bool:
        """Recreate consumer group for a stream (handles NOGROUP recovery).

        This method is called when an XREADGROUP fails with NOGROUP error,
        indicating the consumer group or stream doesn't exist.

        Args:
            stream_name: Name of the Redis stream
            consumer_group: Name of the consumer group

        Returns:
            bool: True if successfully recreated, False otherwise
        """
        try:
            stream_name = self._safe_decode(stream_name)
            consumer_group = self._safe_decode(consumer_group)

            assert self.client is not None
            await self.client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
            logging.info(
                f"Recreated async consumer group '{consumer_group}' for stream '{stream_name}' after NOGROUP error"
            )
            return True
        except Exception as e:
            error_str = str(e)
            if "BUSYGROUP" in error_str:
                # Group was created by another process between error and retry
                logging.debug(f"Async consumer group '{consumer_group}' already exists (concurrent creation)")
                return True
            else:
                logging.error(f"Failed to recreate async consumer group: {error_str}")
                return False

    async def get_messages_batch(
        self,
        stream_name: Optional[str] = None,
        timeout: float = 0.001,
        count: int = 32
    ) -> List[Dict]:
        """Get multiple messages from Redis stream in a single batch.

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
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first.")

        # Determine which streams to read from
        if stream_name:
            if stream_name not in self._consumer_groups:
                raise RuntimeError(f"Stream '{stream_name}' not set up. Call setup_stream() first")
            streams_to_read = [stream_name]
        else:
            streams_to_read = list(self._streams)
            if not streams_to_read:
                raise RuntimeError("No streams configured. Call setup_stream() first")

        start_time = time.time()
        try:
            # Build streams dictionary for XREADGROUP
            first_stream = self._safe_decode(streams_to_read[0])
            primary_consumer_group = None
            primary_consumer_name = None

            for stored_stream in self._consumer_groups:
                if self._safe_decode(stored_stream) == first_stream:
                    primary_consumer_group = self._consumer_groups[stored_stream]
                    primary_consumer_name = self._consumer_names[stored_stream]
                    break

            if not primary_consumer_group or not primary_consumer_name:
                raise RuntimeError(f"Consumer group/name not found for stream '{first_stream}'")

            streams_dict = {}
            for stream in streams_to_read:
                stream_str = self._safe_decode(stream)
                streams_dict[stream_str] = '>'

            timeout_ms = int(timeout * 1000) if timeout > 0 else 0

            # XREADGROUP with COUNT for batch reading
            assert self.client is not None
            assert self.client is not None
            result = await self.client.xreadgroup(
                self._safe_decode(primary_consumer_group),
                self._safe_decode(primary_consumer_name),
                streams_dict,
                count=count,  # BATCH READ: Read up to N messages at once
                block=timeout_ms
            )

            end_time = time.time()

            if not result:
                return []

            # Parse all messages from result
            messages = []
            for stream_name_bytes, stream_messages in result:
                stream_name_str = self._safe_decode(stream_name_bytes)

                for message_id, fields in stream_messages:
                    message_id_str = self._safe_decode(message_id)

                    # Parse fields
                    parsed_data = {}
                    message_key = None
                    for field_name, field_value in fields.items():
                        field_name_str = self._safe_decode(field_name)

                        # Preserve binary content
                        if isinstance(field_value, bytes) and ('__content' in field_name_str or field_name_str == 'content'):
                            parsed_data[field_name_str] = field_value
                            continue

                        field_value_str = self._safe_decode(field_value)

                        if field_name_str == '_message_key':
                            message_key = field_value_str
                            continue

                        try:
                            parsed_data[field_name_str] = json.loads(field_value_str)
                        except (json.JSONDecodeError, ValueError):
                            parsed_data[field_name_str] = field_value_str

                    # Acknowledge message
                    try:
                        consumer_group = self._consumer_groups.get(stream_name_str)
                        if consumer_group:
                            await self.client.xack(stream_name_str, consumer_group, message_id_str)
                    except Exception:
                        pass  # Suppress ack errors for performance

                    messages.append({
                        "stream": stream_name_str,
                        "message_id": message_id_str,
                        "data": parsed_data,
                        "fields": {self._safe_decode(k): self._safe_decode(v, keep_binary=True) for k, v in fields.items()},
                        "message_key": message_key
                    })

            # Record batch metrics (single metric for entire batch)
            if messages:
                self._record_metric(
                    operation="read_batch",
                    stream=first_stream,
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=len(messages)
                )

            return messages

        except asyncio.TimeoutError:
            return []
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Failed to get async message batch: {str(exc)}"
            logging.error(error_msg, exc_info=True)

            self._record_metric(
                operation="read_batch",
                stream="(error)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None
            )
            raise RedisConnectionError(error_msg)

    async def get_message(self, stream_name: Optional[str] = None, timeout: float = 60.0) -> Optional[Dict]:
        """Get a single message from Redis stream asynchronously.
        
        Args:
            stream_name: Stream to read from (if None, reads from all configured streams)
            timeout: Maximum time to wait for message in seconds
            
        Returns:
            Message dictionary if available, None if no message received
            
        Raises:
            RuntimeError: If no streams are configured
            RedisConnectionError: If message retrieval fails
        """
        if not self.client:
            raise RuntimeError("Redis client not initialized. Call setup_client() first.")
        
        # Determine which streams to read from
        if stream_name:
            if stream_name not in self._consumer_groups:
                raise RuntimeError(f"Stream '{stream_name}' not set up. Call setup_stream() first")
            streams_to_read = [stream_name]
        else:
            streams_to_read = list(self._streams)
            if not streams_to_read:
                raise RuntimeError("No streams configured. Call setup_stream() first")
        
        start_time = time.time()
        try:
            # Build streams dictionary for XREADGROUP
            streams_dict = {}
            # For multi-stream setups, we'll use the first stream's consumer group/name
            # This is a limitation of Redis XREADGROUP when reading from multiple streams
            
            # Find the first stream and ensure it's decoded
            first_stream = self._safe_decode(streams_to_read[0])
            primary_consumer_group = None
            primary_consumer_name = None
            
            # Find consumer group and name, handling both bytes and string keys
            for stored_stream in self._consumer_groups:
                if self._safe_decode(stored_stream) == first_stream:
                    primary_consumer_group = self._consumer_groups[stored_stream]
                    primary_consumer_name = self._consumer_names[stored_stream]
                    break
            
            if not primary_consumer_group or not primary_consumer_name:
                raise RuntimeError(f"Consumer group/name not found for stream '{first_stream}'")
            
            for stream in streams_to_read:
                # Ensure stream names are strings, not bytes
                stream_str = self._safe_decode(stream)
                streams_dict[stream_str] = '>'  # Read new messages
            
            # Use XREADGROUP to read from streams
            timeout_ms = int(timeout * 1000) if timeout > 0 else 0
            
            # Ensure all dict keys and values are strings for Redis client
            clean_streams_dict: Dict[str, str] = {}
            for stream_name, stream_id in streams_dict.items():
                clean_streams_dict[self._safe_decode(stream_name)] = self._safe_decode(stream_id)  # type: ignore[arg-type,index,assignment]
            
            # Use the standard dict approach for async Redis client with NOGROUP recovery
            nogroup_retry_attempted = False
            result = None
            while True:
                try:
                    assert self.client is not None
                    result = await self.client.xreadgroup(
                        self._safe_decode(primary_consumer_group),
                        self._safe_decode(primary_consumer_name),
                        clean_streams_dict,
                        count=1,
                        block=timeout_ms
                    )
                    break  # Success, exit retry loop
                except Exception as xread_exc:
                    error_str = str(xread_exc)

                    # Check for NOGROUP error (stream or consumer group doesn't exist)
                    if "NOGROUP" in error_str and not nogroup_retry_attempted:
                        nogroup_retry_attempted = True
                        logging.warning(
                            f"NOGROUP error detected in async get_message, "
                            f"attempting to recreate consumer group: {error_str}"
                        )

                        # Recreate consumer group for the affected stream
                        recreate_success = await self._recreate_consumer_group_async(
                            first_stream,
                            primary_consumer_group
                        )

                        if recreate_success:
                            logging.info("Async consumer group recreated, retrying xreadgroup...")
                            continue  # Retry the xreadgroup call
                        else:
                            logging.error("Failed to recreate async consumer group, raising original error")
                            raise
                    else:
                        logging.error(f"xreadgroup failed: {xread_exc}")
                        raise
            
            end_time = time.time()
            
            if not result:
                # Record timeout as successful operation with no message
                self._record_metric(
                    operation="read",
                    stream="(timeout)",
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=None
                )
                return None
            
            # Extract the first message from the result
            stream_name, messages = result[0]
            if not messages:
                return None
            
            # Decode stream_name and message_id to strings immediately
            stream_name = self._safe_decode(stream_name)  # type: ignore[arg-type,assignment]
            message_id, fields = messages[0]
            message_id = self._safe_decode(message_id)  # type: ignore[arg-type,assignment]
            
            # Parse fields into structured data
            parsed_data = {}
            message_key = None
            total_size = 0

            for field_name, field_value in fields.items():
                field_name = self._safe_decode(field_name)

                # Skip UTF-8 decode for binary content fields to preserve raw bytes
                # This includes both direct 'content' fields and flattened '__content' fields
                if isinstance(field_value, bytes) and ('__content' in field_name or field_name == 'content'):
                    # Keep binary data as bytes (no UTF-8 decode)
                    total_size += len(field_name) + len(field_value)
                    parsed_data[field_name] = field_value
                    continue

                field_value = self._safe_decode(field_value)
                total_size += len(field_name) + len(field_value)

                if field_name == '_message_key':
                    message_key = field_value
                    continue

                # Try to parse JSON values
                try:
                    parsed_data[field_name] = json.loads(field_value)
                except (json.JSONDecodeError, ValueError):
                    parsed_data[field_name] = field_value
            
            # Record successful message retrieval metrics
            self._record_metric(
                operation="read",
                stream=stream_name,  # type: ignore[arg-type]
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=message_key,
                message_size=total_size
            )
            
            # Acknowledge the message
            try:
                consumer_group = self._consumer_groups[stream_name]  # type: ignore[index]
                assert self.client is not None
                await self.client.xack(stream_name, consumer_group, message_id)
            except Exception as ack_exc:
                logging.warning("Failed to acknowledge async message: %s", str(ack_exc))
            
            result = {
                "stream": stream_name,  # Already decoded
                "message_id": message_id,  # Already decoded
                "data": parsed_data,
                "fields": {self._safe_decode(k): self._safe_decode(v, keep_binary=True) for k, v in fields.items()},
                "message_key": message_key
            }
            return result
            
        except asyncio.TimeoutError:
            end_time = time.time()
            # Record timeout as successful operation with no message
            self._record_metric(
                operation="read",
                stream="(timeout)",
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
            logging.error(error_msg, exc_info=True)
            
            # Record error metrics
            self._record_metric(
                operation="read",
                stream="(error)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None
            )
            raise RedisConnectionError(error_msg)

    async def listen_for_messages(self, callback: Optional[Callable] = None, stream_name: Optional[str] = None) -> None:
        """Listen for messages on configured streams asynchronously (blocking).

        Args:
            callback: Optional callback function for all messages
            stream_name: Optional specific stream to listen to (listens to all if None)

        Raises:
            RuntimeError: If no streams are configured
            RedisConnectionError: If listening fails
        """
        if not self._streams:
            raise RuntimeError("No streams configured. Call setup_stream() first")

        try:
            logging.info("Starting to listen for async Redis stream messages...")
            while True:
                try:
                    message = await self.get_message(stream_name=stream_name, timeout=5.0)
                    if message:
                        # Execute callback
                        if callback:
                            try:
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(message)
                                else:
                                    callback(message)
                            except Exception as callback_exc:
                                logging.error("Error in async stream callback: %s", str(callback_exc))
                except RedisConnectionError as exc:
                    logging.error("Async Redis connection error while listening: %s", str(exc))
                    # Sleep briefly before retrying
                    await asyncio.sleep(1.0)
                except Exception as exc:
                    logging.error("Unexpected error while listening async: %s", str(exc))
                    await asyncio.sleep(1.0)
                            
        except asyncio.CancelledError:
            logging.info("Stopped listening for async Redis stream messages (cancelled)")
        except Exception as exc:
            error_msg = f"Error listening for async messages: {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    async def _flush_stream_batch(self, stream_name: str) -> None:
        """Flush pending batch for a specific stream using async pipeline.

        Args:
            stream_name: Name of the Redis stream to flush
        """
        if not self.client:
            return

        if self._batch_lock is None:
            return

        async with self._batch_lock:
            batch = self._batch_buffer.get(stream_name, [])
            if not batch:
                return

            # Clear the buffer for this stream
            self._batch_buffer[stream_name] = []
            self._last_flush_time[stream_name] = time.time()

        # Execute batch using pipeline (outside lock to minimize lock time)
        try:
            assert self.client is not None
            async with self.client.pipeline(transaction=False) as pipe:
                for fields, message_key in batch:
                    # Add to pipeline (let Redis auto-generate ID)
                    # message_key is already in fields as '_message_key', not a stream ID
                    if self.stream_maxlen:
                        pipe.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                    else:
                        pipe.xadd(stream_name, fields)

                # Execute all commands in batch
                await pipe.execute()

            logging.debug(f"Flushed batch of {len(batch)} messages to stream '{stream_name}'")
        except Exception as exc:
            logging.error(f"Error flushing async batch for stream '{stream_name}': {exc}")
            # Re-raise to allow caller to handle
            raise

    async def _flush_cross_stream_batch(self) -> int:
        """Flush ALL pending batches across ALL streams in a SINGLE Redis pipeline.

        This is a key optimization for high-camera-count scenarios (1000+).
        Instead of creating one pipeline per stream (O(n) RTT), this creates
        a single pipeline for ALL streams (O(1) RTT).

        Returns:
            Total number of messages flushed across all streams.
        """
        if not self.client:
            return 0

        if self._batch_lock is None:
            return 0

        # Collect all pending batches atomically
        all_batches = []  # List of (stream_name, fields, message_key)
        current_time = time.time()

        async with self._batch_lock:
            for stream_name, batch in self._batch_buffer.items():
                if not batch:
                    continue

                batch_size = len(batch)
                last_flush = self._last_flush_time.get(stream_name, 0)
                time_since_flush = current_time - last_flush

                # Include if batch is full or timeout reached
                if batch_size >= self.batch_size or time_since_flush >= self.batch_timeout:
                    for fields, message_key in batch:
                        all_batches.append((stream_name, fields, message_key))
                    # Clear this stream's buffer
                    self._batch_buffer[stream_name] = []
                    self._last_flush_time[stream_name] = current_time

        if not all_batches:
            return 0

        # Execute ALL messages in a SINGLE pipeline (O(1) RTT)
        try:
            assert self.client is not None
            async with self.client.pipeline(transaction=False) as pipe:
                for stream_name, fields, message_key in all_batches:
                    if self.stream_maxlen:
                        pipe.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                    else:
                        pipe.xadd(stream_name, fields)

                # Execute all commands in single round-trip
                await pipe.execute()

            logging.debug(f"Cross-stream batch flushed: {len(all_batches)} messages across streams")
            return len(all_batches)
        except Exception as exc:
            logging.error(f"Error in cross-stream batch flush: {exc}")
            raise

    async def _batch_flusher(self) -> None:
        """Background async task that periodically flushes batched messages.

        This runs as a long-lived asyncio task and flushes batches based on:
        - Batch size threshold
        - Timeout threshold

        When enable_cross_stream_batching is True, uses a single Redis pipeline
        for ALL streams (O(1) RTT instead of O(n) RTT).
        """
        mode = "cross-stream" if self.enable_cross_stream_batching else "per-stream"
        logging.info(f"Async Redis batch flusher task started (mode={mode}, interval={self.flusher_interval*1000:.0f}ms)")

        while True:
            try:
                # Check if we should stop
                if self._batch_stop_event and self._batch_stop_event.is_set():
                    logging.info("Async batch flusher stopping")
                    break

                # Sleep for configured interval
                await asyncio.sleep(self.flusher_interval)

                if not self.client or self._batch_lock is None:
                    continue

                # Use cross-stream batching for high throughput (O(1) RTT)
                if self.enable_cross_stream_batching:
                    try:
                        await self._flush_cross_stream_batch()
                    except Exception as exc:
                        logging.error(f"Error in cross-stream batch flush: {exc}")
                else:
                    # Legacy per-stream batching (O(n) RTT)
                    current_time = time.time()
                    streams_to_flush = []

                    # Check which streams need flushing
                    async with self._batch_lock:
                        for stream_name, batch in self._batch_buffer.items():
                            if not batch:
                                continue

                            batch_size = len(batch)
                            last_flush = self._last_flush_time.get(stream_name, 0)
                            time_since_flush = current_time - last_flush

                            # Flush if batch is full or timeout reached
                            if batch_size >= self.batch_size or time_since_flush >= self.batch_timeout:
                                streams_to_flush.append(stream_name)

                    # Flush streams outside the check lock
                    for stream_name in streams_to_flush:
                        try:
                            await self._flush_stream_batch(stream_name)
                        except Exception as exc:
                            logging.error(f"Error in async batch flusher for stream '{stream_name}': {exc}")

            except asyncio.CancelledError:
                logging.info("Async batch flusher task cancelled")
                break
            except Exception as exc:
                logging.error(f"Unexpected error in async batch flusher: {exc}")
                await asyncio.sleep(1.0)  # Back off on error

        # Final flush on exit
        logging.info("Async batch flusher performing final flush")
        try:
            await self.flush_pending_messages()
        except Exception as exc:
            logging.error(f"Error in final async batch flush: {exc}")

        logging.info("Async Redis batch flusher task stopped")

    async def flush_pending_messages(self) -> None:
        """Manually flush all pending batched messages for all streams.

        This is useful when you want to ensure all messages are sent immediately,
        such as before closing the connection or at critical points.
        """
        if not self.client or self._batch_lock is None:
            return

        # Get list of streams to flush
        async with self._batch_lock:
            streams_to_flush = list(self._batch_buffer.keys())

        # Flush each stream
        for stream_name in streams_to_flush:
            try:
                await self._flush_stream_batch(stream_name)
            except Exception as exc:
                logging.error(f"Error flushing async stream '{stream_name}': {exc}")

    async def add_messages_batch(
        self,
        stream_name: str,
        messages: List[Dict[str, Any]],
        message_keys: Optional[List[Optional[str]]] = None
    ) -> List[str]:
        """Add multiple messages to a stream in a single batch operation.

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
        if not self.client:
            await self.setup_client()

        if not messages:
            return []

        # Ensure message_keys list matches messages length
        if message_keys is None:
            message_keys = [None] * len(messages)
        elif len(message_keys) != len(messages):
            raise ValueError("message_keys length must match messages length")

        try:
            message_ids = []

            assert self.client is not None
            async with self.client.pipeline(transaction=False) as pipe:
                for message, message_key in zip(messages, message_keys):
                    # Prepare fields (same logic as add_message)
                    if isinstance(message, dict):
                        fields: Dict[str, Any] = {}
                        for k, v in message.items():
                            key_str = self._safe_decode(k)
                            if isinstance(v, (dict, list)):
                                fields[key_str] = json.dumps(v).encode('utf-8')
                            elif isinstance(v, bytes):
                                # Store binary data directly (NO base64 encoding)
                                fields[key_str] = v
                            else:
                                fields[key_str] = str(v).encode('utf-8')

                        if message_key:
                            fields['_message_key'] = message_key.encode('utf-8')
                    else:
                        if isinstance(message, bytes):
                            fields = {'data': message}
                        else:
                            fields = {'data': str(message).encode('utf-8')}

                        if message_key:
                            fields['_message_key'] = message_key.encode('utf-8')

                    # Add to pipeline (let Redis auto-generate ID)
                    # message_key is already in fields as '_message_key', not a stream ID
                    if self.stream_maxlen:
                        pipe.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                    else:
                        pipe.xadd(stream_name, fields)

                # Execute all at once
                results = await pipe.execute()
                message_ids = [self._safe_decode(mid) for mid in results]

            return message_ids

        except Exception as exc:
            error_msg = f"Failed to add async message batch to stream '{stream_name}': {str(exc)}"
            logging.error(error_msg)
            raise RedisConnectionError(error_msg)

    async def add_frame(
        self,
        stream_name: str,
        frame_data: bytes,
        metadata: Optional[Dict[str, Any]] = None,
        message_key: Optional[str] = None
    ) -> str:
        """Optimized method for adding video frame data to a stream.

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
        if not self.client:
            await self.setup_client()

        # Build message with raw frame data
        fields: Dict[str, Any] = {
            'content': frame_data,  # Raw bytes - NO base64 encoding
            'content_type': b'frame',
            'size': str(len(frame_data)).encode('utf-8'),
            'timestamp': str(time.time()).encode('utf-8')
        }

        # Add metadata if provided
        if metadata:
            for k, v in metadata.items():
                key_str = self._safe_decode(k)
                if isinstance(v, (dict, list)):
                    fields[key_str] = json.dumps(v).encode('utf-8')
                elif isinstance(v, bytes):
                    fields[key_str] = v
                else:
                    fields[key_str] = str(v).encode('utf-8')

        if message_key:
            fields['_message_key'] = message_key.encode('utf-8')

        # Use batching if enabled
        if self.enable_batching and self._batch_lock is not None:
            async with self._batch_lock:
                # Initialize stream buffer if needed
                if stream_name not in self._batch_buffer:
                    self._batch_buffer[stream_name] = []
                    self._last_flush_time[stream_name] = time.time()

                # Add to batch
                self._batch_buffer[stream_name].append((fields, message_key))

                # Check if we should flush immediately
                should_flush = len(self._batch_buffer[stream_name]) >= self.batch_size

            if should_flush:
                await self._flush_stream_batch(stream_name)

            # Return placeholder ID (actual ID assigned during flush)
            return f"{stream_name}:batched:{int(time.time() * 1000000)}"
        else:
            # Direct write without batching
            try:
                assert self.client is not None
                if message_key:
                    if self.stream_maxlen:
                        message_id = await self.client.xadd(stream_name, fields, id=message_key, maxlen=self.stream_maxlen, approximate=True)
                    else:
                        message_id = await self.client.xadd(stream_name, fields, id=message_key)
                else:
                    if self.stream_maxlen:
                        message_id = await self.client.xadd(stream_name, fields, maxlen=self.stream_maxlen, approximate=True)
                    else:
                        message_id = await self.client.xadd(stream_name, fields)

                return self._safe_decode(message_id)
            except Exception as exc:
                error_msg = f"Failed to add async frame to stream '{stream_name}': {str(exc)}"
                logging.error(error_msg)
                raise RedisConnectionError(error_msg)

    async def close(self) -> None:
        """Close async Redis client connections."""
        errors = []
        
        # Stop background metrics reporting first
        try:
            self.stop_metrics_reporting()
        except Exception as exc:
            error_msg = f"Error stopping async Redis metrics reporting: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        # Stop batching task and flush pending messages
        if self._batch_task and not self._batch_task.done():
            try:
                logging.info("Stopping async batch flusher task...")
                # Signal the task to stop
                if self._batch_stop_event:
                    self._batch_stop_event.set()

                # Wait for task to complete gracefully (with timeout)
                try:
                    await asyncio.wait_for(self._batch_task, timeout=5.0)
                except asyncio.TimeoutError:
                    logging.warning("Batch flusher task did not stop in time, cancelling")
                    self._batch_task.cancel()
                    try:
                        await self._batch_task
                    except asyncio.CancelledError:
                        pass

                logging.info("Async batch flusher task stopped")
            except Exception as exc:
                error_msg = f"Error stopping async batch flusher: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)

        # Check if event loop is still running
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                logging.warning("Event loop is closed, skipping async Redis cleanup")
                self.client = None
                return
        except RuntimeError:
            logging.warning("No running event loop, skipping async Redis cleanup")
            self.client = None
            return
        
        # Clear stream tracking
        if self._streams:
            try:
                self._streams.clear()
                self._consumer_groups.clear()
                self._consumer_names.clear()
                logging.debug("Cleared async stream tracking")
            except Exception as exc:
                error_msg = f"Error clearing async stream tracking: {str(exc)}"
                logging.warning(error_msg)
                errors.append(error_msg)
                
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
        consumer_group: Optional[str] = None,
        enable_metrics: bool = True,
        metrics_interval: int = 60
    ) -> None:
        """Initialize Redis streams deployment with deployment ID.

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
        self.session = session
        self.rpc = session.rpc
        self.service_id = service_id
        self.type = type
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.db = db

        self.setup_success = True
        self.request_stream = f"{service_id}_requests"
        self.result_stream = f"{service_id}_results"
        self.publishing_stream: Optional[str] = None
        self.subscribing_stream: Optional[str] = None

        # Consumer group configuration
        self.consumer_group = consumer_group or f"{service_id}_{type}_group"

        # Initialize Redis utilities as None - create as needed
        self.sync_redis: Optional[RedisUtils] = None
        self.async_redis: Optional[AsyncRedisUtils] = None
        
        # Initialize metrics configuration
        self._metrics_config: Optional[Dict[str, Any]] = None

        # Configure streams based on deployment type
        if self.type == "client":
            self.publishing_stream = self.request_stream
            self.subscribing_stream = self.result_stream
        elif self.type == "server":
            self.publishing_stream = self.result_stream
            self.subscribing_stream = self.request_stream
        else:
            raise ValueError("Invalid type: must be 'client' or 'server'")

        logging.info(
            "Initialized MatriceRedisDeployment: deployment_id=%s, type=%s, host=%s:%d, consumer_group=%s",
            service_id, type, host, port, self.consumer_group
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
        all_metrics: Dict[str, Any] = {
            'sync_metrics': [],
            'async_metrics': [],
            'deployment_info': {
                'type': self.type,
                'setup_success': self.setup_success,
                'publishing_stream': getattr(self, 'publishing_stream', None),
                'subscribing_stream': getattr(self, 'subscribing_stream', None),
                'consumer_group': getattr(self, 'consumer_group', None)
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
                db=self.db
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
        """Ensure sync Redis stream subscriber is set up."""
        if not self._ensure_sync_client():
            return False
        
        try:
            # Check if stream is already set up
            if self.subscribing_stream not in self.sync_redis._streams:
                self.sync_redis.setup_stream(
                    stream_name=self.subscribing_stream,
                    consumer_group=self.consumer_group,
                    consumer_name=f"{self.service_id}_{self.type}_sync"
                )
            return True
        except Exception as exc:
            logging.error("Failed to set up sync Redis stream subscriber: %s", str(exc))
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
        """Ensure async Redis stream subscriber is set up.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        if not await self._ensure_async_client():
            return False
        
        try:
            # Check if stream is already set up
            if self.subscribing_stream not in self.async_redis._streams:
                await self.async_redis.setup_stream(
                    stream_name=self.subscribing_stream,
                    consumer_group=self.consumer_group,
                    consumer_name=f"{self.service_id}_{self.type}_async"
                )
            return True
        except Exception as exc:
            logging.error("Failed to set up async Redis stream subscriber: %s", str(exc))
            return False

    def _parse_message(self, result: dict) -> dict:
        """Handle message parsing for consistency."""
        if not result:
            return result
        # Redis messages are already parsed by the utility classes
        return result

    def publish_message(self, message: dict, timeout: float = 60.0) -> str:
        """Add a message to Redis stream.

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
        if not self._ensure_sync_client():
            raise RuntimeError("Failed to set up Redis client")
        assert self.sync_redis is not None
        assert self.publishing_stream is not None
        return self.sync_redis.add_message(self.publishing_stream, message, timeout=timeout)

    def get_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Get a message from Redis stream.

        Args:
            timeout: Maximum time to wait for message in seconds
            
        Returns:
            Message dictionary if available, None if no message received
            
        Raises:
            RuntimeError: If subscriber is not initialized
            RedisConnectionError: If message retrieval fails
        """
        if not self._ensure_sync_subscriber():
            logging.warning("Redis stream subscriber setup unsuccessful, returning None for get request")
            return None

        assert self.sync_redis is not None
        assert self.subscribing_stream is not None
        raw = self.sync_redis.get_message(stream_name=self.subscribing_stream, timeout=timeout)
        return self._parse_message(raw) if raw is not None else None

    async def async_publish_message(self, message: dict, timeout: float = 60.0) -> str:
        """Add a message to Redis stream asynchronously.

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
        if not await self._ensure_async_client():
            raise RuntimeError("Failed to set up async Redis client")
        assert self.async_redis is not None
        assert self.publishing_stream is not None
        return await self.async_redis.add_message(self.publishing_stream, message, timeout=timeout)

    async def async_get_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Get a message from Redis stream asynchronously.

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
                logging.warning("Async Redis stream subscriber setup unsuccessful, returning None for get request")
                return None

            assert self.async_redis is not None
            assert self.subscribing_stream is not None
            raw = await self.async_redis.get_message(stream_name=self.subscribing_stream, timeout=timeout)
            return self._parse_message(raw) if raw is not None else None
        except RuntimeError as exc:
            logging.error("Runtime error in async_get_message: %s", str(exc), exc_info=True)
            return None
        except Exception as exc:
            logging.error("Unexpected error in async_get_message: %s", str(exc), exc_info=True)
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