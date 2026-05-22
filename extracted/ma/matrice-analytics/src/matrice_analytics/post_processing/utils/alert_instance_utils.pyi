"""Auto-generated stub for module: alert_instance_utils."""
from typing import Any, Dict, List, Optional

# Classes
class ALERT_INSTANCE:
    # Manages instant alert configurations and evaluates detection events.
    #
    # This class handles:
    # - Polling alert configs from Redis/Kafka every polling_interval seconds
    # - Maintaining in-memory alert state
    # - Evaluating detection events against alert criteria
    # - Publishing trigger messages when matches occur
    #
    # Transport Priority:
    # - Redis is primary for both config reading and trigger publishing
    # - Kafka is fallback when Redis operations fail

    def __init__(self: Any, redis_client: Optional[Any] = None, kafka_client: Optional[Any] = None, config_topic: str = 'alert_instant_config_request', trigger_topic: str = 'alert_instant_triggered', polling_interval: int = 10, logger: Optional[Any.Any] = None, app_deployment_id: Optional[str] = None) -> None:
        """
        Initialize ALERT_INSTANCE.
        
        Args:
            redis_client: MatriceStream instance configured for Redis (primary transport)
            kafka_client: MatriceStream instance configured for Kafka (fallback transport)
            config_topic: Topic/stream name for receiving alert configs
            trigger_topic: Topic/stream name for publishing triggers
            polling_interval: Seconds between config polling
            logger: Python logger instance
            app_deployment_id: App deployment ID to filter incoming alerts (only process alerts matching this ID)
        """
        ...

    def get_active_alerts_count(self: Any) -> int:
        """
        Get count of active alerts.
        """
        ...

    def get_alerts_for_camera(self: Any, camera_id: str) -> List[Dict[str, Any]]:
        """
        Get all active alerts for a camera (for debugging/monitoring).
        """
        ...

    def process_detection_event(self: Any, detection_payload: Dict[str, Any], stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process a detection event and evaluate against active alerts.
        
        Args:
            detection_payload: Detection event data
            stream_info: Stream metadata containing stream_time and other info
        """
        ...

    def start(self: Any) -> Any:
        """
        Start the background polling thread for config updates.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the background polling thread gracefully.
        """
        ...

class AlertConfig:
    # Represents an instant alert configuration.

    def from_dict(cls: Any, data: Dict[str, Any]) -> 'Any':
        """
        Create AlertConfig from dictionary.
        """
        ...

