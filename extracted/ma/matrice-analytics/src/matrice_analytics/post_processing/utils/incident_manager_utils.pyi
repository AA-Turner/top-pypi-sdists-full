"""Auto-generated stub for module: incident_manager_utils."""
from typing import Any, Dict, List, Optional, Set

# Constants
DEFAULT_THRESHOLDS: List[Any]
SEVERITY_LEVELS: List[Any]

# Functions
def get_incident_manager(config: Any, logger: Optional[Any.Any] = None) -> Optional[Any]:
    """
    Get or create INCIDENT_MANAGER instance.
    
    This is a convenience function that uses a module-level factory.
    For more control, use IncidentManagerFactory directly.
    
    Args:
        config: Configuration object with session, server_id, etc.
        logger: Logger instance
    
    Returns:
        INCIDENT_MANAGER instance or None
    """
    ...

# Classes
class INCIDENT_MANAGER:
    # Manages incident severity level tracking and publishing.
    #
    # Key behaviors:
    # - Polls 'incident_modification_config' topic for dynamic threshold settings
    # - Calculates severity_level from incident_quant using thresholds
    # - Publishes incidents ONLY when severity level changes
    # - Requires different consecutive frames based on level:
    #   - 5 frames for medium/significant/critical
    #   - 10 frames for low (stricter to avoid false positives)
    #   - 101 empty frames to send "info" (incident ended)
    # - Supports both Redis and Kafka transports
    # - Thread-safe operations
    #
    # Usage:
    #     manager = INCIDENT_MANAGER(redis_client=..., kafka_client=...)
    #     manager.start()  # Start config polling
    #     manager.process_incident(camera_id, incident_data, stream_info)
    #     manager.stop()   # Stop polling on shutdown

    def __init__(self: Any, redis_client: Optional[Any] = None, kafka_client: Optional[Any] = None, incident_topic: str = 'incident_res', config_topic: str = 'incident_modification_config', logger: Optional[Any.Any] = None) -> None:
        """
        Initialize INCIDENT_MANAGER.
        
        Args:
            redis_client: MatriceStream instance configured for Redis
            kafka_client: MatriceStream instance configured for Kafka
            incident_topic: Topic/stream name for publishing incidents
            config_topic: Topic/stream name for receiving threshold configs
            logger: Python logger instance
        """
        ...

    CONFIG_POLLING_INTERVAL: int
    CONFIG_TOPIC: str
    CONSECUTIVE_FRAMES_DEFAULT: int
    CONSECUTIVE_FRAMES_EMPTY: int
    CONSECUTIVE_FRAMES_LOW: int
    INCIDENT_TOPIC: str

    def get_all_camera_states(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get all camera states for debugging/monitoring.
        """
        ...

    def get_camera_state(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current incident state for a camera (for debugging).
        """
        ...

    def get_threshold_config(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Get threshold configuration for a camera (for debugging).
        """
        ...

    def process_incident(self: Any, camera_id: str, incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        Process an incident and publish if severity level changed.
        
        This method:
        1. Gets incident_quant from incident_data
        2. Calculates severity_level using dynamic thresholds for this camera
        3. Updates incident_data with new severity_level
        4. Tracks level changes with consecutive-frame validation:
           - 5 frames for medium/significant/critical
           - 10 frames for low (stricter)
        5. Tracks empty incidents and publishes "info" after 101 consecutive empty frames
        6. Publishes on level change
        7. Manages incident_id per camera per cycle (increments after info is sent)
        
        Args:
            camera_id: Unique camera identifier
            incident_data: Incident dictionary from usecase (must include incident_quant)
            stream_info: Stream metadata
        
        Returns:
            True if incident was published, False otherwise
        """
        ...

    def reset_camera_state(self: Any, camera_id: str) -> Any:
        """
        Reset incident state for a specific camera.
        """
        ...

    def set_factory_ref(self: Any, factory: 'Any') -> Any:
        """
        Set reference to factory for accessing deployment info.
        """
        ...

    def set_thresholds_for_camera(self: Any, camera_id: str, thresholds: List[Dict[str, Any]], application_id: str = '', app_deployment_id: str = '', incident_type: str = '', camera_name: str = '') -> Any:
        """
        Manually set thresholds for a camera (useful for testing or direct config).
        
        Args:
            camera_id: Camera identifier
            thresholds: List of threshold configs
            application_id: Application ID
            app_deployment_id: App deployment ID
            incident_type: Incident type (e.g., "fire")
            camera_name: Camera name
        """
        ...

    def start(self: Any) -> Any:
        """
        Start the background config polling thread.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the background polling thread gracefully.
        """
        ...

class IncidentManagerFactory:
    # Factory class for creating INCIDENT_MANAGER instances.
    #
    # Handles session initialization and Redis/Kafka client creation
    # following the same pattern as license_plate_monitoring.py.

    def __init__(self: Any, logger: Optional[Any.Any] = None) -> None: ...

    ACTION_ID_PATTERN: Any

    def incident_manager(self: Any) -> Optional[Any]: ...

    def initialize(self: Any, config: Any) -> Optional[Any]:
        """
        Initialize and return INCIDENT_MANAGER with Redis/Kafka clients.
        
        Args:
            config: Configuration object with session, server_id, etc.
        
        Returns:
            INCIDENT_MANAGER instance or None if initialization failed
        """
        ...

    def is_initialized(self: Any) -> bool: ...

class IncidentState:
    # Tracks the current incident state for a camera/usecase.

    ...
class ThresholdConfig:
    # Stores threshold configuration for a camera.

    ...
