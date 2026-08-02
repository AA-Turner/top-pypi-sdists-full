"""Kafka heartbeat reporter."""

from __future__ import annotations

import base64
import json
import logging
import time
from typing import Any, Dict, Optional

from kafka import KafkaProducer

logger = logging.getLogger(__name__)


class HeartbeatReporter:
    """Sends heartbeat messages to Kafka topic."""

    def __init__(
        self,
        session,
        streaming_gateway_id: str,
        topic: str = "streaming_gateway_heartbeat",
        kafka_timeout: float = 5.0,
    ):
        """Initialize heartbeat reporter.

        Args:
            session: Session object for API calls
            streaming_gateway_id: ID of the streaming gateway
            topic: Kafka topic to send heartbeats to (default: streaming_gateway_heartbeat)
            kafka_timeout: Timeout for Kafka operations
        """
        self.session = session
        self.streaming_gateway_id = streaming_gateway_id
        self.topic = topic
        self.kafka_timeout = kafka_timeout

        self.producer: Optional[KafkaProducer] = None
        self._last_init_attempt: float = 0.0
        self._init_retry_interval: float = 60.0  # Retry connection every 60s
        self._init_kafka_producer()

    def _init_kafka_producer(self):
        """Initialize Kafka producer for heartbeats."""
        self._last_init_attempt = time.time()
        try:
            response = self.session.rpc.get("/v1/actions/get_kafka_info")

            if not response or "data" not in response:
                logger.error(
                    "Failed to get Kafka info for heartbeat reporter. "
                    "Heartbeats will NOT be published until Kafka producer is initialized. "
                    "Will retry in %.0fs.",
                    self._init_retry_interval,
                )
                return

            data = response.get("data", {})

            ip = base64.b64decode(data["ip"]).decode("utf-8")
            port = base64.b64decode(data["port"]).decode("utf-8")
            bootstrap_servers = f"{ip}:{port}"

            kafka_config = {
                "bootstrap_servers": bootstrap_servers,
                "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
                "key_serializer": lambda k: k.encode("utf-8") if k else None,
                "acks": 1,
                "retries": 3,
                "max_in_flight_requests_per_connection": 1,
            }

            if "username" in data and "password" in data:
                username = base64.b64decode(data["username"]).decode("utf-8")
                password = base64.b64decode(data["password"]).decode("utf-8")

                # SECURITY: SASL_PLAINTEXT gives no channel encryption. This is
                # an accepted, documented dependency on the machine-wide
                # private-only firewall posture (broker reachable only over the
                # trusted/localhost subnet). Do not silently regress this to a
                # public bind without moving to SASL_SSL + CA verification.
                kafka_config.update(
                    {
                        "security_protocol": "SASL_PLAINTEXT",
                        "sasl_mechanism": "SCRAM-SHA-256",
                        "sasl_plain_username": username,
                        "sasl_plain_password": password,
                    }
                )

            self.producer = KafkaProducer(**kafka_config)
            logger.info(f"Kafka heartbeat producer initialized: {bootstrap_servers}, topic: {self.topic}")

        except Exception as e:
            logger.exception(
                "Failed to initialize Kafka heartbeat producer: %s. Will retry in %.0fs.",
                e,
                self._init_retry_interval,
            )
            self.producer = None

    def _ensure_producer(self) -> bool:
        """Lazy-reconnect: retry Kafka init if producer is None and retry interval elapsed."""
        if self.producer:
            return True
        if time.time() - self._last_init_attempt >= self._init_retry_interval:
            logger.info("Retrying Kafka heartbeat producer initialization...")
            self._init_kafka_producer()
        return self.producer is not None

    def send_heartbeat(self, camera_config: Dict[str, Any]) -> bool:
        """Send heartbeat to Kafka topic.

        Args:
            camera_config: Camera configuration payload to send

        Returns:
            True if successful, False otherwise
        """
        if not self._ensure_producer():
            logger.warning("Kafka producer not initialized, cannot send heartbeat")
            return False

        try:
            heartbeat = {
                "streaming_gateway_id": self.streaming_gateway_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "cameraConfig": camera_config,
            }

            future = self.producer.send(self.topic, value=heartbeat, key=self.streaming_gateway_id)
            future.get(timeout=self.kafka_timeout)

            logger.info(
                f"Heartbeat sent to Kafka topic '{self.topic}' with {len(camera_config.get('cameras', []))} cameras"
            )
            return True

        except Exception as e:
            logger.exception(f"Failed to send heartbeat to Kafka: {e}")
            return False

    def close(self):
        """Close Kafka producer."""
        if self.producer:
            try:
                self.producer.close(timeout=5)
                logger.info("Kafka heartbeat producer closed")
            except Exception as e:
                logger.exception(f"Error closing Kafka heartbeat producer: {e}")
