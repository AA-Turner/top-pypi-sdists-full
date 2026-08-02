"""Auto-generated stub for module: reporter."""
from typing import Any, Dict, Optional

from __future__ import annotations
from config import MetricsConfig
from kafka import KafkaProducer
import base64
import json
import logging
import time

# Constants
logger: Any

# Classes
class MetricsReporter:
    """
    Sends metrics to Kafka topic.
    """

    def __init__(self: Any, session: Any, streaming_gateway_id: str, config: Any) -> None: ...
        """
        Initialize metrics reporter.
        
                Args:
                    session: Session object for API calls
                    streaming_gateway_id: ID of the streaming gateway
                    config: Metrics configuration
        """

    def close(self: Any) -> Any: ...
        """
        Close Kafka producer.
        """

    def send_metrics(self: Any, metrics: Dict[str, Any]) -> bool: ...
        """
        Send metrics to Kafka topic.
        
                Args:
                    metrics: Metrics payload to send
        
                Returns:
                    True if successful, False otherwise
        """

