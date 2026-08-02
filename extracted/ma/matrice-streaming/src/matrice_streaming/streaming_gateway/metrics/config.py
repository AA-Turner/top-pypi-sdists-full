"""Metrics configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class MetricsConfig:
    """Configuration for metrics collection and reporting."""

    # Collection and reporting intervals
    collection_interval: float = 1.0  # Collect metrics every second
    reporting_interval: float = 30.0  # Report aggregated metrics every 30 seconds
    history_window: int = 30  # Keep 30 seconds of history for statistics
    log_interval: float = 300.0  # Log metrics sends every 5 minutes

    # Kafka configuration
    metrics_topic: str = "streaming_gateway_metrics"
    kafka_timeout: float = 5.0  # Timeout for Kafka operations

    # Statistics configuration
    calculate_percentiles: bool = True
    percentiles: List[int] = field(default_factory=lambda: [0, 50, 100])
