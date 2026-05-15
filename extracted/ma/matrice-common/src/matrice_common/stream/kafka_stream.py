"""Module providing synchronous and asynchronous Kafka utilities."""

import asyncio
import json
import logging
import os
import threading
import time
import uuid
from collections import deque
from datetime import datetime, timezone
from typing import Any, Deque, Dict, List, Optional, Tuple, Union

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.consumer.subscription_state import ConsumerRebalanceListener
from aiokafka.errors import KafkaError as AsyncKafkaError
from confluent_kafka import OFFSET_INVALID, Consumer, KafkaError, Producer, TopicPartition
from confluent_kafka.admin import AdminClient, NewTopic

from matrice_common.stream._stream_helpers import (
    MetricsReporterMixin,
    aggregate_kafka_metrics,
    parse_message_value,
    serialize_key,
    serialize_value,
)

logger = logging.getLogger(__name__)


class AsyncRebalanceListener(ConsumerRebalanceListener):
    """Top-level listener for async partition rebalance events."""

    def __init__(self, consumer, parent) -> None:
        self.consumer = consumer
        self.parent = parent

    async def on_partitions_assigned(self, partitions):
        if partitions:
            logging.info(f"Async consumer rebalanced with {len(partitions)} partition(s) assigned")
            try:
                # committed = await self.consumer.committed(partitions)
                # for tp, offset in committed.items():
                #     if offset == OFFSET_INVALID:
                #         logging.info(f"No offset for {tp.topic}:{tp.partition}, seeking to beginning")
                #         await self.consumer.seek(TopicPartition(tp.topic, tp.partition, 0))
                #     else:
                #         logging.info(f"Resuming {tp.topic}:{tp.partition} at offset {offset}")
                pass
            except Exception as e:
                logging.warning(f"Error checking committed offsets: {str(e)}")
            if self.parent._assigned is not None:
                self.parent._assigned.set()
        else:
            logging.warning("Async consumer rebalanced but no partitions were assigned")

    async def on_partitions_revoked(self, revoked):
        logging.info(f"Async consumer partitions revoked: {len(revoked)} partition(s)")
        if self.parent._assigned is not None:
            self.parent._assigned.clear()


