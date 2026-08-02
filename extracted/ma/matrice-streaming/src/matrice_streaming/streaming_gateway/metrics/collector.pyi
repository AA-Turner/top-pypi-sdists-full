"""Auto-generated stub for module: collector."""
from typing import Any, Dict, List, Optional

from __future__ import annotations
from config import MetricsConfig
import logging
import threading
import time

# Classes
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

