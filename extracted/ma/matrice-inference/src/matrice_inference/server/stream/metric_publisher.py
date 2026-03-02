"""
Inference metrics aggregation and publishing system.

This module provides a background thread that periodically collects metrics
from all active workers, aggregates them by worker type, and publishes to
a configured transport (Kafka by default).

Thread Safety:
    - Uses threading.Timer for periodic execution
    - Atomic snapshot operations on individual WorkerMetrics instances
    - No shared state between collection cycles

Design:
    - Runs on dedicated background thread (non-daemon for graceful shutdown)
    - Wakes every INFERENCE_METRIC_LOGGING_INTERVAL seconds
    - Collects snapshots from all workers via StreamingPipeline reference
    - Aggregates by worker_type (consumer/inference/post_processing/producer)
    - Publishes via pluggable MetricPublisher interface
    - Gracefully handles worker lifecycle changes
"""

import json
import logging
import os
import time
import threading
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from matrice_common.rpc import RPC

logger = logging.getLogger(__name__)

    
class MetricPublisher(ABC):
    """
    Abstract interface for metric publishing.
    
    Implementations must be thread-safe as they may be called from
    the background aggregator thread.
    """
    
    @abstractmethod
    def publish(self, metric_log: Dict[str, Any]) -> bool:
        """
        Publish a metric log.
        
        Args:
            metric_log: InferenceMetricLog dictionary matching schema
        
        Returns:
            True if publish succeeded, False otherwise
        
        Note:
            Implementations should catch and log exceptions internally
            to avoid breaking the aggregator loop.
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """
        Clean up publisher resources.
        
        Called during InferenceMetricLogger shutdown.
        """
        pass


class KafkaMetricPublisher(MetricPublisher):
    """
    Kafka-based metric publisher using confluent-kafka.
    
    Follows the same pattern as error logging producer for consistency.
    Lazy-loads Kafka dependencies and fetches config via RPC.
    
    Thread Safety:
        Producer.produce() is thread-safe per confluent-kafka documentation.
    """
    
    TOPIC_NAME = "app_deployment_metrics"
    
    def __init__(
        self,
        rpc_client: Optional[Any] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None
    ):
        """
        Initialize Kafka publisher.

        Args:
            rpc_client: Optional RPC client for fetching Kafka config
            access_key: Matrice access key (falls back to env var)
            secret_key: Matrice secret key (falls back to env var)

        Raises:
            ImportError: If confluent-kafka not available
            ValueError: If credentials missing or Kafka config fetch fails
        """
        self.producer = None
        self._delivery_failures = 0
        self._delivery_successes = 0
        self._initialize_producer(rpc_client, access_key, secret_key)
    
    def _initialize_producer(
        self,
        rpc_client: Optional[Any],
        access_key: Optional[str],
        secret_key: Optional[str]
    ) -> None:
        """Initialize Kafka producer with config from RPC."""
        try:
            try:
                from confluent_kafka import Producer
            except ImportError:
                logger.error(
                    "confluent-kafka not installed. "
                    "Install with: pip install confluent-kafka"
                )
                raise
            
            access_key = access_key or os.environ.get("MATRICE_ACCESS_KEY_ID")
            secret_key = secret_key or os.environ.get("MATRICE_SECRET_ACCESS_KEY")
            
            if not access_key or not secret_key:
                raise ValueError(
                    "Access key and secret key are required. "
                    "Set MATRICE_ACCESS_KEY_ID and MATRICE_SECRET_ACCESS_KEY "
                    "environment variables or pass explicitly."
                )
            
            if rpc_client is None:
                try:
                    rpc_client = RPC(access_key=access_key, secret_key=secret_key)
                except ImportError:
                    raise ImportError(
                        "RPC client not available. "
                        "Cannot fetch Kafka configuration."
                    )
            
            response = rpc_client.get(
                path="/v1/actions/get_kafka_info",
                raise_exception=True
            )
            
            if not response or not response.get("success"):
                raise ValueError(
                    f"Failed to fetch Kafka config: "
                    f"{response.get('message', 'No response')}"
                )
            
            import base64
            encoded_ip = response["data"]["ip"]
            encoded_port = response["data"]["port"]
            ip = base64.b64decode(encoded_ip).decode("utf-8")
            port = base64.b64decode(encoded_port).decode("utf-8")
            bootstrap_servers = f"{ip}:{port}"
            
            self.producer = Producer({
                "bootstrap.servers": bootstrap_servers,
                "acks": "all",
                "retries": 3,
                "retry.backoff.ms": 1000,
                "request.timeout.ms": 30000,
                "max.in.flight.requests.per.connection": 5,
                "linger.ms": 10,
                "batch.size": 4096,
                "queue.buffering.max.ms": 50,
                "log_level": 0,
            })
            
            logger.info(
                f"Initialized Kafka metric publisher: {bootstrap_servers}, "
                f"topic: {self.TOPIC_NAME}"
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize Kafka publisher: {e}", exc_info=True)
            self.producer = None
            raise
    
    def publish(self, metric_log: Dict[str, Any]) -> bool:
        """
        Publish metric log to Kafka.
        
        Args:
            metric_log: InferenceMetricLog dictionary
        
        Returns:
            True if publish succeeded, False otherwise
        """
        if not self.producer:
            logger.warning("Kafka producer not initialized, skipping publish")
            return False
        
        try:
            # Extract deployment_id for message key NOTE
            deployment_id = metric_log.get("deployment_id", "unknown")
            
            value = json.dumps(metric_log).encode("utf-8")
            key = deployment_id.encode("utf-8")
            
            # Produce message
            self.producer.produce(
                topic=self.TOPIC_NAME,
                value=value,
                key=key,
                callback=self._delivery_callback
            )

            # Trigger delivery with short timeout for better delivery confirmation
            self.producer.poll(0.1)

            return True
            
        except Exception as e:
            logger.error(f"Failed to publish metric log: {e}", exc_info=True)
            return False
    
    def _delivery_callback(self, err, msg):
        """Kafka delivery callback for logging and tracking."""
        if err:
            self._delivery_failures += 1
            logger.error(
                f"Metric log delivery failed: {err} "
                f"(total failures: {self._delivery_failures})"
            )
        else:
            self._delivery_successes += 1
            logger.debug(
                f"Metric log delivered to {msg.topic()} "
                f"[partition {msg.partition()}] "
                f"(total successes: {self._delivery_successes})"
            )
    
    def close(self) -> None:
        """Flush and close Kafka producer."""
        if self.producer:
            try:
                logger.info("Flushing Kafka metric publisher...")
                self.producer.flush(timeout=5.0)
                logger.info("Kafka metric publisher closed")
            except Exception as e:
                logger.error(f"Error closing Kafka publisher: {e}")


class NoOpMetricPublisher(MetricPublisher):
    """
    No-op publisher for testing or when Kafka is unavailable.
    
    Logs metrics to DEBUG level instead of publishing.
    """
    
    def publish(self, metric_log: Dict[str, Any]) -> bool:
        """Log metric instead of publishing."""
        logger.debug(f"NoOp publish: {json.dumps(metric_log, indent=2)}")
        return True
    
    def close(self) -> None:
        """Nothing to clean up."""
        pass


