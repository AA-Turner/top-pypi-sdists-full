"""Generic Kafka event listener for real-time event processing."""

from __future__ import annotations

import base64
import logging
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Union

from kafka import KafkaConsumer
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)


class EventListener:
    """Generic listener for Kafka events with filtering and custom handlers.

    This class provides a flexible event listening infrastructure that can be used
    for various event types (camera events, app events, etc.) from Kafka topics.

    Example:
        ```python
        import logging
        logger = logging.getLogger(__name__)

        def my_handler(event):
            logger.info("Received event: %s", event.get("eventType"))

        listener = EventListener(
            session=session,
            topics=['Camera_Events_Topic', 'App_Events_Topic'],
            event_handler=my_handler,
            filter_field='streamingGatewayId',
            filter_value='gateway123'
        )
        listener.start()
        ```
    """

    def __init__(
        self,
        session,
        topics: Union[str, List[str]],
        event_handler: Callable[[Dict[str, Any]], None],
        filter_field: Optional[str] = None,
        filter_value: Optional[str] = None,
        consumer_group_id: Optional[str] = None,
        offset_reset: str = "latest",
        max_poll_interval_ms: int = 300000,
        session_timeout_ms: int = 45000,
        heartbeat_interval_ms: int = 15000,
    ) -> None:
        """Initialize event listener.

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
        self.session = session
        self.topics = topics if isinstance(topics, list) else [topics]
        self.event_handler = event_handler
        self.filter_field = filter_field
        self.filter_value = filter_value
        self.offset_reset = offset_reset
        self.max_poll_interval_ms = max_poll_interval_ms
        self.session_timeout_ms = session_timeout_ms
        self.heartbeat_interval_ms = heartbeat_interval_ms

        # Generate consumer group ID if not provided
        if consumer_group_id:
            self.consumer_group_id = consumer_group_id
        else:
            # Use first topic name as base for group ID
            topic_base = self.topics[0].replace("_Topic", "").lower()
            filter_suffix = f"_{filter_value}" if filter_value else ""
            self.consumer_group_id = f"{topic_base}_consumer{filter_suffix}"

        # State
        self.consumer: Optional[KafkaConsumer] = None
        self.is_listening = False
        self._stop_event = threading.Event()
        self._listener_thread: Optional[threading.Thread] = None

        # Public liveness signal: monotonic timestamp of the most recent poll
        # cycle (updated on EVERY poll, even when no messages are returned).
        # An external watchdog reads this attribute by name to detect a stalled
        # or silently-evicted consumer, so the name is a public contract.
        self.last_poll_monotonic: float = time.monotonic()

        # Statistics
        self.stats = {
            "events_received": 0,
            "events_processed": 0,
            "events_filtered": 0,
            "events_failed": 0,
        }

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"EventListener initialized for topics {self.topics} (filter: {filter_field}={filter_value})")

    def _get_kafka_config(self):
        """Get Kafka configuration from API.

        Returns:
            dict: Kafka configuration or None if failed
        """
        try:
            response = self.session.rpc.get("/v1/actions/get_kafka_info")

            if not response or not response.get("success"):
                self.logger.warning(f"Failed to fetch Kafka event config: {response.get('message', 'No response')}")
                return None

            # Decode base64 encoded values
            data = response.get("data", {})
            encoded_ip = data.get("ip")
            encoded_port = data.get("port")

            if not encoded_ip or not encoded_port:
                self.logger.warning("Missing IP or port in Kafka config response")
                return None

            ip = base64.b64decode(encoded_ip).decode("utf-8")
            port = base64.b64decode(encoded_port).decode("utf-8")
            bootstrap_servers = f"{ip}:{port}"

            # Build Kafka config with consumer settings
            config = {
                "bootstrap_servers": bootstrap_servers,
                "group_id": self.consumer_group_id,
                "auto_offset_reset": self.offset_reset,
                "enable_auto_commit": True,
                # Explicit liveness/heartbeat tuning (kafka-python otherwise uses
                # its own defaults, which can silently evict the consumer).
                "max_poll_interval_ms": self.max_poll_interval_ms,
                "session_timeout_ms": self.session_timeout_ms,
                "heartbeat_interval_ms": self.heartbeat_interval_ms,
                "value_deserializer": lambda m: self._deserialize_json(m),
                "key_deserializer": lambda m: m.decode("utf-8") if m else None,
            }

            # SASL authentication is configured via environment variables:
            # KAFKA_SASL_USERNAME and KAFKA_SASL_PASSWORD
            # See kafka_stream.py for usage pattern.

            return config

        except Exception as e:
            self.logger.error(f"Exception getting Kafka configuration: {e}")
            return None

    def _deserialize_json(self, message):
        """Deserialize JSON message.

        Args:
            message: Raw message bytes

        Returns:
            dict: Deserialized message or empty dict on error
        """
        import json

        try:
            return json.loads(message.decode("utf-8"))
        except Exception as e:
            raw_preview = message[:200] if message else b"<empty>"
            self.logger.warning(f"Non-JSON Kafka message (len={len(message) if message else 0}): {raw_preview!r} — {e}")
            return {}

    def start(self) -> bool:
        """Start listening to events.

        Returns:
            bool: True if started successfully
        """
        if self.is_listening:
            self.logger.warning("Event listener already running")
            return False

        try:
            # Create Kafka consumer
            kafka_config = self._get_kafka_config()
            if kafka_config:
                self.consumer = KafkaConsumer(**kafka_config)
            else:
                self.logger.error("Failed to get Kafka configuration")
                return False

            # Subscribe to topics
            self.consumer.subscribe(self.topics)
            self.logger.info(f"Subscribed to topics: {self.topics}")

            # Start listener thread
            self._stop_event.clear()
            self.is_listening = True

            thread_name = f"EventListener-{'-'.join(self.topics)}"
            self._listener_thread = threading.Thread(target=self._listen_loop, daemon=True, name=thread_name)
            self._listener_thread.start()

            self.logger.info("Event listener started")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start event listener: {e}")
            self.is_listening = False
            return False

    def stop(self):
        """Stop listening."""
        if not self.is_listening:
            return

        self.logger.info("Stopping event listener...")
        self.is_listening = False
        self._stop_event.set()

        # Wait for thread to stop
        if self._listener_thread and self._listener_thread.is_alive():
            self._listener_thread.join(timeout=3.0)

        # Close consumer
        if self.consumer:
            try:
                self.consumer.close()
            except Exception as e:
                self.logger.error(f"Error closing consumer: {e}")

        self.logger.info("Event listener stopped")

    def _try_recreate_consumer(self) -> bool:
        """Attempt to recreate Kafka consumer after failure."""
        try:
            if self.consumer:
                try:
                    self.consumer.close()
                except Exception:
                    pass
                self.consumer = None

            kafka_config = self._get_kafka_config()
            if not kafka_config:
                return False

            self.consumer = KafkaConsumer(**kafka_config)
            self.consumer.subscribe(self.topics)
            self.logger.info(f"Kafka consumer recreated for topics: {self.topics}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to recreate Kafka consumer: {e}")
            return False

    def _listen_loop(self):
        """Listen and process events with consumer reconnection."""
        self.logger.info(f"Event listening started for topics: {self.topics}")
        retry_delay = 1.0

        # Time-based staleness watchdog. A silent max_poll_interval_ms eviction
        # leaves poll() returning empty with no exception, so an exception-only
        # recreate never fires. Track the last forward progress and proactively
        # recreate the consumer if no progress is seen for longer than
        # 1.5 * max_poll_interval_ms.
        staleness_threshold = (self.max_poll_interval_ms / 1000.0) * 1.5
        last_progress = time.monotonic()

        while not self._stop_event.is_set():
            try:
                if not self.consumer:
                    if not self._try_recreate_consumer():
                        time.sleep(min(retry_delay, 30.0))
                        retry_delay = min(retry_delay * 2, 60.0)
                        continue
                    retry_delay = 1.0
                    last_progress = time.monotonic()

                messages = self.consumer.poll(timeout_ms=1000, max_records=10)

                # Public liveness signal — updated on EVERY poll cycle, even
                # when poll() returns no messages.
                self.last_poll_monotonic = time.monotonic()

                for topic_partition, records in messages.items():
                    for record in records:
                        try:
                            self._process_event(record)
                        except Exception as e:
                            self.logger.error(f"Error processing event: {e}")
                            self.stats["events_failed"] += 1

                if messages:
                    # Real forward progress.
                    last_progress = self.last_poll_monotonic
                elif self.last_poll_monotonic - last_progress > staleness_threshold:
                    # No exception, but the broker may have silently evicted us.
                    self.logger.warning(
                        "No Kafka progress for %.0fs (> %.0fs threshold); recreating consumer for topics %s",
                        self.last_poll_monotonic - last_progress,
                        staleness_threshold,
                        self.topics,
                    )
                    self._try_recreate_consumer()
                    last_progress = time.monotonic()  # reset timer after recreate

                retry_delay = 1.0  # reset on success

            except KafkaError as e:
                self.logger.error(f"Kafka error: {e}")
                time.sleep(min(retry_delay, 30.0))
                retry_delay = min(retry_delay * 2, 60.0)
                # Recreate consumer on persistent Kafka errors
                self._try_recreate_consumer()
            except Exception as e:
                self.logger.error(f"Error in listen loop: {e}")
                time.sleep(min(retry_delay, 30.0))
                retry_delay = min(retry_delay * 2, 60.0)
                self._try_recreate_consumer()

        self.logger.info("Event listening ended")

    def _process_event(self, record):
        """Process a single event.

        Args:
            record: Kafka consumer record
        """
        self.stats["events_received"] += 1

        event = record.value

        # Handle double-JSON-encoded messages: if the deserialized value is
        # still a string, try parsing it one more time.
        if isinstance(event, str):
            import json

            try:
                event = json.loads(event)
            except (json.JSONDecodeError, TypeError):
                self.logger.warning(f"Non-JSON string event, forwarding as empty dict: {event[:200]}")
                event = {}

        if not isinstance(event, dict):
            self.logger.warning(f"Non-dict event (type={type(event).__name__}), forwarding as empty dict")
            event = {}

        # Apply filtering if configured (skip for empty events — always pass through)
        if event and self.filter_field and self.filter_value:
            event_filter_value = event.get(self.filter_field)
            if event_filter_value != self.filter_value:
                self.stats["events_filtered"] += 1
                return

        # Get event details for logging
        event_type = event.get("eventType", "non-json-trigger") if event else "non-json-trigger"

        # Log based on available data
        log_parts = [f"Event: {event_type}"]
        if event and "data" in event and isinstance(event["data"], dict):
            data = event["data"]
            if "id" in data:
                log_parts.append(f"id={data['id']}")
            if "cameraName" in data:
                log_parts.append(f"camera={data['cameraName']}")
            elif "topicName" in data:
                log_parts.append(f"topic={data['topicName']}")

        self.logger.info(" - ".join(log_parts))

        # Call handler — any message type triggers refresh
        try:
            self.event_handler(event)
            self.stats["events_processed"] += 1
        except Exception as e:
            self.logger.error(f"Error in event handler: {e}")
            self.stats["events_failed"] += 1

    def get_statistics(self) -> dict:
        """Get listener statistics.

        Returns:
            dict: Statistics including events received, processed, filtered, and failed
        """
        return {
            **self.stats,
            "is_listening": self.is_listening,
            "topics": self.topics,
            "filter": f"{self.filter_field}={self.filter_value}" if self.filter_field else None,
        }
