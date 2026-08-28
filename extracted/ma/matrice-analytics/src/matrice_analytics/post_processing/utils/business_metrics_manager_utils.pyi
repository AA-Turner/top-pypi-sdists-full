"""Auto-generated stub for module: business_metrics_manager_utils."""
from typing import Any, Dict, List, Optional, Set

from .location_name_cache import LocationNameCache
from .post_processing_config_client import is_null_object_id, is_resolvable_location_id
from .post_processing_config_client import is_resolvable_location_id, normalize_location_id
from .public_ip import resolve_public_ip_once

# Constants
AGGREGATION_TYPES: List[Any]
DEFAULT_AGGREGATION_INTERVAL: int
DEFAULT_METRICS_CONFIG: Dict[Any, Any]

# Functions
def get_business_metrics_manager(config: Any, logger: Optional[Any.Any] = None, aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, metrics_config: Optional[Dict[str, str]] = None) -> Optional[Any]:
    """
    Get or create BUSINESS_METRICS_MANAGER instance.
    
    This is a convenience function that uses a module-level factory.
    For more control, use BusinessMetricsManagerFactory directly.
    
    Args:
        config: Configuration object with session, server_id, etc.
        logger: Logger instance
        aggregation_interval: Interval in seconds for aggregation (default 300)
        metrics_config: Dict of metric_name -> aggregation_type
    
    Returns:
        BUSINESS_METRICS_MANAGER instance or None
    """
    ...

# Classes
class BUSINESS_METRICS_MANAGER:
    # Manages business metrics aggregation and publishing.
    #
    # Key behaviors:
    # - Aggregates business metrics for configurable interval (default 5 minutes)
    # - Publishes aggregated metrics to Redis/Kafka topic
    # - Supports multiple aggregation types (mean, min, max, sum)
    # - Resets all values after publishing
    # - Thread-safe operations
    #
    # Usage:
    #     manager = BUSINESS_METRICS_MANAGER(redis_client=..., kafka_client=...)
    #     manager.start()  # Start aggregation timer
    #     manager.process_metrics(camera_id, metrics_data, stream_info)
    #     manager.stop()   # Stop on shutdown

    def __init__(self: Any, redis_client: Optional[Any] = None, kafka_client: Optional[Any] = None, output_topic: str = 'business_metrics', aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, metrics_config: Optional[Dict[str, str]] = None, logger: Optional[Any.Any] = None) -> None:
        """
        Initialize BUSINESS_METRICS_MANAGER.
        
        Args:
            redis_client: MatriceStream instance configured for Redis
            kafka_client: MatriceStream instance configured for Kafka
            output_topic: Topic/stream name for publishing metrics
            aggregation_interval: Interval in seconds for aggregation (default 300 = 5 minutes)
            metrics_config: Dict of metric_name -> aggregation_type
            logger: Python logger instance
        """
        ...

    OUTPUT_TOPIC: str

    def force_publish_all(self: Any) -> int:
        """
        Force publish all cameras with pending metrics. Returns count published.
        """
        ...

    def get_all_camera_states(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get all camera states for debugging/monitoring.
        """
        ...

    def get_camera_state(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current metrics state for a camera (for debugging).
        """
        ...

    def process_metrics(self: Any, camera_id: str, metrics_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        Process business metrics and add to aggregation.
        
        This method:
        1. Extracts camera info from stream_info
        2. Adds each metric value to the appropriate aggregator
        3. Checks if aggregation interval has passed and publishes if so
        
        Args:
            camera_id: Unique camera identifier
            metrics_data: Business metrics dictionary from usecase
            stream_info: Stream metadata
        
        Returns:
            True if metrics were published, False otherwise
        """
        ...

    def reset_camera_state(self: Any, camera_id: str) -> Any:
        """
        Reset metrics state for a specific camera.
        """
        ...

    def set_aggregation_interval(self: Any, interval_seconds: int) -> Any:
        """
        Set the aggregation interval.
        
        Args:
            interval_seconds: New interval in seconds
        """
        ...

    def set_factory_ref(self: Any, factory: 'Any') -> Any:
        """
        Set reference to factory for accessing deployment info.
        """
        ...

    def set_metrics_config(self: Any, metrics_config: Dict[str, str]) -> Any:
        """
        Set aggregation type configuration for metrics.
        
        Args:
            metrics_config: Dict of metric_name -> aggregation_type
        """
        ...

    def start(self: Any) -> Any:
        """
        Start the background timer thread for periodic publishing.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the background timer thread gracefully.
        """
        ...

class BusinessMetricsManagerFactory:
    # Factory class for creating BUSINESS_METRICS_MANAGER instances.
    #
    # Handles session initialization and Redis/Kafka client creation
    # following the same pattern as IncidentManagerFactory.

    def __init__(self: Any, logger: Optional[Any.Any] = None) -> None: ...

    ACTION_ID_PATTERN: Any

    def business_metrics_manager(self: Any) -> Optional[Any]: ...

    def initialize(self: Any, config: Any, aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, metrics_config: Optional[Dict[str, str]] = None) -> Optional[Any]:
        """
        Initialize and return BUSINESS_METRICS_MANAGER with Redis/Kafka clients.
        
        This follows the same pattern as IncidentManagerFactory for
        session initialization and Redis/Kafka client creation.
        
        Args:
            config: Configuration object with session, server_id, etc.
            aggregation_interval: Interval in seconds for aggregation (default 300)
            metrics_config: Dict of metric_name -> aggregation_type
        
        Returns:
            BUSINESS_METRICS_MANAGER instance or None if initialization failed
        """
        ...

    def is_initialized(self: Any) -> bool: ...

class CameraMetricsState:
    # Stores metrics state for a camera.

    def add_metric_value(self: Any, metric_name: str, value: float, agg_type: str = 'mean') -> Any:
        """
        Add a value for a specific metric.
        """
        ...

    def get_aggregated_metrics(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get all aggregated metrics in output format.
        """
        ...

    def has_metrics(self: Any) -> bool:
        """
        Check if any metrics have values.
        """
        ...

    def reset_metrics(self: Any) -> Any:
        """
        Reset all metric aggregators.
        """
        ...

class MetricAggregator:
    # Stores aggregated values for a single metric.

    def add_value(self: Any, value: float) -> Any:
        """
        Add a value to the aggregator.
        """
        ...

    def get_aggregated_value(self: Any) -> Optional[float]:
        """
        Get the aggregated value based on aggregation type.
        """
        ...

    def has_values(self: Any) -> bool:
        """
        Check if aggregator has any values.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset the aggregator values.
        """
        ...

