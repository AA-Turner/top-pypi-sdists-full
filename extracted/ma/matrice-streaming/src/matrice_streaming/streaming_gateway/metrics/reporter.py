"""Kafka metrics reporter."""

from __future__ import annotations

import base64
import json
import logging
import time
from typing import Any, Dict, Optional

from kafka import KafkaProducer

from .config import MetricsConfig

logger = logging.getLogger(__name__)


class MetricsReporter:
    """Sends metrics to Kafka topic."""

    def __init__(self, session, streaming_gateway_id: str, config: MetricsConfig):
        """Initialize metrics reporter.

        Args:
            session: Session object for API calls
            streaming_gateway_id: ID of the streaming gateway
            config: Metrics configuration
        """
        self.session = session
        self.streaming_gateway_id = streaming_gateway_id
        self.config = config

        self.producer: Optional[KafkaProducer] = None
        self._last_init_attempt: float = 0.0
        self._init_retry_interval: float = 60.0  # Retry connection every 60s
        self._init_kafka_producer()

    def _init_kafka_producer(self):
        """Initialize Kafka producer for metrics."""
        self._last_init_attempt = time.time()
        try:
            response = self.session.rpc.get("/v1/actions/get_kafka_info")

            if not response or "data" not in response:
                logger.error(
                    "Failed to get Kafka info for metrics reporter. "
                    "Metrics will NOT be published until Kafka producer is initialized. "
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
            logger.info(f"Kafka metrics producer initialized: {bootstrap_servers}")

        except Exception as e:
            logger.exception(
                "Failed to initialize Kafka metrics producer: %s. Will retry in %.0fs.",
                e,
                self._init_retry_interval,
            )
            self.producer = None

    def _ensure_producer(self) -> bool:
        """Lazy-reconnect: retry Kafka init if producer is None and retry interval elapsed."""
        if self.producer:
            return True
        if time.time() - self._last_init_attempt >= self._init_retry_interval:
            logger.info("Retrying Kafka metrics producer initialization...")
            self._init_kafka_producer()
        return self.producer is not None

    def send_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Send metrics to Kafka topic.

        Args:
            metrics: Metrics payload to send

        Returns:
            True if successful, False otherwise
        """
        if not self._ensure_producer():
            logger.warning("Kafka producer not initialized, cannot send metrics")
            return False

        try:
            future = self.producer.send(self.config.metrics_topic, value=metrics, key=self.streaming_gateway_id)
            future.get(timeout=self.config.kafka_timeout)
            return True

        except Exception as e:
            logger.exception(f"Failed to send metrics to Kafka: {e}")
            return False

    def close(self):
        """Close Kafka producer."""
        if self.producer:
            try:
                self.producer.close(timeout=5)
                logger.info("Kafka metrics producer closed")
            except Exception as e:
                logger.exception(f"Error closing Kafka producer: {e}")
