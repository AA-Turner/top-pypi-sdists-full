"""Auto-generated stub for module: business_metrics_manager_utils."""
from typing import Any, Dict, Optional

from .business_metrics_aggregation_utils import AGGREGATION_TYPES, BUSINESS_METRICS_MANAGER, DEFAULT_AGGREGATION_INTERVAL, DEFAULT_METRICS_CONFIG, CameraMetricsState, MetricAggregator
from .public_ip import resolve_public_ip_once

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

