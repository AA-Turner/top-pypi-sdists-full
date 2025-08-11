"""Module providing synchronous and asynchronous Kafka utilities."""

import json
import logging
import time
from typing import Dict, List, Optional, Tuple, Union, Any
from confluent_kafka import (
    Consumer,
    Producer,
    KafkaError,
    TopicPartition,
    OFFSET_INVALID
)
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError as AsyncKafkaError
from aiokafka.consumer.subscription_state import ConsumerRebalanceListener
import asyncio


class KafkaUtils:
    """Utility class for synchronous Kafka operations."""

    def __init__(
        self, 
        bootstrap_servers: str,
        sasl_mechanism: Optional[str] = "SCRAM-SHA-256",
        sasl_username: Optional[str] = "matrice-sdk-user",
        sasl_password: Optional[str] = "matrice-sdk-password",
        security_protocol: str = "SASL_PLAINTEXT"
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
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.security_protocol = security_protocol
        self.producer = None
        self.consumer = None
        self._consumer_config = None
        self._consumer_topics = None
        self._consumer_group_id = None
        self._assigned = False
        logging.info(
            "Initialized KafkaUtils with servers: %s",
            bootstrap_servers,
        )

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
            "batch.size": 8388608, # 8MB
            "queue.buffering.max.ms": 50,
            "message.max.bytes": 25000000, # 25MB
            'queue.buffering.max.messages': 100000,
            "delivery.timeout.ms": 600000,
            "request.timeout.ms": 600000,
            "compression.type": "snappy"
        }
        

        # Add SASL authentication if configured
        if self.sasl_mechanism and self.sasl_username and self.sasl_password:
            producer_config.update({
                "security.protocol": self.security_protocol,
                "sasl.mechanism": self.sasl_mechanism,
                "sasl.username": self.sasl_username,
                "sasl.password": self.sasl_password,
            })

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
        group_instance_id: str = None,
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
            consumer_config.update({
                "security.protocol": self.security_protocol,
                "sasl.mechanism": self.sasl_mechanism,
                "sasl.username": self.sasl_username,
                "sasl.password": self.sasl_password,
            })

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
            self.consumer.subscribe(topics, on_assign=self._on_assign_callback)

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

    def _serialize_key(self, key: Any) -> Optional[bytes]:
        """Serialize message key to bytes.
        
        Args:
            key: Message key to serialize
            
        Returns:
            Serialized key as bytes or None
        """
        if key is None:
            return None
        elif isinstance(key, str):
            return key.encode('utf-8')
        elif isinstance(key, bytes):
            return key
        else:
            return str(key).encode('utf-8')

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

        # Serialize value and key
        value_bytes = self._serialize_value(value)
        key_bytes = self._serialize_key(key)

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
                headers=headers,
                on_delivery=self._delivery_callback,
            )
            # Poll to trigger delivery callbacks and handle any queued messages
            self.producer.poll(0)
            
            if wait_for_delivery:
                remaining = int(self.producer.flush(timeout=timeout))
                if remaining > 0:
                    raise KafkaError(f"Failed to deliver {remaining} messages within timeout")
            logging.debug(
                "Successfully produced message to topic: %s",
                topic,
            )
        except KafkaError as exc:
            error_msg = f"Failed to produce message: {str(exc)}"
            logging.error(error_msg)
            raise

    def _delivery_callback(self, err, msg):
        """Callback for message delivery reports."""
        if err is not None:
            logging.error('Message delivery failed: %s', str(err))
        else:
            logging.debug('Message delivered to %s [%d] at offset %d',
                         msg.topic(), msg.partition(), msg.offset())

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
        try:
            msg = self.consumer.poll(timeout)
            if msg is None:
                return None
            if msg.error():
                error_msg = f"Consumer error: {msg.error()}"
                logging.error(error_msg)

                # Check if the error indicates a disconnection
                if msg.error().code() in (
                    KafkaError._TIMED_OUT,
                    KafkaError.NETWORK_EXCEPTION,
                    KafkaError._TRANSPORT,
                    KafkaError._TIMED_OUT,
                    KafkaError._MAX_POLL_EXCEEDED
                ):
                    logging.warning("Kafka consumer disconnected, attempting to reconnect")
                    self._reconnect_consumer()
                    return None

                # Create a KafkaError instance with the error code, not the string
                raise KafkaError(msg.error().code())

            # Parse the message value
            value = self._parse_message_value(msg.value())

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
            error_msg = f"Failed to consume message: {str(exc)}"
            logging.error(error_msg)

            # Try to reconnect if it's a connection-related error
            if exc.code() in (
                KafkaError._TIMED_OUT,
                KafkaError.NETWORK_EXCEPTION,
                KafkaError._TRANSPORT,
                KafkaError._TIMED_OUT,
                KafkaError._MAX_POLL_EXCEEDED
            ):
                logging.warning("Kafka consumer error, attempting to reconnect")
                try:
                    self._reconnect_consumer()
                    return None
                except Exception as reconnect_exc:
                    logging.error("Failed to reconnect consumer: %s", str(reconnect_exc))

            raise

    def close(self) -> None:
        """Close Kafka producer and consumer connections."""
        try:
            if self.producer:
                # Poll aggressively before flushing to process any pending callbacks
                logging.info("Processing pending producer callbacks before close...")
                for _ in range(20):
                    self.producer.poll(0.1)
                
                # First attempt with standard timeout
                remaining = int(self.producer.flush(timeout=10))  # Increased initial timeout
                
                # If messages still remain, try with extended timeout
                if remaining > 0:
                    logging.warning("%d messages still in queue, extending flush timeout", remaining)
                    # More aggressive polling during extended flush
                    for _ in range(50):
                        self.producer.poll(0.1)
                    remaining = int(self.producer.flush(timeout=30))  # Extended timeout
                    
                    if remaining > 0:
                        logging.error("%d messages could not be delivered within timeout", remaining)
                    else:
                        logging.info("All remaining messages delivered successfully")
                
                # Properly close the producer
                try:
                    self.producer.close()
                except Exception as close_exc:
                    logging.warning("Error during producer close: %s", str(close_exc))
                
                self.producer = None
                
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