class KafkaUtils(MetricsReporterMixin):
    """Utility class for synchronous Kafka operations."""

    def __init__(
        self,
        bootstrap_servers: str,
        sasl_mechanism: Optional[str] = "SCRAM-SHA-256",
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        security_protocol: str = "SASL_PLAINTEXT",
    ) -> None:
        """Initialize Kafka utils with bootstrap servers and SASL configuration.

        Args:
            bootstrap_servers: Comma-separated list of Kafka broker addresses
            sasl_mechanism: SASL mechanism for authentication
            sasl_username: Username for SASL authentication
            sasl_password: Password for SASL authentication
            security_protocol: Security protocol for Kafka connection
        """
        self.bootstrap_servers = bootstrap_servers
        self.sasl_mechanism = sasl_mechanism
        self.sasl_username = sasl_username or os.environ.get("KAFKA_SASL_USERNAME")
        self.sasl_password = sasl_password or os.environ.get("KAFKA_SASL_PASSWORD")
        self.security_protocol = security_protocol
        self.producer: Optional[Producer] = None
        self.consumer: Optional[Consumer] = None
        self._consumer_config: Optional[Dict[str, Any]] = None
        self._consumer_topics: Optional[List[str]] = None
        self._consumer_group_id: Optional[str] = None
        self._assigned = False

        # Metrics collection for performance monitoring
        self._metrics_lock = threading.Lock()
        self._metrics_log: Deque[Dict[str, Any]] = deque(maxlen=10000)  # Keep last 10000 metrics entries
        self._pending_produces: Dict[str, Any] = {}  # Track pending produce operations for delivery timing
        self._pending_lock = threading.Lock()  # Protect _pending_produces for callback concurrency

        # Background metrics reporting
        self._metrics_reporting_config: Optional[Dict[str, Any]] = None
        self._metrics_thread: Optional[threading.Thread] = None
        self._metrics_stop_event = threading.Event()
        self._last_metrics_reset = time.time()

        logging.info(
            "Initialized KafkaUtils with servers: %s",
            bootstrap_servers,
        )

    def _record_metric(
        self,
        operation: str,
        topic: str,
        start_time: float,
        end_time: float,
        success: bool,
        error_msg: Optional[str] = None,
        message_key: Optional[str] = None,
        message_size: Optional[int] = None,
    ) -> None:
        """Record a performance metric for aggregation."""
        duration_ms = (end_time - start_time) * 1000

        metric = {
            "timestamp": end_time,
            "operation": operation,
            "topic": topic,
            "duration_ms": duration_ms,
            "success": success,
            "error_msg": error_msg,
            "message_key": message_key,
            "message_size": message_size,
            "bootstrap_servers": self.bootstrap_servers,
            "type": "sync",
        }

        with self._metrics_lock:
            self._metrics_log.append(metric)

        self._log_kafka_metric("Kafka", operation, topic, duration_ms, success, error_msg, message_key, message_size)

    @staticmethod
    def _log_kafka_metric(
        prefix: str,
        operation: str,
        topic: str,
        duration_ms: float,
        success: bool,
        error_msg: Optional[str],
        message_key: Optional[str],
        message_size: Optional[int],
    ) -> None:
        """Log a Kafka metric summary line."""
        status = "SUCCESS" if success else "FAILED"
        logging.info(
            "%s %s %s: topic=%s, duration=%.2fms, key=%s, size=%s%s",
            prefix,
            operation.upper(),
            status,
            topic,
            duration_ms,
            message_key or "None",
            message_size or "Unknown",
            f", error={error_msg}" if error_msg else "",
        )

    def configure_metrics_reporting(
        self, rpc_client, service_id: Optional[str] = None, interval: int = 120, batch_size: int = 1000
    ) -> None:
        """Configure background metrics reporting to backend API.

        Args:
            rpc_client: RPC client instance for API communication
            service_id: Deployment identifier for metrics context
            interval: Reporting interval in seconds (default: 120)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        self._metrics_reporting_config = {
            "rpc_client": rpc_client,
            "deployment_id": service_id,
            "interval": interval,
            "batch_size": batch_size,
            "enabled": True,
        }
        self._start_metrics_reporter(f"kafka-metrics-reporter-{id(self)}")
        logging.info("Started background Kafka metrics reporting thread")

    def _extract_ip_port_from_bootstrap(self) -> Tuple[str, str]:
        """Extract IP and port from bootstrap_servers."""
        try:
            first_server = self.bootstrap_servers.split(",")[0].strip()
            if ":" in first_server:
                ip, port = first_server.split(":", 1)
                return ip.strip(), port.strip()
            else:
                return first_server.strip(), "9092"
        except Exception:
            return "unknown", "unknown"

    def _aggregate_metrics_for_api(self, raw_metrics: List[Dict]) -> Dict:
        """Aggregate raw metrics into the API format expected by backend."""
        ip, port = self._extract_ip_port_from_bootstrap()
        return aggregate_kafka_metrics(raw_metrics, ip, port)

    def _get_reporter_label(self) -> str:
        return "Kafka"

    def _get_metrics_collection_key(self) -> str:
        return "topic"

    def _get_api_path(self) -> str:
        return "/v1/monitoring/add_kafka_metrics"

    def setup_producer(self, config: Optional[Dict] = None) -> None:
        """Set up Kafka producer with optional config.

        Args:
            config: Additional producer configuration

        Raises:
            KafkaError: If producer initialization fails
        """
        producer_config = {
            "bootstrap.servers": self.bootstrap_servers,
            "acks": "1",
            "retries": 1,
            "retry.backoff.ms": 100,
            "max.in.flight.requests.per.connection": 1,
            "linger.ms": 50,
            "batch.size": 8388608,  # 8MB
            "queue.buffering.max.ms": 50,
            "message.max.bytes": 25000000,  # 25MB
            "queue.buffering.max.messages": 100000,
            "delivery.timeout.ms": 600000,
            "request.timeout.ms": 600000,
            "compression.type": "snappy",
        }

        # Add SASL authentication if configured
        if self.sasl_mechanism and self.sasl_username and self.sasl_password:
            producer_config.update(
                {
                    "security.protocol": self.security_protocol,
                    "sasl.mechanism": self.sasl_mechanism,
                    "sasl.username": self.sasl_username,
                    "sasl.password": self.sasl_password,
                }
            )

        if config:
            producer_config.update(config)
        try:
            self.producer = Producer(producer_config)
            logging.info("Successfully set up Kafka producer")
        except KafkaError as exc:
            error_msg = f"Failed to initialize producer: {str(exc)}"
            logging.error(error_msg)
            raise

    def _on_assign_callback(self, consumer, partitions):
        """Callback for when partitions are assigned to the consumer.

        Args:
            consumer: The consumer instance
            partitions: List of assigned partitions
        """
        if partitions:
            logging.info(f"Consumer rebalanced with {len(partitions)} partition(s) assigned")

            try:
                # Check committed offsets for each partition
                # committed = consumer.committed(partitions, timeout=5.0)
                # for tp in committed:
                #     if tp.offset == OFFSET_INVALID:
                #         # No offset saved for this partition, seek to beginning
                #         logging.info(f"No offset for {tp.topic}:{tp.partition}, seeking to beginning")
                #         try:
                #             consumer.seek(TopicPartition(tp.topic, tp.partition, 0))
                #             consumer.poll(0)
                #         except KafkaError as e:
                #             logging.warning(f"Failed to seek to beginning for {tp.topic}:{tp.partition}: {str(e)}")
                #     else:
                #         logging.info(f"Resuming {tp.topic}:{tp.partition} at offset {tp.offset}")
                pass
            except KafkaError as e:
                logging.warning(f"Error checking committed offsets: {str(e)}")

            self._assigned = True
        else:
            logging.warning("Consumer rebalanced but no partitions were assigned")

    def _wait_for_assignment(self, max_wait_time=600):
        """Wait for partition assignment to complete.

        Args:
            max_wait_time: Maximum time to wait in seconds
        """
        start_time = time.time()

        while not self._assigned and time.time() - start_time < max_wait_time:
            # Poll with a short timeout to allow callbacks to be processed
            self.consumer.poll(0.1)

        if not self._assigned:
            logging.warning(f"Consumer rebalancing timed out after {max_wait_time} seconds")
            # Final check for assignment
            assignment = self.consumer.assignment()
            if assignment:
                logging.info(f"Consumer has {len(assignment)} partition(s) assigned after timeout")
                self._assigned = True
            else:
                logging.warning("Consumer has no partitions assigned after rebalancing timeout")

    def setup_consumer(
        self,
        topics: List[str],
        group_id: str,
        group_instance_id: Optional[str] = None,
        config: Optional[Dict] = None,
    ) -> None:
        """Set up Kafka consumer for given topics.

        Args:
            topics: List of topics to subscribe to
            group_id: Consumer group ID
            group_instance_id: Consumer group instance ID for static membership
            config: Additional consumer configuration

        Raises:
            KafkaError: If consumer initialization or subscription fails
            ValueError: If topics list is empty
        """
        if not topics:
            raise ValueError("Topics list cannot be empty")
        consumer_config = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
            "session.timeout.ms": 60000,
            "heartbeat.interval.ms": 20000,
            "max.poll.interval.ms": 600000,
            "fetch.max.bytes": 25000000,
            "max.partition.fetch.bytes": 25000000,
            "partition.assignment.strategy": "cooperative-sticky",
        }

        # Add SASL authentication if configured
        if self.sasl_mechanism and self.sasl_username and self.sasl_password:
            consumer_config.update(
                {
                    "security.protocol": self.security_protocol,
                    "sasl.mechanism": self.sasl_mechanism,
                    "sasl.username": self.sasl_username,
                    "sasl.password": self.sasl_password,
                }
            )

        if group_instance_id:
            consumer_config["group.instance.id"] = group_instance_id
        if config:
            consumer_config.update(config)

        # Store configuration for potential reconnection
        self._consumer_config = consumer_config
        self._consumer_topics = topics
        self._consumer_group_id = group_id
        self._assigned = False

        try:
            self.consumer = Consumer(consumer_config)

            # Subscribe with the callback
            consumer = self.consumer
            if consumer is not None:
                consumer.subscribe(topics, on_assign=self._on_assign_callback)

            # Wait for assignment to complete
            self._wait_for_assignment()

            logging.info(
                "Successfully set up Kafka consumer for topics: %s",
                topics,
            )
        except KafkaError as exc:
            error_msg = f"Failed to initialize consumer: {str(exc)}"
            logging.error(error_msg)
            raise

    def _reconnect_consumer(self) -> None:
        """Reconnect the consumer if it's disconnected.

        Raises:
            KafkaError: If consumer reconnection fails
            RuntimeError: If consumer was never set up
        """
        if not self._consumer_config or not self._consumer_topics:
            raise RuntimeError("Cannot reconnect consumer that was never set up")

        try:
            logging.info("Attempting to reconnect Kafka consumer")
            if self.consumer:
                try:
                    self.consumer.close()
                except Exception:
                    pass  # Ignore errors during close of potentially broken consumer

            self._assigned = False
            self.consumer = Consumer(self._consumer_config)

            # Subscribe with the callback
            self.consumer.subscribe(self._consumer_topics, on_assign=self._on_assign_callback)

            # Wait for assignment to complete
            self._wait_for_assignment()

            logging.info("Successfully reconnected Kafka consumer")
        except KafkaError as exc:
            error_msg = f"Failed to reconnect consumer: {str(exc)}"
            logging.error(error_msg)
            raise

    @staticmethod
    def _serialize_value(value: Any) -> bytes:
        """Serialize message value to bytes."""
        return serialize_value(value)

    @staticmethod
    def _serialize_key(key: Any) -> Optional[bytes]:
        """Serialize message key to bytes."""
        return serialize_key(key)

    def produce_message(
        self,
        topic: str,
        value: Union[dict, str, bytes, Any],
        key: Optional[Union[str, bytes, Any]] = None,
        headers: Optional[List[Tuple]] = None,
        timeout: float = 30.0,
        wait_for_delivery: bool = False,
    ) -> None:
        """Produce message to Kafka topic.

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
        if not self.producer:
            raise RuntimeError("Producer not initialized. Call setup_producer() first")
        if not topic or value is None:
            raise ValueError("Topic and value must be provided")

        # Generate unique ID for tracking delivery timing and embed into value
        message_id = str(uuid.uuid4())
        tracking_field = "_msg_id"

        # Attempt to embed the message_id into the value
        value_bytes: Optional[bytes] = None
        id_embedded = False
        if isinstance(value, dict):
            value_with_id = dict(value)
            value_with_id[tracking_field] = message_id
            value_bytes = self._serialize_value(value_with_id)
            id_embedded = True
        elif isinstance(value, (str, bytes)):
            try:
                raw_str = value if isinstance(value, str) else value.decode("utf-8")
                obj = json.loads(raw_str)
                if isinstance(obj, dict):
                    obj[tracking_field] = message_id
                    value_bytes = json.dumps(obj).encode("utf-8")
                    id_embedded = True
            except Exception:
                value_bytes = None
            if value_bytes is None:
                # Fallback to original value if not JSON or failed to inject
                value_bytes = self._serialize_value(value)
        else:
            value_bytes = self._serialize_value(value)

        # Serialize key and compute sizes
        key_bytes = self._serialize_key(key)
        message_size = len(value_bytes) if value_bytes else 0
        message_key = key_bytes.decode("utf-8") if isinstance(key_bytes, bytes) else str(key) if key else None

        start_time = time.time()

        # Store produce info for delivery callback
        if id_embedded:
            produce_info = {
                "topic": topic,
                "start_time": start_time,
                "message_key": message_key,
                "message_size": message_size,
            }
            with self._pending_lock:
                self._pending_produces[message_id] = produce_info

        # Note: headers are intentionally not used for correlation/metrics

        try:
            # Check queue length before producing
            queue_len = len(self.producer)
            if queue_len > 40000:
                logging.warning(f"Producer queue is getting full: {queue_len} messages")
                # Perform aggressive polling to drain queue
                for _ in range(10):
                    self.producer.poll(0.001)
                    if len(self.producer) < 30000:
                        break
                    time.sleep(0.001)

            self.producer.produce(
                topic,
                value=value_bytes,
                key=key_bytes,
                on_delivery=self._delivery_callback,
            )
            # Poll to trigger delivery callbacks and handle any queued messages
            self.producer.poll(0)

            if wait_for_delivery:
                remaining = int(self.producer.flush(timeout=timeout))
                if remaining > 0:
                    # Clean up pending produce on timeout
                    with self._pending_lock:
                        self._pending_produces.pop(message_id, None)
                    raise KafkaError(f"Failed to deliver {remaining} messages within timeout")

            logging.debug(
                "Successfully queued message for production to topic: %s",
                topic,
            )
        except KafkaError as exc:
            # Clean up pending produce on error and record failure immediately
            with self._pending_lock:
                self._pending_produces.pop(message_id, None)
            end_time = time.time()
            error_msg = f"Failed to produce message: {str(exc)}"
            logging.error(error_msg)

            self._record_metric(
                operation="produce",
                topic=topic,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=message_key,
                message_size=message_size,
            )
            raise

    @staticmethod
    def _extract_msg_id(msg) -> Optional[str]:
        """Extract _msg_id from a Kafka message value, or None."""
        try:
            raw_val = msg.value()
            if raw_val:
                obj = json.loads(raw_val.decode("utf-8"))
                if isinstance(obj, dict) and "_msg_id" in obj:
                    return str(obj.get("_msg_id"))
        except Exception:
            pass
        return None

    def _record_delivery_metric(self, message_id: str, err) -> None:
        """Record delivery metric for a pending produce by message_id."""
        produce_info = None
        with self._pending_lock:
            if message_id in self._pending_produces:
                produce_info = self._pending_produces.pop(message_id)
        if produce_info is not None:
            self._record_metric(
                operation="produce",
                topic=produce_info["topic"],
                start_time=produce_info["start_time"],
                end_time=time.time(),
                success=err is None,
                error_msg=str(err) if err else None,
                message_key=produce_info["message_key"],
                message_size=produce_info["message_size"],
            )

    def _delivery_callback(self, err, msg):
        """Callback for message delivery reports."""
        message_id = self._extract_msg_id(msg)

        if message_id:
            self._record_delivery_metric(message_id, err)

        if err is not None:
            logging.error("Message delivery failed: %s", str(err))
        else:
            logging.debug("Message delivered to %s [%d] at offset %d", msg.topic(), msg.partition(), msg.offset())

    @staticmethod
    def _parse_message_value(value: bytes) -> Any:
        """Parse message value from bytes."""
        return parse_message_value(value)

    def consume_message(self, timeout: float = 1.0) -> Optional[Dict]:
        """Consume single message from subscribed topics.

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
        if not self.consumer:
            raise RuntimeError("Consumer not initialized. Call setup_consumer() first")

        # Time only the actual poll operation
        start_time = time.time()
        try:
            msg = self.consumer.poll(timeout)
            end_time = time.time()

            if msg is None:
                # Record timeout as successful operation with no message
                self._record_metric(
                    operation="consume",
                    topic="(timeout)",
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=None,
                )
                return None

            topic = msg.topic()

            if msg.error():
                error_msg = f"Consumer error: {msg.error()}"
                logging.error(error_msg)

                # Record error metrics
                self._record_metric(
                    operation="consume",
                    topic=topic,
                    start_time=start_time,
                    end_time=end_time,
                    success=False,
                    error_msg=error_msg,
                    message_key=None,
                    message_size=None,
                )

                # Check if the error indicates a disconnection
                if msg.error().code() in (
                    KafkaError._TIMED_OUT,
                    KafkaError.NETWORK_EXCEPTION,
                    KafkaError._TRANSPORT,
                    KafkaError._TIMED_OUT,
                    KafkaError._MAX_POLL_EXCEEDED,
                ):
                    logging.warning("Kafka consumer disconnected, attempting to reconnect")
                    self._reconnect_consumer()
                    return None

                # Create a KafkaError instance with the error code, not the string
                raise KafkaError(msg.error().code())

            # Parse the message value
            value = self._parse_message_value(msg.value())
            message_size = len(msg.value()) if msg.value() else 0
            message_key = (
                msg.key().decode("utf-8")
                if msg.key() and isinstance(msg.key(), bytes)
                else str(msg.key())
                if msg.key()
                else None
            )

            # Record successful consumption metrics
            self._record_metric(
                operation="consume",
                topic=topic,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=message_key,
                message_size=message_size,
            )

            result = {
                "topic": msg.topic(),
                "partition": msg.partition(),
                "offset": msg.offset(),
                "key": msg.key(),
                "value": value,
                "headers": msg.headers(),
                "timestamp": msg.timestamp(),
            }
            return result
        except KafkaError as exc:
            end_time = time.time()
            error_msg = f"Failed to consume message: {str(exc)}"
            logging.error(error_msg)

            # Record error metrics
            self._record_metric(
                operation="consume",
                topic="(error)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None,
            )

            # Try to reconnect if it's a connection-related error
            if exc.code() in (
                KafkaError._TIMED_OUT,
                KafkaError.NETWORK_EXCEPTION,
                KafkaError._TRANSPORT,
                KafkaError._TIMED_OUT,
                KafkaError._MAX_POLL_EXCEEDED,
            ):
                logging.warning("Kafka consumer error, attempting to reconnect")
                try:
                    self._reconnect_consumer()
                    return None
                except Exception as reconnect_exc:
                    logging.error("Failed to reconnect consumer: %s", str(reconnect_exc))

            raise

    # New functions

    def create_topic_dynamic(
        self,
        topic: str,
        partitions: int,
        replication: int,
        kafka_ip: Optional[str] = None,
        kafka_port: Optional[str] = None,
    ) -> bool:
        """Create a Kafka topic dynamically - equivalent to Go CreateTopic().

        Args:
            topic: Topic name to create
            partitions: Number of partitions
            replication: Replication factor
            kafka_ip: Kafka server IP (optional, uses existing bootstrap_servers if None)
            kafka_port: Kafka server port (optional, uses existing bootstrap_servers if None)

        Returns:
            bool: True if topic was created successfully, False otherwise
        """
        try:
            # Use existing bootstrap servers or construct from provided IP/port
            if kafka_ip and kafka_port:
                bootstrap_servers = f"{kafka_ip}:{kafka_port}"
            else:
                bootstrap_servers = self.bootstrap_servers

            # Create admin client configuration
            admin_config = {"bootstrap.servers": bootstrap_servers}

            # Add SASL authentication if configured
            if self.sasl_mechanism and self.sasl_username and self.sasl_password:
                admin_config.update(
                    {
                        "security.protocol": self.security_protocol,
                        "sasl.mechanism": self.sasl_mechanism,
                        "sasl.username": self.sasl_username,
                        "sasl.password": self.sasl_password,
                    }
                )

            admin_client = AdminClient(admin_config)

            # Create topic
            new_topic = NewTopic(topic, num_partitions=partitions, replication_factor=replication)
            futures = admin_client.create_topics([new_topic])

            # Wait for creation to complete
            for topic_name, future in futures.items():
                try:
                    future.result()  # Wait for the operation to complete
                    logging.info(f"Successfully created topic '{topic_name}'")
                    return True
                except Exception as e:
                    if "already exists" in str(e).lower():
                        logging.info(f"Topic '{topic_name}' already exists")
                        return True
                    logging.error(f"Failed to create topic '{topic_name}': {str(e)}")
                    return False
            # If no futures processed, return False to indicate creation did not occur
            return False

        except Exception as exc:
            logging.error(f"Failed to create topic '{topic}': {str(exc)}")
            return False

    def publish_message_with_timestamp(
        self, topic: str, key: bytes, value: bytes, ip: Optional[str] = None, port: Optional[str] = None
    ) -> bool:
        """Publish message using Kafka message timestamp (no headers) - equivalent to Go Publish().

        Args:
            topic: Topic to publish to
            key: Message key as bytes
            value: Message value as bytes
            ip: Kafka server IP (ignored if producer already set up)
            port: Kafka server port (ignored if producer already set up)

        Returns:
            bool: True if message was published successfully, False otherwise
        """
        message_id: Optional[str] = None
        try:
            # Ensure producer is set up
            if not self.producer:
                raise RuntimeError("Producer not initialized. Call setup_producer() first")

            # Track metrics for this message using ID embedded in value
            message_id = str(uuid.uuid4())
            start_time = time.time()
            id_embedded = False
            try:
                raw = value.decode("utf-8") if isinstance(value, (bytes, bytearray)) else str(value)
                obj = json.loads(raw)
                if isinstance(obj, dict):
                    obj["_msg_id"] = message_id
                    value = json.dumps(obj).encode("utf-8")
                    id_embedded = True
            except Exception:
                # Leave value unchanged if not JSON
                pass
            if id_embedded:
                with self._pending_lock:
                    self._pending_produces[message_id] = {
                        "topic": topic,
                        "start_time": start_time,
                        "message_key": key.decode("utf-8") if isinstance(key, bytes) else str(key) if key else None,
                        "message_size": len(value) if value else 0,
                    }

            # Check queue length before producing
            queue_len = len(self.producer)
            if queue_len > 40000:
                logging.warning(f"Producer queue is getting full: {queue_len} messages")
                # Perform aggressive polling to drain queue
                for _ in range(10):
                    self.producer.poll(0.001)
                    if len(self.producer) < 30000:
                        break
                    time.sleep(0.001)

            # Produce message using existing producer (opaque removed)
            self.producer.produce(
                topic,
                key=key,
                value=value,
                on_delivery=self._delivery_callback,
            )

            # Poll to trigger delivery callbacks
            self.producer.poll(0)

            logging.debug(f"Successfully queued message for delivery to topic: {topic}")
            return True

        except Exception as exc:
            # Cleanup pending entry and record failure
            info = None
            if message_id is not None:
                with self._pending_lock:
                    info = self._pending_produces.pop(message_id, None)
            if info is not None:
                self._record_metric(
                    operation="produce",
                    topic=info["topic"],
                    start_time=info["start_time"],
                    end_time=time.time(),
                    success=False,
                    error_msg=str(exc),
                    message_key=info["message_key"],
                    message_size=info["message_size"],
                )
            logging.error(f"Failed to publish message: {str(exc)}")
            return False

    def get_consumer(
        self,
        topic: Optional[str] = None,
        group_id: Optional[str] = None,
        ip: Optional[str] = None,
        port: Optional[str] = None,
    ) -> Optional[Consumer]:
        """Get existing consumer instance or create new one - equivalent to Go GetConsumer().

        Args:
            topic: Topic to subscribe to (optional if consumer already set up)
            group_id: Consumer group ID (optional if consumer already set up)
            ip: Kafka server IP (ignored if consumer already set up)
            port: Kafka server port (ignored if consumer already set up)

        Returns:
            Consumer instance (existing self.consumer) or newly created consumer
        """
        try:
            # Return existing consumer if no specific topic requested
            if self.consumer and not topic:
                logging.debug("Returning existing consumer instance")
                return self.consumer

            # Create new consumer for specific topic if different from current setup
            if topic and (not self._consumer_topics or topic not in self._consumer_topics):
                consumer_config = {
                    "bootstrap.servers": f"{ip}:{port}" if ip and port else self.bootstrap_servers,
                    "group.id": group_id or f"consumer-{topic}-{int(time.time())}",
                    "auto.offset.reset": "earliest",
                    "enable.auto.commit": True,
                }

                # Add SASL authentication if configured
                if self.sasl_mechanism and self.sasl_username and self.sasl_password:
                    consumer_config.update(
                        {
                            "security.protocol": self.security_protocol,
                            "sasl.mechanism": self.sasl_mechanism,
                            "sasl.username": self.sasl_username,
                            "sasl.password": self.sasl_password,
                        }
                    )

                consumer = Consumer(consumer_config)
                consumer.subscribe([topic])

                logging.debug(f"Successfully created new consumer for topic: {topic}")
                return consumer

            # Return existing consumer if available
            if self.consumer:
                return self.consumer
            else:
                logging.warning("No consumer available and insufficient parameters to create new one")
                return None

        except Exception as exc:
            logging.error(f"Failed to get consumer: {str(exc)}")
            return None

    def read_consumer_with_latency(
        self, consumer: Optional[Consumer] = None, ip: Optional[str] = None, port: Optional[str] = None
    ) -> Tuple[Optional[Dict], Optional[float], Optional[str]]:
        """Read message from consumer with latency calculation - equivalent to Go ReadConsumer().

        Args:
            consumer: Consumer instance to read from (uses self.consumer if None)
            ip: Kafka server IP (ignored, for Go compatibility)
            port: Kafka server port (ignored, for Go compatibility)

        Returns:
            Tuple of (message_dict, latency_seconds, error_string)
        """
        try:
            # Use provided consumer or fall back to instance consumer
            active_consumer = consumer or self.consumer

            if not active_consumer:
                error_msg = "No consumer available. Provide consumer parameter or call setup_consumer() first"
                logging.error(error_msg)
                return None, None, error_msg

            msg = active_consumer.poll(timeout=1.0)

            if msg is None:
                return None, None, None

            if msg.error():
                error_msg = f"Consumer error: {msg.error()}"
                logging.error(error_msg)
                return None, None, error_msg

            # Compute latency using Kafka message timestamp
            publish_time = None
            try:
                ts_info = msg.timestamp()
                # confluent_kafka returns (timestamp_type, timestamp_ms)
                if isinstance(ts_info, tuple) and ts_info[1]:
                    publish_time = datetime.fromtimestamp(ts_info[1] / 1000.0, tz=timezone.utc)
            except Exception:
                publish_time = None

            # Calculate latency
            latency = None
            if publish_time:
                current_time = datetime.now(timezone.utc)
                if publish_time.tzinfo is None:
                    publish_time = publish_time.replace(tzinfo=timezone.utc)
                latency = (current_time - publish_time).total_seconds()

            # Parse message value
            value = self._parse_message_value(msg.value())

            # Create message dict with latency field
            message_dict = {
                "topic": msg.topic(),
                "partition": msg.partition(),
                "offset": msg.offset(),
                "key": msg.key(),
                "value": value,
                "headers": msg.headers(),
                "timestamp": msg.timestamp(),
                "latency": latency,
            }

            # Commit message offset
            try:
                active_consumer.commit(msg)
            except Exception as commit_exc:
                logging.warning(f"Failed to commit message: {str(commit_exc)}")

            return message_dict, latency, None

        except Exception as exc:
            error_msg = f"Failed to read message: {str(exc)}"
            logging.error(error_msg)
            return None, None, error_msg

    def _flush_and_close_producer(self) -> None:
        """Flush pending messages and close the Kafka producer."""
        # Poll aggressively before flushing to process any pending callbacks
        logging.info("Processing pending producer callbacks before close...")
        for _ in range(20):
            self.producer.poll(0.1)

        # First attempt with standard timeout
        remaining = int(self.producer.flush(timeout=10))

        # If messages still remain, try with extended timeout
        if remaining > 0:
            logging.warning("%d messages still in queue, extending flush timeout", remaining)
            for _ in range(50):
                self.producer.poll(0.1)
            remaining = int(self.producer.flush(timeout=30))

            if remaining > 0:
                logging.error("%d messages could not be delivered within timeout", remaining)
                self._record_undelivered_failures()
            else:
                logging.info("All remaining messages delivered successfully")

        # Clear pending produces
        with self._pending_lock:
            self._pending_produces.clear()

        # Properly close the producer
        try:
            self.producer.close()
        except Exception as close_exc:
            logging.warning("Error during producer close: %s", str(close_exc))

        self.producer = None

    def _record_undelivered_failures(self) -> None:
        """Record failure metrics for any pending produces that were not delivered."""
        end_time = time.time()
        with self._pending_lock:
            for message_id, produce_info in list(self._pending_produces.items()):
                self._record_metric(
                    operation="produce",
                    topic=produce_info["topic"],
                    start_time=produce_info["start_time"],
                    end_time=end_time,
                    success=False,
                    error_msg="Producer closed before delivery confirmation",
                    message_key=produce_info["message_key"],
                    message_size=produce_info["message_size"],
                )

    def close(self) -> None:
        """Close Kafka producer and consumer connections."""
        try:
            # Stop metrics reporting thread first
            self.stop_metrics_reporting()

            if self.producer:
                self._flush_and_close_producer()

            if self.consumer:
                self.consumer.close()
                self.consumer = None
            logging.info("Closed Kafka connections")
        except Exception as exc:
            logging.error(
                "Error closing Kafka connections: %s",
                str(exc),
            )
            raise


class AsyncKafkaUtils(MetricsReporterMixin):
    """Utility class for asynchronous Kafka operations."""

    def __init__(
        self,
        bootstrap_servers: str,
        sasl_mechanism: Optional[str] = "SCRAM-SHA-256",
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        security_protocol: str = "SASL_PLAINTEXT",
    ) -> None:
        """Initialize async Kafka utils with bootstrap servers and SASL configuration.

        Args:
            bootstrap_servers: Comma-separated list of Kafka broker addresses
            sasl_mechanism: SASL mechanism for authentication
            sasl_username: Username for SASL authentication
            sasl_password: Password for SASL authentication
            security_protocol: Security protocol for Kafka connection
        """
        self.bootstrap_servers = bootstrap_servers
        self.sasl_mechanism = sasl_mechanism
        self.sasl_username = sasl_username or os.environ.get("KAFKA_SASL_USERNAME")
        self.sasl_password = sasl_password or os.environ.get("KAFKA_SASL_PASSWORD")
        self.security_protocol = security_protocol
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumer: Optional[AIOKafkaConsumer] = None
        self._consumer_config: Optional[Dict[str, Any]] = None
        self._consumer_topics: Optional[List[str]] = None
        self._consumer_group_id: Optional[str] = None
        self._assigned: Optional[asyncio.Event] = None

        # Metrics collection for performance monitoring (async-safe)
        self._metrics_log: Deque[Dict[str, Any]] = deque(maxlen=10000)  # Keep last 10000 metrics entries
        self._metrics_lock = threading.Lock()  # Protect metrics deque across reporter thread and event loop
        self._pending_produces: Dict[str, Any] = {}  # Track pending async produce operations for delivery timing
        # Note: accessed only from the event loop thread in async paths

        # Background metrics reporting (shared with sync version)
        self._metrics_reporting_config: Optional[Dict[str, Any]] = None
        self._metrics_thread: Optional[threading.Thread] = None
        self._metrics_stop_event = threading.Event()

        logging.info("Initialized AsyncKafkaUtils with servers: %s", bootstrap_servers)

        # Track producer start state and protect concurrent start attempts
        self._producer_started = False
        self._producer_start_lock: Optional[asyncio.Lock] = None  # Will be created when needed

        # Check if we can create the lock now (if event loop is available)
        try:
            asyncio.get_running_loop()
            # Event loop is available, create the lock
            self._producer_start_lock = asyncio.Lock()
        except RuntimeError:
            # No event loop available at init time, will create lock later when needed
            pass

    def _is_event_loop_available(self) -> bool:
        """Check if event loop is available and not shutting down."""
        try:
            loop = asyncio.get_running_loop()
            return not loop.is_closed()
        except RuntimeError:
            return False

    def _record_metric(
        self,
        operation: str,
        topic: str,
        start_time: float,
        end_time: float,
        success: bool,
        error_msg: Optional[str] = None,
        message_key: Optional[str] = None,
        message_size: Optional[int] = None,
    ) -> None:
        """Record a performance metric for aggregation."""
        duration_ms = (end_time - start_time) * 1000

        metric = {
            "timestamp": end_time,
            "operation": operation,
            "topic": topic,
            "duration_ms": duration_ms,
            "success": success,
            "error_msg": error_msg,
            "message_key": message_key,
            "message_size": message_size,
            "bootstrap_servers": self.bootstrap_servers,
            "type": "async",
        }

        with self._metrics_lock:
            self._metrics_log.append(metric)

        KafkaUtils._log_kafka_metric(
            "Async Kafka",
            operation,
            topic,
            duration_ms,
            success,
            error_msg,
            message_key,
            message_size,
        )

    def configure_metrics_reporting(
        self, rpc_client, service_id: Optional[str] = None, interval: int = 120, batch_size: int = 1000
    ) -> None:
        """Configure background metrics reporting to backend API.

        Args:
            rpc_client: RPC client instance for API communication
            service_id: Deployment identifier for metrics context
            interval: Reporting interval in seconds (default: 120)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        self._metrics_reporting_config = {
            "rpc_client": rpc_client,
            "deployment_id": service_id,
            "interval": interval,
            "batch_size": batch_size,
            "enabled": True,
        }
        self._start_metrics_reporter(f"async-kafka-metrics-reporter-{id(self)}")
        logging.info("Started background async Kafka metrics reporting thread")

    def _extract_ip_port_from_bootstrap(self) -> Tuple[str, str]:
        """Extract IP and port from bootstrap_servers."""
        try:
            first_server = self.bootstrap_servers.split(",")[0].strip()
            if ":" in first_server:
                ip, port = first_server.split(":", 1)
                return ip.strip(), port.strip()
            else:
                return first_server.strip(), "9092"
        except Exception:
            return "unknown", "unknown"

    def _aggregate_metrics_for_api(self, raw_metrics: List[Dict]) -> Dict:
        """Aggregate raw metrics into the API format expected by backend."""
        ip, port = self._extract_ip_port_from_bootstrap()
        return aggregate_kafka_metrics(raw_metrics, ip, port)

    def _get_reporter_label(self) -> str:
        return "Async Kafka"

    def _get_metrics_collection_key(self) -> str:
        return "topic"

    def _get_api_path(self) -> str:
        return "/v1/monitoring/add_kafka_metrics"

    async def setup_producer(self, config: Optional[Dict] = None) -> None:
        """Set up async Kafka producer.

        Args:
            config: Additional producer configuration

        Raises:
            AsyncKafkaError: If producer initialization fails
        """
        # Check if event loop is available and not shutting down
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed, cannot set up async producer")
        except RuntimeError as exc:
            if "no running event loop" in str(exc).lower():
                raise RuntimeError("No event loop available for async producer setup")
            raise

        producer_config = {
            "bootstrap_servers": self.bootstrap_servers,
            "acks": "all",  # Keep "all" for better reliability
            "enable_idempotence": True,
            "request_timeout_ms": 60000,  # Increased timeout
            "retry_backoff_ms": 100,  # Reduced backoff
            "max_batch_size": 1048576,  # Increased batch size (1MB)
            "linger_ms": 5,
            "max_request_size": 25000000,
            # "compression_type": "snappy"
        }

        # Add SASL authentication if configured
        if self.sasl_mechanism and self.sasl_username and self.sasl_password:
            producer_config.update(
                {
                    "security_protocol": self.security_protocol,
                    "sasl_mechanism": self.sasl_mechanism,
                    "sasl_plain_username": self.sasl_username,
                    "sasl_plain_password": self.sasl_password,
                }
            )

        if config:
            producer_config.update(config)

        # Close existing producer if any
        if self.producer:
            try:
                await self.producer.stop()
            except Exception:
                pass  # Ignore errors during cleanup

        self.producer = AIOKafkaProducer(**producer_config)
        try:
            # Ensure only one coroutine starts the producer
            if self._producer_start_lock is None:
                try:
                    self._producer_start_lock = asyncio.Lock()
                except RuntimeError as exc:
                    if "cannot schedule new futures after shutdown" in str(exc):
                        raise RuntimeError("Cannot create producer lock: event loop is shutting down")
                    raise

            async with self._producer_start_lock:
                if not self._producer_started:
                    await self.producer.start()
                    self._producer_started = True
            logging.info("Successfully set up async Kafka producer")
        except (AsyncKafkaError, RuntimeError) as exc:
            error_msg = f"Failed to start async producer: {str(exc)}"
            logging.error(error_msg)
            # Clean up on failure
            self.producer = None
            self._producer_started = False
            raise RuntimeError(error_msg) from exc

    # Nested classes are not supported by mypyc reliably; use a top-level listener instead

    async def _wait_for_assignment(self, timeout: float = 600) -> None:
        """Wait for partition assignment to complete.

        Args:
            timeout: Maximum time to wait for assignment in seconds
        """
        try:
            assigned = self._assigned
            if assigned is None:
                logging.warning("Assignment event not initialized")
                return
            await asyncio.wait_for(assigned.wait(), timeout=timeout)
            logging.info("Async consumer is now ready to receive messages")
        except asyncio.TimeoutError:
            logging.warning(f"Async consumer rebalancing timed out after {timeout} seconds")
            # Final check for assignment
            consumer = self.consumer
            assignment = consumer.assignment() if consumer is not None else None
            if assignment:
                logging.info(f"Async consumer has {len(assignment)} partition(s) assigned after timeout")
                if self._assigned is not None:
                    self._assigned.set()
            else:
                logging.warning("Async consumer has no partitions assigned after rebalancing timeout")

    async def setup_consumer(
        self,
        topics: List[str],
        group_id: str,
        group_instance_id: Optional[str] = None,
        config: Optional[Dict] = None,
    ) -> None:
        """Set up async Kafka consumer.

        Args:
            topics: List of topics to subscribe to
            group_id: Consumer group ID
            group_instance_id: Consumer group instance ID for static membership
            config: Additional consumer configuration

        Raises:
            ValueError: If topics list is empty
            AsyncKafkaError: If consumer initialization fails
        """
        if not topics:
            raise ValueError("Topics list cannot be empty")

        consumer_config = {
            "bootstrap_servers": self.bootstrap_servers,
            "group_id": group_id,
            "auto_offset_reset": "earliest",
            "enable_auto_commit": True,
            "session_timeout_ms": 60000,  # Increased from 30000 to reduce rebalancing
            "heartbeat_interval_ms": 20000,  # Increased from 10000
            "max_poll_interval_ms": 600000,  # Increased to 10 minutes
            "request_timeout_ms": 120000,
            "rebalance_timeout_ms": 600000,
            # TODO: Enable these to avoid timeouts
            # "max_poll_records": 1,  # Process one message at a time to avoid timeouts
            # "consumer_timeout_ms": -1,  # No timeout for consumer
        }

        # Add SASL authentication if configured
        if self.sasl_mechanism and self.sasl_username and self.sasl_password:
            consumer_config.update(
                {
                    "security_protocol": self.security_protocol,
                    "sasl_mechanism": self.sasl_mechanism,
                    "sasl_plain_username": self.sasl_username,
                    "sasl_plain_password": self.sasl_password,
                }
            )

        if group_instance_id:
            consumer_config["group_instance_id"] = group_instance_id
        if config:
            consumer_config.update(config)

        # Store configuration for potential reconnection
        self._consumer_config = consumer_config
        self._consumer_topics = topics
        self._consumer_group_id = group_id

        # Create the event in the current event loop
        self._assigned = asyncio.Event()

        # Close existing consumer if any
        if self.consumer:
            try:
                await self.consumer.stop()
            except Exception:
                pass  # Ignore errors during cleanup

        # Retry setup with exponential backoff for group join errors
        max_retries = 3
        retry_delay = 5.0  # Start with 5 seconds

        for attempt in range(max_retries):
            try:
                self.consumer = AIOKafkaConsumer(*topics, **consumer_config)

                # Create listener instance with reference to consumer
                listener = AsyncRebalanceListener(self.consumer, self)
                # Subscribe with the rebalance listener
                self.consumer.subscribe(topics, listener=listener)
                await self.consumer.start()

                # Wait for assignment to complete with timeout
                await self._wait_for_assignment()

                logging.info("Successfully set up async Kafka consumer for topics: %s", topics)
                return  # Success, exit retry loop

            except AsyncKafkaError as exc:
                # Check for specific errors that warrant retry
                error_msg = str(exc).lower()
                if (
                    "unknownerror" in error_msg or "group coordinator not available" in error_msg
                ) and attempt < max_retries - 1:
                    logging.warning(f"Kafka consumer setup failed (attempt {attempt + 1}/{max_retries}): {str(exc)}")
                    logging.info(f"Retrying consumer setup in {retry_delay} seconds...")

                    # Clean up failed consumer
                    if self.consumer:
                        try:
                            await self.consumer.stop()
                        except Exception:
                            pass
                        self.consumer = None

                    # Wait before retry
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    logging.error("Failed to start async consumer: %s", str(exc))
                    # Clean up on failure
                    self.consumer = None
                    raise

    async def _reconnect_consumer(self) -> None:
        """Reconnect the consumer if it's disconnected.

        Raises:
            AsyncKafkaError: If consumer reconnection fails
            RuntimeError: If consumer was never set up
        """
        if not self._consumer_config or not self._consumer_topics:
            raise RuntimeError("Cannot reconnect consumer that was never set up")

        try:
            logging.info("Attempting to reconnect async Kafka consumer")
            if self.consumer:
                try:
                    await self.consumer.stop()
                except Exception:
                    pass  # Ignore errors during close of potentially broken consumer

            # Create a new event in the current event loop
            self._assigned = asyncio.Event()

            # Wait before reconnecting to give broker time to stabilize
            await asyncio.sleep(15.0)  # Added 15 second delay before reconnection

            self.consumer = AIOKafkaConsumer(*self._consumer_topics, **self._consumer_config)

            # Create listener instance with reference to consumer
            listener = AsyncRebalanceListener(self.consumer, self)

            # Subscribe with the rebalance listener
            self.consumer.subscribe(self._consumer_topics, listener=listener)
            await self.consumer.start()

            # Wait for assignment to complete with timeout
            await self._wait_for_assignment()

            logging.info("Successfully reconnected async Kafka consumer")
        except AsyncKafkaError as exc:
            error_msg = f"Failed to reconnect async consumer: {str(exc)}"
            logging.error(error_msg)
            raise

    @staticmethod
    def _serialize_value(value: Any) -> bytes:
        """Serialize message value to bytes."""
        return serialize_value(value)

    @staticmethod
    def _serialize_key(key: Any) -> Optional[bytes]:
        """Serialize message key to bytes."""
        return serialize_key(key)

    async def produce_message(
        self,
        topic: str,
        value: Union[dict, str, bytes, Any],
        key: Optional[Union[str, bytes, Any]] = None,
        headers: Optional[List[Tuple[str, bytes]]] = None,
        timeout: float = 30.0,
    ) -> None:
        """Produce a message to a Kafka topic.

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
        if not self.producer:
            raise RuntimeError("Producer not initialized. Call setup_producer() first.")
        if not topic or value is None:
            raise ValueError("Topic and value must be provided")

        # Serialize value and key
        value_bytes = self._serialize_value(value)
        key_bytes = self._serialize_key(key)
        message_size = len(value_bytes) if value_bytes else 0
        message_key = key_bytes.decode("utf-8") if isinstance(key_bytes, bytes) else str(key) if key else None
        # Do not use headers for correlation; track via local pending map only
        message_id = str(uuid.uuid4())

        # Ensure producer is fully started (guard against rare race conditions)
        if not self.producer:
            raise RuntimeError("Producer not initialized. Call setup_producer() first.")
        if not self._producer_started:
            # Check if event loop is available
            try:
                loop = asyncio.get_running_loop()
                if loop.is_closed():
                    raise RuntimeError("Cannot start producer: event loop is closed")
            except RuntimeError as exc:
                if "no running event loop" in str(exc).lower():
                    raise RuntimeError("Cannot start producer: no event loop available")
                raise

            # Coordinate concurrent start attempts
            if self._producer_start_lock is None:
                try:
                    self._producer_start_lock = asyncio.Lock()
                except RuntimeError as exc:
                    if "cannot schedule new futures after shutdown" in str(exc):
                        raise RuntimeError("Cannot create producer lock: event loop is shutting down")
                    raise
            async with self._producer_start_lock:
                if not self._producer_started:
                    await self.producer.start()
                    self._producer_started = True

        # Time the actual send_and_wait operation (includes delivery confirmation)
        start_time = time.time()
        try:
            # Track pending before send
            self._pending_produces[message_id] = {
                "topic": topic,
                "start_time": start_time,
                "message_key": message_key,
                "message_size": message_size,
            }
            await self.producer.send_and_wait(
                topic,
                value=value_bytes,
                key=key_bytes,
            )
            end_time = time.time()

            # Clear pending track on success
            self._pending_produces.pop(message_id, None)

            # Record successful delivery metrics
            self._record_metric(
                operation="produce",
                topic=topic,
                start_time=start_time,
                end_time=end_time,
                success=True,
                error_msg=None,
                message_key=message_key,
                message_size=message_size,
            )

            logging.debug("Successfully produced message to topic: %s", topic)
        except AsyncKafkaError as exc:
            end_time = time.time()
            # Clear pending track on failure
            self._pending_produces.pop(message_id, None)
            error_msg = f"Failed to produce message: {str(exc)}"
            logging.error(error_msg)

            # Record failed delivery metrics
            self._record_metric(
                operation="produce",
                topic=topic,
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=message_key,
                message_size=message_size,
            )
            raise

    @staticmethod
    def _parse_message_value(value: bytes) -> Any:
        """Parse message value from bytes."""
        return parse_message_value(value)

    async def consume_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume a single message from Kafka.

        Args:
            timeout: Maximum time to wait for message in seconds

        Returns:
            Message dictionary if available, None if no message received

        Raises:
            RuntimeError: If consumer is not initialized
            AsyncKafkaError: If message consumption fails
        """
        if not self.consumer:
            raise RuntimeError("Consumer not initialized. Call setup_consumer() first.")

        # Ensure we have partitions assigned before attempting to consume
        assigned = self._assigned
        if not assigned or not assigned.is_set():
            try:
                if assigned is None:
                    logging.warning("Assignment event not initialized")
                    return None
                await asyncio.wait_for(assigned.wait(), timeout=60.0)  # Increased from 30.0 to 60.0
            except asyncio.TimeoutError:
                logging.warning("Timed out waiting for partition assignment")
                return None

        # Time only the actual getone operation
        start_time = time.time()
        try:
            # Use getone with timeout to avoid blocking indefinitely
            try:
                msg = await asyncio.wait_for(self.consumer.getone(), timeout=timeout)
                end_time = time.time()

                topic = msg.topic
                message_size = len(msg.value) if msg.value else 0
                message_key = (
                    msg.key.decode("utf-8")
                    if msg.key and isinstance(msg.key, bytes)
                    else str(msg.key)
                    if msg.key
                    else None
                )

                # Parse the message value
                value = self._parse_message_value(msg.value)

                # Record successful consumption metrics
                self._record_metric(
                    operation="consume",
                    topic=topic,
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=message_key,
                    message_size=message_size,
                )

                return {
                    "topic": msg.topic,
                    "partition": msg.partition,
                    "offset": msg.offset,
                    "key": msg.key,
                    "value": value,
                    "headers": msg.headers,
                    "timestamp": msg.timestamp,
                }
            except asyncio.TimeoutError:
                end_time = time.time()
                # Record timeout as successful operation with no message
                self._record_metric(
                    operation="consume",
                    topic="(timeout)",
                    start_time=start_time,
                    end_time=end_time,
                    success=True,
                    error_msg=None,
                    message_key=None,
                    message_size=None,
                )
                return None
        except AsyncKafkaError as exc:
            end_time = time.time()
            error_msg = f"Failed to consume message: {str(exc)}"
            logging.error(error_msg)

            # Record error metrics
            self._record_metric(
                operation="consume",
                topic="(error)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None,
            )

            # Check if it's a connection-related error
            if isinstance(
                exc,
                (
                    AsyncKafkaError.ConnectionError,
                    AsyncKafkaError.NodeNotReadyError,
                    AsyncKafkaError.RequestTimedOutError,
                ),
            ):
                logging.warning("Async Kafka consumer disconnected, attempting to reconnect")
                try:
                    await self._reconnect_consumer()
                    return None
                except Exception as reconnect_exc:
                    logging.error("Failed to reconnect async consumer: %s", str(reconnect_exc))

            raise
        except Exception as exc:
            end_time = time.time()
            error_msg = f"Unexpected error consuming message: {str(exc)}"
            logging.error(error_msg)

            # Record error metrics
            self._record_metric(
                operation="consume",
                topic="(unknown)",
                start_time=start_time,
                end_time=end_time,
                success=False,
                error_msg=error_msg,
                message_key=None,
                message_size=None,
            )

            # Try to reconnect for unexpected errors that might be connection-related
            try:
                await self._reconnect_consumer()
            except Exception:
                pass  # Ignore reconnection errors here

            # Return None for non-critical errors
            return None

    async def close(self) -> None:
        """Close async Kafka producer and consumer connections."""
        errors: List[str] = []

        # Stop background metrics reporting first
        try:
            self.stop_metrics_reporting()
        except Exception as exc:
            error_msg = f"Error stopping async metrics reporting: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        # Check if event loop is still running
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                logging.warning("Event loop is closed, skipping async Kafka cleanup")
                self.producer = None
                self.consumer = None
                return
        except RuntimeError:
            logging.warning("No running event loop, skipping async Kafka cleanup")
            self.producer = None
            self.consumer = None
            return

        # Close producer with timeout
        if self.producer:
            try:
                logging.debug("Closing async Kafka producer...")
                # First flush attempt with standard timeout
                try:
                    await asyncio.wait_for(self.producer.flush(), timeout=5.0)
                    logging.debug("Initial flush completed successfully")
                except asyncio.TimeoutError:
                    logging.warning("Initial flush timed out, attempting extended flush")
                    try:
                        # Extended flush timeout for remaining messages
                        await asyncio.wait_for(self.producer.flush(), timeout=30.0)
                        logging.info("Extended flush completed successfully")
                    except asyncio.TimeoutError:
                        logging.error("Producer flush failed even with extended timeout")
                        # Record failures for any remaining pending produces
                        end_time = time.time()
                        for message_id, produce_info in list(self._pending_produces.items()):
                            self._record_metric(
                                operation="produce",
                                topic=produce_info["topic"],
                                start_time=produce_info["start_time"],
                                end_time=end_time,
                                success=False,
                                error_msg="Async producer closed before delivery confirmation",
                                message_key=produce_info["message_key"],
                                message_size=produce_info["message_size"],
                            )

                # Clear pending produces
                self._pending_produces.clear()

                # Stop the producer
                await asyncio.wait_for(self.producer.stop(), timeout=10.0)
                self.producer = None
                logging.debug("Async Kafka producer closed successfully")
            except asyncio.TimeoutError:
                logging.warning("Async Kafka producer close timed out")
                self.producer = None
            except Exception as exc:
                error_msg = f"Error closing async Kafka producer: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.producer = None
            finally:
                self._producer_started = False

        # Close consumer with timeout
        if self.consumer:
            try:
                logging.debug("Closing async Kafka consumer...")
                await asyncio.wait_for(self.consumer.stop(), timeout=10.0)
                self.consumer = None
                logging.debug("Async Kafka consumer closed successfully")
            except asyncio.TimeoutError:
                logging.warning("Async Kafka consumer close timed out")
                self.consumer = None
            except Exception as exc:
                error_msg = f"Error closing async Kafka consumer: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.consumer = None

        if not errors:
            logging.info("Closed async Kafka connections successfully")
        else:
            # Don't raise exception during cleanup, just log errors
            logging.error("Errors occurred during async Kafka close: %s", "; ".join(errors))


