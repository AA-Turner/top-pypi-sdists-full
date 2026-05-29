"""Auto-generated stub for module: event_listener."""
from typing import Any, Callable, Dict, List, Optional, Union

# Constants
logger: Any

# Classes
class EventListener:
    # Generic listener for Kafka events with filtering and custom handlers.
    #
    #     This class provides a flexible event listening infrastructure that can be used
    #     for various event types (camera events, app events, etc.) from Kafka topics.
    #
    #     Example:
    #         ```python
    #         import logging
    #         logger = logging.getLogger(__name__)
    #
    #         def my_handler(event):
    #             logger.info("Received event: %s", event.get("eventType"))
    #
    #         listener = EventListener(
    #             session=session,
    #             topics=['Camera_Events_Topic', 'App_Events_Topic'],
    #             event_handler=my_handler,
    #             filter_field='streamingGatewayId',
    #             filter_value='gateway123'
    #         )
    #         listener.start()
    #         ```

    def __init__(self: Any, session: Any, topics: Union[str, List[str]], event_handler: Callable[[Dict[str, Any]], None], filter_field: Optional[str] = None, filter_value: Optional[str] = None, consumer_group_id: Optional[str] = None, offset_reset: str = 'latest', max_poll_interval_ms: int = 300000, session_timeout_ms: int = 45000, heartbeat_interval_ms: int = 15000) -> None:
        """
        Initialize event listener.
        
                Args:
                    session: Session object for authentication and API access
                    topics: List of Kafka topics to subscribe to
                    event_handler: Callback function to handle events
                    filter_field: Optional field name to filter events (e.g., 'streamingGatewayId')
                    filter_value: Optional value to match for filtering
                    consumer_group_id: Optional Kafka consumer group ID (auto-generated if not provided)
                    max_poll_interval_ms: Max delay between poll() calls before the broker
                        evicts the consumer (default: 300000). Also drives the time-based
                        staleness recreate in the listen loop.
                    session_timeout_ms: Consumer session timeout (default: 45000).
                    heartbeat_interval_ms: Consumer heartbeat interval (default: 15000).
        """
        ...

    def get_statistics(self: Any) -> dict:
        """
        Get listener statistics.
        
                Returns:
                    dict: Statistics including events received, processed, filtered, and failed
        """
        ...

    def start(self: Any) -> bool:
        """
        Start listening to events.
        
                Returns:
                    bool: True if started successfully
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop listening.
        """
        ...