class AsyncKafkaUtils:
    """Utility class for asynchronous Kafka operations."""

    def __init__(
        self, 
        bootstrap_servers: str,
        sasl_mechanism: Optional[str] = "SCRAM-SHA-256",
        sasl_username: Optional[str] = "matrice-sdk-user",
        sasl_password: Optional[str] = "matrice-sdk-password",
        security_protocol: str = "SASL_PLAINTEXT"
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
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.security_protocol = security_protocol
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumer: Optional[AIOKafkaConsumer] = None
        self._consumer_config = None
        self._consumer_topics = None
        self._consumer_group_id = None
        self._assigned = None
        logging.info("Initialized AsyncKafkaUtils with servers: %s", bootstrap_servers)

    async def setup_producer(self, config: Optional[Dict] = None) -> None:
        """Set up async Kafka producer.
        
        Args:
            config: Additional producer configuration
            
        Raises:
            AsyncKafkaError: If producer initialization fails
        """
        producer_config = {
            "bootstrap_servers": self.bootstrap_servers,
            "acks": "all",  # Changed from "all" for better throughput
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
            producer_config.update({
                "security_protocol": self.security_protocol,
                "sasl_mechanism": self.sasl_mechanism,
                "sasl_plain_username": self.sasl_username,
                "sasl_plain_password": self.sasl_password,
            })
            
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
            await self.producer.start()
            logging.info("Successfully set up async Kafka producer")
        except AsyncKafkaError as exc:
            logging.error("Failed to start async producer: %s", str(exc))
            # Clean up on failure
            self.producer = None
            raise

    class RebalanceListener(ConsumerRebalanceListener):
        """Listener for partition rebalance events."""
        
        def __init__(self, consumer, parent):
            self.consumer = consumer
            self.parent = parent
            
        async def on_partitions_assigned(self, partitions):
            if partitions:
                logging.info(f"Async consumer rebalanced with {len(partitions)} partition(s) assigned")
                
                # Check committed offsets for each partition
                try:
                    # committed = await self.consumer.committed(partitions)
                    # for tp, offset in committed.items():
                    #     if offset == OFFSET_INVALID:
                    #         # No offset saved for this partition, seek to beginning
                    #         logging.info(f"No offset for {tp.topic}:{tp.partition}, seeking to beginning")
                    #         await self.consumer.seek(TopicPartition(tp.topic, tp.partition, 0))
                    #     else:
                    #         logging.info(f"Resuming {tp.topic}:{tp.partition} at offset {offset}")
                    pass
                except Exception as e:
                    logging.warning(f"Error checking committed offsets: {str(e)}")
                
                self.parent._assigned.set()
            else:
                logging.warning("Async consumer rebalanced but no partitions were assigned")
        
        async def on_partitions_revoked(self, revoked):
            logging.info(f"Async consumer partitions revoked: {len(revoked)} partition(s)")
            self.parent._assigned.clear()

    async def _wait_for_assignment(self, timeout: float = 600) -> None:
        """Wait for partition assignment to complete.
        
        Args:
            timeout: Maximum time to wait for assignment in seconds
        """
        try:
            await asyncio.wait_for(self._assigned.wait(), timeout=timeout)
            logging.info("Async consumer is now ready to receive messages")
        except asyncio.TimeoutError:
            logging.warning(f"Async consumer rebalancing timed out after {timeout} seconds")
            # Final check for assignment
            assignment = self.consumer.assignment()
            if assignment:
                logging.info(f"Async consumer has {len(assignment)} partition(s) assigned after timeout")
                self._assigned.set()
            else:
                logging.warning("Async consumer has no partitions assigned after rebalancing timeout")

    async def setup_consumer(
        self,
        topics: List[str],
        group_id: str,
        group_instance_id: str = None,
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
            consumer_config.update({
                "security_protocol": self.security_protocol,
                "sasl_mechanism": self.sasl_mechanism,
                "sasl_plain_username": self.sasl_username,
                "sasl_plain_password": self.sasl_password,
            })
            
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
                listener = self.RebalanceListener(self.consumer, self)
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
                if ("unknownerror" in error_msg or "group coordinator not available" in error_msg) and attempt < max_retries - 1:
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
            listener = self.RebalanceListener(self.consumer, self)
            
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

    def _serialize_key(self, key: Any) -> Optional[bytes]:
        """Serialize message key to bytes.
        
        Args:
            key: Message key to serialize
            
        Returns:
            Serialized key as bytes or None
        """
        if key is None:
            return None
        elif isinstance(key, str):
            return key.encode('utf-8')
        elif isinstance(key, bytes):
            return key
        else:
            return str(key).encode('utf-8')

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
            
        try:
            await self.producer.send_and_wait(
                topic,
                value=value_bytes,
                key=key_bytes,
                headers=headers,
            )
            logging.debug("Successfully produced message to topic: %s", topic)
        except AsyncKafkaError as exc:
            logging.error("Failed to produce message: %s", str(exc))
            raise

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
        if not self._assigned.is_set():
            try:
                await asyncio.wait_for(self._assigned.wait(), timeout=60.0)  # Increased from 30.0 to 60.0
            except asyncio.TimeoutError:
                logging.warning("Timed out waiting for partition assignment")
                return None
        
        try:
            # Use getone with timeout to avoid blocking indefinitely
            try:
                msg = await asyncio.wait_for(self.consumer.getone(), timeout=timeout)
                
                # Parse the message value
                value = self._parse_message_value(msg.value)
                
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
                # Return None if timeout occurs, this is expected behavior
                return None
        except AsyncKafkaError as exc:
            logging.error("Failed to consume message: %s", str(exc))
            
            # Check if it's a connection-related error
            if isinstance(exc, (
                AsyncKafkaError.ConnectionError,
                AsyncKafkaError.NodeNotReadyError,
                AsyncKafkaError.RequestTimedOutError
            )):
                logging.warning("Async Kafka consumer disconnected, attempting to reconnect")
                try:
                    await self._reconnect_consumer()
                    return None
                except Exception as reconnect_exc:
                    logging.error("Failed to reconnect async consumer: %s", str(reconnect_exc))
            
            raise
        except Exception as exc:
            logging.error("Unexpected error consuming message: %s", str(exc))
            
            # Try to reconnect for unexpected errors that might be connection-related
            try:
                await self._reconnect_consumer()
            except Exception:
                pass  # Ignore reconnection errors here
                
            # Return None for non-critical errors
            return None

    async def close(self) -> None:
        """Close async Kafka producer and consumer connections."""
        errors = []
        
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
        consumer_group_id: str = None, 
        consumer_group_instance_id: str = None,
        sasl_mechanism: Optional[str] = "SCRAM-SHA-256",
        sasl_username: Optional[str] = "matrice-sdk-user",
        sasl_password: Optional[str] = "matrice-sdk-password",
        security_protocol: str = "SASL_PLAINTEXT",
        custom_request_service_id: str = None,
        custom_result_service_id: str = None,
    ) -> None:
        """Initialize Kafka deployment with deployment ID.

        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            type: Type of deployment ("client" or "server")
            consumer_group_id: Kafka consumer group ID
            consumer_group_instance_id: Kafka consumer group instance ID for static membership
            sasl_mechanism: SASL mechanism for authentication
            sasl_username: Username for SASL authentication
            sasl_password: Password for SASL authentication
            security_protocol: Security protocol for Kafka connection
            custom_request_service_id: Custom request service ID
            custom_result_service_id: Custom result service ID
        Raises:
            ValueError: If type is not "client" or "server"
        """
        self.session = session
        self.rpc = session.rpc
        self.service_id = service_id
        self.type = type
        self.sasl_mechanism = sasl_mechanism
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
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

        self.setup_success = False
        self.bootstrap_server = None
        self.request_topic = None
        self.result_topic = None
        self.producing_topic = None
        self.consuming_topic = None

        # Initialize Kafka utilities as None - create as needed
        self.sync_kafka = None
        self.async_kafka = None

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
            service_id, type, self.consumer_group_id, self.consumer_group_instance_id
        )

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
                    logging.warning("Failed to get Kafka info again. Streaming API unavailable. "
                                   "Please check your Kafka deployment and try initializing again.")
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
            self.sync_kafka = KafkaUtils(self.bootstrap_server, self.sasl_mechanism, self.sasl_username, self.sasl_password, self.security_protocol)
        
        try:
            if not hasattr(self.sync_kafka, 'producer') or not self.sync_kafka.producer:
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
            self.sync_kafka = KafkaUtils(self.bootstrap_server, self.sasl_mechanism, self.sasl_username, self.sasl_password, self.security_protocol)
        
        try:
            if not hasattr(self.sync_kafka, 'consumer') or not self.sync_kafka.consumer:
                self.sync_kafka.setup_consumer([self.consuming_topic], self.consumer_group_id, self.consumer_group_instance_id)
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
            self.async_kafka = AsyncKafkaUtils(self.bootstrap_server, self.sasl_mechanism, self.sasl_username, self.sasl_password, self.security_protocol)
        
        try:
            if not hasattr(self.async_kafka, 'producer') or not self.async_kafka.producer:
                await self.async_kafka.setup_producer()
            return True
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
            self.async_kafka = AsyncKafkaUtils(self.bootstrap_server, self.sasl_mechanism, self.sasl_username, self.sasl_password, self.security_protocol)
        
        try:
            if not hasattr(self.async_kafka, 'consumer') or not self.async_kafka.consumer:
                await self.async_kafka.setup_consumer([self.consuming_topic], self.consumer_group_id, self.consumer_group_instance_id)
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

            request_data = request_topic.get('data', {})
            result_data = result_topic.get('data', {})

            if not request_data or not result_data:
                raise ValueError("Empty response data from Kafka topic API")

            ip_address = request_data.get('ip_address')
            port = request_data.get('port')

            if not ip_address or not port:
                logging.warning(f"Invalid bootstrap server information: IP={ip_address}, Port={port}")
                setup_success = False
                return setup_success, None, None, None

            bootstrap_server = f"{ip_address}:{port}"

            return setup_success, bootstrap_server, request_data['topic'], result_data['topic']
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
        self.sync_kafka.produce_message(self.producing_topic, message, key=key, timeout=timeout)

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

        result = self.sync_kafka.consume_message(timeout)
        result = self._parse_message(result)
        return result

    async def async_produce_message(self, message: dict, timeout: float = 60.0, key: Optional[str] = None) -> None:
        """Produce a message to Kafka asynchronously.

        Args:
            message: Message to produce
            timeout: Maximum time to wait for message delivery in seconds
            key: Optional key for message partitioning (stream_id/camera_id)
            
        Raises:
            RuntimeError: If producer is not initialized
            ValueError: If message is invalid
            AsyncKafkaError: If message production fails
        """
        if not await self._ensure_async_producer():
            raise RuntimeError("Failed to set up async Kafka producer")
        await self.async_kafka.produce_message(self.producing_topic, message, key=key, timeout=timeout)

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

            result = await self.async_kafka.consume_message(timeout)
            result = self._parse_message(result)
            return result
        except RuntimeError as exc:
            logging.error("Runtime error in async_consume_message: %s", str(exc))
            return None
        except Exception as exc:
            logging.error("Unexpected error in async_consume_message: %s", str(exc))
            return None

    async def close(self) -> None:
        """Close Kafka producer and consumer connections.
        
        This method gracefully closes all Kafka connections without raising exceptions
        to ensure proper cleanup during shutdown.
        """
        errors = []

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
