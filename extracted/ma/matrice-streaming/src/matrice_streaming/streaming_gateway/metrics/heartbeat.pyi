"""Auto-generated stub for module: heartbeat."""
from typing import Any, Dict, Optional

from __future__ import annotations
from kafka import KafkaProducer
import base64
import json
import logging
import time

# Constants
logger: Any

# Classes
class HeartbeatReporter:
    """
    Sends heartbeat messages to Kafka topic.
    """

    def __init__(self: Any, session: Any, streaming_gateway_id: str, topic: str = 'streaming_gateway_heartbeat', kafka_timeout: float = 5.0) -> None: ...
        """
        Initialize heartbeat reporter.
        
                Args:
                    session: Session object for API calls
                    streaming_gateway_id: ID of the streaming gateway
                    topic: Kafka topic to send heartbeats to (default: streaming_gateway_heartbeat)
                    kafka_timeout: Timeout for Kafka operations
        """

    def close(self: Any) -> Any: ...
        """
        Close Kafka producer.
        """

    def send_heartbeat(self: Any, camera_config: Dict[str, Any]) -> bool: ...
        """
        Send heartbeat to Kafka topic.
        
                Args:
                    camera_config: Camera configuration payload to send
        
                Returns:
                    True if successful, False otherwise
        """

