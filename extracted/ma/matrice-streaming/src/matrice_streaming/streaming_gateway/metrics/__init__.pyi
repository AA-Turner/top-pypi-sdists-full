"""Stub file for streaming_gateway.metrics directory."""
from typing import Any, Dict, List, Optional

from __future__ import annotations
from collector import MetricsCollector
from config import MetricsConfig
from dataclasses import dataclass, field
from kafka import KafkaProducer
from reporter import MetricsReporter
import base64
import json
import logging
import threading
import time

# Constants
logger: Any = ...  # From heartbeat
logger: Any = ...  # From manager
logger: Any = ...  # From reporter

# Classes
# From calculator
class MetricsCalculator:
    """
    Calculate statistical metrics over time windows.
    """

    def calculate_fps(frame_count_start: int, frame_count_end: int, time_elapsed: float) -> float: ...
        """
        Calculate frames per second.
        
                Args:
                    frame_count_start: Starting frame count
                    frame_count_end: Ending frame count
                    time_elapsed: Time elapsed in seconds
        
                Returns:
                    Frames per second
        """

    def calculate_statistics(values: List[float]) -> Dict[str, float]: ...
        """
        Calculate min, max, avg, p0, p50, p100 from a list of values.
        
                Args:
                    values: List of numeric values
        
                Returns:
                    Dictionary with statistical metrics
        """


# From collector
class MetricsCollector:
    """
    Collects and aggregates streaming gateway metrics.
    """

    def __init__(self: Any, streaming_gateway: Any, config: Any) -> None: ...
        """
        Initialize metrics collector.
        
                Args:
                    streaming_gateway: StreamingGateway instance
                    config: Metrics configuration
        """

    def add_to_history(self: Any, snapshot: Dict[str, Any]) -> Any: ...
        """
        Add snapshot to rolling history window.
        
                Args:
                    snapshot: Metrics snapshot to add
        """

    def collect_snapshot(self: Any) -> Dict[str, Any]: ...
        """
        Collect current metrics snapshot from streaming gateway.
        
                Returns:
                    Dictionary containing current metrics state
        """

    def get_aggregated_metrics(self: Any) -> Optional[Dict[str, Any]]: ...
        """
        Calculate aggregated metrics from accumulated timing history.
        
                Returns:
                    Dictionary with aggregated per-camera metrics
        """


# From config
class MetricsConfig:
    """
    Configuration for metrics collection and reporting.
    """

    pass

# From heartbeat
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


# From manager
class MetricsManager:
    """
    Main orchestrator for metrics collection and reporting.
    
        This class coordinates the collection of metrics from the streaming gateway,
        calculates statistics, and reports them via Kafka.
    """

    def __init__(self: Any, streaming_gateway: Any, session: Any, streaming_gateway_id: str, action_id: Optional[str] = None, config: Optional[MetricsConfig] = None) -> None: ...
        """
        Initialize metrics manager.
        
                Args:
                    streaming_gateway: StreamingGateway instance
                    session: Session object for API calls
                    streaming_gateway_id: ID of the streaming gateway
                    action_id: Optional action ID
                    config: Optional metrics configuration (uses default if not provided)
        """

    def collect_and_report(self: Any) -> Any: ...
        """
        Collect current metrics and report if interval has elapsed.
        
                This method should be called periodically (e.g., every 1-30 seconds)
                from the health monitoring loop.
        """

    def stop(self: Any) -> Any: ...
        """
        Stop metrics collection and close resources.
        """


# From reporter
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


from . import calculator, collector, config, heartbeat, manager, reporter