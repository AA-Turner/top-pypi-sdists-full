"""Auto-generated stub for module: manager."""
from typing import Any, Dict, Optional

from __future__ import annotations
from collector import MetricsCollector
from config import MetricsConfig
from reporter import MetricsReporter
import logging
import time

# Constants
logger: Any

# Classes
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

