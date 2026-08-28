"""Auto-generated stub for module: analytics_publisher."""
from typing import Any, Callable, Dict, List, Optional, Set

# Classes
class AnalyticsPublisher:
    # Publishes aggregated analytics to Redis (localhost) and Kafka internal streams.
    #
    # Monitors output queue and aggregates tracking statistics over 5-minute windows.
    # Publishes to 'results-agg' topic on both Redis and Kafka.
    #
    # Output structure (zone-keyed: tracking_stats maps zone_id -> stats; the old
    # non-zone-aware flow uses the single "global" zone):
    #     tracking_stats: {
    #         "global": {
    #             "input_timestamp": "2026-06-14T06:30:00Z",                  # RFC3339 UTC event time
    #             "current_counts": [{"category": "person", "count": 2}],         # NEW people in this publish window (delta)
    #             "total_current_counts": [{"category": "person", "count": 7}],   # ALL people in frame right now
    #             "total_counts": [{"category": "person", "count": 15}]           # Cumulative unique since reset
    #         }
    #     }

    def __init__(self: Any, camera_configs: Dict[str, Any], aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, publish_interval: int = DEFAULT_PUBLISH_INTERVAL, app_deployment_id: Optional[str] = None, inference_pipeline_id: Optional[str] = None, deployment_instance_id: Optional[str] = None, app_id: Optional[str] = None, app_name: Optional[str] = None, app_version: Optional[str] = None, redis_host: str = 'localhost', redis_port: int = 6379, redis_password: Optional[str] = None, redis_username: Optional[str] = None, redis_db: int = 0, sentinel_hosts: Optional[List] = None, master_name: Optional[str] = None, kafka_bootstrap_servers: Optional[str] = None, enable_kafka: bool = False) -> None: ...

    ANALYTICS_TOPIC: str
    ANALYTICS_ZONE_GLOBAL: str
    DEFAULT_AGGREGATION_INTERVAL: int
    DEFAULT_PUBLISH_INTERVAL: int

    def enqueue_analytics_data(self: Any, task_data: Dict[str, Any]) -> None:
        """
        Enqueue analytics data from producer for processing.
        Called by ProducerWorker after sending messages.
        
        Args:
            task_data: Task data from output queue containing analytics info
        """
        ...

    def get_metrics(self: Any) -> Dict[str, Any]:
        """
        Get analytics publisher metrics.
        """
        ...

    def set_redis_config_provider(self: Any, provider: Callable[[], Optional[Dict[str, Any]]]) -> None:
        """
        Set a callback that provides fresh Redis connection config for retries.
        
                The provider should return a dict with keys:
                host, port, password, username, sentinel_hosts, master_name
        """
        ...

    def start(self: Any) -> Any.Any:
        """
        Start the analytics publisher in a separate thread.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the analytics publisher.
        """
        ...

    def update_camera_configs(self: Any, camera_configs: Dict[str, Any]) -> None:
        """
        Update camera configurations thread-safely.
        """
        ...