class MatriceKafkaDeployment:
    """Class for managing Kafka deployments for Matrice streaming API."""

    def __init__(
        self,
        session,
        service_id: str,
        type: str,
        consumer_group_id: Optional[str] = None,
        consumer_group_instance_id: Optional[str] = None,
        sasl_mechanism: Optional[str] = "SCRAM-SHA-256",
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        security_protocol: str = "SASL_PLAINTEXT",
        custom_request_service_id: Optional[str] = None,
        custom_result_service_id: Optional[str] = None,
        enable_metrics: bool = True,
        metrics_interval: int = 120,
    ) -> None:
        """Initialize Kafka deployment with deployment ID.

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
        self.session = session
        self.rpc = session.rpc
        self.service_id = service_id
        self.type = type
        self.sasl_mechanism = sasl_mechanism
        self.sasl_username = sasl_username or os.environ.get("KAFKA_SASL_USERNAME")
        self.sasl_password = sasl_password or os.environ.get("KAFKA_SASL_PASSWORD")
        self.security_protocol = security_protocol
        self.custom_request_service_id = custom_request_service_id or service_id
        self.custom_result_service_id = custom_result_service_id or service_id

        # Use provided consumer_group_id or generate a stable one
        if consumer_group_id:
            self.consumer_group_id = consumer_group_id
        else:
            self.consumer_group_id = f"{self.service_id}-{self.type}-{int(time.time())}"

        # Use provided consumer_group_instance_id or generate a stable one
        if consumer_group_instance_id:
            self.consumer_group_instance_id = consumer_group_instance_id
        else:
            self.consumer_group_instance_id = f"{self.service_id}-{self.type}-stable"

        self.setup_success: bool = False
        self.bootstrap_server: Optional[str] = None
        self.request_topic: Optional[str] = None
        self.result_topic: Optional[str] = None
        self.producing_topic: Optional[str] = None
        self.consuming_topic: Optional[str] = None

        # Initialize Kafka utilities as None - create as needed
        self.sync_kafka: Optional[KafkaUtils] = None
        self.async_kafka: Optional[AsyncKafkaUtils] = None

        # Initialize metrics configuration
        self._metrics_config: Optional[Dict[str, Any]] = None

        # Get initial Kafka configuration
        self.setup_success, self.bootstrap_server, self.request_topic, self.result_topic = self.get_kafka_info()
        if not self.setup_success:
            logging.warning("Initial Kafka setup failed. Streaming API may not be available.")
            return

        # Configure topics based on deployment type
        if self.type == "client":
            self.producing_topic = self.request_topic
            self.consuming_topic = self.result_topic
        elif self.type == "server":
            self.producing_topic = self.result_topic
            self.consuming_topic = self.request_topic
        else:
            raise ValueError("Invalid type: must be 'client' or 'server'")

        logging.info(
            "Initialized MatriceKafkaDeployment: deployment_id=%s, type=%s, consumer_group_id=%s, consumer_group_instance_id=%s",
            service_id,
            type,
            self.consumer_group_id,
            self.consumer_group_instance_id,
        )

        # Auto-enable metrics reporting by default
        if enable_metrics:
            self.configure_metrics_reporting(interval=metrics_interval)

    def check_setup_success(self) -> bool:
        """Check if the Kafka setup is successful and attempt to recover if not.

        Returns:
            bool: True if setup was successful, False otherwise
        """
        if not self.setup_success:
            logging.warning("Failed to get Kafka info, attempting to recover connection...")
            try:
                # Retry getting Kafka configuration
                self.setup_success, self.bootstrap_server, self.request_topic, self.result_topic = self.get_kafka_info()

                if not self.setup_success:
                    logging.warning(
                        "Failed to get Kafka info again. Streaming API unavailable. "
                        "Please check your Kafka deployment and try initializing again."
                    )
                    return False

                # Update topics based on deployment type
                if self.type == "client":
                    self.producing_topic = self.request_topic
                    self.consuming_topic = self.result_topic
                else:  # server
                    self.producing_topic = self.result_topic
                    self.consuming_topic = self.request_topic

                logging.info("Successfully recovered Kafka connection")
                return True
            except Exception as exc:
                logging.error("Error refreshing Kafka setup: %s", str(exc))
                return False

        return True

    def get_all_metrics(self) -> Dict:
        """Get aggregated metrics from all Kafka utilities.

        Returns:
            Dict: Combined metrics from sync and async Kafka utilities
        """
        all_metrics: Dict[str, Any] = {
            "sync_metrics": [],
            "async_metrics": [],
            "deployment_info": {
                "type": self.type,
                "setup_success": self.setup_success,
                "producing_topic": getattr(self, "producing_topic", None),
                "consuming_topic": getattr(self, "consuming_topic", None),
            },
        }

        # Get sync metrics
        if self.sync_kafka:
            try:
                all_metrics["sync_metrics"] = self.sync_kafka.get_metrics()
            except Exception as exc:
                logging.warning("Error getting sync metrics: %s", str(exc))

        # Get async metrics
        if self.async_kafka:
            try:
                all_metrics["async_metrics"] = self.async_kafka.get_metrics()
            except Exception as exc:
                logging.warning("Error getting async metrics: %s", str(exc))

        return all_metrics

    def get_metrics_summary(self) -> Dict:
        """Get a summary of metrics from all Kafka utilities.

        Returns:
            Dict: Summarized metrics with counts and statistics
        """
        all_metrics = self.get_all_metrics()

        summary = {
            "sync_summary": self._summarize_metrics(all_metrics["sync_metrics"]),
            "async_summary": self._summarize_metrics(all_metrics["async_metrics"]),
            "deployment_info": all_metrics["deployment_info"],
        }

        return summary

    @staticmethod
    def _summarize_metrics(metrics: List[Dict]) -> Dict:
        """Summarize a list of metrics into counts and average latency."""
        result = {
            "total_operations": len(metrics),
            "success_count": 0,
            "error_count": 0,
            "avg_latency": 0.0,
        }
        latencies = []
        for metric in metrics:
            if metric.get("success"):
                result["success_count"] += 1
                if "latency" in metric:
                    latencies.append(metric["latency"])
            else:
                result["error_count"] += 1
        if latencies:
            result["avg_latency"] = sum(latencies) / len(latencies)
        return result

    def refresh(self):
        """Refresh the Kafka producer and consumer connections."""
        logging.info("Refreshing Kafka connections")
        # Clear existing connections to force recreation
        if self.sync_kafka:
            try:
                self.sync_kafka.close()
            except Exception as exc:
                logging.warning("Error closing sync Kafka during refresh: %s", str(exc))
            self.sync_kafka = None

        if self.async_kafka:
            try:
                # Note: close() is async but we can't await here
                logging.warning("Async Kafka connections will be recreated on next use")
            except Exception as exc:
                logging.warning("Error during async Kafka refresh: %s", str(exc))
            self.async_kafka = None

        if self.check_setup_success():
            logging.info("Kafka connections will be refreshed on next use")
        else:
            logging.warning("Failed to refresh Kafka connections")

    def _ensure_sync_producer(self):
        """Ensure sync Kafka producer is set up."""
        if not self.check_setup_success():
            return False
        if not self.sync_kafka:
            self.sync_kafka = KafkaUtils(
                self.bootstrap_server,
                self.sasl_mechanism,
                self.sasl_username,
                self.sasl_password,
                self.security_protocol,
            )
            # Configure metrics reporting if enabled
            if self._metrics_config and self._metrics_config.get("enabled"):
                try:
                    self.sync_kafka.configure_metrics_reporting(
                        rpc_client=self.session.rpc,
                        service_id=self.service_id,
                        interval=self._metrics_config.get("interval", 60),
                        batch_size=self._metrics_config.get("batch_size", 1000),
                    )
                except Exception as exc:
                    logging.warning(f"Failed to configure sync Kafka metrics reporting: {exc}")

        try:
            if not hasattr(self.sync_kafka, "producer") or not self.sync_kafka.producer:
                self.sync_kafka.setup_producer()
            return True
        except Exception as exc:
            logging.error("Failed to set up sync Kafka producer: %s", str(exc))
            return False

    def _ensure_sync_consumer(self):
        """Ensure sync Kafka consumer is set up."""
        if not self.check_setup_success():
            return False
        if not self.sync_kafka:
            self.sync_kafka = KafkaUtils(
                self.bootstrap_server,
                self.sasl_mechanism,
                self.sasl_username,
                self.sasl_password,
                self.security_protocol,
            )
            # Configure metrics reporting if enabled
            if self._metrics_config and self._metrics_config.get("enabled"):
                try:
                    self.sync_kafka.configure_metrics_reporting(
                        rpc_client=self.session.rpc,
                        service_id=self.service_id,
                        interval=self._metrics_config.get("interval", 60),
                        batch_size=self._metrics_config.get("batch_size", 1000),
                    )
                except Exception as exc:
                    logging.warning(f"Failed to configure sync Kafka metrics reporting: {exc}")

        try:
            if not hasattr(self.sync_kafka, "consumer") or not self.sync_kafka.consumer:
                self.sync_kafka.setup_consumer(
                    [self.consuming_topic], self.consumer_group_id, self.consumer_group_instance_id
                )
            return True
        except Exception as exc:
            logging.error("Failed to set up sync Kafka consumer: %s", str(exc))
            return False

    async def _ensure_async_producer(self):
        """Ensure async Kafka producer is set up.

        Returns:
            bool: True if setup was successful, False otherwise
        """
        if not self.check_setup_success():
            return False
        if not self.async_kafka:
            self.async_kafka = AsyncKafkaUtils(
                self.bootstrap_server,
                self.sasl_mechanism,
                self.sasl_username,
                self.sasl_password,
                self.security_protocol,
            )
            # Configure metrics reporting if enabled
            if self._metrics_config and self._metrics_config.get("enabled"):
                try:
                    self.async_kafka.configure_metrics_reporting(
                        rpc_client=self.session.rpc,
                        service_id=self.service_id,
                        interval=self._metrics_config.get("interval", 60),
                        batch_size=self._metrics_config.get("batch_size", 1000),
                    )
                except Exception as exc:
                    logging.warning(f"Failed to configure async Kafka metrics reporting: {exc}")

        try:
            if not hasattr(self.async_kafka, "producer") or not self.async_kafka.producer:
                await self.async_kafka.setup_producer()
            return True
        except RuntimeError as exc:
            error_msg = str(exc)
            if any(
                phrase in error_msg
                for phrase in [
                    "event loop is closed",
                    "no event loop available",
                    "event loop is shutting down",
                    "cannot schedule new futures after shutdown",
                ]
            ):
                logging.warning(f"Cannot set up async Kafka producer due to event loop state: {error_msg}")
                return False
            logging.error("Failed to set up async Kafka producer: %s", str(exc))
            return False
        except Exception as exc:
            logging.error("Failed to set up async Kafka producer: %s", str(exc))
            return False

    async def _ensure_async_consumer(self):
        """Ensure async Kafka consumer is set up.

        Returns:
            bool: True if setup was successful, False otherwise
        """
        if not self.check_setup_success():
            return False
        if not self.async_kafka:
            self.async_kafka = AsyncKafkaUtils(
                self.bootstrap_server,
                self.sasl_mechanism,
                self.sasl_username,
                self.sasl_password,
                self.security_protocol,
            )
            # Configure metrics reporting if enabled
            if self._metrics_config and self._metrics_config.get("enabled"):
                try:
                    self.async_kafka.configure_metrics_reporting(
                        rpc_client=self.session.rpc,
                        service_id=self.service_id,
                        interval=self._metrics_config.get("interval", 60),
                        batch_size=self._metrics_config.get("batch_size", 1000),
                    )
                except Exception as exc:
                    logging.warning(f"Failed to configure async Kafka metrics reporting: {exc}")

        try:
            if not hasattr(self.async_kafka, "consumer") or not self.async_kafka.consumer:
                await self.async_kafka.setup_consumer(
                    [self.consuming_topic], self.consumer_group_id, self.consumer_group_instance_id
                )
            return True
        except Exception as exc:
            logging.error("Failed to set up async Kafka consumer: %s", str(exc))
            return False

    def get_kafka_info(self):
        """Get Kafka setup information from the API.

        Returns:
            Tuple containing (setup_success, bootstrap_server, request_topic, result_topic)

        Raises:
            ValueError: If API requests fail or return invalid data
        """
        setup_success = True
        try:
            request_topic = self.rpc.get(f"/v1/actions/get_kafka_request_topics/{self.custom_request_service_id}")
            result_topic = self.rpc.get(f"/v1/actions/get_kafka_result_topics/{self.custom_result_service_id}")

            if not request_topic or not request_topic.get("success"):
                raise ValueError(f"Failed to get request topics: {request_topic.get('message', 'Unknown error')}")

            if not result_topic or not result_topic.get("success"):
                raise ValueError(f"Failed to get result topics: {result_topic.get('message', 'Unknown error')}")

            request_data = request_topic.get("data", {})
            result_data = result_topic.get("data", {})

            if not request_data or not result_data:
                raise ValueError("Empty response data from Kafka topic API")

            ip_address = request_data.get("ip_address")
            port = request_data.get("port")

            if not ip_address or not port:
                logging.warning(f"Invalid bootstrap server information: IP={ip_address}, Port={port}")
                setup_success = False
                return setup_success, None, None, None

            bootstrap_server = f"{ip_address}:{port}"

            return setup_success, bootstrap_server, request_data["topic"], result_data["topic"]
        except Exception as exc:
            logging.error("Error getting Kafka info: %s", str(exc))
            return False, None, None, None

    def _parse_message(self, result: dict) -> dict:
        """Handle bytes key and value conversion."""
        if not result:
            return result
        if result.get("key") and isinstance(result["key"], bytes):
            try:
                result["key"] = result["key"].decode("utf-8")
            except UnicodeDecodeError:
                result["key"] = str(result["key"])
        if result.get("value") and isinstance(result["value"], bytes):
            try:
                result["value"] = json.loads(result["value"].decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        return result

    def produce_message(self, message: dict, timeout: float = 60.0, key: Optional[str] = None) -> None:
        """Produce a message to Kafka.

        Args:
            message: Message to produce
            timeout: Maximum time to wait for message delivery in seconds
            key: Optional key for message partitioning (stream_id/camera_id)

        Raises:
            RuntimeError: If producer is not initialized
            ValueError: If message is invalid
            KafkaError: If message production fails
        """
        if not self._ensure_sync_producer():
            raise RuntimeError("Failed to set up Kafka producer")
        sk = self.sync_kafka
        topic = self.producing_topic
        assert sk is not None and topic is not None
        sk.produce_message(topic, message, key=key, timeout=timeout)

    def consume_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume a message from Kafka.

        Args:
            timeout: Maximum time to wait for message in seconds

        Returns:
            Message dictionary if available, None if no message received

        Raises:
            RuntimeError: If consumer is not initialized
            KafkaError: If message consumption fails
        """
        self._ensure_sync_producer()
        if not self._ensure_sync_consumer():
            logging.warning("Kafka consumer setup unsuccessful, returning None for consume request")
            return None

        sk = self.sync_kafka
        assert sk is not None
        result = sk.consume_message(timeout)
        if result is not None:
            result = self._parse_message(result)
        return result

    async def async_produce_message(self, message: dict, timeout: float = 60.0, key: Optional[str] = None) -> None:
        """Produce a message to Kafka asynchronously.

        Args:
            message: Message to produce
            timeout: Maximum time to wait for message delivery in seconds
            key: Optional key for message partitioning (stream_id/camera_id)

        Raises:
            RuntimeError: If producer is not initialized or event loop is unavailable
            ValueError: If message is invalid
            AsyncKafkaError: If message production fails
        """
        # Check if async_kafka is available and event loop is in good state
        if self.async_kafka and not self.async_kafka._is_event_loop_available():
            raise RuntimeError("Cannot produce message: event loop is not available or shutting down")

        if not await self._ensure_async_producer():
            raise RuntimeError("Failed to set up async Kafka producer")
        ak = self.async_kafka
        topic = self.producing_topic
        assert ak is not None and topic is not None
        await ak.produce_message(topic, message, key=key, timeout=timeout)

    async def async_consume_message(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume a message from Kafka asynchronously.

        Args:
            timeout: Maximum time to wait for message in seconds

        Returns:
            Message dictionary if available, None if no message received

        Raises:
            RuntimeError: If consumer is not initialized
            AsyncKafkaError: If message consumption fails
        """
        await self._ensure_async_producer()
        try:
            if not await self._ensure_async_consumer():
                logging.warning("Async Kafka consumer setup unsuccessful, returning None for consume request")
                return None

            ak = self.async_kafka
            assert ak is not None
            result = await ak.consume_message(timeout)
            if result is not None:
                result = self._parse_message(result)
            return result
        except RuntimeError as exc:
            logging.error("Runtime error in async_consume_message: %s", str(exc))
            return None
        except Exception as exc:
            logging.error("Unexpected error in async_consume_message: %s", str(exc))
            return None

    def configure_metrics_reporting(self, interval: int = 120, batch_size: int = 1000) -> None:
        """Configure background metrics reporting for both sync and async Kafka utilities.

        This method enables automatic metrics collection and reporting to the backend API
        for all Kafka operations performed through this deployment.

        Args:
            interval: Reporting interval in seconds (default: 120)
            batch_size: Maximum metrics per batch (default: 1000)
        """
        try:
            # Configure metrics reporting for sync Kafka utils if they exist
            if self.sync_kafka:
                self.sync_kafka.configure_metrics_reporting(
                    rpc_client=self.session.rpc, service_id=self.service_id, interval=interval, batch_size=batch_size
                )
                logging.info(f"Configured sync Kafka metrics reporting for deployment {self.service_id}")

            # Configure metrics reporting for async Kafka utils if they exist
            if self.async_kafka:
                self.async_kafka.configure_metrics_reporting(
                    rpc_client=self.session.rpc, service_id=self.service_id, interval=interval, batch_size=batch_size
                )
                logging.info(f"Configured async Kafka metrics reporting for deployment {self.service_id}")

            # If no Kafka utils exist yet, they will be configured when first created
            if not self.sync_kafka and not self.async_kafka:
                logging.info(
                    f"Metrics reporting will be configured when Kafka connections are established for deployment {self.service_id}"
                )

            # Store configuration for future Kafka utils creation
            self._metrics_config = {"interval": interval, "batch_size": batch_size, "enabled": True}

        except Exception as exc:
            logging.error(f"Error configuring metrics reporting for deployment {self.service_id}: {exc}")

    async def close(self) -> None:
        """Close Kafka producer and consumer connections.

        This method gracefully closes all Kafka connections without raising exceptions
        to ensure proper cleanup during shutdown.
        """
        errors: List[str] = []

        # Close sync Kafka connections
        if self.sync_kafka:
            try:
                logging.debug("Closing sync Kafka connections...")
                self.sync_kafka.close()
                self.sync_kafka = None
                logging.debug("Sync Kafka connections closed successfully")
            except Exception as exc:
                error_msg = f"Error closing sync Kafka connections: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.sync_kafka = None

        # Close async Kafka connections
        if self.async_kafka:
            try:
                logging.debug("Closing async Kafka connections...")
                await self.async_kafka.close()
                self.async_kafka = None
                logging.debug("Async Kafka connections closed successfully")
            except Exception as exc:
                error_msg = f"Error closing async Kafka connections: {str(exc)}"
                logging.error(error_msg)
                errors.append(error_msg)
                self.async_kafka = None

        if not errors:
            logging.info("Closed Kafka connections successfully")
        else:
            # Log errors but don't raise exception during cleanup
            logging.error("Errors occurred during Kafka close: %s", "; ".join(errors))
